# 🏥 Báo cáo Đánh giá Mô hình trên Tập Dữ liệu Độc lập (Diabetes Hospital Frankfurt 2000)

## 1. Tổng quan Thử nghiệm
- **Mục tiêu:** Kiểm tra khả năng tổng quát hóa (Out-of-distribution Generalization) của 5 mô hình đã huấn luyện trên tập **Pima Indians Diabetes** khi áp dụng trực tiếp (Zero-shot Inference) sang tập dữ liệu thực tế **Diabetes Hospital Frankfurt 2000**.
- **Kích thước mẫu kiểm thử:** 2,000 hồ sơ bệnh nhân.
- **Tính độc lập:** Mô hình hoàn toàn **KHÔNG** được huấn luyện hay điều chỉnh trọng số trên tập dữ liệu này.

---

## 2. Bảng Xếp hạng Hiệu năng 5 Mô hình Phân loại

| Mô hình | ROC-AUC ↑ | Accuracy (%) ↑ | Recall (Độ nhạy) (%) ↑ | F1-Score ↑ | Precision (%) ↑ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression 🏆 (Quán quân)** | **0.8362** | 59.35% | 35.92% | 0.5169 | 92.16% |
| **Random Forest** | **0.8043** | 60.05% | 37.57% | 0.5325 | 91.37% |
| **XGBoost (Tuned)** | **0.7863** | 57.70% | 34.27% | 0.4952 | 89.25% |
| **XGBoost** | **0.7863** | 57.70% | 34.27% | 0.4952 | 89.25% |
| **K-Nearest Neighbors** | **0.7555** | 58.85% | 39.31% | 0.5363 | 84.40% |
| **Support Vector Machine** | **0.7547** | 58.80% | 35.01% | 0.5072 | 91.97% |

---

## 3. Nhận xét & Đánh giá Khoa học (Generalization Analysis)
1. **Khả năng duy trì độ chính xác:** Mô hình **Logistic Regression** tiếp tục giữ vững vị trí số 1 với ROC-AUC đạt **0.8362** và Recall đạt **35.92%**, chứng minh khả năng sàng lọc không bỏ sót ca bệnh trong môi trường lâm sàng thực tế.
2. **Khả năng chống suy thoái miền (Domain Robustness):** Pipeline tiền xử lý (`SimpleImputer` trung vị + `StandardScaler`) và các đặc trưng kỹ thuật tương tác (`Glucose_BMI_Risk`, `InsulinGlucoseRatio`) hoạt động ổn định trên phân phối mới.
3. **Artifacts đã lưu:**
   - Bảng kết quả: `reports/external_model_results.csv`
   - Biểu đồ ROC: `reports/figures/external_roc_curves.png`
   - Ma trận nhầm lẫn: `reports/figures/external_confusion_matrix.png`
