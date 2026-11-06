#!/usr/bin/env python3
"""
state_schema.py
===============
Định nghĩa cấu trúc dữ liệu State Schema chuẩn hóa cho Hệ thống Đa Agent DiaAgent-MAS.
Hỗ trợ quản lý dữ liệu 2 chế độ:
- INSUFFICIENT_LABS: Khi người dùng chỉ có triệu chứng, thể trạng, chưa có xét nghiệm.
- SUFFICIENT_LABS: Khi người dùng đã có kết quả xét nghiệm định lượng (HbA1c/Glucose).
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class PatientProfile(BaseModel):
    """Hồ sơ lâm sàng và chỉ số sinh học của người bệnh."""
    patient_id: str = "P_GUEST_001"
    name: str = "Người dùng"
    age: int = 50
    gender: str = "Nam"  # 'Nam' hoặc 'Nữ'
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None
    hypertension: int = 0  # 0: Không, 1: Có
    heart_disease: int = 0  # 0: Không, 1: Có
    smoking_history: str = "never"  # 'never', 'current', 'former', 'not current'
    
    # Các chỉ số xét nghiệm (Mặc định là None, TUYỆT ĐỐI không gán số giả định)
    hba1c: Optional[float] = None  # % (Chỉ số HbA1c)
    blood_glucose_level: Optional[float] = None  # mg/dL (Đường huyết đói FPG)
    egfr: Optional[float] = None  # mL/min/1.73m² (Chức năng lọc thận)
    
    alcohol_use: bool = False
    liver_disease: bool = False
    chief_complaint: str = ""
    reported_symptoms: List[str] = Field(default_factory=list)
    
    # Trạng thái đầy đủ của dữ liệu: 'INSUFFICIENT_LABS' hoặc 'SUFFICIENT_LABS'
    data_completeness: str = "INSUFFICIENT_LABS"

    def compute_bmi(self) -> Optional[float]:
        if self.height_cm and self.weight_kg and self.height_cm > 50:
            self.bmi = round(self.weight_kg / ((self.height_cm / 100.0) ** 2), 1)
        return self.bmi

    def check_completeness(self) -> str:
        if self.hba1c is not None or self.blood_glucose_level is not None:
            self.data_completeness = "SUFFICIENT_LABS"
        else:
            self.data_completeness = "INSUFFICIENT_LABS"
        return self.data_completeness


class MLPredictionResult(BaseModel):
    """Kết quả dự báo định lượng hoặc phân tầng nguy cơ."""
    mode: str = "NON_INVASIVE_SCREENING"  # 'NON_INVASIVE_SCREENING' hoặc 'MACHINE_LEARNING_LAB'
    risk_probability: Optional[float] = None
    predicted_class: int = 0  # 0: Bình thường / Nguy cơ thấp, 1: Nguy cơ cao
    risk_tier: str = "Chưa đánh giá"  # 'Thấp', 'Trung bình', 'Cao'
    risk_score_points: int = 0  # Thang điểm không xâm lấn nếu thiếu xét nghiệm máu
    model_name: str = "Thang điểm Sàng lọc Nguy cơ Lâm sàng (ADA/FINDRISC)"
    inference_latency_ms: float = 0.0
    top_shap_features: List[Dict[str, Any]] = Field(default_factory=list)


class ClinicalPrescription(BaseModel):
    """Đánh giá và phác đồ chuyên môn từ EndocrinologistAgent."""
    assessment_type: str = "SCREENING_RECOMMENDATION"  # 'SCREENING_RECOMMENDATION' hoặc 'CONFIRMED_DIAGNOSIS'
    has_confirmed_diabetes: bool = False
    diagnosis: str = "Chưa đủ dữ liệu xét nghiệm để khẳng định chẩn đoán"
    target_hba1c: Optional[str] = None
    
    # Thuốc chỉ định (Chỉ có giá trị khi assessment_type == 'CONFIRMED_DIAGNOSIS')
    primary_drug: Optional[str] = None
    primary_dose: Optional[str] = None
    add_on_drug: Optional[str] = None
    add_on_dose: Optional[str] = None
    
    # Chỉ định xét nghiệm cần làm nếu đang ở giai đoạn sàng lọc
    diagnostic_workup_needed: List[str] = Field(default_factory=list)
    clinical_rationale: str = ""
    guidelines_cited: List[str] = Field(default_factory=list)


class NutritionRecommendation(BaseModel):
    """Kế hoạch dinh dưỡng từ NutritionAgent."""
    daily_calories: int = 1600
    macronutrient_ratio: str = "Tinh bột chậm 50% - Đạm nạc 20% - Chất béo tốt 30%"
    breakfast: str = ""
    lunch: str = ""
    dinner: str = ""
    snacks: str = ""
    high_gi_foods_to_avoid: List[str] = Field(default_factory=list)
    healthy_swaps: List[Dict[str, str]] = Field(default_factory=list)


class LifestyleRecommendation(BaseModel):
    """Kế hoạch vận động thể lực và phòng ngừa biến chứng."""
    fitt_aerobic: str = "Đi bộ nhanh 30 phút/ngày, 5 ngày/tuần (tổng 150 phút/tuần)"
    fitt_resistance: str = "Squat nhẹ hoặc bài tập vận động các nhóm cơ lớn 2 buổi/tuần"
    foot_care_rules: List[str] = Field(default_factory=list)
    hypoglycemia_protocol: str = "Quy tắc 15-15: Bổ sung 15g đường nhanh khi có triệu chứng hạ đường huyết"


class PharmacyItem(BaseModel):
    """Thông tin sản phẩm tham khảo tại FPT Long Châu."""
    product_id: str = ""
    brand_name: str = ""
    active_ingredient: str = ""
    drug_class: str = ""
    unit_price_vnd: int = 0
    box_price_vnd: int = 0
    is_prescription_rx: bool = False
    indication: str = ""
    longchau_url: str = ""
    monthly_cost_vnd: int = 0


class SafetyCheckResult(BaseModel):
    """Kết quả kiểm tra chéo an toàn từ SafetyGuardianAgent."""
    status: str = "APPROVED"  # 'APPROVED' hoặc 'REJECTED_NEEDS_REVISION'
    passed: bool = True
    critical_alerts: List[str] = Field(default_factory=list)
    caution_notes: List[str] = Field(default_factory=list)
    revision_iteration: int = 0


class DiabetesMASState(BaseModel):
    """Toàn bộ Trạng thái chia sẻ của Hệ thống Đa Agent."""
    patient_profile: PatientProfile = Field(default_factory=PatientProfile)
    ml_prediction: MLPredictionResult = Field(default_factory=MLPredictionResult)
    clinical_prescription: ClinicalPrescription = Field(default_factory=ClinicalPrescription)
    nutrition_recommendation: NutritionRecommendation = Field(default_factory=NutritionRecommendation)
    lifestyle_recommendation: LifestyleRecommendation = Field(default_factory=LifestyleRecommendation)
    pharmacy_items: List[PharmacyItem] = Field(default_factory=list)
    total_monthly_pharmacy_cost_vnd: int = 0
    safety_check: SafetyCheckResult = Field(default_factory=SafetyCheckResult)
    final_patient_summary: str = ""
    
    # Lưu trữ lịch sử đối thoại Chatbot đa vòng
    chat_history: List[Dict[str, str]] = Field(default_factory=list)
    agent_execution_logs: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
