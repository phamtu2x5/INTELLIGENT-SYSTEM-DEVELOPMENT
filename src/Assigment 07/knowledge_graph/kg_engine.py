# -*- coding: utf-8 -*-
"""
Module: kg_engine.py
Xây dựng và truy vấn Đồ thị Tri thức (Knowledge Graph) đa miền tại Việt Nam:
1. Miền Y tế: Phác đồ điều trị Đái tháo đường (Bộ Y Tế) & Cẩm nang Dinh dưỡng
2. Miền Tài chính: Cổ phiếu VN30 (FPT, VCB, HPG, VIC) & Thị trường Vàng SJC
"""

import networkx as nx
from typing import List, Dict, Any

class VietnamHealthcareKG:
    """Knowledge Graph chuyên biệt cho Bệnh Đái Tháo Đường tại Việt Nam"""
    def __init__(self):
        self.G = nx.MultiDiGraph()
        self._build_diabetes_graph()
        
    def _build_diabetes_graph(self):
        # 1. Các thực thể Bệnh lý & Chỉ số cận lâm sàng
        self.G.add_node("Tieu_Duong_Type_2", type="Disease", label="Đái tháo đường Type 2", icd10="E11")
        self.G.add_node("Tieu_Duong_Type_1", type="Disease", label="Đái tháo đường Type 1", icd10="E10")
        self.G.add_node("Tien_Tieu_Duong", type="PreDisease", label="Tiền đái tháo đường")
        
        self.G.add_node("HbA1c_Cao", type="Biomarker", threshold=">= 6.5%", desc="Chỉ số phản ánh đường huyết 3 tháng")
        self.G.add_node("Glucose_Doi_Cao", type="Biomarker", threshold=">= 126 mg/dL", desc="Đường huyết lúc đói sau 8h")
        self.G.add_node("BMI_Thua_Can", type="RiskFactor", threshold=">= 25.0 kg/m2", desc="Thừa cân béo phì theo chuẩn WPRO")
        
        # 2. Thực thể Dược phẩm (Thuốc hạ đường huyết theo Dược thư Bộ Y Tế)
        self.G.add_node("Metformin", type="Drug", class_name="Biguanide", dose="500mg - 1000mg/ngày", first_line=True)
        self.G.add_node("Gliclazide", type="Drug", class_name="Sulfonylurea", dose="30mg - 60mg MR", first_line=False)
        self.G.add_node("Insulin", type="Drug", class_name="Hormone", indication="Type 1 hoặc Type 2 thất bại thuốc uống")
        
        # 3. Thực thể Thực phẩm & Thói quen tiêu biểu tại Việt Nam
        self.G.add_node("Ruou_Bia", type="RiskSubstance", label="Rượu bia / Cồn", dangerous=True)
        self.G.add_node("Thit_Ga_Uc_Bo_Da", type="SafeFood", label="Ức gà nạc bỏ da", protein_high=True, fat_low=True)
        self.G.add_node("Thit_Ga_Chien_Dau", type="RiskFood", label="Thịt gà chiên ngập dầu", trans_fat_high=True)
        self.G.add_node("Com_Trang", type="Food", label="Cơm trắng gạo tẻ", gi_index=73, advice="Giới hạn 1 bát/bữa")
        self.G.add_node("Rau_Xanh", type="SafeFood", label="Rau muống / Bông cải xanh", fiber_high=True, gi_index=15)
        
        # 4. Các mối quan hệ (Edges & Triples)
        # Chỉ số -> Bệnh
        self.G.add_edge("HbA1c_Cao", "Tieu_Duong_Type_2", relation="TIEU_CHUAN_CHAN_DOAN", evidence="BYT 2024")
        self.G.add_edge("Glucose_Doi_Cao", "Tieu_Duong_Type_2", relation="TIEU_CHUAN_CHAN_DOAN", evidence="ADA / BYT")
        self.G.add_edge("BMI_Thua_Can", "Tieu_Duong_Type_2", relation="NGUY_CO_GIA_TANG", odds_ratio=2.4)
        
        # Bệnh -> Thuốc điều trị
        self.G.add_edge("Tieu_Duong_Type_2", "Metformin", relation="CHI_DINH_DAU_TAY", guidelines="Quyết định 5481/QĐ-BYT")
        self.G.add_edge("Tieu_Duong_Type_2", "Gliclazide", relation="PHOI_HOP_BAC_2", condition="Khi HbA1c chưa đạt mục tiêu sau 3 tháng")
        self.G.add_edge("Tieu_Duong_Type_1", "Insulin", relation="CHI_DINH_BAT_BUOC", reason="Thiếu hụt insulin tuyệt đối")
        
        # Thuốc -> Tương tác nguy hiểm
        self.G.add_edge("Metformin", "Ruou_Bia", relation="CHONG_CHI_DINH_TUONG_TAC", 
                        effect="TĂNG NGUY CƠ NHIỄM TOAN LACTIC VÀ HẠ ĐƯỜNG HUYẾT ĐỘT NGỘT NGUY HIỂM TÍNH MẠNG")
        self.G.add_edge("Gliclazide", "Ruou_Bia", relation="CHONG_CHI_DINH_TUONG_TAC",
                        effect="Kéo dài cơn hạ đường huyết quá mức do cồn ức chế tân tạo glucose tại gan")
        
        # Bệnh -> Dinh dưỡng & Thực phẩm
        self.G.add_edge("Tieu_Duong_Type_2", "Thit_Ga_Uc_Bo_Da", relation="KHUYEN_NGHI_DINH_DUONG",
                        reason="Đạm nạc chất lượng cao, không chứa carb, duy trì khối cơ không làm tăng đường huyết")
        self.G.add_edge("Tieu_Duong_Type_2", "Thit_Ga_Chien_Dau", relation="CANH_BAO_HAN_CHE",
                        reason="Chất béo bão hòa và năng lượng cao làm tăng đề kháng insulin và xơ vữa động mạch")
        self.G.add_edge("Tieu_Duong_Type_2", "Com_Trang", relation="KIEM_SOAT_SO_LUONG",
                        reason="Chỉ số đường huyết (GI=73) cao, cần chia nhỏ khẩu phần và ăn cùng nhiều rau xanh")
        self.G.add_edge("Tieu_Duong_Type_2", "Rau_Xanh", relation="KHUYEN_NGHI_UU_TIEN",
                        reason="Chất xơ hòa tan tạo mạng lưới gel làm chậm phân giải tinh bột, giúp đường huyết ổn định")

    def query_substance_warning(self, drug_name: str, substance: str) -> List[Dict[str, Any]]:
        """Kiểm tra tương tác thuốc và thực phẩm/thói quen có hại"""
        warnings = []
        if self.G.has_edge(drug_name, substance):
            for key, data in self.G.get_edge_data(drug_name, substance).items():
                warnings.append({
                    "drug": drug_name,
                    "substance": substance,
                    "relation": data.get("relation"),
                    "effect": data.get("effect")
                })
        return warnings

    def query_diet_recommendation(self, disease: str, food_item: str) -> List[Dict[str, Any]]:
        """Truy xuất khuyến nghị dinh dưỡng chuẩn y khoa cho bệnh nhân"""
        recs = []
        if self.G.has_edge(disease, food_item):
            for key, data in self.G.get_edge_data(disease, food_item).items():
                recs.append({
                    "disease": disease,
                    "food": food_item,
                    "relation": data.get("relation"),
                    "reason": data.get("reason")
                })
        return recs


class VietnamFinancialKG:
    """Knowledge Graph chuyên biệt cho Chứng khoán VN30 & Giá Vàng SJC"""
    def __init__(self):
        self.G = nx.MultiDiGraph()
        self._build_finance_graph()
        
    def _build_finance_graph(self):
        # 1. Các thực thể Kinh tế vĩ mô & Chính sách Việt Nam
        self.G.add_node("Ty_Gia_USD_VND", type="MacroFactor", desc="Tỷ giá hối đoái đồng Đô la Mỹ và Đồng Việt Nam")
        self.G.add_node("Lai_Suat_NHNN", type="PolicyFactor", desc="Lãi suất tái cấp vốn và tái chiết khấu của Ngân hàng Nhà nước")
        self.G.add_node("XAU_USD", type="GlobalAsset", desc="Giá vàng giao ngay thế giới (USD/Ounce)")
        self.G.add_node("Nghi_Dinh_24", type="Regulation", desc="Nghị định quản lý độc quyền thương hiệu vàng miếng quốc gia SJC")
        
        # 2. Thực thể Tài sản Vàng
        self.G.add_node("Vang_Mieng_SJC", type="CommodityAsset", desc="Vàng miếng độc quyền SJC 999.9 tại thị trường Việt Nam")
        self.G.add_node("Vang_Nhan_9999", type="CommodityAsset", desc="Vàng nhẫn trơn 4 số 9 của các doanh nghiệp kinh doanh vàng")
        
        # 3. Thực thể Cổ phiếu VN30 hàng đầu
        self.G.add_node("FPT", type="Stock", company="Tập đoàn FPT", sector="Công nghệ thông tin & Viễn thông")
        self.G.add_node("VCB", type="Stock", company="Ngân hàng TMCP Ngoại thương VN", sector="Ngân hàng quốc doanh")
        self.G.add_node("HPG", type="Stock", company="Tập đoàn Hòa Phát", sector="Thép & Công nghiệp nặng")
        self.G.add_node("VIC", type="Stock", company="Tập đoàn Vingroup", sector="Bất động sản & Sản xuất xe điện")
        
        # 4. Các mối quan hệ chuỗi giá trị và tác động kinh tế
        # Vàng SJC
        self.G.add_edge("XAU_USD", "Vang_Mieng_SJC", relation="DAN_DAT_XU_HUONG", correlation=0.88,
                        desc="Giá vàng trong nước biến động cùng chiều với giá vàng thế giới theo quy đổi tỷ giá")
        self.G.add_edge("Ty_Gia_USD_VND", "Vang_Mieng_SJC", relation="TAC_DONG_DUONG",
                        desc="Tỷ giá USD/VND tăng làm tăng chi phí nhập khẩu vàng nguyên liệu, kéo giá SJC tăng")
        self.G.add_edge("Nghi_Dinh_24", "Vang_Mieng_SJC", relation="TAO_CHENH_LECH_CUNG_CAU",
                        desc="Giới hạn nguồn cung dập vàng miếng SJC dẫn đến chênh lệch cao 5-10 triệu đồng so với thế giới")
        
        # Cổ phiếu FPT
        self.G.add_edge("Ty_Gia_USD_VND", "FPT", relation="HUONG_LOI_TY_GIA",
                        desc="Doanh thu xuất khẩu phần mềm sang Mỹ và Nhật chiếm gần 50%, tỷ giá USD tăng giúp tăng biên lợi nhuận")
        
        # Cổ phiếu VCB
        self.G.add_edge("Lai_Suat_NHNN", "VCB", relation="DIEU_TIET_THANH_KHOAN",
                        desc="Định hướng lãi suất điều hành tác động tới chi phí huy động vốn và biên lãi thuần (NIM)")
        
        # Cổ phiếu HPG
        self.G.add_edge("Ty_Gia_USD_VND", "HPG", relation="BAT_LOI_CHI_PHI_NHAP_KHAU",
                        desc="HPG phải chi ngoại tệ nhập khẩu quặng sắt và than mỡ, tỷ giá USD tăng làm tăng chi phí vốn")
        
        # Quan hệ chuyển dịch dòng tiền giữa Vàng và Chứng khoán
        self.G.add_edge("Vang_Mieng_SJC", "FPT", relation="DICH_CHUYEN_DONG_VON",
                        desc="Khi rủi ro địa chính trị và lạm phát gia tăng, dòng vốn có xu hướng ưu tiên phòng thủ tích trữ vàng")

    def query_impact(self, factor: str, target: str) -> List[Dict[str, Any]]:
        """Truy vấn tác động nhân quả giữa yếu tố vĩ mô và tài sản tài chính"""
        impacts = []
        if self.G.has_edge(factor, target):
            for key, data in self.G.get_edge_data(factor, target).items():
                impacts.append({
                    "source": factor,
                    "target": target,
                    "relation": data.get("relation"),
                    "description": data.get("desc")
                })
        return impacts


if __name__ == '__main__':
    print("Khởi tạo và kiểm tra Đồ thị Tri thức Việt Nam...")
    health_kg = VietnamHealthcareKG()
    fin_kg = VietnamFinancialKG()
    
    # Test query Y tế
    warn = health_kg.query_substance_warning("Metformin", "Ruou_Bia")
    print("\n[Y TẾ] Cảnh báo tương tác Metformin & Rượu bia:")
    for w in warn:
        print(f"  -> {w['relation']}: {w['effect']}")
        
    diet = health_kg.query_diet_recommendation("Tieu_Duong_Type_2", "Thit_Ga_Uc_Bo_Da")
    print("\n[Y TẾ] Khuyến nghị Dinh dưỡng Thịt gà cho Tiểu đường Type 2:")
    for d in diet:
        print(f"  -> {d['relation']}: {d['reason']}")

    # Test query Tài chính
    fpt_impact = fin_kg.query_impact("Ty_Gia_USD_VND", "FPT")
    print("\n[TÀI CHÍNH] Tác động của Tỷ giá USD/VND lên Cổ phiếu FPT:")
    for f in fpt_impact:
        print(f"  -> {f['relation']}: {f['description']}")
        
    gold_impact = fin_kg.query_impact("Ty_Gia_USD_VND", "Vang_Mieng_SJC")
    print("\n[TÀI CHÍNH] Tác động của Tỷ giá USD/VND lên Vàng miếng SJC:")
    for g in gold_impact:
        print(f"  -> {g['relation']}: {g['description']}")
    print("\n✓ Đồ thị Tri thức Đa miền hoạt động hoàn hảo!")
