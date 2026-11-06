#!/usr/bin/env python3
"""
lifestyle_coach_agent.py
========================
Agent Huấn luyện viên Lối sống & Thể chất (Lifestyle & Physical Activity Coach).
Thiết lập kế hoạch vận động FITT, phác đồ chăm sóc bàn chân và quy tắc 15-15 cấp cứu hạ đường huyết.
"""

from typing import Dict, Any, Optional

from src.core.state_schema import DiabetesMASState, LifestyleRecommendation


class LifestyleCoachAgent:
    """
    Agent chuyên trách hướng dẫn hoạt động thể lực phù hợp với độ tuổi và thể trạng,
    phòng ngừa biến chứng thần kinh mạch máu ngoại biên.
    """

    def run(self, state: DiabetesMASState) -> DiabetesMASState:
        p = state.patient_profile

        # Điều chỉnh cường độ theo độ tuổi và bệnh tim mạch
        if p.heart_disease == 1 or (p.age is not None and p.age >= 65):
            aerobic_plan = "Đi bộ nhẹ nhàng 20-30 phút mỗi ngày trên địa hình phẳng, chia làm 2 lần sáng và chiều, không gắng sức quá mức."
            resistance_plan = "Bài tập co duỗi chân tay tại chỗ, hít thở sâu, tập dưỡng sinh 15 phút mỗi sáng."
        else:
            aerobic_plan = "Đi bộ nhanh, đạp xe hoặc bơi lội 30 phút/ngày, tối thiểu 5 ngày/tuần (tổng 150 phút/tuần), đạt nhịp tim 50-70% tối đa."
            resistance_plan = "Squat có ghế đỡ hoặc tạ tay nhẹ 1-2kg x 2-3 buổi/tuần để tăng khối cơ bắp và độ nhạy insulin."

        foot_care = [
            "Kiểm tra lòng bàn chân và các kẽ ngón chân mỗi tối trước khi đi ngủ xem có vết xước, nốt phồng rộp hay đổi màu không.",
            "Rửa chân bằng nước ấm (kiểm tra nhiệt độ nước bằng mu bàn tay, không dùng nước quá nóng), lau khô kỹ bằng khăn mềm sạch.",
            "Tuyệt đối không đi chân đất ngay cả trong nhà; luôn mang dép mềm và kiểm tra dị vật trong giày trước khi xỏ.",
            "Cắt móng chân thẳng ngang, không khoét sâu vào hai bên khóe móng tránh viêm mủ."
        ]

        hypo_rule = (
            "QUY TẮC 15-15: Khi có dấu hiệu run tay, vã mồ hôi lạnh, tim đập nhanh hồi hộp: "
            "1. Uống ngay 1/2 cốc nước hoa quả ngọt (120ml) hoặc ăn 3 viên kẹo ngọt / 1 thìa đường. "
            "2. Nghỉ ngơi tại chỗ 15 phút và đo lại đường huyết. "
            "3. Nếu vẫn dưới 70 mg/dL: lặp lại 15g đường và liên hệ cơ sở y tế gần nhất."
        )

        lifestyle_rec = LifestyleRecommendation(
            fitt_aerobic=aerobic_plan,
            fitt_resistance=resistance_plan,
            foot_care_rules=foot_care,
            hypoglycemia_protocol=hypo_rule
        )

        state.lifestyle_recommendation = lifestyle_rec
        state.agent_execution_logs.append({
            "agent": "LifestyleCoachAgent",
            "status": "SUCCESS",
            "message": f"Phác đồ FITT: {aerobic_plan[:60]}... | Kèm chăm sóc bàn chân & Quy tắc 15-15"
        })

        return state
