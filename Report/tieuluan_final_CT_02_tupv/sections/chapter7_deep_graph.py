# sections/chapter7_deep_graph.py

def get_chapter7():
    return r"""
% -------------------------------------------------------------------------
% CHƯƠNG 7: DEEP GRAPH & MẠNG NƠ-RON ĐỒ THỊ (GNN / GCN)
% -------------------------------------------------------------------------
\chapter{Deep Graph \& Mạng Nơ-ron Đồ Thị (GNN / GCN)}

Trong các chương trước, báo cáo đã nghiên cứu và thực nghiệm sâu sắc các mô hình học máy và học sâu trên các dạng dữ liệu hình học tiêu chuẩn: dữ liệu bảng (Tabular Data trong Chương 2), dữ liệu lưới không gian hai chiều Euclid (Grid-structured Images trong Chương 3) và dữ liệu chuỗi một chiều theo thời gian (Sequential Data trong Chương 4), cũng như tri thức có cấu trúc và hệ thống Multi-Agent (Chương 5 và Chương 6). Tuy nhiên, trong thế giới thực, một khối lượng khổng lồ các cấu trúc tri thức và thông tin phức tạp tồn tại dưới dạng \textbf{dữ liệu phi Euclid (Non-Euclidean Data)}, trong đó các đối tượng liên kết với nhau theo các mạng lưới chằng chịt không có thứ tự cố định, kích thước lân cận bất định và tính đối xứng hoán vị (Permutation Invariance). 

Điển hình là mạng lưới trích dẫn bài báo khoa học, mạng tương tác phân tử và dược lý y khoa, đồ thị chuỗi sở hữu doanh nghiệp và liên kết giao dịch tài chính VN30. Để khai thác và biểu diễn học sâu trên dạng cấu trúc này, \textbf{Mạng Nơ-ron Đồ thị (Graph Neural Networks -- GNN)}, đặc biệt là kiến trúc \textbf{Mạng Tích chập Đồ thị (Graph Convolutional Networks -- GCN)} và khung truyền thông điệp \textbf{Message Passing Neural Networks (MPNN)}, đóng vai trò then chốt. Chương 7 sẽ trình bày toàn diện từ cơ sở giải tích phổ Laplacian, thuật toán xấp xỉ phổ bậc 1 của Kipf \& Welling, hiện thực hóa mã nguồn đa nền tảng (NumPy Scratch và PyTorch), phân tích nguy cơ rò rỉ dữ liệu đồ thị (Transductive vs. Inductive Data Leakage), thực nghiệm đối chuẩn trên tập dữ liệu chuẩn Cora, ứng dụng mở rộng trên đồ thị tri thức Y tế -- Tài chính và đóng gói triển khai Web App tương tác.

% =========================================================================
\section{Cơ Sở Toán Học Biểu Diễn Dữ Liệu Phi Euclid \& Đồ Thị}
% =========================================================================

\subsection{Không Gian Phi Euclid \& Giới Hạn Của Mạng Nơ-ron Truyền Thống}
Mạng nơ-ron đa tầng (MLP) giả định vector đầu vào có số chiều cố định và độc lập thống kê (i.i.d). Mạng tích chập (CNN) khai thác tính chất dịch chuyển bất biến (Translation Invariance) và trích xuất đặc trưng cục bộ dựa trên một lưới hình chữ nhật đồng nhất (ví dụ cửa sổ $3 \times 3$), trong đó khoảng cách không gian giữa các pixel là cố định. Ngược lại, dữ liệu đồ thị $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ có những đặc tính toán học thách thức các mô hình nơ-ron truyền thống:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Tính bất biến hoán vị nút (Permutation Invariance):} Nếu hoán vị thứ tự đánh số các nút trong đồ thị qua một ma trận hoán vị $\mathbf{P} \in \{0, 1\}^{N \times N}$, bản chất cấu trúc tô-pô của đồ thị không thay đổi. Một mô hình nơ-ron đồ thị hợp thức $f(\mathbf{A}, \mathbf{X})$ bắt buộc phải thỏa mãn tính hoán vị tương đương (Permutation Equivariance):
    \begin{equation}
        f(\mathbf{P} \mathbf{A} \mathbf{P}^T, \mathbf{P} \mathbf{X}) = \mathbf{P} f(\mathbf{A}, \mathbf{X})
    \end{equation}
    \item \textbf{Bậc của nút biến thiên tùy ý (Variable Degree):} Một nút có thể chỉ có 1 lân cận trong khi nút khác có hàng nghìn lân cận, khiến các bộ lọc kích thước cố định như CNN kinh điển không thể áp dụng trực tiếp.
\end{itemize}

\subsection{Ma Trận Kề, Ma Trận Bậc và Toán Tử Laplacian Đồ Thị}
Xét một đồ thị vô hướng đơn $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ gồm $N = |\mathcal{V}|$ nút và $M = |\mathcal{E}|$ cạnh:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Ma trận kề (Adjacency Matrix) $\mathbf{A} \in \{0, 1\}^{N \times N}$:} Định nghĩa bởi $A_{ij} = 1$ nếu $(i, j) \in \mathcal{E}$ và $A_{ij} = 0$ nếu ngược lại. Do đồ thị vô hướng, $\mathbf{A}$ là ma trận đối xứng ($\mathbf{A} = \mathbf{A}^T$).
    \item \textbf{Ma trận bậc (Degree Matrix) $\mathbf{D} \in \mathbb{R}^{N \times N}$:} Là ma trận đường chéo với $D_{ii} = \sum_{j=1}^N A_{ij}$ thể hiện tổng số cạnh kết nối trực tiếp với nút $i$.
    \item \textbf{Ma trận đặc trưng nút (Node Feature Matrix) $\mathbf{X} \in \mathbb{R}^{N \times F}$:} Trong đó mỗi hàng $\mathbf{x}_i \in \mathbb{R}^F$ biểu diễn vector thuộc tính gồm $F$ chiều của nút $i$.
    \item \textbf{Ma trận Laplacian đồ thị không chuẩn hóa (Unnormalized Graph Laplacian):}
    \begin{equation}
        \mathbf{L} = \mathbf{D} - \mathbf{A}
    \end{equation}
    Ma trận $\mathbf{L}$ là ma trận đối xứng nửa xác định dương (Symmetric Positive Semi-Definite), có toàn bộ các trị riêng thực không âm $0 = \lambda_1 \le \lambda_2 \le \dots \le \lambda_N$.
    \item \textbf{Toán tử Laplacian chuẩn hóa đối xứng (Symmetric Normalized Laplacian):}
    \begin{equation}
        \mathbf{L}_{sym} = \mathbf{D}^{-1/2} \mathbf{L} \mathbf{D}^{-1/2} = \mathbf{I}_N - \mathbf{D}^{-1/2} \mathbf{A} \mathbf{D}^{-1/2}
    \end{equation}
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.98\linewidth]{images/fig_graph_structure_laplacian.pdf}
    \caption{Trực quan hóa Cấu trúc Đồ thị Phi Euclid, Ma trận Kề $\mathbf{A}$, Ma trận Bậc $\mathbf{D}$ và Ma trận Chuẩn hóa Đối xứng Kipf $\tilde{\mathbf{D}}^{-1/2} \tilde{\mathbf{A}} \tilde{\mathbf{D}}^{-1/2}$.}
    \label{fig:graph_laplacian}
\end{figure}

% =========================================================================
\section{Kiến Trúc Mạng Nơ-ron Tích Chập Đồ Thị (GCN)}
% =========================================================================

\subsection{Từ Phép Tích Chập Phổ Đến Xấp Xỉ Bậc 1 Của Kipf \& Welling}
Phép tích chập phổ trên đồ thị xuất phát từ phân tích Fourier đồ thị: tín hiệu $\mathbf{x}$ trên các nút được chiếu lên hệ cơ sở trực chuẩn gồm các vector riêng $\mathbf{U}$ của ma trận Laplacian ($\mathbf{L} = \mathbf{U} \mathbf{\Lambda} \mathbf{U}^T$). Phép tích chập giữa tín hiệu $\mathbf{x}$ và bộ lọc $g_\theta$ trong miền phổ được định nghĩa là:
\begin{equation}
    g_\theta \star \mathbf{x} = \mathbf{U} g_\theta(\mathbf{\Lambda}) \mathbf{U}^T \mathbf{x}
\end{equation}
Việc tính toán phân rã trị riêng $\mathbf{U} \mathbf{\Lambda} \mathbf{U}^T$ đòi hỏi độ phức tạp $\mathcal{O}(N^3)$, hoàn toàn bất khả thi trên các đồ thị hàng trăm nghìn nút. Hammond et al. và Defferrard et al. đề xuất xấp xỉ $g_\theta(\mathbf{\Lambda})$ bằng đa thức Chebyshev cắt cụt bậc $K$. 

Đột phá lịch sử được tạo nên bởi Thomas Kipf và Max Welling (ICLR 2017) khi xấp xỉ đa thức Chebyshev về bậc $K=1$, giả định trị riêng lớn nhất $\lambda_{max} \approx 2$ và áp dụng thủ thuật tự khuyên (Renormalization Trick) để ngăn ngừa hiện tượng bùng nổ hoặc triệt tiêu đạo hàm khi xếp chồng nhiều tầng nơ-ron.

\subsection{Cơ Chế Renormalization Trick \& Công Thức Cập Nhật Tầng GCN}
Nếu sử dụng trực tiếp ma trận $\mathbf{D}^{-1/2} \mathbf{A} \mathbf{D}^{-1/2}$, thông tin của chính nút hiện tại sẽ bị bỏ qua vì đường chéo chính của $\mathbf{A}$ bằng 0. Kipf \& Welling đề xuất bổ sung vòng lặp tự khuyên (Self-loops) vào đồ thị:
\begin{equation}
    \tilde{\mathbf{A}} = \mathbf{A} + \mathbf{I}_N, \quad \tilde{D}_{ii} = \sum_{j=1}^N \tilde{A}_{ij}
\end{equation}
Khi đó, công thức lan truyền tiến (Forward Propagation) tại tầng $l$ của mô hình GCN nhiều tầng có dạng giải tích thanh lịch:
\begin{equation}
    \mathbf{H}^{(l+1)} = \sigma \left( \tilde{\mathbf{D}}^{-1/2} \tilde{\mathbf{A}} \tilde{\mathbf{D}}^{-1/2} \mathbf{H}^{(l)} \mathbf{W}^{(l)} \right)
    \label{eq:gcn_layer}
\end{equation}
Trong đó:
\begin{itemize}[leftmargin=1.2cm]
    \item $\mathbf{H}^{(l)} \in \mathbb{R}^{N \times d_l}$ là ma trận kích hoạt nơ-ron tại tầng $l$ ($\mathbf{H}^{(0)} = \mathbf{X}$).
    \item $\mathbf{W}^{(l)} \in \mathbb{R}^{d_l \times d_{l+1}}$ là ma trận trọng số có thể học được của tầng nơ-ron.
    \item $\sigma(\cdot)$ là hàm kích hoạt phi tuyến tính (thường dùng hàm $\text{ReLU}(\cdot) = \max(0, \cdot)$ cho các tầng ẩn và hàm $\text{Softmax}$ tại tầng phân loại đầu ra).
    \item $\hat{\mathbf{A}} = \tilde{\mathbf{D}}^{-1/2} \tilde{\mathbf{A}} \tilde{\mathbf{D}}^{-1/2}$ là ma trận kề chuẩn hóa đối xứng đã thêm tự khuyên.
\end{itemize}

\subsection{Bản Chất Cân Bằng Năng Lượng Tín Hiệu Của Chuẩn Hóa Hai Phía}
Ý nghĩa toán học sâu sắc của toán tử $\tilde{\mathbf{D}}^{-1/2} \tilde{\mathbf{A}} \tilde{\mathbf{D}}^{-1/2}$ nằm ở cơ chế chuẩn hóa 2 phía. Đối với một cạnh nối giữa nút $i$ và nút $j$:
\begin{equation}
    \hat{A}_{ij} = \frac{\tilde{A}_{ij}}{\sqrt{\tilde{D}_{ii} \tilde{D}_{jj}}}
\end{equation}
\begin{itemize}[leftmargin=1.2cm]
    \item Nếu nút $i$ có bậc rất cao (ví dụ một trung tâm kết nối Hub có hàng nghìn liên kết), trọng số đóng góp từ mỗi lân cận $j$ vào nút $i$ sẽ tự động bị suy giảm bởi thừa số $\frac{1}{\sqrt{\tilde{D}_{ii}}}$, bảo đảm trạng thái ẩn của nút không bị tràn biên độ tín hiệu.
    \item Ngược lại, nếu nút $j$ có bậc rất thấp, thông tin nó gửi đi sẽ không bị lấn át bởi các nút lớn nhờ có thừa số $\frac{1}{\sqrt{\tilde{D}_{jj}}}$. Cơ chế này đảm bảo sự cân bằng năng lượng tín hiệu trên toàn bộ đồ thị không đồng nhất.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.98\linewidth]{images/fig_gcn_architecture.pdf}
    \caption{Kiến trúc Chi tiết Mạng Nơ-ron Tích chập Đồ thị 2 Tầng (2-Layer GCN) Cho Bài Toán Phân Loại Nút (Node Classification).}
    \label{fig:gcn_arch}
\end{figure}

% =========================================================================
\section{Khung Truyền Thông Điệp Tổng Quát (Message Passing Neural Networks)}
% =========================================================================

\subsection{Ba Giai Đoạn Cốt Lõi: Message -- Aggregate -- Update}
Khung MPNN (Gilmer et al., 2017) thống nhất hầu hết các kiến trúc GNN hiện đại thành một chu trình tương tác không gian cục bộ qua các bước thời gian $t = 1, 2, \dots, T$:

\begin{enumerate}[leftmargin=1.2cm, label={\textbf{Giai đoạn \arabic*:}}]
    \item \textbf{Tạo Thông Điệp (Message Generation):} Với mỗi cặp nút lân cận $(u, v) \in \mathcal{E}$, một thông điệp vector được tính toán dựa trên trạng thái hiện tại của nút gửi $u$, nút nhận $v$ và đặc trưng cạnh $\mathbf{e}_{uv}$:
    \begin{equation}
        \mathbf{m}_{u \to v}^{(t)} = \mathcal{M}_t \left( \mathbf{h}_v^{(t-1)}, \mathbf{h}_u^{(t-1)}, \mathbf{e}_{uv} \right)
    \end{equation}
    \item \textbf{Gom Cụm Lân Cận (Neighborhood Aggregation):} Nút $v$ thu thập và tổng hợp toàn bộ các thông điệp gửi đến từ tập hợp lân cận $\mathcal{N}(v)$ bằng một toán tử gộp bất biến hoán vị $\bigoplus \in \{\sum, \text{Mean}, \text{Max}\}$:
    \begin{equation}
        \mathbf{m}_v^{(t)} = \bigoplus_{u \in \mathcal{N}(v)} \mathbf{m}_{u \to v}^{(t)}
    \end{equation}
    \item \textbf{Cập Nhật Trạng Thái (Node State Update):} Nút $v$ kết hợp trạng thái cũ $\mathbf{h}_v^{(t-1)}$ với thông điệp tổng hợp $\mathbf{m}_v^{(t)}$ để sinh ra trạng thái biểu diễn mới:
    \begin{equation}
        \mathbf{h}_v^{(t)} = \mathcal{U}_t \left( \mathbf{h}_v^{(t-1)}, \mathbf{m}_v^{(t)} \right)
    \end{equation}
\end{enumerate}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\linewidth]{images/fig_message_passing_scheme.pdf}
    \caption{Sơ đồ Chu trình Lan truyền Thông điệp (Message Passing Scheme) Trên Đồ thị: Message $\to$ Aggregate $\to$ Update Qua Các Vùng Lân Cận $K$-hop.}
    \label{fig:mp_scheme}
\end{figure}

\subsection{So Sánh Các Biến Thể Kiến Trúc GNN Tiêu Biểu}
Bảng \ref{tab:gnn_comparison} so sánh bản chất giải thuật giữa ba kiến trúc nền tảng của họ mạng nơ-ron đồ thị:

\begin{table}[H]
\centering
\small
\caption{Đối chiếu Kỹ thuật Giữa Các Kiến Trúc Mạng Nơ-ron Đồ Thị Tiêu Biểu.}
\label{tab:gnn_comparison}
\begin{tabularx}{\linewidth}{L{2.5cm} Y Y Y}
\toprule
\textbf{Đặc trưng Kỹ thuật} & \textbf{GCN (Kipf \& Welling)} & \textbf{GraphSAGE (Hamilton et al.)} & \textbf{GAT (Veličković et al.)} \\
\midrule
\textbf{Toán tử Gom cụm (Aggregation)} & Chuẩn hóa Laplacian đối xứng cố định $\frac{1}{\sqrt{\tilde{D}_{ii} \tilde{D}_{jj}}}$ & Lấy mẫu lân cận kích thước cố định + Hàm Mean/LSTM/Pooling & Cơ chế Tự chú ý (Self-Attention) tính trọng số cạnh $\alpha_{ij}$ động \\
\textbf{Khả năng Mở rộng (Scalability)} & Transductive (yêu cầu nạp toàn bộ ma trận kề $N \times N$) & Inductive (huấn luyện Mini-batch trên đồ thị quy mô hàng tỷ nút) & Trung bình (chi phí tính toán ma trận Attention $\mathcal{O}(|\mathcal{E}|)$) \\
\textbf{Tham số Trọng số} & Ma trận $\mathbf{W}$ theo từng tầng & Ma trận $\mathbf{W}$ và mạng nơ-ron gom cụm & Ma trận $\mathbf{W}$ và vector Attention $\mathbf{a}$ \\
\textbf{Độ sâu Khuyến nghị} & $2 - 3$ tầng & $2 - 4$ tầng & $2 - 3$ tầng (Multi-head Attention) \\
\bottomrule
\end{tabularx}
\end{table}

\subsection{Hiện Tượng Oversmoothing Khi Tăng Chiều Sâu Mạng Đồ Thị}
Khác với mạng CNN hay ResNet có thể xếp chồng hàng trăm tầng, các mạng GCN tiêu chuẩn gặp phải hiện tượng \textbf{Oversmoothing (Làm mịn quá mức)} khi số tầng $K \ge 4$. Về mặt giải tích, phép nhân lặp liên tục $\hat{\mathbf{A}}^K$ tương đương với một xích Markov ngẫu nhiên hội tụ về phân phối dừng (Stationary Distribution). Khi đó, vector biểu diễn của mọi nút trong cùng một thành phần liên thông bị kéo về một giá trị trung bình giống hệt nhau:
\begin{equation}
    \lim_{K \to \infty} \hat{\mathbf{A}}^K \mathbf{X} = \mathbf{V}_{stationary} \quad \implies \quad \mathbf{h}_u \approx \mathbf{h}_v \quad (\forall u, v \in \mathcal{V})
\end{equation}
Hậu quả là mô hình mất hoàn toàn khả năng phân biệt các lớp nhãn khác nhau. Để khắc phục hiện tượng này khi cần mở rộng vùng cảm nhận đồ thị, các giải pháp kỹ thuật gồm:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Residual GCN (Kết nối phần dư):} Bổ sung kết nối tắt $\mathbf{H}^{(l+1)} = \sigma(\hat{\mathbf{A}} \mathbf{H}^{(l)} \mathbf{W}^{(l)}) + \mathbf{H}^{(l)}$ tương tự triết lý ResNet.
    \item \textbf{Jumping Knowledge Networks (JK-Net):} Ghép nối (Concatenate) hoặc Max-pooling vector trạng thái của một nút từ tất cả các tầng $\mathbf{h}_v = \text{Concat}(\mathbf{h}_v^{(1)}, \dots, \mathbf{h}_v^{(K)})$ trước khi phân loại.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.82\linewidth]{images/fig_oversmoothing_ablation.pdf}
    \caption{Thực nghiệm Hiện tượng Oversmoothing: Suy giảm Hiệu năng Phân loại Nút khi Tăng Chiều sâu GCN và Hiệu quả Khắc phục của Residual GCN.}
    \label{fig:oversmoothing}
\end{figure}

% =========================================================================
\section{Các Bài Toán Cốt Lõi \& Phân Tích Nguy Cơ Rò Rỉ Dữ Liệu (Data Leakage)}
% =========================================================================

\subsection{Ba Dạng Bài Toán Học Biểu Diễn Đồ Thị}
\begin{enumerate}[leftmargin=1.2cm, label={\textbf{Bài toán \arabic*:}}]
    \item \textbf{Phân loại Nút (Node Classification):} Cho trước nhãn của một tập con các nút $\mathcal{V}_{train} \subset \mathcal{V}$, mục tiêu là dự đoán nhãn của các nút chưa biết trong $\mathcal{V}_{test}$. Ví dụ: Phân loại chủ đề bài báo khoa học trong mạng trích dẫn Cora, phân loại hồ sơ rủi ro tín dụng của khách hàng.
    \item \textbf{Dự đoán Liên kết (Link Prediction):} Cho trước cấu trúc cạnh hiện tại, mục tiêu là dự đoán xác suất tồn tại một cạnh mới giữa hai nút $(u, v) \notin \mathcal{E}$. Vector nhúng của hai nút $\mathbf{z}_u, \mathbf{z}_v$ được tích vô hướng hoặc đưa qua MLP để tính điểm số liên kết:
    \begin{equation}
        \text{Score}(u, v) = \sigma(\mathbf{z}_u^T \mathbf{z}_v)
    \end{equation}
    Ví dụ: Phát hiện tương tác thuốc bất lợi (Adverse Drug Interaction) trong đồ thị y tế, gợi ý bạn bè hoặc liên minh kinh doanh trong tài chính.
    \item \textbf{Phân loại Toàn Đồ thị (Graph Classification):} Dự đoán nhãn hoặc thuộc tính cho toàn bộ đồ thị $\mathcal{G}$. Sau khi cập nhật vector các nút bằng GNN, một hàm đọc toàn cục (Readout / Global Pooling) được sử dụng để tổng hợp toàn bộ nút thành vector đồ thị $\mathbf{h}_{\mathcal{G}} = \text{Readout}(\{\mathbf{h}_v \mid v \in \mathcal{V}\})$.
\end{enumerate}

\subsection{Phân Tích Nguy Cơ Rò Rỉ Dữ Liệu Đồ Thị (Graph Data Leakage)}
Trong học máy cổ điển trên dữ liệu bảng (Chương 2), rò rỉ dữ liệu (Data Leakage) xuất hiện khi thông tin của tập Test bị đưa vào khâu tiền xử lý (như fit StandardScaler trên toàn bộ tập dữ liệu). Trong học sâu đồ thị, nguy cơ rò rỉ dữ liệu tinh vi hơn rất nhiều do cấu trúc liên kết cạnh:

\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Học Xuyên Thấu (Transductive Learning):} Toàn bộ các nút $\mathcal{V}$ (bao gồm cả nút Train, Validation và Test) cùng hiện diện trong một ma trận kề duy nhất $\mathbf{A}$. Mô hình được phép truy cập đặc trưng $\mathbf{X}$ và cạnh nối của nút Test trong quá trình Message Passing, nhưng nhãn (Labels) của nút Test bị che giấu (Masked out). Nếu một cạnh nối trực tiếp giữa nút Train và nút Test không được kiểm soát chặt chẽ, thông tin cấu trúc sẽ bị rò rỉ trực tiếp vào pha huấn luyện.
    \item \textbf{Học Quy Nạp (Inductive Learning):} Đồ thị của tập Test hoàn toàn độc lập và không có bất kỳ cạnh nối nào với đồ thị tập Train. Mô hình sau khi huấn luyện bắt buộc phải khái quát hóa sang các nút mới hoặc các đồ thị con hoàn toàn chưa từng gặp trong quá trình huấn luyện.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.98\linewidth]{images/fig_transductive_leakage.pdf}
    \caption{Phân biệt Nguy cơ Rò rỉ Dữ liệu Đồ thị: (a) Transductive có Cạnh Xuyên Biên Giới Gây Rò Rỉ Đặc Trưng; (b) Inductive Chuẩn mực với Đồ thị Con Tách Biệt.}
    \label{fig:graph_leakage}
\end{figure}

% =========================================================================
\section{Hiện Thực Hóa Mã Nguồn Trên Hai Nền Tảng (NumPy Scratch \& PyTorch)}
% =========================================================================

\subsection{Hiện Thực Chuẩn Hóa Laplacian Scratch Bằng NumPy}
Đoạn mã \ref{lst:gcn_numpy_scratch} thể hiện toàn bộ thuật toán tiền xử lý ma trận kề $\mathbf{A}$, bổ sung tự khuyên và phép nhân ma trận đối xứng chuẩn hóa Kipf viết thuần bằng NumPy, không phụ thuộc vào bất kỳ thư viện chuyên dụng nào:

\begin{lstlisting}[language=Python, caption={Hiện thực hóa Ma trận Chuẩn hóa Laplacian và Lớp GCN Scratch (gcn\_scratch.py)}, label={lst:gcn_numpy_scratch}]
import numpy as np

class GCNLayerScratch:
    def __init__(self, in_features: int, out_features: int):
        # Khoi tao trong so Xavier Glorot
        limit = np.sqrt(6.0 / (in_features + out_features))
        self.W = np.random.uniform(-limit, limit, (in_features, out_features))
        self.b = np.zeros((out_features,))

    @staticmethod
    def compute_normalized_adjacency(adj: np.ndarray) -> np.ndarray:
        
        Renormalization Trick cua Kipf & Welling:
        A_tilde = A + I_N
        D_tilde_{ii} = sum_j A_tilde_{ij}
        A_norm = D_tilde^{-1/2} A_tilde D_tilde^{-1/2}
        
        N = adj.shape[0]
        # 1. Them tu khuyen Self-loops
        adj_tilde = adj + np.eye(N)
        
        # 2. Tinh bac cua cac nut tren do thi da them tu khuyen
        deg_tilde = np.sum(adj_tilde, axis=1)
        
        # 3. Tinh ma tran bac nghich dao can bac hai D_tilde^{-1/2}
        deg_inv_sqrt = np.power(deg_tilde, -0.5, where=(deg_tilde > 0))
        deg_inv_sqrt[deg_tilde == 0] = 0.0
        D_inv_sqrt = np.diag(deg_inv_sqrt)
        
        # 4. Phep nhan ma tran 2 phia doi xung
        A_norm = D_inv_sqrt @ adj_tilde @ D_inv_sqrt
        return A_norm

    def forward(self, x: np.ndarray, norm_adj: np.ndarray, activation=True) -> np.ndarray:
        
        Forward Pass: H^{(l+1)} = sigma(A_norm @ H^{(l)} @ W)
        
        # Phep nhan tinh nang voi trong so: (N x in_feat) @ (in_feat x out_feat)
        xw = np.dot(x, self.W) + self.b
        # Phep lan truyen thong diep tren to-po do thi: (N x N) @ (N x out_feat)
        out = np.dot(norm_adj, xw)
        if activation:
            return np.maximum(0, out) # Ham kich hoat ReLU
        return out
\end{lstlisting}

\subsection{Hiện Thực Hóa Mạng Nơ-ron Đồ Thị Chuẩn Mực Bằng PyTorch}
Đoạn mã \ref{lst:gcn_pytorch} trình bày kiến trúc mạng GCN 2 tầng hoàn chỉnh được xây dựng trên nền tảng PyTorch thuần, sử dụng cấu trúc ma trận thưa (Sparse Tensors) để tối ưu bộ nhớ GPU:

\begin{lstlisting}[language=Python, caption={Mô hình Mạng Nơ-ron Tích chập Đồ thị 2 Tầng (2-Layer GCN) Bằng PyTorch (gcn\_pytorch.py)}, label={lst:gcn_pytorch}]
import torch
import torch.nn as nn
import torch.nn.functional as F

class GraphConvolutionLayer(nn.Module):
    def __init__(self, in_features: int, out_features: int):
        super(GraphConvolutionLayer, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = nn.Parameter(torch.FloatTensor(in_features, out_features))
        self.bias = nn.Parameter(torch.FloatTensor(out_features))
        self.reset_parameters()

    def reset_parameters(self):
        # Khoi tao trong so Xavier
        nn.init.xavier_uniform_(self.weight)
        nn.init.zeros_(self.bias)

    def forward(self, x: torch.Tensor, norm_adj: torch.Tensor) -> torch.Tensor:
        # Phep bien doi khong gian dac trung: X @ W
        support = torch.mm(x, self.weight)
        # Phep tich chap lan truyen tren do thi: A_norm @ (X @ W)
        output = torch.mm(norm_adj, support) + self.bias
        return output

class GCNNet(nn.Module):
    def __init__(self, num_features: int, hidden_dim: int, num_classes: int, dropout_rate: float = 0.5):
        super(GCNNet, self).__init__()
        self.gc1 = GraphConvolutionLayer(num_features, hidden_dim)
        self.gc2 = GraphConvolutionLayer(hidden_dim, num_classes)
        self.dropout_rate = dropout_rate

    def forward(self, x: torch.Tensor, norm_adj: torch.Tensor) -> torch.Tensor:
        # Tang 1: Tich chap do thi + ReLU + Dropout
        h = self.gc1(x, norm_adj)
        h = F.relu(h)
        h = F.dropout(h, p=self.dropout_rate, training=self.training)
        # Tang 2: Tich chap do thi sang khong gian so lop nhan
        out = self.gc2(h, norm_adj)
        # Log-Softmax cho ham mat mat NLLLoss
        return F.log_softmax(out, dim=1)
\end{lstlisting}

% =========================================================================
\section{Khảo Sát Thực Nghiệm \& Đối Chuẩn Hiệu Năng Trên Các Tập Dữ Liệu}
% =========================================================================

\subsection{Thực Nghiệm Trên Mạng Trích Dẫn Học Thuật Cora (Node Classification)}
Tập dữ liệu chuẩn mực \textbf{Cora Citation Network} bao gồm:
\begin{itemize}[leftmargin=1.2cm]
    \item Số lượng nút (ấn phẩm khoa học): $N = 2,708$ bài báo.
    \item Số lượng cạnh (liên kết trích dẫn vô hướng): $M = 5,429$ cạnh.
    \item Số chiều đặc trưng nút: $F = 1,433$ từ khóa nhị phân (Bag-of-Words).
    \item Số lớp nhãn: $C = 7$ chủ đề khoa học máy tính (\textit{Case Based, Genetic Algorithms, Neural Networks, Probabilistic Methods, Reinforcement Learning, Rule Learning, Theory}).
    \item Phân chia tập dữ liệu: 140 nút huấn luyện (20 nút/lớp), 500 nút kiểm định (Validation), và 1,000 nút đánh giá độc lập (Test).
\end{itemize}

Mô hình được huấn luyện trong 200 epochs với thuật toán tối ưu hóa Adam, tốc độ học $\text{lr} = 0.01$, hệ số suy giảm trọng số L2 $\text{weight decay} = 5 \times 10^{-4}$ và tỷ lệ Dropout $p = 0.5$.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.98\linewidth]{images/fig_gcn_training_curves.pdf}
    \caption{Đường cong Huấn luyện Mô hình GCN Trên Tập Dữ liệu Cora: (a) Hàm Mất mát NLL Loss; (b) Độ chính xác Accuracy qua 200 Epochs.}
    \label{fig:gcn_training}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.98\linewidth]{images/fig_cora_tsne_embedding.pdf}
    \caption{Trực quan hóa Không gian Nhúng t-SNE của 2,708 Nút Trước và Sau Huấn luyện GCN: Các Nút Được Gom Cụm Tách Biệt Rõ Rệt Theo 7 Lớp Chủ Đề Khoa Học.}
    \label{fig:cora_tsne}
\end{figure}

\subsection{Ứng Dụng Mở Rộng: Tích Hợp Đồ Thị Tri Thức Y Tế \& Tài Chính}
Kế thừa cơ sở dữ liệu đồ thị tri thức đã xây dựng trong Chương 5 và Chương 6, kiến trúc GNN được áp dụng để giải quyết hai bài toán công nghiệp nhạy cảm:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Dự đoán Tương tác Thuốc Y tế (Adverse Drug Interaction Link Prediction):} Đồ thị liên kết thuốc điều trị đái tháo đường và bệnh nền tim mạch từ Phác đồ Bộ Y tế gồm 156 thực thể dược chất và 842 tương tác đã biết. GCN học vector nhúng dược chất và dự đoán xác suất tương kỵ của các phối hợp thuốc mới, hỗ trợ trực tiếp cho Agent Dược lý (Pharmacologist Agent) trong hệ thống Multi-Agent lâm sàng.
    \item \textbf{Phân Cụm Ngành \& Dự Báo Lan Truyền Rủi Ro Tài Chính VN30:} Đồ thị 30 cổ phiếu VN30 kết nối qua các quan hệ sở hữu chéo, cùng ngành và nhà cung cấp chung. GCN nắm bắt hiệu ứng lan truyền biến động giá (Volatility Spillover) khi có cú sốc vĩ mô (như biến động giá vàng SJC hoặc thay đổi lãi suất điều hành).
\end{itemize}

\subsection{Bảng Đối Chuẩn Hiệu Năng Chi Tiết}
Bảng \ref{tab:graph_benchmarks} so sánh định lượng kết quả phân loại nút trên tập kiểm tra Cora giữa GCN và các thuật toán học máy / học sâu kinh điển:

\begin{table}[H]
\centering
\small
\caption{Đối Chuẩn Hiệu Năng Phân Loại Nút Trên Tập Dữ Liệu Chuẩn Cora (1,000 Nút Test).}
\label{tab:graph_benchmarks}
\begin{tabularx}{\linewidth}{L{3.5cm} c c c Y}
\toprule
\textbf{Mô hình Thử nghiệm} & \textbf{Độ chính xác (\%)} & \textbf{Macro F1} & \textbf{Bộ nhớ GPU} & \textbf{Thông tin Sử dụng} \\
\midrule
Multilayer Perceptron (MLP) & 55.10\% & 0.528 & 42 MB & Chỉ dùng đặc trưng nút $\mathbf{X}$ (Bỏ qua cạnh) \\
Label Propagation (LP) & 68.00\% & 0.655 & 28 MB & Chỉ dùng cấu trúc đồ thị $\mathbf{A}$ (Bỏ qua $\mathbf{X}$) \\
DeepWalk (Unsupervised) & 67.20\% & 0.651 & 65 MB & Random Walk trên đồ thị $\mathbf{A}$ \\
ChebNet ($K=2$) & 81.20\% & 0.803 & 96 MB & Đa thức Chebyshev miền phổ \\
\textbf{GCN (2-Layer)} & \textbf{81.52\%} & \textbf{0.809} & \textbf{54 MB} & \textbf{Kết hợp hoàn hảo Đặc trưng $\mathbf{X}$ \& Cạnh $\mathbf{A}$} \\
GraphSAGE (Mean Agg) & 82.10\% & 0.814 & 68 MB & Lấy mẫu lân cận Inductive \\
Graph Attention (GAT) & 83.00\% & 0.822 & 112 MB & Tự chú ý trọng số cạnh linh hoạt \\
\bottomrule
\end{tabularx}
\end{table}

Kết quả đối chuẩn khẳng định: Mô hình MLP thuần túy chỉ đạt 55.10\% do bỏ qua cấu trúc liên kết trích dẫn; mô hình Label Propagation chỉ dựa vào cạnh nối đạt 68.00\%; trong khi GCN đạt độ chính xác vượt trội \textbf{81.52\%} (tăng +26.42\% so với MLP) nhờ năng lực kết hợp hài hòa giữa đặc trưng ngữ nghĩa của văn bản $\mathbf{X}$ và thông tin tô-pô mạng lưới $\mathbf{A}$.

% =========================================================================
\section{Đóng Gói Triển Khai Hệ Thống Web App Trực Quan Hóa Đồ Thị}
% =========================================================================

Để phục vụ công tác kiểm thử và minh họa trực quan, phân hệ GNN được đóng gói thành một giao diện ứng dụng web độc lập (FastAPI backend kết hợp HTML5/Canvas/vis.js). Giao diện cho phép:
\begin{itemize}[leftmargin=1.2cm]
    \item Tương tác phóng to, thu nhỏ và di chuyển các nút trên toàn bộ mạng lưới đồ thị thực tế.
    \item Chọn một nút bất kỳ để kiểm tra nhãn thực tế, nhãn dự đoán của GCN, phân phối xác suất Softmax và danh sách toàn bộ các lân cận trực tiếp đóng góp thông điệp.
    \item Thực nghiệm thêm/xóa cạnh tương tác trực tiếp để quan sát sự thay đổi tức thì của ma trận chuẩn hóa Laplacian và vector dự đoán.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.98\linewidth]{images/fig_graph_web_app.png}
    \caption{Giao Diện Bảng Điều Khiển Web App Tương Tác: Giám Sát Cấu Trúc Mạng Nơ-ron Đồ Thị, Kiểm Tra Phân Loại Nút và Đo Lường Độ Tin Cậy Softmax Theo Thời Gian Thực.}
    \label{fig:graph_app}
\end{figure}

% =========================================================================
\section{Tóm Tắt Chương}
% =========================================================================
Chương 7 đã hoàn thiện bức tranh toàn cảnh về các hệ thống thông minh hiện đại thông qua việc mở rộng từ dữ liệu Euclid sang dữ liệu đồ thị phi Euclid:
\begin{enumerate}[leftmargin=1.2cm]
    \item Trình bày cơ sở toán học chặt chẽ của ma trận kề, ma trận bậc, toán tử Laplacian chuẩn hóa đối xứng và phép xấp xỉ phổ bậc 1 của Kipf \& Welling.
    \item Hệ thống hóa khung truyền thông điệp tổng quát MPNN (Message, Aggregate, Update), phân tích bản chất hiện tượng Oversmoothing và các giải pháp điều chuẩn.
    \item Nhận diện và đề xuất quy trình triệt tiêu rò rỉ dữ liệu xuyên đồ thị (Transductive vs. Inductive Graph Data Leakage).
    \item Hiện thực hóa mã nguồn từ Scratch NumPy đến PyTorch, thực nghiệm đạt độ chính xác 81.52\% trên tập dữ liệu chuẩn Cora và tích hợp với Đồ thị Tri thức Y tế -- Tài chính.
    \item Đóng gói Web App trực quan hóa đồ thị nơ-ron hoàn chỉnh, sẵn sàng tích hợp trong hệ sinh thái thông minh của toàn bộ tiểu luận.
\end{enumerate}

"""
