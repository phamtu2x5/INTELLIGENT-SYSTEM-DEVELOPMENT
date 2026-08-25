# 🏠 House Price Prediction — Vietnam Housing Dataset 2024

Hệ thống học máy thông minh (Intelligent System) dự đoán giá bất động sản tại Việt Nam từ Vietnam Housing Dataset 2024, tích hợp giao diện Web tương tác đa mô hình.

---

## 🌟 Tính năng nổi bật

- **Huấn luyện & Đánh giá 5 mô hình hồi quy:**
  1. `XGBoost Regressor (Tuned)` 🏆
  2. `Random Forest Regressor` 🌲
  3. `Gradient Boosting Regressor` ⚡
  4. `Linear Regression (Baseline)` 📐
  5. `Decision Tree Regressor` 🌿
- **5 độ đo chuẩn hóa:** MAE, MSE, RMSE, R², MAPE.
- **Pipeline chống rò rỉ dữ liệu:** `ColumnTransformer` (SimpleImputer median/constant + StandardScaler + OneHotEncoder).
- **Giao diện Web tương tác (FastAPI + Glassmorphism UI):**
  - Hỗ trợ **5 mẫu nhà thực tế (Quick Presets)** để tự động điền form chỉ với 1 click.
  - Tùy chọn chuyển đổi mô hình dự đoán tức thì hoặc **so sánh song song 5 mô hình**.
  - Hiển thị giá dự đoán (tỷ VND) và đơn giá (triệu VNĐ/m²).

---

## 📂 Cấu trúc thư mục

```
house_price_prediction/
├── app.py                              # FastAPI Web Server
├── export_models.py                    # Script huấn luyện & xuất 5 mô hình
├── requirements.txt                    # Danh sách thư viện cần thiết
├── README.md                           # Tài liệu hướng dẫn
│
├── data/
│   └── vietnam_housing_dataset.csv     # Dataset gốc Kaggle (~30,230 dòng)
│
├── notebooks/
│   └── 01_house_price_analysis.ipynb   # Jupyter Notebook chuẩn 19 mục
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
│   ├── full_pipeline.joblib            # Pipeline mô hình tốt nhất (XGBoost)
│   └── best_model.joblib               # Mô hình tốt nhất độc lập
│
└── reports/
    ├── figures/                        # Các biểu đồ trực quan hóa
    │   ├── price_distribution.png
    │   ├── area_distribution.png
    │   ├── bedroom_distribution.png
    │   ├── model_comparison.png
    │   ├── feature_importance.png
    │   └── actual_vs_predicted.png
    ├── model_results.csv               # Bảng so sánh 5 mô hình
    └── evaluation_summary.md           # Báo cáo tổng kết
```

---

## 🚀 Hướng dẫn cài đặt & Khởi chạy

### 1. Cài đặt môi trường
```bash
pip install -r requirements.txt
```

### 2. Xuất toàn bộ 5 mô hình (nếu chưa có trong `models/`)
```bash
python export_models.py
```

### 3. Khởi chạy Giao diện Web
```bash
python app.py
# hoặc
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```
👉 Truy cập trình duyệt tại: **`http://127.0.0.1:8000`**

### 4. Chạy Jupyter Notebook (19 mục phân tích chuyên sâu)
```bash
cd notebooks
jupyter notebook 01_house_price_analysis.ipynb
```

---

## 📊 Kết quả so sánh 5 mô hình

| Mô hình | MAE (tỷ) ↓ | RMSE (tỷ) ↓ | R² ↑ | MAPE (%) ↓ |
| :--- | :---: | :---: | :---: | :---: |
| **XGBoost (Tuned)** 🏆 | **1.0206** | **1.3166** | **0.6329** | **21.89%** |
| **Linear Regression** | 1.0077 | 1.3190 | 0.6315 | 21.07% |
| **Random Forest** | 1.0786 | 1.3972 | 0.5865 | 23.09% |
| **Gradient Boosting** | 1.1553 | 1.4547 | 0.5518 | 25.74% |
| **Decision Tree** | 1.1548 | 1.5121 | 0.5157 | 24.90% |
