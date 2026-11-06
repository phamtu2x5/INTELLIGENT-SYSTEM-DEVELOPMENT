# TÀI LIỆU KỸ THUẬT: CƠ SỞ TRI THỨC & CƠ SỞ DỮ LIỆU ĐỒ THỊ NEO4J
## (KNOWLEDGE BASE & NEO4J GRAPH DATABASE SPECIFICATION)
### Hệ Thống Multi-Agent Tư Vấn Đái Tháo Đường (DiaAgent-MAS)

---

## 1. Tổng Quan Kiến Trúc (Architecture Overview)

Hệ thống DiaAgent-MAS sử dụng kiến trúc dữ liệu kép (Dual-Path Data Architecture) kết hợp giữa:
1. **Nhánh Học máy/Học sâu (Tabular Clinical Database):** Xử lý dữ liệu dạng bảng từ 100.000 hồ sơ bệnh nhân phục vụ huấn luyện các mô hình dự đoán nguy cơ (LightGBM, XGBoost, CatBoost, Deep MLP).
2. **Nhánh Đồ thị Tri thức Y khoa (Neo4j Knowledge Graph & GraphRAG):** Số hóa tri thức chuyên gia từ văn bản hướng dẫn y tế thành mạng lưới đồ thị gồm **143 Node thực thể** và **271 Mối quan hệ liên kết**, đóng vai trò là "chân lý mặt đất" (Ground Truth) để rà soát chống chỉ định dược lý, phác đồ điều trị, thực đơn dinh dưỡng và định vị sản phẩm nhà thuốc.

```
                                    +-------------------------------------------------------------+
                                    |                NGUỒN DỮ LIỆU THÔ ĐA DẠNG                    |
                                    |  • QĐ 5481/QĐ-BYT Bộ Y Tế (PDF 77 trang)                     |
                                    |  • Chuyên đề lâm sàng Bệnh viện Vinmec                      |
                                    |  • Bảng thành phần thực phẩm Viện Dinh Dưỡng NIN            |
                                    |  • Khuyến cáo Hiệp hội ĐTĐ Hoa Kỳ ADA 2024                 |
                                    |  • Danh mục 30 sản phẩm Nhà thuốc FPT Long Châu             |
                                    +------------------------------+------------------------------+
                                                                   |
                                              [Tiền xử lý & Trích xuất Bộ ba Tri thức]
                                                                   |
                                                                   v
                                    +-------------------------------------------------------------+
                                    |               CƠ SỞ DỮ LIỆU ĐỒ THỊ NEO4J                    |
                                    |       (143 Nodes | 271 Relationships | 12 Labels)           |
                                    |       bolt://localhost:7687 | kb_diabet_init.cypher         |
                                    +------------------------------+------------------------------+
                                                                   |
                                                      [GraphRAG & Cypher Engine]
                                                                   |
                                                                   v
                                    +-------------------------------------------------------------+
                                    |                HỆ THỐNG ĐIỀU PHỐI MULTI-AGENT               |
                                    |  1. TriageInterviewerAgent   (Phân loại ca bệnh)            |
                                    |  2. RiskPredictionAgent      (Học máy LightGBM 97.97%)     |
                                    |  3. EndocrinologistAgent     (Phác đồ chuẩn Bộ Y Tế)        |
                                    |  4. NutritionAgent           (Đĩa ăn NIN & Đổi món GI)      |
                                    |  5. LifestyleCoachAgent      (Phác đồ FITT & Chăm sóc chân) |
                                    |  6. PharmacyLocatorAgent     (Sản phẩm FPT Long Châu)       |
                                    |  7. SafetyGuardianAgent      (Rà soát an toàn đồ thị VETO)  |
                                    +-------------------------------------------------------------+
```

---

## 2. Các Nguồn Dữ Liệu Số Hóa Cốt Lõi (Primary Data Sources)

Toàn bộ tri thức trong đồ thị được chuẩn hóa từ 5 nguồn dữ liệu y tế và thương mại:

| STT | Tên Nguồn Dữ Liệu | Loại Dữ Liệu | Nội Dung Đóng Góp Cho Knowledge Graph |
| :---: | :--- | :--- | :--- |
| **1** | **Quyết định 5481/QĐ-BYT (30/12/2020)** | Văn bản pháp lý PDF (77 trang) | Tiêu chuẩn vàng khẳng định chẩn đoán (HbA1c ≥ 6.5%, Glucose đói FPG ≥ 126 mg/dL); phác đồ dùng thuốc bậc 1, bậc 2; quy định giảm liều/ngừng Metformin theo chức năng thận eGFR; quy tắc cấp cứu 15-15 hạ đường huyết. |
| **2** | **Bệnh viện Đa khoa Quốc tế Vinmec** | Tài liệu lâm sàng Web/HTML | Bộ triệu chứng nhận biết sớm (hội chứng 4 nhiều, nhìn mờ, khô miệng); cơ chế bệnh sinh biến chứng loét bàn chân đái tháo đường; quy trình chăm sóc và kiểm tra bàn chân hằng ngày. |
| **3** | **Viện Dinh Dưỡng Quốc Gia (NIN)** | Bảng dinh dưỡng thực phẩm | Chỉ số đường huyết (GI) và tải lượng đường (GL) của 29 món ăn Việt Nam; 15 cặp quy tắc chuyển đổi thực phẩm lành mạnh (Cơm trắng → Gạo lứt/Khoai lang); mô hình đĩa thức ăn chuẩn (1/2 rau, 1/4 đạm, 1/4 tinh bột). |
| **4** | **Hiệp hội Đái tháo đường Hoa Kỳ (ADA 2024)** | Hướng dẫn điều trị quốc tế | Phác đồ bảo vệ tim thận ưu tiên nhóm thuốc SGLT-2i và GLP-1 RA dựa trên thử nghiệm lâm sàng DAPA-CKD, EMPA-REG, SUSTAIN-6; cảnh báo toan ceton đường huyết bình thường (Euglycemic DKA). |
| **5** | **Nhà thuốc FPT Long Châu** | Danh mục thương mại JSON | 30 sản phẩm thương mại thật gồm thuốc viên, bút tiêm insulin, máy đo đường huyết Accu-Chek, que thử và sữa y học Glucerna kèm đơn giá niêm yết VNĐ và tình trạng đơn thuốc (Rx). |

---

## 3. Quy Trình 6 Bước Chuẩn Bị Dữ Liệu Thành Database

### Bước 1: Thu thập Dữ liệu Đa nguồn (Data Ingestion)
- Tải tệp PDF chính thức từ Cổng thông tin Bộ Y Tế lưu tại: `Diabetes_MultiAgent_System/data/guidelines/QD_5481_BYT_Dai_Thao_Duong_Tip_2.pdf`.
- Thu thập dữ liệu thực đơn từ Bảng thành phần thực phẩm Việt Nam của Viện Dinh Dưỡng NIN.
- Thu thập danh mục 30 sản phẩm từ Nhà thuốc FPT Long Châu qua bộ công cụ `crawl_longchau_diabetes.py`.
- Thu thập tập dữ liệu 100.000 hồ sơ bệnh nhân lâm sàng từ Kaggle phục vụ nhánh học máy.

### Bước 2: Tiền xử lý & Lưu trữ Database Chuyên biệt
- **Dữ liệu bảng (Tabular DB cho ML/DL):** Xử lý giá trị khuyết, chuẩn hóa thang đo bằng `StandardScaler`, mã hóa One-Hot và cân bằng mẫu bằng `SMOTE` để huấn luyện LightGBM đạt ROC-AUC 0.9797.
- **Dữ liệu văn bản (Document Store cho Vector RAG):** Sử dụng `pypdf` cắt tài liệu thành các đoạn văn bản (Text Chunks) 500-800 từ có overlap 100 từ phục vụ truy xuất ngữ nghĩa BM25/Vector RAG.

### Bước 3: Thiết kế Lược đồ Đồ thị (Ontology & Schema Design)
- Thiết lập 12 Nhãn Thực thể (`:Disease`, `:Symptom`, `:Biomarker`, `:Complication`, `:Comorbidity`, `:RiskFactor`, `:Drug`, `:Food`, `:PharmacyProduct`, `:ClinicalProtocol`, `:Source`, `:AdverseEffect`).
- Thiết lập 17 Loại Quan hệ (`[:HAS_SYMPTOM]`, `[:DIAGNOSED_BY]`, `[:CAUSES_COMPLICATION]`, `[:AGGRAVATES]`, `[:TREATS]`, `[:HIGHLY_RECOMMENDED_FOR]`, `[:CONTRAINDICATED_IN]`, `[:CAUTION_IN]`, `[:RISK_OF]`, `[:MONITORED_BY]`, `[:CAN_BE_REPLACED_BY]`, `[:DISPENSED_AS_PRODUCT]`, v.v.).
- Khởi tạo ràng buộc duy nhất (Unique Constraints) trên thuộc tính `id` trên Neo4j.

### Bước 4: Trích xuất Bộ ba Tri thức (Triplet Mapping)
- Chuyển đổi toàn bộ tri thức y khoa thành cấu trúc: `Subject -[Predicate {Properties}]-> Object`.
- Ví dụ:
  * `(:Drug {id: 'METFORMIN'}) -[:RISK_OF {trigger: 'Uống rượu bia', severity: 'FATAL'}]-> (:AdverseEffect {id: 'LACTIC_ACIDOSIS'})`
  * `(:Drug {id: 'METFORMIN'}) -[:CONTRAINDICATED_IN {condition: 'eGFR < 30', severity: 'ABSOLUTE'}]-> (:Complication {id: 'CKD'})`
  * `(:Food {id: 'FOOD_COM_TRANG'}) -[:CAN_BE_REPLACED_BY {reason: 'GI thấp hơn 28 đơn vị'}]-> (:Food {id: 'FOOD_COM_GAO_LUC'})`

### Bước 5: Nạp Tự động vào CSDL Neo4j & Xuất Tệp .cypher
- Mã nguồn Python `neo4j_kg_service.py` mở phiên kết nối Bolt tới `bolt://localhost:7687`.
- Nạp lần lượt 143 Node bằng câu lệnh `MERGE` và 271 Relationship bằng câu lệnh `MATCH ... MERGE`.
- Tự động xuất toàn bộ kịch bản ra tệp `Diabetes_MultiAgent_System/data/knowledge_graph/kb_diabet_init.cypher` (994 dòng Cypher).

### Bước 6: Tích hợp Đường ống GraphRAG vào Hệ thống Multi-Agent
- Khi bệnh nhân nhập thông tin, hệ thống sinh truy vấn Cypher thời gian thực để rà soát chống chỉ định.
- `SafetyGuardianAgent` đối chiếu phác đồ với đồ thị tri thức để kích hoạt quyền VETO (phủ quyết) và yêu cầu vòng lặp phản biện (Reflection Loop) sửa đổi nếu phát hiện rủi ro.

---

## 4. Thống Kê Chi Tiết Cấu Trúc Đồ Thị (Graph Metrics)

### 4.1. Phân bố 143 Node Thực Thể theo 12 Nhãn (Labels)

| Nhãn Thực Thể | Số Lượng | Mô Tả & Đại Diện Tiêu Biểu |
| :--- | :---: | :--- |
| **PharmacyProduct** | 30 | Sản phẩm FPT Long Châu: Glucophage XR (500/750/1000mg), Diamicron MR (30/60mg), Amaryl 2mg, Forxiga 10mg, Jardiance (10/25mg), Januvia (50/100mg), Galvus Met, Trajenta, Lantus SoloStar, Toujeo, NovoRapid, Mixtard 30, Máy đo Accu-Chek Guide/Instant, Que thử 50q, Kim lấy máu Softclix, Sữa Glucerna 850g và chai 220ml. |
| **Food** | 29 | Món ăn Việt Nam: 13 món High GI (Cơm trắng GI 83, Xôi nếp GI 90, Bánh mì trắng GI 85, Phở bò nước béo GI 72, Bún bò Huế, Bánh cuốn, Bánh mì thịt, Trà sữa GI 88, Nước ngọt GI 95, Chè ngọt, Dưa hấu, Cháo lòng) và 16 món Low GI chuẩn NIN (Cơm gạo lứt GI 55, Khoai lang luộc GI 48, Bún mọc nhiều rau GI 50, Bánh mì đen GI 48, Yến mạch GI 52, Bông cải xanh, Rau muống, Đậu bắp, Khổ qua xào trứng, Cá hấp, Ức gà, Bưởi, Táo xanh, Trà xanh). |
| **Drug** | 18 | Dược chất hạ đường huyết: Metformin, Gliclazide, Glimepiride, Glibenclamide, Dapagliflozin, Empagliflozin, Canagliflozin, Sitagliptin, Vildagliptin, Linagliptin, Saxagliptin, Semaglutide, Liraglutide, Dulaglutide, Pioglitazone, Acarbose, Insulin Glargine, Insulin Aspart. |
| **Biomarker** | 14 | Chỉ số sinh học: HbA1c, Glucose đói (FPG), Nghiệm pháp 2h (OGTT), Glucose bất kỳ (RPG), Độ lọc cầu thận (eGFR), Creatinine, Tỷ số Albumin/Creatinine niệu (UACR), BMI, Vòng eo, Huyết áp tâm thu/trương, LDL-C, HDL-C, Triglyceride. |
| **AdverseEffect** | 12 | Tác dụng phụ & Cảnh báo: Nhiễm toan Lactic (tử vong 50%), Hạ đường huyết nhẹ/nặng, Toan ceton DKA, Toan ceton Euglycemic DKA của SGLT2i, Tăng áp lực thẩm thấu HHS, Nhiễm khuẩn tiết niệu UTI, Rối loạn tiêu hóa, Phù ngoại biên, Hoại thư Fournier, Viêm tụy cấp. |
| **Symptom** | 10 | Triệu chứng lâm sàng: Hội chứng 4 nhiều (Tiểu nhiều, Khát nhiều, Ăn nhiều mau đói, Sụt cân); Mệt mỏi, Nhìn mờ tạm thời, Tê bì châm chích bàn chân, Vết thương chậm lành, Khô miệng, Nhiễm nấm tái phát. |
| **Complication** | 8 | Biến chứng mạn tính: Thận mạn (CKD), Tim mạch xơ vữa (ASCVD), Suy tim (Heart Failure), Bệnh võng mạc, Bệnh thần kinh ngoại biên, Loét bàn chân đái tháo đường, Động mạch ngoại biên (PAD), Liệt dạ dày. |
| **Disease** | 5 | Bệnh lý: ĐTĐ Type 2 (E11), Tiền ĐTĐ (R73.0), ĐTĐ Type 1 (E10), ĐTĐ thai kỳ (O24.4), Hội chứng chuyển hóa (E88.81). |
| **ClinicalProtocol** | 5 | Phác đồ lâm sàng: Phác đồ FITT (150 phút/tuần), Quy tắc cấp cứu 15-15, Quy trình chăm sóc bàn chân, Đĩa thức ăn chuẩn NIN, Tự đo đường huyết tại nhà (SMBG). |
| **Source** | 5 | Nguồn tri thức: QĐ 5481/QĐ-BYT, Vinmec Clinical, Viện Dinh Dưỡng NIN, ADA 2024, FPT Long Châu. |
| **RiskFactor** | 4 | Yếu tố nguy cơ: Béo phì chuẩn Châu Á (BMI ≥ 23), Tiền sử gia đình, Hút thuốc lá, Lối sống tĩnh tại. |
| **Comorbidity** | 3 | Bệnh đồng mắc: Tăng huyết áp (I10), Rối loạn mỡ máu (E78), Gan nhiễm mỡ (MASLD/NAFLD). |

---

### 4.2. Phân bố 271 Mối Quan Hệ Liên Kết (Relationships)

- `CITED_FROM` (100): Trích dẫn xuất xứ từng thực thể từ 5 nguồn tài liệu chính thống.
- `DISPENSED_AS_PRODUCT` (21): Nối hoạt chất thuốc sang sản phẩm thương mại Long Châu kèm đơn giá.
- `TREATS` (20): Chỉ định điều trị bệnh theo bậc 1, bậc 2 của Bộ Y Tế.
- `RISK_OF` (20): Cảnh báo tác dụng phụ nguy hiểm (toan lactic, hạ đường huyết, toan ceton).
- `DIAGNOSED_BY` (16): Ngưỡng chỉ số sinh học chẩn đoán bệnh lý và biến chứng.
- `HAS_SYMPTOM` (15): Nối bệnh lý với triệu chứng lâm sàng tương ứng.
- `CAN_BE_REPLACED_BY` (15): Đề xuất chuyển đổi món ăn GI cao sang thực phẩm lành mạnh chuẩn NIN.
- `MONITORED_BY` (14): Chỉ số xét nghiệm bắt buộc kiểm tra định kỳ khi dùng thuốc.
- `HIGHLY_RECOMMENDED_FOR` (10): Khuyến cáo bảo vệ tim thận của SGLT-2i và GLP-1 RA.
- `CAUSES_COMPLICATION` (8): Cơ chế tiến triển từ đái tháo đường sang biến chứng đa cơ quan.
- `AGGRAVATES` (8): Tác động hiệp đồng làm nặng thêm bệnh từ tăng huyết áp, mỡ máu, béo phì.
- `RECOMMENDED_DEVICE_FOR` (6): Máy đo đường huyết và que thử phù hợp tình trạng bệnh.
- `CONTRAINDICATED_IN` (5): Chống chỉ định tuyệt đối (Metformin khi eGFR < 30, TZD khi suy tim).
- `RECOMMENDED_LIFESTYLE` (5): Phác đồ tập luyện FITT và đĩa ăn chuẩn NIN.
- `CAUTION_IN` (4): Hướng dẫn giảm 50% liều dùng khi suy giảm chức năng thận.
- `TREATED_BY_PROTOCOL` (2): Quy trình cấp cứu hạ đường huyết và chăm sóc bàn chân.
- `NUTRITIONAL_SUPPORT_FOR` (2): Dinh dưỡng y học hỗ trợ ổn định đường huyết (Glucerna).

---

## 5. Hướng Dẫn Vận Hành & Khám Phá CSDL Neo4j

### 5.1. Khởi động CSDL Neo4j bằng Docker
```bash
docker run -d \
  --name neo4j-diabetes \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password123 \
  neo4j:5-community
```

### 5.2. Nạp hoặc Tái tạo Dữ liệu Đồ thị bằng Python
```bash
python3 Diabetes_MultiAgent_System/src/knowledge/neo4j_kg_service.py
```

### 5.3. Nhập thủ công bằng tệp Cypher Script
Mở giao diện web **http://localhost:7474**, mở tệp `Diabetes_MultiAgent_System/data/knowledge_graph/kb_diabet_init.cypher`, sao chép toàn bộ nội dung và dán vào thanh lệnh Cypher để nạp trực tiếp.

### 5.4. Các câu lệnh Cypher khám phá hữu ích (Tránh giới hạn LIMIT 25)

**1. Xem TOÀN BỘ 143 Node và 271 Liên kết trên cùng màn hình:**
```cypher
MATCH (n)-[r]->(m) RETURN n, r, m
```

**2. Khám phá cụm Thuốc và Sản phẩm Long Châu kèm đơn giá:**
```cypher
MATCH (dr:Drug)-[r:DISPENSED_AS_PRODUCT]->(p:PharmacyProduct)
RETURN dr, r, p
```

**3. Tra cứu toàn bộ Quy tắc Chống chỉ định & Cảnh báo an toàn dược lý:**
```cypher
MATCH (dr:Drug)-[r:CONTRAINDICATED_IN|RISK_OF]->(target)
RETURN dr, r, target
```

**4. Tra cứu Bệnh lý, Triệu chứng và Ngưỡng chỉ số xét nghiệm chẩn đoán:**
```cypher
MATCH (d:Disease)-[r:HAS_SYMPTOM|DIAGNOSED_BY]->(target)
RETURN d, r, target
```

**5. Tra cứu các cặp Chuyển đổi Thực phẩm lành mạnh theo Viện Dinh Dưỡng NIN:**
```cypher
MATCH (f1:Food)-[r:CAN_BE_REPLACED_BY]->(f2:Food)
RETURN f1, r, f2
```

---

## 6. Sơ Đồ Không Gian Nhúng 2D (Node & Link Embeddings)

Toàn bộ đồ thị tri thức được chiếu vào không gian tiềm ẩn 2 chiều thông qua thuật toán bố trí lực lò xo Force-Directed Graph Layout kết hợp vector tiên nghiệm phân cụm ngữ nghĩa (Semantic Clustering Priors).

- **Tệp ảnh chất lượng cao 300 DPI:** `Diabetes_MultiAgent_System/data/knowledge_graph_node_embeddings.png` (Dung lượng: 4.79 MB).
- **Đặc điểm không gian:**
  * Các thực thể cùng vai trò chuyên môn tự động co cụm chặt chẽ (Cụm Dược chất Bộ Y Tế, Cụm 30 Biệt dược & Thiết bị Long Châu, Cụm 14 Xét nghiệm sinh học, Cụm 10 Triệu chứng lâm sàng Vinmec, Cụm 29 Món ăn NIN, Cụm 12 Cảnh báo an toàn).
  * Các mũi tên định hướng phản ánh toàn vẹn tô-pô phác đồ lâm sàng và cơ chế phản biện an toàn y khoa của hệ thống DiaAgent-MAS.
