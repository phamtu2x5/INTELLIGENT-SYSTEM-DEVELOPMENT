#!/usr/bin/env python3
"""
diabetes_kg.py
==============
Đồ thị Tri thức Y khoa & Dinh dưỡng (Medical & Nutritional Knowledge Graph - KG)
dành cho hệ thống Multi-Agent chẩn đoán và quản lý Đái Tháo Đường.

Nguồn tri thức cốt lõi:
1. Quyết định 5481/QĐ-BYT (Bộ Y Tế): Hướng dẫn chẩn đoán và điều trị đái tháo đường típ 2.
2. Dược thư Quốc gia Việt Nam: Chống chỉ định và tương tác thuốc (Drug-Drug & Drug-Disease).
3. Bảng thành phần thực phẩm Việt Nam (Viện Dinh Dưỡng Quốc Gia - NIN): Chỉ số GI/GL các món ăn Việt.
4. Danh mục Dược phẩm FPT Long Châu: Liên kết hoạt chất sang sản phẩm thương mại và giá bán.
"""

import os
import json
import networkx as nx
from typing import Dict, List, Any, Optional, Tuple


class DiabetesKnowledgeGraph:
    """
    Knowledge Graph quản lý mối liên kết giữa:
    - Bệnh lý (Disease: Type 2 Diabetes, Pre-diabetes, CKD, CVD...)
    - Chỉ số sinh học (Biomarker: HbA1c, Glucose, BMI, eGFR, Blood Pressure...)
    - Thuốc & Hoạt chất (Drug / Active Ingredient: Metformin, Gliclazide, Dapagliflozin, Sitagliptin, Insulin...)
    - Chống chỉ định & Tác dụng phụ (Contraindication / Adverse Event: Lactic Acidosis, Hypoglycemia...)
    - Món ăn Việt Nam (Vietnamese Foods with GI / GL: Cơm trắng, Bún bò, Phở, Khoai lang...)
    - Sản phẩm thương mại FPT Long Châu (Commercial Products with VNĐ price & Rx status)
    """

    def __init__(self, pharmacy_catalog_path: Optional[str] = None):
        self.graph = nx.MultiDiGraph()
        if pharmacy_catalog_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.pharmacy_catalog_path = os.path.join(base_dir, "data", "pharmacy", "longchau_diabetes_products.json")
        else:
            self.pharmacy_catalog_path = pharmacy_catalog_path

        self.pharmacy_products = self._load_pharmacy_catalog()
        self._build_graph()

    def _load_pharmacy_catalog(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.pharmacy_catalog_path):
            try:
                with open(self.pharmacy_catalog_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[KG Warning] Không thể đọc catalog Long Châu: {e}")
        return []

    def _build_graph(self):
        """Khởi tạo toàn bộ các Node và Cạnh quan hệ của Đồ thị Tri thức."""
        g = self.graph

        # Ưu tiên đồng bộ trực tiếp từ Neo4j CSDL Đồ thị nếu đang hoạt động
        try:
            from neo4j import GraphDatabase
            driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password123"))
            with driver.session() as session:
                n_res = session.run("MATCH (n) RETURN n.id AS id, labels(n)[0] AS ntype, properties(n) AS props")
                nodes_found = False
                for r in n_res:
                    props = dict(r["props"])
                    props["type"] = r["ntype"]
                    g.add_node(r["id"], **props)
                    nodes_found = True
                if nodes_found:
                    r_res = session.run("MATCH (a)-[r]->(b) RETURN a.id AS src, b.id AS tgt, type(r) AS rel, properties(r) AS props")
                    for r in r_res:
                        g.add_edge(r["src"], r["tgt"], relation=r["rel"], **r["props"])
                    print(f"[KnowledgeGraph] Đã đồng bộ thành công từ Neo4j: {g.number_of_nodes()} Nodes, {g.number_of_edges()} Edges")
                    driver.close()
                    return
            driver.close()
        except Exception:
            pass

        # =====================================================================
        # 1. BỆNH LÝ & GIAI ĐOẠN (DISEASES / CONDITIONS)
        # =====================================================================
        g.add_node("T2D", type="Disease", name="Đái tháo đường Type 2", icd10="E11")
        g.add_node("PRE_DIABETES", type="Disease", name="Tiền đái tháo đường (Rối loạn dung nạp Glucose / IFG)", icd10="R73.0")
        g.add_node("CKD", type="Complication", name="Bệnh thận mạn do đái tháo đường (Diabetic Nephropathy)", icd10="N18")
        g.add_node("CVD", type="Complication", name="Bệnh lý tim mạch xơ vữa (ASCVD)", icd10="I25")
        g.add_node("HEART_FAILURE", type="Complication", name="Suy tim sung huyết (Heart Failure)", icd10="I50")
        g.add_node("OBESITY", type="RiskFactor", name="Thừa cân / Béo phì (BMI >= 23 kg/m² theo chuẩn Châu Á)")
        g.add_node("HYPERTENSION", type="Comorbidity", name="Tăng huyết áp", icd10="I10")

        # =====================================================================
        # 2. CHỈ SỐ SINH HỌC & NGƯỠNG LÂM SÀNG (BIOMARKERS & CRITERIA)
        # =====================================================================
        g.add_node("HBA1C", type="Biomarker", unit="%", normal="< 5.7%", pre_diabetes="5.7 - 6.4%", diabetes=">= 6.5%")
        g.add_node("FPG", type="Biomarker", unit="mg/dL", normal="< 100", pre_diabetes="100 - 125", diabetes=">= 126")
        g.add_node("EGFR", type="Biomarker", unit="mL/min/1.73m²", severe_ckd="< 30", moderate_ckd="30 - 59", normal=">= 60")
        g.add_node("BMI", type="Biomarker", unit="kg/m²", overweight="23 - 24.9", obese=">= 25")

        g.add_edge("T2D", "HBA1C", relation="DIAGNOSED_BY", threshold=">= 6.5%")
        g.add_edge("T2D", "FPG", relation="DIAGNOSED_BY", threshold=">= 126 mg/dL")
        g.add_edge("PRE_DIABETES", "HBA1C", relation="DIAGNOSED_BY", threshold="5.7 - 6.4%")
        g.add_edge("PRE_DIABETES", "FPG", relation="DIAGNOSED_BY", threshold="100 - 125 mg/dL")

        # =====================================================================
        # 3. NHÓM THUỐC & HOẠT CHẤT (DRUGS & ACTIVE INGREDIENTS)
        # =====================================================================
        drugs_data = [
            {
                "id": "METFORMIN",
                "name": "Metformin Hydrochloride",
                "class": "Biguanide",
                "first_line": True,
                "mechanism": "Giảm tân tạo glucose ở gan, tăng nhạy cảm insulin ngoại vi, không gây tăng cân",
                "dose_typical": "500mg - 2000mg/ngày chia 1-2 lần trong hoặc sau bữa ăn"
            },
            {
                "id": "GLICLAZIDE",
                "name": "Gliclazide MR",
                "class": "Sulfonylurea",
                "first_line": False,
                "mechanism": "Kích thích tế bào beta tụy tiết insulin phụ thuộc thụ thể SUR-1",
                "dose_typical": "30mg - 120mg/ngày uống vào bữa sáng"
            },
            {
                "id": "DAPAGLIFLOZIN",
                "name": "Dapagliflozin",
                "class": "SGLT2 inhibitor",
                "first_line": True, # Theo ADA 2024 & QĐ 5481 nếu có bệnh thận/suy tim
                "mechanism": "Ức chế tái hấp thu glucose ở ống lượn gần thận, tăng bài tiết đường qua nước tiểu, hạ huyết áp nhẹ, giảm cân",
                "dose_typical": "10mg/ngày uống 1 lần"
            },
            {
                "id": "EMPAGLIFLOZIN",
                "name": "Empagliflozin",
                "class": "SGLT2 inhibitor",
                "first_line": True,
                "mechanism": "Bảo vệ tim mạch rõ rệt, giảm tử vong tim mạch ở bệnh nhân đái tháo đường kèm suy tim hoặc bệnh thận mạn",
                "dose_typical": "10mg - 25mg/ngày"
            },
            {
                "id": "SITAGLIPTIN",
                "name": "Sitagliptin",
                "class": "DPP-4 inhibitor",
                "first_line": False,
                "mechanism": "Kéo dài hoạt tính hoóc-môn Incretin (GLP-1), tăng tiết insulin phụ thuộc nồng độ đường, không gây hạ đường huyết",
                "dose_typical": "50mg - 100mg/ngày"
            },
            {
                "id": "INSULIN_GLARGINE",
                "name": "Insulin Glargine (Lantus)",
                "class": "Basal Insulin Analogue",
                "first_line": False,
                "mechanism": "Bổ sung lượng insulin nền ổn định suốt 24 giờ không có đỉnh nhọn, kiểm soát đường huyết lúc đói",
                "dose_typical": "0.1 - 0.2 đơn vị/kg tiêm dưới da trước khi đi ngủ"
            }
        ]

        for d in drugs_data:
            drug_id = d["id"]
            g.add_node(drug_id, type="Drug", **d)
            g.add_edge(drug_id, "T2D", relation="TREATS")

        # =====================================================================
        # 4. CHỐNG CHỈ ĐỊNH VÀ QUY TẮC AN TOÀN DƯỢC LÝ (CONTRAINDICATIONS & SAFETY)
        # =====================================================================
        # Metformin:
        g.add_node("LACTIC_ACIDOSIS", type="AdverseEffect", name="Nhiễm toan Lactic (Nguy cơ tử vong cao)")
        g.add_edge("METFORMIN", "CKD", relation="CONTRAINDICATED_IN", condition="eGFR < 30 mL/min/1.73m²", severe=True)
        g.add_edge("METFORMIN", "EGFR", relation="MONITORED_BY", note="Giảm nửa liều khi eGFR 30-44; ngừng hoàn toàn khi eGFR < 30")
        g.add_edge("METFORMIN", "LACTIC_ACIDOSIS", relation="RISK_OF", cofactor="Rượu bia mạn tính, suy gan nặng, thiếu oxy mô")

        # Sulfonylurea (Gliclazide):
        g.add_node("HYPOGLYCEMIA", type="AdverseEffect", name="Hạ đường huyết cấp tính (< 70 mg/dL)")
        g.add_edge("GLICLAZIDE", "HYPOGLYCEMIA", relation="RISK_OF", condition="Bỏ bữa, tập thể dục quá mức, hoặc người cao tuổi")
        g.add_edge("GLICLAZIDE", "CKD", relation="CAUTION_IN", condition="Tăng nguy cơ tích tụ thuốc và hạ đường huyết kéo dài khi suy thận")

        # SGLT2i:
        g.add_node("EUG_DKA", type="AdverseEffect", name="Toan Ceton đường huyết bình thường (Euglycemic DKA)")
        g.add_node("UTI", type="AdverseEffect", name="Nhiễm khuẩn tiết niệu và sinh dục do glucose niệu cao")
        g.add_edge("DAPAGLIFLOZIN", "EGFR", relation="CONTRAINDICATED_IN", condition="eGFR < 20 mL/min/1.73m² để khởi đầu")
        g.add_edge("DAPAGLIFLOZIN", "UTI", relation="RISK_OF", prevention="Uống nhiều nước (1.5-2L/ngày), vệ sinh sạch sẽ")
        g.add_edge("DAPAGLIFLOZIN", "HEART_FAILURE", relation="HIGHLY_RECOMMENDED_FOR", benefit="Giảm 25-30% nhập viện do suy tim")
        g.add_edge("DAPAGLIFLOZIN", "CKD", relation="HIGHLY_RECOMMENDED_FOR", benefit="Làm chậm tốc độ suy giảm eGFR")

        # =====================================================================
        # 5. MÓN ĂN VIỆT NAM VÀ CHỈ SỐ GI / GL (VIETNAMESE FOODS KNOWLEDGE)
        # =====================================================================
        foods_data = [
            {
                "id": "FOOD_COM_TRANG",
                "name": "Cơm trắng (Gạo tẻ nấu)",
                "category": "Tinh bột truyền thống",
                "gi": 83,
                "gi_level": "Cao (High GI >= 70)",
                "gl_per_serving": 28.5,
                "calories_per_100g": 130,
                "advice": "Gây tăng vọt đường huyết sau ăn. Giảm khẩu phần xuống 1/2 - 1 bát, ưu tiên ăn cùng nhiều rau xanh trước.",
                "healthy_alternatives": ["FOOD_COM_GAO_LUC", "FOOD_KHOAI_LANG"]
            },
            {
                "id": "FOOD_COM_GAO_LUC",
                "name": "Cơm gạo lứt",
                "category": "Ngũ cốc nguyên cám",
                "gi": 55,
                "gi_level": "Trung bình thấp (Low-Medium GI <= 55)",
                "gl_per_serving": 15.2,
                "calories_per_100g": 111,
                "advice": "Giàu chất xơ hòa tan và vitamin nhóm B, giúp đường huyết tăng chậm, tạo cảm giác no lâu.",
                "healthy_alternatives": []
            },
            {
                "id": "FOOD_KHOAI_LANG",
                "name": "Khoai lang luộc (ăn cả vỏ)",
                "category": "Củ giàu tinh bột tốt",
                "gi": 48,
                "gi_level": "Thấp (Low GI <= 55)",
                "gl_per_serving": 11.0,
                "calories_per_100g": 86,
                "advice": "Lựa chọn thay thế tinh bột tuyệt vời cho bữa sáng hoặc bữa phụ, kiểm soát calo tốt.",
                "healthy_alternatives": []
            },
            {
                "id": "FOOD_PHO_BO",
                "name": "Phở bò truyền thống (1 tô)",
                "category": "Món nước truyền thống",
                "gi": 72,
                "gi_level": "Cao",
                "gl_per_serving": 32.0,
                "calories_per_100g": 110,
                "advice": "Nước dùng phở chứa nhiều chất béo bão hòa và muối Natri, bánh phở GI cao. Nên ăn bánh phở vừa phải, xin thêm giá trụng/rau thơm, hạn chế húp cạn nước dùng.",
                "healthy_alternatives": ["FOOD_BUN_MOC_RAU"]
            },
            {
                "id": "FOOD_BANH_MI_THIT",
                "name": "Bánh mì kẹp thịt pate",
                "category": "Thức ăn nhanh đường phố",
                "gi": 75,
                "gi_level": "Cao",
                "gl_per_serving": 29.0,
                "calories_per_100g": 260,
                "advice": "Bánh mì bột mì tinh luyện tiêu hóa cực nhanh gây tăng đường huyết, pate nhiều mỡ động vật. Nên giảm 1/2 phần bánh hoặc chuyển sang bánh mì đen nguyên cám.",
                "healthy_alternatives": ["FOOD_BANH_MI_DEN"]
            },
            {
                "id": "FOOD_TRA_SUA",
                "name": "Trà sữa trân châu có đường",
                "category": "Đồ uống ngọt giải khát",
                "gi": 88,
                "gi_level": "Rất cao (Nguy hiểm cho bệnh nhân ĐTĐ)",
                "gl_per_serving": 45.0,
                "calories_per_100g": 180,
                "advice": "Chứa lượng đường siro fructose tự do và chất béo chuyển hóa cực lớn. Bệnh nhân đái tháo đường cần kiêng hoàn toàn.",
                "healthy_alternatives": ["FOOD_TRA_XANH_MATCHA"]
            },
            {
                "id": "FOOD_TRA_XANH_MATCHA",
                "name": "Trà xanh nguyên chất / Trà Ô long không đường",
                "category": "Đồ uống lành mạnh",
                "gi": 0,
                "gi_level": "0 (Không đường)",
                "gl_per_serving": 0,
                "calories_per_100g": 1,
                "advice": "Chứa polyphenol và EGCG tăng độ nhạy insulin, chống oxy hóa mạch máu.",
                "healthy_alternatives": []
            }
        ]

        for f in foods_data:
            fid = f["id"]
            g.add_node(fid, type="Food", **f)
            for alt in f.get("healthy_alternatives", []):
                g.add_edge(fid, alt, relation="CAN_BE_REPLACED_BY")

        # =====================================================================
        # 6. LIÊN KẾT HOẠT CHẤT VỚI DANH MỤC THUỐC LONG CHÂU (PHARMACY MAPPING)
        # =====================================================================
        ingredient_map = {
            "METFORMIN": ["lc_dia_01", "lc_dia_02", "lc_dia_03"],
            "GLICLAZIDE": ["lc_dia_04", "lc_dia_05"],
            "DAPAGLIFLOZIN": ["lc_dia_06"],
            "EMPAGLIFLOZIN": ["lc_dia_07"],
            "SITAGLIPTIN": ["lc_dia_08"],
            "INSULIN_GLARGINE": ["lc_dia_09"]
        }

        # Lưu thông tin sản phẩm vào node
        for prod in self.pharmacy_products:
            pid = prod["id"]
            g.add_node(pid, type="PharmacyProduct", **prod)

        for drug_id, prod_ids in ingredient_map.items():
            for pid in prod_ids:
                if pid in g:
                    g.add_edge(drug_id, pid, relation="DISPENSED_AS_PRODUCT")

        print(f"[KnowledgeGraph] Khởi tạo thành công Đồ thị Tri thức ĐTĐ: {g.number_of_nodes()} Nodes, {g.number_of_edges()} Edges")

    # =========================================================================
    # CÁC HÀM TRUY VẤN VÀ SUY LUẬN TRI THỨC (INFERENCE & QUERY APIS)
    # =========================================================================

    def check_contraindications(
        self,
        drugs: List[str],
        patient_egfr: Optional[float] = None,
        has_heavy_alcohol: bool = False,
        has_heart_failure: bool = False,
        has_liver_disease: bool = False,
        age: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Kiểm tra rà soát an toàn dược lý (Safety Guardian Check) dựa trên KG:
        Phát hiện chống chỉ định tuyệt đối, cảnh báo tương tác và nguy cơ biến cố.
        """
        warnings = []
        drugs_upper = [d.upper() for d in drugs]

        for d in drugs_upper:
            # 1. Kiểm tra Metformin
            if "METFORMIN" in d or "GLUCOPHAGE" in d:
                if patient_egfr is not None:
                    if patient_egfr < 30:
                        warnings.append({
                            "severity": "CRITICAL_BLOCKED",
                            "drug": "Metformin",
                            "violation": f"Mức lọc cầu thận eGFR = {patient_egfr} mL/min (< 30 mL/min). Chống chỉ định tuyệt đối Metformin do nguy cơ Nhiễm toan Lactic (Lactic Acidosis) đe dọa tính mạng theo QĐ 5481/QĐ-BYT.",
                            "recommended_action": "Ngừng ngay Metformin. Đổi sang phác đồ Insulin hoặc ức chế DPP-4 chỉnh liều theo chức năng thận."
                        })
                    elif patient_egfr < 45:
                        warnings.append({
                            "severity": "WARNING_ADJUST_DOSE",
                            "drug": "Metformin",
                            "violation": f"Mức lọc cầu thận eGFR = {patient_egfr} mL/min (suy thận độ 3b: 30-44 mL/min).",
                            "recommended_action": "Giảm 50% liều Metformin tối đa (không vượt quá 1000mg/ngày) và theo dõi định kỳ chức năng thận mỗi 3 tháng."
                        })

                if has_heavy_alcohol:
                    warnings.append({
                        "severity": "CRITICAL_BLOCKED",
                        "drug": "Metformin",
                        "violation": "Bệnh nhân có tiền sử uống rượu bia nhiều/mãn tính kết hợp Metformin gây ức chế thanh thải Lactate tại gan, làm tăng đột biến nguy cơ toan Lactic.",
                        "recommended_action": "Khuyên bệnh nhân kiêng rượu tuyệt đối hoặc thay đổi nhóm thuốc hạ đường huyết an toàn hơn."
                    })

                if has_liver_disease:
                    warnings.append({
                        "severity": "CRITICAL_BLOCKED",
                        "drug": "Metformin",
                        "violation": "Bệnh nhân suy gan hoặc xơ gan nặng: Giảm đào thải acid lactic.",
                        "recommended_action": "Chống chỉ định dùng Metformin ở bệnh nhân suy gan tiến triển."
                    })

            # 2. Kiểm tra Sulfonylurea (Gliclazide)
            if "GLICLAZIDE" in d or "DIAMICRON" in d:
                if age is not None and age >= 75:
                    warnings.append({
                        "severity": "WARNING_CAUTION",
                        "drug": "Gliclazide",
                        "violation": f"Bệnh nhân cao tuổi ({age} tuổi) dùng Sulfonylurea có nguy cơ cao bị hạ đường huyết thầm lặng dẫn tới ngã quỵ hoặc hôn mê.",
                        "recommended_action": "Dùng liều khởi đầu thấp (30mg MR) hoặc ưu tiên nhóm DPP-4i (Sitagliptin) ít gây hạ đường huyết."
                    })

            # 3. Kiểm tra SGLT-2i (Dapagliflozin / Empagliflozin)
            if "DAPAGLIFLOZIN" in d or "FORXIGA" in d or "EMPAGLIFLOZIN" in d or "JARDIANCE" in d:
                if patient_egfr is not None and patient_egfr < 20:
                    warnings.append({
                        "severity": "CRITICAL_BLOCKED",
                        "drug": "SGLT2 inhibitor",
                        "violation": f"eGFR = {patient_egfr} mL/min (< 20 mL/min). Cơ chế lọc thải đường qua cầu thận không còn hiệu quả.",
                        "recommended_action": "Không chỉ định bắt đầu SGLT2i khi eGFR < 20 mL/min."
                    })
                if has_heart_failure:
                    warnings.append({
                        "severity": "BENEFICIAL_INDICATION",
                        "drug": "SGLT2 inhibitor",
                        "violation": "Chỉ định vàng: SGLT2i giảm nguy cơ nhập viện vì suy tim và giảm tử vong tim mạch (Class I, Level A theo ADA/ESC).",
                        "recommended_action": "Rất khuyến khích đưa SGLT2i vào phác đồ điều trị nền tảng."
                    })

        return warnings

    def get_pharmacy_products_for_drug(self, drug_id: str) -> List[Dict[str, Any]]:
        """Lấy danh sách các sản phẩm Long Châu tương ứng với hoạt chất thuốc."""
        g = self.graph
        products = []
        if drug_id in g:
            for neighbor in g.neighbors(drug_id):
                node_data = g.nodes[neighbor]
                if node_data.get("type") == "PharmacyProduct":
                    products.append(node_data)
        return products

    def lookup_food_nutrition(self, food_query: str) -> Optional[Dict[str, Any]]:
        """Tra cứu chỉ số GI/GL và phương án thay thế lành mạnh cho món ăn Việt Nam."""
        q = food_query.lower()
        for node, data in self.graph.nodes(data=True):
            if data.get("type") == "Food":
                name = data.get("name", "").lower()
                cat = data.get("category", "").lower()
                if q in name or q in cat:
                    # Lấy danh sách món ăn thay thế lành mạnh
                    alternatives = []
                    for succ in self.graph.successors(node):
                        alt_data = self.graph.nodes[succ]
                        if alt_data.get("type") == "Food":
                            alternatives.append({
                                "name": alt_data.get("name"),
                                "gi": alt_data.get("gi"),
                                "gi_level": alt_data.get("gi_level"),
                                "calories": alt_data.get("calories_per_100g")
                            })
                    res = dict(data)
                    res["alternatives_info"] = alternatives
                    return res
        return None

    def export_summary(self) -> Dict[str, Any]:
        """Tóm tắt số liệu của Đồ thị Tri thức."""
        type_counts = {}
        for _, data in self.graph.nodes(data=True):
            t = data.get("type", "Unknown")
            type_counts[t] = type_counts.get(t, 0) + 1
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "nodes_by_type": type_counts
        }


if __name__ == "__main__":
    kg = DiabetesKnowledgeGraph()
    summary = kg.export_summary()
    print("\n--- TỔNG KẾT ĐỒ THỊ TRI THỨC ĐÁI THÁO ĐƯỜNG ---")
    print(f"Tổng số node: {summary['total_nodes']} | Cạnh quan hệ: {summary['total_edges']}")
    for k, v in summary["nodes_by_type"].items():
        print(f" - {k}: {v} nodes")

    print("\n--- TEST RÀ SOÁT CHỐNG CHỈ ĐỊNH DƯỢC LÝ ---")
    # Tình huống 1: Bệnh nhân suy thận nặng eGFR = 24 mL/min được kê Metformin
    alerts = kg.check_contraindications(drugs=["Metformin", "Forxiga"], patient_egfr=24.0)
    for a in alerts:
        print(f"[{a['severity']}] {a['drug']}: {a['violation']}")
        print(f"  → Khuyến nghị: {a['recommended_action']}")

    print("\n--- TEST TRA CỨU MÓN ĂN VIỆT NAM (CƠM TRẮNG) ---")
    food = kg.lookup_food_nutrition("Cơm trắng")
    if food:
        print(f"Món: {food['name']} | GI: {food['gi']} ({food['gi_level']}) | Calo: {food['calories_per_100g']} kcal/100g")
        print(f"Lời khuyên: {food['advice']}")
        print("Món thay thế lành mạnh:")
        for alt in food.get("alternatives_info", []):
            print(f"  * {alt['name']} (GI: {alt['gi']}, {alt['gi_level']})")

    print("\n--- TEST MAPPING THUỐC SANG LONG CHÂU PHARMACY ---")
    prods = kg.get_pharmacy_products_for_drug("METFORMIN")
    print(f"Tìm thấy {len(prods)} sản phẩm Long Châu cho hoạt chất Metformin:")
    for p in prods:
        print(f" - {p['brand_name']} | Giá: {p['unit_price_vnd']:,}đ/viên | URL: {p['longchau_url']}")
