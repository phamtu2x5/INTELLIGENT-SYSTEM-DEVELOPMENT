# 🩺 Diabetes Prediction Intelligent System — Week 1

Hệ thống học máy thông minh (Intelligent System) dự đoán nguy cơ mắc bệnh đái tháo đường từ Pima Indians Diabetes Dataset, tích hợp giao diện Web tương tác đa mô hình.

---

## 🌟 Tính năng nổi bật

- **Huấn luyện & Đánh giá 5 mô hình phân loại:**
  1. `XGBoost Classifier (Tuned)` 🏆
  2. `Random Forest Classifier` 🌲
  3. `Support Vector Machine (RBF Kernel)` 🎯
  4. `Logistic Regression (Baseline)` 📐
  5. `K-Nearest Neighbors (KNN)` 👥
- **5 độ đo phân loại chuẩn y khoa:** Accuracy, Precision, Recall (Sensitivity), F1-Score, ROC-AUC.
- **Xử lý đặc thù sinh học:** Chuyển đổi các giá trị 0 bất hợp lý (Glucose, BloodPressure, SkinThickness, Insulin, BMI) thành `NaN` và điền khuyết bằng trung vị (`median`).
- **Giao diện Web tương tác (FastAPI + Glassmorphism UI):**
  - Hỗ trợ **5 hồ sơ bệnh nhân mẫu (Quick Presets)** để tự động điền form chỉ với 1 click.
  - Tùy chọn chuyển đổi mô hình chẩn đoán tức thì hoặc **so sánh đồng thời cả 5 mô hình**.
  - Hiển thị xác suất mắc bệnh (Risk Probability %), phân loại kết luận và khuyến nghị lâm sàng.

---

## 📂 Cấu trúc thư mục

```
Week 1/
├── app.py                              # FastAPI Web Server (phục vụ Web UI + REST APIs)
├── export_models.py                    # Script huấn luyện & đóng gói 5 mô hình
├── requirements.txt                    # Danh sách thư viện đầy đủ
├── README.md                           # Tài liệu hướng dẫn
│
├── data/
│   └── diabetes.csv                    # Dataset Pima Indians Diabetes gốc
│
├── notebooks/
│   └── 01_diabetes_analysis.ipynb      # Jupyter Notebook chuẩn 22 MỤC theo Assignment 01
│
├── templates/
│   └── index.html                      # Giao diện Web HTML5
│
├── static/
│   ├── style.css                       # Giao diện Glassmorphism hiện đại
│   └── app.js                          # Client-side JavaScript
│
├── models/
│   ├── all_models.joblib               # 5 Pipelines mô hình đã đóng gói
│   └── full_pipeline.joblib            # Pipeline mô hình tốt nhất (XGBoost)
│
└── reports/
    ├── figures/                        # Các biểu đồ trực quan hóa
    │   ├── eda_distributions.png
    │   ├── correlation_heatmap.png
    │   ├── roc_curves.png
    │   ├── feature_importance.png
    │   └── confusion_matrix.png
    ├── model_results.csv               # Bảng so sánh 5 mô hình
    └── evaluation_summary.md           # Báo cáo tổng kết khoa học
```

---

## 🚀 Hướng dẫn cài đặt & Khởi chạy

### 1. Cài đặt môi trường
```bash
pip install -r requirements.txt
```

### 2. Xuất toàn bộ 5 mô hình (nếu cần huấn luyện lại)
```bash
python export_models.py
```

### 3. Khởi chạy Giao diện Web Chẩn đoán
```bash
python app.py
# hoặc
uvicorn app:app --host 127.0.0.1 --port 8080 --reload
```
👉 Truy cập trình duyệt tại: **`http://127.0.0.1:8080`**

### 4. Chạy Jupyter Notebook (22 mục phân tích chuyên sâu)
```bash
cd notebooks
jupyter notebook 01_diabetes_analysis.ipynb
```

---

## 📊 Kết quả so sánh 5 mô hình

| Mô hình | Accuracy (%) ↑ | Precision (%) ↑ | Recall (%) ↑ | F1-Score ↑ | ROC-AUC ↑ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **XGBoost (Tuned)** 🏆 | **74.68%** | **64.15%** | **62.96%** | **0.6355** | **0.8167** |
| **Random Forest** | 74.68% | 61.22% | 55.56% | 0.5979 | 0.8141 |
| **Logistic Regression (Baseline)** | 71.43% | 56.00% | 51.85% | 0.5600 | 0.8144 |
| **Support Vector Machine (RBF)** | 73.38% | 58.33% | 51.85% | 0.5773 | 0.7974 |
| **K-Nearest Neighbors (k=9)** | 74.03% | 60.00% | 61.11% | 0.6226 | 0.7959 |
