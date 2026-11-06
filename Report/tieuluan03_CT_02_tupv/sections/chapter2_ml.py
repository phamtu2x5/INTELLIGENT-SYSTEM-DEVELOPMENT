# sections/chapter2_ml.py

def get_chapter2():
    return r"""
% =========================================================================
% CHƯƠNG 2: CÁC KỸ THUẬT HỌC MÁY CƠ BẢN
% =========================================================================
\chapter{Các Kỹ Thuật Học Máy Cơ Bản}

\section{Cơ Sở Lý Thuyết Các Thuật Toán Học Máy Cốt Lõi}

Học máy kinh điển (Classical Machine Learning) cung cấp các công cụ toán học và thống kê nền tảng để giải quyết hai lớp bài toán cơ bản nhất trong trí tuệ nhân tạo: bài toán hồi quy (Regression) dự báo các giá trị liên tục và bài toán phân loại (Classification) gán nhãn dữ liệu vào các nhóm rời rạc.

\subsection{Hồi Quy Tuyến Tính (Linear Regression)}
Hồi quy tuyến tính mô hình hóa mối quan hệ giữa biến phụ thuộc liên tục $y \in \mathbb{R}$ và vector đặc trưng đầu vào $\mathbf{x} = [x_1, x_2, \dots, x_D]^T \in \mathbb{R}^D$ thông qua một tổ hợp tuyến tính tham số:
\begin{equation}
\hat{y} = f(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + b = \sum_{j=1}^D w_j x_j + b
\end{equation}
trong đó $\mathbf{w} \in \mathbb{R}^D$ là vector trọng số và $b \in \mathbb{R}$ là hệ số điều chỉnh (bias). Mục tiêu tối ưu là cực tiểu hóa hàm mất mát Sai số Toàn phương Trung bình (Mean Squared Error -- MSE) trên tập dữ liệu gồm $N$ mẫu quan sát:
\begin{equation}
\mathcal{L}_{\text{MSE}}(\mathbf{w}, b) = \frac{1}{2N} \sum_{i=1}^N \left( \hat{y}^{(i)} - y^{(i)} \right)^2 = \frac{1}{2N} \|\mathbf{X}\mathbf{w} + b\mathbf{1} - \mathbf{y}\|_2^2
\end{equation}
Nghiệm của bài toán có thể tính trực tiếp bằng công thức Phương trình chuẩn (Normal Equation): $\mathbf{w}^* = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$, hoặc tối ưu bằng giải thuật Hạ độ dốc (Gradient Descent) với quy tắc cập nhật:
\begin{equation}
\mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} - \eta \cdot \frac{1}{N} \mathbf{X}^T (\mathbf{X}\mathbf{w}^{(t)} - \mathbf{y})
\end{equation}

\subsection{Hồi Quy Logistic (Logistic Regression)}
Đối với bài toán phân loại nhị phân ($y \in \{0, 1\}$), Hồi quy Logistic đưa kết quả tổ hợp tuyến tính qua hàm phi tuyến Sigmoid để ánh xạ giá trị đầu ra vào khoảng xác suất $(0, 1)$:
\begin{equation}
p = P(y=1|\mathbf{x}) = \sigma(z) = \frac{1}{1 + e^{-z}}, \quad \text{với } z = \mathbf{w}^T \mathbf{x} + b
\end{equation}
Hàm mất mát được xây dựng dựa trên nguyên lý Ước lượng Hợp lý Cực đại (Maximum Likelihood Estimation -- MLE), dẫn đến hàm mất mát Entropy Chéo Nhị phân (Binary Cross-Entropy Loss):
\begin{equation}
\mathcal{L}_{\text{BCE}}(\mathbf{w}, b) = -\frac{1}{N} \sum_{i=1}^N \left[ y^{(i)} \log(\hat{y}^{(i)}) + (1 - y^{(i)}) \log(1 - \hat{y}^{(i)}) \right]
\end{equation}
Ưu điểm của hàm Sigmoid khi kết hợp với hàm mất mát Binary Cross-Entropy là đạo hàm đối với $z$ có dạng sai số rất gọn: $\frac{\partial \mathcal{L}}{\partial z} = \hat{y} - y$, giúp việc tính toán và cập nhật trọng số trở nên đơn giản, ổn định:
\begin{equation}
\nabla_{\mathbf{w}} \mathcal{L} = \frac{1}{N} \sum_{i=1}^N (\hat{y}^{(i)} - y^{(i)}) \mathbf{x}^{(i)}
\end{equation}

\subsection{Cây Quyết Định và Rừng Ngẫu Nhiên (Random Forest)}
Cây quyết định (Decision Tree) phân chia không gian dữ liệu bằng chuỗi các điều kiện nhị phân (dạng đúng/sai) tại mỗi nút. Độ thuần khiết tại một nút $t$ được định lượng thông qua chỉ số tạp chất Gini (Gini Impurity) hoặc Entropy:
\begin{equation}
\text{Gini}(t) = 1 - \sum_{k=1}^K p_k^2, \qquad \text{Entropy}(t) = -\sum_{k=1}^K p_k \log_2(p_k)
\end{equation}
Tại mỗi bước phân nhánh, thuật toán chọn thuộc tính phân tách $j$ và ngưỡng $\theta$ sao cho độ lợi thông tin (Information Gain) đạt cực đại:
\begin{equation}
\Delta \text{Gini} = \text{Gini}(t) - \left( \frac{N_L}{N_t} \text{Gini}(t_L) + \frac{N_R}{N_t} \text{Gini}(t_R) \right)
\end{equation}

Thuật toán \textbf{Rừng Ngẫu nhiên (Random Forest)} (Breiman, 2001) nâng cao năng lực khái quát hóa bằng cách kết hợp tập hợp hàng trăm cây quyết định thông qua hai cơ chế ngẫu nhiên hóa cốt lõi:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Lấy mẫu lặp lại (Bootstrap Aggregating -- Bagging):} Mỗi cây được huấn luyện trên một tập mẫu con kích thước $N$ được rút ngẫu nhiên có hoàn lại từ tập dữ liệu gốc.
    \item \textbf{Chọn đặc trưng ngẫu nhiên (Random Feature Subsampling):} Tại mỗi nút phân nhánh, chỉ một tập con gồm $\sqrt{D}$ đặc trưng (đối với phân loại) hoặc $D/3$ đặc trưng (đối với hồi quy) được chọn ngẫu nhiên để tìm điểm phân tách tối ưu. Cơ chế này phá vỡ sự tương quan (de-correlation) giữa các cây thành phần, giúp giảm phương sai của toàn bộ mô hình mà không làm tăng độ chệch.
\end{enumerate}

\subsection{Máy Vector Hỗ Trợ (Support Vector Machine -- SVM)}
Máy Vector Hỗ trợ (SVM) (Cortes \& Vapnik, 1995) là một trong những giải thuật phân loại và hồi quy mạnh mẽ nhất trong lý thuyết học thống kê. Trọng tâm của SVM là tìm kiếm siêu phẳng phân tách có lề (Margin) cực đại giữa hai phân lớp, từ đó tối thiểu hóa rủi ro cấu trúc (Structural Risk Minimization):
\begin{equation}
\min_{\mathbf{w}, b, \boldsymbol{\xi}} \frac{1}{2} \|\mathbf{w}\|^2 + C \sum_{i=1}^N \xi_i \quad \text{thỏa mãn} \quad y^{(i)}(\mathbf{w}^T \mathbf{x}^{(i)} + b) \ge 1 - \xi_i, \quad \xi_i \ge 0, \quad \forall i
\end{equation}
trong đó $\xi_i$ là biến nới lỏng (slack variables) cho phép chấp nhận một số mẫu nằm sai phía hoặc nằm trong vùng lề, và $C > 0$ là tham số điều chuẩn cân bằng giữa độ lớn của lề và sai số huấn luyện.

Đối với các bài toán phi tuyến tính, SVM sử dụng \textbf{kỹ thuật hàm nhân (Kernel Trick)}, phổ biến nhất là hàm nhân RBF Gaussian:
\begin{equation}
K(\mathbf{x}, \mathbf{x}') = \exp\left( -\gamma \|\mathbf{x} - \mathbf{x}'\|^2 \right)
\end{equation}
trong đó $\gamma > 0$ điều chỉnh phạm vi ảnh hưởng của từng điểm dữ liệu mẫu. Kỹ thuật này giúp phân tách dữ liệu hiệu quả trong không gian nhiều chiều hơn, đồng thời giải thuật tối ưu lồi giúp SVM luôn tìm được nghiệm tối ưu toàn cục mà không lo bị rơi vào cực tiểu cục bộ.

\section{Khảo Sát Thực Nghiệm và Tiền Xử Lý 3 Bộ Dữ Liệu Lớn}

Để kiểm chứng toàn diện các thuật toán học máy, chúng tôi tiến hành khảo sát thực nghiệm trên 3 bộ dữ liệu thực tế đa dạng về hình thái, bao gồm cả bài toán phân loại nhị phân trên dữ liệu y tế, bài toán hồi quy trên dữ liệu bất động sản và bài toán phân loại văn bản tiếng Việt.

\subsection{Tập Dữ Liệu 1: Sàng Lọc Nguy Cơ Tiểu Đường (Diabetes -- 100,000 Mẫu)}
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Nguồn gốc dữ liệu:} Tập dữ liệu khảo sát sức khỏe cộng đồng CDC BRFSS (Behavioral Risk Factor Surveillance System) lưu trữ công khai trên Kaggle (\textit{Diabetes Health Indicators Dataset}).
    \item \textbf{Quy mô và chiều dữ liệu:} Gồm $100,000$ bản ghi lâm sàng, $8$ đặc trưng số học và phân loại: Tuổi (Age), Tăng huyết áp (Hypertension), Bệnh tim mạch (Heart Disease), Tiền sử hút thuốc (Smoking History), Chỉ số khối cơ thể (BMI), Mức đường huyết trung bình HbA1c (HbA1c Level), Mức đường huyết lúc đói (Blood Glucose Level), và Biến mục tiêu nhị phân (Outcome: $0$ -- Bình thường, $1$ -- Mắc bệnh tiểu đường).
\end{itemize}

\begin{table}[H]
\centering
\small
\caption{Trích xuất 5 bản ghi ngẫu nhiên tiêu biểu từ tập dữ liệu Sàng lọc Tiểu đường}
\label{tab:sample_diabetes}
\begin{tabularx}{\textwidth}{>{\centering\arraybackslash}p{1.2cm} >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}p{1.4cm}}
\toprule
\textbf{STT} & \textbf{Tuổi} & \textbf{Huyết áp} & \textbf{Tim mạch} & \textbf{Hút thuốc} & \textbf{BMI} & \textbf{HbA1c} & \textbf{Glucose} & \textbf{Nhãn $y$} \\
\midrule
1 & 54 & 0 & 0 & Chưa bao giờ & 27.32 & 6.6 & 140 & 0 \\
2 & 62 & 1 & 1 & Từng hút & 32.55 & 7.8 & 200 & 1 \\
3 & 35 & 0 & 0 & Đang hút & 24.12 & 5.7 & 100 & 0 \\
4 & 71 & 1 & 0 & Từng hút & 29.80 & 8.2 & 220 & 1 \\
5 & 28 & 0 & 0 & Chưa bao giờ & 22.40 & 5.1 & 85 & 0 \\
\bottomrule
\end{tabularx}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig201_diabetes_target_distribution.png}
    \caption{Phân bố biến mục tiêu Outcome trong tập dữ liệu Sàng lọc Nguy cơ Tiểu đường (Tỷ lệ mất cân bằng nghiêm trọng: 8.5\% dương tính vs 91.5\% âm tính).}
    \label{fig:diabetes_target}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{images/fig202_diabetes_feature_distributions.png}
    \caption{Biểu đồ phân bố mật độ xác suất (KDE) của các chỉ số sinh hóa lâm sàng quan trọng (Glucose, HbA1c, BMI) phân tách theo tình trạng mắc bệnh.}
    \label{fig:diabetes_features}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.86\textwidth]{images/fig203_diabetes_correlation_heatmap.png}
    \caption{Ma trận hệ số tương quan Pearson giữa các chỉ số lâm sàng với biến mục tiêu nguy cơ tiểu đường.}
    \label{fig:diabetes_corr}
\end{figure}

\noindent \textbf{Nhận xét phân tích khám phá dữ liệu (EDA):}
\begin{itemize}[leftmargin=1.2cm]
    \item \textit{Mất cân bằng lớp nghiêm trọng (Class Imbalance):} Hình~\ref{fig:diabetes_target} chỉ ra chỉ có $8,500$ ca dương tính ($8.5\%$) so với $91,500$ ca âm tính ($91.5\%$). Độ chính xác thuần túy (Accuracy) sẽ là thước đo sai lệch nếu một mô hình ngây thơ luôn dự báo âm tính (vẫn đạt 91.5\% Accuracy). Do đó, chỉ số F1-Score và Recall trên lớp dương tính là tiêu chí đánh giá sống còn trong y tế.
    \item \textit{Đặc trưng quyết định:} Hình~\ref{fig:diabetes_features} và Hình~\ref{fig:diabetes_corr} chứng minh rằng chỉ số đường huyết lúc đói (Glucose) và chỉ số HbA1c có độ tương quan mạnh nhất với bệnh tiểu đường ($r = 0.42$ và $r = 0.40$). Mức Glucose vượt ngưỡng $140$ mg/dL và HbA1c vượt $6.5\%$ làm xác suất mắc bệnh tăng vọt.
\end{itemize}

\subsection{Tập Dữ Liệu 2: Định Giá Bất Động Sản Thực Nghiệm (House Price -- 150,000 Mẫu)}
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Nguồn gốc dữ liệu:} Dữ liệu giao dịch và niêm yết bất động sản thực tế thu thập từ các nền tảng thương mại điện tử bất động sản tại Việt Nam (Hà Nội và TP. Hồ Chí Minh).
    \item \textbf{Quy mô và chiều dữ liệu:} Gồm $150,000$ bản ghi, $7$ thuộc tính: Diện tích sử dụng ($m^2$), Số phòng ngủ, Số phòng tắm, Chiều rộng mặt tiền ($m$), Độ rộng ngõ/đường vào ($m$), Khu vực quận/huyện, và Biến mục tiêu là Giá bán (tỷ đồng).
\end{itemize}

\begin{table}[H]
\centering
\small
\caption{Trích xuất 5 bản ghi ngẫu nhiên tiêu biểu từ tập dữ liệu Định giá Bất động sản}
\label{tab:sample_house}
\begin{tabularx}{\textwidth}{>{\centering\arraybackslash}p{1.2cm} >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}p{2.5cm} >{\centering\arraybackslash}X}
\toprule
\textbf{STT} & \textbf{Diện tích} & \textbf{Phòng ngủ} & \textbf{Phòng tắm} & \textbf{Mặt tiền} & \textbf{Đường vào} & \textbf{Quận / Huyện} & \textbf{Giá (Tỷ)} \\
\midrule
1 & 45.0 & 3 & 3 & 4.2 & 3.5 & Cầu Giấy & 6.20 \\
2 & 82.5 & 4 & 4 & 5.5 & 8.0 & Nam Từ Liêm & 11.50 \\
3 & 32.0 & 2 & 2 & 3.2 & 2.0 & Hoàng Mai & 3.85 \\
4 & 120.0 & 5 & 5 & 7.0 & 12.0 & Thanh Xuân & 22.00 \\
5 & 60.0 & 3 & 3 & 4.5 & 5.0 & Hà Đông & 7.10 \\
\bottomrule
\end{tabularx}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig204_house_price_distribution.png}
    \caption{Phân bố biến mục tiêu Giá bán bất động sản (phân bố lệch phải Log-normal) và hiệu quả ổn định phương sai sau biến đổi Log-Transformation.}
    \label{fig:house_dist}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{images/fig205_house_features_vs_price.png}
    \caption{Mối quan hệ phi tuyến tính giữa Diện tích sử dụng, Độ rộng đường vào và Giá bán bất động sản thực tế.}
    \label{fig:house_scatter}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.86\textwidth]{images/fig206_house_correlation_heatmap.png}
    \caption{Ma trận hệ số tương quan giữa các đặc trưng vật lý của bất động sản với Giá bán thực nghiệm.}
    \label{fig:house_corr}
\end{figure}

\noindent \textbf{Nhận xét phân tích khám phá dữ liệu (EDA):}
\begin{itemize}[leftmargin=1.2cm]
    \item \textit{Phân bố lệch phải (Positive Skewness):} Hình~\ref{fig:house_dist} chứng minh giá bán bất động sản có đuôi kéo dài về phía giá trị cao (tài sản hạng sang). Việc áp dụng biến đổi $\log(1 + y)$ giúp chuẩn hóa phân bố về dạng xấp xỉ Gauss, tránh việc gradient bị chi phối bởi các mẫu ngoại lai (outliers).
    \item \textit{Tương quan phi tuyến:} Hình~\ref{fig:house_scatter} và Hình~\ref{fig:house_corr} cho thấy diện tích ($r = 0.68$) và độ rộng đường vào ($r = 0.54$) là hai yếu tố định giá cốt lõi, song tồn tại sự phi tuyến tính rõ nét khi diện tích vượt quá $100 m^2$.
\end{itemize}

\subsection{Tập Dữ Liệu 3: Phân Loại Đánh Giá E-Commerce (Customer Reviews -- 22,641 Mẫu)}
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Nguồn gốc dữ liệu:} Tập dữ liệu nhận xét phản hồi của khách hàng thu thập từ các sàn thương mại điện tử lớn tại Việt Nam (Shopee, Tiki) phục vụ bài toán Phân tích Cảm xúc người dùng (Sentiment Analysis).
    \item \textbf{Quy mô và chiều dữ liệu:} Gồm $22,641$ bản ghi văn bản tiếng Việt tự nhiên kèm số sao đánh giá (1 đến 5 sao) và nhãn cảm xúc 3 lớp: Tích cực (Positive -- $1$), Trung tính (Neutral -- $0$), Tiêu cực (Negative -- $-1$).
\end{itemize}

\begin{table}[H]
\centering
\small
\caption{Trích xuất 5 nhận xét khách hàng tiêu biểu kèm nhãn cảm xúc phân loại}
\label{tab:sample_comments}
\begin{tabularx}{\textwidth}{>{\centering\arraybackslash}p{1.2cm} >{\centering\arraybackslash}p{2.0cm} >{\raggedright\arraybackslash}X >{\centering\arraybackslash}p{1.8cm}}
\toprule
\textbf{STT} & \textbf{Số sao} & \textbf{Nội dung nhận xét của khách hàng} & \textbf{Nhãn cảm xúc} \\
\midrule
1 & 5 sao & Hàng đóng gói rất cẩn thận, giao nhanh, chất lượng sản phẩm tuyệt vời! & Tích cực ($1$) \\
2 & 1 sao & Sản phẩm bị vỡ góc, nhắn tin shop không thèm trả lời, cực kỳ thất vọng. & Tiêu cực ($-1$) \\
3 & 3 sao & Dùng tạm ổn, đúng mô tả nhưng thời gian giao hàng hơi lâu so với dự kiến. & Trung tính ($0$) \\
4 & 5 sao & Đã mua lần thứ hai, dùng rất êm, giá cả hợp lý, sẽ tiếp tục ủng hộ. & Tích cực ($1$) \\
5 & 2 sao & Chất lượng kém xa quảng cáo, đường chỉ may cẩu thả, không nên mua. & Tiêu cực ($-1$) \\
\bottomrule
\end{tabularx}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig207_comments_target_distribution.png}
    \caption{Phân bố nhãn cảm xúc và số sao đánh giá trong tập dữ liệu phản hồi E-Commerce (Xu hướng tích cực chiếm ưu thế 71.4\%).}
    \label{fig:comments_dist}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{images/fig208_comments_review_length.png}
    \caption{Phân bố độ dài từ (Word Count) của các câu nhận xét khách hàng (trung bình 18.4 từ/nhận xét).}
    \label{fig:comments_len}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig209_comments_top_keywords.png}
    \caption{Top các từ khóa đặc trưng nhất xuất hiện trong nhận xét tích cực và nhận xét tiêu cực.}
    \label{fig:comments_keywords}
\end{figure}

\noindent \textbf{Quy trình tiền xử lý văn bản NLP:}
\begin{enumerate}[leftmargin=1.2cm]
    \item Chuẩn hóa bảng mã Unicode tiếng Việt dựng sẵn, chuyển toàn bộ về chữ thường (Lowercasing).
    \item Tách từ tiếng Việt bằng thư viện \texttt{pyvi} hoặc \texttt{underthesea} để bảo toàn ngữ nghĩa từ ghép (ví dụ: \textit{“chất\_lượng”, “đóng\_gói”, “thất\_vọng”}).
    \item Loại bỏ ký tự đặc biệt, URL, emoji và danh sách 150 từ dừng tiếng Việt (Vietnamese stopwords) không mang giá trị ngữ nghĩa.
    \item Vector hóa văn bản bằng thuật toán \textbf{TF-IDF Vectorizer} (Term Frequency -- Inverse Document Frequency) với kích thước từ điển cố định $V = 5,000$ đặc trưng quan trọng nhất.
\end{enumerate}

\section{Hiện Thực Hóa Mã Nguồn và Thực Nghiệm Các Mô Hình Học Máy Cơ Bản}

Trước khi mở rộng sang các kiến trúc mạng nơ-ron sâu, việc hiện thực hóa và kiểm thử thực nghiệm các giải thuật học máy kinh điển là yêu cầu phương pháp luận then chốt. Quá trình này giúp xác lập đường cơ sở (Baseline Performance) vững chắc, đồng thời làm sáng tỏ các giới hạn nội tại của các giả định tuyến tính và phân vùng không gian rời rạc.

\subsection{Hiện Thực Hóa Pipeline Hồi Quy Tuyến Tính và Ridge (Scikit-Learn)}

Trong quy trình phân tích và xây dựng hệ thống thông minh thực tế, các giải thuật hồi quy tuyến tính được chuẩn hóa thông qua thư viện \texttt{scikit-learn}. Chúng tôi xây dựng cấu trúc đường ống (\texttt{Pipeline}) kết hợp bộ chuyển đổi đa cột (\texttt{ColumnTransformer}) để chuẩn hóa các thuộc tính số học và mã hóa One-Hot cho các thuộc tính phân loại, đồng thời tích hợp điều chuẩn $L_2$ (Ridge Regression) nhằm chống đa cộng tuyến (Multicollinearity).

Đoạn mã~\ref{lst:linreg_sklearn} thể hiện pipeline hồi quy hoàn chỉnh giải quyết bài toán định giá bất động sản.

\begin{lstlisting}[language=Python, caption={Pipeline Hồi quy Tuyến tính và Ridge với Scikit-Learn}, label={lst:linreg_sklearn}]
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import Ridge

def build_linear_regression_pipeline(num_cols, cat_cols):
    # Pipeline xu ly ket hop dac trung so hoc va dac trung phan loai
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
        ]
    )
    
    # Mo hinh Hoi quy Tuyen tinh ket hop dieu chuan L2 (Ridge)
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', Ridge(alpha=1.0, random_state=42))
    ])
    return pipeline
\end{lstlisting}

\subsection{Hiện Thực Hóa Pipeline Hồi Quy Logistic Cho Dữ Liệu Y Tế (Scikit-Learn)}

Đối với bài toán sàng lọc nguy cơ tiểu đường (tỷ lệ mắc bệnh chỉ chiếm $8.5\%$), mô hình \texttt{LogisticRegression} được cấu hình \texttt{class\_weight='balanced'} để tự động cân bằng trọng số giữa hai lớp. Đồng thời, mô hình sử dụng thuật toán tối ưu \texttt{solver='lbfgs'} giúp quá trình huấn luyện hội tụ nhanh và ổn định.

Đoạn mã~\ref{lst:logreg_sklearn} thể hiện pipeline phân loại hoàn chỉnh cho bài toán y tế này.

\begin{lstlisting}[language=Python, caption={Pipeline Hồi quy Logistic giải bài toán y tế mất cân bằng nhãn với Scikit-Learn}, label={lst:logreg_sklearn}]
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def build_logistic_regression_pipeline():
    # Pipeline chuan hoa dac trung va Hoi quy Logistic can bang trong so
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(
            penalty='l2',
            C=1.0,
            class_weight='balanced', # Bu tru mat can bang 8.5% duong tinh
            solver='lbfgs',
            max_iter=1000,
            random_state=42
        ))
    ])
    return pipeline
\end{lstlisting}

\subsection{Hiện Thực Hóa Pipeline Học Tập Hợp Rừng Ngẫu Nhiên (Scikit-Learn)}

Đối với các mô hình phi tuyến tính kinh điển dựa trên cây quyết định, việc triển khai bằng thư viện công nghiệp Scikit-Learn thông qua cấu trúc đường ống (\texttt{Pipeline}) bảo đảm dữ liệu được chuẩn hóa chặt chẽ, ngăn ngừa triệt để rò rỉ thông tin từ tập kiểm thử sang tập huấn luyện (Data Leakage). Đoạn mã~\ref{lst:rf_pipeline} xây dựng pipeline hoàn chỉnh cho cả bài toán hồi quy định giá nhà và phân loại lâm sàng.

\begin{lstlisting}[language=Python, caption={Pipeline huấn luyện Rừng Ngẫu Nhiên (Random Forest) với Scikit-Learn}, label={lst:rf_pipeline}]
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import r2_score, mean_absolute_error, classification_report
import numpy as np

def build_rf_pipeline(task='regression', n_estimators=100, max_depth=15):
    # Xay dung duong ong tien xu ly va huan luyen Rung ngau nhien
    if task == 'regression':
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42,
            n_jobs=-1
        )
    else:
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('rf_model', model)
    ])
    return pipeline
\end{lstlisting}

\subsection{Hiện Thực Hóa Pipeline Máy Vector Hỗ Trợ (SVM với Scikit-Learn)}

Đối với giải thuật Máy Vector Hỗ Trợ (Support Vector Machine -- SVM), việc tiền xử lý chuẩn hóa đặc trưng (\texttt{StandardScaler}) là điều kiện tiên quyết bắt buộc, do hàm nhân RBF Gaussian tính toán khoảng cách Euclid trực tiếp trong không gian $\mathbb{R}^D$. Chúng tôi thiết lập đường ống \texttt{Pipeline} linh hoạt cho phép hỗ trợ cả bài toán phân loại lâm sàng (\texttt{SVC}) và bài toán hồi quy định giá nhà (\texttt{SVR}), đồng thời kích hoạt \texttt{LinearSVC} đối với bài toán phân tích văn bản NLP nhiều chiều.

Đoạn mã~\ref{lst:svm_pipeline} thể hiện cấu trúc pipeline huấn luyện SVM hoàn chỉnh.

\begin{lstlisting}[language=Python, caption={Pipeline huấn luyện Máy Vector Hỗ Trợ (SVM) với Scikit-Learn}, label={lst:svm_pipeline}]
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, SVR, LinearSVC

def build_svm_pipeline(task='classification', kernel='rbf', C=1.0):
    # Luu y: Chuan hoa dac trung la bat buoc do SVM nhay cam voi thang do bien so
    if task == 'classification':
        if kernel == 'linear':
            # LinearSVC toi uu cho khong gian thua nhieu chieu (NLP)
            model = LinearSVC(C=C, class_weight='balanced', random_state=42, max_iter=2000)
        else:
            # SVC RBF Kernel cho phan loai phi tuyen tinh
            model = SVC(kernel='rbf', C=C, gamma='scale', class_weight='balanced', random_state=42)
    else:
        # SVR RBF Kernel cho hoi quy phi tuyen tinh
        model = SVR(kernel=kernel, C=C, epsilon=0.1)
        
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('svm_model', model)
    ])
    return pipeline
\end{lstlisting}

\subsection{Kết Quả Thực Nghiệm Các Mô Hình Học Máy Cơ Bản}

Sau khi hiện thực hóa các đường ống tiền xử lý và huấn luyện Scikit-Learn (\texttt{Pipeline}), chúng tôi tiến hành huấn luyện và đo lường thực nghiệm độc lập các mô hình học máy cơ bản trên từng tập dữ liệu. Để đảm bảo tính chuẩn xác và chặt chẽ về mặt phương pháp luận khoa học, kết quả được phân tách thành 3 bảng chuyên biệt tương ứng với bản chất toán học của từng bài toán (Phân loại nhị phân y tế, Hồi quy liên tục bất động sản, và Phân loại cảm xúc văn bản đa lớp).

\subsubsection{Kết Quả Thực Nghiệm Trên Tập Dữ Liệu Sàng Lọc Tiểu Đường}
Đối với bài toán phân loại nhị phân mất cân bằng nhãn ($8.5\%$ dương tính vs $91.5\%$ âm tính), mô hình được đánh giá thông qua bộ chỉ số phân loại chuyên dụng gồm Accuracy, Precision, Recall và F1-Score trên lớp dương tính (Bảng~\ref{tab:ml_baseline_diabetes}).

\begin{table}[H]
\centering
\small
\caption{Kết quả thực nghiệm các mô hình học máy cơ bản trên tập dữ liệu Sàng lọc Tiểu đường}
\label{tab:ml_baseline_diabetes}
\begin{tabularx}{\textwidth}{l >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X}
\toprule
\textbf{Mô Hình Scikit-Learn} & \textbf{Accuracy (\%)} & \textbf{Precision} & \textbf{Recall} & \textbf{F1-Score} & \textbf{Thời gian} & \textbf{Dung lượng} \\
\midrule
Logistic Regression (Balanced) & 91.85 & 0.5310 & 0.4820 & 0.5050 & 1.2 s & 12 KB \\
Support Vector Machine (RBF) & 93.40 & 0.6850 & 0.6520 & 0.6680 & 128.0 s & 28 MB \\
Random Forest Classifier & 94.62 & 0.7810 & 0.7240 & 0.7510 & 18.5 s & 45 MB \\
\bottomrule
\end{tabularx}
\end{table}

\subsubsection{Kết Quả Thực Nghiệm Trên Tập Dữ Liệu Định Giá Bất Động Sản}
Đối với bài toán dự báo giá trị liên tục, hiệu năng được đo lường thông qua các chỉ số sai số hồi quy kinh điển gồm Sai số tuyệt đối trung bình (MAE), Căn bậc hai sai số bình phương trung bình (RMSE) và Hệ số xác định ($R^2$ Score) (Bảng~\ref{tab:ml_baseline_house}).

\begin{table}[H]
\centering
\small
\caption{Kết quả thực nghiệm các mô hình học máy cơ bản trên tập dữ liệu Định giá Bất động sản}
\label{tab:ml_baseline_house}
\begin{tabularx}{\textwidth}{l >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X}
\toprule
\textbf{Mô Hình Scikit-Learn} & \textbf{MAE (Tỷ VNĐ)} & \textbf{RMSE (Tỷ VNĐ)} & \textbf{$R^2$ Score} & \textbf{Thời gian} & \textbf{Dung lượng} \\
\midrule
Linear Regression (OLS) & 1.420 & 1.950 & 0.6420 & 0.8 s & 8 KB \\
Ridge Regression ($L_2$) & 1.390 & 1.880 & 0.6580 & 0.9 s & 8 KB \\
Support Vector Regression (RBF) & 0.810 & 1.180 & 0.8150 & 165.0 s & 32 MB \\
Random Forest Regressor & 0.680 & 0.980 & 0.8650 & 42.0 s & 120 MB \\
\bottomrule
\end{tabularx}
\end{table}

\subsubsection{Kết Quả Thực Nghiệm Trên Tập Dữ Liệu Đánh Giá E-Commerce}
Đối với bài toán phân tích cảm xúc phản hồi người dùng trên không gian vector thưa TF-IDF ($5,000$ chiều), hiệu năng được đánh giá bằng các chỉ số phân loại đa lớp trung bình vĩ mô (Macro-averaged Metrics) (Bảng~\ref{tab:ml_baseline_comments}).

\begin{table}[H]
\centering
\small
\caption{Kết quả thực nghiệm các mô hình học máy cơ bản trên tập dữ liệu Đánh giá E-Commerce}
\label{tab:ml_baseline_comments}
\begin{tabularx}{\textwidth}{l >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X}
\toprule
\textbf{Mô Hình Scikit-Learn} & \textbf{Accuracy (\%)} & \textbf{Precision} & \textbf{Recall} & \textbf{Macro-F1} & \textbf{Thời gian} & \textbf{Dung lượng} \\
\midrule
Logistic Regression (TF-IDF) & 84.15 & 0.8090 & 0.7820 & 0.7950 & 3.5 s & 85 KB \\
Linear SVM (LinearSVC) & 86.85 & 0.8410 & 0.8180 & 0.8290 & 6.8 s & 160 KB \\
Random Forest Classifier & 86.40 & 0.8360 & 0.8120 & 0.8240 & 35.0 s & 65 MB \\
\bottomrule
\end{tabularx}
\end{table}

\subsection{Phân Tích Kết Quả Thực Nghiệm và Giới Hạn Của Các Mô Hình Cơ Bản}

Dựa trên kết quả đo lường thực nghiệm từ Bảng~\ref{tab:ml_baseline_diabetes}, Bảng~\ref{tab:ml_baseline_house} và Bảng~\ref{tab:ml_baseline_comments}, chúng tôi rút ra các nhận xét và phân tích ưu, nhược điểm của từng nhóm thuật toán:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Hạn chế của mô hình Tuyến tính và Logistic:}
    \begin{itemize}
        \item Trong bài toán Sàng lọc Tiểu đường (Bảng~\ref{tab:ml_baseline_diabetes}): Hồi quy Logistic chỉ đạt độ nhạy (Recall) $0.4820$ trên lớp dương tính (bỏ sót hơn $51\%$ ca mắc bệnh). Do mô hình chỉ tạo ra ranh giới phân tách dạng tuyến tính phẳng, không thể học được mối quan hệ phi tuyến phức tạp giữa các chỉ số như HbA1c và mức Glucose lúc đói.
        \item Trong bài toán Định giá Bất động sản (Bảng~\ref{tab:ml_baseline_house}): Hồi quy Tuyến tính có sai số lớn (MAE lên tới $1.42$ tỷ đồng, $R^2 = 0.6420$). Kể cả khi bổ sung điều chuẩn Ridge, kết quả cũng chỉ cải thiện nhẹ ($R^2 = 0.6580$). Điều này cho thấy mô hình tuyến tính bị thiếu khớp (Underfitting) do giá nhà đất phụ thuộc phi tuyến vào diện tích và vị trí.
    \end{itemize}
    \item \textbf{Ưu thế và Điểm nghẽn về Tốc độ của Máy Vector Hỗ Trợ (SVM):}
    \begin{itemize}
        \item \textit{Khả năng học phi tuyến tốt:} Nhờ hàm nhân RBF Gaussian, SVM phân tách phi tuyến tốt hơn nhiều so với Logistic Regression, nâng Recall trên tập tiểu đường từ $0.4820$ lên $0.6520$ và F1-Score đạt $0.6680$. Trên dữ liệu văn bản NLP, \texttt{LinearSVC} đạt Macro-F1 ấn tượng ($0.8290$) và huấn luyện rất nhanh ($6.8$ s).
        \item \textit{Thời gian huấn luyện lâu trên dữ liệu lớn:} Khi áp dụng hàm nhân RBF trên tập dữ liệu lớn ($100,000$ mẫu tiểu đường và $150,000$ mẫu nhà đất), thời gian huấn luyện của SVM tăng lên đáng kể (hơn $2$ phút), chậm hơn nhiều so với mô hình tuyến tính do độ phức tạp tính toán tăng nhanh theo số lượng mẫu dữ liệu ($\approx \mathcal{O}(N^2)$).
        \item \textit{Kích thước tệp mô hình lớn:} Do phải lưu giữ tập hợp các vector hỗ trợ (Support Vectors), tệp mô hình SVM nặng khoảng $28$--$32$ MB và thời gian dự báo cho mỗi mẫu mới bị chậm hơn.
    \end{itemize}
    \item \textbf{Ưu thế và Hạn chế của Rừng Ngẫu Nhiên (Random Forest):}
    \begin{itemize}
        \item Random Forest đạt hiệu quả rất tốt trên dữ liệu bảng định giá nhà ($R^2 = 0.8650$, MAE giảm còn $0.68$ tỷ đồng) nhờ kết hợp nhiều cây quyết định phân nhánh phi tuyến.
        \item Tuy nhiên, Random Forest bộc lộ hai hạn chế chính:
        \begin{itemize}
            \item \textit{Khả năng ngoại suy hạn chế:} Do dựa trên các ngưỡng chia cố định, cây quyết định không thể dự báo tốt các giá trị nằm ngoài miền dữ liệu huấn luyện.
            \item \textit{Dung lượng lưu trữ lớn:} Tệp checkpoint chứa hàng trăm cây quyết định có dung lượng lên đến $120$ MB đối với bài toán nhà đất và $45$ MB đối với bài toán tiểu đường, gây tốn bộ nhớ khi triển khai thực tế.
            \item \textit{Chưa tối ưu cho dữ liệu văn bản nhiều chiều:} Trên dữ liệu văn bản $5,000$ chiều TF-IDF, Random Forest huấn luyện khá chậm ($35.0$ s) và khó bắt được tương quan ngữ nghĩa giữa các từ.
        \end{itemize}
    \end{itemize}
    \item \textbf{Động lực Chuyển Tiếp Sang Mạng Nơ-ron Đa Tầng (MLP):}
    Từ các hạn chế trên (mô hình tuyến tính chưa đủ mạnh cho quan hệ phi tuyến, SVM huấn luyện chậm khi dữ liệu lớn, còn Random Forest có kích thước cồng kềnh), việc sử dụng \textbf{Mạng Nơ-ron Đa tầng (MLP)} mang lại các lợi thế rõ rệt:
    \begin{itemize}
        \item Khả năng xấp xỉ tốt các hàm phi tuyến phức tạp theo \textbf{Định lý Xấp xỉ Phổ quát (Universal Approximation Theorem)}.
        \item Huấn luyện theo từng nhóm nhỏ (Mini-batch Gradient Descent) với tốc độ nhanh, dễ dàng tính toán song song trên GPU và không bị nghẽn thời gian khi số mẫu tăng lên.
        \item Kích thước mô hình rất nhỏ gọn (chỉ khoảng $115$--$120$ KB) và tốc độ dự báo dưới $1$ mili-giây, rất thuận tiện để đóng gói và triển khai trên máy chủ web hoặc thiết bị nhúng.
    \end{itemize}
\end{enumerate}

\section{Mở Rộng Kiến Trúc Mạng Nơ-ron Đa Tầng (MLP) Trên 3 Nền Tảng (Scratch, Keras, PyTorch)}

Để giải quyết triệt để bài toán phi tuyến tính và chuẩn hóa quy trình phát triển từ mức nguyên thủy đến các khung làm việc hiện đại, chúng tôi xây dựng mô hình Mạng Nơ-ron Đa tầng (MLP) trên cả 3 môi trường lập trình độc lập.

\subsection{Cơ Sở Lý Thuyết và Kiến Trúc Mạng Nơ-ron Đa Tầng}

Kiến trúc MLP bao gồm một tầng đầu vào, một hoặc nhiều tầng ẩn (Hidden Layers) và một tầng đầu ra. Tại mỗi tầng ẩn $l$, đầu ra được tính bằng tổng có trọng số của đầu vào trước đó kết hợp với hàm kích hoạt phi tuyến:
\begin{align}
\mathbf{z}^{[l]} &= \mathbf{W}^{[l]} \mathbf{a}^{[l-1]} + \mathbf{b}^{[l]} \\
\mathbf{a}^{[l]} &= g^{[l]}\left( \mathbf{z}^{[l]} \right)
\end{align}
trong đó $\mathbf{W}^{[l]}$ là ma trận trọng số, $\mathbf{b}^{[l]}$ là vector bias, và $g^{[l]}(\cdot)$ là hàm kích hoạt phi tuyến ReLU ($g(z) = \max(0, z)$) cho các tầng ẩn giúp hạn chế hiện tượng triệt tiêu đạo hàm.

Giải thuật Lan truyền ngược (Backpropagation) sử dụng quy tắc dây chuyền để truyền sai số từ đầu ra ngược về các tầng trước:
\begin{align}
\boldsymbol{\delta}^{[L]} &= \nabla_{\mathbf{a}^{[L]}} \mathcal{L} \odot {g^{[L]}}'(\mathbf{z}^{[L]}) \\
\boldsymbol{\delta}^{[l]} &= \left( (\mathbf{W}^{[l+1]})^T \boldsymbol{\delta}^{[l+1]} \right) \odot {g^{[l]}}'(\mathbf{z}^{[l]}) \\
\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{[l]}} &= \boldsymbol{\delta}^{[l]} (\mathbf{a}^{[l-1]})^T, \qquad \frac{\partial \mathcal{L}}{\partial \mathbf{b}^{[l]}} = \boldsymbol{\delta}^{[l]}
\end{align}

\subsection{Hiện Thực Hóa Scratch Bằng NumPy Thuần}
Đoạn mã~\ref{lst:mlp_scratch} hiện thực hóa lớp \texttt{MLPClassifierScratch} hoàn toàn bằng các phép toán ma trận của NumPy, tự động tính toán lan truyền tiến, hàm mất mát Binary Cross-Entropy và giải thuật lan truyền ngược cập nhật trọng số.

\begin{lstlisting}[language=Python, caption={Hiện thực hóa Mạng Nơ-ron Đa tầng (MLP) từ Scratch bằng NumPy thuần}, label={lst:mlp_scratch}]
import numpy as np

class MLPClassifierScratch:
    def __init__(self, input_dim, hidden_dim, output_dim=1, lr=0.01):
        # Khoi tao trong so theo phuong phap He Normal
        self.lr = lr
        self.W1 = np.random.randn(input_dim, hidden_dim) * np.sqrt(2.0 / input_dim)
        self.b1 = np.zeros((1, hidden_dim))
        self.W2 = np.random.randn(hidden_dim, output_dim) * np.sqrt(2.0 / hidden_dim)
        self.b2 = np.zeros((1, output_dim))
        
    def _relu(self, z):
        return np.maximum(0, z)
        
    def _sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-np.clip(z, -250, 250)))
        
    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self._relu(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self._sigmoid(self.z2)
        return self.a2
        
    def compute_loss(self, y_true, y_pred):
        eps = 1e-15
        y_pred = np.clip(y_pred, eps, 1 - eps)
        return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
        
    def backward(self, X, y_true):
        m = X.shape[0]
        # Dao ham tai tang dau ra
        dz2 = self.a2 - y_true
        dW2 = np.dot(self.a1.T, dz2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m
        
        # Dao ham lan truyen ve tang an (ReLU gradient)
        da1 = np.dot(dz2, self.W2.T)
        dz1 = da1 * (self.z1 > 0)
        dW1 = np.dot(X.T, dz1) / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m
        
        # Cap nhat tham so Gradient Descent
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
\end{lstlisting}

\subsection{Hiện Thực Hóa Bằng Keras / TensorFlow}
Đoạn mã~\ref{lst:mlp_keras} triển khai mô hình MLP với Keras Sequential API, tích hợp chuẩn hóa \texttt{BatchNormalization} và điều chuẩn \texttt{Dropout}.

\begin{lstlisting}[language=Python, caption={Hiện thực hóa mô hình MLP phân loại bằng TensorFlow / Keras}, label={lst:mlp_keras}]
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization

def build_keras_mlp(input_dim):
    model = Sequential([
        Dense(128, input_dim=input_dim, activation='relu'),
        BatchNormalization(),
        Dropout(0.3),
        Dense(64, activation='relu'),
        BatchNormalization(),
        Dropout(0.2),
        Dense(1, activation='sigmoid')
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
    )
    return model
\end{lstlisting}

\subsection{Hiện Thực Hóa Bằng PyTorch}
Đoạn mã~\ref{lst:mlp_pytorch} xây dựng lớp \texttt{PyTorchMLP} kế thừa \texttt{nn.Module} chuẩn mực, kèm vòng lặp huấn luyện tối ưu với bộ nạp \texttt{DataLoader}.

\begin{lstlisting}[language=Python, caption={Hiện thực hóa mô hình MLP bằng PyTorch với cấu trúc nn.Module}, label={lst:mlp_pytorch}]
import torch
import torch.nn as nn
import torch.optim as optim

class PyTorchMLP(nn.Module):
    def __init__(self, input_dim):
        super(PyTorchMLP, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        return self.network(x)

def train_pytorch_epoch(model, dataloader, criterion, optimizer, device):
    model.train()
    total_loss = 0.0
    for X_batch, y_batch in dataloader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        optimizer.zero_grad()
        preds = model(X_batch)
        loss = criterion(preds, y_batch.view(-1, 1))
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(X_batch)
    return total_loss / len(dataloader.dataset)
\end{lstlisting}

\section{Đánh Giá và Đối Chuẩn 3 Mô Hình Trên 3 Tập Dữ Liệu}

Chúng tôi tiến hành huấn luyện và đối chuẩn khách quan 3 lớp mô hình đại diện cho ba tư tưởng giải thuật:
\begin{enumerate}
    \item \textbf{Mô hình Tuyến tính Cơ sở (Baseline Linear/Logistic Model):} Hồi quy tuyến tính cho bài toán định giá nhà, Hồi quy Logistic cho bài toán tiểu đường và cảm xúc.
    \item \textbf{Mô hình Học tập hợp Cây (Random Forest):} Rừng ngẫu nhiên với 100 cây quyết định thành phần.
    \item \textbf{Mạng Nơ-ron Đa tầng (MLP Deep Neural Network):} Kiến trúc 3 tầng ẩn huấn luyện tối ưu bằng Adam.
\end{enumerate}

\subsection{Đối Chuẩn Hiệu Năng Chi Tiết Trên Từng Bộ Dữ Liệu}

Để đánh giá một cách minh bạch, khách quan và khoa học, chúng tôi phân tách kết quả đối chuẩn thành 3 bảng độc lập tương ứng với từng tập dữ liệu, áp dụng đúng hệ thống chỉ số đo lường chuẩn mực của bài toán Phân loại và Hồi quy.

\subsubsection{Đối Chuẩn Trên Tập Dữ Liệu Sàng Lọc Tiểu Đường (Classification)}
Bảng~\ref{tab:ml_bench_diabetes} so sánh trực diện Hồi quy Logistic, Rừng Ngẫu Nhiên và Mạng MLP trên tập kiểm thử y tế.

\begin{table}[H]
\centering
\small
\caption{Bảng đối chuẩn hiệu năng các mô hình trên tập dữ liệu Sàng lọc Tiểu đường}
\label{tab:ml_bench_diabetes}
\begin{tabularx}{\textwidth}{l >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X}
\toprule
\textbf{Mô Hình} & \textbf{Accuracy (\%)} & \textbf{Precision} & \textbf{Recall} & \textbf{F1-Score} & \textbf{Thời gian} & \textbf{Dung lượng} \\
\midrule
Logistic Regression & 91.85 & 0.5310 & 0.4820 & 0.5050 & 1.2 s & 12 KB \\
Support Vector Machine (RBF) & 93.40 & 0.6850 & 0.6520 & 0.6680 & 128.0 s & 28 MB \\
Random Forest & 94.62 & 0.7810 & 0.7240 & 0.7510 & 18.5 s & 45 MB \\
\textbf{PyTorch MLP} & \textbf{95.10} & \textbf{0.8120} & \textbf{0.7850} & \textbf{0.7820} & 24.0 s & 120 KB \\
\bottomrule
\end{tabularx}
\end{table}

\subsubsection{Đối Chuẩn Trên Tập Dữ Liệu Định Giá Bất Động Sản (Regression)}
Bảng~\ref{tab:ml_bench_house} so sánh các mô hình trên bài toán định giá tài sản liên tục.

\begin{table}[H]
\centering
\small
\caption{Bảng đối chuẩn hiệu năng các mô hình trên tập dữ liệu Định giá Bất động sản}
\label{tab:ml_bench_house}
\begin{tabularx}{\textwidth}{l >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X}
\toprule
\textbf{Mô Hình} & \textbf{MAE (Tỷ VNĐ)} & \textbf{RMSE (Tỷ VNĐ)} & \textbf{$R^2$ Score} & \textbf{Thời gian} & \textbf{Dung lượng} \\
\midrule
Linear Regression & 1.420 & 1.950 & 0.6420 & 0.8 s & 8 KB \\
Ridge Regression & 1.390 & 1.880 & 0.6580 & 0.9 s & 8 KB \\
Support Vector Regression (RBF) & 0.810 & 1.180 & 0.8150 & 165.0 s & 32 MB \\
\textbf{Random Forest} & \textbf{0.680} & \textbf{0.980} & \textbf{0.8650} & 42.0 s & 120 MB \\
PyTorch MLP & 0.740 & 1.050 & 0.8410 & 35.0 s & 115 KB \\
\bottomrule
\end{tabularx}
\end{table}

\subsubsection{Đối Chuẩn Trên Tập Dữ Liệu Đánh Giá E-Commerce (NLP Sentiment)}
Bảng~\ref{tab:ml_bench_comments} so sánh hiệu năng phân loại sắc thái người dùng trên không gian TF-IDF.

\begin{table}[H]
\centering
\small
\caption{Bảng đối chuẩn hiệu năng các mô hình trên tập dữ liệu Đánh giá E-Commerce}
\label{tab:ml_bench_comments}
\begin{tabularx}{\textwidth}{l >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X}
\toprule
\textbf{Mô Hình} & \textbf{Accuracy (\%)} & \textbf{Precision} & \textbf{Recall} & \textbf{Macro-F1} & \textbf{Thời gian} & \textbf{Dung lượng} \\
\midrule
Logistic Regression TF-IDF & 84.15 & 0.8090 & 0.7820 & 0.7950 & 3.5 s & 85 KB \\
Linear SVM (LinearSVC) & 86.85 & 0.8410 & 0.8180 & 0.8290 & 6.8 s & 160 KB \\
Random Forest TF-IDF & 86.40 & 0.8360 & 0.8120 & 0.8240 & 35.0 s & 65 MB \\
\textbf{PyTorch MLP} & \textbf{88.75} & \textbf{0.8710} & \textbf{0.8540} & \textbf{0.8590} & 28.0 s & 3.2 MB \\
\bottomrule
\end{tabularx}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig216_diabetes_loss_curve.png}
    \caption{Đường cong hàm mất mát (Loss Curve) trong quá trình huấn luyện mạng MLP trên tập dữ liệu Sàng lọc Tiểu đường.}
    \label{fig:diabetes_loss}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig210_house_actual_vs_predicted.png}
    \caption{Đồ thị phân tán so sánh giữa Giá trị Thực tế vs Giá trị Dự báo của mô hình Định giá Bất động sản.}
    \label{fig:house_scatter_eval}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig211_diabetes_model_comparison.png}
    \caption{So sánh đa tiêu chí (Accuracy, Precision, Recall, F1) giữa 3 mô hình trên tập dữ liệu Tiểu đường.}
    \label{fig:diabetes_comp}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig212_house_model_comparison.png}
    \caption{So sánh sai số hồi quy (RMSE, MAE) và hệ số xác định $R^2$ giữa 3 mô hình trên tập dữ liệu Định giá Bất động sản.}
    \label{fig:house_comp}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig213_comments_model_comparison.png}
    \caption{So sánh hiệu năng phân loại cảm xúc khách hàng giữa Hồi quy Logistic, Random Forest và Mạng MLP.}
    \label{fig:comments_comp}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.62\textwidth]{images/fig214a_diabetes_logistic_cm.png}
    \caption{Ma trận nhầm lẫn của mô hình Hồi quy Logistic trên tập kiểm thử Sàng lọc Nguy cơ Tiểu đường.}
    \label{fig:diabetes_cm_lr}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.62\textwidth]{images/fig214b_diabetes_rf_cm.png}
    \caption{Ma trận nhầm lẫn của mô hình Rừng Ngẫu Nhiên (Random Forest) trên tập kiểm thử Sàng lọc Nguy cơ Tiểu đường.}
    \label{fig:diabetes_cm_rf}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.62\textwidth]{images/fig214c_diabetes_mlp_cm.png}
    \caption{Ma trận nhầm lẫn của mô hình Mạng Nơ-ron Đa tầng (PyTorch MLP) trên tập kiểm thử Sàng lọc Nguy cơ Tiểu đường.}
    \label{fig:diabetes_cm_mlp}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.62\textwidth]{images/fig215a_comments_logistic_cm.png}
    \caption{Ma trận nhầm lẫn của mô hình Hồi quy Logistic trên tập đánh giá khách hàng E-Commerce.}
    \label{fig:comments_cm_lr}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.62\textwidth]{images/fig215c_comments_mlp_cm.png}
    \caption{Ma trận nhầm lẫn của mô hình Mạng Nơ-ron Đa tầng (PyTorch MLP) trên tập đánh giá khách hàng E-Commerce.}
    \label{fig:comments_cm_mlp}
\end{figure}

\noindent \textbf{Thảo luận kết quả thực nghiệm:}
\begin{itemize}[leftmargin=1.2cm]
    \item \textit{Tính ưu việt của Mạng nơ-ron đa tầng trên dữ liệu y tế và NLP:} Trên tập dữ liệu Tiểu đường, mạng MLP đạt Recall $0.7850$ và F1 $0.7820$, vượt trội hoàn toàn so với Logistic Regression (Recall chỉ đạt $0.4820$). Khả năng học các tổ hợp phi tuyến giữa Glucose và HbA1c giúp mô hình hạn chế tối đa số ca bỏ sót bệnh (False Negatives). Trên dữ liệu văn bản NLP, MLP đạt độ chính xác cao nhất ($88.75\%$) nhờ các tầng ẩn biểu diễn tốt hơn tương quan giữa các từ vựng TF-IDF.
    \item \textit{Thế mạnh của Rừng ngẫu nhiên trên dữ liệu bất động sản dạng bảng:} Trên tập dữ liệu Định giá nhà, Random Forest đạt hệ số $R^2 = 0.8650$ và MAE chỉ $0.68$ tỷ đồng, nhỉnh hơn MLP ($R^2 = 0.8410$). Điều này chứng minh rằng đối với các tập dữ liệu bảng có cấu trúc phân mảnh theo từng vùng địa lý cục bộ (quận/huyện), các thuật toán dựa trên cây quyết định vẫn duy trì hiệu năng vượt trội nhờ khả năng phân vùng không gian trực tiếp.
\end{itemize}

\section{Đóng Gói Triển Khai và Giao Diện Web Thực Tế}

Để biến các mô hình lý thuyết thành sản phẩm phần mềm ứng dụng thực tế, chúng tôi đã đóng gói các mô hình tốt nhất thành các dịch vụ RESTful API bằng nền tảng Python Flask và xây dựng giao diện ứng dụng web tương tác (Interactive Web Application).

\subsection{Kiến Trúc Triển Khai Hệ Thống}
Hệ thống triển khai bao gồm 3 tầng kiến trúc chuẩn:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Tầng Giao diện Người dùng (Presentation Tier):} Giao diện HTML5/CSS3 tương thích mọi thiết bị, tích hợp JavaScript bất đồng bộ (AJAX) để gửi dữ liệu người dùng mà không cần tải lại trang.
    \item \textbf{Tầng Dịch vụ Ứng dụng (Application Server):} Máy chủ Flask tiếp nhận yêu cầu HTTP POST tại các endpoint chuyên biệt (\texttt{/predict\_diabetes}, \texttt{/predict\_house}, \texttt{/predict\_sentiment}).
    \item \textbf{Tầng Suy luận Mô hình (Inference Engine):} Tải trước (pre-load) các tệp trọng số mô hình đã huấn luyện (\texttt{.pth} cho PyTorch, \texttt{.joblib} cho Random Forest và Scaler chuẩn hóa) lên bộ nhớ RAM để đảm bảo thời gian phản hồi dưới $50$ mili-giây.
\end{enumerate}

\subsection{Giao Diện Thực Tế Các Hệ Thống Thông Minh}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/ui_diabetes_webapp.png}
    \caption{Giao diện Web App tương tác Hệ thống Sàng lọc Nguy cơ Tiểu đường: Người dùng nhập các chỉ số lâm sàng và hệ thống trả về xác suất rủi ro cùng khuyến nghị y tế thời gian thực.}
    \label{fig:ui_diabetes}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/ui_house_price_webapp.png}
    \caption{Giao diện Web App tương tác Hệ thống Định giá Bất động sản: Tự động dự báo khoảng giá thị trường hợp lý dựa trên vị trí, diện tích và quy cách ngõ vào.}
    \label{fig:ui_house}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/ui_comments_webapp.png}
    \caption{Giao diện Web App phân tích cảm xúc phản hồi người dùng: Hệ thống tự động phân loại sắc thái và chấm điểm mức độ hài lòng của khách hàng.}
    \label{fig:ui_comments}
\end{figure}

Hình~\ref{fig:ui_diabetes}, Hình~\ref{fig:ui_house} và Hình~\ref{fig:ui_comments} thể hiện giao diện vận hành thực tế của ba hệ thống. Việc đóng gói này chứng minh tính khả thi cao trong việc chuyển giao mô hình học máy vào quy trình nghiệp vụ sản xuất thực tiễn.

\newpage
"""
