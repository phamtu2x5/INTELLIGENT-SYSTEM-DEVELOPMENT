# -*- coding: utf-8 -*-
"""
sections/experiments.py
Chương 3: Triển khai Thực nghiệm và Đánh giá Kết quả
"""

def get_experiments():
    return r"""
% =========================================================================
% CHƯƠNG 3: TRIỂN KHAI THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ
% =========================================================================
\section{TRIỂN KHAI THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ}

\subsection{Dữ liệu Huấn luyện và Đánh giá Mô hình Học máy}

\subsubsection{Bộ Dữ liệu Lâm sàng và Phân tích Khám phá (EDA)}
Mô hình học máy dự báo nguy cơ trong DiaAgent-MAS được huấn luyện và đối chuẩn trên bộ dữ liệu lâm sàng quy mô lớn gồm \textbf{100,000 hồ sơ bệnh nhân} (Diabetes Prediction Dataset từ cơ sở dữ liệu y tế cộng đồng). Bộ dữ liệu bao gồm 8 biến lâm sàng ban đầu: Giới tính (Gender), Tuổi (Age), Tiền sử Tăng huyết áp (Hypertension), Tiền sử Bệnh tim mạch (Heart Disease), Tiền sử Hút thuốc (Smoking History), Chỉ số Khối cơ thể (BMI), Chỉ số $\text{HbA1c}$ và Mức đường huyết đói (Blood Glucose Level).

\begin{figure}[H]
    \centering
    \begin{subfigure}[b]{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{images/fig201_diabetes_target_distribution.png}
        \caption{Phân phối nhãn mục tiêu (Mất cân bằng lớp: 8.5\% dương tính).}
        \label{fig:diabetes_target}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{images/fig203_diabetes_correlation_heatmap.png}
        \caption{Biểu đồ nhiệt tương quan Pearson giữa các đặc trưng y tế.}
        \label{fig:diabetes_corr}
    \end{subfigure}
    \caption{Phân tích Khám phá Dữ liệu Lâm sàng (Exploratory Data Analysis -- EDA) Đái tháo đường.}
    \label{fig:diabetes_eda}
\end{figure}

Dữ liệu phản ánh đặc thù mất cân bằng nghiêm trọng của bài toán sàng lọc y tế trong cộng đồng: chỉ có $8.5\%$ số ca mắc bệnh (8,500 ca dương tính) so với $91.5\%$ số ca không mắc bệnh (91,500 ca âm tính). Phân tích tương quan chỉ ra rằng hai chỉ số sinh hóa máu $\text{HbA1c}$ ($r = 0.44$) và $\text{Blood Glucose Level}$ ($r = 0.42$) có mối tương quan thuận mạnh nhất với nguy cơ đái tháo đường.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.96\textwidth]{images/fig202_diabetes_feature_distributions.png}
    \caption{Phân phối xác suất của các biến liên tục (Age, BMI, HbA1c, Blood Glucose) phân tách theo tình trạng bệnh.}
    \label{fig:diabetes_features}
\end{figure}

\subsubsection{Kết quả Đối chuẩn Các Thuật toán Học máy}
Chúng tôi tiến hành huấn luyện và so sánh đối chuẩn 4 kiến trúc học máy tiêu biểu trên cùng tập kiểm thử độc lập ($20,000$ mẫu, tỷ lệ phân chia Train/Test 80/20 có phân tầng Stratified K-Fold): \textbf{Logistic Regression (Hồi quy Logistic)}, \textbf{Random Forest (Rừng ngẫu nhiên)}, \textbf{Multi-Layer Perceptron (MLP Mạng nơ-ron đa tầng)}, và \textbf{LightGBM (Hệ thống đề xuất)}. 

\begin{table}[H]
\centering
\small
\caption{Bảng đối chuẩn hiệu năng các mô hình học máy trên tập kiểm thử độc lập}
\label{tab:model_comparison}
\begin{tabularx}{\textwidth}{@{} l c c c c c @{}}
\toprule
\textbf{Mô hình Học máy} & \textbf{Độ chính xác (Acc)} & \textbf{Precision} & \textbf{Recall (Độ nhạy)} & \textbf{F1-Score} & \textbf{ROC-AUC} \\
\midrule
Logistic Regression & 88.50\% & 52.10\% & 63.80\% & 57.36\% & 0.8845 \\
Random Forest & \textbf{96.85\%} & \textbf{94.21\%} & 68.45\% & \textbf{79.32\%} & 0.9612 \\
Multi-Layer Perceptron (MLP) & 92.15\% & 61.20\% & 74.30\% & 67.12\% & 0.9230 \\
\textbf{LightGBM (DiaAgent-MAS)} & 90.45\% & 47.85\% & \textbf{92.53\%} & 63.08\% & \textbf{0.9797} \\
\bottomrule
\end{tabularx}
\end{table}

\begin{figure}[H]
    \centering
    \begin{subfigure}[b]{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{images/fig211_diabetes_model_comparison.png}
        \caption{Biểu đồ so sánh trực quan các chỉ số đo lường hiệu năng.}
        \label{fig:model_comp_chart}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{images/fig214_diabetes_confusion_matrix.png}
        \caption{Ma trận nhầm lẫn (Confusion Matrix) của mô hình đề xuất.}
        \label{fig:confusion_matrix}
    \end{subfigure}
    \caption{Đánh giá Thực nghiệm Hiệu năng Mô hình Học máy Sàng lọc Nguy cơ Đái tháo đường.}
    \label{fig:ml_eval}
\end{figure}

\begin{tcolorbox}[colback=blue!5!white,colframe=ptitblue,title=Phân Tích Chuyên Sâu Về Ý Nghĩa Lâm Sàng Của Recall]
Trong bài toán sàng lọc y tế đối với các bệnh mạn tính nguy hiểm, \textbf{chỉ số Recall (Độ nhạy) và diện tích dưới đường cong ROC-AUC giữ vai trò quyết định tối thượng}, vượt trội hơn hẳn so với Accuracy hay Precision. 
\begin{itemize}[leftmargin=0.8cm]
    \item Nếu mô hình có Precision cao nhưng Recall thấp (như Random Forest chỉ đạt Recall $68.45\%$), nó sẽ \textbf{bỏ sót hơn 31\% số bệnh nhân thực sự mắc đái tháo đường} trong cộng đồng (âm tính giả -- False Negative). Những bệnh nhân bị bỏ sót này sẽ không được đi khám và tiếp tục âm thầm phát triển biến chứng mù lòa hoặc suy thận giai đoạn cuối.
    \item Ngược lại, mô hình \textbf{LightGBM đạt Recall vượt bậc lên tới 92.53\% và ROC-AUC đạt 0.9797}. Tỷ lệ bỏ sót ca bệnh giảm xuống mức cực thấp ($< 7.5\%$). Điều này chứng minh LightGBM là lựa chọn tối ưu tuyệt đối cho vai trò sàng lọc nguy cơ ban đầu trong hệ thống lâm sàng.
\end{itemize}
\end{tcolorbox}

\subsubsection{Minh bạch hóa Quyết định Y khoa bằng SHAP}
Để chuyển hóa mô hình LightGBM từ dạng "hộp đen" thành công cụ hỗ trợ quyết định y khoa có thể giải thích được, hệ thống áp dụng kỹ thuật TreeSHAP để trích xuất trọng số đóng góp của từng đặc trưng lâm sàng:
\begin{enumerate}[leftmargin=1.2cm]
    \item Chỉ số $\text{HbA1c}$ là biến số có tác động mạnh nhất: khi $\text{HbA1c} > 6.5\%$, giá trị SHAP dương nhảy vọt từ $+0.35$ đến $+0.65$, đẩy mạnh xác suất dự báo về phía mắc bệnh.
    \item Chỉ số Glucose lúc đói (Blood Glucose Level) là yếu tố quyết định thứ hai: các giá trị vượt ngưỡng $126\text{ mg/dL}$ đóng góp trực tiếp $+0.25$ đến $+0.45$ vào xác suất rủi ro.
    \item Chỉ số Khối cơ thể ($\text{BMI}$) và Tuổi (Age) đóng vai trò điều biến nền: những người có $\text{BMI} \ge 25\text{ kg/m}^2$ (thừa cân theo chuẩn châu Á) và tuổi trên 45 có nguy cơ nền tảng cao hơn hẳn, khuếch đại tác động tiêu cực của lượng đường trong máu.
\end{enumerate}

\subsection{Thu thập và Cấu trúc hóa Dữ liệu Thực tế từ Nhà thuốc FPT Long Châu}

Nhằm mang lại giá trị ứng dụng thực tiễn cao cho người dân Việt Nam, nhóm nghiên cứu đã xây dựng module \texttt{crawl\_longchau\_diabetes.py} để tự động thu thập và chuẩn hóa dữ liệu dược phẩm, thiết bị y tế chính hãng từ Hệ thống Nhà thuốc FPT Long Châu:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Cơ chế thu thập an toàn:} Gửi yêu cầu truy vấn API có phân trang, bóc tách cấu trúc dữ liệu theo 5 trường thông tin: Tên sản phẩm biệt dược (\texttt{brand\_name}), Hoạt chất chính (\texttt{active\_ingredient}), Nhóm điều trị (\texttt{drug\_class}), Đơn giá niêm yết (\texttt{unit\_price\_vnd}), Quy chế đơn thuốc (\texttt{is\_prescription\_rx}), và Đường dẫn tra cứu (\texttt{longchau\_url}).
    \item \textbf{Cơ sở dữ liệu cấu trúc hóa:} Đã trích xuất và phân loại thành công 50+ mặt hàng thiết yếu, lưu trữ tại \texttt{longchau\_diabetes\_products.json}. Cơ sở dữ liệu này được chia thành 2 nhóm chuyên biệt phục vụ phân luồng:
    \begin{enumerate}[leftmargin=0.8cm]
        \item \textbf{Nhóm Thiết bị Tự theo dõi tại nhà (Không kê đơn):} Máy đo đường huyết Accu-Chek Guide (1,450,000 VNĐ), Hộp 50 Que thử đường huyết Accu-Chek Instant (440,000 VNĐ), Hộp 100 kim lấy máu Accu-Chek Softclix (120,000 VNĐ).
        \item \textbf{Nhóm Dược phẩm Kiểm soát Đường huyết (Thuốc kê đơn Rx):} Glucophage $850\text{ mg}$ (Metformin Hydrochloride -- hộp 30 viên, 125,000 VNĐ), Diamicron MR $60\text{ mg}$ (Gliclazide phóng thích kéo dài -- hộp 60 viên, 210,000 VNĐ), Jardiance $10\text{ mg}$ (Empagliflozin -- bảo vệ tim thận, 680,000 VNĐ).
    \end{enumerate}
\end{itemize}

\subsection{Thực nghiệm Toàn diện trên Hai Ca Lâm sàng Điển hình}

Để chứng minh tính ưu việt của cơ chế Phân luồng Lâm sàng Kép và năng lực phối hợp phản biện của 7 Agent, hệ thống đã được thử nghiệm thực tế với 2 tình huống lâm sàng đại diện cho hai nhóm đối tượng phổ biến nhất trong thực tiễn.

\subsubsection{Ca Lâm sàng 1: Giai đoạn Sàng lọc Nguy cơ Ban đầu (Chưa có xét nghiệm)}
\begin{tcolorbox}[colback=lightgray,colframe=blue!60!black,title=Dữ Liệu Đầu Vào Ca Lâm Sàng 1]
\textbf{Người dùng nhập hội thoại:} \textit{“Tôi năm nay 55 tuổi, cao 1m65, nặng 74kg, dạo này hay khát nước liên tục, đêm đi tiểu 3 lần, người sụt 2kg. Tôi có bị tiểu đường không?”}
\end{tcolorbox}

\textbf{Quy trình phân tích và điều phối của Hệ Multi-Agent:}
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{TriageInterviewerAgent:} Nhận diện ý định \texttt{MEDICAL\_CONSULTATION}. Trích xuất thực thể: $\text{Tuổi} = 55$, $\text{Chiều cao} = 165.0\text{ cm}$, $\text{Cân nặng} = 74.0\text{ kg}$, tính toán $\text{BMI} = 27.2\text{ kg/m}^2$ (Thừa cân độ 1 theo chuẩn châu Á IDI \& WPRO). Bóc tách 3 triệu chứng kinh điển: khát nhiều, tiểu đêm, sụt cân. Xác định trạng thái dữ liệu: \texttt{INSUFFICIENT\_LABS} (chưa có xét nghiệm máu).
    \item \textbf{RiskPredictionAgent:} Phát hiện trạng thái \texttt{INSUFFICIENT\_LABS}, Agent lập tức \textbf{khóa hoàn toàn mô hình LightGBM}, gán \texttt{risk\_probability = None}. Thay vào đó, kích hoạt thang điểm sàng lọc lâm sàng không xâm lấn: Đạt 7 điểm (Tuổi $\ge 45$: +2, $\text{BMI} \ge 25$: +3, Triệu chứng khát/tiểu/sụt cân: +2) $\to$ Phân loại: \textbf{Nguy cơ Cao (Cần đi khám xét nghiệm máu sớm)}.
    \item \textbf{EndocrinologistAgent:} Đưa ra đánh giá chuyên môn chuẩn xác: \textit{“Chưa đủ dữ liệu xét nghiệm để khẳng định chẩn đoán. Theo Quyết định số 5481/QĐ-BYT, việc chẩn đoán xác định đái tháo đường bắt buộc phải dựa vào xét nghiệm định lượng máu tĩnh mạch. Tuyệt đối không tự ý mua và dùng thuốc hạ đường huyết khi chưa có kết quả xét nghiệm.”} Đề xuất chỉ định xét nghiệm cận lâm sàng: Định lượng Glucose huyết tương lúc đói (FPG) và $\text{HbA1c}$.
    \item \textbf{NutritionAgent:} Tính toán cân nặng lý tưởng của bệnh nhân là $58.5\text{ kg}$. Với mức độ lao động nhẹ, năng lượng mục tiêu hàng ngày được điều chỉnh về $1500\text{ kcal/ngày}$ để giảm dần $0.5\text{ kg/tuần}$. Thiết lập thực đơn mẫu: Sáng yến mạch nấu ức gà; Trưa cơm gạo lứt, cá thu sốt cà chua, canh rau ngót; Tối salad ức gà và canh bí đao luộc.
    \item \textbf{LifestyleCoachAgent:} Khuyến nghị chế độ vận động Aerobic đi bộ nhanh 30 phút/ngày (5 buổi/tuần); hướng dẫn quy tắc kiểm tra bàn chân hàng ngày.
    \item \textbf{PharmacyLocatorAgent:} Chỉ truy vấn các thiết bị theo dõi không cần kê đơn từ FPT Long Châu: Hộp que thử đường huyết Accu-Chek Instant (440,000 VNĐ) và Máy đo đường huyết Accu-Chek Guide (1,450,000 VNĐ).
    \item \textbf{SafetyGuardianAgent:} Kiểm tra toàn diện kết quả hội đồng: Xác nhận trạng thái \texttt{APPROVED}. Đảm bảo 100\% rằng không có bất kỳ dòng nào kê đơn thuốc hoặc gán nhãn khẳng định bệnh nhân bị đái tháo đường khi chưa có xét nghiệm.
\end{enumerate}

\subsubsection{Ca Lâm sàng 2: Giai đoạn Khẳng định Chẩn đoán \& Đa Bệnh lý Phức tạp}
\begin{tcolorbox}[colback=warnbg,colframe=warnframe,title=Dữ Liệu Đầu Vào Ca Lâm Sàng 2]
\textbf{Người dùng nhập hội thoại:} \textit{“Tôi 58 tuổi, cao 1m68, nặng 70kg, vừa có kết quả xét nghiệm máu: đường huyết đói 155 mg/dL và chỉ số HbA1c 7.8\%, độ lọc cầu thận eGFR là 42 mL/phút. Tôi đang uống Metformin 1000mg ngày 2 lần. Chiều nay tôi có tiệc liên hoan công ty thì có uống vài cốc bia và ăn nhiều đồ xào rán được không?”}
\end{tcolorbox}

\textbf{Quy trình phân tích và phản biện của Hệ Multi-Agent:}
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{TriageInterviewerAgent:} Bóc tách đầy đủ các chỉ số: $\text{Tuổi} = 58$, $\text{HbA1c} = 7.8\%$, $\text{Glucose} = 155\text{ mg/dL}$, $\text{eGFR} = 42\text{ mL/phút/1.73m}^2$, thuốc đang dùng \textit{"Metformin 1000mg x 2 lần/ngày"}, phát hiện ý định sử dụng rượu bia (\texttt{alcohol\_use = True}). Xác định trạng thái: \texttt{SUFFICIENT\_LABS}.
    \item \textbf{RiskPredictionAgent:} Kích hoạt mô hình LightGBM: Xác suất nguy cơ đạt \textbf{98.5\%} (Nhóm Nguy cơ Rất Cao). Trích xuất SHAP: $\text{HbA1c} = 7.8\%$ đóng góp $+0.43$, $\text{Glucose} = 155\text{ mg/dL}$ đóng góp $+0.33$.
    \item \textbf{EndocrinologistAgent:} Khẳng định chẩn đoán \textbf{Đái tháo đường Típ 2 kiểm soát đường huyết kém} theo QĐ 5481/QĐ-BYT. Thiết lập mục tiêu $\text{HbA1c} < 7.0\%$.
    \item \textbf{SafetyGuardianAgent (Kích hoạt Thẩm định Phản biện Khẩn cấp):}
    Agent Hộ vệ An toàn phát hiện hai mối nguy cơ đe dọa trực tiếp tính mạng người bệnh:
    \begin{itemize}[leftmargin=0.8cm]
        \item \textbf{CẢNH BÁO ĐỎ TƯƠNG TÁC THUỐC CỰC KỲ NGUY HIỂM:} Bệnh nhân đang dùng Metformin mà uống rượu bia sẽ ức chế quá trình đào thải acid lactic tại gan, làm bùng phát nguy cơ \textbf{Nhiễm toan Acid Lactic cấp tính (Lactic Acidosis)} -- biến chứng có tỷ lệ tử vong lên tới 50\%. Agent Hộ vệ ban hành lệnh \textbf{CẤM TUYỆT ĐỐI RƯỢU BIA}.
        \item \textbf{CẢNH BÁO CHỐNG CHỈ ĐỊNH QUÁ LIỀU THUỐC THEO CHỨC NĂNG THẬN:} Chỉ số $\text{eGFR} = 42\text{ mL/phút/1.73m}^2$ phản ánh bệnh nhân đã bước vào \textbf{Suy thận mạn giai đoạn 3b}. Theo Quyết định 5481/QĐ-BYT, liều tối đa cho phép của Metformin ở mức eGFR này là $1000\text{ mg/ngày}$. Việc bệnh nhân đang dùng liều $2000\text{ mg/ngày}$ ($1000\text{ mg} \times 2$) là \textbf{QUÁ LIỀU NGUY HIỂM}, gây tích tụ thuốc và đẩy nhanh tiến trình suy thận. Agent yêu cầu bệnh nhân thông báo ngay cho bác sĩ điều trị để giảm 50\% liều hoặc cân nhắc phối hợp nhóm thuốc ức chế SGLT-2 (như Dapagliflozin/Empagliflozin) có tác dụng bảo tồn thận.
    \end{itemize}
    \item \textbf{NutritionAgent \& LifestyleCoachAgent:} Yêu cầu kiêng đồ xào rán, mỡ động vật; bổ sung chất đạm nạc chọn lọc ($0.8\text{ g/kg/ngày}$ phù hợp bệnh thận mạn); hướng dẫn quy tắc 15-15 phòng ngừa hạ đường huyết do vận động.
    \item \textbf{PharmacyLocatorAgent:} Cung cấp thông tin giá thuốc Glucophage $500\text{ mg}$ (để điều chỉnh giảm liều) và đường link tra cứu chính sách BHYT tại Nhà thuốc Long Châu.
\end{enumerate}

\subsection{Triển khai Giao diện Web Ứng dụng Trực quan (Streamlit Chatbot-First)}

Toàn bộ hệ thống DiaAgent-MAS được đóng gói và triển khai thành ứng dụng Web tương tác thời gian thực trên nền tảng Streamlit, áp dụng triết lý thiết kế hiện đại \textbf{Chatbot-First Healthcare Interface}.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.98\textwidth]{images/fig_diaagent_chat_ui.png}
    \caption{Giao Diện Web Ứng Dụng Thực Tế Của Hệ Multi-Agent DiaAgent-MAS: Thiết kế Song song 2 Cột Giữa Hội thoại Tư vấn Trực tuyến và Bảng Điều khiển Lâm sàng Thời gian thực.}
    \label{fig:streamlit_ui}
\end{figure}

Giao diện ứng dụng được cấu trúc khoa học thành hai không gian làm việc đồng bộ:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Cột 1: Cuộc trò chuyện tư vấn trực tuyến (Conversational Chat Column):} 
    \begin{itemize}[leftmargin=0.8cm]
        \item Cung cấp các nút bấm nhanh (Pill Buttons) cho phép tải ngay dữ liệu thực nghiệm Ca 1 và Ca 2 chỉ với một cú nhấp chuột.
        \item Luồng hội thoại đàm thoại mượt mà giữa Người dùng và Trợ lý Sức khỏe DiaAgent.
        \item \textbf{Tối ưu hóa trải nghiệm nhập liệu (Unified Input Experience):} Loại bỏ hoàn toàn sự xung đột giữa ô \texttt{st.text\_area} và nút bấm phụ. Toàn bộ hội thoại được vận hành duy nhất thông qua ô nhập liệu chuẩn \texttt{st.chat\_input} đặt cố định tại chân trang giao diện, ngăn chặn hoàn toàn lỗi kích hoạt hai lần (double-trigger error).
    \end{itemize}
    \item \textbf{Cột 2: Hồ sơ đánh giá sức khỏe \& Khuyến nghị hành động (Clinical Dashboard Column):}
    \begin{itemize}[leftmargin=0.8cm]
        \item Huy hiệu trạng thái thời gian thực hiển thị rõ chế độ hoạt động: "Giai đoạn sàng lọc nguy cơ (Chưa có xét nghiệm)" hoặc "Giai đoạn khẳng định chẩn đoán".
        \item Bảng chỉ số tổng quan 3 cột: Mức độ nguy cơ, Xác suất dự báo ML (hoặc thông báo Không kích hoạt), và Thể trạng BMI tính toán tự động.
        \item Hộp khuyến nghị điều trị nổi bật trích xuất căn cứ pháp lý QĐ 5481/QĐ-BYT.
        \item Danh mục thiết bị y tế và dược phẩm đề xuất từ FPT Long Châu kèm giá niêm yết, phân loại kê đơn rõ ràng và đường dẫn truy cập trực tiếp.
        \item Menu mở rộng (Expander) chứa Kế hoạch dinh dưỡng theo NIN và Vận động thể lực FITT.
    \end{itemize}
\end{enumerate}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.98\textwidth]{images/fig707_agent_webapp_interface.png}
    \caption{Giao Diện Bảng Điều Khiển Mở Rộng: Tích Hợp Chi Tiết Mô Hình Học Máy và Rà Soát Dược Lý Ngầm.}
    \label{fig:agent_dashboard_deep}
\end{figure}

\subsubsection{Tối ưu hóa Hiệu năng và Độ trễ Phản hồi Hệ thống}
Trong các phiên bản thử nghiệm sơ khai, hệ thống gặp hiện tượng phản hồi chậm (độ trễ lên tới 16 -- 20 giây cho mỗi lượt tương tác) do hàm \texttt{chat\_turn} kích hoạt cuộc gọi API Gemini hai lần liên tiếp (một lần trong luồng hội chẩn đa Agent và một lần để tái tóm tắt văn bản chat). 

Thông qua kỹ thuật tái cấu trúc luồng dữ liệu \textbf{Single-Pass Synthesis}:
\begin{itemize}[leftmargin=1.2cm]
    \item Triệt tiêu hoàn toàn cuộc gọi LLM trùng lặp tại hàm điều phối \texttt{chat\_turn}. Bản tóm tắt chuyên môn toàn diện do \texttt{SafetyGuardianAgent} tạo ra (\texttt{state.final\_patient\_summary}) được sử dụng trực tiếp làm nội dung phản hồi trong khung chat.
    \item Thời gian phản hồi trung bình (Response Latency) được \textbf{cắt giảm ngoạn mục từ 16.5 giây xuống chỉ còn 5.2 -- 6.8 giây} (giảm hơn 60\% độ trễ), mang lại trải nghiệm tương tác trực tuyến mượt mà và tức thời cho người sử dụng.
\end{itemize}
"""
