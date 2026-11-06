# -*- coding: utf-8 -*-
"""
sections/theory.py
Chương 1: Cơ sở lý thuyết và Nền tảng công nghệ
"""

def get_theory():
    return r"""
% =========================================================================
% CHƯƠNG 1: CƠ SỞ LÝ THUYẾT VÀ NỀN TẢNG CÔNG NGHỆ
% =========================================================================
\section{CƠ SỞ LÝ THUYẾT VÀ NỀN TẢNG CÔNG NGHỆ}

\subsection{Lý thuyết Hệ Multi-Agent (Multi-Agent Systems -- MAS)}

\subsubsection{Động lực chuyển dịch từ Single-Agent sang Multi-Agent Systems}
Trong các ứng dụng trí tuệ nhân tạo thế hệ đầu dựa trên LLM, mô hình phổ biến là \textbf{Single-Agent ReAct (Reasoning and Acting)}. Một Agent đơn lẻ tiếp nhận prompt của người dùng, thực hiện vòng lặp suy ngẫm (Thought), gọi công cụ (Action) và quan sát kết quả (Observation). Tuy nhiên, khi đối mặt với các miền bài toán chuyên sâu, đa biến và đòi hỏi tính chuẩn xác tuyệt đối như y tế lâm sàng, kiến trúc Single-Agent nhanh chóng bộc lộ các giới hạn không thể khắc phục:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Hiện tượng quá tải cửa sổ ngữ cảnh (Context Overload):} Một prompt duy nhất chứa đồng thời hướng dẫn chẩn đoán nội tiết, nguyên tắc dược thư, bảng thành phần dinh dưỡng và thuật toán vận động sẽ khiến mô hình bị phân tán chú ý (attention dilution), làm giảm độ chuẩn xác trong việc tuân thủ các quy tắc an toàn nghiêm ngặt.
    \item \textbf{Tích lũy sai số chuỗi suy luận (Error Cascading):} Nếu bước suy luận ban đầu bị sai lệch (ví dụ hiểu nhầm triệu chứng khát nước thành chẩn đoán chắc chắn đái tháo đường), các bước sau sẽ tiếp tục suy diễn sai mà không có cơ chế nào để tự phát hiện và dừng lại.
    \item \textbf{Thiếu hụt tính chuyên môn hóa và phản biện chéo:} Trong thực tế bệnh viện, không một bác sĩ đơn lẻ nào đưa ra mọi quyết định từ chẩn đoán, dinh dưỡng đến dược lý và tâm lý. Việc hội chẩn đa chuyên khoa (Multi-Specialty Consultation) là quy chuẩn bắt buộc để bảo vệ người bệnh.
\end{itemize}

Để giải quyết triệt để vấn đề này, kiến trúc \textbf{Hệ Multi-Agent (Multi-Agent Systems -- MAS)} ra đời, dựa trên nguyên lý phân rã nhiệm vụ phức tạp thành các bài toán con chuyên biệt cho các Agent độc lập có vai trò (Role), mục tiêu (Goal) và bộ công cụ (Tools) riêng biệt.

\subsubsection{Cơ sở toán học hình thức: Dec-POMDP}
Về mặt toán học hình thức, môi trường tương tác hợp tác của hệ Multi-Agent gồm $N$ Agent $\mathcal{I} = \{1, 2, \dots, N\}$ được mô hình hóa bằng \textbf{Quá trình Quyết định Markov Đa Agent Phi tập trung quan sát một phần (Decentralized Partially Observable Markov Decision Process -- Dec-POMDP)}, định nghĩa bởi bộ 8 thành phần:
\begin{equation}
    \mathcal{M} = \langle \mathcal{I}, \mathcal{S}, \{\mathcal{A}_i\}, \mathcal{P}, \{\mathcal{R}_i\}, \{\Omega_i\}, \mathcal{O}, \gamma \rangle
\end{equation}
trong đó:
\begin{itemize}[leftmargin=1.2cm]
    \item $\mathcal{S}$ là không gian trạng thái toàn cục (Global State Space), bao gồm toàn bộ hồ sơ bệnh án, các chỉ số sinh hóa máu và lịch sử tương tác.
    \item $\mathcal{A}_i$ là không gian hành động khả dĩ của Agent $i$. Không gian hành động chung của toàn hệ thống là tích Descartes $\mathbf{A} = \mathcal{A}_1 \times \mathcal{A}_2 \times \dots \times \mathcal{A}_N$. Tại mỗi bước thời gian $t$, các Agent đồng thời thực thi vector hành động chung $\mathbf{a}_t = (a_{1,t}, \dots, a_{N,t}) \in \mathbf{A}$.
    \item $\mathcal{P}(s_{t+1} \mid s_t, \mathbf{a}_t)$ là hàm phân phối xác suất chuyển trạng thái của môi trường khi chịu tác động đồng thời của vector hành động $\mathbf{a}_t$.
    \item $\mathcal{R}_i(s_t, \mathbf{a}_t)$ là hàm phần thưởng của Agent $i$. Trong hệ thống y tế DiaAgent-MAS, các Agent hoạt động theo cơ chế hợp tác hoàn toàn (Fully Cooperative MAS), nghĩa là mọi Agent đều chia sẻ chung một hàm mục tiêu tối ưu hóa an toàn và sức khỏe người bệnh: $\mathcal{R}_1 = \mathcal{R}_2 = \dots = \mathcal{R}_N = \mathcal{R}$.
    \item $\Omega_i$ là không gian quan sát cục bộ của Agent $i$. Do tính chất quan sát một phần (Partially Observable), mỗi Agent chỉ tiếp nhận tín hiệu quan sát $o_{i,t} \in \Omega_i$ được sinh ra từ trạng thái môi trường thông qua hàm quan sát xác suất $\mathcal{O}(\mathbf{o}_t \mid s_{t+1}, \mathbf{a}_t)$. Ví dụ: Agent Dược chỉ quan sát danh mục thuốc và chỉ số thận, Agent Dinh dưỡng chỉ quan sát chỉ số thể trạng và đường huyết.
    \item $\gamma \in [0, 1)$ là hệ số chiết khấu phần thưởng theo thời gian.
\end{itemize}

Mục tiêu của hệ thống là tìm kiếm tập hợp các chính sách ứng xử tối ưu $\boldsymbol{\pi}^* = (\pi_1^*, \dots, \pi_N^*)$, trong đó $\pi_i(a_{i,t} \mid h_{i,t})$ ánh xạ từ lịch sử quan sát $h_{i,t} = (o_{i,1}, a_{i,1}, \dots, o_{i,t})$ sang hành động, nhằm tối đa hóa tổng kỳ vọng phần thưởng tích lũy:
\begin{equation}
    J(\boldsymbol{\pi}) = \mathbb{E}_{\mathbf{a}_t \sim \boldsymbol{\pi}, s_{t+1} \sim \mathcal{P}} \left[ \sum_{t=0}^{\infty} \gamma^t \mathcal{R}(s_t, \mathbf{a}_t) \right]
\end{equation}

\subsubsection{Mô hình nhận thức BDI và Vòng lặp Phản biện (Reflection Loop)}
Kiến trúc nhận thức của từng Agent thông minh trong hệ thống được thiết kế theo mô hình kinh điển \textbf{BDI (Belief -- Desire -- Intention)} của Michael Bratman:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Niềm tin (Beliefs -- $\mathcal{B}$):} Tri thức mà Agent nắm giữ về tình trạng sức khỏe bệnh nhân, phác đồ điều trị hiện hành và thông điệp nhận được từ các Agent khác.
    \item \textbf{Mong muốn (Desires -- $\mathcal{D}$):} Các mục tiêu chuyên môn mà Agent hướng tới (ví dụ: đưa ra thực đơn dưới 1600 kcal/ngày, kiểm tra chống chỉ định suy thận của Metformin).
    \item \textbf{Ý định (Intentions -- $\mathcal{I}$):} Kế hoạch hành động cụ thể đã được cam kết thực hiện sau quá trình lập luận và gọi công cụ.
\end{itemize}

Đặc biệt, hệ thống tích hợp cơ chế \textbf{Reflection \& Self-Correction Loop}: Trước khi phát hành kết quả cho người bệnh, kết quả được chuyển giao cho Agent Hộ vệ An toàn (Safety Guardian Agent) để thẩm định độc lập. Nếu phát hiện vi phạm quy tắc an toàn (ví dụ: chỉ định thuốc khi chưa có xét nghiệm, hoặc không cảnh báo chống chỉ định suy thận), hệ thống kích hoạt cơ chế hồi quy (Rollback) và yêu cầu Agent chuyên trách cập nhật lại Intention của mình.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.96\textwidth]{images/fig601_mas_architecture_taxonomy.png}
    \caption{Phân loại các hình thái kiến trúc Hệ Multi-Agent (MAS Architecture Taxonomy) trong các hệ thống thông minh hiện đại.}
    \label{fig:mas_taxonomy}
\end{figure}

\subsubsection{Các mô hình điều phối Multi-Agent và đối chuẩn Framework}
Việc tổ chức tương tác giữa các Agent có thể thực hiện theo nhiều hình thái (Topologies) khác nhau như mô tả trong Hình~\ref{fig:mas_taxonomy} và Hình~\ref{fig:mas_comms}:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Điều phối tuần tự (Sequential Pipeline):} Đầu ra của Agent này là đầu vào của Agent tiếp theo. Phù hợp cho chu trình xử lý dữ liệu chuẩn từ Tiếp đón $\to$ Dự báo $\to$ Chẩn đoán $\to$ Dinh dưỡng.
    \item \textbf{Điều phối phân tầng (Hierarchical / Router-Worker):} Một Agent Điều phối trung tâm (Orchestrator) phân tích ngữ cảnh và quyết định định tuyến linh hoạt nhiệm vụ cho nhóm Agent phù hợp.
    \item \textbf{Vòng lặp Phản biện (Reflection / Guardian Loop):} Một Agent giám sát có thẩm quyền phủ quyết (Veto Power) để kiểm tra chéo và yêu cầu hiệu chỉnh khi phát hiện sai phạm chuyên môn.
\end{enumerate}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.96\textwidth]{images/fig602_mas_communication_protocols.png}
    \caption{Các giao thức truyền thông điệp (A2A Communication Protocols) và cơ chế chia sẻ bộ nhớ dùng chung trong Hệ Multi-Agent.}
    \label{fig:mas_comms}
\end{figure}

Bảng~\ref{tab:mas_frameworks} đối chuẩn kỹ thuật giữa các framework phát triển Multi-Agent hàng đầu hiện nay:

\begin{table}[H]
\centering
\footnotesize
\caption{Bảng đối chuẩn kỹ thuật giữa các nền tảng phát triển Hệ Multi-Agent}
\label{tab:mas_frameworks}
\begin{tabularx}{\textwidth}{@{} l Y Y Y Y @{}}
\toprule
\textbf{Tiêu chí} & \textbf{LangGraph} & \textbf{Microsoft AutoGen} & \textbf{CrewAI} & \textbf{DiaAgent-MAS (Hệ thống đề xuất)} \\
\midrule
Mô hình Trọng tâm & Đồ thị trạng thái có chu trình (Cyclic StateGraph) & Hội thoại nhóm đàm thoại (Conversable GroupChat) & Đóng vai tổ chức nhân sự (Role-Playing Crew) & Kiến trúc Hỗn hợp: Pipeline kết hợp Router \& Reflection Guardian \\
Cơ chế Lưu trữ & State dict tuần hoàn & Lịch sử tin nhắn Chat & Ngữ cảnh chia sẻ Task & Schema cấu trúc nghiêm ngặt (Pydantic Global State) \\
Kiểm soát Luồng & Cực cao (Điều kiện Edge) & Trung bình (Dựa vào LLM) & Trung bình (Tuần tự/Phân cấp) & Cực cao: Dual-mode Clinical Routing (Khóa/Mở ML xác định) \\
An toàn Y tế & Cần cấu hình ngoài & Dễ bị ảo giác chéo & Khó kiểm soát nhánh lặp & Tích hợp sẵn Safety Guardian với thẩm quyền phủ quyết tuyệt đối \\
Độ trễ phản hồi & 12 -- 20 giây & 15 -- 30 giây & 15 -- 25 giây & 5 -- 7 giây (Nhờ tối ưu hóa trích xuất NER có cấu trúc) \\
\bottomrule
\end{tabularx}
\end{table}

\subsection{Học máy Dự báo Nguy cơ và Khả năng Giải thích (Explainable AI -- XAI)}

\subsubsection{Thuật toán LightGBM và các đột phá tối ưu hóa}
Để dự báo định lượng xác suất nguy cơ mắc đái tháo đường từ các chỉ số sinh hóa máu và thể trạng, mô hình \textbf{LightGBM (Light Gradient Boosting Machine)} do Microsoft phát triển được lựa chọn làm mô hình học máy nòng cốt. Khác với các thuật toán Gradient Boosting truyền thống (như XGBoost hay CatBoost) duyệt qua toàn bộ mẫu dữ liệu và toàn bộ giá trị đặc trưng, LightGBM sở hữu hai cải tiến toán học vượt bậc:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Gradient-based One-Side Sampling (GOSS):} Nhận thấy rằng các mẫu có độ dốc đạo hàm (Gradient) lớn đóng góp nhiều hơn vào việc giảm hàm mất mát, GOSS giữ lại toàn bộ các mẫu có độ dốc lớn nhất (tỷ lệ $a$), và chỉ lấy mẫu ngẫu nhiên một tỷ lệ nhỏ $b$ các mẫu có độ dốc thấp. Để bù đắp cho sự thay đổi phân phối dữ liệu, các mẫu có độ dốc thấp được nhân thêm một trọng số bù $\frac{1-a}{b}$ khi tính toán độ lợi thông tin (Information Gain):
    \begin{equation}
        \tilde{V}_j(d) = \frac{1}{n} \left( \frac{\left( \sum_{x_i \in A_l} g_i + \frac{1-a}{b} \sum_{x_i \in B_l} g_i \right)^2}{n_{l}^j(d)} + \frac{\left( \sum_{x_i \in A_r} g_i + \frac{1-a}{b} \sum_{x_i \in B_r} g_i \right)^2}{n_{r}^j(d)} \right)
    \end{equation}
    Nhờ đó, mô hình tập trung học từ các ca bệnh khó mà vẫn đảm bảo tính không thiên lệch (unbiased estimation) của phân phối mẫu.
    \item \textbf{Exclusive Feature Bundling (EFB):} Trong các tập dữ liệu lâm sàng lớn, nhiều đặc trưng rời rạc (One-hot encoding) có tính chất loại trừ lẫn nhau (hiếm khi đồng thời nhận giá trị khác 0). EFB gộp các đặc trưng này thành một đặc trưng dày đặc duy nhất (Dense Bundle) thông qua bài toán tô màu đồ thị, giúp giảm mạnh số chiều không gian mà không làm mất mát thông tin.
    \item \textbf{Chiến lược phát triển cây theo chiều sâu (Leaf-wise Tree Growth):} Thay vì phát triển cây cân bằng theo từng tầng (Level-wise) như XGBoost, LightGBM lựa chọn nút lá có độ giảm tổn thất lớn nhất để phân nhánh, giúp đạt độ chuẩn xác cao hơn với cùng số lượng lá quy định.
\end{enumerate}

Hàm mất mát Log-loss nhị phân của bài toán dự đoán nguy cơ đái tháo đường ($y_i \in \{0, 1\}$) được biểu diễn bởi:
\begin{equation}
    \mathcal{L}(y, \hat{y}) = - \frac{1}{N} \sum_{i=1}^N \left[ y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right] + \sum_{k=1}^K \Omega(f_k)
\end{equation}
trong đó $\hat{y}_i = \sigma(\sum_{k=1}^K f_k(x_i))$ là xác suất dự báo sau hàm Sigmoid, và $\Omega(f_k) = \gamma T + \frac{1}{2} \lambda \|w\|^2$ là thành phần điều chuẩn chống quá khớp (Overfitting).

\subsubsection{Lý thuyết Giá trị Shapley và Phương pháp Giải thích SHAP}
Trong y tế, một mô hình đạt độ chính xác cao nhưng hoạt động như một "hộp đen" hoàn toàn không thể được đưa vào ứng dụng thực tiễn vì bác sĩ và bệnh nhân không thể biết được yếu tố nào đang thúc đẩy kết luận. Để giải quyết vấn đề này, hệ thống ứng dụng phương pháp \textbf{SHAP (SHapley Additive exPlanations)} dựa trên nền tảng lý thuyết trò chơi hợp tác của Lloyd Shapley (giải Nobel Kinh tế 2012).

Giá trị Shapley $\phi_j(x)$ biểu diễn mức đóng góp công bằng của đặc trưng thứ $j$ vào sai khác giữa giá trị dự báo của mẫu $f(x)$ so với kỳ vọng trung bình toàn bộ tập dữ liệu $\mathbb{E}[f(X)]$:
\begin{equation}
    \phi_j(x) = \sum_{S \subseteq F \setminus \{j\}} \frac{|S|! (|F| - |S| - 1)!}{|F|!} \left[ f(S \cup \{j\}) - f(S) \right]
\end{equation}
trong đó:
\begin{itemize}[leftmargin=1.2cm]
    \item $F$ là toàn bộ tập hợp $M$ đặc trưng đầu vào ($|F| = M$).
    \item $S$ là tập hợp con các đặc trưng không chứa đặc trưng $j$.
    \item $f(S)$ là giá trị dự đoán khi chỉ biết các đặc trưng trong $S$.
    \item Phân số $\frac{|S|! (|F| - |S| - 1)!}{|F|!}$ là xác suất hoán vị xuất hiện của liên minh $S$.
\end{itemize}

Mô hình giải thích SHAP thỏa mãn 4 tính chất toán học quan trọng:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Tính cộng tính địa phương (Local Accuracy):} Tổng giá trị SHAP của tất cả đặc trưng cộng với giá trị cơ sở bằng đúng đầu ra của mô hình: $f(x) = \phi_0 + \sum_{j=1}^M \phi_j(x)$.
    \item \textbf{Tính khuyết thiếu (Missingness):} Đặc trưng không có mặt trong đầu vào nhận giá trị $\phi_j = 0$.
    \item \textbf{Tính đối xứng (Symmetry):} Nếu hai đặc trưng $j$ và $k$ có đóng góp tương đương vào mọi liên minh thì $\phi_j = \phi_k$.
    \item \textbf{Tính đơn điệu (Monotonicity):} Nếu mô hình thay đổi sao cho đóng góp biên của đặc trưng $j$ luôn tăng hoặc giữ nguyên thì giá trị Shapley $\phi_j$ chắc chắn không giảm.
\end{enumerate}

Nhờ SHAP, Agent Dự báo (Risk Prediction Agent) có thể trích xuất chính xác Top-3 yếu tố rủi ro hàng đầu (ví dụ: chỉ số $\text{HbA1c} = 7.8\%$ đóng góp $+0.42$ vào xác suất bệnh; chỉ số Glucose đói $155\text{ mg/dL}$ đóng góp $+0.31$) để giải thích minh bạch cho người bệnh.

\subsection{Đồ thị Tri thức Y tế (Clinical Knowledge Graph) và Phác đồ Lâm sàng}

\subsubsection{Cấu trúc Biểu diễn Tri thức Bộ ba RDF}
Để đảm bảo các Agent không bị ảo giác về mặt y khoa, tri thức y tế cần được cấu trúc hóa dưới dạng \textbf{Đồ thị Tri thức (Knowledge Graph -- KG)}. Đồ thị tri thức biểu diễn các mối quan hệ ngữ nghĩa thông qua các bộ ba (Triples) theo chuẩn RDF:
\begin{equation}
    \mathcal{KG} = \{ (h, r, t) \mid h, t \in \mathcal{E}, \ r \in \mathcal{R}_{rel} \}
\end{equation}
trong đó $h$ là thực thể đầu (Head), $t$ là thực thể cuối (Tail), và $r$ là mối quan hệ định hướng (Relation).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.96\textwidth]{images/fig702_knowledge_graph_triples_ontology.png}
    \caption{Mô hình hóa Bản thể học (Ontology) và Cấu trúc Bộ ba Tri thức (RDF Triples) trong Y tế Lâm sàng.}
    \label{fig:kg_triples}
\end{figure}

Trong bài toán đái tháo đường, Ontology đồ thị bao gồm các lớp thực thể: $\mathcal{E} = \{\text{Bệnh lý}, \text{Triệu chứng}, \text{Thuốc}, \text{Chỉ số Xét nghiệm}, \text{Thực phẩm}, \text{Chống chỉ định}\}$; và các mối quan hệ lâm sàng: $\mathcal{R}_{rel} = \{\text{has\_symptom}, \text{indicated\_for}, \text{contraindicated\_with}, \text{adverse\_interaction}, \text{requires\_lab}\}$.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.96\textwidth]{images/fig704_diabetes_vietnam_knowledge_graph.png}
    \caption{Đồ thị Tri thức Chuyên biệt Quản trị Bệnh Đái Tháo Đường tại Việt Nam: Phác đồ Bộ Y Tế 5481, Tương tác Dược lý và Dinh dưỡng Thực phẩm Việt.}
    \label{fig:diabetes_kg}
\end{figure}

\subsubsection{Không Gian Biểu Diễn Vector Tiềm Ẩn (Node \& Link Embeddings)}
Để hỗ trợ các tác vụ suy luận ngữ nghĩa nhanh và tìm kiếm lân cận tương đồng trong chẩn đoán, toàn bộ 143 nút thực thể và 271 mối liên kết trong Đồ thị Tri thức Neo4j DiaAgent-MAS được chiếu vào một \textbf{Không gian Vector Nhúng Tiềm ẩn (Latent Node Embedding Space)} thông qua thuật toán bố trí lực lò xo Force-Directed Graph Layout kết hợp vector tiên nghiệm phân cụm ngữ nghĩa (Semantic Clustering Priors) (Hình~\ref{fig:kg_node_embeddings}).

Trong không gian nhúng 2 chiều:
\begin{itemize}[leftmargin=1.2cm]
    \item Các nút có cùng vai trò chuyên môn tự động hội tụ thành các cụm mật độ cao (Dense Clusters) được bao quanh bởi các đường bao mây: Cụm Dược chất phác đồ Bộ Y Tế và ADA (Metformin, Gliclazide, SGLT-2i, DPP-4i, GLP-1 RA, Insulin), Cụm 30 Biệt dược và Thiết bị y tế thương mại FPT Long Châu (Glucophage, Diamicron, Jardiance, Forxiga, Máy đo và que thử Accu-Chek, Sữa Glucerna), Cụm 14 Chỉ số sinh học xét nghiệm (HbA1c, FPG, OGTT, RPG, eGFR, Creatinine, UACR, BMI, Huyết áp, Lipid), Cụm Triệu chứng lâm sàng kinh điển (Hội chứng 4 nhiều, nhìn mờ, tê bì bàn chân, vết thương lâu lành từ Vinmec), Cụm Bệnh lý và Biến chứng đa cơ quan (CKD, ASCVD, Suy tim, Võng mạc, Thần kinh, Loét bàn chân), Cụm Dinh dưỡng 29 món ăn Việt Nam (NIN) và Cụm Cảnh báo an toàn (Nhiễm toan Lactic, Hạ đường huyết, Toan Ceton).
    \item Các liên kết quan hệ định hướng (\texttt{TREATS}, \texttt{CONTRAINDICATED\_IN}, \texttt{RISK\_OF}, \texttt{HIGHLY\_RECOMMENDED\_FOR}, \texttt{DIAGNOSED\_BY}, \texttt{HAS\_SYMPTOM}, \texttt{CAN\_BE\_REPLACED\_BY}, \texttt{DISPENSED\_AS\_PRODUCT}) kết nối trực tiếp các vector nhúng, phản ánh toàn vẹn tô-pô phác đồ và cơ chế rà soát an toàn dược lý đa tầng của hệ thống.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.98\textwidth]{images/fig_kg_node_embeddings.png}
    \caption{Không Gian Vector Embedding 2D (Force-Directed Graph Layout \& Semantic Clustering) Biểu Diễn 143 Node Thực Thể và 271 Mối Quan Hệ Liên Kết Lâm Sàng trong Đồ Thị Tri Thức Neo4j DiaAgent-MAS.}
    \label{fig:kg_node_embeddings}
\end{figure}

\subsubsection{Chuẩn hóa Phác đồ Đái Tháo Đường Type 2 theo Quyết định 5481/QĐ-BYT}
Hệ thống DiaAgent-MAS số hóa và áp dụng nghiêm ngặt các quy định chuyên môn từ \textbf{Quyết định số 5481/QĐ-BYT ngày 30/12/2020 của Bộ Trưởng Bộ Y Tế Việt Nam} về việc ban hành tài liệu chuyên môn "Hướng dẫn chẩn đoán và điều trị đái tháo đường típ 2":
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Tiêu chuẩn vàng khẳng định chẩn đoán đái tháo đường:}
    Bắt buộc phải dựa vào kết quả xét nghiệm định lượng từ mẫu huyết tương tĩnh mạch thực hiện tại phòng xét nghiệm chuẩn, thỏa mãn ít nhất một trong 4 tiêu chuẩn:
    \begin{itemize}[leftmargin=0.8cm]
        \item Glucose huyết tương lúc đói (Fasting Plasma Glucose -- FPG) $\ge 126\text{ mg/dL}$ ($\ge 7.0\text{ mmol/L}$) sau ít nhất 8 giờ nhịn ăn.
        \item Glucose huyết tương ở thời điểm 2 giờ sau nghiệm pháp dung nạp 75g glucose đường uống (OGTT) $\ge 200\text{ mg/dL}$ ($\ge 11.1\text{ mmol/L}$).
        \item $\text{HbA1c} \ge 6.5\%$ ($48\text{ mmol/mol}$) thực hiện theo phương pháp chuẩn hóa NGSP/DCCT.
        \item Bệnh nhân có các triệu chứng lâm sàng kinh điển của tăng đường huyết (khát nhiều, uống nhiều, tiểu nhiều, sụt cân không rõ nguyên nhân) kèm theo một mẫu glucose huyết tương bất kỳ $\ge 200\text{ mg/dL}$ ($\ge 11.1\text{ mmol/L}$).
    \end{itemize}
    \begin{tcolorbox}[colback=warnbg,colframe=warnframe,title=Nguyên tắc An toàn Bắt buộc theo QĐ 5481/QĐ-BYT]
    Tuyệt đối KHÔNG sử dụng các triệu chứng lâm sàng đơn thuần hoặc que thử mao mạch nhanh để khẳng định chẩn đoán xác định đái tháo đường. Khi bệnh nhân chưa có kết quả xét nghiệm máu định lượng, hệ thống CHỈ ĐƯỢC PHÉP xếp bệnh nhân vào diện "Sàng lọc nguy cơ" và hướng dẫn đi làm xét nghiệm, tuyệt đối KHÔNG chỉ định thuốc điều trị đặc trị.
    \end{tcolorbox}
    \item \textbf{Phác đồ điều trị và các chống chỉ định thuốc cốt tử:}
    \begin{itemize}[leftmargin=0.8cm]
        \item \textbf{Thuốc đầu tay (First-line Therapy):} \textit{Metformin} là lựa chọn ưu tiên hàng đầu ngay khi được chẩn đoán đái tháo đường típ 2, kết hợp với thay đổi lối sống.
        \item \textbf{Chống chỉ định suy giảm chức năng thận của Metformin:}
        Theo QĐ 5481/QĐ-BYT, việc sử dụng Metformin bắt buộc phải căn cứ vào Độ lọc cầu thận ước tính (eGFR):
        \begin{equation}
            \text{eGFR} = \begin{cases}
                \ge 60\text{ mL/phút/1.73m}^2: & \text{Liều tối đa 2000 -- 2500 mg/ngày (An toàn)} \\
                45 \le \text{eGFR} < 60: & \text{Liều tối đa 1500 mg/ngày, theo dõi mỗi 3--6 tháng} \\
                30 \le \text{eGFR} < 45: & \text{Liều tối đa 1000 mg/ngày (Thận trọng, giảm 50\% liều)} \\
                < 30\text{ mL/phút/1.73m}^2: & \textbf{CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI}
            \end{cases}
        \end{equation}
        \item \textbf{Tương tác nghiêm trọng giữa Metformin và Rượu bia:}
        Cồn (Ethanol) ức chế quá trình tân tạo đường tại gan và cạnh tranh chuyển hóa với acid lactic, làm tăng đột biến nguy cơ \textbf{Nhiễm toan Acid Lactic (Lactic Acidosis)} cấp tính -- một biến chứng có tỷ lệ tử vong lên tới 50\%. Bệnh nhân đang sử dụng Metformin bắt buộc phải kiêng tuyệt đối rượu bia.
    \end{itemize}
\end{enumerate}

\subsubsection{Cơ sở Dữ liệu Dinh dưỡng theo Viện Dinh Dưỡng Quốc Gia (NIN)}
Hệ thống DiaAgent-MAS tích hợp bảng thành phần dinh dưỡng thực phẩm Việt Nam của Viện Dinh Dưỡng Quốc Gia (NIN). Chế độ can thiệp dinh dưỡng y khoa (Medical Nutrition Therapy -- MNT) cho người bệnh đái tháo đường tại Việt Nam được cá nhân hóa dựa trên:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Tổng năng lượng hàng ngày (Total Daily Energy Expenditure -- TDEE):}
    Tính toán dựa trên chỉ số khối cơ thể (BMI) và mức độ tiêu hao năng lượng do hoạt động thể lực:
    \begin{equation}
        E_{target} = W_{ideal} \times k_{activity}
    \end{equation}
    trong đó cân nặng lý tưởng của người Việt Nam tính theo công thức: $W_{ideal} = (\text{Chiều cao (cm)} - 100) \times 0.9$. Hệ số vận động $k_{activity} = 25\text{ kcal/kg}$ với người nằm viện hoặc ít vận động; $k_{activity} = 30\text{ kcal/kg}$ với lao động nhẹ; và $35\text{ kcal/kg}$ với lao động vừa. Đối với người thừa cân/béo phì ($\text{BMI} \ge 23\text{ kg/m}^2$ theo chuẩn châu Á IDI \& WPRO), năng lượng nạp vào giảm 500 kcal/ngày để hướng tới giảm 5--10\% trọng lượng cơ thể.
    \item \textbf{Tỷ lệ phân bổ các chất đa lượng (Macronutrient Distribution):}
    \begin{itemize}[leftmargin=0.8cm]
        \item Carbohydrate (Tinh bột): 50 -- 60\% tổng năng lượng. Ưu tiên tinh bột có chỉ số đường huyết thấp ($\text{GI} < 55$), giàu chất xơ hòa tan (gạo lứt, yến mạch, các loại đậu). Hạn chế tối đa carbohydrate hấp thu nhanh ($\text{GI} > 70$ như đường tinh luyện, nước ngọt, bánh mì trắng).
        \item Protein (Chất đạm): 15 -- 20\% tổng năng lượng ($1.0 - 1.2\text{ g/kg/ngày}$). Nếu có suy thận mạn ($\text{eGFR} < 60$), tỷ lệ đạm giảm xuống $0.8\text{ g/kg/ngày}$ để làm chậm tiến triển suy thận.
        \item Lipid (Chất béo): 20 -- 25\% tổng năng lượng. Chất béo bão hòa $< 7\%$, cholesterol $< 200\text{ mg/ngày}$, không sử dụng chất béo chuyển hóa (trans fat).
    \end{itemize}
\end{itemize}
"""
