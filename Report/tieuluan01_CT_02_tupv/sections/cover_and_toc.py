# sections/cover_and_toc.py

def get_cover_and_toc():
    return r"""
% -------------------------------------------------------------------------
% TRANG BÌA CHUẨN HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG
% -------------------------------------------------------------------------
\begin{titlepage}
\begin{tikzpicture}[remember picture, overlay]
    \node[anchor=center] at (current page.center) {
        \includegraphics[width=\dimexpr\paperwidth-2.0cm\relax, height=\dimexpr\paperheight-2.0cm\relax]{images/ptit_cover_border.jpeg}
    };
\end{tikzpicture}

\begin{center}
    \vspace*{-0.2cm}
    {\fontsize{14.5pt}{19pt}\selectfont \textbf{HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG}}\\[0.3cm]
    {\fontsize{14.5pt}{19pt}\selectfont \textbf{KHOA CÔNG NGHỆ THÔNG TIN 1}}\\[0.3cm]
    {\fontsize{14.5pt}{19pt}\selectfont \textbf{HỌC PHẦN PHÁT TRIỂN CÁC HỆ THỐNG THÔNG MINH}}\\[1.1cm]
    
    % Logo PTIT chuẩn
    \includegraphics[width=4.5cm]{images/ptit_logo.png}\\[1.3cm]
    
    {\fontsize{18pt}{22pt}\selectfont \textbf{BÁO CÁO TIỂU LUẬN MÔN HỌC}}\\[0.5cm]
    {\fontsize{13pt}{18pt}\selectfont \textbf{ĐỀ TÀI: NGHIÊN CỨU VÀ TRIỂN KHAI CÁC MÔ HÌNH}}\\[0.25cm]
    {\fontsize{13pt}{18pt}\selectfont \textbf{HỌC MÁY CƠ BẢN, MẠNG NƠ-RON TÍCH CHẬP (CNN)}}\\[0.25cm]
    {\fontsize{13pt}{18pt}\selectfont \textbf{VÀ MẠNG NƠ-RON HỒI QUY (RNN) TRONG HỆ THỐNG THÔNG MINH}}\\[1.1cm]
\end{center}

\begin{flushleft}
    \hspace{2.8cm}
    \begin{tabular}{ll}
        \textbf{Lớp:} & D23CTPM01 \\[0.3cm]
        \textbf{Họ và tên:} & Phạm Văn Tư \\[0.3cm]
        \textbf{Mã sinh viên:} & B23DCCN879 \\[0.3cm]
        \textbf{Giảng viên hướng dẫn:} & PGS.TS Trần Đình Quế \\[0.3cm]
        \textbf{Học kỳ:} & Học kỳ 1 năm học 2026 – 2027
    \end{tabular}
\end{flushleft}

\vfill
\begin{center}
    {\fontsize{12pt}{15pt}\selectfont \textbf{Hà Nội, 2026}}\\[0.4cm]
\end{center}
\end{titlepage}

% -------------------------------------------------------------------------
% MỤC LỤC & DANH MỤC HÌNH ẢNH / BẢNG BIỂU / ĐOẠN MÃ
% -------------------------------------------------------------------------
\pagenumbering{roman}
\tableofcontents
\newpage
\listoffigures
\newpage
\listoftables
\newpage
\lstlistoflistings
\newpage

% -------------------------------------------------------------------------
% PHẦN MỞ ĐẦU (3 - 4 TRANG)
% -------------------------------------------------------------------------
\pagenumbering{arabic}
\chapter*{Phần Mở Đầu}
\addcontentsline{toc}{chapter}{Phần Mở Đầu}

\section*{1. Bối Cảnh Khoa Học và Tính Cấp Thiết Của Đề Tài}

Trong làn sóng của cuộc Cách mạng Công nghiệp lần thứ tư, Trí tuệ Nhân tạo (Artificial Intelligence - AI) và Học máy (Machine Learning - ML) đã chuyển mình mạnh mẽ từ các lý thuyết hàn lâm trong phòng thí nghiệm trở thành động lực cốt lõi định hình lại toàn bộ nền kinh tế số và xã hội hiện đại. Trọng tâm của sự phát triển này là quá trình chuyển dịch mô hình tính toán: từ các hệ thống chuyên gia cổ điển hoạt động dựa trên các tập luật tường minh (rule-based expert systems) do con người xây dựng thủ công sang các hệ thống thông minh học hỏi từ dữ liệu (data-driven intelligent systems).

Sự bùng nổ của dữ liệu lớn (Big Data) cùng sự phát triển vượt bậc của năng lực phần cứng tính toán song song (đặc biệt là GPU và TPU) đã thúc đẩy Học sâu (Deep Learning - DL) tạo ra những bước nhảy vọt mang tính lịch sử. Tuy nhiên, trong môi trường ứng dụng công nghiệp thực tế, các hệ thống thông minh không bao giờ đối mặt với một dạng dữ liệu đơn lẻ, mà luôn phải xử lý ba hình thái thông tin cơ bản:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Dữ liệu Bảng (Tabular Data):} Là dạng dữ liệu phổ biến nhất trong các hệ thống nghiệp vụ (y tế, tài chính, bất động sản, chuỗi cung ứng), đòi hỏi các thuật toán học máy thống kê cổ điển (như Hồi quy tuyến tính, Logistic Regression, Cây quyết định, Rừng ngẫu nhiên, SVM) và Mạng nơ-ron đa tầng (MLP) để nắm bắt các mối quan hệ phi tuyến tính phức tạp giữa các đặc trưng có cấu trúc.
    \item \textbf{Dữ liệu Không gian Thị giác (Spatial Visual Data):} Bao gồm hình ảnh và thị giác máy tính, nơi các điểm ảnh (pixels) có mối tương quan không gian chặt chẽ và tính bất biến tịnh tiến (translation invariance). Mạng nơ-ron Tích chập (Convolutional Neural Networks - CNN) với các cơ chế chia sẻ trọng số (weight sharing), vùng cảm nhận (receptive field) và kết nối phần dư (residual connections) đã trở thành chuẩn mực không thể thay thế.
    \item \textbf{Dữ liệu Chuỗi Thời gian và Hành vi (Temporal \& Sequential Data):} Bao gồm dữ liệu tài chính, nhật ký tương tác người dùng, tín hiệu cảm biến IoT và chuỗi văn bản. Đặc tính cốt lõi của dạng dữ liệu này là mối quan hệ nhân quả theo thời gian (temporal causality) và tính phụ thuộc ngữ cảnh dài hạn, đòi hỏi Mạng nơ-ron Hồi quy (Recurrent Neural Networks - RNN) cùng các biến thể cổng tiên tiến như LSTM (Long Short-Term Memory) và GRU (Gated Recurrent Unit).
\end{itemize}

Việc làm chủ toàn diện cơ sở toán học, quy trình tiền xử lý chống rò rỉ dữ liệu, năng lực hiện thực hóa giải thuật trên các nền tảng lập trình khác nhau (từ mức tính toán nguyên thủy Scratch đến các khung làm việc hiện đại PyTorch và Keras), cũng như đánh giá đối chuẩn khoa học và triển khai thực tế là yêu cầu sống còn đối với một kỹ sư phát triển hệ thống thông minh. Xuất phát từ yêu cầu thực tiễn đó, đề tài tiểu luận: \textbf{\textit{“Nghiên cứu và Triển khai các Mô hình Học máy Cơ bản, Mạng Nơ-ron Tích chập (CNN) và Mạng Nơ-ron Hồi quy (RNN) trong Hệ thống Thông minh”}} được xây dựng nhằm cung cấp một bức tranh toàn cảnh, sâu sắc và có tính hệ thống cao từ lý thuyết đến thực nghiệm ứng dụng.

\section*{2. Mục Tiêu và Nhiệm Vụ Nghiên Cứu}

Mục tiêu tổng quát của tiểu luận môn học là xây dựng một nền tảng tri thức học thuật vững chắc kết hợp năng lực thực hành chuyên sâu, bao quát toàn bộ tiến trình từ các kỹ thuật học máy cổ điển đến các kiến trúc học sâu hiện đại xử lý không gian và thời gian. Cụ thể, các nhiệm vụ trọng tâm được xác định như sau:
\begin{enumerate}[leftmargin=1.2cm, label={\textbf{Nhiệm vụ \arabic*:}}]
    \item \textbf{Khảo cứu Lịch sử Phát triển của AI:} Khảo sát các mốc phát triển lịch sử từ 1950 đến nay, phân tích nguyên nhân của hai thời kỳ “Mùa đông AI” (AI Winters), sự chuyển dịch sang học máy thống kê và cuộc cách mạng học sâu, cùng các xu hướng hiện đại (Foundation Models, Graph AI, Multi-Agent Systems).
    \item \textbf{Nghiên cứu Cơ sở Lý thuyết và Thuật toán:} Trình bày rõ nguyên lý hoạt động, hàm mất mát và thuật toán tối ưu của từng mô hình: giải thuật lan truyền ngược (Backpropagation) trong mạng nơ-ron, phép toán tích chập trong CNN, và cơ chế xử lý dữ liệu chuỗi thời gian trong RNN.
    \item \textbf{Khảo sát Thực nghiệm trên các Bộ Dữ liệu Thực tế:} Khám phá (EDA), trực quan hóa phân bố và tiền xử lý dữ liệu trên 7 bộ dữ liệu đa dạng: Y tế (Tiểu đường), Tài chính (Chứng khoán Việt Nam VN30), Bất động sản, Thương mại điện tử (Đánh giá NLP và Hành vi khách hàng), Thị giác máy tính (SVHN) và Ảnh vệ tinh (EuroSAT).
    \item \textbf{Hiện thực hóa Đa Nền tảng (Tri-Framework Implementation):} Xây dựng độc lập mã nguồn giải thuật trên cả 3 môi trường:
    \begin{itemize}
        \item \textit{Scratch (NumPy thuần):} Tự viết các lớp, phép tính lan truyền tiến/lùi và cập nhật trọng số từ các phép toán cơ bản nhằm hiểu rõ bản chất giải thuật.
        \item \textit{Keras / TensorFlow:} Xây dựng mô hình với API cấp cao, thuận tiện cho việc thử nghiệm nhanh.
        \item \textit{PyTorch:} Xây dựng mô hình dạng module (\texttt{torch.nn.Module}), tối ưu hóa vòng lặp huấn luyện và kiểm soát gradient chặt chẽ.
    \end{itemize}
    \item \textbf{Đánh giá và Đối chuẩn Thực nghiệm:} So sánh khách quan các mô hình trên từng tập dữ liệu theo các tiêu chí thực tế: Độ chính xác (Accuracy, F1, RMSE, MAE, $R^2$), Số lượng tham số, Dung lượng tệp trọng số và Tốc độ suy luận (thời gian dự báo).
    \item \textbf{Đóng Gói và Triển Khai Thực Tế (Deployment):} Xây dựng giao diện ứng dụng web tương tác (Web Applications) cho phép người dùng nhập liệu trực quan và nhận kết quả dự báo thời gian thực.
\end{enumerate}

\section*{3. Đối Tượng và Phương Pháp Nghiên Cứu}

\subsection*{3.1. Đối Tượng Nghiên Cứu}
Đối tượng nghiên cứu của tiểu luận bao gồm các cấu trúc dữ liệu đa miền và các lớp giải thuật học máy, học sâu tiêu biểu:
\begin{itemize}[leftmargin=1.2cm]
    \item \textit{Các mô hình học máy cơ bản:} Linear Regression, Logistic Regression, Decision Tree, Random Forest, Support Vector Machine (SVM), và Multilayer Perceptron (MLP).
    \item \textit{Các kiến trúc mạng tích chập:} Custom 2D CNN, VGGNet, ResNet (Residual Learning với ResNet-18), MobileNet (Depthwise Separable Convolution) và 1D CNN cho chuỗi.
    \item \textit{Các kiến trúc mạng hồi quy:} Simple RNN, Long Short-Term Memory (LSTM), Gated Recurrent Unit (GRU), và Bidirectional LSTM (BiLSTM).
    \item \textit{Các bộ dữ liệu đối chuẩn thực tế:} Pima/CDC Diabetes (100,000 bản ghi), Vietnam Real Estate (150,000 bản ghi), Shopee/Tiki Reviews (22,641 bản ghi), SVHN (99,289 ảnh), EuroSAT (27,000 ảnh), Chứng khoán Việt Nam VN30 (15,225 phiên) và Customer Sequential Behavior (60,000 bản ghi chuỗi).
\end{itemize}

\subsection*{3.2. Phương Pháp Nghiên Cứu}
Báo cáo áp dụng kết hợp giữa nghiên cứu lý thuyết và kiểm chứng thực nghiệm:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Phương pháp Nghiên cứu Lý thuyết:} Hệ thống hóa cơ sở toán học, giải thuật tối ưu hóa và nguyên lý hoạt động của từng mô hình học máy và học sâu.
    \item \textbf{Phương pháp Thực nghiệm Thực tế:} Xây dựng quy trình xử lý dữ liệu chuẩn hóa, phân chia tập dữ liệu huấn luyện và kiểm thử chặt chẽ (Chronological Split cho chuỗi thời gian, phân tầng cho phân loại mất cân bằng); đo đạc thời gian chạy và dung lượng mô hình trên cùng cấu hình phần cứng để đảm bảo tính khách quan.
\end{itemize}

\section*{4. Bố Cục Báo Cáo Tiểu Luận}

Báo cáo tiểu luận trong giai đoạn này tập trung hoàn thiện trọn vẹn từ Phần Mở đầu đến hết Chương 4:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Chương 1: Lịch sử Phát triển Trí tuệ Nhân tạo:} Khảo cứu bức tranh lịch sử 75 năm của AI từ năm 1950 đến 2026, phân tích nguyên nhân hai Mùa đông AI, sự trỗi dậy của học máy thống kê, cuộc cách mạng Deep Learning và xu thế phát triển tương lai.
    \item \textbf{Chương 2: Các Kỹ thuật Học máy Cơ bản:} Trình bày cơ sở lý thuyết của các thuật toán ML cốt lõi; phân tích khám phá dữ liệu (EDA) trên 3 tập dữ liệu lớn; hiện thực hóa mã nguồn Scikit-Learn và bộ ba Scratch, Keras, PyTorch cho MLP; đối chuẩn hiệu năng các mô hình và triển khai Web App.
    \item \textbf{Chương 3: Mạng Nơ-ron Tích chập (CNN):} Trình bày nguyên lý phép toán tích chập, pooling, vùng cảm nhận (receptive field); khảo sát các kiến trúc VGG, ResNet, MobileNet; phân tích 3 bộ dữ liệu ảnh (SVHN, EuroSAT, 1D CNN); hiện thực hóa trên Scratch, Keras, PyTorch; đối chuẩn hiệu năng và minh họa ứng dụng.
    \item \textbf{Chương 4: Mạng Nơ-ron Hồi quy (RNN):} Trình bày nguyên lý xử lý chuỗi thời gian, cơ chế hoạt động của LSTM, GRU, BiLSTM; phân tích EDA 2 tập dữ liệu chuỗi lớn (Chứng khoán Việt Nam VN30 và Churn Khách hàng); hiện thực hóa trên Scratch, Keras, PyTorch; đánh giá đối chuẩn và triển khai Web App dự báo thời gian thực.
\end{itemize}

\noindent Các chương tiếp theo trong lộ trình học phần (Chương 5: Knowledge Graph và RAG; Chương 6: Deep Graph Neural Networks; Chương 7: Hệ đa Agent thông minh) sẽ tiếp tục kế thừa trực tiếp các thành quả mô hình hóa nền tảng đã đạt được trong báo cáo này.

\newpage
"""
