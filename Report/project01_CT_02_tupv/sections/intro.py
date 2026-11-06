# -*- coding: utf-8 -*-
"""
sections/intro.py
Lời mở đầu và Giới thiệu Tổng quan Dự án Project 01
"""

def get_intro():
    return r"""
% =========================================================================
% LỜI MỞ ĐẦU
% =========================================================================
\section*{LỜI MỞ ĐẦU}
\addcontentsline{toc}{section}{LỜI MỞ ĐẦU}

\subsection*{1. Bối cảnh thực tiễn và tính cấp thiết của đề tài}
Bệnh đái tháo đường (Diabetes Mellitus) hiện đang là một trong những đại dịch bệnh lý không lây nhiễm đe dọa nghiêm trọng đến sức khỏe cộng đồng toàn cầu nói chung và Việt Nam nói riêng. Theo số liệu thống kê công bố từ Liên đoàn Đái tháo đường Thế giới (IDF Diabetes Atlas 2023) và Bộ Y Tế Việt Nam, hiện có hơn 5,3 triệu người trưởng thành tại Việt Nam đang sống chung với bệnh đái tháo đường, chiếm khoảng 7,1\% dân số. Đáng báo động hơn, có tới hơn \textbf{65\% số người mắc bệnh trong cộng đồng chưa được chẩn đoán xác định}, và trên \textbf{50\% bệnh nhân đã phát hiện có biến chứng tim mạch, suy giảm chức năng thận hoặc tổn thương thần kinh đáy mắt} ngay tại thời điểm được phát hiện lần đầu. Chi phí điều trị biến chứng đái tháo đường chiếm đến 70\% tổng ngân sách y tế dành cho căn bệnh này, tạo gánh nặng kinh tế - xã hội khổng lồ cho gia đình và hệ thống an sinh quốc gia.

Để kiểm soát hiệu quả bệnh đái tháo đường, hai rào cản cốt tử cần được giải quyết:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Phát hiện sớm và phân tầng nguy cơ kịp thời:} Phần lớn bệnh nhân ở giai đoạn tiền đái tháo đường (Pre-diabetes) hoặc đái tháo đường giai đoạn đầu hầu như không có triệu chứng rầm rộ hoặc chỉ xuất hiện các biểu hiện mơ hồ (mệt mỏi, sụt cân nhẹ, khát nước, tiểu đêm). Việc thiếu các công cụ sàng lọc không xâm lấn dễ tiếp cận khiến người dân bỏ lỡ "giai đoạn vàng" để can thiệp đảo ngược bệnh lý.
    \item \textbf{Quản lý lâm sàng toàn diện và liên tục:} Đái tháo đường là bệnh mạn tính đòi hỏi sự phối hợp đa chuyên khoa: từ chỉ định phác đồ thuốc hạ đường huyết chuẩn mực theo phác đồ Bộ Y Tế, giám sát chức năng lọc cầu thận (eGFR), kiểm soát tương tác thuốc nguy hiểm, đến thiết lập chế độ dinh dưỡng cá nhân hóa theo thói quen ẩm thực Việt và duy trì lối sống vận động an toàn.
\end{enumerate}

\subsection*{2. Giới hạn mang tính cấu trúc của các hệ thống AI đơn lẻ (Single-Agent)}
Sự trỗi dậy của các Mô hình Ngôn ngữ Lớn (LLMs) trong thời gian gần đây đã mở ra tiềm năng ứng dụng Trí tuệ Nhân tạo (AI) trong y tế. Tuy nhiên, việc ứng dụng các mô hình Chatbot đàm thoại đơn lẻ (\textit{Single-Agent LLM}) hoặc hệ thống RAG sơ khai vào thực hành lâm sàng đối mặt với những nguy cơ nghiêm trọng:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Hiện tượng ảo giác y khoa (Medical Hallucination):} Mô hình có xu hướng tự sinh thông tin thuốc hoặc chỉ định liều lượng không có căn cứ khi bị quá tải cửa sổ ngữ cảnh, có thể gây hạ đường huyết đột ngột dẫn đến hôn mê tử vong.
    \item \textbf{Xóa nhòa ranh giới giữa Sàng lọc và Khẳng định chẩn đoán:} Các Chatbot thông thường thường kết luận bệnh nhân "đã bị đái tháo đường" chỉ dựa vào vài triệu chứng mơ hồ như sụt cân hay khát nước, hoặc nguy hiểm hơn là tự ý kê đơn thuốc đặc trị (như Metformin, Sulfonylurea) cho người bệnh khi chưa hề có kết quả xét nghiệm sinh hóa máu định lượng. Điều này vi phạm nghiêm trọng Quyết định số 5481/QĐ-BYT của Bộ Y Tế.
    \item \textbf{Bỏ sót tương tác thuốc và chống chỉ định suy thận:} Khi một mô hình đơn lẻ phải giải quyết cùng lúc câu hỏi về chế độ ăn uống, lối sống và bệnh nền, nó thường bỏ qua các dữ kiện quan trọng như chỉ số lọc cầu thận $\text{eGFR} < 30\text{ mL/phút/1.73m}^2$ (chống chỉ định tuyệt đối của Metformin) hay nguy cơ nhiễm toan acid lactic tử vong khi dùng chung Metformin với cồn.
    \item \textbf{Hộp đen thiếu giải thích (Black-box nature):} Các mô hình học máy phân loại nguy cơ truyền thống chỉ trả về một con số xác suất vô hồn mà không giải thích được vì sao chỉ số HbA1c hay Glucose lại đóng vai trò quyết định, khiến người dùng và bác sĩ không thể tin cậy.
\end{itemize}

\subsection*{3. Mục tiêu và Giải pháp của Đề tài: Hệ Multi-Agent DiaAgent-MAS}
Xuất phát từ các yêu cầu cấp thiết trên, dự án này tập trung nghiên cứu, thiết kế và phát triển \textbf{DiaAgent-MAS} -- Hệ thống Multi-Agent thông minh chuyên sâu hỗ trợ sàng lọc, chẩn đoán và quản trị bệnh đái tháo đường tại Việt Nam. Hệ thống tích hợp hài hòa các công nghệ tiên tiến nhất của AI hiện đại:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Kiến trúc Multi-Agent phối hợp nhịp nhàng (Collaborative Multi-Agent Systems):} Phân rã bài toán y tế phức tạp thành 7 Agent chuyên trách: Agent Tiếp đón phân loại (Triage), Agent Dự báo học máy (Risk Prediction), Bác sĩ Nội tiết (Endocrinologist), Chuyên gia Dinh dưỡng (Nutritionist), Huấn luyện viên Lối sống (Lifestyle Coach), Định vị Dược phẩm Long Châu (Pharmacy Locator), và Hộ vệ An toàn Y tế (Safety Guardian).
    \item \textbf{Cơ chế Phân luồng Lâm sàng Kép (Dual-mode Clinical Routing):} Tách biệt tuyệt đối hai chế độ: Chế độ Sàng lọc nguy cơ (dành cho người dùng chưa có xét nghiệm máu, khóa mô hình ML để tránh giả định sai) và Chế độ Khẳng định chẩn đoán (kích hoạt đầy đủ mô hình học máy và phác đồ thuốc Bộ Y Tế).
    \item \textbf{Học máy có khả năng giải thích (Explainable AI - XAI):} Sử dụng mô hình Gradient Boosting (LightGBM) được huấn luyện trên 100,000 hồ sơ bệnh án, kết hợp giá trị Shapley (SHAP) để minh bạch hóa mức độ đóng góp của từng đặc trưng can thiệp.
    \item \textbf{Đồ thị Tri thức Y tế \& RAG Chuẩn hóa:} Hệ thống hóa toàn bộ hướng dẫn chẩn đoán của Bộ Y Tế (Quyết định số 5481/QĐ-BYT), bảng thành phần dinh dưỡng thực phẩm Việt Nam của Viện Dinh Dưỡng Quốc Gia (NIN), và dữ liệu dược phẩm, thiết bị y tế cá nhân thu thập từ Hệ thống Nhà thuốc FPT Long Châu.
    \item \textbf{Vòng lặp Phản biện và Tự hiệu chỉnh (Reflection \& Safety Guardian Loop):} Đảm bảo 100\% khuyến nghị y tế đều trải qua kiểm chứng chéo độc lập, chặn đứng hoàn toàn ảo giác y khoa trước khi phản hồi người dùng.
\end{enumerate}

\subsection*{4. Bố cục của Báo cáo}
Báo cáo dự án được cấu trúc thành các chương chính như sau:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Chương 1: Cơ sở Lý thuyết và Nền tảng Công nghệ:} Trình bày cơ sở toán học của Hệ Multi-Agent (Dec-POMDP, BDI), mô hình học máy LightGBM và lý thuyết giải thích SHAP, cùng cơ chế Đồ thị Tri thức Y tế và hướng dẫn lâm sàng Quyết định 5481/QĐ-BYT.
    \item \textbf{Chương 2: Thiết kế Kiến trúc Hệ thống DiaAgent-MAS:} Mô tả chi tiết sơ đồ luồng dữ liệu, cấu trúc trạng thái dùng chung (Global State Schema), cơ chế phân luồng lâm sàng kép và nguyên lý hoạt động của 7 Agent chuyên trách.
    \item \textbf{Chương 3: Triển khai Thực nghiệm và Đánh giá Kết quả:} Đánh giá thực nghiệm mô hình học máy LightGBM, dữ liệu dược phẩm FPT Long Châu, thực nghiệm toàn diện trên 2 ca lâm sàng thực tế, và triển khai ứng dụng Web tương tác Streamlit Chatbot-First.
    \item \textbf{Kết luận và Định hướng Phát triển:} Tổng kết các đóng góp nổi bật và thảo luận các hướng mở rộng trong tương lai.
\end{itemize}
"""
