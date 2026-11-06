#!/usr/bin/env python3
"""
endocrinologist_agent.py
========================
Agent Bác sĩ Nội tiết Lâm sàng (Endocrinologist Clinical Agent).
Chuẩn hóa logic chẩn đoán theo QĐ 5481/QĐ-BYT:
- Khi THIẾU xét nghiệm: Tuyệt đối KHÔNG kết luận bệnh, KHÔNG kê đơn thuốc.
  Đưa ra khuyến nghị đi làm xét nghiệm cận lâm sàng (FPG, HbA1c).
- Khi ĐỦ xét nghiệm: Đối chiếu tiêu chuẩn chẩn đoán, xác định giai đoạn (ĐTĐ Type 2, Tiền ĐTĐ)
  và thiết lập phác đồ thuốc khuyến nghị phù hợp chức năng thận (eGFR).
"""

from typing import Dict, Any, Optional, List

from src.core.state_schema import DiabetesMASState, ClinicalPrescription
from src.core.gemini_client import GeminiMASClient
from src.knowledge.vietnamese_guidelines_rag import VietnameseGuidelinesRAG


class EndocrinologistAgent:
    """
    Agent Bác sĩ Nội tiết tuân thủ quy chuẩn y tế Bộ Y Tế Việt Nam.
    """

    def __init__(self, gemini_client: Optional[GeminiMASClient] = None, rag: Optional[VietnameseGuidelinesRAG] = None):
        self.gemini = gemini_client or GeminiMASClient()
        self.rag = rag or VietnameseGuidelinesRAG()

    def run(self, state: DiabetesMASState, is_revision: bool = False) -> DiabetesMASState:
        p = state.patient_profile
        ml = state.ml_prediction
        p.check_completeness()

        # =====================================================================
        # TRƯỜNG HỢP 1: THIẾU CHỈ SỐ XÉT NGHIỆM ĐỊNH LƯỢNG (INSUFFICIENT_LABS)
        # =====================================================================
        if p.data_completeness == "INSUFFICIENT_LABS":
            # -----------------------------------------------------------------
            # TRUY XUẤT TEXT-RAG: Tiêu chuẩn chẩn đoán theo QĐ 5481/QĐ-BYT Bộ Y Tế
            # Mục đích:
            #   - Tìm kiếm semantic chunks trong bộ hướng dẫn chẩn đoán quốc gia.
            #   - Đưa ra chứng cứ khẳng định: Chẩn đoán ĐTĐ bắt buộc dựa trên sinh hóa
            #     (FPG >= 126 mg/dL hoặc HbA1c >= 6.5%), ngăn ngừa kê đơn sai quy định.
            # -----------------------------------------------------------------
            rag_query = "Tiêu chuẩn chẩn đoán đái tháo đường theo Bộ Y Tế QĐ 5481"
            guideline_chunks = self.rag.retrieve(rag_query, top_k=1)
            cited_sources = [c["source"] for c in guideline_chunks]

            diag = "Chưa đủ dữ liệu xét nghiệm để khẳng định chẩn đoán"
            workup = [
                "Xét nghiệm đường huyết tương lúc đói (FPG) - nhịn ăn ít nhất 8 giờ",
                "Xét nghiệm chỉ số HbA1c (phương pháp chuẩn hóa NGSP)"
            ]
            rationale = (
                "Theo Quyết định 5481/QĐ-BYT của Bộ Y Tế, chẩn đoán xác định đái tháo đường "
                "bắt buộc phải dựa trên xét nghiệm sinh hóa máu định lượng (FPG >= 126 mg/dL hoặc HbA1c >= 6.5%). "
                "Dựa trên thể trạng và các dấu hiệu bạn chia sẻ, bạn thuộc diện cần được tầm soát sớm. "
                "Tuyệt đối không tự ý mua và sử dụng thuốc hạ đường huyết khi chưa có kết quả xét nghiệm."
            )

            state.clinical_prescription = ClinicalPrescription(
                assessment_type="SCREENING_RECOMMENDATION",
                has_confirmed_diabetes=False,
                diagnosis=diag,
                target_hba1c="Cần duy trì < 5.7% (ngưỡng bình thường)",
                primary_drug=None,  # CẤM KÊ ĐƠN THUỐC
                primary_dose=None,
                add_on_drug=None,
                add_on_dose=None,
                diagnostic_workup_needed=workup,
                clinical_rationale=rationale,
                guidelines_cited=cited_sources
            )

            state.agent_execution_logs.append({
                "agent": "EndocrinologistAgent",
                "status": "SCREENING_ADVICE",
                "message": f"Chưa đủ xét nghiệm máu -> Đưa ra khuyến nghị tầm soát, không kê đơn thuốc Rx"
            })
            return state

        # =====================================================================
        # TRƯỜNG HỢP 2: ĐÃ CÓ XÉT NGHIỆM ĐỊNH LƯỢNG (SUFFICIENT_LABS)
        # =====================================================================
        # ---------------------------------------------------------------------
        # TRUY XUẤT TEXT-RAG: Phác đồ điều trị cá nhân hóa theo hướng dẫn Bộ Y Tế
        # Mục đích:
        #   - Tra cứu phác đồ chuẩn cho mức HbA1c, bệnh đồng mắc (suy tim, suy thận).
        #   - Cung cấp căn cứ y khoa lựa chọn thuốc đầu tay (Metformin) hoặc thay thế (DPP-4i).
        # ---------------------------------------------------------------------
        rag_query = f"Phác đồ điều trị đái tháo đường HbA1c {p.hba1c}% suy tim {p.heart_disease} suy thận eGFR {p.egfr}"
        guideline_chunks = self.rag.retrieve(rag_query, top_k=2)
        cited_sources = [c["source"] for c in guideline_chunks]

        # Kiểm tra tiêu chuẩn chẩn đoán Bộ Y Tế (QĐ 5481/QĐ-BYT)
        is_diabetic = False
        is_prediabetic = False

        if (p.hba1c and p.hba1c >= 6.5) or (p.blood_glucose_level and p.blood_glucose_level >= 126.0):
            is_diabetic = True
            diag = "Đái tháo đường Type 2 (ICD-10: E11)"
            target_a1c = "< 7.0%"
        elif (p.hba1c and 5.7 <= p.hba1c < 6.5) or (p.blood_glucose_level and 100.0 <= p.blood_glucose_level < 126.0):
            is_prediabetic = True
            diag = "Tiền đái tháo đường / Rối loạn dung nạp Glucose (ICD-10: R73.0)"
            target_a1c = "< 5.7%"
        else:
            diag = "Chỉ số xét nghiệm trong giới hạn bình thường"
            target_a1c = "< 5.7%"

        # Phác đồ điều trị bằng thuốc
        primary_drug = None
        primary_dose = None
        add_on_drug = None
        add_on_dose = None
        rationale = ""

        if is_diabetic:
            # Thuốc đầu tay tiêu chuẩn
            primary_drug = "Metformin"
            primary_dose = "500mg x 2 lần/ngày (uống cùng hoặc sau bữa ăn)"

            # Kiểm tra phản biện suy thận nặng hoặc dị ứng cồn
            if (is_revision or (p.egfr is not None and p.egfr < 30)) and (p.egfr is not None and p.egfr < 30):
                primary_drug = "Sitagliptin (DPP-4i)"
                primary_dose = "25mg x 1 lần/ngày (đã chỉnh giảm 75% liều do suy thận eGFR < 30)"
                rationale = "Thay thế Metformin bằng Sitagliptin liều thấp do bệnh nhân suy thận nặng (eGFR < 30 mL/min) để loại trừ nguy cơ nhiễm toan Lactic theo QĐ 5481."
            elif is_revision and p.alcohol_use:
                primary_drug = "Sitagliptin (DPP-4i)"
                primary_dose = "50mg x 1 lần/ngày"
                rationale = "Thay thế Metformin vì bệnh nhân uống nhiều rượu bia thường xuyên có nguy cơ toan Lactic."
            else:
                rationale = "Khởi đầu Metformin đơn trị liệu kết hợp điều chỉnh chế độ ăn theo khuyến cáo bậc 1 của Bộ Y Tế."
                if p.heart_disease == 1 or (p.egfr is not None and 20 <= p.egfr < 60):
                    add_on_drug = "Dapagliflozin (SGLT2i)"
                    add_on_dose = "10mg x 1 lần/ngày (uống buổi sáng)"
                    rationale += " Phối hợp thêm Dapagliflozin (SGLT2i) để bảo vệ tim mạch và làm chậm suy thận."
        elif is_prediabetic:
            rationale = "Ở giai đoạn tiền đái tháo đường, ưu tiên can thiệp lối sống tích cực (giảm 5-7% cân nặng, tập thể dục 150 phút/tuần), chưa chỉ định dùng thuốc."

        state.clinical_prescription = ClinicalPrescription(
            assessment_type="CONFIRMED_DIAGNOSIS",
            has_confirmed_diabetes=is_diabetic,
            diagnosis=diag,
            target_hba1c=target_a1c,
            primary_drug=primary_drug,
            primary_dose=primary_dose,
            add_on_drug=add_on_drug,
            add_on_dose=add_on_dose,
            diagnostic_workup_needed=[],
            clinical_rationale=rationale,
            guidelines_cited=cited_sources
        )

        state.agent_execution_logs.append({
            "agent": "EndocrinologistAgent",
            "status": "SUCCESS" if not is_revision else "REVISED_SUCCESS",
            "message": f"Chẩn đoán: {diag} | Thuốc: {primary_drug or 'Không dùng thuốc'}"
        })

        return state
