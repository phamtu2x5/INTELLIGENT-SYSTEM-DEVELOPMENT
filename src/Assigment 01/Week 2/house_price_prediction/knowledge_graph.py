"""
Knowledge Graph Engine for Real Estate Valuation, Urban Infrastructure & Mortgage Loans (Week 2)
Provides semantic ontology, spatial amenities mapping, and bank loan simulation for property buyers.
"""

from typing import Dict, Any, List
import math

# Urban Amenities & Infrastructure Knowledge Base by Region
AMENITIES_KB = {
    "Hồ Chí Minh": {
        "Gò Vấp": [
            {"name": "Vincom Plaza Phan Văn Trị", "type": "TTTM", "distance": "1.2 km", "icon": "🛍️"},
            {"name": "Công viên Gia Định (32ha)", "type": "Công viên", "distance": "2.0 km", "icon": "🌳"},
            {"name": "Bệnh viện Quân Y 175", "type": "Bệnh viện", "distance": "2.5 km", "icon": "🏥"},
            {"name": "Tuyến Metro số 2 (Bến Thành - Tham Lương)", "type": "Quy hoạch Metro", "distance": "1.8 km", "icon": "🚆"}
        ],
        "Quận 1": [
            {"name": "Vincom Center Đồng Khởi", "type": "TTTM", "distance": "0.5 km", "icon": "🛍️"},
            {"name": "Tuyến Metro số 1 (Ga Nhà Hát TP)", "type": "Metro", "distance": "0.4 km", "icon": "🚆"},
            {"name": "Bệnh viện Đa khoa Sài Gòn", "type": "Bệnh viện", "distance": "0.8 km", "icon": "🏥"},
            {"name": "Phố đi bộ Nguyễn Huệ", "type": "Cảnh quan", "distance": "0.6 km", "icon": "🌆"}
        ],
        "Quận 7": [
            {"name": "TTTM Crescent Mall & SC VivoCity", "type": "TTTM", "distance": "1.0 km", "icon": "🛍️"},
            {"name": "Đại học Quốc tế RMIT", "type": "Giáo dục", "distance": "1.5 km", "icon": "🎓"},
            {"name": "Bệnh viện Quốc tế FV & Tâm Đức", "type": "Bệnh viện", "distance": "1.2 km", "icon": "🏥"},
            {"name": "Hồ Bán Nguyệt & Cầu Ánh Sao", "type": "Công viên", "distance": "0.9 km", "icon": "🌳"}
        ],
        "Thủ Đức": [
            {"name": "Tuyến Metro số 1 (Ga Thảo Điền)", "type": "Metro", "distance": "0.6 km", "icon": "🚆"},
            {"name": "Vincom Mega Mall Thảo Điền", "type": "TTTM", "distance": "0.7 km", "icon": "🛍️"},
            {"name": "Trường Quốc tế Anh BIS", "type": "Giáo dục", "distance": "1.1 km", "icon": "🎓"},
            {"name": "Khu đô thị Đại học Quốc gia TP.HCM", "type": "Giáo dục", "distance": "3.5 km", "icon": "📚"}
        ]
    },
    "Hà Nội": {
        "Cầu Giấy": [
            {"name": "Tuyến Metro Nhổn - Ga Hà Nội (Ga Cầu Giấy)", "type": "Metro", "distance": "0.8 km", "icon": "🚆"},
            {"name": "Công viên Cầu Giấy (10ha)", "type": "Công viên", "distance": "1.0 km", "icon": "🌳"},
            {"name": "Bệnh viện 19-8 Bộ Công An", "type": "Bệnh viện", "distance": "1.8 km", "icon": "🏥"},
            {"name": "Đại học Quốc gia Hà Nội & Sư Phạm", "type": "Giáo dục", "distance": "1.2 km", "icon": "🎓"}
        ],
        "Thanh Xuân": [
            {"name": "Tuyến Đường sắt trên cao Cát Linh - Hà Đông", "type": "Metro", "distance": "0.5 km", "icon": "🚆"},
            {"name": "TTTM Royal City Mega Mall", "type": "TTTM", "distance": "1.2 km", "icon": "🛍️"},
            {"name": "Bệnh viện Đại học Y Hà Nội", "type": "Bệnh viện", "distance": "2.0 km", "icon": "🏥"},
            {"name": "Đại học Khoa học Tự nhiên & KHXH&NV", "type": "Giáo dục", "distance": "1.0 km", "icon": "🎓"}
        ],
        "Hoàn Kiếm": [
            {"name": "Hồ Hoàn Kiếm & Phố Cổ", "type": "Cảnh quan", "distance": "0.3 km", "icon": "🌆"},
            {"name": "Tràng Tiền Plaza", "type": "TTTM", "distance": "0.5 km", "icon": "🛍️"},
            {"name": "Bệnh viện Hữu nghị Việt Đức", "type": "Bệnh viện", "distance": "0.7 km", "icon": "🏥"},
            {"name": "Bệnh viện Phụ sản Trung ương", "type": "Bệnh viện", "distance": "0.9 km", "icon": "🏥"}
        ]
    },
    "Hưng Yên": {
        "Văn Giang": [
            {"name": "Đại đô thị Ecopark & Hồ Thiên Nga (50ha)", "type": "Sinh thái", "distance": "0.5 km", "icon": "🌳"},
            {"name": "Trường Quốc tế Chadwick & BUV", "type": "Giáo dục", "distance": "1.2 km", "icon": "🎓"},
            {"name": "Bệnh viện Quốc tế Kusumi (ĐH Y Tokyo)", "type": "Bệnh viện", "distance": "1.5 km", "icon": "🏥"},
            {"name": "Đường Vành đai 3.5 & Cầu Mễ Sở (Quy hoạch)", "type": "Hạ tầng", "distance": "2.0 km", "icon": "🛣️"}
        ]
    },
    "Bình Dương": {
        "Dĩ An": [
            {"name": "Bến xe Miền Đông Mới & Ga Metro số 1", "type": "Giao thông", "distance": "2.0 km", "icon": "🚆"},
            {"name": "Khu Đô thị Đại học Quốc gia TP.HCM", "type": "Giáo dục", "distance": "1.5 km", "icon": "🎓"},
            {"name": "TTTM Vincom Plaza Dĩ An", "type": "TTTM", "distance": "1.8 km", "icon": "🛍️"},
            {"name": "Bệnh viện Đa khoa Quốc tế Hoàn Mỹ", "type": "Bệnh viện", "distance": "2.2 km", "icon": "🏥"}
        ]
    }
}

# Partner Banks Mortgage Programs
PARTNER_BANKS = [
    {
        "id": "TCB",
        "bank_name": "Techcombank",
        "logo_text": "Techcombank",
        "max_ltv_pct": 75,
        "preferential_rate_pct": 6.8,
        "tenure_years": 35,
        "grace_period_months": 24,
        "highlight": "Ân hạn gốc 24 tháng, thời hạn vay đến 35 năm."
    },
    {
        "id": "VCB",
        "bank_name": "Vietcombank",
        "logo_text": "Vietcombank",
        "max_ltv_pct": 70,
        "preferential_rate_pct": 6.5,
        "tenure_years": 25,
        "grace_period_months": 12,
        "highlight": "Lãi suất ưu đãi thấp nhất Big4, thủ tục minh bạch."
    },
    {
        "id": "VPB",
        "bank_name": "VPBank",
        "logo_text": "VPBank",
        "max_ltv_pct": 80,
        "preferential_rate_pct": 7.2,
        "tenure_years": 30,
        "grace_period_months": 12,
        "highlight": "Hạn mức tài trợ tới 80%, duyệt hồ sơ trực tuyến 2h."
    }
]


def calculate_mortgage(price_billion: float, ltv_pct: float = 70.0, rate_pct: float = 6.8, tenure_years: int = 25) -> Dict[str, Any]:
    """Calculate monthly installment and loan parameters."""
    loan_amount_billion = price_billion * (ltv_pct / 100.0)
    equity_billion = price_billion - loan_amount_billion
    
    # Monthly interest
    monthly_rate = (rate_pct / 100.0) / 12.0
    num_months = tenure_years * 12
    
    # Principal per month (Linear method)
    principal_monthly_mil = (loan_amount_billion * 1000.0) / num_months
    # First month interest
    interest_first_month_mil = (loan_amount_billion * 1000.0) * monthly_rate
    total_first_month_mil = principal_monthly_mil + interest_first_month_mil
    
    return {
        "loan_amount_billion": round(loan_amount_billion, 2),
        "loan_amount_formatted": f"{loan_amount_billion:.2f} tỷ VNĐ",
        "equity_billion": round(equity_billion, 2),
        "equity_formatted": f"{equity_billion:.2f} tỷ VNĐ",
        "ltv_pct": ltv_pct,
        "rate_pct": rate_pct,
        "tenure_years": tenure_years,
        "monthly_estimate_mil": round(total_first_month_mil, 1),
        "monthly_estimate_formatted": f"{total_first_month_mil:.1f} triệu/tháng",
        "principal_monthly_formatted": f"{principal_monthly_mil:.1f} tr",
        "interest_monthly_formatted": f"{interest_first_month_mil:.1f} tr"
    }


def get_surrounding_amenities(city: str, district: str) -> List[Dict[str, str]]:
    """Retrieve nearby amenities from knowledge base or fallback defaults."""
    city_clean = city.strip()
    district_clean = district.strip()
    
    if city_clean in AMENITIES_KB and district_clean in AMENITIES_KB[city_clean]:
        return AMENITIES_KB[city_clean][district_clean]
    elif city_clean in AMENITIES_KB:
        # Take first available district in that city
        first_dist = list(AMENITIES_KB[city_clean].keys())[0]
        return AMENITIES_KB[city_clean][first_dist]
    else:
        # Default urban amenities
        return [
            {"name": "Trường học liên cấp Chuẩn Quốc gia", "type": "Giáo dục", "distance": "0.8 km", "icon": "🎓"},
            {"name": "Trung tâm Thương mại & Siêu thị", "type": "Mua sắm", "distance": "1.2 km", "icon": "🛍️"},
            {"name": "Bệnh viện Đa khoa Khu vực", "type": "Y tế", "distance": "1.5 km", "icon": "🏥"},
            {"name": "Công viên Cây xanh & Hồ điều hòa", "type": "Sinh thái", "distance": "1.0 km", "icon": "🌳"}
        ]


def build_housing_knowledge_graph(
    property_data: Dict[str, Any],
    pred_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Construct dynamic graph nodes and edges for Real Estate Knowledge Graph
    connecting Property specs, AI valuation, Urban amenities, and Mortgage bank packages.
    """
    price_billion = pred_result.get("price_billion", 5.0)
    city = property_data.get("City", "Hồ Chí Minh")
    district = property_data.get("District", "Gò Vấp")
    ward = property_data.get("Ward", "Phường 11")
    area = property_data.get("Area", 85.0)
    floors = property_data.get("Floors", 4)
    legal = property_data.get("Legal status", "Have certificate")
    model_name = pred_result.get("model_name", "XGBoost")

    nodes = []
    edges = []

    # 1. Property Node (Center)
    nodes.append({
        "id": "property",
        "label": f"Nhà {area}m² ({floors}T)",
        "group": "property",
        "color": "#2563eb",
        "size": 28,
        "details": f"Diện tích: {area}m² | {floors} Tầng | Pháp lý: {legal}"
    })

    # 2. Location Hierarchy Node
    nodes.append({
        "id": "location",
        "label": f"{district}, {city}",
        "group": "location",
        "color": "#059669",
        "size": 24,
        "details": f"Địa chỉ: {ward}, {district}, {city}"
    })
    edges.append({
        "from": "property",
        "to": "location",
        "label": "TỌA_LẠC_TẠI",
        "color": "#10b981"
    })

    # 3. AI Valuation Node
    nodes.append({
        "id": "valuation",
        "label": f"AI: {pred_result.get('price_formatted', f'{price_billion:.2f} tỷ')}",
        "group": "valuation",
        "color": "#1e3a8a",
        "size": 28,
        "details": f"Định giá bởi {model_name}: {pred_result.get('price_formatted')} ({pred_result.get('price_per_m2_formatted')})"
    })
    edges.append({
        "from": "property",
        "to": "valuation",
        "label": "ĐƯỢC_ĐỊNH_GIÁ_BỞI",
        "color": "#3b82f6"
    })

    # 4. Amenities Nodes (Top & Left)
    amenities = get_surrounding_amenities(city, district)
    for i, am in enumerate(amenities[:3]):
        node_id = f"amenity_{i}"
        nodes.append({
            "id": node_id,
            "label": am["name"][:20] + "...",
            "group": "amenity",
            "color": "#d97706",
            "size": 20,
            "details": f"{am['name']} ({am['type']}) — Cách {am['distance']}"
        })
        edges.append({
            "from": "location",
            "to": node_id,
            "label": f"CÁCH_{am['distance']}",
            "color": "#f59e0b"
        })

    # 5. Financial & Mortgage Package Node (Right)
    primary_bank = PARTNER_BANKS[0]  # Techcombank
    mortgage_info = calculate_mortgage(price_billion, ltv_pct=primary_bank["max_ltv_pct"], rate_pct=primary_bank["preferential_rate_pct"], tenure_years=25)
    
    nodes.append({
        "id": "bank_loan",
        "label": f"Gói vay: {mortgage_info['loan_amount_formatted']}",
        "group": "bank",
        "color": "#dc2626",
        "size": 24,
        "details": f"{primary_bank['bank_name']}: Vay {mortgage_info['loan_amount_formatted']} (Góp {mortgage_info['monthly_estimate_formatted']})"
    })
    edges.append({
        "from": "valuation",
        "to": "bank_loan",
        "label": "BẢO_LÃNH_VAY_75%",
        "color": "#ef4444"
    })

    # 6. Brokerage / Platform Node
    nodes.append({
        "id": "broker",
        "label": "OneHousing / Batdongsan",
        "group": "platform",
        "color": "#7c3aed",
        "size": 22,
        "details": "Chuyên viên thẩm định & Môi giới khu vực — Hotline: 1800 6464"
    })
    edges.append({
        "from": "property",
        "to": "broker",
        "label": "NIÊM_YẾT_GIAO_DỊCH",
        "color": "#8b5cf6"
    })

    return {
        "graph": {
            "nodes": nodes,
            "edges": edges
        },
        "financial_package": {
            "price_billion": price_billion,
            "banks": [
                {
                    **b,
                    "mortgage": calculate_mortgage(price_billion, ltv_pct=b["max_ltv_pct"], rate_pct=b["preferential_rate_pct"], tenure_years=b["tenure_years"])
                }
                for b in PARTNER_BANKS
            ]
        },
        "amenities": amenities,
        "broker_hotline": "1800 6464"
    }
