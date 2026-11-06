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
    {\fontsize{14.5pt}{19pt}\selectfont \textbf{HỌC PHẦN PHÁT TRIỂN CÁC HỆ THỐNG THÔNG MINH}}\\[1.0cm]
    
    % Logo PTIT chuẩn
    \includegraphics[width=4.3cm]{images/ptit_logo.png}\\[1.1cm]
    
    {\fontsize{22pt}{28pt}\selectfont \textbf{BÁO CÁO TIỂU LUẬN}}\\[2.2cm]
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
% MỤC LỤC \& DANH MỤC HÌNH ẢNH / BẢNG BIỂU / ĐOẠN MÃ
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
% PHẦN MỞ ĐẦU
% -------------------------------------------------------------------------
\pagenumbering{arabic}
\chapter*{Phần Mở Đầu}
\addcontentsline{toc}{chapter}{Phần Mở Đầu}

\section*{1. Bối Cảnh Khoa Học và Tính Cấp Thiết Của Đề Tài}

Trong làn sóng của cuộc Cách mạng Công nghiệp lần thứ tư, Trí tuệ Nhân tạo (Artificial Intelligence - AI) và Học máy (Machine Learning - ML) đã chuyển mình mạnh mẽ từ các lý thuyết hàn lâm trong phòng thí nghiệm trở thành động lực cốt lõi định hình lại toàn bộ nền kinh tế số và xã hội hiện đại. Trọng tâm của sự phát triển này là quá trình chuyển dịch mô hình tính toán: từ các hệ thống chuyên gia cổ điển hoạt động dựa trên các tập luật tường minh (rule-based expert systems) sang các hệ thống thông minh học hỏi từ dữ liệu (data-driven intelligent systems) và hệ thống lai kết hợp biểu tượng (Neuro-Symbolic Multi-Agent Systems).

Sự bùng nổ của dữ liệu lớn (Big Data) cùng sự phát triển vượt bậc của năng lực phần cứng tính toán song song (đặc biệt là GPU và TPU) đã thúc đẩy Học sâu (Deep Learning - DL) tạo ra những bước nhảy vọt mang tính lịch sử. Tuy nhiên, trong môi trường ứng dụng công nghiệp thực tế, các hệ thống thông minh không bao giờ đối mặt với một dạng dữ liệu đơn lẻ, mà luôn phải xử lý bốn hình thái thông tin cơ bản:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Dữ liệu Bảng (Tabular Data):} Đòi hỏi các thuật toán học máy thống kê cổ điển (Hồi quy tuyến tính, Logistic Regression, Cây quyết định, Random Forest, SVM) và Mạng nơ-ron đa tầng (MLP) để nắm bắt các mối quan hệ phi tuyến tính phức tạp giữa các đặc trưng có cấu trúc.
    \item \textbf{Dữ liệu Không gian Thị giác (Spatial Visual Data):} Mạng nơ-ron Tích chập (Convolutional Neural Networks - CNN) với các cơ chế chia sẻ trọng số, vùng cảm nhận (receptive field) và kết nối phần dư (Residual connections) là chuẩn mực không thể thay thế cho dữ liệu ảnh và thị giác máy tính.
    \item \textbf{Dữ liệu Chuỗi Thời gian (Temporal \& Sequential Data):} Đòi hỏi Mạng nơ-ron Hồi quy (Recurrent Neural Networks - RNN) cùng các biến thể cổng tiên tiến như LSTM và BiLSTM để nắm bắt mối quan hệ nhân quả và phụ thuộc dài hạn.
    \item \textbf{Tri thức Có Cấu trúc \& Tác tử Xã hội (Knowledge Graphs \& Multi-Agent Systems):} Khắc phục triệt để hiện tượng ảo giác (hallucination) và thiếu logic suy luận đa bước của LLM thông qua Đồ thị Tri thức (KG), công nghệ RAG nâng cao và sự phối hợp phản biện giữa nhiều tác tử tự chủ chuyên biệt hóa (Multi-Agent Systems - MAS).
\end{itemize}

Xuất phát từ yêu cầu thực tiễn đó, đề tài tiểu luận: \textbf{\textit{“Nghiên cứu và Triển khai Toàn diện các Hệ thống Thông minh: Từ Học máy Cơ bản, CNN, RNN đến Đồ thị Tri thức (KG), RAG và Hệ Đa Tác tử (Multi-Agent Systems)”}} được xây dựng nhằm cung cấp một bức tranh toàn cảnh, sâu sắc và có tính hệ thống cao từ lý thuyết toán học đến thực nghiệm ứng dụng trên dữ liệu Việt Nam.

\section*{2. Mục Tiêu và Nhiệm Vụ Nghiên Cứu}

Mục tiêu tổng quát của tiểu luận môn học là xây dựng một nền tảng tri thức học thuật vững chắc kết hợp năng lực thực hành chuyên sâu, bao quát toàn bộ tiến trình tiến hóa của các hệ thống thông minh. Cụ thể, các nhiệm vụ trọng tâm gồm:
\begin{enumerate}[leftmargin=1.2cm, label={\textbf{Nhiệm vụ \arabic*:}}]
    \item \textbf{Khảo cứu Lịch sử Phát triển của AI:} Khảo sát bức tranh 75 năm phát triển của AI (1950--2026), phân tích hai mùa đông AI, sự trỗi dậy của học máy thống kê, cuộc cách mạng Deep Learning và kỷ nguyên tác tử tự chủ (Agentic AI).
    \item \textbf{Nghiên cứu Cơ sở Lý thuyết \& Thuật toán:} Trình bày tường minh nguyên lý toán học, hàm mất mát và tối ưu hóa: Lan truyền ngược (Backpropagation), phép toán tích chập trong CNN, cơ chế cổng trong LSTM/BiLSTM, bộ ba RDF trong Knowledge Graph, và phương trình Dec-POMDP trong Hệ Đa Tác Tử.
    \item \textbf{Khảo sát Thực nghiệm trên Dữ liệu Đa Miền Việt Nam:} Thực nghiệm trên 9 bộ dữ liệu đa dạng: Y tế đái tháo đường (CDC \& Bệnh viện Việt Nam), Bất động sản, Đánh giá thương mại điện tử, Ảnh vệ tinh EuroSAT, Biến động cổ phiếu VN30 (FPT, VCB, HPG, VIC) và Giá vàng miếng SJC.
    \item \textbf{Hiện thực hóa Đa Nền tảng \& Hệ Tác tử:} Xây dựng mã nguồn giải thuật trên Scratch (NumPy thuần), PyTorch, NetworkX, cùng kiến trúc Hệ Đa Tác Tử hướng đối tượng tích hợp các công cụ chuyên biệt.
    \item \textbf{Đánh giá \& Đối chuẩn Thực nghiệm:} Đối sánh khoa học giữa các mô hình học máy, các biến thể CNN/RNN, và so sánh định lượng giữa Tác tử đơn lẻ (Single-Agent) với Hệ Đa Tác Tử (Multi-Agent Systems).
    \item \textbf{Triển Khai Bảng Điều Khiển Tương Tác (Deployment):} Xây dựng giao diện ứng dụng web Dashboard Streamlit trực quan hóa thời gian thực các mô hình chẩn đoán y tế, dự báo tài chính và mạng lưới trao đổi thông điệp đa tác tử.
\end{enumerate}

\section*{3. Bố Cục Báo Cáo Tiểu Luận 03}

Nội dung báo cáo Tiểu luận 03 được cấu trúc chặt chẽ thành 6 chương chuyên môn:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Chương 1: Lịch sử Phát triển Trí tuệ Nhân tạo:} Toàn cảnh lịch sử 75 năm của AI từ 1950 đến 2026, các thời kỳ Mùa đông AI, sự chuyển dịch mô hình tính toán và xu thế Agentic AI hiện đại.
    \item \textbf{Chương 2: Các Kỹ thuật Học máy Cơ bản \& Mạng Nơ-ron Đa tầng (MLP):} Cơ sở lý thuyết của các thuật toán ML cốt lõi (Linear, Logistic, Decision Tree, Random Forest, SVM); phân tích EDA trên 3 tập dữ liệu lớn; hiện thực hóa đa nền tảng và đối chuẩn mô hình.
    \item \textbf{Chương 3: Mạng Nơ-ron Tích chập (CNN) \& Thị giác Máy tính:} Nguyên lý phép toán tích chập, pooling, receptive field; khảo sát kiến trúc VGG, ResNet, MobileNet; thực nghiệm trên tập ảnh SVHN, EuroSAT và đối chuẩn hiệu năng.
    \item \textbf{Chương 4: Mạng Nơ-ron Hồi quy (RNN) \& Dự báo Chuỗi Thời gian:} Nguyên lý xử lý tuần tự, cơ chế cổng LSTM, GRU, BiLSTM; thực nghiệm dự báo chuỗi thời gian cổ phiếu VN30 và hành vi khách hàng; triển khai Web App dự báo thời gian thực.
    \item \textbf{Chương 5: Đồ thị Tri thức (Knowledge Graph), RAG \& Tác tử Thông minh (AI Agent):} Cơ sở lý thuyết RDF Triples, Ontology, Graph DB vs Vector DB; 5 chiến lược phân mảnh (Chunking) và GraphRAG; mô hình hóa dữ liệu Y tế Đái tháo đường (Bộ Y Tế) và Tài chính (VN30 \& Vàng SJC); hiện thực tác tử tự chủ ReAct đơn lẻ và phân tích các điểm nghẽn kiến trúc.
    \item \textbf{Chương 6: Hệ Đa Tác Tử (Multi-Agent Systems - MAS) Trong Hệ Thống Thông Minh:} Cơ sở toán học Dec-POMDP, Markov Games, BDI; các cấu trúc phối hợp (Supervisor, Hierarchical, Debate); đối chuẩn framework (LangGraph, AutoGen, CrewAI); hiện thực hóa hệ đa tác tử hội chẩn y tế đa chuyên khoa và bàn phân tích tài chính; kiểm chứng thực nghiệm đối sánh định lượng vượt trội so với tác tử đơn lẻ.
\end{itemize}

\newpage
"""
