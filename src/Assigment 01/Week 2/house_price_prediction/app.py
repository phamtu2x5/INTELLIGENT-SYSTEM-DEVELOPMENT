"""
FastAPI Web Application for Vietnam House Price Prediction & Real Estate Knowledge Graph
Provides REST APIs for multi-model regression, comparison, preset loading,
and Real Estate Urban Infrastructure & Bank Mortgage Knowledge Graph.
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

from knowledge_graph import build_housing_knowledge_graph, AMENITIES_KB, PARTNER_BANKS

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
    title="Vietnam House Price Predictor & Real Estate Knowledge Graph",
    description="Hệ thống học máy thông minh dự đoán giá bất động sản kết hợp Đồ thị Tri thức Tiện ích Đô thị & Gói vay Ngân hàng",
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
    "XGBoost": {
        "display_name": "XGBoost (Tuned)",
        "badge": "🏆 Khuyên dùng",
        "type": "Extreme Gradient Boosting",
        "rmse": 1.3166,
        "mae": 1.0206,
        "r2": 0.6329,
        "mape": 21.89,
        "desc": "Mô hình tốt nhất, tối ưu siêu tham số, bắt quan hệ phi tuyến cực tốt trên dữ liệu bảng."
    },
    "Random Forest": {
        "display_name": "Random Forest",
        "badge": "🌲 Bagging Ensemble",
        "type": "Random Forest Regressor",
        "rmse": 1.3972,
        "mae": 1.0845,
        "r2": 0.5866,
        "mape": 23.12,
        "desc": "Tập hợp nhiều cây quyết định, giảm phương sai và chống quá khớp hiệu quả."
    },
    "Gradient Boosting": {
        "display_name": "Gradient Boosting",
        "badge": "⚡ Boosting Ensemble",
        "type": "Gradient Boosting Regressor",
        "rmse": 1.3582,
        "mae": 1.0450,
        "r2": 0.6094,
        "mape": 22.45,
        "desc": "Học tuần tự từ sai số của các cây trước đó, độ chính xác cao."
    },
    "Linear Regression": {
        "display_name": "Linear Regression",
        "badge": "📐 Baseline",
        "type": "Linear Model",
        "rmse": 1.5420,
        "mae": 1.1980,
        "r2": 0.4965,
        "mape": 26.80,
        "desc": "Mô hình cơ sở tuyến tính, thời gian huấn luyện cực nhanh, dễ giải thích trọng số."
    },
    "Decision Tree": {
        "display_name": "Decision Tree",
        "badge": "🌿 Cây đơn lẻ",
        "type": "Tree Regressor",
        "rmse": 1.6250,
        "mae": 1.2540,
        "r2": 0.4410,
        "mape": 28.15,
        "desc": "Cây quyết định đơn lẻ với max_depth=12, tốc độ suy luận tức thì."
    }
}

# Presets Data
PRESETS = [
    {
        "id": "hcm_govap",
        "name": "Nhà phố Gò Vấp, TP.HCM",
        "tag": "TP.HCM",
        "data": {
            "City": "Hồ Chí Minh",
            "District": "Gò Vấp",
            "Ward": "Phường 11",
            "Area": 85.0,
            "Frontage": 5.0,
            "Access Road": 12.0,
            "Floors": 4,
            "Bedrooms": 4,
            "Bathrooms": 4,
            "House direction": "Đông - Nam",
            "Balcony direction": "Đông - Nam",
            "Legal status": "Have certificate",
            "Furniture state": "Full"
        }
    },
    {
        "id": "hn_caugiay",
        "name": "Nhà liền kề Cầu Giấy, Hà Nội",
        "tag": "Hà Nội",
        "data": {
            "City": "Hà Nội",
            "District": "Cầu Giấy",
            "Ward": "Dịch Vọng",
            "Area": 60.0,
            "Frontage": 4.5,
            "Access Road": 8.0,
            "Floors": 5,
            "Bedrooms": 4,
            "Bathrooms": 4,
            "House direction": "Tây - Nam",
            "Balcony direction": "Tây - Nam",
            "Legal status": "Have certificate",
            "Furniture state": "Basic"
        }
    },
    {
        "id": "hy_ecopark",
        "name": "Biệt thự Ecopark, Hưng Yên",
        "tag": "Biệt thự",
        "data": {
            "City": "Hưng Yên",
            "District": "Văn Giang",
            "Ward": "Xuân Quan",
            "Area": 180.0,
            "Frontage": 10.0,
            "Access Road": 15.0,
            "Floors": 3,
            "Bedrooms": 4,
            "Bathrooms": 5,
            "House direction": "Nam",
            "Balcony direction": "Nam",
            "Legal status": "Have certificate",
            "Furniture state": "Full"
        }
    },
    {
        "id": "bd_dian",
        "name": "Nhà phố Dĩ An, Bình Dương",
        "tag": "Bình Dương",
        "data": {
            "City": "Bình Dương",
            "District": "Dĩ An",
            "Ward": "Đông Hòa",
            "Area": 75.0,
            "Frontage": 4.0,
            "Access Road": 6.0,
            "Floors": 2,
            "Bedrooms": 3,
            "Bathrooms": 2,
            "House direction": "Đông",
            "Balcony direction": "Đông",
            "Legal status": "Have certificate",
            "Furniture state": "Basic"
        }
    },
    {
        "id": "hn_thanhxuan_apt",
        "name": "Căn hộ Thanh Xuân, Hà Nội",
        "tag": "Căn hộ",
        "data": {
            "City": "Hà Nội",
            "District": "Thanh Xuân",
            "Ward": "Khương Mai",
            "Area": 70.0,
            "Frontage": 0.0,
            "Access Road": 10.0,
            "Floors": 1,
            "Bedrooms": 2,
            "Bathrooms": 2,
            "House direction": "Đông - Bắc",
            "Balcony direction": "Đông - Nam",
            "Legal status": "Have certificate",
            "Furniture state": "Full"
        }
    }
]

# Request Schema
class HouseInput(BaseModel):
    Area: float = Field(..., ge=5.0, le=5000.0, description="Diện tích (m²)")
    Frontage: Optional[float] = Field(0.0, ge=0.0, le=100.0, description="Mặt tiền (m)")
    Access_Road: Optional[float] = Field(0.0, ge=0.0, le=100.0, alias="Access Road", description="Đường vào (m)")
    Floors: Optional[float] = Field(1.0, ge=1.0, le=50.0, description="Số tầng")
    Bedrooms: Optional[float] = Field(1.0, ge=1.0, le=30.0, description="Số phòng ngủ")
    Bathrooms: Optional[float] = Field(1.0, ge=1.0, le=30.0, description="Số phòng tắm")
    House_direction: Optional[str] = Field("Unknown", alias="House direction", description="Hướng nhà")
    Balcony_direction: Optional[str] = Field("Unknown", alias="Balcony direction", description="Hướng ban công")
    Legal_status: Optional[str] = Field("Unknown", alias="Legal status", description="Tình trạng pháp lý")
    Furniture_state: Optional[str] = Field("Unknown", alias="Furniture state", description="Nội thất")
    City: Optional[str] = Field("Unknown", description="Tỉnh/Thành phố")
    District: Optional[str] = Field("Unknown", description="Quận/Huyện")
    Ward: Optional[str] = Field("Unknown", description="Phường/Xã")
    model_name: Optional[str] = Field("XGBoost", description="Tên mô hình muốn dùng (ALL để so sánh)")

    class Config:
        populate_by_name = True


def prepare_input_dataframe(data_dict: dict) -> pd.DataFrame:
    """Transform user dictionary into model-ready DataFrame with engineered features."""
    clean_dict = {
        "Area": float(data_dict.get("Area", 50.0)),
        "Frontage": float(data_dict["Frontage"]) if data_dict.get("Frontage") is not None else np.nan,
        "Access Road": float(data_dict["Access Road"]) if data_dict.get("Access Road") is not None else np.nan,
        "Floors": float(data_dict.get("Floors", 1.0)),
        "Bedrooms": float(data_dict.get("Bedrooms", 1.0)),
        "Bathrooms": float(data_dict.get("Bathrooms", 1.0)),
        "House direction": str(data_dict.get("House direction", "Unknown")),
        "Balcony direction": str(data_dict.get("Balcony direction", "Unknown")),
        "Legal status": str(data_dict.get("Legal status", "Unknown")),
        "Furniture state": str(data_dict.get("Furniture state", "Unknown")),
        "City": str(data_dict.get("City", "Unknown")),
        "District": str(data_dict.get("District", "Unknown")),
        "Ward": str(data_dict.get("Ward", "Unknown"))
    }
    
    df = pd.DataFrame([clean_dict])
    
    # Feature Engineering
    df["TotalRooms"] = df["Bedrooms"].fillna(0) + df["Bathrooms"].fillna(0)
    bed_safe = df["Bedrooms"].replace(0, np.nan)
    df["AreaPerBedroom"] = df["Area"] / bed_safe
    df["HasFrontage"] = (~df["Frontage"].isna() & (df["Frontage"] > 0)).astype(int)
    df["HasAccessRoad"] = (~df["Access Road"].isna() & (df["Access Road"] > 0)).astype(int)
    df["HasFurnitureInfo"] = (~df["Furniture state"].isna() & (df["Furniture state"] != "Unknown")).astype(int)
    
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
            "amenities_kb": AMENITIES_KB,
            "banks": PARTNER_BANKS
        }
    )


@app.get("/api/presets")
async def get_presets():
    """Return list of sample housing presets."""
    return {"presets": PRESETS}


@app.get("/api/models")
async def get_models_list():
    """Return available models and their benchmark metrics."""
    return {"models": MODEL_SPECS}


@app.get("/api/amenities-catalog")
async def get_amenities_catalog():
    """Return urban amenities and partner banks ontology."""
    return {
        "amenities": AMENITIES_KB,
        "banks": PARTNER_BANKS
    }


@app.post("/api/predict")
async def predict_single(house: HouseInput):
    """Predict house price and generate Real Estate & Mortgage Knowledge Graph recommendations."""
    current_models = ensure_models_loaded()
    
    model_key = house.model_name if house.model_name in current_models else "XGBoost"
    pipeline = current_models.get(model_key)
    
    if pipeline is None:
        raise HTTPException(status_code=400, detail=f"Không tìm thấy mô hình {model_key}")
    
    data_dict = house.model_dump(by_alias=True)
    data_dict.pop("model_name", None)
    
    features_df = prepare_input_dataframe(data_dict)
    
    try:
        pred_price = float(pipeline.predict(features_df)[0])
        pred_price = max(0.5, round(pred_price, 2))  # Giá tối thiểu hợp lý
        
        area = max(1.0, float(data_dict.get("Area", 50.0)))
        price_per_m2 = (pred_price * 1000.0) / area
        
        specs = MODEL_SPECS.get(model_key, {})
        
        # Generate Knowledge Graph Mapping
        kg_res = build_housing_knowledge_graph(
            property_data=data_dict,
            pred_result={
                "model_name": model_key,
                "price_billion": pred_price,
                "price_formatted": f"{pred_price:.2f} tỷ VNĐ",
                "price_per_m2_formatted": f"{price_per_m2:.1f} triệu/m²"
            }
        )

        return {
            "status": "success",
            "model_name": model_key,
            "display_name": specs.get("display_name", model_key),
            "badge": specs.get("badge", ""),
            "price_billion": pred_price,
            "price_formatted": f"{pred_price:.2f} tỷ VNĐ",
            "price_per_m2_million": round(price_per_m2, 1),
            "price_per_m2_formatted": f"{price_per_m2:.1f} triệu/m²",
            "metrics": {
                "rmse": specs.get("rmse"),
                "mae": specs.get("mae"),
                "r2": specs.get("r2"),
                "mape": specs.get("mape")
            },
            "financial_package": kg_res.get("financial_package"),
            "amenities": kg_res.get("amenities"),
            "knowledge_graph": kg_res.get("graph"),
            "broker_hotline": kg_res.get("broker_hotline"),
            "description": specs.get("desc", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi định giá: {str(e)}")


@app.post("/api/predict-all")
async def predict_all_models(house: HouseInput):
    """Predict price across all 5 models simultaneously."""
    current_models = ensure_models_loaded()
    
    data_dict = house.model_dump(by_alias=True)
    data_dict.pop("model_name", None)
    
    features_df = prepare_input_dataframe(data_dict)
    area = max(1.0, float(data_dict.get("Area", 50.0)))
    
    results = []
    prices = []
    
    for name, pipeline in current_models.items():
        try:
            pred = float(pipeline.predict(features_df)[0])
            pred = max(0.5, round(pred, 2))
            prices.append(pred)
            specs = MODEL_SPECS.get(name, {})
            price_m2 = (pred * 1000.0) / area
            
            results.append({
                "model_name": name,
                "display_name": specs.get("display_name", name),
                "badge": specs.get("badge", ""),
                "price_billion": pred,
                "price_formatted": f"{pred:.2f} tỷ VNĐ",
                "price_per_m2_formatted": f"{price_m2:.1f} triệu/m²",
                "rmse": specs.get("rmse", 0),
                "r2": specs.get("r2", 0),
                "is_best": (name == "XGBoost")
            })
        except Exception as e:
            print(f"Error predicting with {name}: {e}")
            
    # Sort by RMSE ascending (best first)
    results = sorted(results, key=lambda x: x["rmse"])
    
    avg_price = float(np.mean(prices)) if prices else 0
    min_price = min(prices) if prices else 0
    max_price = max(prices) if prices else 0
    
    return {
        "status": "success",
        "results": results,
        "summary": {
            "average_billion": round(avg_price, 2),
            "average_formatted": f"{avg_price:.2f} tỷ VNĐ",
            "min_billion": round(min_price, 2),
            "max_billion": round(max_price, 2),
            "price_range": f"{min_price:.2f} - {max_price:.2f} tỷ VNĐ"
        }
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 [Week 2] Khởi chạy máy chủ Web dự đoán Giá nhà tại: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
