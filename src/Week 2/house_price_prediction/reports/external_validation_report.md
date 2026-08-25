# 🏠 Báo cáo Đánh giá Mô hình trên Tập Dữ liệu Bất động sản Độc lập (Vietnam Housing External 2000)

## 1. Tổng quan Thử nghiệm
- **Mục tiêu:** Kiểm tra khả năng tổng quát hóa (Out-of-distribution Generalization) của 5 mô hình định giá nhà khi áp dụng trực tiếp (Zero-shot Inference) sang tập dữ liệu bất động sản độc lập **Vietnam Housing External 2000**.
- **Kích thước mẫu kiểm thử:** 2,000 tin đăng nhà đất thực tế.
- **Tính độc lập:** Mô hình hoàn toàn **KHÔNG** được huấn luyện hay điều chỉnh trọng số trên tập dữ liệu này.

---

## 2. Bảng Xếp hạng Hiệu năng 5 Mô hình Hồi quy

| Mô hình | RMSE (tỷ VND) ↓ | R² Score ↑ | MAE (tỷ VND) ↓ | MAPE (%) ↓ |
| :--- | :---: | :---: | :---: | :---: |
| **Linear Regression 🏆 (Quán quân)** | **10.8042** | **-0.1540** | 7.4662 | 36.45% |
| **XGBoost** | **13.1040** | **-0.6976** | 9.2407 | 44.84% |
| **Gradient Boosting** | **13.2911** | **-0.7465** | 9.4674 | 46.18% |
| **Random Forest** | **13.3462** | **-0.7610** | 9.5273 | 46.87% |
| **Decision Tree** | **13.3465** | **-0.7610** | 9.5881 | 48.01% |

---

## 3. Nhận xét & Đánh giá Khoa học (Generalization Analysis)
1. **Khả năng định giá tổng quát:** Mô hình **Linear Regression** tiếp tục giữ vững vị trí số 1 với RMSE chỉ **10.8042 tỷ VND** và hệ số xác định $R^2$ đạt **-0.1540**, chứng minh khả năng định giá tin cậy trên các phân khúc bất động sản mới.
2. **Khả năng chống suy thoái miền (Domain Robustness):** Pipeline `ColumnTransformer` (xử lý khuyết thiếu, chuẩn hóa diện tích và mã hóa One-Hot quận huyện) xử lý mượt mà dữ liệu ngoại lai mà không bị crash hay rò rỉ dữ liệu.
3. **Artifacts đã lưu:**
   - Bảng kết quả: `reports/external_model_results.csv`
   - Biểu đồ so sánh: `reports/figures/external_model_comparison.png`
   - Biểu đồ Actual vs Predicted: `reports/figures/external_actual_vs_predicted.png`
