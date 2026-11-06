#!/usr/bin/env python3
"""
orchestrator.py
===============
Bộ Điều phối Đa Agent Trung tâm (Multi-Agent System Orchestrator).
Chuẩn hóa logic thực hành lâm sàng và hội thoại đa vòng (Multi-turn Chat):
- Phân biệt rõ ràng 2 trạng thái dữ liệu:
  * Trạng thái 1 (INSUFFICIENT_LABS): Chỉ có triệu chứng và thể trạng -> Chỉ sàng lọc nguy cơ và khuyến cáo xét nghiệm, KHÔNG kết luận bệnh, KHÔNG kê đơn thuốc.
  * Trạng thái 2 (SUFFICIENT_LABS): Đã có xét nghiệm định lượng -> Đánh giá chẩn đoán theo QĐ 5481/QĐ-BYT, phác đồ thuốc và tra cứu Long Châu.
- Hỗ trợ hàm hội thoại `chat_turn` để tương tác trực tiếp qua Chatbot.
"""

import os
import sys
import json
import time
from typing import Dict, Any, Optional, Tuple

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from src.core.state_schema import DiabetesMASState, PatientProfile
from src.core.gemini_client import GeminiMASClient
from src.knowledge.diabetes_kg import DiabetesKnowledgeGraph
from src.knowledge.vietnamese_guidelines_rag import VietnameseGuidelinesRAG

from src.agents.triage_interviewer_agent import TriageInterviewerAgent
from src.agents.risk_prediction_agent import RiskPredictionAgent
from src.agents.endocrinologist_agent import EndocrinologistAgent
from src.agents.nutrition_agent import NutritionAgent
from src.agents.lifestyle_coach_agent import LifestyleCoachAgent
from src.agents.pharmacy_locator_agent import PharmacyLocatorAgent
from src.agents.safety_guardian_agent import SafetyGuardianAgent


class DiabetesMASOrchestrator:
    """
    Bộ điều phối toàn diện cho hệ thống DiaAgent-MAS.
    """

    def __init__(self):
        self.gemini = GeminiMASClient()
        self.kg = DiabetesKnowledgeGraph()
        self.rag = VietnameseGuidelinesRAG()

        # Khởi tạo 7 Agents chuyên trách
        self.triage_agent = TriageInterviewerAgent(gemini_client=self.gemini)
        self.risk_agent = RiskPredictionAgent()
        self.endocrinologist_agent = EndocrinologistAgent(gemini_client=self.gemini, rag=self.rag)
        self.nutrition_agent = NutritionAgent(kg=self.kg)
        self.lifestyle_agent = LifestyleCoachAgent()
        self.pharmacy_agent = PharmacyLocatorAgent()
        self.safety_agent = SafetyGuardianAgent(kg=self.kg)

    def run_workflow(
        self,
        patient_data: Optional[Dict[str, Any]] = None,
        user_query: str = "",
        existing_state: Optional[DiabetesMASState] = None,
        max_reflections: int = 2
    ) -> DiabetesMASState:
        """
        Thực thi quy trình làm việc Đa Agent có phân luồng theo mức độ đầy đủ của dữ liệu.
        """
        state = existing_state or DiabetesMASState()

        # 1. Nạp dữ liệu cập nhật nếu có
        if patient_data:
            for k, v in patient_data.items():
                if hasattr(state.patient_profile, k) and v is not None:
                    setattr(state.patient_profile, k, v)

        # 2. Bước 1: Tiếp nhận triệu chứng qua lời nói người bệnh (Triage)
        if user_query:
            state = self.triage_agent.process_intake(user_query, state)

        # Kiểm tra trạng thái dữ liệu (đủ hay thiếu xét nghiệm)
        state.patient_profile.check_completeness()

        # 3. Bước 2: Dự báo nguy cơ thích ứng (Risk Prediction)
        state = self.risk_agent.run(state)

        # 4. Bước 3: Đưa ra nhận định chuyên môn (Endocrinologist)
        state = self.endocrinologist_agent.run(state, is_revision=False)

        # 5. Bước 4: Xây dựng chế độ dinh dưỡng & lối sống song song
        state = self.nutrition_agent.run(state)
        state = self.lifestyle_agent.run(state)

        # 6. Bước 5: Ánh xạ danh mục sản phẩm FPT Long Châu
        state = self.pharmacy_agent.run(state)

        # 7. Bước 6: Rà soát an toàn và phản biện chéo (Safety Guardian VETO & Reflection Loop)
        state = self.safety_agent.run(state)

        reflection_count = 0
        while not state.safety_check.passed and reflection_count < max_reflections:
            reflection_count += 1
            # Bác sĩ Nội tiết sửa đổi phác đồ an toàn
            state = self.endocrinologist_agent.run(state, is_revision=True)
            # Cập nhật lại sản phẩm Long Châu
            state = self.pharmacy_agent.run(state)
            # Kiểm tra lại an toàn
            state = self.safety_agent.run(state)

        # 8. Bước 7: Tổng hợp bản tư vấn súc tích, tự nhiên
        state = self._synthesize_final_report(state)

        return state

    def _synthesize_final_report(self, state: DiabetesMASState) -> DiabetesMASState:
        """
        Sử dụng Gemini API tổng hợp kết quả tư vấn phân nhánh chuẩn mực:
        - Nhánh 1: Thiếu xét nghiệm -> Khuyến cáo tầm soát, khuyên đi xét nghiệm, hướng dẫn ăn uống, KHÔNG khẳng định bệnh.
        - Nhánh 2: Đủ xét nghiệm -> Đánh giá chẩn đoán theo ngưỡng Bộ Y Tế, phác đồ thuốc, giá Long Châu.
        """
        p = state.patient_profile
        ml = state.ml_prediction
        rx = state.clinical_prescription
        nutri = state.nutrition_recommendation
        life = state.lifestyle_recommendation
        safety = state.safety_check

        # TRƯỜNG HỢP 1: THIẾU CHỈ SỐ XÉT NGHIỆM ĐỊNH LƯỢNG
        if p.data_completeness == "INSUFFICIENT_LABS":
            prompt = f"""
Hãy đưa ra bản tư vấn y tế ngắn gọn, ân cần và thực tế cho một người bệnh CHƯA CÓ KẾT QUẢ XÉT NGHIỆM MÁU:

- Thông tin người bệnh: {p.age} tuổi, Giới tính: {p.gender}, Thể trạng BMI: {p.bmi or 'Chưa rõ'} kg/m²
- Triệu chứng người bệnh chia sẻ: {p.chief_complaint or 'Có dấu hiệu nghi ngờ'}
- Phân tầng nguy cơ sàng lọc lâm sàng: {ml.risk_tier} ({ml.risk_score_points} điểm theo thang điểm sàng lọc không xâm lấn)
- Hướng dẫn xét nghiệm cần làm: {', '.join(rx.diagnostic_workup_needed)}
- Dinh dưỡng ban đầu: Nhu cầu ~{nutri.daily_calories} kcal/ngày, hạn chế cơm trắng, kiêng nước ngọt có ga
- Vận động: 150 phút/tuần (đi bộ nhanh 30 phút/ngày)

Yêu cầu định dạng:
1. Xưng hô tự nhiên, lịch sự (dùng 'bạn').
2. Trình bày rõ ràng 3 phần:
   - Đánh giá nguy cơ sơ bộ (NÓI RÕ: Căn cứ vào triệu chứng và thể trạng, bạn thuộc diện nguy cơ {ml.risk_tier}. TUYỆT ĐỐI CHƯA THỂ KẾT LUẬN có bị đái tháo đường hay không vì bắt buộc phải có xét nghiệm máu).
   - Hướng dẫn xét nghiệm cần làm tại cơ sở y tế (Đo đường huyết lúc đói FPG và chỉ số HbA1c).
   - Lời khuyên ăn uống và sinh hoạt tạm thời trong thời gian chờ đi khám.
3. Nhắc nhở người bệnh KHÔNG tự ý mua bất kỳ loại thuốc hạ đường huyết nào để uống khi chưa có kết quả xét nghiệm và đơn của bác sĩ.
4. Không dùng ký hiệu LaTeX toán học.
"""
        # TRƯỜNG HỢP 2: ĐÃ CÓ KẾT QUẢ XÉT NGHIỆM MÁU
        else:
            prompt = f"""
Hãy đưa ra bản tư vấn y tế ngắn gọn, súc tích và thực tế cho người bệnh ĐÃ CÓ KẾT QUẢ XÉT NGHIỆM MÁU:

- Người bệnh: {p.age} tuổi, Giới tính: {p.gender}, BMI: {p.bmi} kg/m²
- Chỉ số xét nghiệm: HbA1c {p.hba1c}%, Đường huyết lúc đói {p.blood_glucose_level} mg/dL, Chức năng thận eGFR {p.egfr} mL/min
- Kết quả mô hình dự báo: Xác suất nguy cơ {round(ml.risk_probability*100, 1)}% ({ml.risk_tier})
- Nhận định chuyên môn: {rx.diagnosis} (Mục tiêu điều trị: HbA1c {rx.target_hba1c})
- Phác đồ thuốc khuyến nghị ban đầu: {rx.primary_drug or 'Chưa cần dùng thuốc'} ({rx.primary_dose or ''})
- Thuốc phối hợp (nếu có): {rx.add_on_drug or 'Không'}
- Dược phẩm tham khảo tại FPT Long Châu: Ước tính chi phí ~{state.total_monthly_pharmacy_cost_vnd:,} VNĐ/tháng
- Dinh dưỡng: Nhu cầu ~{nutri.daily_calories} kcal/ngày, giảm cơm trắng, ưu tiên gạo lứt/khoai lang luộc
- Vận động: 150 phút/tuần, lưu ý quy tắc 15-15 xử trí hạ đường huyết

Yêu cầu định dạng:
1. Xưng hô tự nhiên, lịch sự (dùng 'bạn').
2. Trình bày ngắn gọn theo 3 ý chính:
   - Nhận định chỉ số xét nghiệm đối chiếu tiêu chuẩn Bộ Y Tế và mục tiêu đường huyết cần đạt.
   - Hướng dẫn dùng thuốc và lưu ý thuốc kê đơn (Rx) bắt buộc cần có đơn chính thức từ bác sĩ chuyên khoa khi mua tại hiệu thuốc.
   - Chế độ ăn uống (giảm tinh bột nhanh) và tập luyện thể chất.
3. Không dùng ký hiệu LaTeX toán học.
"""

        sys_ins = "Bạn là Trợ lý AI Tư vấn Sức khỏe Đái tháo đường theo hướng dẫn của Bộ Y Tế. Văn phong chuẩn mực, súc tích, thực tế, nói thẳng vào vấn đề."
        try:
            report = self.gemini.generate_response(prompt, system_instruction=sys_ins, temperature=0.2)
            state.final_patient_summary = report
        except Exception:
            if p.data_completeness == "INSUFFICIENT_LABS":
                state.final_patient_summary = (
                    f"TƯ VẤN SÀNG LỌC NGUY CƠ:\n"
                    f"- Mức độ nguy cơ: {ml.risk_tier} (Dựa trên thể trạng và các triệu chứng bạn chia sẻ).\n"
                    f"- Lưu ý quan trọng: Chưa thể kết luận bạn có bị đái tháo đường hay không vì bắt buộc phải có xét nghiệm máu.\n"
                    f"- Việc cần làm: Bạn nên đến cơ sở y tế gần nhất làm xét nghiệm đường huyết lúc đói (FPG) và chỉ số HbA1c.\n"
                    f"- Chế độ sinh hoạt tạm thời: Hạn chế cơm trắng, không uống nước ngọt có ga, ăn nhiều rau xanh và đi bộ 30 phút mỗi ngày."
                )
            else:
                state.final_patient_summary = (
                    f"TƯ VẤN SỨC KHỎE ĐÁI THÁO ĐƯỜNG:\n"
                    f"- Nhận định: {rx.diagnosis} (Mục tiêu: HbA1c {rx.target_hba1c})\n"
                    f"- Thuốc khuyến nghị: {rx.primary_drug} ({rx.primary_dose})\n"
                    f"- Chi phí tham khảo tại Long Châu: ~{state.total_monthly_pharmacy_cost_vnd:,} VNĐ/tháng (Lưu ý cần đơn bác sĩ)\n"
                    f"- Chế độ ăn: Giảm cơm trắng, thay bằng gạo lứt/khoai lang, ăn nhiều rau xanh."
                )

        return state

    def is_greeting(self, text: str) -> bool:
        """Nhận diện lời chào thông qua Gemini Triage Agent."""
        extracted = self.triage_agent.extract_entities_with_llm(text)
        return extracted.get("intent") == "GREETING"

    def chat_turn(self, user_message: str, state: DiabetesMASState) -> Tuple[str, DiabetesMASState]:
        """
        Xử lý hội thoại tự nhiên tương tác từng lượt qua Chatbot:
        - Tiếp nhận ngữ nghĩa thông minh qua Gemini Triage Agent
        - Chạy workflow Đa Agent đồng bộ và tổng hợp tư vấn y khoa
        """
        # 1. Cập nhật vào lịch sử trò chuyện
        state.chat_history.append({"role": "user", "content": user_message})

        # 2. Tiếp nhận qua Gemini Triage Agent
        state = self.triage_agent.process_intake(user_message, state)

        # 3. Xử lý lời chào xã giao ban đầu (được nhận diện bởi Gemini LLM)
        if state.metadata.get("last_intent") == "GREETING":
            reply = (
                "Chào bạn! Tôi là DiaAgent, Trợ lý AI tư vấn và quản lý bệnh lý đái tháo đường "
                "theo phác đồ chuẩn của Bộ Y Tế Việt Nam.\n\n"
                "Tôi có thể đồng hành và hỗ trợ bạn:\n"
                "- **Sàng lọc nguy cơ:** Phân tích thể trạng (tự tính chỉ số BMI từ chiều cao, cân nặng) "
                "và các triệu chứng cảnh báo (hay khát nước, tiểu nhiều, sụt cân, mệt mỏi...).\n"
                "- **Đánh giá xét nghiệm:** Đối chiếu chỉ số đường huyết lúc đói (FPG), HbA1c và chức năng thận (eGFR) theo chuẩn QĐ 5481/QĐ-BYT.\n"
                "- **Dinh dưỡng & Lối sống:** Thiết kế thực đơn bữa ăn Việt Nam (NIN), đĩa ăn chuẩn và kế hoạch vận động an toàn.\n"
                "- **Tra cứu dược phẩm Long Châu:** Tham khảo sản phẩm, máy đo đường huyết chính hãng và dự toán chi phí dùng thuốc.\n\n"
                "Bạn hãy chia sẻ thể trạng (chiều cao, cân nặng), các triệu chứng bạn đang gặp phải hoặc kết quả xét nghiệm (nếu có) "
                "để tôi bắt đầu phân tích giúp bạn nhé!"
            )
            state.chat_history.append({"role": "assistant", "content": reply})
            return reply, state

        # 4. Chạy workflow cập nhật phác đồ, dinh dưỡng, dược phẩm và phản biện an toàn
        state = self.run_workflow(user_query=user_message, existing_state=state)

        # 5. Sử dụng bản tư vấn tổng hợp chuẩn y tế làm câu trả lời trong hội thoại
        reply = state.final_patient_summary
        state.chat_history.append({"role": "assistant", "content": reply})

        return reply, state


if __name__ == "__main__":
    orchestrator = DiabetesMASOrchestrator()

    print("\n" + "="*70)
    print("TEST CASE 1: Bệnh nhân CHỈ CÓ TRIỆU CHỨNG, CHƯA CÓ XÉT NGHIỆM MÁU")
    print("="*70)
    user_msg_1 = "Dạo này tôi 55 tuổi, cao 1m65, nặng 74kg, hay khát nước và sụt 2kg. Tôi có bị tiểu đường không?"
    state1 = orchestrator.run_workflow(user_query=user_msg_1)
    print(f"-> Mức độ dữ liệu: {state1.patient_profile.data_completeness}")
    print(f"-> Chế độ ML: {state1.ml_prediction.mode} ({state1.ml_prediction.risk_tier})")
    print(f"-> Kết luận lâm sàng: {state1.clinical_prescription.diagnosis}")
    print(f"-> Thuốc điều trị: {state1.clinical_prescription.primary_drug}")
    print(f"-> Xét nghiệm cần làm: {state1.clinical_prescription.diagnostic_workup_needed}")
    print(f"-> Số sản phẩm Long Châu: {len(state1.pharmacy_items)} (Đơn thuốc: {state1.total_monthly_pharmacy_cost_vnd}đ/tháng)")
    print(f"-> Safety Check: {state1.safety_check.status}")
    print("\n--- BẢN TƯ VẤN SÀNG LỌC ---")
    print(state1.final_patient_summary)

    print("\n" + "="*70)
    print("TEST CASE 2: Bệnh nhân ĐÃ CÓ XÉT NGHIỆM (HbA1c = 7.8%, Glucose = 155 mg/dL)")
    print("="*70)
    user_msg_2 = "Tôi có xét nghiệm HbA1c 7.8% và đường huyết lúc đói 155 mg/dL, xin phác đồ thuốc và ăn uống."
    state2 = orchestrator.run_workflow(patient_data={"age": 55, "bmi": 27.2, "hba1c": 7.8, "blood_glucose_level": 155.0, "egfr": 75.0}, user_query=user_msg_2)
    print(f"-> Mức độ dữ liệu: {state2.patient_profile.data_completeness}")
    print(f"-> Chế độ ML: {state2.ml_prediction.mode} (Xác suất: {state2.ml_prediction.risk_probability*100:.1f}%)")
    print(f"-> Chẩn đoán xác định: {state2.clinical_prescription.diagnosis}")
    print(f"-> Thuốc chỉ định: {state2.clinical_prescription.primary_drug} ({state2.clinical_prescription.primary_dose})")
    print(f"-> Chi phí thuốc tại Long Châu: {state2.total_monthly_pharmacy_cost_vnd:,} VNĐ/tháng")
    print(f"-> Safety Check: {state2.safety_check.status}")
