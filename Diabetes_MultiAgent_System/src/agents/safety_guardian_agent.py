#!/usr/bin/env python3
"""
safety_guardian_agent.py
========================
Agent Người Giám sát An toàn Y khoa & Dược lý (Medical Safety Guardian Agent).
Thực hiện phản biện đa Agent (Adversarial Multi-Agent Cross-Examination):
1. Rà soát chống chỉ định thuốc hạ đường huyết khi chưa có xét nghiệm xác định.
2. Rà soát chống chỉ định tuyệt đối theo Đồ thị Tri thức (KG): Suy thận eGFR < 30, Rượu bia, Suy tim.
3. Kích hoạt quyền VETO (phủ quyết) và yêu cầu chu trình phản biện (Reflection Loop) sửa đổi nếu vi phạm.
"""

from typing import Dict, Any, List, Optional

from src.core.state_schema import DiabetesMASState, SafetyCheckResult
from src.knowledge.diabetes_kg import DiabetesKnowledgeGraph
from src.knowledge.neo4j_kg_service import neo4j_service


class SafetyGuardianAgent:
    """
    Agent độc lập có quyền VETO (phủ quyết) phác đồ điều trị nếu phát hiện rủi ro y khoa
    đe dọa tính mạng hoặc vi phạm quy chế kê đơn của Bộ Y Tế.
    """

    def __init__(self, kg: Optional[DiabetesKnowledgeGraph] = None):
        self.kg = kg or DiabetesKnowledgeGraph()

    def run(self, state: DiabetesMASState) -> DiabetesMASState:
        p = state.patient_profile
        rx = state.clinical_prescription
        critical_violations = []
        caution_notes = []

        # =====================================================================
        # LUẬT AN TOÀN 1: KHÔNG ĐƯỢC PHÉP KÊ ĐƠN KHI THIẾU XÉT NGHIỆM XÁC ĐỊNH
        # =====================================================================
        if p.data_completeness == "INSUFFICIENT_LABS":
            if rx.primary_drug is not None or rx.has_confirmed_diabetes:
                critical_violations.append(
                    "[An toàn Kê đơn] Vi phạm y đức và quy chế Bộ Y Tế: Tuyệt đối không được phép chỉ định thuốc hạ đường huyết kê đơn (Rx) hoặc khẳng định bệnh khi chưa có kết quả xét nghiệm định lượng sinh hóa (FPG/HbA1c)."
                )

        # =====================================================================
        # LUẬT AN TOÀN 2: ĐỐI CHIẾU CHỐNG CHỈ ĐỊNH DƯỢC LÝ VỚI KNOWLEDGE GRAPH (NEO4J)
        # =====================================================================
        prescribed_drugs = []
        if rx.primary_drug:
            prescribed_drugs.append(rx.primary_drug)
        if rx.add_on_drug:
            prescribed_drugs.append(rx.add_on_drug)

        if prescribed_drugs:
            # -----------------------------------------------------------------
            # TRUY XUẤT NEO4J GRAPH-RAG: Rà soát chống chỉ định dược lý thời gian thực
            # Mục đích:
            #   - Truy vấn CSDL Đồ thị Neo4j qua giao thức Bolt (port 7687) bằng ngôn ngữ Cypher.
            #   - Khai thác 2 mối quan hệ an toàn y khoa:
            #       1. (:Drug)-[:RISK_OF]->(:AdverseEffect) (Metformin + Rượu bia -> Nhiễm toan Lactic)
            #       2. (:Drug)-[:CONTRAINDICATED_IN]->(:Complication) (Metformin + Suy thận eGFR < 30)
            #   - Nếu phát hiện vi phạm FATAL, kích hoạt quyền phủ quyết (VETO) để bảo vệ tính mạng người bệnh.
            # -----------------------------------------------------------------
            if neo4j_service.is_connected():
                for d in prescribed_drugs:
                    neo_alerts = neo4j_service.query_safety_contraindications(
                        drug_name=d,
                        has_alcohol=p.alcohol_use,
                        egfr_value=p.egfr
                    )
                    for na in neo_alerts:
                        if na["level"] == "FATAL":
                            critical_violations.append(f"[Neo4j Cypher Live] {na['title']}: {na['message']}")
                        else:
                            caution_notes.append(f"[Neo4j Cypher Live] {na['title']}: {na['message']}")

            # -----------------------------------------------------------------
            # TRUY XUẤT ĐỒ THỊ ĐỒNG BỘ (Fallback & Multi-Hop Validation):
            # Rà soát đa điều kiện trên 143 nodes và 271 liên kết đã sync từ Neo4j
            # -----------------------------------------------------------------
            kg_alerts = self.kg.check_contraindications(
                drugs=prescribed_drugs,
                patient_egfr=p.egfr,
                has_heavy_alcohol=p.alcohol_use,
                has_heart_failure=(p.heart_disease == 1),
                has_liver_disease=p.liver_disease,
                age=p.age
            )

            for alert in kg_alerts:
                sev = alert.get("severity")
                msg = f"[{alert.get('drug')}] {alert.get('violation')} (Hành động: {alert.get('recommended_action')})"
                if sev == "CRITICAL_BLOCKED":
                    critical_violations.append(msg)
                elif sev in ["WARNING_CAUTION", "WARNING_ADJUST_DOSE"]:
                    caution_notes.append(msg)

        passed = len(critical_violations) == 0
        new_status = "APPROVED" if passed else "REJECTED_NEEDS_REVISION"

        safety_res = SafetyCheckResult(
            status=new_status,
            passed=passed,
            critical_alerts=critical_violations,
            caution_notes=caution_notes,
            revision_iteration=state.safety_check.revision_iteration + (1 if not passed else 0)
        )

        state.safety_check = safety_res
        state.agent_execution_logs.append({
            "agent": "SafetyGuardianAgent",
            "status": "PASSED" if passed else "VETO_REJECTED",
            "message": "Phác đồ an toàn được phê duyệt (APPROVED)" if passed else f"PHỦ QUYẾT: Phát hiện {len(critical_violations)} vi phạm nghiêm trọng! Kích hoạt phản hồi sửa đổi."
        })

        return state
