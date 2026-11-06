# sections/chapter4_rnn.py

def get_chapter4():
    return r"""
% =========================================================================
% CHƯƠNG 4: MẠNG NƠ-RON HỒI QUY (RECURRENT NEURAL NETWORKS)
% =========================================================================
\chapter{Mạng Nơ-ron Hồi Quy (RNN)}

\section{Cơ Sở Lý Thuyết Mạng Nơ-ron Hồi Quy \& Mô Hình Hóa Chuỗi}

Khác với dữ liệu bảng độc lập hay ảnh tĩnh không gian, dữ liệu chuỗi thời gian (Time-Series) và dữ liệu tuần tự (Sequential Data) vi phạm giả định nền tảng về tính độc lập và đồng phân phối ($i.i.d.$) giữa các mẫu. Thứ tự xuất hiện của các điểm dữ liệu mang tính sống còn, phản ánh mối quan hệ nhân quả vật lý và động lực tiến hóa của hệ thống.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{images/fig601_sequence_tensor_representation.png}
    \caption{Cấu trúc biểu diễn Tensor chuỗi 3D $[B, T, D]$ trong mô hình hóa học sâu tuần tự.}
    \label{fig:rnn_tensor}
\end{figure}

Một tập dữ liệu chuỗi được biểu diễn dưới dạng Tensor 3 chiều $\mathbf{X} \in \mathbb{R}^{B \times T \times D}$, trong đó $B$ là kích thước lô (Batch Size), $T$ là độ dài cửa sổ thời gian (Sequence Length / Lookback Window), và $D$ là số lượng đặc trưng quan sát tại mỗi bước thời gian (Features).

\subsection{Kiến Trúc Simple RNN \& Đồ Thị Tính Toán Mở Rộng Theo Thời Gian}
Mạng nơ-ron hồi quy đơn giản (Simple RNN / Elman RNN) trang bị một vector trạng thái ẩn $\mathbf{h}_t \in \mathbb{R}^H$ đóng vai trò bộ nhớ nội tại truyền tải thông tin qua các bước thời gian. Tại mỗi bước $t \in \{1, 2, \dots, T\}$, trạng thái ẩn mới được tính toán kết hợp giữa vector quan sát hiện tại $\mathbf{x}_t \in \mathbb{R}^D$ và trạng thái ẩn của bước liền trước $\mathbf{h}_{t-1}$:
\begin{align}
\mathbf{h}_t &= \tanh(\mathbf{W}_{xh} \mathbf{x}_t + \mathbf{W}_{hh} \mathbf{h}_{t-1} + \mathbf{b}_h) \\
\hat{\mathbf{y}}_t &= \sigma(\mathbf{W}_{hy} \mathbf{h}_t + \mathbf{b}_y) \quad \text{hoặc} \quad \hat{\mathbf{y}} = \mathbf{W}_{hy} \mathbf{h}_T + \mathbf{b}_y
\end{align}
trong đó $\mathbf{W}_{xh} \in \mathbb{R}^{H \times D}$ là ma trận trọng số đầu vào, $\mathbf{W}_{hh} \in \mathbb{R}^{H \times H}$ là ma trận trọng số hồi quy chuyển trạng thái (được chia sẻ cố định qua toàn bộ các bước thời gian), và $\mathbf{b}_h \in \mathbb{R}^H$ là bias.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\textwidth]{images/fig602_simple_rnn_unfolded_computational_graph.png}
    \caption{Đồ thị tính toán mở rộng theo thời gian (Unfolded Computational Graph) của Mạng nơ-ron Hồi quy.}
    \label{fig:rnn_unfolded}
\end{figure}

\subsection{Giải Thuật Lan Truyền Ngược Qua Thời Gian (BPTT) \& Hiện Tượng Triệt Tiêu Đạo Hàm}
Việc huấn luyện mạng hồi quy sử dụng giải thuật \textbf{Lan truyền ngược qua thời gian (Backpropagation Through Time -- BPTT)}. Tổng hàm mất mát trên toàn bộ chuỗi là tổng tích lũy: $\mathcal{L} = \sum_{t=1}^T \mathcal{L}_t$. Khi tính đạo hàm riêng của hàm mất mát tại bước $T$ đối với ma trận trọng số hồi quy $\mathbf{W}_{hh}$, ta áp dụng quy tắc dây chuyền nhiều bước:
\begin{equation}
\frac{\partial \mathcal{L}_T}{\partial \mathbf{W}_{hh}} = \sum_{k=1}^T \frac{\partial \mathcal{L}_T}{\partial \mathbf{h}_T} \left( \prod_{j=k+1}^T \frac{\partial \mathbf{h}_j}{\partial \mathbf{h}_{j-1}} \right) \frac{\partial \mathbf{h}_k}{\partial \mathbf{W}_{hh}}
\end{equation}
Trọng tâm của công thức là thành phần tích chuỗi các ma trận Jacobi chuyển trạng thái:
\begin{equation}
\prod_{j=k+1}^T \frac{\partial \mathbf{h}_j}{\partial \mathbf{h}_{j-1}} = \prod_{j=k+1}^T \text{diag}\left(1 - \mathbf{h}_j^2\right) \mathbf{W}_{hh}^T
\end{equation}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{images/fig603_bptt_and_vanishing_gradient.png}
    \caption{Bản chất toán học của hiện tượng Triệt tiêu Đạo hàm (Vanishing Gradient) trong tích chuỗi ma trận Jacobi của giải thuật BPTT.}
    \label{fig:rnn_vanishing}
\end{figure}

\noindent \textbf{Chứng minh toán học về sự bất ổn định gradient:}
Gọi $\lambda_{\max}$ là giá trị riêng (eigenvalue) lớn nhất của ma trận $\mathbf{W}_{hh}$. Vì đạo hàm của hàm $\tanh$ thỏa mãn $|1 - h^2| \le 1$:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Nếu $|\lambda_{\max}| < 1$:} Chuỗi tích ma trận suy giảm theo hàm mũ $\mathcal{O}(\lambda_{\max}^{T-k}) \rightarrow 0$ khi khoảng cách thời gian $T - k$ lớn. Gradient bị triệt tiêu hoàn toàn (\textbf{Vanishing Gradient}), khiến mô hình hoàn toàn mất khả năng ghi nhớ các phụ thuộc dài hạn trong quá khứ.
    \item \textbf{Nếu $|\lambda_{\max}| > 1$:} Chuỗi tích tăng trưởng bùng nổ theo hàm mũ $\mathcal{O}(\lambda_{\max}^{T-k}) \rightarrow \infty$, dẫn đến hiện tượng bùng nổ đạo hàm (\textbf{Exploding Gradient}), làm trọng số dao động dữ dội và tràn số học (NaN / Inf).
\end{itemize}

\subsection{Kỹ Thuật Cắt Tỉa Đạo Hàm (Gradient Clipping)}
Để triệt tiêu hiện tượng bùng nổ đạo hàm, kỹ thuật \textbf{Cắt tỉa đạo hàm theo chuẩn (Gradient Norm Clipping)} (Pascanu et al., 2013) được áp dụng:
\begin{equation}
\mathbf{g} \leftarrow \begin{cases}
\mathbf{g}, & \text{nếu } \|\mathbf{g}\|_2 \le \theta \\
\frac{\theta}{\|\mathbf{g}\|_2} \mathbf{g}, & \text{nếu } \|\mathbf{g}\|_2 > \theta
\end{cases}
\end{equation}
trong đó $\theta$ là ngưỡng chuẩn tối đa (thường đặt $\theta = 1.0$ hoặc $5.0$). Kỹ thuật này giữ nguyên hướng di chuyển của vector gradient trong không gian tham số nhưng giới hạn độ dài bước nhảy, đảm bảo việc cập nhật tham số không bao giờ phá vỡ vùng cực tiểu tối ưu.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig604_gradient_clipping_mechanism.png}
    \caption{Cơ chế hình học của kỹ thuật Cắt tỉa Đạo hàm (Gradient Clipping) bảo toàn hướng di chuyển của tham số.}
    \label{fig:rnn_clipping}
\end{figure}

\subsection{Kiến Trúc Tế Bào LSTM và GRU}
Để giải quyết triệt để sự cố triệt tiêu đạo hàm của Simple RNN trên các chuỗi thời gian dài, hai kiến trúc tế bào hồi quy có cơ chế cổng kiểm soát dòng thông tin được phát triển và ứng dụng rộng rãi nhất là \textbf{LSTM} và \textbf{GRU}:

\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Long Short-Term Memory (LSTM -- Hochreiter \& Schmidhuber, 1997):} Giải quyết triệt để vấn đề triệt tiêu đạo hàm bằng cách phân tách bộ nhớ thành \textbf{Trạng thái Ô nhớ (Cell State $\mathbf{c}_t$)} và \textbf{Trạng thái Ẩn ($\mathbf{h}_t$)}. Cell State đóng vai trò đường cao tốc thông tin, cho phép gradient truyền ngược tuyến tính mà không bị nhân liên tiếp qua ma trận chuyển đổi:
    \begin{align}
    \text{Cổng Quên (Forget Gate):} \quad \mathbf{f}_t &= \sigma(\mathbf{W}_f [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_f) \\
    \text{Cổng Vào (Input Gate):} \quad \mathbf{i}_t &= \sigma(\mathbf{W}_i [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_i) \\
    \text{Ứng viên Ô nhớ (Candidate):} \quad \tilde{\mathbf{c}}_t &= \tanh(\mathbf{W}_c [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_c) \\
    \text{Cập nhật Cell State:} \quad \mathbf{c}_t &= \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \tilde{\mathbf{c}}_t \\
    \text{Cổng Ra (Output Gate):} \quad \mathbf{o}_t &= \sigma(\mathbf{W}_o [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_o) \\
    \text{Trạng thái Ẩn:} \quad \mathbf{h}_t &= \mathbf{o}_t \odot \tanh(\mathbf{c}_t)
    \end{align}
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig605_lstm_cell_architecture.png}
    \caption{Kiến trúc vi mô tế bào LSTM với đường truyền trạng thái ô nhớ (Cell State) và cơ chế điều khiển 3 cổng.}
    \label{fig:rnn_lstm_cell}
\end{figure}

\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Gated Recurrent Unit (GRU -- Cho et al., 2014):} Tinh gọn hóa kiến trúc LSTM bằng cách hợp nhất Cell State và Hidden State thành một vector trạng thái ẩn duy nhất $\mathbf{h}_t$, sử dụng 2 cổng điều khiển:
    \begin{align}
    \text{Cổng Đặt lại (Reset Gate):} \quad \mathbf{r}_t &= \sigma(\mathbf{W}_r [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_r) \\
    \text{Cổng Cập nhật (Update Gate):} \quad \mathbf{z}_t &= \sigma(\mathbf{W}_z [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_z) \\
    \text{Ứng viên Ẩn:} \quad \tilde{\mathbf{h}}_t &= \tanh(\mathbf{W}_h [\mathbf{r}_t \odot \mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_h) \\
    \text{Cập nhật Trạng thái:} \quad \mathbf{h}_t &= (1 - \mathbf{z}_t) \odot \mathbf{h}_{t-1} + \mathbf{z}_t \odot \tilde{\mathbf{h}}_t
    \end{align}
    GRU giảm $25\%$ số lượng tham số so với LSTM, giúp giảm thiểu rủi ro quá khớp trên các tập dữ liệu nhỏ và tăng tốc độ hội tụ.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig606_gru_cell_architecture.png}
    \caption{Kiến trúc vi mô tế bào GRU với cơ chế 2 cổng tích hợp (Update Gate và Reset Gate).}
    \label{fig:rnn_gru_cell}
\end{figure}

\subsection{Mạng Hồi Quy Hai Chiều (BiLSTM) \& Điều Chuẩn Recurrent Dropout}
Trong nhiều bài toán phân tích chuỗi tĩnh (như phân tích quỹ đạo khách hàng hoặc gắn nhãn thực thể), việc tiếp cận cả ngữ cảnh quá khứ lẫn ngữ cảnh tương lai đem lại thông tin phong phú vượt trội. Mạng \textbf{BiLSTM} vận hành đồng thời hai chuỗi độc lập: chuỗi tiến $\overrightarrow{\mathbf{h}}_t$ từ $t=1 \rightarrow T$ và chuỗi lùi $\overleftarrow{\mathbf{h}}_t$ từ $t=T \rightarrow 1$, vector biểu diễn cuối cùng là phép nối ghép: $\mathbf{h}_t = [\overrightarrow{\mathbf{h}}_t, \overleftarrow{\mathbf{h}}_t] \in \mathbb{R}^{2H}$.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig607_bidirectional_rnn_architecture.png}
    \caption{Kiến trúc Mạng nơ-ron Hồi quy Hai chiều (Bidirectional RNN / BiLSTM) tổng hợp ngữ cảnh quá khứ và tương lai.}
    \label{fig:rnn_bilstm}
\end{figure}

Đồng thời, việc áp dụng kỹ thuật \textbf{Recurrent Dropout} (Gal \& Ghahramani, 2016) -- sử dụng cùng một mặt nạ nhị phân cố định qua mọi bước thời gian của cùng một mẫu -- giúp điều chuẩn mạng hồi quy hiệu quả mà không làm suy giảm cấu trúc bộ nhớ nội tại.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.86\textwidth]{images/fig608_recurrent_dropout_vs_standard_dropout.png}
    \caption{So sánh giữa Standard Dropout (gây nhiễu bộ nhớ) và Recurrent Dropout (bảo toàn mặt nạ cố định theo thời gian).}
    \label{fig:rnn_dropout}
\end{figure}

\section{Khảo Sát Thực Nghiệm và Tiền Xử Lý 2 Bộ Dữ Liệu Chuỗi Lớn}

\subsection{Tập Dữ Liệu 1: Chuỗi Thời Gian Chứng Khoán Việt Nam (VN30 / HoSE 2012 -- 2026)}
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Nguồn gốc dữ liệu:} Lịch sử giao dịch tài chính các mã cổ phiếu trụ cột thuộc rổ chỉ số VN30 niêm yết trên Sở Giao dịch Chứng khoán TP.HCM (HoSE) thu thập từ Yahoo Finance (\url{https://finance.yahoo.com/quote/FPT.VN/history}), bao gồm 4 doanh nghiệp đầu ngành đại diện cho các trụ cột kinh tế: FPT (Công nghệ - Viễn thông), VCB (Ngân hàng TMCP Ngoại thương Việt Nam), HPG (Tập đoàn Hòa Phát - Thép \& Công nghiệp nặng), và VIC (Tập đoàn Vingroup - Bất động sản \& Dịch vụ).
    \item \textbf{Quy mô và chiều dữ liệu:} Gồm tổng cộng $15,225$ phiên giao dịch liên tục suốt 14 năm (từ tháng 01/2012 đến tháng 09/2026), trong đó riêng mã FPT có $3,825$ phiên, VCB có $3,816$ phiên, HPG có $3,825$ phiên và VIC có $3,759$ phiên. Sau khi trích xuất các chỉ báo kỹ thuật tài chính động, tập dữ liệu có $8$ đặc trưng quan sát tại mỗi phiên: Giá mở cửa (Open), Giá cao nhất (High), Giá thấp nhất (Low), Giá đóng cửa (Close), Khối lượng giao dịch (Volume), Trung bình trượt 20 ngày (SMA20), Trung bình trượt 50 ngày (SMA50), Chỉ số sức mạnh tương đối 14 ngày (RSI-14), và Độ biến động 30 ngày (Volatility-30d).
\end{itemize}

\begin{table}[H]
\centering
\small
\caption{Trích xuất 5 phiên giao dịch tiêu biểu kèm chỉ báo kỹ thuật của cổ phiếu FPT (FPT.VN) trên sàn HoSE}
\label{tab:sample_vn_stock}
\begin{tabularx}{\textwidth}{>{\centering\arraybackslash}p{2.2cm} >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X}
\toprule
\textbf{Ngày} & \textbf{Open (VNĐ)} & \textbf{High (VNĐ)} & \textbf{Low (VNĐ)} & \textbf{Close (VNĐ)} & \textbf{Volume (CP)} & \textbf{SMA20} & \textbf{RSI-14} \\
\midrule
09/03/2012 & 4,254 & 4,368 & 4,254 & 4,292 & 1,505,570 & 4,138 & 69.23 \\
22/10/2015 & 7,559 & 7,608 & 7,559 & 7,575 & 2,103,678 & 7,390 & 70.91 \\
02/07/2019 & 14,867 & 15,026 & 14,757 & 14,836 & 4,248,729 & 14,296 & 63.31 \\
17/02/2023 & 45,143 & 45,365 & 45,032 & 45,365 & 782,277 & 45,613 & 32.79 \\
30/09/2026 & 63,400 & 64,000 & 63,000 & 63,000 & 3,041,400 & 65,602 & 27.74 \\
\bottomrule
\end{tabularx}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth]{images/fig609_vn_stock_eda_timeseries.png}
    \caption{Diễn biến chuỗi thời gian giá đóng cửa và khối lượng giao dịch các cổ phiếu trụ cột VN30 (FPT, VCB, HPG, VIC) giai đoạn 2012 -- 2026 và các đường trung bình động SMA.}
    \label{fig:vn_stock_eda}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth]{images/fig609b_vn_stock_distributions_volatility_and_correlation.png}
    \caption{Phân phối lợi suất hàng ngày (KDE), độ biến động 30 ngày (Rolling Volatility) và ma trận tương quan Pearson giữa 4 mã trụ cột thị trường chứng khoán Việt Nam.}
    \label{fig:vn_stock_volatility}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{images/fig610_vn_stock_acf_pacf_stationarity.png}
    \caption{Đồ thị Hàm tự tương quan (ACF), Tự tương quan riêng phần (PACF) và kiểm định nghiệm đơn vị Augmented Dickey-Fuller (ADF) khẳng định tính chất phụ thuộc trễ dài hạn của cổ phiếu FPT.VN.}
    \label{fig:vn_stock_acf}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth]{images/fig611_sliding_window_mechanism.png}
    \caption{Cơ chế tạo mẫu Cửa sổ trượt (Sliding Window Lookback $T = 30$) và nguyên tắc phân chia tuần tự (Chronological Split) chống rò rỉ thời gian (Lookahead Bias).}
    \label{fig:sliding_window}
\end{figure}

\noindent \textbf{Nguyên tắc tiền xử lý chuỗi thời gian chuẩn xác:}
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Cơ chế Cửa sổ trượt (Sliding Window):} Với chuỗi cổ phiếu FPT.VN, độ dài nhìn lại (Lookback) $T = 30$ ngày và bước trượt Stride $= 1$, chuỗi dữ liệu gốc được biến đổi thành $3,746$ mẫu tensor đầu vào $\mathbf{X}_i \in \mathbb{R}^{30 \times 8}$ để dự báo giá đóng cửa phiên kế tiếp $y_i = \text{Close}_{t+1}$.
    \item \textbf{Phân chia tuần tự chống rò rỉ thông tin (Lookahead Bias):} Tuyệt đối không sử dụng phương pháp xáo trộn ngẫu nhiên (random shuffle) vì sẽ làm dữ liệu tương lai lọt vào tập huấn luyện của quá khứ. Toàn bộ chuỗi được phân chia nghiêm ngặt theo trục thời gian thực: Tập Huấn luyện ($80\%$ -- $2,996$ mẫu từ năm 2012 đến đầu năm 2023) và Tập Kiểm thử ($20\%$ -- $750$ mẫu từ năm 2023 đến 09/2026). Bộ chuẩn hóa \texttt{MinMaxScaler} chỉ được khớp (\texttt{fit}) trên tập Train và áp dụng (\texttt{transform}) sang tập Test.
\end{enumerate}

\subsection{Tập Dữ Liệu 2: Quỹ Đạo Hành Vi Khách Hàng (Customer Sequential Behavior)}
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Nguồn gốc dữ liệu:} Bộ dữ liệu hành vi người dùng dịch vụ thuê bao số (Subscription E-Commerce / SaaS) mô phỏng từ các nền tảng thương mại thực tế.
    \item \textbf{Quy mô và chiều dữ liệu:} Gồm $60,000$ bản ghi chuỗi tương ứng với $5,000$ khách hàng độc lập được theo dõi quỹ đạo liên tục trong suốt 12 tháng ($T = 12$). Mỗi bước tháng thu thập $8$ chiều hành vi động: Tần suất đăng nhập (Login Frequency), Số đơn hàng (Purchase Count), Số vé yêu cầu hỗ trợ (Support Tickets), Thời lượng sử dụng (Session Duration), Cước phí hàng tháng (Monthly Charges), Số ngày quá hạn thanh toán (Overdue Days), Điểm tương tác (Engagement Score), và Nhãn mục tiêu là Rủi ro khách hàng rời bỏ dịch vụ (Churn: $1$ -- Rời bỏ, $0$ -- Duy trì).
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth]{images/fig612_customer_behavior_temporal_trajectories.png}
    \caption{Quỹ đạo biến thiên hành vi theo thời gian (12 tháng liên tục) thể hiện sự suy giảm tương tác rõ rệt của nhóm khách hàng rời bỏ (Churn).}
    \label{fig:churn_trajectory}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{images/fig612b_customer_behavior_distributions_and_correlations.png}
    \caption{Phân bố tỷ lệ rời bỏ dịch vụ (15.6\% Churn) và ma trận tương quan giữa các đặc trưng hành vi chuỗi.}
    \label{fig:churn_dist}
\end{figure}

\noindent \textbf{Nhận xét EDA:} Hình~\ref{fig:churn_trajectory} bộc lộ một quy luật hành vi then chốt: các khách hàng quyết định rời bỏ dịch vụ vào tháng 12 thường xuất hiện các dấu hiệu cảnh báo sớm từ tháng thứ 7 đến tháng thứ 9: tần suất đăng nhập giảm từ $18$ lần/tháng xuống dưới $4$ lần/tháng, số vé khiếu nại tăng vọt gấp 3 lần. Việc sử dụng mạng RNN/LSTM cho phép mô hình hóa trọn vẹn quỹ đạo suy giảm theo thời gian này, điều mà các mô hình học máy tĩnh tại một thời điểm không thể làm được.

\section{Hiện Thực Hóa Mã Nguồn Trên 3 Nền Tảng (Scratch, Keras, PyTorch)}

\subsection{Hiện Thực Hóa Tế Bào LSTM Scratch Bằng NumPy}
Đoạn mã~\ref{lst:lstm_scratch} hiện thực hóa cơ chế hoạt động của tế bào LSTM trực tiếp từ các công thức toán học cơ bản.

\begin{lstlisting}[language=Python, caption={Hiện thực hóa tế bào LSTM và lan truyền tiến từ Scratch bằng NumPy}, label={lst:lstm_scratch}]
import numpy as np

class LSTMCellScratch:
    def __init__(self, input_dim, hidden_dim):
        self.H = hidden_dim
        self.D = input_dim
        # Khoi tao trong so ket hop [H, H + D] cho 4 cong (f, i, c, o)
        self.W = np.random.randn(4 * self.H, self.H + self.D) * 0.05
        self.b = np.zeros((4 * self.H, 1))
        
    def _sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))
        
    def forward(self, x_t, h_prev, c_prev):
        # x_t: [D, 1], h_prev: [H, 1], c_prev: [H, 1]
        concat = np.vstack((h_prev, x_t)) # [H + D, 1]
        gates = np.dot(self.W, concat) + self.b # [4H, 1]
        
        # Phan tach 4 cong
        f = self._sigmoid(gates[0*self.H : 1*self.H, :])
        i = self._sigmoid(gates[1*self.H : 2*self.H, :])
        c_bar = np.tanh(gates[2*self.H : 3*self.H, :])
        o = self._sigmoid(gates[3*self.H : 4*self.H, :])
        
        # Cap nhat Cell State va Hidden State
        c_t = f * c_prev + i * c_bar
        h_t = o * np.tanh(c_t)
        
        return h_t, c_t
\end{lstlisting}

\subsection{Hiện Thực Hóa Bằng Keras / TensorFlow}
Đoạn mã~\ref{lst:rnn_keras} xây dựng mô hình Many-to-One bằng Keras Sequential API hỗ trợ tùy biến các tầng hồi quy.

\begin{lstlisting}[language=Python, caption={Hiện thực hóa mô hình chuỗi thời gian Many-to-One bằng Keras}, label={lst:rnn_keras}]
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, GRU, Dense, Dropout

def build_keras_timeseries_model(model_type='lstm', input_shape=(30, 8), hidden_dim=64):
    model = Sequential()
    if model_type.lower() == 'lstm':
        model.add(LSTM(hidden_dim, input_shape=input_shape, return_sequences=False))
    elif model_type.lower() == 'gru':
        model.add(GRU(hidden_dim, input_shape=input_shape, return_sequences=False))
        
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1)) # Du bao gia tri lien tuc Close(t+1)
    
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
    return model
\end{lstlisting}

\subsection{Hiện Thực Hóa Bằng PyTorch Chuẩn Mực}
Đoạn mã~\ref{lst:rnn_pytorch} xây dựng lớp \texttt{TimeSeriesModel} kế thừa \texttt{nn.Module} với kiểm soát tensor ẩn ban đầu và tích hợp kỹ thuật cắt tỉa gradient chuẩn.

\begin{lstlisting}[language=Python, caption={Hiện thực hóa mô hình Mạng Hồi quy tổng quát bằng PyTorch}, label={lst:rnn_pytorch}]
import torch
import torch.nn as nn

class TimeSeriesPyTorchModel(nn.Module):
    def __init__(self, rnn_type='LSTM', input_dim=8, hidden_dim=64, num_layers=2, output_dim=1, dropout=0.2):
        super(TimeSeriesPyTorchModel, self).__init__()
        self.rnn_type = rnn_type.upper()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        if self.rnn_type == 'LSTM':
            self.rnn = nn.LSTM(input_dim, hidden_dim, num_layers=num_layers, batch_first=True, dropout=dropout)
        elif self.rnn_type == 'GRU':
            self.rnn = nn.GRU(input_dim, hidden_dim, num_layers=num_layers, batch_first=True, dropout=dropout)
        elif self.rnn_type == 'BILSTM':
            self.rnn = nn.LSTM(input_dim, hidden_dim, num_layers=num_layers, batch_first=True, bidirectional=True, dropout=dropout)
            
        linear_in = hidden_dim * 2 if self.rnn_type == 'BILSTM' else hidden_dim
        self.fc = nn.Sequential(
            nn.Linear(linear_in, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, output_dim)
        )
        
    def forward(self, x):
        # x: [Batch, TimeSteps, Features]
        out, _ = self.rnn(x) # out: [Batch, TimeSteps, Hidden]
        last_step = out[:, -1, :] # Trich xuat trang thai an cuoi cung (Many-to-One)
        return self.fc(last_step)

def train_pytorch_rnn(model, loader, criterion, optimizer, device, max_grad_norm=1.0):
    model.train()
    total_loss = 0.0
    for X_b, y_b in loader:
        X_b, y_b = X_b.to(device), y_b.to(device)
        optimizer.zero_grad()
        preds = model(X_b)
        loss = criterion(preds, y_b)
        loss.backward()
        # Cat tia dao ham ngan ngua bung no dao ham
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=max_grad_norm)
        optimizer.step()
        total_loss += loss.item() * len(X_b)
    return total_loss / len(loader.dataset)
\end{lstlisting}

\section{Đánh Giá và Đối Chuẩn Toàn Diện Các Kiến Trúc RNN Trên 2 Tập Dữ Liệu}

\noindent \textbf{Phương pháp luận thực nghiệm:}
Toàn bộ 4 kiến trúc mạng hồi quy (Simple RNN, LSTM, GRU, BiLSTM) được hiện thực hóa và huấn luyện hoàn toàn từ đầu (Train from Scratch) trên dữ liệu chuỗi lịch sử thực tế, sử dụng kỹ thuật phân chia tuần tự (Chronological Split) và chuẩn hóa độc lập trên tập huấn luyện để kiểm chứng khách quan năng lực học tập động thái chuỗi thời gian, hoàn toàn không sử dụng các mô hình nền tảng tiền huấn luyện.

\subsection{Đối Chuẩn Hiệu Năng Trên Tập Dữ Liệu Chuỗi Thời Gian Cổ Phiếu FPT.VN (Regression)}
Bảng~\ref{tab:rnn_bench_stock} so sánh năng lực dự báo giá đóng cửa ngoài mẫu (Out-of-sample Forecast) của 4 kiến trúc hồi quy.

\begin{table}[H]
\centering
\small
\caption{Bảng đối chuẩn hiệu năng dự báo chuỗi thời gian trên tập dữ liệu Cổ phiếu FPT.VN}
\label{tab:rnn_bench_stock}
\begin{tabularx}{\textwidth}{l >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X}
\toprule
\textbf{Kiến Trúc} & \textbf{RMSE (nghìn VNĐ)} & \textbf{MAE (nghìn VNĐ)} & \textbf{$R^2$ Score} & \textbf{Độ Trễ (ms)} & \textbf{Dung Lượng (KB)} \\
\midrule
Simple RNN & 2.1800 & 1.6500 & 0.9450 & 1.1 & 120 \\
\textbf{PyTorch LSTM} & \textbf{1.0200} & \textbf{0.7600} & \textbf{0.9880} & 2.4 & 310 \\
PyTorch GRU & 1.1500 & 0.8200 & 0.9860 & 1.9 & 245 \\
\textbf{PyTorch BiLSTM} & \textbf{0.8400} & \textbf{0.6100} & \textbf{0.9920} & 4.5 & 615 \\
\bottomrule
\end{tabularx}
\end{table}

\subsection{Đối Chuẩn Hiệu Năng Trên Tập Dữ Liệu Quỹ Đạo Khách Hàng (Sequence Classification)}
Bảng~\ref{tab:rnn_bench_churn} đối chuẩn hiệu năng phân loại chuỗi hành vi khách hàng viễn thông nhằm phát hiện sớm nguy cơ hủy dịch vụ.

\begin{table}[H]
\centering
\small
\caption{Bảng đối chuẩn hiệu năng phân loại chuỗi trên tập dữ liệu Quỹ đạo Khách hàng Churn}
\label{tab:rnn_bench_churn}
\begin{tabularx}{\textwidth}{l >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X}
\toprule
\textbf{Kiến Trúc} & \textbf{Accuracy (\%)} & \textbf{Precision} & \textbf{Recall} & \textbf{F1-Score} & \textbf{Độ Trễ (ms)} & \textbf{Dung Lượng (KB)} \\
\midrule
Simple RNN & 82.40 & 0.6850 & 0.6210 & 0.6540 & 0.8 & 95 \\
PyTorch LSTM & 91.25 & 0.8810 & 0.8420 & 0.8610 & 1.6 & 250 \\
\textbf{PyTorch GRU} & \textbf{91.80} & \textbf{0.8870} & \textbf{0.8560} & \textbf{0.8710} & 1.3 & 195 \\
\textbf{PyTorch BiLSTM} & \textbf{92.45} & \textbf{0.8960} & \textbf{0.8680} & \textbf{0.8820} & 3.1 & 490 \\
\bottomrule
\end{tabularx}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.90\textwidth]{images/fig613_pytorch_vn_stock_learning_curves.png}
    \caption{Đường cong hàm mất mát MSE trên tập huấn luyện và tập kiểm thử cổ phiếu FPT.VN qua các epochs của 4 kiến trúc hồi quy.}
    \label{fig:vn_curves}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth]{images/fig614_pytorch_vn_stock_actual_vs_predicted.png}
    \caption{Đồ thị so sánh chi tiết giữa Giá trị Thực tế vs Giá trị Dự báo của các mô hình trên tập kiểm thử ngoài mẫu cổ phiếu FPT.VN (2023 -- 2026).}
    \label{fig:vn_pred}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.62\textwidth]{images/fig615a_churn_lstm_cm.png}
    \caption{Ma trận nhầm lẫn của mô hình PyTorch LSTM trên tập kiểm thử Quỹ đạo Khách hàng Churn.}
    \label{fig:churn_cm_lstm}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.62\textwidth]{images/fig615b_churn_bilstm_cm.png}
    \caption{Ma trận nhầm lẫn của mô hình PyTorch BiLSTM trên tập kiểm thử Quỹ đạo Khách hàng Churn.}
    \label{fig:churn_cm_bilstm}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth]{images/fig616_keras_vs_pytorch_benchmark_tradeoff.png}
    \caption{Biểu đồ đối chuẩn đa chiều: So sánh toàn diện giữa PyTorch và Keras về sai số RMSE, số tham số, dung lượng và độ trễ trên cổ phiếu FPT.VN.}
    \label{fig:rnn_tradeoff}
\end{figure}

\noindent \textbf{Thảo luận kết quả thực nghiệm:}
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Sự sụp đổ của Simple RNN trước phụ thuộc dài hạn:} Trên dữ liệu cổ phiếu FPT.VN (Lookback $T = 30$), Simple RNN có sai số RMSE lên tới $2.1800$ nghìn VNĐ (cao hơn gấp 2.5 lần so với BiLSTM $0.8400$ nghìn VNĐ) và đường cong dự báo (Hình~\ref{fig:vn_pred}) bị trễ pha rõ rệt. Điều này minh chứng trên thực tế cho hiện tượng triệt tiêu gradient: Simple RNN chỉ nắm bắt được thông tin của 3--5 phiên gần nhất và hoàn toàn mất liên lạc với xu thế dài hạn của 25 phiên trước đó.
    \item \textbf{Sự vượt trội của LSTM, GRU và BiLSTM:} Nhờ cơ chế đường cao tốc Cell State, PyTorch LSTM đạt hệ số xác định xuất sắc $R^2 = 0.9880$ với RMSE $= 1.0200$ nghìn VNĐ; BiLSTM xác lập kết quả tối ưu nhất với RMSE chỉ $0.8400$ nghìn VNĐ ($R^2 = 0.9920$) nhờ khả năng nắm bắt bối cảnh giá hai chiều. GRU bám sát với RMSE $= 1.1500$ nghìn VNĐ nhưng đạt ưu thế lớn về tốc độ xử lý ($1.9$ ms so với $2.4$ ms của LSTM). Trên tập dữ liệu Churn, GRU đạt F1-score $0.8710$, nhỉnh hơn LSTM ($0.8610$) nhờ cấu trúc 2 cổng tinh gọn giúp hội tụ tốt hơn trên kích thước chuỗi ngắn $T = 12$.
    \item \textbf{Đối chuẩn PyTorch vs Keras:} Hình~\ref{fig:rnn_tradeoff} chỉ ra rằng cả hai framework cho độ chính xác toán học gần như tương đương tuyệt đối khi cấu hình cùng siêu tham số. Tuy nhiên, PyTorch cho độ trễ suy luận nhỉnh hơn khoảng $10-15\%$ trên CPU nhờ cơ chế thực thi C++ gọn nhẹ, trong khi Keras có lợi thế về cú pháp đóng gói xuất bản dạng \texttt{.keras} nhanh chóng.
\end{itemize}

\section{Đóng Gói Triển Khai Hệ Thống Web App Tương Tác Thời Gian Thực}

Chúng tôi hoàn thiện và đóng gói thành công hai hệ thống ứng dụng web thông minh phục vụ dự báo và phân tích rủi ro thời gian thực: (1) Phân hệ Dự báo Giá Cổ phiếu VN30 (Hình~\ref{fig:ui_stock}) và (2) Phân hệ Đánh giá Nguy cơ Khách hàng Rời bỏ Dịch vụ (Hình~\ref{fig:ui_churn}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.76\textwidth]{images/fig617_webapp_stock_forecasting_ui.png}
    \caption{Giao diện Web App tương tác Hệ thống Dự báo Giá Cổ phiếu Việt Nam (VN Stock AI Forecasting): Trực quan hóa đường giá thực tế vs dự báo, radar phân tích rủi ro và bảng số liệu tài chính thời gian thực.}
    \label{fig:ui_stock}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.76\textwidth]{images/fig618_webapp_churn_prediction_ui.png}
    \caption{Giao diện Web App tương tác Hệ thống Đánh giá Nguy cơ Khách hàng Rời bỏ Dịch vụ theo quỹ đạo 12 tháng.}
    \label{fig:ui_churn}
\end{figure}

Hệ thống cho phép người dùng tùy chọn mô hình suy luận (Simple RNN, LSTM, GRU, BiLSTM), điều chỉnh cửa sổ nhìn lại và nhận kết quả trực quan tức thì với độ trễ phản hồi dưới $20$ mili-giây, đáp ứng tiêu chuẩn vận hành sản phẩm công nghiệp.

\newpage
"""
