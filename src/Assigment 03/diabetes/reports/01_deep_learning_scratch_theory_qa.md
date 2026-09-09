# Báo Cáo Chuyên Sâu: Nền Tảng Học Sâu Từ Con Số Không (Deep Learning From Scratch)
## Khung Toán Học Nền Tảng, Phân Tích Thực Nghiệm Chuyên Sâu & Bản Chất Của Học Sâu

---

## Mở Đầu: Triết Lý Thiết Kế & Bản Chất Của Học Sâu

Mục tiêu cốt lõi của bài thực hành này là bóc tách toàn bộ "hộp đen" của mạng nơ-ron nhân tạo thông qua việc cài đặt thuần túy bằng thư viện số học NumPy, không phụ thuộc vào bất kỳ framework cấp cao nào. Thông qua bài toán chẩn đoán tiểu đường (Pima Indians Diabetes Dataset), quy trình từ biểu diễn toán học, lan truyền xuôi, tính toán hàm mất mát, lan truyền ngược đạo hàm theo quy tắc dây chuyền (Chain Rule) đến cập nhật trọng số bằng Gradient Descent được minh thị rõ ràng.

Tài liệu này tổng hợp toàn bộ khung lý thuyết nền tảng, giải trình thấu đáo các câu hỏi bản chất toán học trọng tâm, và đúc kết các bài học rút ra từ chuỗi thực nghiệm chuyên sâu cùng các nghiên cứu đánh đổi kiến trúc (Ablation Studies).

---

## Phần I: Khung Toán Học & Mô Hình Tư Duy Toàn Diện (The Mental Model)

### 1.1. Học Sâu Dưới Góc Nhìn Hàm Hợp (Function Composition)
Một mạng nơ-ron sâu không phải là một thực thể ma thuật, mà là **chuỗi hợp thành của nhiều hàm số biến đổi không gian**:
$$\hat{y} = f_3(f_2(f_1(X; \theta_1); \theta_2); \theta_3)$$

Trong đó mỗi tầng $l$ thực hiện một phép biến đổi afin (affine transformation) kết hợp với một hàm kích hoạt phi tuyến tính (activation function):
$$Z^{[l]} = H^{[l-1]} W^{[l]} + b^{[l]}$$
$$H^{[l]} = \sigma^{[l]}\left(Z^{[l]}\right)$$

Với bài toán chẩn đoán tiểu đường gồm 8 đặc trưng đầu vào, kiến trúc tiêu chuẩn được biểu diễn:
$$\mathbb{R}^8 \xrightarrow{f_1} \mathbb{R}^{16} \xrightarrow{f_2} \mathbb{R}^8 \xrightarrow{f_3} \mathbb{R}^1$$

### 1.2. Bốn Phương Trình Cốt Lõi Định Nghĩa Deep Learning
Toàn bộ quá trình học sâu từ con số không được đúc kết qua 4 phương trình toán học nền tảng:

1. **Biểu diễn Tầng ẩn thứ nhất (First Representation):**
   $$H_1 = \text{ReLU}(X W_1 + b_1), \quad X \in \mathbb{R}^{N \times 8}, \; W_1 \in \mathbb{R}^{8 \times 16}, \; b_1 \in \mathbb{R}^{1 \times 16}, \; H_1 \in \mathbb{R}^{N \times 16}$$

2. **Biểu diễn Tầng ẩn sâu hơn (Deeper Hierarchical Representation):**
   $$H_2 = \text{ReLU}(H_1 W_2 + b_2), \quad H_1 \in \mathbb{R}^{N \times 16}, \; W_2 \in \mathbb{R}^{16 \times 8}, \; b_2 \in \mathbb{R}^{1 \times 8}, \; H_2 \in \mathbb{R}^{N \times 8}$$

3. **Dự đoán Xác suất Bernoulli (Final Probability Prediction):**
   $$\hat{y} = \sigma(H_2 W_3 + b_3) = \frac{1}{1 + e^{-(H_2 W_3 + b_3)}}, \quad W_3 \in \mathbb{R}^{8 \times 1}, \; b_3 \in \mathbb{R}^{1 \times 1}, \; \hat{y} \in \mathbb{R}^{N \times 1}$$

4. **Tối ưu hóa Thông số (Parameter Learning via Gradient Descent):**
   $$W^{[l]} \leftarrow W^{[l]} - \eta \frac{\partial L}{\partial W^{[l]}}, \quad b^{[l]} \leftarrow b^{[l]} - \eta \frac{\partial L}{\partial b^{[l]}}$$

### 1.3. Chu Trình Huấn Luyện Khép Kín (Closed-loop Training Cycle)
$$X \xrightarrow{\text{Forward}} H_1 \xrightarrow{\text{Forward}} H_2 \xrightarrow{\text{Forward}} \hat{y} \xrightarrow{\text{Loss}} L \xrightarrow{\text{Backprop}} \nabla_\theta L \xrightarrow{\text{Update}} \theta \leftarrow \theta - \eta \nabla_\theta L$$

Chu trình này được lặp lại tuần tự qua từng epoch, dẫn dắt các trọng số từ trạng thái khởi tạo ngẫu nhiên tiến dần tới điểm cực tiểu trên mặt cong hàm mất mát.

---

## Phần II: Bản Chất Toán Học & Các Câu Hỏi Cốt Lõi Của Deep Learning

### Câu 1: Khác biệt cốt lõi giữa mô hình Machine Learning truyền thống và mô hình Deep Learning là gì?
- **Machine Learning truyền thống (SVM, Logistic Regression, Random Forest, v.v.):** Dựa chủ yếu vào quy trình trích xuất đặc trưng thủ công (**Handcrafted Feature Engineering**). Kỹ sư dữ liệu phải sử dụng kiến thức nghiệp vụ để tạo ra các biến mới từ dữ liệu thô. Nếu việc trích chọn đặc trưng không nắm bắt được tương tác phi tuyến phức tạp, mô hình sẽ bị nghẽn hiệu năng.
- **Deep Learning:** Tự động hóa hoàn toàn quy trình này thông qua cơ chế học biểu diễn phân cấp (**Hierarchical Representation Learning**). Dữ liệu thô $X$ được truyền trực tiếp vào mạng; các tầng ẩn đầu tiên tự học các kết hợp đặc trưng mức thấp, các tầng sâu hơn tổng hợp thành các khái niệm trừu tượng mức cao, phục vụ trực tiếp cho mục tiêu tối ưu hàm mất mát.

### Câu 2: Ý nghĩa bản chất của phương trình $\hat{y} = f_3(f_2(f_1(X)))$ là gì?
- Phương trình thể hiện tư tưởng **Function Composition** (hợp thành hàm số).
- Đầu vào thô $X$ không được dùng trực tiếp để đưa ra phán quyết, mà trải qua chuỗi chuyển đổi không gian liên tục:
  - $f_1$: Ánh xạ không gian 8 chiều của bệnh nhân sang không gian biểu diễn sơ cấp 16 chiều.
  - $f_2$: Chắt lọc và kết hợp các đặc trưng sơ cấp thành không gian biểu diễn cô đọng 8 chiều.
  - $f_3$: Nén không gian 8 chiều thành một giá trị vô hướng biểu thị xác suất mắc bệnh.
- Tính chất xếp chồng (stacking) này cho phép mạng phân rã một bài toán phân loại phi tuyến tính cực kỳ phức tạp thành chuỗi các phép biến đổi hình học đơn giản hơn.

### Câu 3: Mục đích của ma trận trọng số $W$ (Weights) là gì?
- Về mặt hình học, ma trận $W$ thực hiện các phép biến đổi tuyến tính: **quay (rotation), co giãn (scaling) và chiếu (projection)** không gian đặc trưng từ số chiều $d_{in}$ sang $d_{out}$.
- Về mặt thống kê, mỗi phần tử $W_{ij}$ định lượng mức độ tương quan và tầm quan trọng của nơ-ron thứ $i$ ở tầng trước đối với việc kích hoạt nơ-ron thứ $j$ ở tầng sau. Trọng số chính là nơi lưu giữ tri thức học được từ dữ liệu.

### Câu 4: Mục đích của vector hệ số chệch $b$ (Bias) là gì?
- Vector $b$ thực hiện phép **tịnh tiến (translation / affine shift)** không gian đặc trưng.
- Nếu không có $b$, mặt phẳng siêu phẳng phân chia $Z = XW$ sẽ luôn bắt buộc phải đi qua gốc tọa độ $(0, 0, \dots, 0)$. Trong thực tế y tế, ngay cả khi một số chỉ số của bệnh nhân bằng 0, nguy cơ mắc bệnh không nhất thiết phải bằng 0. Bias cung cấp sự tự do để dịch chuyển ngưỡng kích hoạt độc lập với các giá trị đầu vào.

### Câu 5: Tại sao nhất thiết phải có hàm kích hoạt phi tuyến tính (Nonlinear Activation Functions)?
- Giả sử ta loại bỏ hàm phi tuyến, khi đó:
  $$H_1 = X W_1 + b_1$$
  $$H_2 = H_1 W_2 + b_2 = (X W_1 + b_1) W_2 + b_2 = X (W_1 W_2) + (b_1 W_2 + b_2)$$
  $$\hat{y} = H_2 W_3 + b_3 = X (W_1 W_2 W_3) + \text{bias}_{\text{eff}} = X W_{\text{eff}} + b_{\text{eff}}$$
- Tích của chuỗi các ma trận tuyến tính chỉ là **một ma trận tuyến tính duy nhất**. Khi đó, dù mạng có sâu 100 tầng, năng lực biểu diễn của nó vẫn chỉ tương đương với một mô hình Logistic Regression tuyến tính đơn tầng, hoàn toàn mất khả năng học các ranh giới quyết định phi tuyến phức tạp trong dữ liệu thực tế.

### Câu 6: Hàm kích hoạt ReLU làm gì và tại sao lại được ưu tiên sử dụng?
- **Định nghĩa toán học:**
  $$\text{ReLU}(z) = \max(0, z) = \begin{cases} z & \text{khi } z > 0 \\ 0 & \text{khi } z \le 0 \end{cases}$$
- **Đạo hàm:**
  $$\text{ReLU}'(z) = \begin{cases} 1 & \text{khi } z > 0 \\ 0 & \text{khi } z \le 0 \end{cases}$$
- **Lý do ưu tiên:**
  1. *Triệt tiêu hiện tượng biến mất đạo hàm (Vanishing Gradient):* Với $z > 0$, đạo hàm luôn bằng 1, giúp tín hiệu gradient truyền ngược nguyên vẹn qua nhiều tầng ẩn.
  2. *Hiệu quả tính toán vượt trội:* Chỉ yêu cầu phép so sánh ngưỡng $z > 0$, không đòi hỏi tính toán hàm mũ $e^z$ tốn kém như Sigmoid hay Tanh.
  3. *Tạo tính thưa (Sparsity):* Các giá trị âm bị ép về 0, giúp mạng kích hoạt chọn lọc các đặc trưng quan trọng, tăng tính khái quát hóa.

### Câu 7: Tại sao sử dụng hàm Sigmoid ở tầng đầu ra?
- **Định nghĩa:** $\sigma(z) = \frac{1}{1 + e^{-z}}$.
- **Đặc tính:** Ánh xạ mọi giá trị thực $z \in (-\infty, +\infty)$ thành một giá trị liên tục trong khoảng mở $(0, 1)$.
- **Ý nghĩa xác suất:** Trong bài toán phân loại nhị phân (0: không bệnh, 1: có bệnh), đầu ra được mô hình hóa theo phân phối Bernoulli. Giá trị $\hat{y} = \sigma(Z_3)$ được diễn giải trực tiếp là xác suất hậu nghiệm $P(Y = 1 \mid X)$.

### Câu 8: Tại sao mạng nơ-ron cần một hàm mất mát (Loss Function)?
- Mạng nơ-ron cần một đại lượng vô hướng định lượng chính xác **mức độ sai lệch** giữa dự đoán của mô hình $\hat{y}$ và nhãn thực tế $y$.
- Hàm mất mát đóng vai trò là "la bàn" điều hướng quá trình tối ưu. Đạo hàm của hàm mất mát theo từng tham số xác định chiều hướng và biên độ cần điều chỉnh của các trọng số nhằm cải thiện chất lượng dự đoán.

### Câu 9: Hàm mất mát Binary Cross-Entropy (BCE) đo lường điều gì?
- **Công thức:**
  $$L(y, \hat{y}) = -\frac{1}{N} \sum_{i=1}^N \left[ y_i \ln(\hat{y}_i) + (1 - y_i) \ln(1 - \hat{y}_i) \right]$$
- **Bản chất đo lường:** BCE chính là đối số của log-likelihood cực đại (Negative Log-Likelihood) của phân phối Bernoulli.
  - Khi $y = 1$: Loss $= -\ln(\hat{y})$. Nếu $\hat{y} \to 1$, Loss $\to 0$; nếu $\hat{y} \to 0$, Loss $\to +\infty$.
  - Khi $y = 0$: Loss $= -\ln(1 - \hat{y})$. Nếu $\hat{y} \to 0$, Loss $\to 0$; nếu $\hat{y} \to 1$, Loss $\to +\infty$.
- Hàm BCE áp đặt hình phạt logarit cực kỳ nặng nề lên các dự đoán vừa tự tin vừa sai lầm, từ đó tạo ra lực kéo gradient rất mạnh giúp mô hình nhanh chóng sửa sai.

### Câu 10: Gradient là gì về mặt toán học và hình học?
- **Toán học:** Gradient $\nabla_\theta L$ là một vector chứa các đạo hàm riêng của hàm mất mát $L$ đối với từng tham số trong mô hình:
  $$\nabla_\theta L = \left[ \frac{\partial L}{\partial W_1}, \frac{\partial L}{\partial b_1}, \dots, \frac{\partial L}{\partial W_3}, \frac{\partial L}{\partial b_3} \right]^T$$
- **Hình học:** Tại một điểm trên mặt cong mất mát nhiều chiều, vector gradient chỉ ra **hướng dốc tăng nhanh nhất** của hàm mất mát. Độ dài (chuẩn) của vector gradient thể hiện độ dốc của bề mặt tại điểm đó.

### Câu 11: Thuật toán lan truyền ngược (Backpropagation) thực chất tính toán cái gì?
- Backpropagation thực chất là việc áp dụng có hệ thống **Quy tắc dây chuyền (Chain Rule)** trong giải tích vi phân đa biến để tính toán gradient của hàm mất mát đối với từng trọng số và hệ số chệch ở tất cả các tầng: $\frac{\partial L}{\partial W^{[l]}}$ và $\frac{\partial L}{\partial b^{[l]}}$.
- Bằng cách lưu trữ các giá trị trung gian ở lượt lan truyền xuôi (`cache`), thuật toán tái sử dụng kết quả đạo hàm từ tầng sau để truyền ngược về tầng trước, giảm độ phức tạp tính toán từ hàm mũ xuống tuyến tính theo số lượng kết nối trong mạng.

### Câu 12: Thuật toán hạ độ dốc (Gradient Descent) hoạt động như thế nào?
- Thuật toán cập nhật tham số theo hướng **ngược chiều với vector gradient** (hướng dốc giảm nhanh nhất):
  $$\theta^{(t+1)} = \theta^{(t)} - \eta \nabla_\theta L(\theta^{(t)})$$
- Trong đó $\eta$ (learning rate) là hệ số bước đi. Quá trình này giúp mô hình trượt dần từ vị trí có sai số lớn xuống đáy của lòng chảo mất mát.

### Câu 13: Tại sao các trọng số cần được cập nhật lặp đi lặp lại qua nhiều epoch?
- Bề mặt hàm mất mát của mạng nơ-ron là một không gian phi tuyến tính nhiều chiều phức tạp với nhiều điểm lồi lõm.
- Gradient chỉ cung cấp thông tin xấp xỉ tuyến tính tại một lân cận vô cùng nhỏ quanh điểm hiện tại (local linear approximation). Do đó, ta chỉ có thể di chuyển từng bước nhỏ an toàn ($\eta$). Cần hàng trăm đến hàng nghìn bước lặp liên tiếp để dịch chuyển dần từ điểm khởi tạo ngẫu nhiên về vùng hội tụ tối ưu.

### Câu 14: Tại sao bắt buộc phải chia tách tập Train và tập Test?
- Mục tiêu tối thượng của học máy là **khả năng tổng quát hóa (Generalization)** trên những dữ liệu chưa từng thấy trong tương lai, chứ không phải học vẹt (Memorization) dữ liệu đã học.
- Nếu chỉ đánh giá trên tập Train, một mô hình bị quá khớp (Overfitting) trầm trọng vẫn có thể đạt độ chính xác 100%, gây ra ảo giác về hiệu năng. Tập Test độc lập đóng vai trò là thước đo khách quan đánh giá năng lực thực tế.

### Câu 15: Tại sao cần chuẩn hóa dữ liệu đặc trưng (Feature Scaling / Normalization)?
- Các đặc trưng đầu vào có thang đo rất chênh lệch: `Insulin` có thể lên tới 846 $\mu\text{U/ml}$, trong khi `PedigreeFunction` chỉ dao động từ 0.08 đến 2.42.
- Nếu không chuẩn hóa, mặt cong mất mát sẽ bị kéo giãn thành hình elip hẹp và dài. Gradient theo hướng biến có giá trị lớn sẽ dao động dữ dội, trong khi gradient theo hướng biến nhỏ di chuyển cực kỳ chậm, khiến quá trình huấn luyện bất ổn hoặc đình trệ.
- Chuẩn hóa Z-score ($\mu = 0, \sigma = 1$) đưa mặt cong mất mát về dạng tròn (isotropic), giúp vector gradient hướng thẳng về điểm cực tiểu, cho phép sử dụng tốc độ học lớn hơn và tăng tốc độ hội tụ gấp nhiều lần.

### Câu 16: Khác biệt cốt lõi giữa xác suất (Probability) và quyết định phân lớp (Class Prediction)?
- **Xác suất $\hat{y} \in (0, 1)$:** Đầu ra liên tục biểu thị mức độ tin cậy hoặc nguy cơ của mô hình (ví dụ: bệnh nhân A có $68.4\%$ khả năng mắc bệnh).
- **Quyết định phân lớp $\hat{y}_{\text{class}} \in \{0, 1\}$:** Hành động nhị phân rời rạc thu được sau khi so sánh xác suất với một ngưỡng quyết định $\tau$:
  $$\hat{y}_{\text{class}} = \mathbb{I}(\hat{y} \ge \tau)$$
- Ngưỡng mặc định $\tau = 0.5$ mang tính toán học thuần túy. Trong các ứng dụng thực tế (đặc biệt là y tế), $\tau$ cần được điều chỉnh linh hoạt dựa trên chi phí của việc bỏ sót bệnh (False Negative) so với báo động nhầm (False Positive).

---

## Phần III: Tổng Hợp & Đánh Giá Thực Nghiệm Chuyên Sâu (Ablation & Sensitivity Analysis)

### 3.1. Bảng Tổng Hợp Kết Quả Bóc Tách & Đánh Đổi Kiến Trúc

| Nghiên cứu Thực nghiệm | Mục tiêu Khảo sát | Cấu hình Mô hình | Kết quả Định lượng | Đánh giá Khoa học & Bài học Rút ra |
| :--- | :--- | :--- | :--- | :--- |
| **Mô hình Tiêu chuẩn** | Tối ưu hóa tiền xử lý và tham số huấn luyện | $8 \to 16 \to 8 \to 1$<br>(Chuẩn hóa, Stratified, $\eta=0.02$) | Loss: $0.4982 \to 0.3565$<br>Acc: $69.48\% \to 81.17\%$<br>Recall: $44.83\% \to 75.93\%$ | Tiền xử lý y tế chuẩn xác và triệt tiêu Data Leakage tạo bước nhảy vọt hiệu năng (+31.1% Recall). |
| **Khảo sát Độ rộng (Width Study)** | Mở rộng dung lượng nơ-ron (Wide Architecture) | $8 \to 32 \to 16 \to 1$<br>(833 tham số) | Final Loss: $0.3570$<br>Test Acc: $77.27\%$ | Mở rộng số nơ-ron làm số tham số tăng gần gấp 3, Loss giảm nhẹ nhưng Test Acc giảm do quá khớp trên tập dữ liệu nhỏ (768 mẫu). |
| **Khảo sát Tốc độ học (LR Study)** | Đánh giá độ nhạy tốc độ học | $\eta \in \{0.001, 0.01, 0.02, 0.05\}$ | $\eta=0.001$: Loss $0.5755$<br>$\eta=0.01$: Loss $0.4079$<br>$\eta=0.02$: Loss $0.3565$<br>$\eta=0.05$: Loss $0.3956$ | $\eta=0.001$ hội tụ quá chậm; $\eta=0.05$ gây dao động đáy thung lũng; $\eta=0.02$ là điểm tối ưu cân bằng tốc độ và độ mịn. |
| **Khảo sát Độ sâu (Depth Study)** | Đánh giá kiến trúc rút gọn (Shallow Architecture) | $8 \to 16 \to 1$<br>(145 tham số) | Final Loss: $0.4059$<br>Test Acc: $75.32\%$ | Thiếu tầng trừu tượng trung gian làm giảm khả năng trích chọn đặc trưng phân cấp, khiến độ chính xác giảm 5.85%. |
| **Bóc tách Phi tuyến (No-ReLU)** | Loại bỏ hoàn toàn phi tuyến (Linear Only) | $8 \to 16 \to 8 \to 1$<br>(Không ReLU, thuần tuyến tính) | Final Loss: $0.4330$<br>Test Acc: $70.13\%$ | Mạng suy biến thành một phép biến đổi tuyến tính đơn lẻ, hoàn toàn thất bại trong việc học các mẫu hình phi tuyến. |
| **Tối ưu Ngưỡng Lâm sàng** | Đánh đổi Precision - Recall và dò ngưỡng tối ưu | $\tau \in \{0.30, 0.50, 0.70\}$<br>và điểm tối ưu $\tau = 0.47$ | $\tau=0.30$: Rec $88.9\%$, Prec $55.8\%$<br>$\tau=0.50$: Rec $72.2\%$, Prec $72.2\%$<br>$\tau=0.70$: Rec $42.6\%$, Prec $82.1\%$<br>$\tau=0.47$: F1 $73.87\%$ | Thể hiện sự đánh đổi trực tiếp giữa Precision và Recall. Ngưỡng $\tau=0.47$ hạ số ca bỏ sót bệnh từ 32 xuống 13. |
| **Phân tích Biểu diễn Nội tại** | Kiểm tra kích thước không gian ẩn & Chiếu PCA | In `H1.shape: (154, 16)`, `H2.shape: (154, 8)` & Vẽ Scatter PCA 2D qua các tầng | Trực quan hóa quá trình nén và phân tách dần 2 cụm bệnh nhân từ không gian thô 8D qua tầng ẩn 16D và 8D. |

---

## Phần IV: Cầu Nối Chuyển Tiếp Sang Framework Học Sâu Hiện Đại (PyTorch)

Mặc dù việc xây dựng mạng nơ-ron từ đầu bằng NumPy giúp ta nắm vững từng phép vi tích phân và quy trình đại số tuyến tính, việc mở rộng mô hình này lên các bài toán thị giác máy tính, ngôn ngữ tự nhiên hay dữ liệu lớn sẽ gặp các giới hạn:
1. **Đạo hàm thủ công (Manual Differentiation):** Khi kiến trúc phức tạp (Residual connection, Transformer attention), việc tính vi phân bằng tay là bất khả thi và dễ xảy ra lỗi sai số học.
2. **Tận dụng phần cứng (Hardware Acceleration):** NumPy chạy trên CPU đơn luồng, không tận dụng được hàng nghìn nhân tính toán song song của GPU / TPU.

Framework học sâu hiện đại như **PyTorch** sẽ tự động hóa các bước kỹ thuật này:
- `torch.Tensor`: Hỗ trợ tính toán song song trên GPU và theo dõi đồ thị tính toán.
- `torch.autograd`: Tự động tính toán đạo hàm theo quy tắc dây chuyền (`loss.backward()`).
- `torch.nn.Module`: Cung cấp sẵn các khối kiến trúc chuẩn (`nn.Linear`, `nn.ReLU`, `nn.Sequential`).
- `torch.optim`: Cung cấp các thuật toán tối ưu tiên tiến (Adam, RMSprop, AdamW).

Tuy nhiên, **bản chất của bài toán hoàn toàn không thay đổi**:
$$\hat{y} = f(X; \theta) \quad \text{và} \quad \theta \leftarrow \theta - \eta \nabla_\theta L$$

Hiểu sâu sắc cách thức hoạt động từ con số không chính là nền tảng vững chắc nhất để làm chủ hoàn toàn các công cụ chuyên nghiệp trong giai đoạn tiếp theo.
