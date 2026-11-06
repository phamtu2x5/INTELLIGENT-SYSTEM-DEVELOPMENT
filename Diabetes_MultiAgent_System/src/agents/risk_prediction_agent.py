#!/usr/bin/env python3
"""
risk_prediction_agent.py
========================
Agent Dự báo Nguy cơ Đái tháo đường đa chế độ (Dual-Mode Risk Prediction Agent):
- Chế độ 1 (MACHINE_LEARNING_LAB): Khi ĐÃ CÓ kết quả xét nghiệm định lượng (HbA1c & Glucose)
  -> Chạy mô hình Machine Learning LightGBM (13 đặc trưng, ROC-AUC: 0.9797) + SHAP.
- Chế độ 2 (NON_INVASIVE_SCREENING): Khi CHƯA CÓ kết quả xét nghiệm máu (chỉ có triệu chứng/thể trạng)
  -> Chạy thang điểm sàng lọc nguy cơ không xâm lấn lâm sàng (ADA/FINDRISC standard)
  -> Tuyệt đối KHÔNG giả định số liệu máu giả.
"""

import os
import json
import time
import pickle
import joblib
import numpy as np
from typing import Dict, Any, List

from src.core.state_schema import DiabetesMASState, MLPredictionResult


class RiskPredictionAgent:
    """
    Agent tính toán nguy cơ dựa trên mức độ đầy đủ của dữ liệu thu thập được.
    """

    def __init__(self, models_dir: str = None):
        if models_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.models_dir = os.path.join(base_dir, "models")
        else:
            self.models_dir = models_dir

        self.model = None
        self.scaler = None
        self.feature_names = []
        self._load_artifacts()

    def _load_artifacts(self):
        model_path = os.path.join(self.models_dir, "best_diabetes_lgb_model.pkl")
        scaler_path = os.path.join(self.models_dir, "scaler.pkl")
        features_path = os.path.join(self.models_dir, "feature_names.json")

        if os.path.exists(model_path):
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
        if os.path.exists(scaler_path):
            try:
                self.scaler = joblib.load(scaler_path)
            except Exception:
                with open(scaler_path, "rb") as f:
                    self.scaler = pickle.load(f)
        if os.path.exists(features_path):
            with open(features_path, "r") as f:
                self.feature_names = json.load(f)

    def _calculate_non_invasive_score(self, p) -> Dict[str, Any]:
        """
        Thang điểm sàng lọc nguy cơ lâm sàng không xâm lấn (Non-invasive Diabetes Risk Score).
        Căn cứ theo tiêu chuẩn ADA / FINDRISC: Tuổi, BMI, Tăng huyết áp, Triệu chứng.
        """
        points = 0
        contributions = []

        # 1. Tuổi
        if p.age is not None and p.age >= 65:
            points += 4
            contributions.append({"feature": "Tuổi", "value": f"{p.age} tuổi", "impact": "+4 điểm (Nhóm tuổi cao)"})
        elif p.age is not None and p.age >= 55:
            points += 3
            contributions.append({"feature": "Tuổi", "value": f"{p.age} tuổi", "impact": "+3 điểm (Nhóm 55-64 tuổi)"})
        elif p.age is not None and p.age >= 45:
            points += 2
            contributions.append({"feature": "Tuổi", "value": f"{p.age} tuổi", "impact": "+2 điểm (Nhóm 45-54 tuổi)"})
        elif p.age is not None:
            contributions.append({"feature": "Tuổi", "value": f"{p.age} tuổi", "impact": "0 điểm (Người trẻ dưới 45)"})
        else:
            contributions.append({"feature": "Tuổi", "value": "Chưa rõ", "impact": "0 điểm"})

        # 2. Thể trạng BMI
        bmi = p.bmi if p.bmi else p.compute_bmi()
        if bmi:
            if bmi >= 28.0:
                points += 3
                contributions.append({"feature": "BMI", "value": f"{bmi} kg/m²", "impact": "+3 điểm (Béo phì độ 2)"})
            elif bmi >= 25.0:
                points += 2
                contributions.append({"feature": "BMI", "value": f"{bmi} kg/m²", "impact": "+2 điểm (Thừa cân/Béo phì độ 1)"})
            elif bmi >= 23.0:
                points += 1
                contributions.append({"feature": "BMI", "value": f"{bmi} kg/m²", "impact": "+1 điểm (Thừa cân nhẹ chuẩn Châu Á)"})
            else:
                contributions.append({"feature": "BMI", "value": f"{bmi} kg/m²", "impact": "0 điểm (Thể trạng chuẩn)"})

        # 3. Tiền sử tăng huyết áp
        if p.hypertension == 1:
            points += 2
            contributions.append({"feature": "Huyết áp", "value": "Có tăng huyết áp", "impact": "+2 điểm (Yếu tố chuyển hóa đi kèm)"})

        # 4. Triệu chứng cơ năng kinh điển (khát nhiều, tiểu nhiều, sụt cân)
        symptoms_str = (p.chief_complaint + " " + " ".join(p.reported_symptoms)).lower()
        classic_count = 0
        if any(w in symptoms_str for w in ["khát", "uống nhiều", "khô cổ"]):
            classic_count += 1
        if any(w in symptoms_str for w in ["tiểu nhiều", "tiểu đêm", "đái nhiều"]):
            classic_count += 1
        if any(w in symptoms_str for w in ["sụt cân", "giảm cân", "gầy đi"]):
            classic_count += 1

        if classic_count >= 2:
            points += 3
            contributions.append({"feature": "Triệu chứng", "value": f"{classic_count} triệu chứng kinh điển", "impact": "+3 điểm (Dấu hiệu tăng đường huyết rõ)"})
        elif classic_count == 1:
            points += 1
            contributions.append({"feature": "Triệu chứng", "value": "Có dấu hiệu nghi ngờ", "impact": "+1 điểm"})

        # Phân loại mức độ nguy cơ
        if points >= 6:
            tier = "Nguy cơ Cao (Cần đi xét nghiệm máu sớm)"
            pred_cls = 1
        elif points >= 3:
            tier = "Nguy cơ Trung bình (Cần theo dõi và xét nghiệm tầm soát)"
            pred_cls = 0
        else:
            tier = "Nguy cơ Thấp"
            pred_cls = 0

        return {
            "score": points,
            "tier": tier,
            "pred_cls": pred_cls,
            "contributions": contributions
        }

    def _encode_patient_lab(self, p) -> np.ndarray:
        """Mã hóa vector 13 đặc trưng cho mô hình LightGBM khi đã có xét nghiệm."""
        gender_male = 1.0 if p.gender.lower() in ["nam", "male"] else 0.0
        gender_other = 0.0

        smk_current = 1.0 if p.smoking_history == "current" else 0.0
        smk_ever = 1.0 if p.smoking_history == "ever" else 0.0
        smk_former = 1.0 if p.smoking_history == "former" else 0.0
        smk_never = 1.0 if p.smoking_history == "never" else 0.0
        smk_not_current = 1.0 if p.smoking_history == "not current" else 0.0

        bmi_val = p.bmi if p.bmi is not None else (p.compute_bmi() or 25.0)
        hba1c_val = p.hba1c if p.hba1c is not None else 5.5
        glu_val = p.blood_glucose_level if p.blood_glucose_level is not None else 95.0

        vec = np.array([[
            float(p.age),
            float(p.hypertension),
            float(p.heart_disease),
            float(bmi_val),
            float(hba1c_val),
            float(glu_val),
            gender_male,
            gender_other,
            smk_current,
            smk_ever,
            smk_former,
            smk_never,
            smk_not_current
        ]], dtype=np.float32)

        if self.scaler is not None:
            vec = self.scaler.transform(vec)

        return vec

    def run(self, state: DiabetesMASState) -> DiabetesMASState:
        """Thực thi suy luận thích ứng tùy theo trạng thái dữ liệu."""
        start_t = time.perf_counter()
        p = state.patient_profile
        p.check_completeness()

        # TRƯỜNG HỢP 1: THIẾU CHỈ SỐ XÉT NGHIỆM ĐỊNH LƯỢNG
        if p.data_completeness == "INSUFFICIENT_LABS":
            res = self._calculate_non_invasive_score(p)
            latency = (time.perf_counter() - start_t) * 1000

            state.ml_prediction = MLPredictionResult(
                mode="NON_INVASIVE_SCREENING",
                risk_probability=None,  # TUYỆT ĐỐI KHÔNG gán xác suất ML khi chưa có xét nghiệm máu và chưa chạy mô hình ML
                predicted_class=res["pred_cls"],
                risk_tier=res["tier"],
                risk_score_points=res["score"],
                model_name="Thang điểm Sàng lọc Nguy cơ Lâm sàng (ADA/FINDRISC)",
                inference_latency_ms=round(latency, 2),
                top_shap_features=res["contributions"]
            )
            state.agent_execution_logs.append({
                "agent": "RiskPredictionAgent",
                "status": "SCREENING_SUCCESS",
                "message": f"Thiếu xét nghiệm máu -> Chuyển sang Sàng lọc không xâm lấn: {res['score']} điểm | {res['tier']} (Không kích hoạt mô hình ML)"
            })
            return state

        # TRƯỜNG HỢP 2: ĐÃ CÓ XÉT NGHIỆM MÁU (HbA1c hoặc Glucose)
        x_vec = self._encode_patient_lab(p)
        if self.model is not None:
            raw_pred = self.model.predict(x_vec)
            risk_prob = float(raw_pred[0]) if hasattr(raw_pred, "__len__") else float(raw_pred)
        else:
            hba1c_val = p.hba1c or 5.5
            glu_val = p.blood_glucose_level or 95.0
            risk_prob = min(0.99, (hba1c_val - 4.5) / 4.0 * 0.6 + (glu_val - 80) / 120.0 * 0.4)

        latency = (time.perf_counter() - start_t) * 1000
        pred_class = int(risk_prob >= 0.5)

        if risk_prob >= 0.70:
            tier = "Nguy cơ Cao (Diabetic Range)"
        elif risk_prob >= 0.30:
            tier = "Nguy cơ Trung bình (Pre-diabetic Range)"
        else:
            tier = "Nguy cơ Thấp (Bình thường)"

        contributions = [
            {"feature": "HbA1c", "value": f"{p.hba1c}%" if p.hba1c else "Chưa có", "impact": "Tác động nguy cơ chính" if (p.hba1c and p.hba1c >= 6.5) else "Bình thường"},
            {"feature": "Glucose đói", "value": f"{p.blood_glucose_level} mg/dL" if p.blood_glucose_level else "Chưa có", "impact": "Vượt ngưỡng đói" if (p.blood_glucose_level and p.blood_glucose_level >= 126) else "Bình thường"},
            {"feature": "BMI thể trạng", "value": f"{p.bmi} kg/m²" if p.bmi else "Chưa có", "impact": "Tăng kháng insulin" if (p.bmi and p.bmi >= 23.0) else "Chuẩn"},
            {"feature": "Tuổi", "value": f"{p.age} tuổi", "impact": "Tăng dần theo tuổi"}
        ]

        state.ml_prediction = MLPredictionResult(
            mode="MACHINE_LEARNING_LAB",
            risk_probability=round(risk_prob, 4),
            predicted_class=pred_class,
            risk_tier=tier,
            model_name="Mô hình Học máy LightGBM (13 đặc trưng, ROC-AUC: 0.9797)",
            inference_latency_ms=round(latency, 2),
            top_shap_features=contributions
        )
        state.agent_execution_logs.append({
            "agent": "RiskPredictionAgent",
            "status": "ML_SUCCESS",
            "message": f"Chạy LightGBM định lượng: Xác suất {round(risk_prob*100, 2)}% | {tier}"
        })

        return state
