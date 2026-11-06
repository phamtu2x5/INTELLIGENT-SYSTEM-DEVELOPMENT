#!/usr/bin/env python3
"""
triage_interviewer_agent.py
===========================
Agent Tiếp đón, Phân luồng và Phỏng vấn Lâm sàng (Triage & Intake Interviewer Agent).
Sử dụng mô hình ngôn ngữ lớn Gemini trích xuất thực thể y khoa (Clinical Named Entity Extraction - JSON mode):
- Loại bỏ hoàn toàn regex cứng nhắc, dễ sai sót khi gặp phủ định, dấu ngoặc hay văn phong tự nhiên.
- Tự động hiểu ngữ nghĩa: Intent (Chào hỏi / Tư vấn y tế), Thể trạng, Triệu chứng, Chỉ số xét nghiệm.
- Hiểu chính xác ngữ cảnh phủ định (ví dụ: "không uống rượu bia" -> alcohol_use = false, "không bị huyết áp" -> hypertension = false).
"""

import json
from typing import Dict, Any, Optional, List

from src.core.state_schema import DiabetesMASState, PatientProfile
from src.core.gemini_client import GeminiMASClient


class TriageInterviewerAgent:
    """
    Agent tiếp đón thông minh sử dụng Gemini để bóc tách thực thể y tế chính xác từ tiếng Việt.
    """

    def __init__(self, gemini_client: Optional[GeminiMASClient] = None):
        self.gemini = gemini_client or GeminiMASClient()

    def extract_entities_with_llm(self, user_text: str) -> Dict[str, Any]:
        """
        Sử dụng Gemini API trích xuất thực thể có cấu trúc định dạng JSON.
        """
        prompt = f"""Bạn là chuyên gia trích xuất thực thể y tế lâm sàng (Clinical Named Entity Extraction).
Phân tích câu nói của người bệnh và trả về DUY NHẤT một chuỗi JSON hợp lệ theo đúng cấu trúc sau:
{{
  "intent": "GREETING" hoặc "MEDICAL_CONSULTATION",
  "age": null hoặc số nguyên,
  "height_cm": null hoặc số thực (cm, ví dụ: 1m65 -> 165.0, mét rưỡi -> 150.0),
  "weight_kg": null hoặc số thực (kg cân nặng hiện tại),
  "hba1c": null hoặc số thực (% chỉ số xét nghiệm HbA1c, ví dụ 7.8),
  "blood_glucose_level": null hoặc số thực (mg/dL đường huyết đói; nếu bệnh nhân dùng mmol/L hãy tự nhân 18 quy đổi sang mg/dL, ví dụ 8.5 mmol/L -> 153.0),
  "egfr": null hoặc số thực (mL/min chỉ số lọc cầu thận eGFR),
  "symptoms": ["danh sách triệu chứng cơ năng người bệnh kể, ví dụ: khát nước, tiểu nhiều, tiểu đêm, sụt cân, mệt mỏi, mắt mờ, tê bì..."],
  "hypertension": true hoặc false hoặc null (chú ý ngữ cảnh phủ định: "không bị huyết áp" -> false),
  "heart_disease": true hoặc false hoặc null (chú ý ngữ cảnh phủ định: "không bị tim" -> false),
  "alcohol_use": true hoặc false hoặc null (chú ý ngữ cảnh phủ định: "không uống rượu bia" -> false)
}}

Quy tắc phân loại Intent:
- Nếu người dùng chỉ gửi lời chào (như "xin chào", "chào bạn", "hello", "hi") hoặc câu hỏi chung chung về trợ lý -> intent là "GREETING".
- Nếu người dùng cung cấp thông tin sức khỏe, thể trạng, triệu chứng hoặc hỏi về bệnh -> intent là "MEDICAL_CONSULTATION".

Câu nói của người bệnh:
"{user_text}"
"""
        try:
            resp = self.gemini.generate_response(prompt, temperature=0.1, response_json=True)
            data = json.loads(resp)
            return data
        except Exception as e:
            # Dự phòng an toàn nếu mất mạng
            return {"intent": "MEDICAL_CONSULTATION", "symptoms": []}

    def process_intake(self, user_text: str, state: DiabetesMASState) -> DiabetesMASState:
        """
        Xử lý thông tin người dùng nhập qua hội thoại tự nhiên bằng mô hình LLM ngữ nghĩa.
        """
        p = state.patient_profile
        p.chief_complaint = user_text

        # 1. Gọi Gemini trích xuất ngữ nghĩa và thực thể y khoa
        extracted = self.extract_entities_with_llm(user_text)

        # Lưu intent vào metadata để Orchestrator điều hướng
        state.metadata["last_intent"] = extracted.get("intent", "MEDICAL_CONSULTATION")

        # Nếu là lời chào, không cần ép trích xuất dữ liệu lâm sàng
        if extracted.get("intent") == "GREETING":
            state.agent_execution_logs.append({
                "agent": "TriageInterviewerAgent",
                "status": "GREETING_DETECTED",
                "message": "Phát hiện lời chào xã giao ban đầu -> Điều hướng phản hồi thân thiện."
            })
            return state

        # 2. Cập nhật thông tin thể trạng
        if extracted.get("age") is not None:
            p.age = int(extracted["age"])
        if extracted.get("height_cm") is not None:
            p.height_cm = float(extracted["height_cm"])
        if extracted.get("weight_kg") is not None:
            p.weight_kg = float(extracted["weight_kg"])

        p.compute_bmi()

        # 3. Cập nhật chỉ số cận lâm sàng
        if extracted.get("hba1c") is not None:
            p.hba1c = float(extracted["hba1c"])
        if extracted.get("blood_glucose_level") is not None:
            p.blood_glucose_level = float(extracted["blood_glucose_level"])
        if extracted.get("egfr") is not None:
            p.egfr = float(extracted["egfr"])

        # 4. Tích lũy triệu chứng qua các lượt hội thoại (không ghi đè thành rỗng)
        new_symptoms = extracted.get("symptoms", [])
        for sym in new_symptoms:
            if sym not in p.reported_symptoms:
                p.reported_symptoms.append(sym)

        # 5. Tiền sử bệnh lý (chính xác theo ngữ cảnh khẳng định / phủ định của LLM)
        if extracted.get("hypertension") is not None:
            p.hypertension = 1 if extracted["hypertension"] else 0
        if extracted.get("heart_disease") is not None:
            p.heart_disease = 1 if extracted["heart_disease"] else 0
        if extracted.get("alcohol_use") is not None:
            p.alcohol_use = bool(extracted["alcohol_use"])

        # 6. Kiểm tra mức độ đầy đủ của dữ liệu
        completeness = p.check_completeness()

        state.agent_execution_logs.append({
            "agent": "TriageInterviewerAgent",
            "status": "LLM_INTAKE_SUCCESS",
            "message": f"Dữ liệu: {completeness} | Tuổi: {p.age}, BMI: {p.bmi or 'Chưa rõ'}, Xét nghiệm: HbA1c={p.hba1c}, FPG={p.blood_glucose_level}"
        })

        return state
