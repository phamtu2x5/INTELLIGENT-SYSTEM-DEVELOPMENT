# HỆ MULTI-AGENT CHẨN ĐOÁN, DỰ ĐOÁN & TƯ VẤN ĐÁI THÁO ĐƯỜNG (DiaAgent-MAS)

Dự án nghiên cứu và phát triển Hệ Multi-Agent y tế thông minh tích hợp **Mô hình Học máy/Học sâu (ML/DL)**, **Đồ thị Tri thức Dược lý Bộ Y Tế (Knowledge Graph)**, **Truy hồi tăng cường sinh (RAG)**, **Mô hình Ngôn ngữ Lớn (Google Gemini API)** và **Dữ liệu Dược phẩm FPT Long Châu**.

---

## 1. Cấu Trúc Dự Án (Project Structure)

```
Diabetes_MultiAgent_System/
├── .env                                  # Khóa Google AI Studio API Key & cấu hình mô hình
├── README.md                             # Tài liệu kỹ thuật dự án
├── requirements.txt                      # Danh sách các gói phụ thuộc Python
├── docs/                                 # Tài liệu kỹ thuật chuyên sâu
│   └── KNOWLEDGE_BASE_GRAPH.md           # Hồ sơ đặc tả 143 Nodes & 271 Relationships Neo4j
├── data/                                 # Dữ liệu phục vụ huấn luyện, lâm sàng và dược phẩm
│   ├── diabetes_prediction_dataset.csv   # Tập dữ liệu lớn (100.000 mẫu) huấn luyện ML/DL
│   ├── diabetes_clinical_records_vn.csv  # 1.000 bệnh án thực tế tại Việt Nam (kèm thuốc & ICD-10)
│   └── pharmacy/                         # Dữ liệu thương mại dược phẩm & thiết bị y tế
│       ├── longchau_diabetes_products.json # Danh mục sản phẩm Long Châu (giá VNĐ, phân loại Rx, URL)
│       └── crawl_longchau_diabetes.py     # Script crawler & tìm kiếm/báo giá Long Châu
├── notebooks/                            # Jupyter Notebooks thực nghiệm độc lập
│   └── 01_diabetes_model_training_and_optimization.ipynb
│                                         # Notebook huấn luyện 5 mô hình (Logistic, RF, LightGBM,
│                                         # PyTorch MLP, PyTorch 1D-CNN) có đầy đủ log từng epoch và SHAP
├── models/                               # Checkpoint mô hình & artifacts sau huấn luyện
│   ├── best_diabetes_lgb_model.pkl       # Mô hình LightGBM tối ưu ROC-AUC (0.9797)
│   ├── best_mlp_weights.pth              # Checkpoint PyTorch Deep MLP (Recall 93.32%)
│   ├── best_cnn_weights.pth              # Checkpoint PyTorch Tabular 1D-CNN (ROC-AUC 0.9748)
│   ├── scaler.pkl                        # StandardScaler đã fit trên tập Train (13 features)
│   ├── feature_names.json                # Danh sách 13 đặc trưng đầu vào
│   └── model_metadata.json               # Báo cáo đánh giá chi tiết
└── src/                                  # Mã nguồn hệ thống Multi-Agent
    ├── app.py                            # Giao diện Web Dashboard tương tác (Streamlit)
    ├── orchestrator.py                   # Bộ điều phối Đa Agent trung tâm (Cyclic Reflection Loop)
    ├── core/                             # Hạ tầng lõi
    │   ├── gemini_client.py              # Client Google AI Studio (gemini-3.1-flash-lite)
    │   └── state_schema.py               # Pydantic State Schema chia sẻ giữa các Agent
    ├── knowledge/                        # Tri thức chuyên gia Y tế & Dinh dưỡng
    │   ├── diabetes_kg.py                # Đồ thị Tri thức (NetworkX) rà soát chống chỉ định dược lý
    │   └── vietnamese_guidelines_rag.py  # BM25 RAG truy xuất hướng dẫn QĐ 5481/QĐ-BYT & NIN
    └── agents/                           # 7 Agents chuyên trách phối hợp
        ├── triage_interviewer_agent.py   # Phỏng vấn tiếp đón & trích xuất thực thể (NER)
        ├── risk_prediction_agent.py      # Suy luận mô hình Machine Learning & giải thích SHAP
        ├── endocrinologist_agent.py      # Bác sĩ Nội tiết chẩn đoán & ra phác đồ theo Bộ Y Tế
        ├── nutrition_agent.py            # Chuyên gia Dinh dưỡng thiết kế bữa ăn Việt & chỉ số GI
        ├── lifestyle_coach_agent.py      # HLV Lối sống lập phác đồ FITT & chăm sóc bàn chân
        ├── pharmacy_locator_agent.py     # Định vị thuốc Long Châu, báo giá VNĐ & cảnh báo Rx
        └── safety_guardian_agent.py      # Giám sát an toàn y khoa có quyền VETO phản biện
```

---

## 2. Kết Quả Huấn Luyện & Đối Chuẩn Mô Hình (Đo trên 14.422 mẫu Test)

| Mô hình | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | Độ trễ suy luận |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. Logistic Regression** | 88.74% | 43.25% | 88.60% | 58.12% | 0.9639 | 0.8319 | 0.0001 ms |
| **2. Random Forest** | **92.50%** | **54.65%** | 87.74% | **67.35%** | 0.9769 | 0.8840 | 0.0037 ms |
| **3. LightGBM Boosting** | 90.45% | 47.85% | 92.53% | 63.08% | **0.9797** | **0.8916** | 0.0071 ms |
| **4. PyTorch Deep MLP** | 87.77% | 41.42% | **93.32%** | 57.37% | 0.9761 | 0.8786 | 0.0101 ms |
| **5. PyTorch 1D-CNN** | 89.88% | 46.23% | 90.57% | 61.21% | 0.9748 | 0.8704 | 0.1057 ms |

Mô hình **LightGBM Boosting** được tích hợp vào `RiskPredictionAgent` làm động cơ chính nhờ độ cân bằng tối ưu giữa **ROC-AUC (0.9797)**, **Recall (92.53%)**, độ trễ cực thấp (0.0071 ms) và khả năng trích xuất giải thích đặc trưng SHAP theo thời gian thực.

---

## 3. Quy Trình Điều Phối Đa Agent & Chu Trình Phản Biện (Reflection Loop)

```
[Bệnh nhân] 
    │
    ▼
[1. TriageInterviewerAgent]  ──► Trích xuất triệu chứng, tuổi, thói quen ăn uống, xét nghiệm
    │
    ▼
[2. RiskPredictionAgent]     ──► Suy luận LightGBM: Xác suất nguy cơ (%) + SHAP Importance
    │
    ▼
[3. EndocrinologistAgent]   ──► Chẩn đoán QĐ 5481/QĐ-BYT & Kê phác đồ thuốc ban đầu
    │
    ├──► [4. NutritionAgent]      ──► Đĩa thức ăn NIN, chỉ số GI món ăn Việt, giảm cơm trắng
    │
    ├──► [5. LifestyleCoachAgent] ──► Phác đồ FITT 150p/tuần, chăm sóc chân, Quy tắc 15-15
    │
    ▼
[6. PharmacyLocatorAgent]    ──► Ánh xạ hoạt chất sang thuốc FPT Long Châu, tính giá VNĐ/tháng
    │
    ▼
[7. SafetyGuardianAgent]     ──► Rà soát chống chỉ định (eGFR < 30, rượu bia, suy tim...)
    │
    ├── [PHÁT HIỆN VI PHẠM (VETO)] ──► KÍCH HOẠT VÒNG LẶP PHẢN BIỆN (REFLECTION LOOP)
    │                                  Yêu cầu EndocrinologistAgent đổi thuốc an toàn!
    └── [PHÊ DUYỆT (APPROVED)]    ──► TỔNG HỢP BÁO CÁO TOÀN DIỆN CHO BỆNH NHÂN
```

---

## 4. Hướng Dẫn Cài Đặt & Chạy Hệ Thống

### 4.1. Cài đặt môi trường
```bash
cd Diabetes_MultiAgent_System
pip install -r requirements.txt
```

### 4.2. Chạy thử nghiệm điều phối Orchestrator qua CLI
```bash
python3 src/orchestrator.py
```

### 4.3. Khởi chạy Giao diện Web Dashboard (Streamlit)
```bash
streamlit run src/app.py
```
Giao diện sẽ tự động mở tại `http://localhost:8501`, hỗ trợ chọn các kịch bản mẫu hoặc tùy biến hồ sơ bệnh nhân, hiển thị gauge đo nguy cơ, cây giải thích SHAP, thẻ thuốc Long Châu kèm link đặt hàng chính hãng và thực đơn món ăn Việt Nam.

---

## 5. Tài Liệu Kỹ Thuật Đồ Thị Tri Thức & Neo4j (Knowledge Graph Specification)

Chi tiết thiết kế cơ sở tri thức, lược đồ Ontology, danh mục 143 Node thực thể và 271 Mối quan hệ liên kết xem tại:
👉 **[Tài liệu Kỹ thuật Cơ sở Dữ liệu Đồ thị Neo4j (KNOWLEDGE_BASE_GRAPH.md)](docs/KNOWLEDGE_BASE_GRAPH.md)**

- **CSDL Đồ thị Trực tiếp:** Neo4j Community Server 5.x (`bolt://localhost:7687` | Web UI: `http://localhost:7474`)
- **Tệp Khởi tạo Cypher Độc lập:** `data/knowledge_graph/kb_diabet_init.cypher` (994 dòng lệnh)
- **Sơ đồ Vector Nhúng 2D (300 DPI):** `data/knowledge_graph_node_embeddings.png` (4.79 MB)
