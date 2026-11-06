"""
Knowledge Graph Engine for Diabetes Clinical Care & FPT Long Châu Pharmacy Ecosystem.
Provides semantic ontology, medical reasoning, and graph mapping for personalized healthcare packages.
"""

from typing import Dict, Any, List

# Long Châu Healthcare Knowledge Base
LONG_CHAU_KB = {
    "disease": {
        "id": "DIS_E11",
        "code": "E11",
        "name": "Đái tháo đường Type 2",
        "icd10": "E11",
        "slug": "dai-thao-duong",
        "url": "https://nhathuoclongchau.com.vn/benh/dai-thao-duong-42.html",
        "desc": "Bệnh lý rối loạn chuyển hóa mạn tính do giảm tiết insulin hoặc đề kháng insulin."
    },
    "medical_devices": [
        {
            "id": "DEV_01",
            "name": "Máy đo đường huyết Accu-Chek Instant",
            "brand": "Roche (Đức)",
            "price_vnd": 950000,
            "price_formatted": "950.000 đ",
            "tag": "Thiết bị y tế",
            "category": "Máy đo đường huyết",
            "benefit": "Độ chính xác chuẩn quốc tế ISO 15197:2013, kết quả trong 4 giây.",
            "url": "https://nhathuoclongchau.com.vn/thiet-bi-y-te/may-do-duong-huyet-accu-chek-instant-32145.html"
        },
        {
            "id": "DEV_02",
            "name": "Que thử đường huyết Accu-Chek Instant (Hộp 50 que)",
            "brand": "Roche (Đức)",
            "price_vnd": 360000,
            "price_formatted": "360.000 đ",
            "tag": "Vật tư y tế",
            "category": "Que thử đường huyết",
            "benefit": "Vùng hút máu rộng, tự động hút máu nhanh không đau.",
            "url": "https://nhathuoclongchau.com.vn/thiet-bi-y-te/que-thu-duong-huyet-accu-chek-instant-50-que-32146.html"
        },
        {
            "id": "DEV_03",
            "name": "Máy đo huyết áp bắp tay tự động Omron HEM-7120",
            "brand": "Omron (Nhật Bản)",
            "price_vnd": 850000,
            "price_formatted": "850.000 đ",
            "tag": "Thiết bị y tế",
            "category": "Máy đo huyết áp",
            "benefit": "Công nghệ Intellisense tự động bơm khí theo kích thước bắp tay.",
            "url": "https://nhathuoclongchau.com.vn/thiet-bi-y-te/may-do-huyet-ap-bap-tay-omron-hem-7120-15342.html"
        }
    ],
    "supplements": [
        {
            "id": "SUP_01",
            "name": "Sữa bột Abbott Glucerna 850g",
            "brand": "Abbott (Hoa Kỳ)",
            "price_vnd": 865000,
            "price_formatted": "865.000 đ",
            "tag": "Dinh dưỡng y học",
            "category": "Sữa chuyên biệt tiểu đường",
            "benefit": "Hệ bột đường giải phóng chậm Triple Care giúp ổn định đường huyết sau uống.",
            "url": "https://nhathuoclongchau.com.vn/thuc-pham-chuc-nang/sua-bot-abbott-glucerna-850g-18234.html"
        },
        {
            "id": "SUP_02",
            "name": "Viên uống Dây thìa canh Diabetna (Hộp 40 viên)",
            "brand": "Nam Dược (Việt Nam)",
            "price_vnd": 115000,
            "price_formatted": "115.000 đ",
            "tag": "Thảo dược",
            "category": "Hạ đường huyết tự nhiên",
            "benefit": "Chuẩn hóa 100% dây thìa canh chuẩn GACP-WHO, hỗ trợ giảm HbA1c.",
            "url": "https://nhathuoclongchau.com.vn/thuc-pham-chuc-nang/vien-uong-day-thia-canh-diabetna-hop-40-vien-2914.html"
        },
        {
            "id": "SUP_03",
            "name": "Đường ăn kiêng cỏ ngọt Equal Stevia (Hộp 50 gói)",
            "brand": "Equal (Mỹ)",
            "price_vnd": 78000,
            "price_formatted": "78.000 đ",
            "tag": "Thực phẩm ăn kiêng",
            "category": "Đường không sinh năng lượng",
            "benefit": "0 Calorie, thay thế đường kính cho người cần kiểm soát calo và đường huyết.",
            "url": "https://nhathuoclongchau.com.vn/thuc-pham-chuc-nang/duong-an-kieng-equal-stevia-50-goi-3312.html"
        }
    ],
    "medications_ref": [
        {
            "id": "MED_01",
            "name": "Glucophage 500mg (Hộp 50 viên)",
            "active": "Metformin HCl",
            "note": "Thuốc kê đơn — Cần có chỉ định của Bác sĩ chuyên khoa.",
            "price_vnd": 115000,
            "price_formatted": "115.000 đ"
        },
        {
            "id": "MED_02",
            "name": "Diamicron MR 60mg (Hộp 60 viên)",
            "active": "Gliclazide",
            "note": "Thuốc kê đơn — Kích thích tuyến tụy bài tiết insulin.",
            "price_vnd": 210000,
            "price_formatted": "210.000 đ"
        }
    ],
    "stores": [
        {
            "name": "Nhà thuốc FPT Long Châu — 123 Quang Trung, Gò Vấp, TP.HCM",
            "city": "Hồ Chí Minh",
            "district": "Gò Vấp",
            "hotline": "1800 6928 (Miễn phí)"
        },
        {
            "name": "Nhà thuốc FPT Long Châu — 45 Trần Thái Tông, Cầu Giấy, Hà Nội",
            "city": "Hà Nội",
            "district": "Cầu Giấy",
            "hotline": "1800 6928 (Miễn phí)"
        },
        {
            "name": "Nhà thuốc FPT Long Châu — 88 Nguyễn Văn Linh, Hải Châu, Đà Nẵng",
            "city": "Đà Nẵng",
            "district": "Hải Châu",
            "hotline": "1800 6928 (Miễn phí)"
        }
    ]
}


def build_patient_knowledge_graph(
    patient_id: str,
    patient_data: Dict[str, Any],
    pred_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Construct dynamic graph nodes and edges for Neo4j / UI visualization
    connecting patient metrics, AI prediction, clinical risks, and Long Châu recommendations.
    """
    prob = pred_result.get("diabetic_probability", 0.0)
    outcome = pred_result.get("prediction", 0)
    glucose = patient_data.get("Glucose", 100)
    bmi = patient_data.get("BMI", 25.0)
    age = patient_data.get("Age", 30)

    nodes = []
    edges = []

    # 1. Patient Node (Center Left)
    nodes.append({
        "id": "patient",
        "label": f"Bệnh nhân ({age} tuổi)",
        "group": "patient",
        "color": "#2563eb",
        "size": 28,
        "details": f"Tuổi: {age} | Glucose: {glucose} mg/dL | BMI: {bmi}"
    })

    # 2. Prediction Node
    pred_color = "#dc2626" if prob >= 60 else ("#d97706" if prob >= 35 else "#16a34a")
    nodes.append({
        "id": "prediction",
        "label": f"AI: {prob}% ({pred_result.get('model_name', 'XGBoost')})",
        "group": "prediction",
        "color": pred_color,
        "size": 26,
        "details": f"Xác suất mắc bệnh: {prob}% — {pred_result.get('status_text', '')}"
    })
    edges.append({
        "from": "patient",
        "to": "prediction",
        "label": "ĐƯỢC_DỰ_ĐOÁN",
        "color": "#94a3b8"
    })

    # 3. Biomarker Nodes
    nodes.append({
        "id": "bio_glucose",
        "label": f"Glucose ({glucose} mg/dL)",
        "group": "biomarker",
        "color": "#ef4444" if glucose >= 140 else "#10b981",
        "size": 20,
        "details": f"Đường huyết: {glucose} mg/dL ({'Vượt chuẩn' if glucose >= 140 else 'Bình thường'})"
    })
    edges.append({
        "from": "patient",
        "to": "bio_glucose",
        "label": "CHỈ_SỐ_ĐO",
        "color": "#cbd5e1"
    })

    nodes.append({
        "id": "bio_bmi",
        "label": f"BMI ({bmi} kg/m²)",
        "group": "biomarker",
        "color": "#f59e0b" if bmi >= 25 else "#10b981",
        "size": 20,
        "details": f"Chỉ số BMI: {bmi} ({'Thừa cân / Béo phì' if bmi >= 25 else 'Bình thường'})"
    })
    edges.append({
        "from": "patient",
        "to": "bio_bmi",
        "label": "CHỈ_SỐ_ĐO",
        "color": "#cbd5e1"
    })

    # 4. Disease Node & Risk Factors
    nodes.append({
        "id": "disease",
        "label": "Đái tháo đường T2 (E11)",
        "group": "disease",
        "color": "#7c3aed",
        "size": 30,
        "details": "Bệnh lý chuyển hóa mạn tính — ICD-10: E11"
    })

    if prob >= 35.0:
        edges.append({
            "from": "prediction",
            "to": "disease",
            "label": f"CẢNH_BÁO_NGUY_CƠ ({prob}%)",
            "color": pred_color
        })

    # 5. Long Châu Care Package Nodes (Devices, Supplements, Pharmacist)
    recommended_devices = []
    recommended_supplements = []

    if prob >= 60.0:
        # High Risk -> Full monitoring bundle
        recommended_devices = [LONG_CHAU_KB["medical_devices"][0], LONG_CHAU_KB["medical_devices"][1]]
        recommended_supplements = [LONG_CHAU_KB["supplements"][0], LONG_CHAU_KB["supplements"][1]]
    elif prob >= 35.0:
        # Borderline -> Screening & Herbal
        recommended_devices = [LONG_CHAU_KB["medical_devices"][0]]
        recommended_supplements = [LONG_CHAU_KB["supplements"][1], LONG_CHAU_KB["supplements"][2]]
    else:
        # Healthy -> Wellness & preventive diet
        recommended_supplements = [LONG_CHAU_KB["supplements"][2]]

    for dev in recommended_devices:
        nodes.append({
            "id": dev["id"],
            "label": dev["name"][:22] + "...",
            "group": "device",
            "color": "#0284c7",
            "size": 22,
            "details": f"{dev['name']} — Giá: {dev['price_formatted']} ({dev['brand']})"
        })
        edges.append({
            "from": "disease",
            "to": dev["id"],
            "label": "THEO_DÕI_TẠI_NHÀ",
            "color": "#0284c7"
        })
        edges.append({
            "from": "patient",
            "to": dev["id"],
            "label": "GỢI_Ý_MUA",
            "color": "#0284c7"
        })

    for sup in recommended_supplements:
        nodes.append({
            "id": sup["id"],
            "label": sup["name"][:22] + "...",
            "group": "supplement",
            "color": "#059669",
            "size": 22,
            "details": f"{sup['name']} — Giá: {sup['price_formatted']}"
        })
        edges.append({
            "from": "disease",
            "to": sup["id"],
            "label": "DINH_DƯỠNG_BỔ_TRỢ",
            "color": "#059669"
        })
        edges.append({
            "from": "patient",
            "to": sup["id"],
            "label": "KHUYÊN_DÙNG",
            "color": "#059669"
        })

    # Store Node
    store = LONG_CHAU_KB["stores"][0]
    nodes.append({
        "id": "store_01",
        "label": "Nhà thuốc Long Châu",
        "group": "store",
        "color": "#ea580c",
        "size": 24,
        "details": f"{store['name']} — Hotline: {store['hotline']}"
    })
    edges.append({
        "from": "patient",
        "to": "store_01",
        "label": "ĐIỂM_TƯ_VẤN_GẦN_NHẤT",
        "color": "#ea580c"
    })

    return {
        "graph": {
            "nodes": nodes,
            "edges": edges
        },
        "care_package": {
            "risk_level": "Nguy cơ cao" if prob >= 60 else ("Tiền tiểu đường" if prob >= 35 else "Khỏe mạnh"),
            "devices": recommended_devices,
            "supplements": recommended_supplements,
            "store": store,
            "hotline": "1800 6928"
        }
    }
