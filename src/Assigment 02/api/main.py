from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
import re

app = FastAPI(
    title="Intelligent Systems API",
    description="REST API for Diabetes, House Price, and Customer Behavior Prediction.",
    version="1.0.0"
)

# Allow CORS for Web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIABETES_MODEL_DIR = os.path.join(BASE_DIR, 'diabetes', 'model')
HOUSE_MODEL_DIR = os.path.join(BASE_DIR, 'house_price', 'model')
ECOM_MODEL_DIR = os.path.join(BASE_DIR, 'customer_behavior', 'model')

# Global variables for models
diabetes_prep = None
diabetes_models = {}
diabetes_meta = None

house_prep = None
house_model = None

ecom_prep = None
ecom_models = None

@app.on_event("startup")
def load_models():
    global diabetes_prep, diabetes_model, diabetes_meta
    global house_prep, house_model
    global ecom_prep, ecom_models
    
    # Load Diabetes
    try:
        diabetes_prep = joblib.load(os.path.join(DIABETES_MODEL_DIR, 'preprocessor.joblib'))
        diabetes_models['hist_gb'] = joblib.load(os.path.join(DIABETES_MODEL_DIR, 'model.joblib'))
        diabetes_models['lr'] = joblib.load(os.path.join(DIABETES_MODEL_DIR, 'model_lr.joblib'))
        diabetes_models['rf'] = joblib.load(os.path.join(DIABETES_MODEL_DIR, 'model_rf.joblib'))
        import json
        with open(os.path.join(DIABETES_MODEL_DIR, 'metadata.json'), 'r') as f:
            diabetes_meta = json.load(f)
    except Exception as e:
        print("Could not load Diabetes models:", e)
        
    # Load House Price
    try:
        house_prep = joblib.load(os.path.join(HOUSE_MODEL_DIR, 'preprocessor.joblib'))
        house_model = joblib.load(os.path.join(HOUSE_MODEL_DIR, 'model.joblib'))
    except Exception as e:
        print("Could not load House Price models:", e)
        
    # Load Customer Behavior
    try:
        ecom_prep = joblib.load(os.path.join(ECOM_MODEL_DIR, 'preprocessor.joblib'))
        ecom_models = joblib.load(os.path.join(ECOM_MODEL_DIR, 'dual_models.joblib'))
    except Exception as e:
        print("Could not load Customer Behavior models:", e)

# ==========================================
# 1. DIABETES PREDICTION
# ==========================================
class DiabetesInput(BaseModel):
    gender: str
    age: float
    hypertension: int
    heart_disease: int
    smoking_history: str
    bmi: float
    HbA1c_level: float
    blood_glucose_level: float
    model_name: str = "hist_gb"

@app.post("/api/v1/diabetes/predict")
def predict_diabetes(data: DiabetesInput):
    if not diabetes_models:
        raise HTTPException(status_code=500, detail="Diabetes models not loaded.")
        
    model = diabetes_models.get(data.model_name)
    if not model:
        raise HTTPException(status_code=400, detail="Model not found.")
    
    df_in = pd.DataFrame([data.dict(exclude={'model_name'})])
    # Compute interaction features
    df_in['glucose_hba1c_interaction'] = df_in['blood_glucose_level'] * df_in['HbA1c_level']
    df_in['age_hypertension_risk'] = df_in['age'] * df_in['hypertension']
    
    # Preprocess
    X_trans = diabetes_prep.transform(df_in)
    
    # Predict
    prob = model.predict_proba(X_trans)[0, 1]
    
    # HistGB used a specific threshold, others use 0.5 default or we just use 0.5 for LR/RF
    threshold = 0.5
    if data.model_name == "hist_gb":
        threshold = diabetes_meta.get('decision_threshold', 0.5)
        
    pred_class = 1 if prob >= threshold else 0
    
    # Decision Support & Clinical Advisory
    clinical_flags = []
    
    # HbA1c assessment
    if data.HbA1c_level >= 6.5:
        clinical_flags.append({"param": "Chỉ số HbA1c", "value": f"{data.HbA1c_level}%", "status": "danger", "note": "Vượt ngưỡng chẩn đoán ĐTĐ (≥ 6.5%)"})
    elif data.HbA1c_level >= 5.7:
        clinical_flags.append({"param": "Chỉ số HbA1c", "value": f"{data.HbA1c_level}%", "status": "warning", "note": "Giai đoạn Tiền đái tháo đường (5.7 - 6.4%)"})
    else:
        clinical_flags.append({"param": "Chỉ số HbA1c", "value": f"{data.HbA1c_level}%", "status": "normal", "note": "Trong giới hạn bình thường (< 5.7%)"})
        
    # Glucose assessment
    if data.blood_glucose_level >= 126:
        clinical_flags.append({"param": "Đường huyết", "value": f"{data.blood_glucose_level} mg/dL", "status": "danger", "note": "Đường huyết lúc đói tăng cao (≥ 126 mg/dL)"})
    elif data.blood_glucose_level >= 100:
        clinical_flags.append({"param": "Đường huyết", "value": f"{data.blood_glucose_level} mg/dL", "status": "warning", "note": "Rối loạn đường huyết đói (100 - 125 mg/dL)"})
    else:
        clinical_flags.append({"param": "Đường huyết", "value": f"{data.blood_glucose_level} mg/dL", "status": "normal", "note": "Mức sinh lý bình thường (< 100 mg/dL)"})
        
    # BMI assessment
    if data.bmi >= 30:
        clinical_flags.append({"param": "Thể trạng (BMI)", "value": f"{data.bmi}", "status": "danger", "note": "Béo phì (tăng kháng insulin)"})
    elif data.bmi >= 25:
        clinical_flags.append({"param": "Thể trạng (BMI)", "value": f"{data.bmi}", "status": "warning", "note": "Thừa cân (cần kiểm soát cân nặng)"})
    else:
        clinical_flags.append({"param": "Thể trạng (BMI)", "value": f"{data.bmi}", "status": "normal", "note": "Thể trạng cân đối"})
        
    # Cardiovascular & Lifestyle
    comorb = []
    if data.hypertension: comorb.append("Tăng huyết áp")
    if data.heart_disease: comorb.append("Bệnh tim mạch")
    if data.smoking_history in ['current', 'ever', 'former']: comorb.append(f"Hút thuốc ({data.smoking_history})")
    
    if comorb:
        clinical_flags.append({"param": "Yếu tố phối hợp", "value": ", ".join(comorb), "status": "warning", "note": "Gia tăng rủi ro biến chứng mạch máu"})
    else:
        clinical_flags.append({"param": "Yếu tố phối hợp", "value": "Không ghi nhận", "status": "normal", "note": "Không có bệnh nền tim mạch/hút thuốc"})

    # Actionable Recommendations
    if pred_class == 1:
        lifestyle = [
            "Dinh dưỡng: Hạn chế carbohydrate đơn (đường, bánh ngọt, nước có gas); tăng chất xơ hòa tan từ rau xanh và ngũ cốc nguyên hạt để làm chậm hấp thu glucose.",
            "Vận động: Đạt tối thiểu 150 phút/tuần hoạt động thể lực cường độ vừa (như đi bộ nhanh 30 phút/ngày, 5 ngày/tuần).",
            "Mục tiêu cân nặng: Đặt lộ trình giảm 5 - 7% thể trọng trong 3 tháng để phục hồi độ nhạy insulin ngoại vi."
        ]
        clinical_action = [
            "Chỉ định cận lâm sàng: Khuyến nghị xét nghiệm khẳng định (lặp lại HbA1c và đường huyết tương tĩnh mạch lúc đói hoặc nghiệm pháp OGTT 75g).",
            "Tầm soát biến chứng mục tiêu: Kiểm tra định kỳ đáy mắt (võng mạc), vi đạm niệu (thận) và kiểm tra mạch máu/cảm giác bàn chân.",
            "Kế hoạch theo dõi: Thiết lập sổ theo dõi đường huyết mao mạch tại nhà 2 lần/tuần trước bữa ăn."
        ]
    else:
        lifestyle = [
            "Dinh dưỡng: Tiếp tục duy trì chế độ ăn cân bằng dinh dưỡng, kiểm soát khẩu phần muối và đường tinh luyện.",
            "Vận động: Duy trì thói quen tập luyện thể thao ít nhất 3 - 4 buổi mỗi tuần để bảo vệ hệ tim mạch.",
            "Lối sống: Đảm bảo giấc ngủ đủ 7 - 8 tiếng/ngày và tránh căng thẳng thần kinh kéo dài."
        ]
        clinical_action = [
            "Tầm soát định kỳ: Khám sức khỏe tổng quát và làm xét nghiệm đường huyết/HbA1c định kỳ 6 - 12 tháng/lần.",
            "Duy trì chỉ số BMI trong ngưỡng lý tưởng từ 18.5 đến 22.9 theo chuẩn người châu Á."
        ]

    return {
        "prediction_class": pred_class,
        "risk_level": "High" if pred_class == 1 else "Low",
        "message": "Cảnh báo Nguy cơ Tiểu đường CAO" if pred_class == 1 else "Nguy cơ Tiểu đường THẤP",
        "probability": float(prob),
        "threshold": float(threshold),
        "clinical_flags": clinical_flags,
        "lifestyle_recommendations": lifestyle,
        "clinical_actions": clinical_action
    }

# ==========================================
# 2. HOUSE PRICE PREDICTION
# ==========================================
class HouseInput(BaseModel):
    house_size: float
    bed: float
    bath: float
    acre_lot: float
    city: str
    state: str
    zip_code: float

@app.post("/api/v1/house-price/predict")
def predict_house(data: HouseInput):
    if not house_model:
        raise HTTPException(status_code=500, detail="House Price model not loaded.")
    
    gm = house_prep['global_mean']
    gsm = house_prep['global_size_mean']
    
    zip3 = int(data.zip_code // 100)
    log_size = np.log(data.house_size)
    log_acre = np.log1p(data.acre_lot)
    tot_rooms = data.bed + data.bath
    sqft_rm = data.house_size / tot_rooms if tot_rooms > 0 else 0
    b_b_ratio = data.bath / data.bed if data.bed > 0 else 0
    b_b_prod = data.bed * data.bath
    
    st_enc = house_prep['state_enc'].get(data.state, gm)
    z3_enc = house_prep['zip3_enc'].get(zip3, gm)
    zp_enc = house_prep['zip_enc'].get(data.zip_code, gm)
    ct_enc = house_prep['city_enc'].get(data.city, gm)
    
    zip_sz = house_prep['zip_size_mean'].get(data.zip_code, gsm)
    rel_sqft = data.house_size / zip_sz if zip_sz > 0 else 1.0
    
    vec = np.array([[
        log_size, data.bed, data.bath, tot_rooms, b_b_prod,
        sqft_rm, b_b_ratio, log_acre, rel_sqft, st_enc, z3_enc, zp_enc, ct_enc
    ]])
    
    pred_log = house_model.predict(vec)[0]
    est_price = float(np.exp(pred_log))
    
    # Market Context & Segment
    if est_price >= 850000:
        segment = "Phân khúc Cao cấp (Luxury Asset)"
    elif est_price >= 350000:
        segment = "Phân khúc Trung cấp (Mid-tier Residential)"
    else:
        segment = "Phân khúc Phổ thông (Affordable Housing)"
        
    local_benchmark = float(np.exp(ct_enc))
    price_diff_pct = ((est_price - local_benchmark) / local_benchmark) * 100
    
    if abs(price_diff_pct) < 5:
        market_position = f"Sát mặt bằng chung thị trường tại {data.city} (chênh lệch {price_diff_pct:+.1f}%)"
    elif price_diff_pct > 0:
        market_position = f"Cao hơn {abs(price_diff_pct):.1f}% so với giá nhà bình quân tại {data.city}"
    else:
        market_position = f"Thấp hơn {abs(price_diff_pct):.1f}% so với giá nhà bình quân tại {data.city} (tiềm năng cạnh tranh tốt)"
        
    sqft_per_room = data.house_size / tot_rooms if tot_rooms > 0 else 0
    layout_eval = "Không gian phòng rộng rãi, độ thông thoáng cao" if sqft_per_room >= 350 else "Mật độ bố trí phòng tối ưu, phù hợp gia đình trẻ"
    
    # Strategy advice
    listing_min = est_price * 0.97
    listing_max = est_price * 1.04
    buyer_target = est_price * 0.93
    
    return {
        "predicted_price_usd": est_price,
        "price_formatted": f"${est_price:,.0f}",
        "price_per_sqft": f"${est_price/data.house_size:,.1f} / sqft",
        "segment": segment,
        "market_position": market_position,
        "layout_evaluation": layout_eval,
        "strategic_advisory": {
            "listing_range": f"${listing_min:,.0f} - ${listing_max:,.0f}",
            "buyer_target": f"${buyer_target:,.0f}",
            "liquidity_timeline": "Dự kiến 30 - 45 ngày nếu niêm yết trong khoảng giá đề xuất"
        }
    }

# ==========================================
# 3. CUSTOMER BEHAVIOR & CATEGORY DISCOVERY
# ==========================================
class ReviewInput(BaseModel):
    review_text: str

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.post("/api/v1/customer-behavior/predict")
def predict_behavior(data: ReviewInput):
    if not ecom_models:
        raise HTTPException(status_code=500, detail="Customer Behavior models not loaded.")
        
    cleaned = clean_text(data.review_text)
    vec = ecom_prep['tfidf_vectorizer'].transform([cleaned])
    
    # Task 1: Sentiment
    model_t1 = ecom_models['task1']
    pred_t1 = int(model_t1.predict(vec)[0])
    
    # Task 2: Category Discovery
    model_t2 = ecom_models['task2']
    pred_t2_id = model_t2.predict(vec)[0]
    category = ecom_prep['label_encoder'].inverse_transform([pred_t2_id])[0]
    
    # Extract Sentiment Driver Keywords
    pos_lexicon = {'love', 'perfect', 'comfortable', 'flattering', 'beautiful', 'great', 'soft', 'favorite', 'compliments', 'recommend', 'nice', 'gorgeous'}
    neg_lexicon = {'returned', 'disappointed', 'cheap', 'poor', 'unflattering', 'small', 'tight', 'scratchy', 'bad', 'huge', 'horrible', 'thin', 'waste'}
    
    words = set(cleaned.split())
    found_pos = list(words.intersection(pos_lexicon))
    found_neg = list(words.intersection(neg_lexicon))
    
    if pred_t1 == 1:
        sentiment = "Hài lòng (Khuyên mua)"
        key_signals = found_pos if found_pos else ["Tín hiệu hài lòng tổng thể"]
        crm_action = {
            "priority": "Khách hàng Tiềm năng (Loyalty & Retention)",
            "immediate_action": "Tự động gửi thông điệp cảm ơn và lời mời để lại ảnh review thực tế để tích 50 điểm thành viên VIP.",
            "commercial_strategy": f"Kích hoạt thuật toán Recommender System đề xuất phụ kiện phối đồ cùng dòng sản phẩm {category} (giày dép, túi xách, khăn quàng).",
            "marketing_action": f"Gắn nhãn tệp người dùng yêu thích danh mục {category} để đưa vào chiến dịch Retargeting bộ sưu tập mùa mới."
        }
    else:
        sentiment = "Thất vọng (Không khuyên mua)"
        key_signals = found_neg if found_neg else ["Tín hiệu trải nghiệm chưa đạt kỳ vọng"]
        crm_action = {
            "priority": "Khẩn cấp - Nguy cơ mất khách (Churn Risk)",
            "immediate_action": "Kích hoạt Ticket hỗ trợ 1-1: Gửi email tự động xin lỗi kèm đường link tạo đơn đổi size / hoàn hàng miễn phí trong 7 ngày.",
            "commercial_strategy": "Tặng mã Voucher giảm 15% (Mã: CARE15) áp dụng cho đơn hàng kế tiếp để phục hồi lòng tin khách hàng.",
            "marketing_action": f"Tự động chuyển tiếp trích đoạn phản hồi tới Trưởng bộ phận Đảm bảo Chất lượng (QC) ngành hàng {category} để kiểm tra form may và chất liệu vải."
        }
    
    return {
        "sentiment_prediction": sentiment,
        "sentiment_class": pred_t1,
        "category_prediction": category,
        "key_signals": key_signals,
        "crm_action_plan": crm_action
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
