#!/usr/bin/env python3
"""
nutrition_agent.py
==================
Agent Chuyên gia Dinh dưỡng Lâm sàng Việt Nam (Clinical Nutritionist Agent).
Thiết kế thực đơn cá nhân hóa phù hợp ẩm thực Việt Nam (Cơm, Phở, Bún, Khoai lang),
kiểm soát chỉ số đường huyết (GI/GL) theo khuyến nghị Viện Dinh Dưỡng Quốc Gia (NIN).
"""

from typing import Dict, Any, Optional

from src.core.state_schema import DiabetesMASState, NutritionRecommendation
from src.knowledge.diabetes_kg import DiabetesKnowledgeGraph
from src.knowledge.neo4j_kg_service import neo4j_service


class NutritionAgent:
    """
    Agent tính toán nhu cầu năng lượng hàng ngày dựa trên BMI và xây dựng
    kế hoạch bữa ăn chi tiết theo đĩa thức ăn (1/2 rau - 1/4 đạm - 1/4 tinh bột).
    """

    def __init__(self, kg: Optional[DiabetesKnowledgeGraph] = None):
        self.kg = kg or DiabetesKnowledgeGraph()

    def run(self, state: DiabetesMASState) -> DiabetesMASState:
        p = state.patient_profile

        # 1. Tính toán nhu cầu năng lượng (Calo/ngày)
        # Bệnh nhân thừa cân/béo phì (BMI >= 23): giảm 300-500 kcal
        bmi = p.bmi if p.bmi is not None else p.compute_bmi()
        if bmi is not None and bmi >= 25.0:
            daily_kcal = 1500
        elif bmi is not None and bmi >= 23.0:
            daily_kcal = 1600
        else:
            daily_kcal = 1800  # Mức chuẩn cho người thể trạng bình thường hoặc chưa rõ BMI

        # 2. Xây dựng thực đơn bữa ăn Việt Nam chuẩn y khoa
        breakfast = "1 củ khoai lang luộc vừa (100g) + 1 quả trứng gà luộc + 1 ly sữa hạt không đường hoặc đậu nành nguyên chất."
        lunch = (
            "1/2 bát cơm gạo lứt (hoặc 1/2 bát cơm trắng) + 1 đĩa lớn rau muống/cải luộc (ăn rau trước) "
            "+ 100g ức gà hấp nấm hoặc cá lóc nấu canh chua ít ngọt."
        )
        dinner = (
            "1 bát canh bí đao sườn nạc + 100g đậu phụ nhồi thịt nạc sốt cà chua ít muối "
            "+ 1 đĩa dưa chuột thái lát. Giảm tối đa tinh bột bữa tối."
        )
        snacks = "1 hũ sữa chua không đường hoặc 5-7 hạt óc chó/hạnh nhân (khi thấy đói nhẹ giữa chiều)."

        # ---------------------------------------------------------------------
        # TRUY XUẤT NEO4J GRAPH-RAG: Đề xuất hoán đổi thực phẩm chỉ số GI thấp (NIN)
        # Mục đích:
        #   - Gửi truy vấn Cypher tới CSDL Neo4j:
        #       MATCH (f1:Food)-[r:CAN_BE_REPLACED_BY]->(f2:Food)
        #       RETURN f1.name, f1.gi, f2.name, f2.gi, r.reason
        #   - Khai thác quan hệ [:CAN_BE_REPLACED_BY] đã được mã hóa theo khuyến nghị
        #     của Viện Dinh Dưỡng Quốc Gia (NIN).
        #   - Tự động thay thế món ăn Việt Nam có GI cao (Cơm trắng, Bún, Trà sữa)
        #     bằng món có GI thấp (Gạo lứt, Khoai lang luộc, Trà xanh) giúp ổn định đường huyết.
        # ---------------------------------------------------------------------
        swaps = []
        if neo4j_service.is_connected():
            neo_swaps = neo4j_service.query_food_swaps("")
            for row in neo_swaps[:3]:
                swaps.append({
                    "avoid": f"{row.get('original')} (GI: {row.get('original_gi')})",
                    "swap_to": f"{row.get('replacement')} (GI: {row.get('replacement_gi')})",
                    "benefit": row.get('rationale', 'Kiểm soát chỉ số đường huyết sau ăn')
                })

        if not swaps:
            swaps = [
                {"avoid": "Cơm trắng (GI: 83 - Cao)", "swap_to": "Cơm gạo lứt (GI: 55) hoặc Khoai lang luộc (GI: 48)", "benefit": "Giảm đỉnh đường huyết sau ăn, no lâu"},
                {"avoid": "Trà sữa / Nước ngọt có ga (GI: 88)", "swap_to": "Trà xanh nguyên chất hoặc Nước lọc có vài giọt chanh", "benefit": "Không nạp calo rỗng và đường tự do"},
                {"avoid": "Bánh mì pate nhiều mỡ (GI: 75)", "swap_to": "Bánh mì nguyên cám kẹp ức gà dưa chuột", "benefit": "Tăng chất xơ hòa tan, hạ mỡ máu"}
            ]

        high_gi = [
            "Cơm trắng gạo dẻo", "Xôi nếp", "Bánh mì trắng", 
            "Bún/Phở húp cạn nước béo", "Nước ngọt có ga", "Chè ngọt"
        ]

        nutri_rec = NutritionRecommendation(
            daily_calories=daily_kcal,
            macronutrient_ratio="Tinh bột chuyển hóa chậm 50% - Đạm nạc 20% - Chất béo tốt 30%",
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
            snacks=snacks,
            high_gi_foods_to_avoid=high_gi,
            healthy_swaps=swaps
        )

        state.nutrition_recommendation = nutri_rec
        state.agent_execution_logs.append({
            "agent": "NutritionAgent",
            "status": "SUCCESS",
            "message": f"Nhu cầu năng lượng: {daily_kcal} kcal/ngày | Đĩa thức ăn chuẩn NIN"
        })

        return state
