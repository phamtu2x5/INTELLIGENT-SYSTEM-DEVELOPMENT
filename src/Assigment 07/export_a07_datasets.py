# -*- coding: utf-8 -*-
"""
Script: export_a07_datasets.py
Tạo và xuất bản các bộ dữ liệu (Datasets) chuyên biệt cho Assignment 07:
1. diabetes_clinical_records_vn.csv: 1,000 bản ghi lâm sàng bệnh nhân ĐTĐ tại Việt Nam
2. vietnam_stock_gold_timeseries.csv: Chuỗi thời gian tài chính Việt Nam (Tỷ giá USD/VND, Vàng SJC, FPT, HPG)
3. healthcare_triplets.json: Bộ ba RDF đồ thị tri thức Y tế chuẩn hóa theo QĐ 5481/QĐ-BYT
4. financial_triplets.json: Bộ ba RDF đồ thị tri thức Tài chính vĩ mô Việt Nam
5. rag_corpus_vietnam.json: Kho văn bản quy chuẩn phục vụ Dense Vector RAG
"""

import os
import json
import numpy as np
import pandas as pd

DATA_DIR = "src/Assigment 07/data"
os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Dataset Lâm sàng Y tế Việt Nam: diabetes_clinical_records_vn.csv
# -----------------------------------------------------------------------------
def export_clinical_dataset(n_samples=1000):
    np.random.seed(42)
    patient_ids = [f"VN-MED-{i+10001}" for i in range(n_samples)]
    ages = np.random.randint(25, 80, size=n_samples)
    genders = np.random.choice(["Nam", "Nữ"], size=n_samples, p=[0.48, 0.52])
    
    # BMI theo chuẩn người châu Á (IDI & WHO WPRO: thừa cân >= 23, béo phì >= 25)
    bmis = np.round(np.random.normal(24.2, 3.1, size=n_samples), 1)
    bmis = np.clip(bmis, 17.5, 38.0)
    
    # HbA1c (%) và Fasting Glucose (mg/dL) tương quan sinh học
    hba1c = np.round(np.random.normal(6.8, 1.2, size=n_samples), 1)
    hba1c = np.clip(hba1c, 4.8, 12.5)
    
    fasting_glucose = np.round(hba1c * 18.5 + np.random.normal(15, 12, size=n_samples), 1)
    fasting_glucose = np.clip(fasting_glucose, 70.0, 320.0)
    
    systolic_bp = np.random.choice([110, 120, 130, 140, 150, 160], size=n_samples, p=[0.1, 0.3, 0.3, 0.15, 0.1, 0.05])
    
    diagnoses = []
    medications = []
    alcohol_habits = []
    
    for i in range(n_samples):
        # Tiêu chuẩn chẩn đoán theo QĐ 5481/QĐ-BYT
        if hba1c[i] >= 6.5 or fasting_glucose[i] >= 126.0:
            diag = "Đái tháo đường Típ 2 (E11)"
            med = np.random.choice(["Metformin 500mg", "Metformin 1000mg", "Metformin + Gliclazide", "Insulin"], p=[0.45, 0.30, 0.15, 0.10])
        elif hba1c[i] >= 5.7 or fasting_glucose[i] >= 100.0:
            diag = "Tiền đái tháo đường (R73.0)"
            med = np.random.choice(["Không dùng thuốc (Điều chỉnh lối sống)", "Metformin 500mg (Dự phòng)"], p=[0.85, 0.15])
        else:
            diag = "Bình thường"
            med = "Không dùng thuốc"
        
        alc = np.random.choice(["Không uống", "Thỉnh thoảng (dưới 1 lần/tuần)", "Thường xuyên (uống hàng tuần)"], p=[0.45, 0.35, 0.20])
        
        diagnoses.append(diag)
        medications.append(med)
        alcohol_habits.append(alc)
        
    df = pd.DataFrame({
        "Patient_ID": patient_ids,
        "Tuoi": ages,
        "Gioi_Tinh": genders,
        "BMI": bmis,
        "HbA1c_Phan_Tram": hba1c,
        "Glucose_Doi_mg_dL": fasting_glucose,
        "Huyet_Ap_Tam_Thu": systolic_bp,
        "Chan_Doan_ICD10": diagnoses,
        "Thuoc_Dang_Dung": medications,
        "Thoi_Quen_Ruou_Bia": alcohol_habits
    })
    
    out_csv = os.path.join(DATA_DIR, "diabetes_clinical_records_vn.csv")
    df.to_csv(out_csv, index=False, encoding="utf-8-sig")
    print(f"✓ Đã xuất bản dataset y tế: {out_csv} ({len(df)} dòng)")

# -----------------------------------------------------------------------------
# 2. Dataset Chuỗi thời gian Tài chính: vietnam_stock_gold_timeseries.csv
# -----------------------------------------------------------------------------
def export_financial_dataset(n_days=1200):
    date_rng = pd.date_range(start="2021-01-04", periods=n_days, freq="B")
    
    np.random.seed(101)
    # Tỷ giá USD/VND trung tâm và ngân hàng thương mại
    usd_vnd = [23150.0]
    for _ in range(1, n_days):
        ret = np.random.normal(0.00008, 0.0012)
        usd_vnd.append(round(usd_vnd[-1] * (1 + ret), 1))
        
    # Vàng miếng SJC (triệu đồng/lượng)
    gold_sjc = [56.2]
    for _ in range(1, n_days):
        ret = np.random.normal(0.00035, 0.0055)
        gold_sjc.append(round(gold_sjc[-1] * (1 + ret), 2))
        
    # Cổ phiếu FPT (nghìn đồng/cổ phiếu)
    fpt_price = [42.5]
    for _ in range(1, n_days):
        ret = np.random.normal(0.00095, 0.014)
        fpt_price.append(round(fpt_price[-1] * (1 + ret), 2))
        
    # Cổ phiếu HPG (nghìn đồng/cổ phiếu)
    hpg_price = [22.0]
    for _ in range(1, n_days):
        ret = np.random.normal(0.00025, 0.016)
        hpg_price.append(round(hpg_price[-1] * (1 + ret), 2))
        
    df = pd.DataFrame({
        "Ngay_Giao_Dich": date_rng.strftime("%Y-%m-%d"),
        "Ty_Gia_USD_VND": usd_vnd,
        "Gia_Vang_SJC_Trieu": gold_sjc,
        "Co_Phieu_FPT_Nghin": fpt_price,
        "Co_Phieu_HPG_Nghin": hpg_price
    })
    
    out_csv = os.path.join(DATA_DIR, "vietnam_stock_gold_timeseries.csv")
    df.to_csv(out_csv, index=False, encoding="utf-8-sig")
    print(f"✓ Đã xuất bản dataset tài chính: {out_csv} ({len(df)} phiên giao dịch)")

# -----------------------------------------------------------------------------
# 3. Đồ thị Tri thức Bộ ba RDF Y tế: healthcare_triplets.json
# -----------------------------------------------------------------------------
def export_healthcare_triplets():
    triplets = [
        {"subject": "HbA1c_Mau_Lon_Hon_6.5", "predicate": "TIEU_CHUAN_CHAN_DOAN", "object": "Dai_Thao_Duong_Tip_2", "source": "QD_5481_QD_BYT", "confidence": 1.0},
        {"subject": "Glucose_Doi_Lon_Hon_126", "predicate": "TIEU_CHUAN_CHAN_DOAN", "object": "Dai_Thao_Duong_Tip_2", "source": "QD_5481_QD_BYT", "confidence": 1.0},
        {"subject": "Nghiem_Phap_OGTT_Lon_Hon_200", "predicate": "TIEU_CHUAN_CHAN_DOAN", "object": "Dai_Thao_Duong_Tip_2", "source": "WHO_BYT", "confidence": 1.0},
        {"subject": "BMI_Chau_A_Lon_Hon_23", "predicate": "YEU_TO_NGUY_CO", "object": "Dai_Thao_Duong_Tip_2", "odds_ratio": 2.4, "note": "Chuẩn thừa cân WPRO"},
        {"subject": "Tang_Huyet_Ap_140_90", "predicate": "YEU_TO_NGUY_CO", "object": "Dai_Thao_Duong_Tip_2", "odds_ratio": 1.8},
        {"subject": "Dai_Thao_Duong_Tip_2", "predicate": "DIEU_TRI_DAU_TAY", "object": "Metformin_Biguanide", "dose": "500-1000mg x 2 lan/ngay"},
        {"subject": "Metformin_Biguanide", "predicate": "CHONG_CHI_DINH_TUONG_TAC_CAP_TINH", "object": "Ruou_Bia_Con", "severity": "FATAL_RISK", "effect": "Toan Lactic tu vong 50%"},
        {"subject": "Gliclazide_MR", "predicate": "CHONG_CHI_DINH_TUONG_TAC", "object": "Ruou_Bia_Con", "severity": "HIGH", "effect": "Ha duong huyet dot ngot keo dai"},
        {"subject": "Dai_Thao_Duong_Tip_2", "predicate": "PHOI_HOP_THUOC_BAC_2", "object": "SGLT2_Inhibitor", "benefit": "Bao ve tim mach va than"},
        {"subject": "Dai_Thao_Duong_Tip_2", "predicate": "BIEN_CHUNG_MAN_TINH", "object": "Benh_Vong_Mac_Tieu_Duong", "icd10": "H36.0"},
        {"subject": "Dai_Thao_Duong_Tip_2", "predicate": "BIEN_CHUNG_MAN_TINH", "object": "Suy_Than_Man_Tinh", "icd10": "N18"},
        {"subject": "Dai_Thao_Duong_Tip_2", "predicate": "BIEN_CHUNG_MAN_TINH", "object": "Dot_Quy_Va_Nhoi_Mau_Co_Tim", "icd10": "I21_I63"},
        {"subject": "Dai_Thao_Duong_Tip_2", "predicate": "KHUYEN_NGHI_DINH_DUONG", "object": "Uc_Ga_Nac_Bo_Da_Luoc", "gi_index": 0, "protein_clean": True},
        {"subject": "Dai_Thao_Duong_Tip_2", "predicate": "KHUYEN_NGHI_DINH_DUONG", "object": "Rau_Xanh_Chat_Xo_Hoa_Tan", "gi_index": 15, "fiber_high": True},
        {"subject": "Dai_Thao_Duong_Tip_2", "predicate": "KHUYEN_NGHI_DINH_DUONG", "object": "Gao_Lut_Nguyen_Cam", "gi_index": 50, "fiber_high": True},
        {"subject": "Dai_Thao_Duong_Tip_2", "predicate": "NGHIEM_CAM_AN", "object": "Da_Ga_Va_Ga_Chien_Dau", "reason": "Chat beo bao hoa gay de khang insulin"},
        {"subject": "Dai_Thao_Duong_Tip_2", "predicate": "NGHIEM_CAM_AN", "object": "Nuoc_Ngot_Co_Ga_Banh_Keo", "reason": "GI > 70 gay soc duong huyet cap"}
    ]
    out_json = os.path.join(DATA_DIR, "healthcare_triplets.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(triplets, f, ensure_ascii=False, indent=2)
    print(f"✓ Đã xuất bản RDF triplets y tế: {out_json} ({len(triplets)} bộ ba)")

# -----------------------------------------------------------------------------
# 4. Đồ thị Tri thức Bộ ba RDF Tài chính: financial_triplets.json
# -----------------------------------------------------------------------------
def export_financial_triplets():
    triplets = [
        {"subject": "Ngan_Hang_Nha_Nuoc", "predicate": "DIEU_HANH_CHINH_SACH", "object": "Lai_Suat_Tai_Cap_Von_4_5", "status": "On dinh ho tro tang truong"},
        {"subject": "Ngan_Hang_Nha_Nuoc", "predicate": "CAN_THIEP_THI_TRUONG", "object": "Ty_Gia_USD_VND", "mechanism": "Ban ngoai te can thiep & tin phieu SBV"},
        {"subject": "Chinh_Phu_NHNN", "predicate": "BAN_HANH_QUAN_LY", "object": "Nghi_Dinh_24_2012_ND_CP", "scope": "Doc quyen san xuat vang mieng SJC"},
        {"subject": "Nghi_Dinh_24_2012_ND_CP", "predicate": "TAC_DONG_NGUON_CUNG", "object": "Vang_Mieng_SJC", "effect": "Khan hiem cung, chenh lech gia the gioi 16-18 trieu"},
        {"subject": "Ty_Gia_USD_VND_Tang", "predicate": "HUONG_LOI_TY_GIA_DUONG", "object": "Co_Phieu_FPT", "mechanism": "Xuat khau phan mem thu ngoai te USD/JPY chiem 50% doanh thu"},
        {"subject": "Ty_Gia_USD_VND_Tang", "predicate": "AP_LUC_CHI_PHI_VON_AM", "object": "Co_Phieu_HPG", "mechanism": "Nhap khau 100% quang sat va than mo tinh bang USD"},
        {"subject": "Co_Phieu_FPT", "predicate": "DU_BAO_BiLSTM", "object": "Muc_Tieu_138_142K", "expected_return": "+1.8%", "confidence": 0.842},
        {"subject": "Co_Phieu_HPG", "predicate": "DU_BAO_BiLSTM", "object": "Vung_Ho_Tro_27_5_28_2K", "expected_return": "0.0%", "recommendation": "Quan sat"},
        {"subject": "Vang_Mieng_SJC", "predicate": "DU_BAO_BiLSTM", "object": "Bien_Do_89_8_91_5_Trieu", "volatility": "HIGH", "recommendation": "Tranh fomo du dinh"}
    ]
    out_json = os.path.join(DATA_DIR, "financial_triplets.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(triplets, f, ensure_ascii=False, indent=2)
    print(f"✓ Đã xuất bản RDF triplets tài chính: {out_json} ({len(triplets)} bộ ba)")

# -----------------------------------------------------------------------------
# 5. Kho Văn bản Quy chuẩn RAG: rag_corpus_vietnam.json
# -----------------------------------------------------------------------------
def export_rag_corpus():
    corpus = [
        {
            "id": "RAG-MED-01",
            "domain": "Y Tế",
            "source": "Quyết định 5481/QĐ-BYT Bộ Y Tế",
            "title": "Hướng dẫn chẩn đoán và điều trị đái tháo đường típ 2",
            "content": "Metformin (thuộc nhóm Biguanide) là lựa chọn đầu tay trong điều trị đái tháo đường típ 2, bắt đầu với liều 500mg hoặc 850mg cùng bữa ăn để giảm tác dụng phụ trên đường tiêu hóa. Chống chỉ định tuyệt đối Metformin đối với bệnh nhân suy thận nặng (eGFR < 30 mL/phút/1.73 m2) và người lạm dụng rượu bia cấp hoặc mạn tính do nguy cơ nhiễm toan acid lactic có tỷ lệ tử vong lên tới 50%."
        },
        {
            "id": "RAG-MED-02",
            "domain": "Y Tế",
            "source": "Viện Dinh Dưỡng Quốc Gia Việt Nam",
            "title": "Chỉ số đường huyết (GI) và chế độ ăn người tiểu đường",
            "content": "Bệnh nhân đái tháo đường cần được tư vấn kiểm soát khẩu phần carbohydrate, ưu tiên thực phẩm có chỉ số đường huyết thấp (GI < 55) như rau xanh, các loại đậu, ngũ cốc nguyên cám. Về nguồn đạm, ức gà nạc bỏ da luộc hoặc hấp là nguồn protein sinh học cao với GI = 0, không làm tăng đường huyết. Cần kiêng tuyệt đối da gà và các món gà rán tẩm bột chiên ngập dầu do lượng chất béo bão hòa và trans-fat cao gây nặng thêm tình trạng kháng insulin."
        },
        {
            "id": "RAG-FIN-01",
            "domain": "Tài Chính",
            "source": "Báo cáo phân tích vĩ mô CTCK SSI & Ngân Hàng Nhà Nước",
            "title": "Tác động của diễn biến tỷ giá USD/VND lên doanh nghiệp niêm yết",
            "content": "Khi tỷ giá USD/VND chịu áp lực tăng giá, các doanh nghiệp có tỷ trọng doanh thu xuất khẩu bằng đồng USD chiếm đa số như Tập đoàn FPT (xuất khẩu phần mềm sang Mỹ, Nhật Bản, châu Âu) sẽ được hưởng lợi chênh lệch tỷ giá dương, góp phần cải thiện biên lợi nhuận gộp. Ngược lại, các doanh nghiệp sản xuất thâm dụng nguyên liệu nhập khẩu như Hòa Phát (HPG) phải chịu chi phí vốn tăng cao do nguyên liệu quặng sắt và than mỡ luyện cốc được niêm yết bằng USD."
        },
        {
            "id": "RAG-FIN-02",
            "domain": "Tài Chính",
            "source": "Ngân Hàng Nhà Nước Việt Nam",
            "title": "Chính sách quản lý thị trường vàng và Nghị định 24/2012/NĐ-CP",
            "content": "Nghị định 24/2012/NĐ-CP quy định Nhà nước độc quyền sản xuất vàng miếng và quản lý chặt chẽ hoạt động xuất nhập khẩu vàng nguyên liệu. Điều này dẫn đến sự chênh lệch lớn giữa giá vàng miếng SJC trong nước và giá vàng thế giới quy đổi, có thời điểm lên đến 16 - 18 triệu đồng/lượng. Nhà đầu tư cá nhân cần hết sức thận trọng khi giao dịch vàng SJC ở vùng đỉnh lịch sử để tránh rủi ro điều chỉnh mạnh khi chính sách được nới lỏng."
        }
    ]
    out_json = os.path.join(DATA_DIR, "rag_corpus_vietnam.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
    print(f"✓ Đã xuất bản kho văn bản RAG: {out_json} ({len(corpus)} tài liệu)")

if __name__ == "__main__":
    print("="*60)
    print("XUẤT BẢN TOÀN BỘ CÁC TỆP DATASET CHO ASSIGNMENT 07")
    print("="*60)
    export_clinical_dataset()
    export_financial_dataset()
    export_healthcare_triplets()
    export_financial_triplets()
    export_rag_corpus()
    print("="*60)
    print("✓ HOÀN TẤT XUẤT BẢN DATASETS TRONG THƯ MỤC src/Assigment 07/data/")
    print("="*60)
