# sections/chapter1_history.py

def get_chapter1():
    return r"""
% =========================================================================
% CHƯƠNG 1: LỊCH SỬ PHÁT TRIỂN TRÍ TUỆ NHÂN TẠO
% =========================================================================
\chapter{Lịch Sử Phát Triển Trí Tuệ Nhân Tạo}

\section{Tổng Quan Bức Tranh Lịch Sử 75 Năm Của AI}

Lịch sử phát triển của Trí tuệ Nhân tạo (Artificial Intelligence -- AI) không phải là một đường thẳng tịnh tiến liên tục, mà là một chuỗi các chu kỳ dao động mạnh mẽ giữa những giai đoạn bùng nổ kỳ vọng (hype cycles) và những thời kỳ thoái trào sâu sắc được gọi là “Mùa đông AI” (AI Winters). Trải qua hơn 7 thập kỷ kể từ những ý niệm đầu tiên vào thập niên 1950 đến kỷ nguyên bùng nổ của AI Tạo sinh và Hệ đa Agent hiện nay, AI đã chứng kiến sự chuyển dịch căn bản trong hệ hình tư duy tính toán (computational paradigm): từ suy diễn logic hình thức dựa trên ký hiệu sang mô hình hóa xác suất thống kê, và đỉnh cao là học biểu diễn phân cấp phi tuyến tính với học sâu.

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth]{images/fig101_ai_evolution_timeline.png}
    \caption{Dòng thời gian tiến hóa Trí tuệ Nhân tạo (1950 -- 2026): Các mốc bước ngoặt lịch sử và sự chuyển dịch mô hình tính toán.}
    \label{fig:ai_timeline}
\end{figure}

Hình~\ref{fig:ai_timeline} tổng kết 15 cột mốc then chốt xác lập quỹ đạo phát triển của AI. Để thấu hiểu sâu sắc bản chất của các mô hình học máy và học sâu hiện đại, việc khảo cứu nguồn gốc lịch sử, các thất bại mang tính hệ thống trong quá khứ và động lực thúc đẩy các cuộc cách mạng công nghệ là một yêu cầu học thuật thiết yếu.

\section{Khởi Nguồn và Kỷ Nguyên Logic Biểu Tượng (1940s -- 1960s)}

\subsection{Ý Niệm Về Máy Tính Có Tư Duy và Phép Thử Turing}
Khởi nguồn lý thuyết của AI bắt đầu từ công trình kinh điển của nhà toán học Alan Turing vào năm 1950 với bài báo mang tựa đề \textit{“Computing Machinery and Intelligence”} đăng trên tạp chí \textit{Mind}. Trong công trình này, Turing đã đặt ra câu hỏi mang tính bản lề: \textit{“Máy móc có thể tư duy được hay không?”} (Can machines think?). Để tránh những tranh cãi trừu tượng về khái niệm ý thức và tư duy, ông đã đề xuất một phép thử thực nghiệm hành vi mang tên \textit{“Trò chơi bắt chước”} (The Imitation Game), ngày nay được biết đến rộng rãi với tên gọi \textbf{Phép thử Turing (Turing Test)}.

Theo tiêu chí của Turing, một cỗ máy được coi là có trí tuệ nếu trong một cuộc giao tiếp bằng văn bản được che giấu (blind text test), một người thẩm vấn bình thường không thể phân biệt được đối tượng đang trò chuyện là một con người hay là một chương trình máy tính. Dù còn nhiều tranh luận triết học, Phép thử Turing đã đặt nền móng phương pháp luận đầu tiên cho việc định lượng hóa hành vi thông minh nhân tạo.

\subsection{Mô Hình Nơ-ron Hình Thức và Hội Thảo Dartmouth (1956)}
Trước công trình của Turing, vào năm 1943, Warren McCulloch (nhà thần kinh học) và Walter Pitts (nhà logic học) đã công bố mô hình nơ-ron hình thức đầu tiên (McCulloch-Pitts Neuron). Họ đã chứng minh rằng các nơ-ron sinh học được đơn giản hóa có thể thực thi các phép toán logic cơ bản như AND, OR, NOT thông qua cơ chế tổng tích lũy tín hiệu đầu vào và so sánh với một ngưỡng kích hoạt:
\begin{equation}
y = f\left(\sum_{i=1}^n w_i x_i - \theta\right)
\end{equation}
trong đó $x_i \in \{0, 1\}$ là tín hiệu nhị phân đầu vào, $w_i$ là trọng số liên kết, $\theta$ là ngưỡng kích hoạt, và $f(\cdot)$ là hàm bước nhảy Heaviside. Đến năm 1949, Donald Hebb đề xuất quy tắc học Hebbian (\textit{“Neurons that fire together, wire together”}), đặt cơ sở cho việc thay đổi độ mạnh liên kết khớp thần kinh sinh học.

Bước ngoặt lịch sử chính thức khai sinh ra ngành khoa học Trí tuệ Nhân tạo diễn ra vào mùa hè năm 1956 tại \textbf{Hội thảo Dartmouth (Dartmouth Summer Research Project on Artificial Intelligence)} do John McCarthy (Đại học Dartmouth), Marvin Minsky (Đại học Harvard), Claude Shannon (Bell Labs) và Nathaniel Rochester (IBM) đồng tổ chức. Chính tại hội thảo này, John McCarthy đã đề xuất thuật ngữ \textbf{“Artificial Intelligence”} với mệnh đề cốt lõi: \textit{“Mọi khía cạnh của việc học hỏi hay bất kỳ đặc tính nào khác của trí tuệ về nguyên tắc đều có thể được mô tả chính xác đến mức một cỗ máy có thể được chế tạo để mô phỏng nó”}.

\subsection{Perceptron của Rosenblatt và Các Hệ Suy Diễn Ký Hiệu Đầu Tiên}
Năm 1957, Frank Rosenblatt tại Phòng thí nghiệm Hàng không Cornell đã chế tạo thành công mô hình phần cứng \textbf{Perceptron} trên máy tính IBM 704. Khác với nơ-ron McCulloch-Pitts vốn có trọng số cố định, Perceptron là mô hình nơ-ron nhân tạo đầu tiên có khả năng \textit{tự động học trọng số} từ dữ liệu mẫu thông qua thuật toán học có giám sát:
\begin{equation}
\mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} + \eta (y - \hat{y}) \mathbf{x}
\end{equation}
với $\eta > 0$ là tốc độ học (learning rate), $y \in \{0, 1\}$ là nhãn thực tế và $\hat{y}$ là nhãn dự báo. Định lý hội tụ Perceptron (Perceptron Convergence Theorem) của Rosenblatt chứng minh rằng nếu tập dữ liệu khả phân tuyến tính (linearly separable), thuật toán chắc chắn sẽ hội tụ về một siêu phẳng phân tách sau một số hữu hạn các bước lặp.

Song song với hướng tiếp cận kết nối (connectionism) của Perceptron, nhánh tiếp cận biểu tượng (symbolic AI) cũng đạt được những thành tựu rực rỡ với \textit{Logic Theorist} (1956) của Allen Newell, Herbert Simon và Cliff Shaw -- chương trình máy tính đầu tiên chứng minh được 38 trên 52 định lý trong chương 2 cuốn \textit{Principia Mathematica} của Russell và Whitehead. Tiếp sau đó là chương trình \textit{General Problem Solver (GPS)} (1959) sử dụng kỹ thuật phân tích phương tiện -- cứu cánh (means-ends analysis) để giải quyết các bài toán giải đố hình thức.

\section{“Mùa Đông AI” Lần Thứ Nhất (1970s)}

\subsection{Giới Hạn Toán Học Của Perceptron và Cuốn Sách Của Minsky \& Papert (1969)}
Sự lạc quan tột độ trong thập niên 1960 nhanh chóng nhường chỗ cho một cuộc khủng hoảng học thuật sâu sắc. Năm 1969, Marvin Minsky và Seymour Papert xuất bản cuốn sách mang tính bước ngoặt \textbf{\textit{“Perceptrons: An Introduction to Computational Geometry”}}. Bằng các chứng minh hình học và đại số chặt chẽ, hai tác giả đã chỉ ra một hạn chế căn bản: \textbf{Perceptron đơn tầng không có khả năng giải quyết các bài toán phi tuyến tính cơ bản, điển hình là hàm logic XOR (Exclusive-OR)}.

\begin{table}[H]
\centering
\caption{Bảng chân lý hàm logic XOR chứng minh tính chất không khả phân tuyến tính}
\label{tab:xor_truth_table}
\begin{tabularx}{0.75\textwidth}{>{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\raggedright\arraybackslash}X}
\toprule
\textbf{Đầu vào $x_1$} & \textbf{Đầu vào $x_2$} & \textbf{Đầu ra $y = x_1 \oplus x_2$} & \textbf{Vị trí hình học trên mặt phẳng $\mathbb{R}^2$} \\
\midrule
0 & 0 & 0 & Gốc tọa độ $(0, 0)$ -- Nhãn âm \\
0 & 1 & 1 & Điểm $(0, 1)$ -- Nhãn dương \\
1 & 0 & 1 & Điểm $(1, 0)$ -- Nhãn dương \\
1 & 1 & 0 & Điểm $(1, 1)$ -- Nhãn âm \\
\bottomrule
\end{tabularx}
\end{table}

Để phân tách nhãn dương $\{ (0,1), (1,0) \}$ khỏi nhãn âm $\{ (0,0), (1,1) \}$, không tồn tại bất kỳ một đường thẳng nào dạng $w_1 x_1 + w_2 x_2 + b = 0$ có thể chia đôi mặt phẳng sao cho hai nhóm điểm nằm về hai phía đối lập. Mặc dù Minsky và Papert thừa nhận rằng mạng nơ-ron nhiều tầng (multilayer networks) có thể giải quyết được bài toán phi tuyến tính, nhưng vào thời điểm đó, chưa một ai tìm ra được giải thuật toán học hiệu quả để huấn luyện các trọng số ở các tầng ẩn (hidden layers). Cuốn sách đã giáng một đòn chí mạng vào cộng đồng nghiên cứu mạng nơ-ron, khiến các cơ quan tài trợ gần như đóng băng toàn bộ nguồn lực dành cho hướng tiếp cận kết nối.

\subsection{Báo Cáo Lighthill (1973) và Sự Cắt Giảm Tài Trợ Của DARPA}
Tại Vương quốc Anh, Hội đồng Nghiên cứu Khoa học (SRC) đã ủy quyền cho Giáo sư James Lighthill tiến hành đánh giá độc lập về thực trạng nghiên cứu AI. Năm 1973, \textbf{Báo cáo Lighthill (Lighthill Report)} được công bố với những kết luận vô cùng bi quan. Lighthill chỉ ra rằng các hệ thống AI biểu tượng chỉ hoạt động được trong các “thế giới đồ chơi” (toy worlds) vô cùng hạn hẹp và hoàn toàn bất lực trước các bài toán thực tế do hiện tượng \textbf{bùng nổ tổ hợp (combinatorial explosion)}. Số lượng trạng thái tìm kiếm tăng theo hàm mũ đối với kích thước bài toán, vượt xa khả năng xử lý của mọi hệ thống máy tính đương thời.

Báo cáo Lighthill đã dẫn đến việc chính phủ Anh chấm dứt tài trợ nghiên cứu AI tại hầu hết các trường đại học (ngoại trừ Edinburgh, Sussex và Essex). Cùng thời điểm đó tại Hoa Kỳ, Cơ quan Chỉ đạo các Dự án Nghiên cứu Tiên tiến Quốc phòng (DARPA) cũng áp dụng Đạo luật Mansfield, cắt giảm các khoản tài trợ cho nghiên cứu cơ bản không có ứng dụng quân sự trực tiếp. Giai đoạn 1974 -- 1980 chính thức đi vào lịch sử với tên gọi \textbf{“Mùa đông AI lần thứ nhất”}.

\section{Sự Trỗi Dậy Của Hệ Chuyên Gia và “Mùa Đông AI” Lần Thứ Hai (1980s -- 1990s)}

\subsection{Kỷ Nguyên Vàng Của Hệ Chuyên Gia (Expert Systems)}
Đầu thập niên 1980, AI phục hưng mạnh mẽ nhờ sự chuyển dịch từ tìm kiếm tổng quát sang biểu diễn tri thức chuyên gia trong các miền hẹp (domain-specific knowledge). Đây là thời kỳ hoàng kim của \textbf{Hệ Chuyên gia (Expert Systems)}. Khác với các thuật toán tối ưu toán học, hệ chuyên gia mô phỏng quá trình ra quyết định của các chuyên gia con người thông qua việc tách biệt rõ ràng giữa hai thành phần:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Cơ sở tri thức (Knowledge Base):} Lưu trữ các sự kiện và tập luật dưới dạng các mệnh đề điều kiện \texttt{IF <điều kiện> THEN <hành động/kết luận>}.
    \item \textbf{Máy suy diễn (Inference Engine):} Động cơ thực thi logic, vận hành theo cơ chế suy diễn tiến (Forward Chaining -- từ dữ kiện suy ra kết luận) hoặc suy diễn lùi (Backward Chaining -- từ giả thuyết truy ngược về dữ kiện cần chứng minh).
\end{enumerate}

Các hệ chuyên gia tiêu biểu giai đoạn này bao gồm:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{DENDRAL (Đại học Stanford):} Phân tích phổ khối lượng để xác định cấu trúc phân tử hóa học hữu cơ.
    \item \textbf{MYCIN (Đại học Stanford):} Chẩn đoán các bệnh nhiễm trùng máu và đề xuất phác đồ kháng sinh, đạt tỷ lệ chẩn đoán chính xác tương đương các bác sĩ chuyên khoa hàng đầu.
    \item \textbf{XCON / R1 (Đại học Carnegie Mellon \& Digital Equipment Corporation - DEC):} Hệ thống thương mại hóa thành công rực rỡ nhất, tự động cấu hình các hệ thống máy tính VAX theo đơn đặt hàng của khách hàng, giúp DEC tiết kiệm ước tính hơn 40 triệu USD mỗi năm vào năm 1986.
\end{itemize}

Sự thành công của XCON đã châm ngòi cho một làn sóng đầu tư thương mại khổng lồ vào các công ty khởi nghiệp phần cứng chuyên dụng chạy ngôn ngữ Lisp (Lisp Machines như Symbolics, LMI) và các dự án quốc gia quy mô lớn như Dự án Máy tính Thế hệ thứ Năm (Fifth Generation Computer Systems - FGCS) của Nhật Bản với ngân sách hàng trăm triệu USD.

\subsection{Sự Tái Sinh Của Mạng Nơ-ron: Giải Thuật Lan Truyền Ngược (1986)}
Trong khi hệ chuyên gia thống trị về mặt thương mại, hướng tiếp cận mạng nơ-ron đã âm thầm tạo nên bước đột phá khoa học quan trọng nhất của thế kỷ 20. Năm 1986, David Rumelhart, Geoffrey Hinton và Ronald Williams đã công bố bài báo lịch sử trên tạp chí \textit{Nature}: \textit{“Learning representations by back-propagating errors”}.

Công trình này đã phổ biến rộng rãi giải thuật \textbf{Lan truyền ngược (Backpropagation)} cho mạng nơ-ron đa tầng (Multilayer Perceptron -- MLP). Bằng cách áp dụng quy tắc dây chuyền của giải tích vi phân (chain rule of calculus) kết hợp với các hàm kích hoạt phi tuyến khả vi liên tục (như hàm Sigmoid $\sigma(z) = \frac{1}{1 + e^{-z}}$), giải thuật cho phép tính toán đạo hàm riêng của hàm mất mát $L$ đối với từng trọng số ở bất kỳ tầng ẩn nào trong mạng:
\begin{equation}
\frac{\partial L}{\partial w_{ij}^{(l)}} = \delta_i^{(l)} \cdot a_j^{(l-1)}
\end{equation}
với $\delta_i^{(l)}$ là sai số truyền ngược tại nơ-ron $i$ của tầng $l$, và $a_j^{(l-1)}$ là giá trị kích hoạt của nơ-ron $j$ tại tầng trước đó. Đột phá này đã phá vỡ hoàn toàn “lời nguyền XOR” của Minsky và Papert, chứng minh rằng mạng nơ-ron hoàn toàn có thể tự động học các biểu diễn đặc trưng ẩn phi tuyến tính phức tạp. Cũng trong giai đoạn này, Kunihiko Fukushima (1980) công bố mô hình \textbf{Neocognitron}, đưa ra khái niệm xếp chồng các tầng trích xuất đặc trưng (S-cells) và tầng bất biến vị trí (C-cells), đặt nền tảng kiến trúc trực tiếp cho Mạng nơ-ron Tích chập (CNN) sau này.

\subsection{“Mùa Đông AI” Lần Thứ Hai (1987 -- 1993)}
Tuy nhiên, sự bùng nổ thương mại của hệ chuyên gia nhanh chóng bộc lộ những rạn nứt cấu trúc nghiêm trọng:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Điểm nghẽn thu nhận tri thức (Knowledge Acquisition Bottleneck):} Việc phỏng vấn các chuyên gia con người để mã hóa tri thức thành hàng vạn luật logic là một quá trình cực kỳ tốn kém, chậm chạp và dễ phát sinh mâu thuẫn.
    \item \textbf{Tính giòn (Brittleness) và Khủng hoảng bảo trì:} Khi cơ sở tri thức tăng lên quy mô hàng chục nghìn luật, sự tương tác phức tạp giữa các luật dẫn đến các vòng lặp vô tận hoặc kết luận sai lệch khi gặp các tình huống nằm ngoài biên tri thức đã định nghĩa. Chi phí bảo trì hệ thống vượt xa lợi ích kinh tế mang lại.
    \item \textbf{Sự sụp đổ của thị trường phần cứng Lisp:} Cuối thập niên 1980, sự phát triển vượt bậc của vi xử lý thông dụng x86 (Intel 386, 486) và các máy trạm Unix (Sun Microsystems) đã khiến các máy tính chuyên dụng Lisp Machines đắt đỏ trở nên lỗi thời về hiệu năng trên chi phí. Thị trường Lisp sụp đổ kéo theo hàng loạt công ty AI phá sản.
\end{itemize}

Cuộc khủng hoảng này đã mở ra \textbf{“Mùa đông AI lần thứ hai”} kéo dài từ 1987 đến đầu thập niên 1990.

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth]{images/fig102_ai_winters_and_hype_cycles.png}
    \caption{Chu kỳ kỳ vọng và hai thời kỳ “Mùa đông AI” (AI Winters) trong tiến trình 75 năm lịch sử.}
    \label{fig:ai_winters}
\end{figure}

Hình~\ref{fig:ai_winters} trực quan hóa các chu kỳ kỳ vọng (Hype Cycles) và hai giai đoạn “Mùa đông AI”. Đồ thị cho thấy sau mỗi cuộc khủng hoảng thoái trào, cộng đồng khoa học lại tái cấu trúc nền tảng phương pháp luận, chuyển dịch sang các mô hình thực dụng và có cơ sở toán học vững chắc hơn.

\section{Kỷ Nguyên Học Máy Thống Kê Thực Nghiệm (1990s -- 2010)}

Sau thất bại của các hệ chuyên gia dựa trên luật, cộng đồng AI đã rút ra một bài học sống còn: \textbf{Thay vì cố gắng lập trình thủ công toàn bộ các quy tắc tri thức phức tạp của thế giới, hãy để máy tính tự học các quy luật xác suất thống kê trực tiếp từ dữ liệu thực nghiệm}.

\subsection{Lý Thuyết Học Thống Kê và Máy Vector Hỗ Trợ (SVM)}
Thập niên 1990 chứng kiến sự trỗi dậy áp đảo của \textbf{Lý thuyết Học Thống kê (Statistical Learning Theory)} do Vladimir Vapnik và Alexey Chervonenkis hoàn thiện. Trọng tâm của lý thuyết này là nguyên lý Cực tiểu hóa Rủi ro Cấu trúc (Structural Risk Minimization -- SRM), nhằm kiểm soát sự cân bằng giữa sai số trên tập huấn luyện và năng lực khái quát hóa thông qua chiều VC (Vapnik-Chervonenkis Dimension).

Đỉnh cao của giai đoạn này là sự ra đời của \textbf{Máy Vector Hỗ trợ (Support Vector Machines -- SVM)} (Boser, Guyon \& Vapnik, 1992; Cortes \& Vapnik, 1995). Khác với Perceptron vốn tìm bất kỳ mặt phân cách nào, SVM tìm kiếm siêu phẳng tối ưu có khoảng cách biên (margin) lớn nhất tới các điểm dữ liệu gần nhất (support vectors):
\begin{equation}
\min_{\mathbf{w}, b} \frac{1}{2} \|\mathbf{w}\|^2 \quad \text{thỏa mãn} \quad y_i (\mathbf{w}^T \mathbf{x}_i + b) \ge 1, \quad \forall i
\end{equation}
Đặc biệt, thông qua \textbf{Kỹ thuật biến đổi hàm nhân (Kernel Trick)} (Mercer's Theorem), SVM cho phép ánh xạ ngầm các vector dữ liệu vào không gian đặc trưng vô hạn chiều (với nhân RBF Gaussian: $K(\mathbf{x}, \mathbf{x}') = \exp(-\gamma \|\mathbf{x} - \mathbf{x}'\|^2)$) để giải quyết các bài toán phi tuyến tính phức tạp mà không làm gia tăng độ phức tạp tính toán. Với nền tảng toán học tối ưu hóa lồi toàn cục (Convex Optimization) tuyệt đối không rơi vào cực tiểu cục bộ, SVM đã đánh bại hoàn toàn mạng nơ-ron đa tầng trên hầu hết các bài toán thị giác và phân loại văn bản trong suốt hơn một thập kỷ.

\subsection{Cây Quyết Định và Các Phương Pháp Học Tập Hợp (Ensemble Learning)}
Bên cạnh SVM, các phương pháp học tập hợp (Ensemble Learning) cũng xác lập vị thế thống trị trên dữ liệu bảng:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Cây quyết định (Decision Trees):} Các thuật toán CART (Breiman et al., 1984) và C4.5 (Quinlan, 1993) cung cấp khả năng diễn giải trực quan dựa trên chỉ số tạp chất Gini và độ lợi thông tin (Information Gain).
    \item \textbf{Boosting (AdaBoost):} Yoav Freund và Robert Schapire (1996) đề xuất giải thuật AdaBoost, chứng minh định lý toán học rằng có thể kết hợp tuyến tính nhiều bộ phân loại yếu (weak learners) để tạo thành một bộ phân loại mạnh (strong learner). Sau đó, Jerome Friedman (2001) tổng quát hóa thành Gradient Boosting Machine (GBM).
    \item \textbf{Rừng ngẫu nhiên (Random Forest):} Leo Breiman (2001) kết hợp kỹ thuật lấy mẫu lặp lại (Bootstrap Aggregating -- Bagging) với việc chọn tập con đặc trưng ngẫu nhiên (Random Feature Subsampling) để giảm phương sai (variance) của mô hình cây mà không làm tăng độ chệch (bias), tạo ra thuật toán học máy mạnh mẽ và ổn định nhất cho dữ liệu cấu trúc bảng.
\end{itemize}

\subsection{LeNet-5 (1998) -- Nền Tảng Của Mạng Tích Chập Hiện Đại}
Năm 1998, Yann LeCun cùng các cộng sự tại AT\&T Bell Labs đã công bố bài báo lịch sử \textit{“Gradient-based learning applied to document recognition”}, giới thiệu kiến trúc \textbf{LeNet-5}. LeNet-5 tích hợp hoàn chỉnh ba ý tưởng kiến trúc cốt lõi:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Vùng tiếp nhận cục bộ (Local Receptive Fields):} Nơ-ron chỉ kết nối với một vùng lân cận không gian nhỏ của ảnh đầu vào.
    \item \textbf{Chia sẻ trọng số (Shared Weights):} Một bộ lọc (filter) quét qua toàn bộ ảnh, giảm mạnh số lượng tham số tự do và tạo tính bất biến tịnh tiến.
    \item \textbf{Lấy mẫu giảm dần (Sub-sampling / Pooling):} Giảm độ phân giải không gian của bản đồ đặc trưng, tăng cường khả năng chống nhiễu dịch chuyển và co dãn hình học.
\end{enumerate}
LeNet-5 đã được triển khai thương mại hóa thành công rực rỡ, xử lý hàng triệu tờ séc ngân hàng mỗi ngày trên khắp hệ thống ngân hàng Hoa Kỳ. Tuy nhiên, do giới hạn về năng lực tính toán của CPU và sự thiếu hụt các tập dữ liệu ảnh quy mô lớn vào thời điểm đó, mô hình này chưa thể mở rộng ra các bài toán nhận dạng ảnh tự nhiên phức tạp hơn.

\section{Cuộc Cách Mạng Học Sâu (Deep Learning Boom, 2012 -- 2020)}

\subsection{Bước Ngoặt Lịch Sử ImageNet 2012 và AlexNet}
Năm 2012 được ghi nhận là mốc khởi đầu của cuộc cách mạng học sâu hiện đại. Tại cuộc thi nhận dạng hình ảnh quy mô lớn thế giới \textbf{ImageNet Large Scale Visual Recognition Challenge (ILSVRC 2012)}, nhóm nghiên cứu của Đại học Toronto gồm Alex Krizhevsky, Ilya Sutskever và Geoffrey Hinton đã giới thiệu mô hình mạng nơ-ron tích chập sâu mang tên \textbf{AlexNet}.

Kết quả thi đấu đã gây chấn động toàn bộ cộng đồng khoa học máy tính: AlexNet đạt tỷ lệ sai số Top-5 là \textbf{15.3\%}, bỏ xa mô hình đứng thứ hai (sử dụng phương pháp học máy truyền thống kết hợp trích xuất đặc trưng thủ công SIFT/HOG + SVM) với sai số \textbf{26.2\%}. Mức chênh lệch hơn 10.9\% sai số tuyệt đối đã chứng minh tính ưu việt áp đảo của việc học biểu diễn tự động (end-to-end representation learning) so với kỹ nghệ đặc trưng thủ công (hand-crafted feature engineering).

Cuộc cách mạng này được thúc đẩy bởi sự hội tụ đồng thời của \textbf{“Bộ ba trụ cột” (The Holy Trinity of Deep Learning)}:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Dữ liệu quy mô lớn (Big Data):} Tập dữ liệu ImageNet do Fei-Fei Li và cộng sự xây dựng chứa hơn 1.2 triệu ảnh có gán nhãn thuộc 1,000 phân lớp đối tượng tự nhiên khác nhau, cung cấp đủ bằng chứng thống kê để huấn luyện hàng chục triệu tham số mà không bị quá khớp nghiêm trọng.
    \item \textbf{Năng lực tính toán song song (Massive Parallel Hardware):} Việc ứng dụng GPU (Graphics Processing Units) của NVIDIA kết hợp nền tảng lập trình CUDA đã tăng tốc độ nhân ma trận lên hàng chục lần so với CPU truyền thống, cho phép huấn luyện mạng sâu 8 tầng với 60 triệu tham số trong vòng vài ngày thay vì hàng tháng.
    \item \textbf{Đột phá giải thuật tối ưu hóa và kích hoạt:}
    \begin{itemize}
        \item \textit{Hàm kích hoạt ReLU (Rectified Linear Unit) $f(x) = \max(0, x)$:} Thay thế hàm Sigmoid/Tanh, triệt tiêu hiện tượng bão hòa đạo hàm ở vùng dương, giúp tốc độ huấn luyện hội tụ nhanh hơn gấp 6 lần.
        \item \textit{Kỹ thuật điều chuẩn Dropout (Hinton et al., 2012):} Ngẫu nhiên vô hiệu hóa một tỷ lệ nơ-ron trong quá trình lan truyền tiến, phá vỡ sự phụ thuộc đồng biến phức tạp (co-adaptation) giữa các nơ-ron, ngăn ngừa quá khớp hiệu quả.
    \end{itemize}
\end{enumerate}

\subsection{Sự Tiến Hóa Của Các Kiến Trúc Thị Giác: VGG, ResNet, MobileNet}
Sau AlexNet, cộng đồng nghiên cứu bước vào cuộc chạy đua thiết kế kiến trúc mạng nơ-ron sâu hơn và hiệu quả hơn:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{VGGNet (Simonyan \& Zisserman, 2014):} Chuẩn hóa nguyên lý thiết kế mô-đun hóa: thay vì dùng các bộ lọc lớn ($11 \times 11$ hay $5 \times 5$), VGG xếp chồng liên tiếp các bộ lọc tích chập siêu nhỏ kích thước $3 \times 3$. Hai tầng $3 \times 3$ liên tiếp có cùng vùng cảm nhận hiệu dụng ($5 \times 5$) nhưng giảm được $28\%$ số lượng tham số và tăng tính phi tuyến thông qua hai hàm kích hoạt ReLU.
    \item \textbf{ResNet (He et al., 2015 -- Đạt giải nhất ILSVRC 2015):} Khi chiều sâu của mạng vượt quá 20 tầng, hiện tượng thoái hóa mạng (degradation problem) xuất hiện khiến sai số huấn luyện tăng vọt (không phải do quá khớp). Kaiming He và các cộng sự đã đề xuất khối \textbf{Kết nối phần dư (Residual Block / Skip Connection)}:
    \begin{equation}
    \mathbf{y} = \mathcal{F}(\mathbf{x}, \{W_i\}) + \mathbf{x}
    \end{equation}
    Bằng cách cho phép tín hiệu đầu vào $\mathbf{x}$ cộng trực tiếp vào đầu ra của các tầng biến đổi, gradient trong quá trình lan truyền ngược có thể chảy trực tiếp qua kết nối tắt mà không bị suy hao. Đột phá này cho phép huấn luyện thành công các mạng có độ sâu chưa từng có (lên tới 152 tầng và thậm chí 1,000 tầng), đưa tỷ lệ lỗi phân loại ảnh ImageNet xuống \textbf{3.57\%}, chính thức vượt qua ngưỡng chính xác của mắt người ($5.1\%$).
    \item \textbf{MobileNet (Howard et al., 2017):} Tối ưu hóa tính toán cho các thiết bị nhúng và di động biên (Edge AI) thông qua kỹ thuật \textbf{Tích chập tách biệt chiều sâu (Depthwise Separable Convolution)}, phân rã phép tích chập chuẩn thành hai bước độc lập: Depthwise Conv (lọc không gian) và Pointwise Conv $1 \times 1$ (kết hợp kênh), giúp giảm chi phí tính toán FLOPs từ 8 đến 9 lần mà độ chính xác chỉ suy giảm nhẹ.
\end{itemize}

\subsection{Mô Hình Hóa Chuỗi: Từ RNN, LSTM Đến Cuộc Cách Mạng Transformer}
Song song với thị giác máy tính, việc xử lý dữ liệu chuỗi tuần tự (Sequential Data) như ngôn ngữ tự nhiên và chuỗi thời gian tài chính cũng có những bước chuyển mình căn bản:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{RNN và Rào cản triệt tiêu đạo hàm:} Mạng nơ-ron hồi quy (Simple RNN) sử dụng trạng thái ẩn hồi quy để duy trì bộ nhớ chuỗi. Tuy nhiên, giải thuật lan truyền ngược qua thời gian (BPTT) gặp rào cản toán học nghiêm trọng: tích liên tiếp các ma trận chuyển trạng thái khiến gradient suy giảm theo hàm mũ, dẫn đến hiện tượng triệt tiêu đạo hàm (vanishing gradient), khiến mô hình không thể học được phụ thuộc dài hạn.
    \item \textbf{LSTM và GRU:} Kiến trúc \textbf{LSTM} (Hochreiter \& Schmidhuber, 1997) giải quyết triệt để vấn đề này nhờ cơ chế đường cao tốc ô nhớ trạng thái (Cell State) được điều khiển bởi 3 cổng tuyến tính: Cổng Quên (Forget Gate), Cổng Vào (Input Gate), và Cổng Ra (Output Gate). Biến thể \textbf{GRU} (Cho et al., 2014) tinh gọn kiến trúc xuống còn 2 cổng (Reset và Update), giúp tối ưu hóa tốc độ huấn luyện.
    \item \textbf{Transformer (2017):} Dù LSTM và GRU thống trị suốt hai thập kỷ, bản chất tính toán tuần tự từng bước thời gian của mạng hồi quy ngăn cản việc tính toán song song hóa trên quy mô lớn của GPU. Năm 2017, Vaswani và các cộng sự tại Google công bố bài báo lịch sử mang tựa đề \textbf{\textit{“Attention Is All You Need”}}, giới thiệu kiến trúc \textbf{Transformer}. Bằng cách loại bỏ hoàn toàn các liên kết hồi quy và dựa hoàn toàn vào \textbf{Cơ chế Tự chú ý đa đầu (Multi-Head Self-Attention)}, Transformer cho phép mô hình nắm bắt tương quan giữa mọi vị trí trong chuỗi với độ phức tạp đường dẫn là $O(1)$ và hỗ trợ song song hóa tuyệt đối, mở ra kỷ nguyên của các mô hình ngôn ngữ khổng lồ.
\end{itemize}

\section{Kỷ Nguyên AI Tạo Sinh, Mô Hình Nền Tảng và Xu Hướng Hệ Đa Agent (2020 -- Hiện Nay)}

\subsection{Mô Hình Ngôn Ngữ Lớn (LLMs) và Định Luật Tỷ Lệ (Scaling Laws)}
Từ năm 2020 đến nay, thế giới chứng kiến sự bùng nổ của kỷ nguyên \textbf{AI Tạo sinh (Generative AI)} và các \textbf{Mô hình Nền tảng (Foundation Models)}. Các nghiên cứu của Kaplan et al. (2020) và Chinchilla (Hoffmann et al., 2022) đã xác lập các \textbf{Định luật Tỷ lệ (Scaling Laws)}: hiệu năng của các mô hình ngôn ngữ tuân theo hàm lũy thừa chặt chẽ đối với ba yếu tố: số lượng tham số mô hình, kích thước tập dữ liệu huấn luyện và ngân sách tính toán (FLOPs).

Khi mô hình đạt quy mô hàng trăm tỷ tham số (như GPT-3, GPT-4 của OpenAI; Llama của Meta; Gemini của Google), các \textbf{năng lực nổi trội (Emergent Abilities)} xuất hiện: khả năng học trong ngữ cảnh mà không cần cập nhật trọng số (In-Context Few-Shot Learning), tư duy giải quyết vấn đề từng bước thông qua chuỗi suy luận (Chain-of-Thought Prompting), và năng lực sinh mã nguồn lập trình chuẩn xác.

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth]{images/fig103_ai_ml_dl_taxonomy.png}
    \caption{Cấu trúc phân tầng quan hệ bao hàm giữa AI, Học máy, Học sâu và AI Tạo sinh / Hệ Đa Agent.}
    \label{fig:ai_taxonomy}
\end{figure}

Hình~\ref{fig:ai_taxonomy} minh họa cấu trúc phân tầng phân cấp giữa các thế hệ công nghệ: Trí tuệ Nhân tạo là phạm trù rộng nhất, Học máy là tập con học từ dữ liệu, Học sâu là tập con tự động học biểu diễn đặc trưng phân cấp, và AI Tạo sinh kết hợp Hệ Đa Agent là đỉnh cao ứng dụng hiện đại.

\subsection{Giới Hạn Của Mô Hình Thuần Tham Số và Sự Cần Thiết Của Đồ Thị Tri Thức \& RAG}
Mặc dù có năng lực mạnh mẽ, các mô hình ngôn ngữ lớn dựa trên tham số tĩnh (Parametric Models) bộc lộ ba giới hạn bản chất:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Hiện tượng Ảo giác (Hallucination):} Mô hình sinh ra các câu trả lời nghe rất trôi chảy, thuyết phục nhưng hoàn toàn sai lệch thực tế do bản chất mô hình hóa xác suất từ ngữ tiếp theo thay vì nắm giữ chân lý logic.
    \item \textbf{Dữ liệu tĩnh và Lạc hậu tri thức (Knowledge Cutoff):} Tri thức mô hình bị đóng băng tại thời điểm kết thúc quá trình tiền huấn luyện; chi phí tính toán để huấn luyện lại từ đầu là hàng chục triệu USD, không thể thực hiện thường xuyên.
    \item \textbf{Hộp đen không thể truy vết nguồn gốc (Black-box Unverifiability):} Khó khăn trong việc xác minh trích dẫn nguồn dữ liệu trong các miền đòi hỏi độ tin cậy tuyệt đối như y tế, luật pháp và tài chính.
\end{enumerate}

Để khắc phục các điểm yếu cốt tử này, xu thế phát triển hiện đại đang hội tụ theo hướng tích hợp \textbf{Bộ nhớ phi tham số (Non-parametric Memory)}:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Đồ thị Tri thức (Knowledge Graphs -- KG):} Biểu diễn tri thức thế giới thực dưới dạng các bộ ba thực thể và quan hệ $(h, r, t)$ có cấu trúc đồ thị logic tường minh, cho phép suy diễn chính xác và giải thích được.
    \item \textbf{Mạng Nơ-ron Đồ thị (Graph Neural Networks -- GNN):} Mở rộng phép tích chập và học sâu lên các cấu trúc dữ liệu topo phi Euclid, tổng hợp thông tin thông qua cơ chế truyền tin giữa các nút lân cận (Message Passing).
    \item \textbf{Kiến trúc Tăng cường Truy xuất (Retrieval-Augmented Generation -- RAG):} Kết hợp sức mạnh truy xuất dữ liệu động từ kho tài liệu và đồ thị tri thức để cung cấp ngữ cảnh thời gian thực (grounding context) trước khi mô hình ngôn ngữ sinh câu trả lời, triệt tiêu ảo giác và đảm bảo tính minh bạch học thuật.
\end{itemize}

\subsection{Xu Hướng Tương Lai: Hệ Multi-Agent Tự Trị (Multi-Agent Systems)}
Bước phát triển tiếp theo của AI không chỉ dừng lại ở các mô hình đàm thoại tĩnh (chatbots), mà là sự chuyển dịch sang \textbf{Các Agent Thông minh Tự chủ (Autonomous AI Agents)} và \textbf{Hệ Multi-Agent (Multi-Agent Systems -- MAS)}. 

Một Agent thông minh hiện đại được trang bị chu trình nhận thức hoàn chỉnh: Nhận thức (Perception) $\rightarrow$ Lập kế hoạch suy luận (Planning \& Reasoning) $\rightarrow$ Sử dụng công cụ (Tool Use \& API Execution) $\rightarrow$ Phản tư và hiệu chỉnh (Reflection \& Self-Correction). Khi nhiều Agent chuyên biệt (như Agent Lập kế hoạch, Agent Nghiên cứu, Agent Lập trình, Agent Kiểm thử) phối hợp và phản biện lẫn nhau trong một môi trường cộng tác multi-agent, hệ thống có khả năng giải quyết các bài toán kỹ thuật phức tạp quy mô công nghiệp mà một mô hình đơn lẻ không thể thực hiện được. Đây chính là định hướng phát triển then chốt của các hệ thống thông minh thế hệ mới.

\newpage
"""
