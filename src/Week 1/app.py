"""
FastAPI Web Application for Diabetes Prediction & FPT Long Châu Healthcare Knowledge Graph
Provides REST APIs for multi-model classification, model comparison, preset loading,
and Healthcare Knowledge Graph recommendations.
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from knowledge_graph import build_patient_knowledge_graph, LONG_CHAU_KB

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
MODELS_DIR = os.path.join(BASE_DIR, "models")
ALL_MODELS_PATH = os.path.join(MODELS_DIR, "all_models.joblib")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

app = FastAPI(
    title="Diabetes Prediction & Healthcare Knowledge Graph",
    description="Hệ thống học máy thông minh dự đoán đái tháo đường kết hợp Đồ thị tri thức Y tế FPT Long Châu",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Models Dictionary
models_dict = {}

def ensure_models_loaded():
    """Ensure models are loaded from serialized joblib artifact."""
    global models_dict
    if not models_dict and os.path.exists(ALL_MODELS_PATH):
        models_dict = joblib.load(ALL_MODELS_PATH)
        print(f"✓ Đã nạp thành công {len(models_dict)} mô hình từ {ALL_MODELS_PATH}")
    return models_dict

# Initial check on startup
ensure_models_loaded()

# Model Specs & Metadata
MODEL_SPECS = {
    "XGBoost (Tuned)": {
        "display_name": "XGBoost (Tuned)",
        "badge": "🏆 Khuyên dùng",
        "type": "Extreme Gradient Boosting",
        "accuracy": 75.32,
        "f1": 0.6122,
        "roc_auc": 0.8289,
        "recall": 55.56,
        "precision": 68.18,
        "desc": "Mô hình phân loại tốt nhất, tối ưu siêu tham số, kiểm soát độ phức tạp cây và chống phân cực xác suất."
    },
    "Random Forest": {
        "display_name": "Random Forest Classifier",
        "badge": "🌲 Bagging Ensemble",
        "type": "Random Forest Ensemble",
        "accuracy": 71.43,
        "f1": 0.5417,
        "roc_auc": 0.8230,
        "recall": 48.15,
        "precision": 61.90,
        "desc": "Tập hợp các cây quyết định, giảm phương sai và chống quá khớp hiệu quả."
    },
    "Support Vector Machine": {
        "display_name": "Support Vector Machine (SVM)",
        "badge": "🎯 RBF Kernel",
        "type": "Kernel Classifier",
        "accuracy": 74.03,
        "f1": 0.5833,
        "roc_auc": 0.7976,
        "recall": 51.85,
        "precision": 66.67,
        "desc": "Tìm siêu phẳng phân cách tối ưu trong không gian đặc trưng vô hạn chiều (RBF)."
    },
    "Logistic Regression": {
        "display_name": "Logistic Regression",
        "badge": "📐 Linear Baseline",
        "type": "Linear Classifier",
        "accuracy": 70.78,
        "f1": 0.5455,
        "roc_auc": 0.8130,
        "recall": 50.00,
        "precision": 60.00,
        "desc": "Mô hình hồi quy Logistic tuyến tính làm đường cơ sở đối chuẩn."
    },
    "K-Nearest Neighbors": {
        "display_name": "K-Nearest Neighbors (KNN)",
        "badge": "📍 Instance-based",
        "type": "Non-parametric",
        "accuracy": 72.73,
        "f1": 0.5686,
        "roc_auc": 0.7980,
        "recall": 53.70,
        "precision": 60.42,
        "desc": "Phân loại dựa trên khoảng cách Euclidean trong không gian đa chiều."
    }
}

def resolve_model(model_name: str, models: dict):
    """Robustly find the matching model pipeline."""
    if model_name in models:
        return model_name, models[model_name]
    if "XGBoost" in model_name or model_name == "XGBoost":
        if "XGBoost (Tuned)" in models:
            return "XGBoost (Tuned)", models["XGBoost (Tuned)"]
    for k, v in models.items():
        if model_name.lower() in k.lower() or k.lower() in model_name.lower():
            return k, v
    first_k = list(models.keys())[-1]
    return first_k, models[first_k]

# Presets Data
PRESETS = [
    {
        "id": "high_risk_50",
        "name": "Bệnh nhân nguy cơ cao (50 tuổi, Glucose 180)",
        "tag": "Nguy cơ cao",
        "data": {
            "Pregnancies": 6,
            "Glucose": 180.0,
            "BloodPressure": 85.0,
            "SkinThickness": 35.0,
            "Insulin": 220.0,
            "BMI": 38.0,
            "DiabetesPedigreeFunction": 0.85,
            "Age": 50
        }
    },
    {
        "id": "medium_risk_42",
        "name": "Tiền tiểu đường (42 tuổi, Glucose 135)",
        "tag": "Nguy cơ TB",
        "data": {
            "Pregnancies": 2,
            "Glucose": 135.0,
            "BloodPressure": 74.0,
            "SkinThickness": 28.0,
            "Insulin": 110.0,
            "BMI": 30.5,
            "DiabetesPedigreeFunction": 0.45,
            "Age": 42
        }
    },
    {
        "id": "healthy_24",
        "name": "Người trẻ khỏe mạnh (24 tuổi, Glucose 88)",
        "tag": "Khỏe mạnh",
        "data": {
            "Pregnancies": 0,
            "Glucose": 88.0,
            "BloodPressure": 68.0,
            "SkinThickness": 20.0,
            "Insulin": 65.0,
            "BMI": 21.8,
            "DiabetesPedigreeFunction": 0.22,
            "Age": 24
        }
    },
    {
        "id": "young_overweight_28",
        "name": "Thừa cân (28 tuổi, Glucose 115, BMI 34.2)",
        "tag": "Thừa cân",
        "data": {
            "Pregnancies": 1,
            "Glucose": 115.0,
            "BloodPressure": 78.0,
            "SkinThickness": 32.0,
            "Insulin": 95.0,
            "BMI": 34.2,
            "DiabetesPedigreeFunction": 0.38,
            "Age": 28
        }
    },
    {
        "id": "gestational_36",
        "name": "Tiểu đường thai kỳ (36 tuổi, Sinh 7 lần)",
        "tag": "Thai kỳ",
        "data": {
            "Pregnancies": 7,
            "Glucose": 150.0,
            "BloodPressure": 80.0,
            "SkinThickness": 30.0,
            "Insulin": 140.0,
            "BMI": 32.0,
            "DiabetesPedigreeFunction": 0.62,
            "Age": 36
        }
    }
]

# Request Schema
class PatientInput(BaseModel):
    Pregnancies: Optional[float] = Field(0.0, ge=0.0, le=25.0, description="Số lần mang thai")
    Glucose: float = Field(..., ge=40.0, le=350.0, description="Nồng độ đường huyết (mg/dL)")
    BloodPressure: Optional[float] = Field(None, ge=30.0, le=200.0, description="Huyết áp tâm trương (mm Hg)")
    SkinThickness: Optional[float] = Field(None, ge=5.0, le=100.0, description="Độ dày nếp gấp da (mm)")
    Insulin: Optional[float] = Field(None, ge=5.0, le=900.0, description="Nồng độ Insulin 2h (mu U/ml)")
    BMI: float = Field(..., ge=10.0, le=80.0, description="Chỉ số khối cơ thể (kg/m²)")
    DiabetesPedigreeFunction: Optional[float] = Field(0.47, ge=0.05, le=3.0, description="Hệ số di truyền tiểu đường")
    Age: float = Field(..., ge=15.0, le=110.0, description="Tuổi bệnh nhân")
    model_name: Optional[str] = Field("XGBoost", description="Mô hình được chọn")


def process_patient_features(data_dict: dict) -> pd.DataFrame:
    """Preprocess patient input, handle invalid biological values, and compute interaction features."""
    clean_dict = {
        "Pregnancies": data_dict.get("Pregnancies", 0.0),
        "Glucose": data_dict.get("Glucose", 100.0),
        "BloodPressure": data_dict.get("BloodPressure") if data_dict.get("BloodPressure") is not None else np.nan,
        "SkinThickness": data_dict.get("SkinThickness") if data_dict.get("SkinThickness") is not None else np.nan,
        "Insulin": data_dict.get("Insulin") if data_dict.get("Insulin") is not None else np.nan,
        "BMI": data_dict.get("BMI", 25.0),
        "DiabetesPedigreeFunction": data_dict.get("DiabetesPedigreeFunction", 0.47),
        "Age": data_dict.get("Age", 30.0)
    }
    
    # Replace 0s with NaN for biological metrics
    for k in ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]:
        if clean_dict[k] == 0:
            clean_dict[k] = np.nan
            
    df = pd.DataFrame([clean_dict])
    
    # Feature Engineering & Selection (9 Features)
    df["Glucose_BMI_Risk"] = df["Glucose"] * df["BMI"]
    
    return df


@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    """Render main web interface."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "models": MODEL_SPECS,
            "presets": PRESETS,
            "longchau": LONG_CHAU_KB
        }
    )


@app.get("/api/presets")
async def get_presets():
    """Return list of sample patient presets."""
    return {"presets": PRESETS}


@app.get("/api/models")
async def get_models_list():
    """Return available models and their benchmark metrics."""
    return {"models": MODEL_SPECS}


@app.get("/api/longchau-catalog")
async def get_longchau_catalog():
    """Return FPT Long Châu Healthcare products and services ontology."""
    return {"catalog": LONG_CHAU_KB}


@app.post("/api/predict")
async def predict_single(patient: PatientInput):
    """Predict diabetes outcome and generate Long Châu Knowledge Graph recommendations."""
    current_models = ensure_models_loaded()
    
    model_key, pipeline = resolve_model(patient.model_name or "XGBoost (Tuned)", current_models)
    
    if pipeline is None:
        raise HTTPException(status_code=400, detail=f"Không tìm thấy mô hình {model_key}")
    
    data_dict = patient.model_dump()
    data_dict.pop("model_name", None)
    
    features_df = process_patient_features(data_dict)
    
    try:
        pred_class = int(pipeline.predict(features_df)[0])
        probabilities = pipeline.predict_proba(features_df)[0]
        diabetic_prob = round(float(probabilities[1]) * 100, 1)
        healthy_prob = round(float(probabilities[0]) * 100, 1)
        
        specs = MODEL_SPECS.get(model_key, {})
        
        if diabetic_prob >= 65.0:
            status_text = "Nguy cơ cao mắc Tiểu đường (Diabetic)"
            status_color = "danger"
            advice = "Chỉ số Glucose và BMI vượt ngưỡng an toàn. Cần tiến hành xét nghiệm HbA1c và tư vấn bác sĩ chuyên khoa nội tiết."
        elif diabetic_prob >= 35.0:
            status_text = "Tiền tiểu đường / Cần theo dõi (Borderline Risk)"
            status_color = "warning"
            advice = "Có dấu hiệu kháng Insulin và rối loạn dung nạp Glucose. Cần kiểm soát chế độ ăn và theo dõi đường huyết tại nhà."
        else:
            status_text = "Nguy cơ thấp / Bình thường (Non-Diabetic)"
            status_color = "success"
            advice = "Các chỉ số chuyển hóa nằm trong giới hạn an toàn. Duy trì lối sống lành mạnh và kiểm tra định kỳ."

        # Generate Knowledge Graph Mapping
        kg_res = build_patient_knowledge_graph(
            patient_id="BN_CURRENT",
            patient_data=data_dict,
            pred_result={
                "model_name": model_key,
                "prediction": pred_class,
                "diabetic_probability": diabetic_prob,
                "status_text": status_text
            }
        )

        return {
            "status": "success",
            "model_name": model_key,
            "display_name": specs.get("display_name", model_key),
            "badge": specs.get("badge", ""),
            "prediction": pred_class,
            "status_text": status_text,
            "status_color": status_color,
            "diabetic_probability": diabetic_prob,
            "healthy_probability": healthy_prob,
            "advice": advice,
            "metrics": {
                "accuracy": specs.get("accuracy"),
                "f1": specs.get("f1"),
                "roc_auc": specs.get("roc_auc"),
                "recall": specs.get("recall"),
                "precision": specs.get("precision")
            },
            "longchau_care": kg_res.get("care_package"),
            "knowledge_graph": kg_res.get("graph"),
            "description": specs.get("desc", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi dự đoán: {str(e)}")


@app.post("/api/predict-all")
async def predict_all_models(patient: PatientInput):
    """Predict diabetes probability across all 5 models simultaneously."""
    current_models = ensure_models_loaded()
    
    data_dict = patient.model_dump()
    data_dict.pop("model_name", None)
    
    features_df = process_patient_features(data_dict)
    
    results = []
    probs = []
    
    for name, pipeline in current_models.items():
        try:
            pred_class = int(pipeline.predict(features_df)[0])
            probabilities = pipeline.predict_proba(features_df)[0]
            prob = round(float(probabilities[1]) * 100, 1)
            probs.append(prob)
            specs = MODEL_SPECS.get(name, {})
            
            results.append({
                "model_name": name,
                "display_name": specs.get("display_name", name),
                "badge": specs.get("badge", ""),
                "prediction": pred_class,
                "diabetic_probability": prob,
                "prob_formatted": f"{prob:.1f}%",
                "accuracy": specs.get("accuracy", 0),
                "f1": specs.get("f1", 0),
                "roc_auc": specs.get("roc_auc", 0),
                "recall": specs.get("recall", 0),
                "is_best": (name == "XGBoost")
            })
        except Exception as e:
            print(f"Error predicting with {name}: {e}")
    
    results = sorted(results, key=lambda x: x["roc_auc"], reverse=True)
    
    avg_prob = round(float(np.mean(probs)), 1) if probs else 0
    min_prob = min(probs) if probs else 0
    max_prob = max(probs) if probs else 0
    
    if avg_prob >= 60.0:
        consensus = "🔴 Đa số mô hình đồng thuận: Nguy cơ cao mắc Tiểu đường"
        status_color = "danger"
    elif avg_prob >= 35.0:
        consensus = "🟡 Đa số mô hình đồng thuận: Tiền tiểu đường / Cần theo dõi"
        status_color = "warning"
    else:
        consensus = "🟢 Đa số mô hình đồng thuận: Nguy cơ thấp / Khỏe mạnh"
        status_color = "success"

    return {
        "status": "success",
        "results": results,
        "summary": {
            "average_probability": avg_prob,
            "average_formatted": f"{avg_prob:.1f}%",
            "min_probability": min_prob,
            "max_probability": max_prob,
            "prob_range": f"{min_prob:.1f}% - {max_prob:.1f}%",
            "consensus": consensus,
            "status_color": status_color
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 [Week 1] Khởi chạy máy chủ Web dự đoán Tiểu đường tại: http://127.0.0.1:8080")
    uvicorn.run(app, host="127.0.0.1", port=8080)
