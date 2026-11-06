# -*- coding: utf-8 -*-
"""
sections/conclusion.py
Kết luận và Định hướng Phát triển
"""

def get_conclusion():
    return r"""
% =========================================================================
% KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
% =========================================================================
\section*{KẾT LUẬN VÀ ĐỊNH HƯỚNG PHÁT TRIỂN}
\addcontentsline{toc}{section}{KẾT LUẬN VÀ ĐỊNH HƯỚNG PHÁT TRIỂN}

\subsection*{1. Tổng kết Các Đóng Góp Chính Của Dự Án}
Dự án nghiên cứu và triển khai \textbf{DiaAgent-MAS} đã giải quyết thành công bài toán xây dựng một hệ thống Trí tuệ Nhân tạo hỗ trợ y tế đái tháo đường toàn diện, an toàn và có khả năng ứng dụng thực tiễn cao tại Việt Nam. Những đóng góp học thuật và kỹ nghệ nổi bật của dự án bao gồm:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Hiện thực hóa Kiến trúc Multi-Agent Hợp tác \& Phản biện An toàn:} Khắc phục triệt để các nhược điểm cố hữu của mô hình Single-Agent (quá tải ngữ cảnh, ảo giác y khoa, tích lũy sai số chuỗi suy luận). Hệ thống phân rã bài toán thành 7 Agent chuyên trách: Tiếp đón phân loại, Dự báo học máy, Bác sĩ Nội tiết, Chuyên gia Dinh dưỡng, Huấn luyện viên Lối sống, Định vị Dược phẩm, và Hộ vệ An toàn.
    \item \textbf{Cơ chế Phân luồng Lâm sàng Kép (Dual-Mode Clinical Routing):} Thiết lập ranh giới pháp lý và y khoa rõ ràng giữa giai đoạn "Sàng lọc nguy cơ" (khi chưa có xét nghiệm máu) và "Khẳng định chẩn đoán" (khi đã có xét nghiệm định lượng). Hệ thống kiên quyết khóa mô hình ML dự báo và từ chối kê đơn bừa bãi khi thiếu dữ liệu máu, bảo đảm tuân thủ nghiêm ngặt theo \textbf{Quyết định số 5481/QĐ-BYT của Bộ Y Tế}.
    \item \textbf{Mô hình Học máy Độ nhạy Cao \& Giải thích Minh bạch (XAI):} Mô hình LightGBM được huấn luyện trên 100,000 bản ghi bệnh nhân đạt chỉ số \textbf{Recall vượt trội lên tới 92.53\% và ROC-AUC 0.9797}, giảm thiểu tối đa nguy cơ bỏ sót ca bệnh trong cộng đồng. Việc tích hợp giá trị Shapley (SHAP) giúp người bệnh và nhân viên y tế thấu hiểu cặn kẽ các yếu tố nguy cơ thúc đẩy bệnh lý.
    \item \textbf{Cầu nối Tri thức Lâm sàng \& Thị trường Dược phẩm Thực tế:} Số hóa thành công quy tắc dinh dưỡng cho người Việt Nam của Viện Dinh Dưỡng Quốc Gia (NIN), đồng thời liên kết trực tiếp với dữ liệu 50+ sản phẩm, giá bán và tình trạng kê đơn từ Hệ thống Nhà thuốc FPT Long Châu, giúp người bệnh tiếp cận giải pháp y tế khả thi.
    \item \textbf{Ứng dụng Web Chatbot-First Mượt mà và Hiệu năng Cao:} Xây dựng giao diện Web đồng bộ song song giữa hội thoại thông minh và bảng điều khiển lâm sàng thời gian thực, loại bỏ hoàn toàn lỗi kích hoạt lặp và tối ưu hóa thời gian phản hồi từ 16.5 giây xuống chỉ còn 5 -- 7 giây.
\end{enumerate}

\subsection*{2. Thách Thức và Hạn Chế Hiện Tại}
Mặc dù đạt được những kết quả thực nghiệm rất khả quan, hệ thống vẫn tồn tại một số hạn chế cần tiếp tục hoàn thiện:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Sự phụ thuộc vào Hạ tầng API Đám mây:} Agent Tiếp đón và Hộ vệ An toàn hiện đang sử dụng mô hình nền tảng đám mây (Gemini API), đòi hỏi đường truyền Internet liên tục và có thể đối mặt với nguy cơ gián đoạn dịch vụ khi mạng gặp sự cố.
    \item \textbf{Quy mô Đồ thị Tri thức:} Đồ thị tri thức y tế hiện tại được lưu trữ trong bộ nhớ cấu trúc Python nội bộ. Khi mở rộng sang hàng chục nghìn thực thể dược chất và bệnh lý đa cơ quan, hệ thống cần một giải pháp lưu trữ đồ thị chuyên dụng.
\end{itemize}

\subsection*{3. Định Hướng Phát Triển Tương Lai}
Trong giai đoạn tiếp theo, dự án định hướng mở rộng theo các trọng tâm kỹ thuật sau:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Nâng cấp Đồ thị Tri thức Phân tán Neo4j \& Mạng Nơ-ron Đồ thị (GNN):} Chuyển đổi toàn bộ cơ sở tri thức y tế sang cơ sở dữ liệu đồ thị phân tán Neo4j. Ứng dụng Mạng Tích chập Đồ thị (GCN) để dự đoán tương tác thuốc -- thuốc (Drug-Drug Interaction) và thuốc -- bệnh nền đối với các ca bệnh lão khoa phức tạp.
    \item \textbf{Tích hợp Cảm biến Theo dõi Đường huyết Liên tục (CGM -- IoT):} Kết nối với các thiết bị cảm biến dán dưới da (như Freestyle Libre) thông qua Bluetooth Low Energy (BLE) để theo dõi biến thiên đường huyết thời gian thực (Time-in-Range -- TIR), cảnh báo nguy cơ hạ đường huyết ban đêm cho bệnh nhân.
    \item \textbf{Chuẩn hóa Cổng Giao tiếp Bệnh án Điện tử HL7/FHIR:} Xây dựng API đạt chuẩn quốc tế HL7/FHIR (Fast Healthcare Interoperability Resources) cho phép tích hợp trực tiếp DiaAgent-MAS vào hệ thống Quản lý Bệnh viện (HIS) và Hồ sơ Bệnh án Điện tử (EMR) tại các cơ sở khám chữa bệnh công lập và tư nhân tại Việt Nam.
\end{enumerate}
"""
