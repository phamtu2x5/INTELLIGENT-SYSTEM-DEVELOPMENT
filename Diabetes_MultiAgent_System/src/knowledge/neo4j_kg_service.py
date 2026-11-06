#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
neo4j_kg_service.py
===================
Dịch vụ Quản lý và Tích hợp Đồ thị Tri thức Đái tháo đường Mở rộng trên Neo4j (Graph Database).
Lưu trữ toàn diện KB thành Graph chuẩn hóa với 143+ Nodes và 280+ Relationships từ các nguồn:
1. Văn bản PDF: Quyết định 5481/QĐ-BYT Bộ Y Tế.
2. Web / Y khoa: Bài viết lâm sàng Vinmec (Triệu chứng, Bệnh tim mạch, Biến chứng bàn chân, Thần kinh).
3. Viện Dinh Dưỡng Quốc Gia (NIN): Chỉ số GI/GL và thực phẩm thay thế lành mạnh.
4. ADA 2024 (Standards of Care in Diabetes).
5. Hệ thống Dược phẩm & Nhà thuốc FPT Long Châu (Thuốc Rx, Vật tư que thử/máy đo, Dinh dưỡng y học).
"""

import os
import json
from typing import Dict, List, Any, Optional
from neo4j import GraphDatabase, Driver

class Neo4jKGService:
    def __init__(
        self,
        uri: str = "bolt://localhost:7687",
        user: str = "neo4j",
        password: str = "password123"
    ):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver: Optional[Driver] = None
        self._connect()

    def _connect(self) -> bool:
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            self.driver.verify_connectivity()
            print(f"[Neo4j] ✓ Kết nối thành công tới Neo4j tại {self.uri}")
            return True
        except Exception as e:
            print(f"[Neo4j Warning] Không thể kết nối Neo4j ({e}). Sẽ sử dụng Fallback NetworkX.")
            self.driver = None
            return False

    def is_connected(self) -> bool:
        if self.driver is None:
            return False
        try:
            self.driver.verify_connectivity()
            return True
        except Exception:
            return False

    def close(self):
        if self.driver:
            self.driver.close()

    def execute_cypher(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Thực thi câu truy vấn Cypher và trả về danh sách bản ghi dạng dict."""
        if not self.is_connected():
            return []
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def init_database_schema(self):
        """Khởi tạo ràng buộc duy nhất (Unique Constraints) trên Neo4j cho mọi loại thực thể."""
        if not self.is_connected():
            return
        
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Source) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Disease) REQUIRE d.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (sym:Symptom) REQUIRE sym.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (b:Biomarker) REQUIRE b.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Complication) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (cb:Comorbidity) REQUIRE cb.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (rf:RiskFactor) REQUIRE rf.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (dr:Drug) REQUIRE dr.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (a:AdverseEffect) REQUIRE a.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (f:Food) REQUIRE f.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:PharmacyProduct) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (cp:ClinicalProtocol) REQUIRE cp.id IS UNIQUE"
        ]
        
        with self.driver.session() as session:
            for c in constraints:
                try:
                    session.run(c)
                except Exception as e:
                    pass

    def populate_from_kb(self, export_cypher_file: Optional[str] = None):
        """
        Nạp đồ thị tri thức quy mô mở rộng (>140 nodes, >280 relationships) vào Neo4j.
        Đồng thời xuất tệp kb_diabet_init.cypher để backup và sử dụng ngoại tuyến.
        """
        if not self.is_connected():
            print("[Neo4j] Không thể nạp dữ liệu vì chưa kết nối được Neo4j.")
            return False

        print("[Neo4j] Đang khởi tạo và nạp Đồ thị Tri thức Mở rộng vào Neo4j...")
        self.init_database_schema()

        # Đọc dữ liệu sản phẩm Long Châu
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        pharmacy_file = os.path.join(base_dir, "data", "pharmacy", "longchau_diabetes_products.json")
        pharmacy_items = []
        if os.path.exists(pharmacy_file):
            with open(pharmacy_file, "r", encoding="utf-8") as f:
                pharmacy_items = json.load(f)

        node_statements = []
        rel_statements = []

        # -------------------------------------------------------------
        # 1. TẠO CÁC NODE (ENTITIES)
        # -------------------------------------------------------------
        # A. Sources (5 nodes)
        node_statements.append("""
        MERGE (:Source {id: 'SRC_BYT_5481', name: 'QĐ 5481/QĐ-BYT Bộ Y Tế (30/12/2020)', type: 'PDF_GUIDELINE', scope: 'Chuẩn quốc gia Việt Nam'});
        """)
        node_statements.append("""
        MERGE (:Source {id: 'SRC_VINMEC', name: 'Hướng dẫn Lâm sàng Nội tiết Bệnh viện Vinmec', type: 'WEB_CLINICAL', scope: 'Chẩn đoán và biến chứng lâm sàng'});
        """)
        node_statements.append("""
        MERGE (:Source {id: 'SRC_NIN', name: 'Bảng thành phần thực phẩm Viện Dinh Dưỡng Quốc Gia (NIN)', type: 'NUTRITION_TABLE', scope: 'Dinh dưỡng lâm sàng & Chỉ số GI/GL'});
        """)
        node_statements.append("""
        MERGE (:Source {id: 'SRC_ADA_2024', name: 'Standards of Care in Diabetes - ADA 2024', type: 'INT_GUIDELINE', scope: 'Khuyến cáo tim thận quốc tế'});
        """)
        node_statements.append("""
        MERGE (:Source {id: 'SRC_LONGCHAU', name: 'Hệ thống Nhà thuốc FPT Long Châu', type: 'PHARMACY_ECOMMERCE', scope: 'Danh mục thuốc thương mại & Thiết bị y tế'});
        """)

        # B. Diseases (5 nodes)
        node_statements.append("""
        MERGE (:Disease {id: 'T2D', name: 'Đái tháo đường Type 2', icd10: 'E11', desc: 'Rối loạn chuyển hóa glucose mạn tính đặc trưng bởi sự đề kháng insulin và suy giảm tiết insulin tiến triển'});
        """)
        node_statements.append("""
        MERGE (:Disease {id: 'PRE_DIABETES', name: 'Tiền đái tháo đường', icd10: 'R73.0', desc: 'Rối loạn đường huyết lúc đói (IFG) hoặc rối loạn dung nạp glucose (IGT), nguy cơ cao tiến triển T2D'});
        """)
        node_statements.append("""
        MERGE (:Disease {id: 'T1D', name: 'Đái tháo đường Type 1', icd10: 'E10', desc: 'Phá hủy tế bào beta tụy qua trung gian tự miễn, dẫn đến thiếu hụt insulin tuyệt đối'});
        """)
        node_statements.append("""
        MERGE (:Disease {id: 'GESTATIONAL_DIABETES', name: 'Đái tháo đường thai kỳ', icd10: 'O24.4', desc: 'Tình trạng rối loạn dung nạp đường huyết được phát hiện lần đầu trong thai kỳ'});
        """)
        node_statements.append("""
        MERGE (:Disease {id: 'METABOLIC_SYNDROME', name: 'Hội chứng chuyển hóa', icd10: 'E88.81', desc: 'Tập hợp các yếu tố nguy cơ bao gồm béo phì trung tâm, tăng huyết áp, tăng triglycerid và giảm HDL-C'});
        """)

        # C. Symptoms (10 nodes)
        symptoms = [
            ('SYM_POLYURIA', 'Đi tiểu nhiều lần (Polyuria)', 'Hội chứng 4 nhiều', 'Thận tăng bài tiết nước tiểu để đào thải nồng độ glucose dư thừa qua ngưỡng lọc'),
            ('SYM_POLYDIPSIA', 'Thường xuyên khát nước (Polydipsia)', 'Hội chứng 4 nhiều', 'Cơ thể kích hoạt trung tâm khát ở não do mất nước thẩm thấu'),
            ('SYM_POLYPHAGIA', 'Ăn nhiều / Nhanh đói (Polyphagia)', 'Hội chứng 4 nhiều', 'Tế bào thiếu năng lượng do glucose không vào được bên trong tế bào'),
            ('SYM_WEIGHT_LOSS', 'Sụt cân bất thường (Weight Loss)', 'Hội chứng 4 nhiều', 'Dị hóa lipid và protein cơ bắp để cung cấp năng lượng thay thế cho glucose'),
            ('SYM_FATIGUE', 'Mệt mỏi kéo dài (Fatigue)', 'Triệu chứng toàn thân', 'Tế bào suy giảm chuyển hóa năng lượng ATP'),
            ('SYM_BLURRED_VISION', 'Nhìn mờ tạm thời (Blurred Vision)', 'Triệu chứng thị giác', 'Tăng áp lực thẩm thấu làm thay đổi thể tích nước và hình dạng thủy tinh thể'),
            ('SYM_NUMBNESS', 'Tê bì, dị cảm châm chích bàn chân (Paresthesia)', 'Thần kinh ngoại biên', 'Tổn thương sớm bao myelin và các sợi thần kinh cảm giác ngoại vi'),
            ('SYM_SLOW_HEALING', 'Vết thương chậm lành (Slow Wound Healing)', 'Tổn thương vi mạch', 'Lưu thông máu kém và suy giảm chức năng thực bào của bạch cầu'),
            ('SYM_DRY_MOUTH', 'Khô miệng họng (Dry Mouth)', 'Mất nước', 'Giảm bài tiết tuyến nước bọt do mất nước mạn tính'),
            ('SYM_RECURRENT_INFECTION', 'Nhiễm trùng nấm tái phát (Recurrent Infections)', 'Miễn dịch', 'Môi trường đường huyết cao tạo điều kiện thuận lợi cho nấm Candida và vi khuẩn phát triển')
        ]
        for sid, sname, scat, sdesc in symptoms:
            node_statements.append(f"""
            MERGE (:Symptom {{id: '{sid}', name: '{sname}', category: '{scat}', desc: '{sdesc}'}});
            """)

        # D. Biomarkers (14 nodes)
        biomarkers = [
            ('HBA1C', 'Chỉ số HbA1c (Hemoglobin A1c)', '%', '< 5.7', '5.7 - 6.4', '>= 6.5', '< 7.0'),
            ('FPG', 'Glucose huyết tương lúc đói (FPG)', 'mg/dL', '70 - 99', '100 - 125', '>= 126', '80 - 130'),
            ('OGTT_2H', 'Nghiệm pháp dung nạp glucose đường uống 2h (OGTT 75g)', 'mg/dL', '< 140', '140 - 199', '>= 200', '< 140'),
            ('RPG', 'Glucose huyết tương bất kỳ (RPG)', 'mg/dL', '< 140', '140 - 199', '>= 200', '< 180'),
            ('EGFR', 'Độ lọc cầu thận ước tính (eGFR CKD-EPI)', 'mL/min/1.73m2', '>= 90', '60 - 89', '< 60', '>= 60'),
            ('CREATININE', 'Creatinine huyết thanh', 'mg/dL', '0.7 - 1.2', '1.3 - 1.5', '>= 1.5', '< 1.2'),
            ('UACR', 'Tỷ số Albumin / Creatinine niệu (UACR)', 'mg/g', '< 30', '30 - 299', '>= 300', '< 30'),
            ('BMI', 'Chỉ số khối cơ thể (BMI)', 'kg/m2', '18.5 - 22.9', '23.0 - 24.9', '>= 25.0', '18.5 - 22.9'),
            ('WAIST', 'Chu vi vòng eo', 'cm', '< 90 (Nam) / < 80 (Nữ)', '90 (Nam) / 80 (Nữ)', '>= 90 (Nam) / >= 80 (Nữ)', '< 90 / < 80'),
            ('BP_SYS', 'Huyết áp tâm thu', 'mmHg', '< 120', '120 - 129', '>= 130', '< 130'),
            ('BP_DIA', 'Huyết áp tâm trương', 'mmHg', '< 80', '80 - 84', '>= 85', '< 80'),
            ('LIPID_LDL', 'Cholesterol LDL-C (Xấu)', 'mg/dL', '< 100', '100 - 129', '>= 130', '< 70'),
            ('LIPID_HDL', 'Cholesterol HDL-C (Tốt)', 'mg/dL', '> 50', '40 - 50', '< 40', '> 40 (Nam) / > 50 (Nữ)'),
            ('LIPID_TRIGLYCERIDE', 'Triglyceride huyết thanh', 'mg/dL', '< 150', '150 - 199', '>= 200', '< 150')
        ]
        for bid, bname, unit, norm, pre, dia, target in biomarkers:
            node_statements.append(f"""
            MERGE (:Biomarker {{id: '{bid}', name: '{bname}', unit: '{unit}', normal: '{norm}', prediabetic: '{pre}', diabetic: '{dia}', target: '{target}'}});
            """)

        # E. Complications (8 nodes), Comorbidities (3 nodes), Risk Factors (4 nodes)
        complications = [
            ('CKD', 'Bệnh thận mạn do đái tháo đường (Diabetic Kidney Disease)', 'N18', 'Xơ hóa cầu thận tiến triển dẫn đến suy thận giai đoạn cuối'),
            ('ASCVD', 'Bệnh lý tim mạch do xơ vữa (ASCVD)', 'I25', 'Nhồi máu cơ tim cấp, đột quỵ thiếu máu cục bộ não'),
            ('HEART_FAILURE', 'Suy tim sung huyết (Heart Failure - HFrEF/HFpEF)', 'I50', 'Khó thở khi gắng sức, phù phổi, giảm phân suất tống máu'),
            ('DIABETIC_RETINOPATHY', 'Bệnh võng mạc đái tháo đường', 'E11.3', 'Xuất huyết dịch kính, bong võng mạc, nguy cơ mù lòa vĩnh viễn'),
            ('DIABETIC_NEUROPATHY', 'Bệnh thần kinh ngoại biên đái tháo đường', 'E11.4', 'Mất cảm giác bảo vệ đau nhiệt, dị cảm đối xứng kiểu mang bít tất'),
            ('DIABETIC_FOOT_ULCER', 'Loét bàn chân đái tháo đường (Diabetic Foot Ulcer)', 'E11.7', 'Hoại tử mô sâu nhiễm khuẩn kết hợp bệnh mạch máu ngoại biên, nguy cơ cắt cụt chi'),
            ('PAD', 'Bệnh động mạch ngoại biên chi dưới (PAD)', 'I73.9', 'Đau cách hồi, thiếu máu nuôi dưỡng bàn chân'),
            ('DIABETIC_GASTROPARESIS', 'Liệt dạ dày do đái tháo đường', 'K31.84', 'Chậm làm rỗng dạ dày, buồn nôn, chướng bụng, đường huyết dao động khó lường')
        ]
        for cid, cname, icd, risk in complications:
            node_statements.append(f"""
            MERGE (:Complication {{id: '{cid}', name: '{cname}', icd10: '{icd}', risk: '{risk}'}});
            """)

        comorbidities = [
            ('HYPERTENSION', 'Tăng huyết áp đồng mắc', 'I10', '< 130/80 mmHg'),
            ('DYSLIPIDEMIA', 'Rối loạn lipid máu hỗn hợp', 'E78', 'LDL-C < 70 mg/dL'),
            ('NAFLD', 'Gan nhiễm mỡ liên quan rối loạn chuyển hóa (MASLD/NAFLD)', 'K76.0', 'Kiểm soát cân nặng và enzyme men gan ALT/AST')
        ]
        for cbid, cbname, icd, target in comorbidities:
            node_statements.append(f"""
            MERGE (:Comorbidity {{id: '{cbid}', name: '{cbname}', icd10: '{icd}', target: '{target}'}});
            """)

        risk_factors = [
            ('OBESITY', 'Béo phì / Thừa cân theo chuẩn IDI & WPRO', 'BMI >= 23.0 kg/m2'),
            ('FAMILY_HISTORY', 'Tiền sử gia đình trực hệ mắc đái tháo đường', 'Bố mẹ hoặc anh chị em ruột mắc T2D'),
            ('SMOKING', 'Hút thuốc lá chủ động / thụ động', 'Làm tổn thương nặng thêm nội mô mạch máu'),
            ('PHYSICAL_INACTIVITY', 'Lối sống tĩnh tại ít vận động thể lực', '< 150 phút hoạt động thể lực mỗi tuần')
        ]
        for rfid, rfname, thresh in risk_factors:
            node_statements.append(f"""
            MERGE (:RiskFactor {{id: '{rfid}', name: '{rfname}', threshold: '{thresh}'}});
            """)

        # F. Adverse Effects (12 nodes)
        adverse_effects = [
            ('LACTIC_ACIDOSIS', 'Nhiễm toan Acid Lactic cấp tính', 'FATAL', '50%', 'Cồn rượu bia / Suy thận nặng eGFR < 30 mL/phút'),
            ('HYPOGLYCEMIA_MILD', 'Hạ đường huyết mức độ nhẹ - trung bình (< 70 mg/dL)', 'MODERATE', '0.1%', 'Quy tắc 15-15 bổ sung 15g đường nhanh'),
            ('HYPOGLYCEMIA_SEVERE', 'Hạ đường huyết mức độ nặng', 'SEVERE', '5%', 'Cần người khác trợ giúp, co giật hoặc hôn mê sâu'),
            ('DKA', 'Nhiễm toan Ceton đái tháo đường (Diabetic Ketoacidosis)', 'CRITICAL', '5-10%', 'Thở nhanh sâu Kussmaul, mùi hơi thở táo thối ceton'),
            ('EUG_DKA', 'Nhiễm toan Ceton đường huyết bình thường (Euglycemic DKA)', 'HIGH', '2-5%', 'Tác dụng không mong muốn của thuốc SGLT2i khi thiếu insulin'),
            ('HHS', 'Hội chứng tăng áp lực thẩm thấu do tăng đường huyết', 'CRITICAL', '10-20%', 'Đường huyết > 600 mg/dL, áp lực thẩm thấu máu > 320 mOsm/kg'),
            ('UTI', 'Nhiễm khuẩn đường tiết niệu & nấm sinh dục', 'MODERATE', '< 0.01%', 'Tăng nồng độ đường trong nước tiểu nuôi dưỡng vi khuẩn'),
            ('GI_UPSET', 'Rối loạn tiêu hóa (Buồn nôn, tiêu chảy, đầy bụng)', 'MILD', '0%', 'Thường gặp khi bắt đầu dùng Metformin hoặc GLP-1 RA'),
            ('WEIGHT_GAIN', 'Tăng cân ngoài ý muốn', 'MILD_MODERATE', '0%', 'Tác dụng đồng hóa của Sulfonylurea hoặc Insulin'),
            ('PERIPHERAL_EDEMA', 'Phù ngoại biên (Giữ nước)', 'MODERATE', '0%', 'Tăng giữ muối nước do cơ chế Thiazolidinediones'),
            ('FOURNIER_GANGRENE', 'Hoại thư sinh dục hoại tử Fournier', 'RARE_FATAL', '20-30%', 'Cảnh báo FDA và Bộ Y Tế cho nhóm thuốc SGLT2i'),
            ('PANCREATITIS_ACUTE', 'Viêm tụy cấp', 'SEVERE', '5%', 'Cảnh báo thận trọng hiếm gặp của DPP-4i hoặc GLP-1 RA')
        ]
        for aid, aname, sev, mort, desc in adverse_effects:
            node_statements.append(f"""
            MERGE (:AdverseEffect {{id: '{aid}', name: '{aname}', severity: '{sev}', mortality: '{mort}', detail: '{desc}'}});
            """)

        # G. Drugs (18 nodes)
        drugs = [
            ('METFORMIN', 'Metformin Hydrochloride', 'Biguanide', 'First-line (Thuốc đầu tay bắt buộc nếu không chống chỉ định)'),
            ('GLICLAZIDE', 'Gliclazide MR', 'Sulfonylurea thế hệ 2', 'Add-on kích thích tiết insulin'),
            ('GLIMEPIRIDE', 'Glimepiride', 'Sulfonylurea thế hệ 3', 'Add-on kích thích tiết insulin 1 lần/ngày'),
            ('GLIBENCLAMIDE', 'Glibenclamide', 'Sulfonylurea thế hệ 2 cũ', 'Hạn chế dùng do nguy cơ hạ đường huyết kéo dài'),
            ('DAPAGLIFLOZIN', 'Dapagliflozin', 'SGLT-2 Inhibitor', 'Bảo vệ tim mạch & Làm chậm suy thận mạn'),
            ('EMPAGLIFLOZIN', 'Empagliflozin', 'SGLT-2 Inhibitor', 'Giảm tử vong tim mạch & Bảo vệ thận'),
            ('CANAGLIFLOZIN', 'Canagliflozin', 'SGLT-2 Inhibitor', 'Bảo vệ tim thận & Giảm biến cố CKD'),
            ('SITAGLIPTIN', 'Sitagliptin', 'DPP-4 Inhibitor', 'Add-on dung nạp tốt, an toàn ít hạ đường huyết'),
            ('VILDAGLIPTIN', 'Vildagliptin', 'DPP-4 Inhibitor', 'Add-on tăng tiết insulin theo glucose máu'),
            ('LINAGLIPTIN', 'Linagliptin', 'DPP-4 Inhibitor (Thải qua gan mật)', 'An toàn cho mọi mức độ suy thận không cần chỉnh liều'),
            ('SAXAGLIPTIN', 'Saxagliptin', 'DPP-4 Inhibitor', 'Thận trọng tiền sử suy tim'),
            ('SEMAGLUTIDE', 'Semaglutide', 'GLP-1 Receptor Agonist', 'Bảo vệ tim mạch vượt trội & Giảm cân mạnh'),
            ('LIRAGLUTIDE', 'Liraglutide', 'GLP-1 Receptor Agonist', 'Bảo vệ tim mạch & Giảm biến cố xơ vữa'),
            ('DULAGLUTIDE', 'Dulaglutide', 'GLP-1 Receptor Agonist', 'Tiêm 1 lần/tuần bảo vệ tim mạch'),
            ('PIOGLITAZONE', 'Pioglitazone', 'Thiazolidinedione (TZD)', 'Tăng nhạy cảm insulin ngoại vi, giảm đề kháng gan'),
            ('ACARBOSE', 'Acarbose', 'Alpha-glucosidase Inhibitor', 'Làm chậm hấp thu glucose tinh bột tại ruột non'),
            ('INSULIN_GLARGINE', 'Insulin Glargine (Lantus / Toujeo)', 'Basal Insulin Analogue', 'Kiểm soát đường huyết nền 24h ổn định không đỉnh'),
            ('INSULIN_ASPART', 'Insulin Aspart (NovoRapid)', 'Rapid-acting Insulin Analogue', 'Kiểm soát đường huyết đỉnh sau bữa ăn')
        ]
        for drid, drname, drclass, drline in drugs:
            node_statements.append(f"""
            MERGE (:Drug {{id: '{drid}', name: '{drname}', class: '{drclass}', line: '{drline}'}});
            """)

        # H. Foods (29 nodes: 13 High GI, 16 Low GI)
        foods = [
            # High GI (13 món)
            ('FOOD_COM_TRANG', 'Cơm trắng (Gạo tẻ)', 83, 'Tinh bột nhanh', 'Tăng vọt đường huyết sau ăn, cần hạn chế khẩu phần và ăn kèm nhiều rau xanh'),
            ('FOOD_XOI_NEP', 'Xôi nếp các loại', 90, 'Tinh bột nếp cực nhanh', 'Mật độ năng lượng và amylopectin rất cao, tránh ăn bữa sáng liên tục'),
            ('FOOD_BANH_MI_TRANG', 'Bánh mì trắng', 85, 'Bột mì tinh luyện', 'Hấp thu glucose nhanh chóng, không có chất xơ cám'),
            ('FOOD_BANH_CHUNG', 'Bánh chưng / Bánh tét', 85, 'Nếp bão hòa mỡ', 'Năng lượng cực cao kết hợp mỡ động vật thịt ba chỉ, hạn chế ngày lễ Tết'),
            ('FOOD_PHO_BO', 'Phở bò nước béo', 72, 'Món nước nhiều dầu mỡ', 'Bánh phở GI cao kết hợp nước dùng nhiều mỡ bão hòa và muối Natri'),
            ('FOOD_BUN_BO_HUE', 'Bún bò Huế nước béo', 75, 'Món nước đậm vị', 'Nhiều gia vị muối và mỡ bò, dễ tăng vọt đường huyết và huyết áp'),
            ('FOOD_BANH_CUON', 'Bánh cuốn chả quế', 78, 'Bột gạo hấp', 'Lượng tinh bột cao dễ gây no nhanh và tăng đường sau 1 giờ'),
            ('FOOD_BANH_MI_THIT', 'Bánh mì kẹp thịt pate', 76, 'Thức ăn nhanh đường phố', 'Bột mì tinh luyện kết hợp pate gan béo mỡ động vật'),
            ('FOOD_TRA_SUA', 'Trà sữa trân châu có đường', 88, 'Đường lỏng fructose', 'Cấm kỵ tuyệt đối: đường siro lỏng và bột béo công nghiệp chuyển hóa xấu'),
            ('FOOD_NUOC_NGOT', 'Nước ngọt có gas / Tăng lực', 95, 'Đường đơn hấp thu tức thì', 'Chỉ sử dụng 100-150ml khi cấp cứu hạ đường huyết nặng theo Quy tắc 15-15'),
            ('FOOD_CHE_NGOT', 'Chè ngọt nước cốt dừa', 82, 'Đồ ngọt truyền thống', 'Lượng đường tinh luyện và chất béo bão hòa từ dừa rất cao'),
            ('FOOD_DUA_HAU', 'Dưa hấu đỏ', 76, 'Trái cây ngọt nhanh', 'Chỉ số GI cao, chỉ nên ăn 1-2 miếng nhỏ sau bữa chính cách 2 tiếng'),
            ('FOOD_CHAO_LONG', 'Cháo lòng heo / Cháo hoa', 80, 'Cháo ninh nhừ', 'Tinh bột hồ hóa phân giải đường tức thì, nội tạng nhiều cholesterol'),
            # Low GI (16 món)
            ('FOOD_COM_GAO_LUC', 'Cơm gạo lứt (Đỏ/Đen)', 55, 'Ngũ cốc nguyên cám', 'Giàu chất xơ hòa tan beta-glucan và vitamin B, giúp đường huyết ổn định'),
            ('FOOD_KHOAI_LANG', 'Khoai lang luộc cả vỏ', 48, 'Củ giàu chất xơ', 'Lựa chọn tinh bột thay thế tuyệt vời cho bữa sáng, tạo cảm giác no lâu'),
            ('FOOD_BUN_MOC_RAU', 'Bún mọc nhiều rau xanh', 50, 'Món nước thanh đạm', 'Nước dùng trong ít béo, kèm nhiều rau sống xà lách, giá đỗ làm chậm hấp thu đường'),
            ('FOOD_BANH_MI_DEN', 'Bánh mì lúa mạch đen nguyên cám', 48, 'Ngũ cốc nguyên hạt', 'Hạn chế tăng đường huyết đỉnh sau ăn nhờ tỷ lệ xơ thô cao'),
            ('FOOD_YEN_MACH', 'Yến mạch nguyên hạt nấu', 52, 'Ngũ cốc chất lượng cao', 'Hạ mỡ máu LDL-C và kiểm soát đường huyết đói rất tốt'),
            ('FOOD_NGO_LUOC', 'Ngô (bắp) nếp luộc', 52, 'Ngũ cốc thô', 'Ăn 1/2 bắp cho bữa phụ giúp chống hạ đường huyết êm dịu'),
            ('FOOD_BONG_CAI_XANH', 'Bông cải xanh (Súp lơ) luộc', 15, 'Rau họ cải', 'Giàu sulforaphane chống viêm nội mô mạch máu và chất xơ tuyệt hảo'),
            ('FOOD_RAU_MUONG', 'Rau muống luộc / xào tỏi', 10, 'Rau lá xanh Việt Nam', 'Ăn một đĩa rau luộc trước bữa ăn chính để phủ một lớp màng chất xơ ở ruột'),
            ('FOOD_DAU_BAP', 'Đậu bắp hấp / luộc', 20, 'Rau nhớt bảo vệ', 'Chất nhầy tự nhiên làm chậm tốc độ tiêu hóa tinh bột tại tá tràng'),
            ('FOOD_KHO_QUA', 'Mướp đắng (Khổ qua) xào trứng / hấp', 15, 'Rau dược liệu', 'Chứa Charantin có tác dụng hỗ trợ hạ glucose tương tự insulin nội sinh'),
            ('FOOD_CA_HAP', 'Cá lóc / Cá hồi hấp hành gừng', 0, 'Đạm lành mạnh Omega-3', 'Không chứa carbohydrate, cung cấp đạm dễ tiêu và bảo vệ tim mạch'),
            ('FOOD_UC_GA', 'Ức gà hấp / áp chảo ít dầu', 0, 'Đạm nạc chất lượng', 'Cung cấp năng lượng duy trì cơ bắp cho người bệnh đái tháo đường'),
            ('FOOD_DAU_PHU', 'Đậu phụ luộc / hấp', 15, 'Đạm thực vật', 'Giàu Isoflavone, không chứa cholesterol xấu'),
            ('FOOD_BUOI', 'Bưởi da xanh / Năm roi', 25, 'Trái cây múi giàu Vitamin C', 'Ăn 2-3 múi mỗi ngày giúp tăng cường đề kháng mà không tăng đường'),
            ('FOOD_TAO_XANH', 'Táo xanh tươi cả vỏ', 36, 'Trái cây giàu Pectin', 'Chất xơ Pectin làm sạch đường ruột và ổn định chuyển hóa'),
            ('FOOD_TRA_XANH_MATCHA', 'Trà xanh nguyên chất / Ô long', 0, 'Đồ uống chống oxy hóa', 'Chứa hợp chất EGCG bảo vệ tế bào beta tụy và tăng độ nhạy insulin')
        ]
        for fid, fname, fgi, fcat, fadv in foods:
            node_statements.append(f"""
            MERGE (:Food {{id: '{fid}', name: '{fname}', gi: {fgi}, category: '{fcat}', advice: '{fadv}'}});
            """)

        # I. Clinical Protocols (5 nodes)
        protocols = [
            ('PROTOCOL_FITT', 'Phác đồ vận động thể lực FITT chuẩn ADA & Bộ Y Tế', '150 phút aerobic cường độ trung bình/tuần kết hợp 2-3 buổi tập kháng lực, không ngưng quá 2 ngày'),
            ('PROTOCOL_RULE_15', 'Quy tắc cấp cứu 15-15 hạ đường huyết', 'Bổ sung ngay 15g carbohydrate tác dụng nhanh (3 viên đường / 150ml nước ngọt), nghỉ ngơi và đo lại sau 15 phút'),
            ('PROTOCOL_FOOT_CARE', 'Quy trình kiểm tra & chăm sóc bàn chân hằng ngày', 'Rửa chân nước ấm, lau khô kỹ các kẽ ngón, quan sát vết nứt hoặc chai sần, mang tất đệm mềm, không đi chân đất'),
            ('PROTOCOL_PLATE_METHOD', 'Mô hình đĩa thức ăn chuẩn NIN & Harvard', '1/2 đĩa là rau củ quả không chứa tinh bột; 1/4 đĩa là protein nạc lành mạnh; 1/4 đĩa là tinh bột chuyển hóa chậm'),
            ('PROTOCOL_SMBG', 'Quy trình tự theo dõi đường huyết mao mạch (SMBG)', 'Đo đường huyết lúc đói sáng sớm, trước bữa ăn và 2 giờ sau ăn để theo dõi hiệu quả điều trị')
        ]
        for cpid, cpname, cpdesc in protocols:
            node_statements.append(f"""
            MERGE (:ClinicalProtocol {{id: '{cpid}', name: '{cpname}', desc: '{cpdesc}'}});
            """)

        # J. Pharmacy Products (30 nodes)
        for item in pharmacy_items:
            pid = item.get("id")
            bname = item.get("brand_name", "").replace("'", "\\'")
            ingred = item.get("active_ingredient", "").replace("'", "\\'")
            dclass = item.get("drug_class", "").replace("'", "\\'")
            mfg = item.get("manufacturer", "").replace("'", "\\'")
            pkg = item.get("packaging", "").replace("'", "\\'")
            price = item.get("box_price_vnd", 0)
            uprice = item.get("unit_price_vnd", 0)
            rx = "true" if item.get("is_prescription_rx", False) else "false"
            url = item.get("longchau_url", "")
            ind = item.get("indication", "").replace("'", "\\'")

            node_statements.append(f"""
            MERGE (p:PharmacyProduct {{id: '{pid}'}})
            SET p.brand_name = '{bname}',
                p.active_ingredient = '{ingred}',
                p.drug_class = '{dclass}',
                p.manufacturer = '{mfg}',
                p.packaging = '{pkg}',
                p.box_price_vnd = {price},
                p.unit_price_vnd = {uprice},
                p.is_prescription_rx = {rx},
                p.indication = '{ind}',
                p.longchau_url = '{url}';
            """)

        # -------------------------------------------------------------
        # 2. TẠO CÁC MỐI QUAN HỆ (RELATIONSHIPS)
        # Sử dụng MATCH (a {id: ...}), (b {id: ...}) MERGE (a)-[r:...]->(b)
        # -------------------------------------------------------------

        # Triệu chứng lâm sàng
        sym_map = [
            ('T2D', 'SYM_POLYURIA', 'VERY_COMMON'),
            ('T2D', 'SYM_POLYDIPSIA', 'VERY_COMMON'),
            ('T2D', 'SYM_POLYPHAGIA', 'COMMON'),
            ('T2D', 'SYM_WEIGHT_LOSS', 'COMMON'),
            ('T2D', 'SYM_FATIGUE', 'COMMON'),
            ('T2D', 'SYM_BLURRED_VISION', 'OCCASIONAL'),
            ('T2D', 'SYM_NUMBNESS', 'COMMON'),
            ('T2D', 'SYM_SLOW_HEALING', 'COMMON'),
            ('T2D', 'SYM_DRY_MOUTH', 'COMMON'),
            ('T2D', 'SYM_RECURRENT_INFECTION', 'OCCASIONAL'),
            ('PRE_DIABETES', 'SYM_FATIGUE', 'INSIDIOUS'),
            ('PRE_DIABETES', 'SYM_NUMBNESS', 'INSIDIOUS'),
            ('T1D', 'SYM_POLYURIA', 'ACUTE'),
            ('T1D', 'SYM_POLYDIPSIA', 'ACUTE'),
            ('T1D', 'SYM_WEIGHT_LOSS', 'ACUTE')
        ]
        for did, sid, freq in sym_map:
            rel_statements.append(f"""
            MATCH (d:Disease {{id: '{did}'}}), (s:Symptom {{id: '{sid}'}})
            MERGE (d)-[:HAS_SYMPTOM {{frequency: '{freq}'}}]->(s);
            """)

        # Chẩn đoán theo Chỉ số sinh học (DIAGNOSED_BY)
        diag_map = [
            ('T2D', 'HBA1C', "threshold: 'HbA1c >= 6.5%', method: 'Chuẩn NGSP/DCCT theo QĐ 5481'"),
            ('T2D', 'FPG', "threshold: 'FPG >= 126 mg/dL', condition: 'Nhịn đói ít nhất 8 tiếng'"),
            ('T2D', 'OGTT_2H', "threshold: 'OGTT 2h >= 200 mg/dL', method: '75g Anhydrous Glucose'"),
            ('T2D', 'RPG', "threshold: 'RPG >= 200 mg/dL', condition: 'Đi kèm triệu chứng lâm sàng kinh điển'"),
            ('PRE_DIABETES', 'HBA1C', "threshold: '5.7% <= HbA1c <= 6.4%'"),
            ('PRE_DIABETES', 'FPG', "threshold: '100 mg/dL <= FPG <= 125 mg/dL'"),
            ('PRE_DIABETES', 'OGTT_2H', "threshold: '140 mg/dL <= OGTT 2h <= 199 mg/dL'"),
            ('CKD', 'EGFR', "threshold: 'eGFR < 60 mL/min/1.73m2 kéo dài > 3 tháng'"),
            ('CKD', 'UACR', "threshold: 'UACR >= 30 mg/g'"),
            ('CKD', 'CREATININE', "threshold: 'Creatinine tăng cao'"),
            ('HYPERTENSION', 'BP_SYS', "threshold: 'Huyết áp tâm thu >= 130 mmHg'"),
            ('HYPERTENSION', 'BP_DIA', "threshold: 'Huyết áp tâm trương >= 80 mmHg'"),
            ('DYSLIPIDEMIA', 'LIPID_LDL', "threshold: 'LDL-C >= 100 mg/dL'"),
            ('DYSLIPIDEMIA', 'LIPID_TRIGLYCERIDE', "threshold: 'Triglyceride >= 150 mg/dL'"),
            ('OBESITY', 'BMI', "threshold: 'BMI >= 23.0 kg/m2 (Chuẩn IDI/WPRO)'"),
            ('OBESITY', 'WAIST', "threshold: 'Vòng eo >= 90cm (Nam) / >= 80cm (Nữ)'")
        ]
        for src_id, target_id, props in diag_map:
            rel_statements.append(f"""
            MATCH (a {{id: '{src_id}'}}), (b {{id: '{target_id}'}})
            MERGE (a)-[:DIAGNOSED_BY {{{props}}}]->(b);
            """)

        # Biến chứng (CAUSES_COMPLICATION)
        comp_map = [
            ('T2D', 'CKD', 'Tổn thương màng đáy mao mạch cầu thận và tăng áp lực lọc'),
            ('T2D', 'ASCVD', 'Rối loạn nội mô mạch máu và oxy hóa hạt LDL xơ vữa'),
            ('T2D', 'HEART_FAILURE', 'Bệnh cơ tim đái tháo đường và quá tải thể tích mạn tính'),
            ('T2D', 'DIABETIC_RETINOPATHY', 'Tổn thương vi mạch võng mạc gây vi phình mạch và tân mạch xuất huyết'),
            ('T2D', 'DIABETIC_NEUROPATHY', 'Độc tính glucose tích tụ Sorbitol và tổn thương mạch nuôi dây thần kinh'),
            ('T2D', 'DIABETIC_FOOT_ULCER', 'Phối hợp mất cảm giác thần kinh và thiếu máu tưới nuôi dưỡng mô sâu'),
            ('T2D', 'PAD', 'Xơ cứng và hẹp tắc các động mạch vừa và lớn nuôi chi dưới'),
            ('T2D', 'DIABETIC_GASTROPARESIS', 'Tổn thương dây thần kinh phế vị chi phối nhu động dạ dày')
        ]
        for did, cid, mech in comp_map:
            rel_statements.append(f"""
            MATCH (d:Disease {{id: '{did}'}}), (c:Complication {{id: '{cid}'}})
            MERGE (d)-[:CAUSES_COMPLICATION {{mechanism: '{mech}'}}]->(c);
            """)

        # Yếu tố tăng nặng (AGGRAVATES)
        agg_map = [
            ('HYPERTENSION', 'ASCVD', 'Gia tăng gấp 3 lần nguy cơ đột quỵ và nhồi máu cơ tim'),
            ('HYPERTENSION', 'CKD', 'Đẩy nhanh tốc độ giảm eGFR và xuất hiện đạm niệu'),
            ('DYSLIPIDEMIA', 'ASCVD', 'Tăng sinh và tích tụ mảng xơ vữa không ổn định'),
            ('OBESITY', 'T2D', 'Gia tăng đề kháng insulin và viêm mạn tính hệ thống'),
            ('OBESITY', 'NAFLD', 'Tích tụ mỡ nội tạng xâm lấn và thoái hóa nhu mô gan'),
            ('SMOKING', 'ASCVD', 'Làm co thắt mạch vành và hoại tử tế bào nội mạc'),
            ('SMOKING', 'PAD', 'Tăng nguy cơ hoại tử chi dưới và cắt cụt chi gấp 4 lần'),
            ('PHYSICAL_INACTIVITY', 'T2D', 'Giảm vận chuyển kênh GLUT4 lên màng tế bào cơ vân')
        ]
        for aid, bid, impact in agg_map:
            rel_statements.append(f"""
            MATCH (a {{id: '{aid}'}}), (b {{id: '{bid}'}})
            MERGE (a)-[:AGGRAVATES {{impact: '{impact}'}}]->(b);
            """)

        # Điều trị thuốc (TREATS)
        treat_map = [
            ('METFORMIN', 'T2D', 'priority: 1, guideline: "QĐ 5481/QĐ-BYT"'),
            ('GLICLAZIDE', 'T2D', 'priority: 2'),
            ('GLIMEPIRIDE', 'T2D', 'priority: 2'),
            ('GLIBENCLAMIDE', 'T2D', 'priority: 3'),
            ('DAPAGLIFLOZIN', 'T2D', 'priority: 1, condition: "Kèm suy tim hoặc bệnh thận mạn"'),
            ('EMPAGLIFLOZIN', 'T2D', 'priority: 1, condition: "Kèm bệnh tim mạch hoặc suy tim"'),
            ('CANAGLIFLOZIN', 'T2D', 'priority: 2'),
            ('SITAGLIPTIN', 'T2D', 'priority: 2'),
            ('VILDAGLIPTIN', 'T2D', 'priority: 2'),
            ('LINAGLIPTIN', 'T2D', 'priority: 2'),
            ('SAXAGLIPTIN', 'T2D', 'priority: 3'),
            ('SEMAGLUTIDE', 'T2D', 'priority: 1, condition: "Kèm béo phì hoặc bệnh tim mạch xơ vữa"'),
            ('LIRAGLUTIDE', 'T2D', 'priority: 1, condition: "Kèm bệnh tim mạch xơ vữa"'),
            ('DULAGLUTIDE', 'T2D', 'priority: 2'),
            ('PIOGLITAZONE', 'T2D', 'priority: 2'),
            ('ACARBOSE', 'T2D', 'priority: 3'),
            ('INSULIN_GLARGINE', 'T2D', 'priority: 2, condition: "Thất bại thuốc uống hoặc HbA1c > 9.0%"'),
            ('INSULIN_ASPART', 'T2D', 'priority: 3, condition: "Phác đồ Basal-Bolus hoặc ăn nhiều carb"'),
            ('INSULIN_GLARGINE', 'T1D', 'priority: 1, condition: "Liệu pháp bắt buộc suốt đời"'),
            ('INSULIN_ASPART', 'T1D', 'priority: 1, condition: "Liệu pháp bắt buộc trước bữa ăn"')
        ]
        for drid, did, props in treat_map:
            rel_statements.append(f"""
            MATCH (dr:Drug {{id: '{drid}'}}), (d:Disease {{id: '{did}'}})
            MERGE (dr)-[:TREATS {{{props}}}]->(d);
            """)

        # Khuyến cáo mạnh bảo vệ tim thận (HIGHLY_RECOMMENDED_FOR)
        rec_map = [
            ('DAPAGLIFLOZIN', 'CKD', 'DAPA-CKD: Giảm 39% nguy cơ suy thận tiến triển'),
            ('DAPAGLIFLOZIN', 'HEART_FAILURE', 'DAPA-HF: Giảm 26% tử vong tim mạch và tái nhập viện'),
            ('DAPAGLIFLOZIN', 'ASCVD', 'Làm giảm gánh nặng tim mạch toàn diện'),
            ('EMPAGLIFLOZIN', 'CKD', 'EMPA-KIDNEY: Làm chậm rõ rệt suy giảm chức năng lọc'),
            ('EMPAGLIFLOZIN', 'HEART_FAILURE', 'EMPEROR-Reduced & Preserved: Bảo vệ phân suất tống máu'),
            ('EMPAGLIFLOZIN', 'ASCVD', 'EMPA-REG OUTCOME: Giảm 38% tử vong do biến cố tim mạch'),
            ('SEMAGLUTIDE', 'ASCVD', 'SUSTAIN-6: Giảm 26% biến cố tim mạch chính MACE'),
            ('SEMAGLUTIDE', 'CKD', 'FLOW trial: Bảo vệ thận độc lập'),
            ('SEMAGLUTIDE', 'OBESITY', 'STEP trial: Giảm trung bình 15% trọng lượng cơ thể'),
            ('LIRAGLUTIDE', 'ASCVD', 'LEADER trial: Giảm 13% biến cố tim mạch lớn')
        ]
        for drid, cid, ev in rec_map:
            rel_statements.append(f"""
            MATCH (dr:Drug {{id: '{drid}'}}), (c {{id: '{cid}'}})
            MERGE (dr)-[:HIGHLY_RECOMMENDED_FOR {{evidence: '{ev}'}}]->(c);
            """)

        # Chống chỉ định (CONTRAINDICATED_IN)
        contra_map = [
            ('METFORMIN', 'CKD', "condition: 'eGFR < 30 mL/min/1.73m2', severity: 'ABSOLUTE', reason: 'Tích tụ nguy cơ nhiễm toan acid lactic tử vong'"),
            ('DAPAGLIFLOZIN', 'CKD', "condition: 'eGFR < 20 mL/min/1.73m2 để khởi đầu điều trị', severity: 'ABSOLUTE'"),
            ('EMPAGLIFLOZIN', 'CKD', "condition: 'eGFR < 20 mL/min/1.73m2 để khởi đầu điều trị', severity: 'ABSOLUTE'"),
            ('PIOGLITAZONE', 'HEART_FAILURE', "condition: 'Suy tim mức độ NYHA II - IV', severity: 'ABSOLUTE', reason: 'Gây giữ nước và làm trầm trọng suy tim'"),
            ('SAXAGLIPTIN', 'HEART_FAILURE', "condition: 'Bệnh nhân có tiền sử hoặc nguy cơ suy tim cao (SAVOR-TIMI 53)', severity: 'RELATIVE'")
        ]
        for drid, cid, props in contra_map:
            rel_statements.append(f"""
            MATCH (dr:Drug {{id: '{drid}'}}), (c {{id: '{cid}'}})
            MERGE (dr)-[:CONTRAINDICATED_IN {{{props}}}]->(c);
            """)

        # Thận trọng điều chỉnh liều (CAUTION_IN)
        caution_map = [
            ('METFORMIN', 'CKD', "condition: '30 <= eGFR < 45 mL/min', instruction: 'Giảm 50% liều dùng (tối đa 1000 mg/ngày), kiểm tra eGFR mỗi 3 tháng'"),
            ('GLICLAZIDE', 'CKD', "condition: 'eGFR < 45 mL/min', instruction: 'Cần giảm liều và cảnh báo nguy cơ hạ đường huyết kéo dài'"),
            ('GLIMEPIRIDE', 'CKD', "condition: 'Suy giảm chức năng thận', instruction: 'Khởi đầu với liều thấp 1mg/ngày'"),
            ('LINAGLIPTIN', 'CKD', "instruction: 'Thải trừ 95% qua gan mật, an toàn tuyệt đối không cần chỉnh liều ở mọi giai đoạn CKD'")
        ]
        for drid, cid, props in caution_map:
            rel_statements.append(f"""
            MATCH (dr:Drug {{id: '{drid}'}}), (c {{id: '{cid}'}})
            MERGE (dr)-[:CAUTION_IN {{{props}}}]->(c);
            """)

        # Nguy cơ tác dụng phụ (RISK_OF)
        risk_map = [
            ('METFORMIN', 'LACTIC_ACIDOSIS', "trigger: 'Uống rượu bia / Sử dụng cồn / Thiếu oxy mô cấp', severity: 'FATAL'"),
            ('METFORMIN', 'GI_UPSET', "frequency: '20-30% bệnh nhân trong 2-4 tuần đầu'"),
            ('GLICLAZIDE', 'HYPOGLYCEMIA_MILD', "trigger: 'Bỏ bữa ăn, lao động thể lực quá mức, hoặc người cao tuổi'"),
            ('GLICLAZIDE', 'WEIGHT_GAIN', "cause: 'Tác dụng đồng hóa của việc tăng tiết insulin'"),
            ('GLIMEPIRIDE', 'HYPOGLYCEMIA_MILD', "trigger: 'Bỏ bữa ăn hoặc dùng quá liều'"),
            ('GLIBENCLAMIDE', 'HYPOGLYCEMIA_SEVERE', "severity: 'HIGH_RISK_OF_FATAL_HYPO'"),
            ('DAPAGLIFLOZIN', 'UTI', "prevention: 'Uống đủ nước (1.5 - 2L/ngày), vệ sinh sạch sẽ bộ phận sinh dục'"),
            ('DAPAGLIFLOZIN', 'EUG_DKA', "trigger: 'Thiếu hụt insulin tương đối hoặc nhịn ăn kéo dài'"),
            ('DAPAGLIFLOZIN', 'FOURNIER_GANGRENE', "severity: 'RARE_WARNING'"),
            ('EMPAGLIFLOZIN', 'UTI', "prevention: 'Uống nhiều nước'"),
            ('EMPAGLIFLOZIN', 'EUG_DKA', "trigger: 'Thiếu insulin'"),
            ('SEMAGLUTIDE', 'GI_UPSET', "frequency: 'Buồn nôn nhẹ khi tăng liều, thường tự hết sau vài tuần'"),
            ('SEMAGLUTIDE', 'PANCREATITIS_ACUTE', "warning: 'Ngừng thuốc vĩnh viễn nếu nghi ngờ viêm tụy'"),
            ('LIRAGLUTIDE', 'GI_UPSET', "frequency: 'Thường gặp giai đoạn đầu'"),
            ('PIOGLITAZONE', 'PERIPHERAL_EDEMA', "cause: 'Giữ muối nước ở ống thận'"),
            ('PIOGLITAZONE', 'WEIGHT_GAIN', "cause: 'Tăng sinh mô mỡ dưới da'"),
            ('INSULIN_GLARGINE', 'HYPOGLYCEMIA_MILD', "trigger: 'Tiêm quá liều hoặc ăn không đủ lượng carb'"),
            ('INSULIN_GLARGINE', 'HYPOGLYCEMIA_SEVERE', "trigger: 'Bỏ bữa ăn chính sau khi tiêm'"),
            ('INSULIN_GLARGINE', 'WEIGHT_GAIN', "cause: 'Tích tụ mỡ do insulin đồng hóa'"),
            ('INSULIN_ASPART', 'HYPOGLYCEMIA_MILD', "trigger: 'Tiêm nhưng ăn muộn quá 15 phút'")
        ]
        for drid, aid, props in risk_map:
            rel_statements.append(f"""
            MATCH (dr:Drug {{id: '{drid}'}}), (a:AdverseEffect {{id: '{aid}'}})
            MERGE (dr)-[:RISK_OF {{{props}}}]->(a);
            """)

        # Theo dõi chỉ số (MONITORED_BY)
        mon_map = [
            ('METFORMIN', 'EGFR'),
            ('METFORMIN', 'CREATININE'),
            ('METFORMIN', 'HBA1C'),
            ('GLICLAZIDE', 'FPG'),
            ('GLICLAZIDE', 'HBA1C'),
            ('DAPAGLIFLOZIN', 'EGFR'),
            ('DAPAGLIFLOZIN', 'BP_SYS'),
            ('DAPAGLIFLOZIN', 'HBA1C'),
            ('EMPAGLIFLOZIN', 'EGFR'),
            ('EMPAGLIFLOZIN', 'HBA1C'),
            ('SEMAGLUTIDE', 'BMI'),
            ('SEMAGLUTIDE', 'HBA1C'),
            ('INSULIN_GLARGINE', 'FPG'),
            ('INSULIN_ASPART', 'FPG')
        ]
        for drid, bid in mon_map:
            rel_statements.append(f"""
            MATCH (dr:Drug {{id: '{drid}'}}), (b:Biomarker {{id: '{bid}'}})
            MERGE (dr)-[:MONITORED_BY]->(b);
            """)

        # Chuyển đổi thực phẩm lành mạnh (CAN_BE_REPLACED_BY)
        food_swaps = [
            ('FOOD_COM_TRANG', 'FOOD_COM_GAO_LUC', 'Chỉ số GI thấp hơn 28 đơn vị, hàm lượng chất xơ cao gấp 3 lần'),
            ('FOOD_COM_TRANG', 'FOOD_KHOAI_LANG', 'Chỉ số GI thấp hơn 35 đơn vị, tạo cảm giác no lâu cho bữa chính'),
            ('FOOD_XOI_NEP', 'FOOD_YEN_MACH', 'Thay thế nếp dẻo bằng ngũ cốc thô giàu chất xơ hòa tan beta-glucan'),
            ('FOOD_XOI_NEP', 'FOOD_NGO_LUOC', 'Ngô luộc GI thấp hơn 38 đơn vị so với xôi nếp béo'),
            ('FOOD_BANH_MI_TRANG', 'FOOD_BANH_MI_DEN', 'Bánh mì đen nguyên cám GI 48 so với bánh mì trắng GI 85'),
            ('FOOD_BANH_CHUNG', 'FOOD_COM_GAO_LUC', 'Cắt giảm chất béo động vật bão hòa và tinh bột nếp'),
            ('FOOD_PHO_BO', 'FOOD_BUN_MOC_RAU', 'Bún mọc nước thanh kết hợp nhiều rau xanh giúp giảm 22 đơn vị GI'),
            ('FOOD_BUN_BO_HUE', 'FOOD_BUN_MOC_RAU', 'Giảm lượng mỡ bò và muối bão hòa gây biến chứng tim thận'),
            ('FOOD_BANH_CUON', 'FOOD_BANH_MI_DEN', 'Bánh mì đen nguyên cám giàu dinh dưỡng và ít gây nhũ hóa đường ruột'),
            ('FOOD_BANH_MI_THIT', 'FOOD_BANH_MI_DEN', 'Bánh mì đen kẹp ức gà nạc thay thế cho pate mỡ động vật'),
            ('FOOD_TRA_SUA', 'FOOD_TRA_XANH_MATCHA', 'Trà xanh tự nhiên không đường bổ sung EGCG chống oxy hóa'),
            ('FOOD_NUOC_NGOT', 'FOOD_TRA_XANH_MATCHA', 'Nước lọc hoặc trà xanh nguyên chất không chứa calo rỗng'),
            ('FOOD_CHE_NGOT', 'FOOD_BUOI', 'Bưởi tươi ngọt nhẹ giàu vitamin thay thế cho chè đường ngọt'),
            ('FOOD_DUA_HAU', 'FOOD_TAO_XANH', 'Táo xanh chỉ số GI 36 so với dưa hấu GI 76'),
            ('FOOD_CHAO_LONG', 'FOOD_CA_HAP', 'Cá hồi hấp cung cấp protein lành mạnh không làm tăng vọt đường huyết')
        ]
        for f1, f2, reason in food_swaps:
            rel_statements.append(f"""
            MATCH (orig:Food {{id: '{f1}'}}), (rep:Food {{id: '{f2}'}})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {{reason: '{reason}'}}]->(rep);
            """)

        # Phác đồ lâm sàng & lối sống (RECOMMENDED_LIFESTYLE / TREATED_BY_PROTOCOL)
        protocol_links = [
            ('T2D', 'PROTOCOL_FITT', 'RECOMMENDED_LIFESTYLE'),
            ('T2D', 'PROTOCOL_PLATE_METHOD', 'RECOMMENDED_LIFESTYLE'),
            ('T2D', 'PROTOCOL_SMBG', 'RECOMMENDED_LIFESTYLE'),
            ('PRE_DIABETES', 'PROTOCOL_FITT', 'RECOMMENDED_LIFESTYLE'),
            ('PRE_DIABETES', 'PROTOCOL_PLATE_METHOD', 'RECOMMENDED_LIFESTYLE'),
            ('HYPOGLYCEMIA_MILD', 'PROTOCOL_RULE_15', 'TREATED_BY_PROTOCOL'),
            ('DIABETIC_FOOT_ULCER', 'PROTOCOL_FOOT_CARE', 'TREATED_BY_PROTOCOL')
        ]
        for aid, pid, rel in protocol_links:
            rel_statements.append(f"""
            MATCH (a {{id: '{aid}'}}), (p:ClinicalProtocol {{id: '{pid}'}})
            MERGE (a)-[:{rel}]->(p);
            """)

        # Ánh xạ Dược chất sang Sản phẩm thương mại Long Châu (DISPENSED_AS_PRODUCT)
        drug_product_map = [
            ('METFORMIN', 'lc_dia_01'),
            ('METFORMIN', 'lc_dia_02'),
            ('METFORMIN', 'lc_dia_03'),
            ('METFORMIN', 'lc_dia_04'),
            ('METFORMIN', 'lc_dia_05'),
            ('GLICLAZIDE', 'lc_dia_06'),
            ('GLICLAZIDE', 'lc_dia_07'),
            ('GLIMEPIRIDE', 'lc_dia_08'),
            ('DAPAGLIFLOZIN', 'lc_dia_09'),
            ('EMPAGLIFLOZIN', 'lc_dia_10'),
            ('EMPAGLIFLOZIN', 'lc_dia_11'),
            ('SITAGLIPTIN', 'lc_dia_12'),
            ('SITAGLIPTIN', 'lc_dia_13'),
            ('VILDAGLIPTIN', 'lc_dia_14'),
            ('LINAGLIPTIN', 'lc_dia_15'),
            ('PIOGLITAZONE', 'lc_dia_16'),
            ('ACARBOSE', 'lc_dia_17'),
            ('INSULIN_GLARGINE', 'lc_dia_18'),
            ('INSULIN_GLARGINE', 'lc_dia_19'),
            ('INSULIN_ASPART', 'lc_dia_20'),
            ('LIRAGLUTIDE', 'lc_dia_22')
        ]
        for drug_id, prod_id in drug_product_map:
            rel_statements.append(f"""
            MATCH (dr:Drug {{id: '{drug_id}'}}), (p:PharmacyProduct {{id: '{prod_id}'}})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
            """)

        # Thiết bị y tế & Dinh dưỡng Long Châu
        device_mappings = [
            ('T2D', 'lc_dia_23', 'RECOMMENDED_DEVICE_FOR'),
            ('T2D', 'lc_dia_24', 'RECOMMENDED_DEVICE_FOR'),
            ('T2D', 'lc_dia_25', 'RECOMMENDED_DEVICE_FOR'),
            ('T2D', 'lc_dia_26', 'RECOMMENDED_DEVICE_FOR'),
            ('T2D', 'lc_dia_27', 'RECOMMENDED_DEVICE_FOR'),
            ('T2D', 'lc_dia_28', 'RECOMMENDED_DEVICE_FOR'),
            ('T2D', 'lc_dia_29', 'NUTRITIONAL_SUPPORT_FOR'),
            ('T2D', 'lc_dia_30', 'NUTRITIONAL_SUPPORT_FOR')
        ]
        for did, pid, rel in device_mappings:
            rel_statements.append(f"""
            MATCH (d:Disease {{id: '{did}'}}), (p:PharmacyProduct {{id: '{pid}'}})
            MERGE (d)-[:{rel}]->(p);
            """)

        # Nguồn trích dẫn (CITED_FROM)
        citations = [
            # Từ QĐ 5481/QĐ-BYT Bộ Y Tế
            ('T2D', 'SRC_BYT_5481'),
            ('PRE_DIABETES', 'SRC_BYT_5481'),
            ('T1D', 'SRC_BYT_5481'),
            ('GESTATIONAL_DIABETES', 'SRC_BYT_5481'),
            ('METABOLIC_SYNDROME', 'SRC_BYT_5481'),
            ('HBA1C', 'SRC_BYT_5481'),
            ('FPG', 'SRC_BYT_5481'),
            ('OGTT_2H', 'SRC_BYT_5481'),
            ('RPG', 'SRC_BYT_5481'),
            ('EGFR', 'SRC_BYT_5481'),
            ('CREATININE', 'SRC_BYT_5481'),
            ('UACR', 'SRC_BYT_5481'),
            ('BMI', 'SRC_BYT_5481'),
            ('CKD', 'SRC_BYT_5481'),
            ('ASCVD', 'SRC_BYT_5481'),
            ('HEART_FAILURE', 'SRC_BYT_5481'),
            ('DIABETIC_RETINOPATHY', 'SRC_BYT_5481'),
            ('DIABETIC_NEUROPATHY', 'SRC_BYT_5481'),
            ('HYPERTENSION', 'SRC_BYT_5481'),
            ('DYSLIPIDEMIA', 'SRC_BYT_5481'),
            ('OBESITY', 'SRC_BYT_5481'),
            ('METFORMIN', 'SRC_BYT_5481'),
            ('GLICLAZIDE', 'SRC_BYT_5481'),
            ('GLIMEPIRIDE', 'SRC_BYT_5481'),
            ('GLIBENCLAMIDE', 'SRC_BYT_5481'),
            ('DAPAGLIFLOZIN', 'SRC_BYT_5481'),
            ('EMPAGLIFLOZIN', 'SRC_BYT_5481'),
            ('SITAGLIPTIN', 'SRC_BYT_5481'),
            ('VILDAGLIPTIN', 'SRC_BYT_5481'),
            ('LINAGLIPTIN', 'SRC_BYT_5481'),
            ('INSULIN_GLARGINE', 'SRC_BYT_5481'),
            ('INSULIN_ASPART', 'SRC_BYT_5481'),
            ('LACTIC_ACIDOSIS', 'SRC_BYT_5481'),
            ('HYPOGLYCEMIA_MILD', 'SRC_BYT_5481'),
            ('HYPOGLYCEMIA_SEVERE', 'SRC_BYT_5481'),
            ('DKA', 'SRC_BYT_5481'),
            ('HHS', 'SRC_BYT_5481'),
            ('PROTOCOL_FITT', 'SRC_BYT_5481'),
            ('PROTOCOL_RULE_15', 'SRC_BYT_5481'),
            ('PROTOCOL_SMBG', 'SRC_BYT_5481'),

            # Từ Hướng dẫn Vinmec
            ('SYM_NUMBNESS', 'SRC_VINMEC'),
            ('SYM_SLOW_HEALING', 'SRC_VINMEC'),
            ('SYM_BLURRED_VISION', 'SRC_VINMEC'),
            ('DIABETIC_FOOT_ULCER', 'SRC_VINMEC'),
            ('DIABETIC_NEUROPATHY', 'SRC_VINMEC'),
            ('PAD', 'SRC_VINMEC'),
            ('DIABETIC_GASTROPARESIS', 'SRC_VINMEC'),
            ('PROTOCOL_FOOT_CARE', 'SRC_VINMEC'),

            # Từ Viện Dinh Dưỡng NIN
            ('FOOD_COM_TRANG', 'SRC_NIN'),
            ('FOOD_COM_GAO_LUC', 'SRC_NIN'),
            ('FOOD_KHOAI_LANG', 'SRC_NIN'),
            ('FOOD_PHO_BO', 'SRC_NIN'),
            ('FOOD_BUN_MOC_RAU', 'SRC_NIN'),
            ('FOOD_BANH_MI_TRANG', 'SRC_NIN'),
            ('FOOD_BANH_MI_DEN', 'SRC_NIN'),
            ('FOOD_YEN_MACH', 'SRC_NIN'),
            ('FOOD_BONG_CAI_XANH', 'SRC_NIN'),
            ('FOOD_RAU_MUONG', 'SRC_NIN'),
            ('FOOD_DAU_BAP', 'SRC_NIN'),
            ('FOOD_KHO_QUA', 'SRC_NIN'),
            ('FOOD_CA_HAP', 'SRC_NIN'),
            ('FOOD_UC_GA', 'SRC_NIN'),
            ('FOOD_BUOI', 'SRC_NIN'),
            ('FOOD_TAO_XANH', 'SRC_NIN'),
            ('PROTOCOL_PLATE_METHOD', 'SRC_NIN'),

            # Từ ADA 2024
            ('EUG_DKA', 'SRC_ADA_2024'),
            ('SEMAGLUTIDE', 'SRC_ADA_2024'),
            ('LIRAGLUTIDE', 'SRC_ADA_2024'),
            ('DULAGLUTIDE', 'SRC_ADA_2024'),
            ('CANAGLIFLOZIN', 'SRC_ADA_2024')
        ]
        for src_node, source_id in citations:
            rel_statements.append(f"""
            MATCH (n {{id: '{src_node}'}}), (s:Source {{id: '{source_id}'}})
            MERGE (n)-[:CITED_FROM]->(s);
            """)

        # Gán nguồn Long Châu cho toàn bộ sản phẩm
        for item in pharmacy_items:
            rel_statements.append(f"""
            MATCH (p:PharmacyProduct {{id: '{item['id']}'}}), (s:Source {{id: 'SRC_LONGCHAU'}})
            MERGE (p)-[:CITED_FROM]->(s);
            """)

        # -------------------------------------------------------------
        # THỰC THI TOÀN BỘ VÀO NEO4J DATABASE
        # -------------------------------------------------------------
        with self.driver.session() as session:
            # Thực thi tạo nodes
            for stmt in node_statements:
                stmt_clean = stmt.strip()
                if stmt_clean:
                    session.run(stmt_clean)
            
            # Thực thi tạo relationships
            for stmt in rel_statements:
                stmt_clean = stmt.strip()
                if stmt_clean:
                    session.run(stmt_clean)

        # Xuất tệp kb_diabet_init.cypher hoàn chỉnh
        if export_cypher_file is None:
            export_cypher_file = os.path.join(base_dir, "data", "knowledge_graph", "kb_diabet_init.cypher")
        
        os.makedirs(os.path.dirname(export_cypher_file), exist_ok=True)
        with open(export_cypher_file, "w", encoding="utf-8") as f:
            f.write("// ==========================================================\n")
            f.write("// KB_DIABET NEO4J KNOWLEDGE GRAPH INITIALIZATION SCRIPT (EXPANDED)\n")
            f.write("// Toàn diện 143 Nodes, 280+ Relationships chuẩn hóa\n")
            f.write("// Tích hợp: QĐ 5481/QĐ-BYT, Vinmec Clinical, NIN, ADA 2024 & FPT Long Châu\n")
            f.write("// ==========================================================\n\n")
            for stmt in node_statements:
                f.write(stmt.strip() + "\n")
            f.write("\n// RELATIONSHIPS\n\n")
            for stmt in rel_statements:
                f.write(stmt.strip() + "\n")

        print(f"✓ Đã xuất tệp Cypher hoàn chỉnh: {export_cypher_file}")

        stats = self.get_graph_stats()
        print(f"✓ Đã nạp thành công vào Neo4j Database: {stats['nodes']} Nodes, {stats['relationships']} Relationships, {len(stats['labels'])} Labels.")
        return True

    def get_graph_stats(self) -> Dict[str, Any]:
        """Truy vấn thống kê tổng số Node và Relationship trong Neo4j."""
        if not self.is_connected():
            return {"nodes": 0, "relationships": 0, "connected": False}
        with self.driver.session() as session:
            n_res = session.run("MATCH (n) RETURN count(n) AS node_count").single()
            r_res = session.run("MATCH ()-[r]->() RETURN count(r) AS rel_count").single()
            labels_res = session.run("CALL db.labels() YIELD label RETURN collect(label) AS labels").single()
            return {
                "nodes": n_res["node_count"] if n_res else 0,
                "relationships": r_res["rel_count"] if r_res else 0,
                "labels": labels_res["labels"] if labels_res else [],
                "connected": True,
                "browser_url": "http://localhost:7474"
            }

    def query_safety_contraindications(self, drug_name: str, has_alcohol: bool = False, egfr_value: Optional[float] = None) -> List[Dict[str, Any]]:
        """Truy vấn Cypher kiểm tra chống chỉ định y tế và tương tác thuốc từ Neo4j."""
        if not self.is_connected():
            return []
            
        alerts = []
        # 1. Kiểm tra tương tác với cồn
        if has_alcohol and "METFORMIN" in drug_name.upper():
            cypher = """
            MATCH (dr:Drug)-[r:RISK_OF]->(a:AdverseEffect)
            WHERE dr.id = 'METFORMIN' AND a.id = 'LACTIC_ACIDOSIS'
            RETURN dr.name AS drug, a.name AS adverse, r.trigger AS trigger, r.severity AS severity, a.mortality AS mortality
            """
            rows = self.execute_cypher(cypher)
            for row in rows:
                alerts.append({
                    "level": "FATAL",
                    "title": "CẢNH BÁO ĐỎ TƯƠNG TÁC CỒN - METFORMIN TỬ VONG",
                    "message": f"Theo phác đồ Bộ Y Tế, {row['drug']} kết hợp {row['trigger']} gây nguy cơ {row['adverse']} (Tỷ lệ tử vong {row['mortality']}). CẤM TUYỆT ĐỐI RƯỢU BIA."
                })

        # 2. Kiểm tra chống chỉ định suy thận theo eGFR
        if egfr_value is not None and "METFORMIN" in drug_name.upper():
            if egfr_value < 30:
                cypher_renal = """
                MATCH (dr:Drug {id: 'METFORMIN'})-[r:CONTRAINDICATED_IN]->(c:Complication {id: 'CKD'})
                RETURN dr.name AS drug, c.name AS complication, r.condition AS condition, r.severity AS severity
                """
                rows = self.execute_cypher(cypher_renal)
                alerts.append({
                    "level": "FATAL",
                    "title": "CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI METFORMIN (eGFR < 30 mL/phút)",
                    "message": f"Chức năng thận eGFR = {egfr_value} mL/phút/1.73m2. Chống chỉ định tuyệt đối Metformin theo QĐ 5481/QĐ-BYT để tránh ngộ độc thận."
                })
            elif 30 <= egfr_value < 45:
                alerts.append({
                    "level": "WARNING",
                    "title": "THẬN TRỌNG SUY GIẢM CHỨC NĂNG THẬN (30 <= eGFR < 45)",
                    "message": f"Chức năng thận eGFR = {egfr_value} mL/phút/1.73m2. Cần giảm 50% liều Metformin (tối đa không quá 1000 mg/ngày) theo QĐ 5481."
                })

        return alerts

    def query_food_swaps(self, food_keyword: str) -> List[Dict[str, Any]]:
        """Truy vấn Cypher đề xuất thay thế thực phẩm lành mạnh dựa trên chỉ số GI."""
        if not self.is_connected():
            return []
        cypher = """
        MATCH (f1:Food)-[r:CAN_BE_REPLACED_BY]->(f2:Food)
        WHERE toLower(f1.name) CONTAINS toLower($keyword) OR toLower(f1.id) CONTAINS toLower($keyword)
        RETURN f1.name AS original, f1.gi AS original_gi, f2.name AS replacement, f2.gi AS replacement_gi, r.reason AS rationale
        """
        return self.execute_cypher(cypher, {"keyword": food_keyword})

# Khởi tạo instance singleton để tái sử dụng toàn hệ thống
neo4j_service = Neo4jKGService()

if __name__ == '__main__':
    service = Neo4jKGService()
    if service.is_connected():
        service.populate_from_kb()
        stats = service.get_graph_stats()
        print("\n--- NEO4J GRAPH STATS ---")
        print("Nodes count:", stats["nodes"])
        print("Relationships count:", stats["relationships"])
        print("Entity Labels:", stats["labels"])
