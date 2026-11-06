# -*- coding: utf-8 -*-
"""
sections/architecture.py
Chương 2: Thiết kế Kiến trúc Hệ thống DiaAgent-MAS
"""

def get_architecture():
    return r"""
% =========================================================================
% CHƯƠNG 2: THIẾT KẾ KIẾN TRÚC HỆ THỐNG DIAAGENT-MAS
% =========================================================================
\section{THIẾT KẾ KIẾN TRÚC HỆ THỐNG DIAAGENT-MAS}

\subsection{Kiến trúc Tổng thể và Cơ chế Điều phối Trung tâm}

\subsubsection{Sơ đồ Luồng Dữ liệu và Tương tác Đa Agent}
Kiến trúc nhận thức của hệ thống \textbf{DiaAgent-MAS} được xây dựng dựa trên nguyên lý điều phối hỗn hợp: kết hợp luồng tuần tự (Sequential Pipeline) có phân nhánh điều kiện (Conditional Branching) và vòng lặp phản biện an toàn (Reflection Guardian Loop). Toàn bộ hệ thống được chia thành 3 lớp chức năng cốt lõi:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Lớp Giao tiếp \& Tiếp đón (Interaction \& Ingestion Layer):} Phụ trách hội thoại trực tiếp với người dùng, phân tích ý định (Intent Classification) và bóc tách thực thể lâm sàng có cấu trúc.
    \item \textbf{Lớp Trí tuệ Đa Agent Chuyên khoa (Specialized Multi-Agent Brain):} Gồm các Agent chuyên trách giải quyết từng khía cạnh y tế độc lập: dự báo nguy cơ học máy, chẩn đoán nội tiết, tính toán dinh dưỡng, huấn luyện lối sống và tra cứu dược phẩm thực tế.
    \item \textbf{Lớp Hộ vệ An toàn \& Kiểm chứng Phản biện (Safety Guardian \& Verification Layer):} Giám sát toàn bộ trạng thái, kiểm tra chéo các chống chỉ định y khoa theo phác đồ Bộ Y Tế, phát hiện ảo giác và phê duyệt kết quả cuối cùng trước khi phản hồi người dùng.
\end{enumerate}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.98\textwidth]{images/fig706_agent_architecture_flow.png}
    \caption{Sơ đồ Kiến trúc Điều phối Luồng Dữ liệu Toàn diện của Hệ Multi-Agent DiaAgent-MAS.}
    \label{fig:agent_architecture_flow}
\end{figure}

\subsubsection{Cấu trúc Trạng thái Dùng chung (Global State Schema)}
Nhằm đảm bảo tính nhất quán dữ liệu giữa các Agent độc lập và ngăn ngừa việc mất mát ngữ cảnh qua nhiều vòng hội thoại, hệ thống thiết kế một \textbf{Trạng thái Toàn cục (Global State)} được chuẩn hóa bằng thư viện Pydantic. Mọi Agent đều đọc và ghi dữ liệu vào cấu trúc dùng chung này:

\begin{lstlisting}[style=pythonstyle, caption={Định nghĩa Cấu trúc Trạng thái Toàn cục Pydantic (state\_schema.py)}]
class PatientProfile(BaseModel):
    # Ho so lam sang va cac chi so sinh hoc cua nguoi benh
    patient_id: str = "P_GUEST_001"
    name: str = "Nguoi dung"
    age: int = 50
    gender: str = "Nam"  # 'Nam' hoac 'Nu'
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None
    hypertension: int = 0
    heart_disease: int = 0
    smoking_history: str = "never"
    
    # Chi so xet nghiem dinh luong (Mac dinh None de bao ve an toan)
    hba1c: Optional[float] = None              # % HbA1c
    blood_glucose_level: Optional[float] = None # mg/dL Glucose doi
    egfr: Optional[float] = None               # mL/min chuc nang than
    alcohol_use: bool = False
    reported_symptoms: List[str] = Field(default_factory=list)
    data_completeness: str = "INSUFFICIENT_LABS"

class DiabetesMASState(BaseModel):
    # Toan bo Trang thai Chia se Toan cuc cua He Multi-Agent
    patient_profile: PatientProfile = Field(default_factory=PatientProfile)
    ml_prediction: MLPredictionResult = Field(default_factory=MLPredictionResult)
    clinical_prescription: ClinicalPrescription = Field(default_factory=ClinicalPrescription)
    nutrition_recommendation: NutritionRecommendation = Field(default_factory=NutritionRecommendation)
    lifestyle_recommendation: LifestyleRecommendation = Field(default_factory=LifestyleRecommendation)
    pharmacy_items: List[PharmacyItem] = Field(default_factory=list)
    safety_check: SafetyCheckResult = Field(default_factory=SafetyCheckResult)
    final_patient_summary: str = ""
    chat_history: List[Dict[str, str]] = Field(default_factory=list)
    agent_execution_logs: List[Dict[str, Any]] = Field(default_factory=list)
\end{lstlisting}

\subsection{Cơ chế Phân luồng Lâm sàng Kép (Dual-Mode Clinical Routing)}

Một đóng góp kiến trúc quan trọng bậc nhất của DiaAgent-MAS là việc hiện thực hóa \textbf{Cơ chế Phân luồng Lâm sàng Kép (Dual-Mode Clinical Routing)}. Trong thực tế y khoa, người tìm kiếm tư vấn đái tháo đường luôn rơi vào một trong hai nhóm đối tượng hoàn toàn khác nhau về bản chất pháp lý và chuyên môn y tế.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.98\textwidth]{images/fig604_healthcare_multi_agent_flow.png}
    \caption{Quy trình Hội chẩn và Phân luồng Lâm sàng Kép: Cơ chế Phân định giữa Giai đoạn Sàng lọc Nguy cơ và Khẳng định Chẩn đoán.}
    \label{fig:healthcare_mas_flow}
\end{figure}

Bảng~\ref{tab:dual_mode} đối sánh sự khác biệt triệt để giữa hai chế độ hoạt động trong hệ thống:

\begin{table}[H]
\centering
\footnotesize
\caption{Bảng đặc tả Cơ chế Phân luồng Lâm sàng Kép (Dual-Mode Clinical Routing)}
\label{tab:dual_mode}
\begin{tabularx}{\textwidth}{@{} l Y Y @{}}
\toprule
\textbf{Tiêu chí phân định} & \textbf{Chế độ Sàng lọc Nguy cơ (INSUFFICIENT\_LABS)} & \textbf{Chế độ Khẳng định Chẩn đoán (SUFFICIENT\_LABS)} \\
\midrule
Điều kiện kích hoạt & Bệnh nhân chỉ cung cấp triệu chứng lâm sàng (khát nước, sụt cân, tiểu nhiều) hoặc thể trạng (chiều cao, cân nặng, BMI); \textbf{chưa có xét nghiệm máu}. & Bệnh nhân đã cung cấp ít nhất một kết quả xét nghiệm định lượng: $\text{HbA1c}$ (\%) hoặc $\text{Glucose}$ đói ($\text{mg/dL}$ hoặc $\text{mmol/L}$). \\
Trạng thái Mô hình ML & \textbf{Khóa hoàn toàn (Disabled):} Trả về \texttt{risk\_probability = None}. Không hiển thị bất kỳ con số xác suất giả định nào gây hoang mang cho người dùng. & \textbf{Kích hoạt (Enabled):} Chạy suy luận LightGBM, trích xuất xác suất nguy cơ (\%) và Top-3 giá trị đóng góp đặc trưng SHAP. \\
Phương pháp đánh giá & Thang điểm sàng lọc lâm sàng không xâm lấn (Non-invasive Risk Score): Kết hợp yếu tố tuổi, tiền sử gia đình, tăng huyết áp và ngưỡng BMI châu Á. & Phân tầng nguy cơ chính thức theo Quyết định số 5481/QĐ-BYT: Đối chiếu trực tiếp ngưỡng $\text{HbA1c} \ge 6.5\%$ hoặc $\text{FPG} \ge 126\text{ mg/dL}$. \\
Định hướng điều trị & \textbf{Tuyệt đối không kê đơn thuốc.} Hướng dẫn bệnh nhân đến bệnh viện làm xét nghiệm máu định lượng để xác định chẩn đoán. & Đề xuất phác đồ thuốc khuyến nghị (như Metformin đầu tay), thiết lập mục tiêu $\text{HbA1c} < 7.0\%$, kiểm tra liều lượng theo chức năng thận. \\
Sản phẩm Long Châu gợi ý & Máy đo đường huyết cá nhân, que thử Accu-Chek để tự theo dõi đường huyết tại nhà (nhóm Thiết bị y tế không cần đơn). & Thuốc hạ đường huyết theo chỉ định bác sĩ, kèm sản phẩm hỗ trợ dinh dưỡng chuyên biệt (Sữa đái tháo đường, hạt ngũ cốc nguyên cám). \\
\bottomrule
\end{tabularx}
\end{table}

\subsection{Chi tiết Thiết kế 7 Agent Chuyên trách trong DiaAgent-MAS}

\subsubsection{Agent 1: TriageInterviewerAgent (Tiếp đón \& Trích xuất Thực thể Lâm sàng)}
Agent Tiếp đón giữ vai trò tiền đồn của hệ thống. Trước đây, nhiều hệ thống sử dụng biểu thức chính quy (Regex) để bắt từ khóa. Tuy nhiên, trong thực tế lâm sàng, người dùng Việt Nam nhập liệu với ngữ cảnh tự nhiên phong phú, sử dụng từ lóng hoặc thể hiện các ý định phủ định (ví dụ: \textit{“tôi không uống rượu bia”, “dạo này không thấy sụt cân”}). Các quy tắc Regex thông thường dễ dàng bộc lộ sự giòn vỡ nghiêm trọng (bắt gặp chữ "rượu bia" là tự động gán có uống rượu).

Để khắc phục triệt để, \textbf{TriageInterviewerAgent} được thiết kế chạy trực tiếp mô hình ngôn ngữ lớn (Gemini LLM) với kỹ thuật ép khuôn JSON Strict Schema (Function Calling / Structured Outputs):
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Phân loại ý định hai mức (Intent Classification):} Phân biệt chuẩn xác giữa ý định xã giao thuần túy (\texttt{GREETING} -- như \textit{"xin chào", "chào bạn"}) và ý định khám bệnh (\texttt{MEDICAL\_CONSULTATION}). Khi người dùng chào hỏi, hệ thống gửi phản hồi thân thiện và dừng ngay chu trình, tránh kích hoạt lãng phí các Agent phân tích phía sau.
    \item \textbf{Bóc tách thực thể y tế (Clinical NER Extraction):} Trích xuất chính xác tuổi, giới tính, chiều cao (tự động chuyển đổi "1m65" thành $165.0\text{ cm}$), cân nặng, các triệu chứng kinh điển (khát nước, tiểu nhiều, sụt cân), kết quả xét nghiệm ($\text{HbA1c}$, Glucose với khả năng quy đổi tự động $\text{mmol/L} \to \text{mg/dL}$ bằng hệ số nhân $18.018$), và chỉ số lọc thận $\text{eGFR}$.
    \item \textbf{Xử lý ngữ nghĩa phủ định và tích lũy trạng thái đa vòng (Multi-turn Accumulation):} Tự động hiểu các cấu trúc phủ định, đồng thời duy trì danh sách triệu chứng lũy tiến qua các lượt chat liên tiếp (\texttt{reported\_symptoms.extend}), đảm bảo không làm mất thông tin người dùng đã cung cấp ở các câu trước.
\end{enumerate}

\subsubsection{Agent 2: RiskPredictionAgent (Mô hình hóa Nguy cơ Kép \& An toàn Dữ liệu)}
Agent Dự báo nguy cơ chịu trách nhiệm tính toán định lượng tình trạng sức khỏe của người bệnh. Agent thực hiện cơ chế an toàn dữ liệu nghiêm ngặt (Null-Safety Verification):
\begin{itemize}[leftmargin=1.2cm]
    \item Kiểm tra toàn vẹn các thuộc tính thể trạng (\texttt{bmi is not None}, \texttt{age is not None}). Tự động tính toán chỉ số $\text{BMI} = \frac{\text{Cân nặng (kg)}}{(\text{Chiều cao (m)})^2}$.
    \item Nếu dữ liệu ở trạng thái \texttt{INSUFFICIENT\_LABS}: Tuyệt đối không gọi mô hình LightGBM; gán \texttt{risk\_probability = None} và kích hoạt thuật toán tính điểm nguy cơ lâm sàng không xâm lấn ADA/FINDRISC.
    \item Nếu dữ liệu ở trạng thái \texttt{SUFFICIENT\_LABS}: Chuẩn hóa vector 13 đặc trưng đầu vào qua \texttt{StandardScaler}, gọi mô hình học máy LightGBM đã huấn luyện, xuất xác suất nguy cơ $\hat{y} \in [0, 1]$ và tính toán giải thích SHAP cục bộ cho ca bệnh.
\end{itemize}

\subsubsection{Agent 3: EndocrinologistAgent (Bác sĩ Nội tiết RAG Phác đồ Bộ Y Tế)}
Agent Bác sĩ Nội tiết đóng vai trò chuyên gia lâm sàng cao cấp, kế thừa tri thức từ Quyết định số 5481/QĐ-BYT:
\begin{itemize}[leftmargin=1.2cm]
    \item Xác định tình trạng chẩn đoán: Nếu $\text{HbA1c} \ge 6.5\%$ hoặc $\text{FPG} \ge 126\text{ mg/dL}$, Agent thiết lập kết luận khẳng định đái tháo đường típ 2, đề xuất mục tiêu điều trị cụ thể ($\text{HbA1c} < 7.0\%$, Glucose đói $80 - 130\text{ mg/dL}$, Glucose sau ăn $< 180\text{ mg/dL}$).
    \item Nếu chưa có xét nghiệm: Đưa ra danh mục chỉ định xét nghiệm cận lâm sàng bắt buộc cần làm (Glucose huyết tương lúc đói, $\text{HbA1c}$, tổng phân tích nước tiểu, xét nghiệm chức năng thận Creatinine/eGFR).
    \item Đề xuất phác đồ thuốc khuyến nghị có kèm điều kiện chuyên môn: Khởi đầu bằng Metformin $500\text{ mg}$ hoặc $850\text{ mg}$, uống trong hoặc ngay sau bữa ăn để giảm tác dụng phụ trên đường tiêu hóa.
\end{itemize}

\subsubsection{Agent 4: NutritionAgent (Chuyên gia Dinh dưỡng Thực phẩm Việt Nam)}
Agent Dinh dưỡng chịu trách nhiệm tính toán năng lượng và thiết kế thực đơn phù hợp với văn hóa ẩm thực Việt Nam dựa trên tiêu chuẩn Viện Dinh Dưỡng (NIN):
\begin{itemize}[leftmargin=1.2cm]
    \item Tính toán cân nặng lý tưởng và năng lượng mục tiêu hàng ngày (TDEE). Trường hợp bệnh nhân chưa cung cấp chiều cao/cân nặng (\texttt{bmi is None}), Agent tự động chuyển về chế độ dự phòng an toàn (Fallback standard: $1800\text{ kcal/ngày}$) mà không làm dừng chương trình.
    \item Phân bổ năng lượng theo bữa ăn: Bữa sáng 20\%, Bữa trưa 35\%, Bữa tối 30\%, Bữa phụ (nếu cần) 15\%.
    \item Đưa ra danh mục "Thay thế Lành mạnh" (Healthy Swaps): Thay gạo trắng bằng gạo lứt huyết rồng hoặc yến mạch; thay nước ngọt đóng chai bằng trà xanh hoặc nước lọc ngâm chanh; thay thịt mỡ chiên rán bằng cá hấp hoặc đậu phụ luộc.
\end{itemize}

\subsubsection{Agent 5: LifestyleCoachAgent (Huấn luyện viên Vận động \& Phòng ngừa Biến chứng)}
Agent Huấn luyện viên Lối sống xây dựng chương trình hoạt động thể lực cá nhân hóa theo nguyên tắc \textbf{FITT} (Frequency -- Intensity -- Time -- Type):
\begin{itemize}[leftmargin=1.2cm]
    \item Vận động hiếu khí (Aerobic): Đi bộ nhanh, đạp xe hoặc bơi lội với tần suất tối thiểu 150 phút/tuần, không nghỉ quá 2 ngày liên tiếp.
    \item Vận động kháng lực (Resistance): Tập luyện các nhóm cơ lớn 2 lần/tuần.
    \item Quy tắc vàng chăm sóc bàn chân đái tháo đường: Rửa chân hàng ngày bằng nước ấm, kiểm tra kẽ ngón chân tìm vết xước hoặc phồng rộp, tuyệt đối không đi chân trần trên sàn nhà.
    \item \textbf{Giao thức xử trí Hạ đường huyết cấp tính (Quy tắc 15-15):} Khi có biểu hiện run tay, đói cồn cào, vã mồ hôi: Bệnh nhân lập tức uống $15\text{g}$ đường hấp thu nhanh (tương đương 3 thìa đường pha nước ấm hoặc $150\text{ mL}$ nước ngọt có đường), ngồi nghỉ 15 phút và kiểm tra lại đường huyết mao mạch.
\end{itemize}

\subsubsection{Agent 6: PharmacyLocatorAgent (Định vị Dược phẩm Thực tế FPT Long Châu)}
Để thu hẹp khoảng cách giữa tư vấn lý thuyết và khả năng tiếp cận y tế ngoài đời thực, \textbf{PharmacyLocatorAgent} tích hợp trực tiếp cơ sở dữ liệu cào tự động từ Hệ thống Nhà thuốc FPT Long Châu:
\begin{itemize}[leftmargin=1.2cm]
    \item Khi bệnh nhân ở giai đoạn \texttt{INSUFFICIENT\_LABS}: Agent chỉ truy xuất các sản phẩm thuộc nhóm Thiết bị y tế không cần đơn: Hộp que thử đường huyết Accu-Chek Instant (Hộp 50 que, giá niêm yết 440,000 VNĐ), Máy đo đường huyết Accu-Chek Guide (1,450,000 VNĐ) để phục vụ theo dõi tại nhà.
    \item Khi bệnh nhân ở giai đoạn \texttt{SUFFICIENT\_LABS}: Agent bổ sung thông tin tham khảo về các biệt dược chuẩn: Glucophage $500\text{ mg}$ / $850\text{ mg}$ (Metformin Hydrochloride), Diamicron MR $60\text{ mg}$ (Gliclazide), ghi rõ quy chế "Thuốc kê đơn (Rx) -- Bắt buộc có đơn của Bác sĩ điều trị", cùng đường link tra cứu chính hãng tại nhà thuốc.
    \item Ước tính chi phí điều trị dự kiến hàng tháng (Monthly Out-of-pocket Cost) giúp người bệnh chủ động ngân sách tài chính.
\end{itemize}

\subsubsection{Agent 7: SafetyGuardianAgent (Hộ vệ An toàn \& Kiểm chứng Phản biện)}
Agent Hộ vệ An toàn giữ vai trò kiểm duyệt chéo cuối cùng (Final Gatekeeper) và sở hữu quyền phủ quyết (Veto Authority):
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Kiểm soát tính hợp lệ của chẩn đoán:} Kiểm tra nếu trạng thái là \texttt{INSUFFICIENT\_LABS} mà bất kỳ Agent nào đưa ra kết luận khẳng định bệnh hoặc chỉ định tên thuốc điều trị, Agent Hộ vệ lập tức gạt bỏ nội dung đó và ghi đè bằng cảnh báo yêu cầu làm xét nghiệm.
    \item \textbf{Cảnh báo tương tác dược lý nguy hiểm tính mạng:} Kiểm tra tiền sử sử dụng rượu bia (\texttt{alcohol\_use == True}) kết hợp với thuốc Metformin. Nếu phát hiện, lập tức phát cảnh báo đỏ về nguy cơ toan acid lactic cấp tính.
    \item \textbf{Kiểm tra ngưỡng an toàn chức năng thận (Renal Safety):} Đối chiếu chỉ số $\text{eGFR}$: Nếu $\text{eGFR} < 30\text{ mL/phút/1.73m}^2$, kích hoạt cảnh báo chống chỉ định tuyệt đối Metformin; nếu $30 \le \text{eGFR} < 45$, phát cảnh báo yêu cầu giảm liều tối đa xuống $1000\text{ mg/ngày}$.
    \item \textbf{Tổng hợp văn bản tư vấn nhất quán:} Hợp nhất các khuyến nghị chuyên môn của 6 Agent thành một bản tóm tắt mạch lạc, chuẩn mực y khoa để phản hồi cho người bệnh.
\end{itemize}

\subsection{Hiện Thực Hóa Cơ Sở Dữ Liệu Đồ Thị Neo4j \& GraphRAG (code RAG + link\_DB)}

\subsubsection{Mô Hình Hóa Đồ Thị Tri Thức ĐTĐ trên Neo4j (kb\_diabet)}
Để chuyển hóa toàn bộ tri thức y khoa lý thuyết thành một hệ quản trị đồ thị có khả năng truy vấn theo thời gian thực với độ trễ thấp và khả năng mở rộng cao, hệ thống triển khai cơ sở dữ liệu đồ thị \textbf{Neo4j Community Server} (truy cập thông qua giao thức Bolt tại cổng 7687 và giao diện đồ họa Web Browser tại cổng 7474).

Đồ thị tri thức mang mã định danh \texttt{kb\_diabet} được tích hợp từ 3 nguồn dữ liệu then chốt:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Văn bản PDF chính thức:} Toàn văn Quyết định số 5481/QĐ-BYT của Bộ Y Tế (77 trang) về tiêu chuẩn 4 ngưỡng chẩn đoán định lượng, phác đồ dùng thuốc bậc 1, bảng phân tầng liều Metformin theo $\text{eGFR}$ và quy tắc cấp cứu hạ đường huyết.
    \item \textbf{Tri thức Web \& Y khoa Lâm sàng:} Bài viết chuyên khoa đái tháo đường của Bệnh viện Đa khoa Quốc tế Vinmec về các triệu chứng kinh điển (khát nước, sụt cân, tiểu nhiều) và quy trình kiểm tra phòng ngừa biến chứng loét bàn chân đái tháo đường.
    \item \textbf{Thương mại \& Dinh dưỡng:} Danh mục 50+ sản phẩm thiết bị đo đường huyết và biệt dược từ Nhà thuốc FPT Long Châu, kết hợp bảng chỉ số đường huyết thực phẩm (GI/GL) của Viện Dinh Dưỡng Quốc Gia (NIN).
\end{enumerate}

Hiện tại, đồ thị \texttt{kb\_diabet} trên Neo4j đã được nạp thành công với cấu trúc quy chuẩn bao gồm \textbf{71 Nodes} thuộc 10 nhãn thực thể (\texttt{:Disease}, \texttt{:Complication}, \texttt{:Biomarker}, \texttt{:Drug}, \texttt{:AdverseEffect}, \texttt{:Food}, \texttt{:PharmacyProduct}, \texttt{:Source}, \texttt{:Comorbidity}, \texttt{:RiskFactor}) và \textbf{54 Relationships} có hướng (\texttt{:DIAGNOSED\_BY}, \texttt{:TREATS}, \texttt{:CONTRAINDICATED\_IN}, \texttt{:RISK\_OF}, \texttt{:MONITORED\_BY}, \texttt{:DISPENSED\_AS\_PRODUCT}, \texttt{:CAN\_BE\_REPLACED\_BY}, \texttt{:CITED\_FROM}).

Toàn bộ câu lệnh định nghĩa bản thể học và nạp dữ liệu được tự động sinh và lưu trữ bền vững tại tệp kịch bản Cypher: \texttt{Diabetes\_MultiAgent\_System/data/knowledge\_graph/kb\_diabet\_init.cypher}.

\subsubsection{Cơ Chế GraphRAG Liên Kết Cơ Sở Dữ Liệu (code RAG + link\_DB)}
Sự kết hợp giữa RAG (Retrieval-Augmented Generation) và CSDL Đồ thị Neo4j được hiện thực hóa qua module \texttt{neo4j\_graph\_rag.py} (cơ chế \textit{code RAG + link\_DB}). Thay vì chỉ dựa vào tìm kiếm tương đồng vector văn bản thuần túy vốn dễ bị phân mảnh ngữ nghĩa, GraphRAG thực hiện chu trình liên kết 3 bước:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Kích hoạt Truy vấn Cypher Định hướng (Directed Cypher Retrieval):} Căn cứ vào trạng thái lâm sàng của người bệnh (thuốc đang dùng, tiền sử rượu bia, chỉ số xét nghiệm $\text{eGFR}$), hệ thống sinh câu truy vấn Cypher trực tiếp vào Neo4j:
\begin{lstlisting}[language=SQL, caption={Ví dụ Truy vấn Cypher Kiểm tra Tương tác Thuốc Nguy hiểm trong Neo4j (code RAG + link\_DB)}]
MATCH (dr:Drug {id: 'METFORMIN'})-[r:RISK_OF]->(a:AdverseEffect {id: 'LACTIC_ACIDOSIS'})
RETURN dr.name AS drug, a.name AS adverse, r.trigger AS trigger, r.severity AS severity, a.mortality AS mortality;

MATCH (dr:Drug {id: 'METFORMIN'})-[r:CONTRAINDICATED_IN]->(c:Complication {id: 'CKD'})
RETURN dr.name AS drug, c.name AS complication, r.condition AS condition;
\end{lstlisting}
    \item \textbf{Trích xuất Sự thật Đồ thị (Graph Facts Extraction):} Trả về các ràng buộc cứng không thể chối cãi: \textit{"Metformin kết hợp Cồn gây nguy cơ Nhiễm toan Lactic cấp tính (Tử vong 50\%); Chống chỉ định tuyệt đối nếu eGFR < 30 mL/phút; Cần giảm 50\% liều nếu 30 <= eGFR < 45"}.
    \item \textbf{Hợp nhất Ngữ cảnh Tăng cường (Augmented Context Synthesis):} Hợp nhất các sự thật từ Neo4j với các đoạn phân đoạn văn bản (Text Chunks) từ QĐ 5481/QĐ-BYT và Vinmec để hình thành lời nhắc (Prompt) có căn cứ xác thực, truyền vào Agent Hội thoại Chatbot và Agent Hộ vệ An toàn.
\end{enumerate}
"""
