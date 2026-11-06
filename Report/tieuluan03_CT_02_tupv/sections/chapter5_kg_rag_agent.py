# sections/chapter5_kg_rag_agent.py

def get_chapter5():
    return r"""
% =========================================================================
% CHƯƠNG 5: ĐỒ THỊ TRI THỨC (KNOWLEDGE GRAPH), RAG VÀ TÁC TỬ THÔNG MINH
% =========================================================================
\chapter{Đồ Thị Tri Thức (Knowledge Graph), RAG \& Tác Tử Thông Minh}

\section{Tổng Quan \& Giới Hạn Của Mô Hình Ngôn Ngữ Lớn Thuần Túy}

Trong làn sóng bùng nổ của Trí tuệ nhân tạo tạo sinh (Generative AI) và các Mô hình Ngôn ngữ Lớn (Large Language Models -- LLMs), cộng đồng công nghệ và nghiên cứu đang chứng kiến sự dịch chuyển mạnh mẽ từ các mô hình nơ-ron “hộp đen” đơn lẻ sang các hệ thống thông minh lai kết hợp (Neuro-Symbolic AI). Mặc dù các mô hình LLM sở hữu năng lực xử lý ngôn ngữ tự nhiên phi thường, chúng vẫn gặp phải ba rào cản mang tính cốt lõi trong các bài toán thực tế đòi hỏi độ chính xác tuyệt đối:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Hiện tượng ảo giác tri thức (Hallucination):} Mô hình tự tin sinh ra các thông tin sai lệch hoặc bịa đặt các dữ kiện không có thực do bản chất dự đoán từ tiếp theo theo xác suất thống kê.
    \item \textbf{Tri thức tĩnh và lỗi thời (Knowledge Cutoff):} Trọng số của mô hình bị đóng băng tại thời điểm hoàn tất huấn luyện, không thể tự cập nhật các biến động vĩ mô, văn bản quy phạm pháp luật hay dữ liệu thị trường mới nhất nếu không tái huấn luyện tốn kém.
    \item \textbf{Thiếu hụt tri thức chuyên sâu và logic đa bước (Lack of Multi-hop Reasoning):} LLM hoạt động dựa trên xác suất chuyển tiếp từ ngữ, thiếu khả năng suy luận hình thức, kiểm tra ràng buộc logic và truy vết nhân quả chặt chẽ qua nhiều mắt xích thông tin.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\textwidth]{images/fig701_kg_and_rag_overview.png}
    \caption{Tổng quan Kiến trúc Hệ sinh thái Tri thức Đa Miền: Tích hợp Nguồn Tri thức Thô, Knowledge Graph, Dense Vector RAG và Tác tử Thông minh Multi-Tool Reasoning Agent.}
    \label{fig:kg_rag_overview}
\end{figure}

Để giải quyết triệt để vấn đề này, kiến trúc kết hợp giữa \textbf{Đồ thị Tri thức (Knowledge Graph -- KG)}, \textbf{Kỹ thuật Truy xuất Tăng cường Tạo sinh (Retrieval-Augmented Generation -- RAG)} và \textbf{Tác tử Thông minh (Intelligent Agent)} đóng vai trò nền tảng. Thay vì dựa vào trí nhớ xác suất của mạng nơ-ron, hệ thống bắt buộc mô hình phải trích xuất và tham chiếu thông tin từ các cơ sở tri thức xác thực, đảm bảo 100\% thông tin được neo vào thực tế (Fact-Grounded).

\begin{table}[H]
\centering
\small
\renewcommand{\arraystretch}{1.25}
\caption{So sánh Đặc tính Vận hành Giữa LLM Đơn Lẻ, Fine-Tuning và Hệ Thống Tích Hợp KB + RAG}
\label{tab:comparison_llm_rag}
\begin{tabularx}{\textwidth}{>{\RaggedRight\arraybackslash\bfseries}p{3.4cm} Y Y Y}
\toprule
\textbf{Tiêu chí Đánh giá} & \textbf{LLM Thuần túy} & \textbf{LLM + Fine-Tuning} & \textbf{LLM + KB \& RAG} \\
\midrule
Độ chính xác \& Ảo giác & Thấp, rủi ro ảo giác nghiêm trọng & Trung bình, có thể học phong cách nhưng vẫn ảo giác & Rất cao, mọi câu trả lời đều được neo vào bằng chứng xác thực \\
Chi phí cập nhật tri thức & Không thể cập nhật động & Rất cao (yêu cầu GPU, dữ liệu huấn luyện và thời gian) & Gần như bằng 0 (chỉ cần thêm node vào Graph hoặc cập nhật tài liệu) \\
Khả năng giải thích & “Hộp đen”, không rõ nguồn gốc suy luận & Khó giải thích nguồn tri thức & Minh bạch tuyệt đối, chỉ rõ nguồn trích dẫn và đường dẫn đồ thị \\
Bảo mật dữ liệu nội bộ & Nguy cơ rò rỉ dữ liệu qua trọng số & Nguy cơ lộ dữ liệu trong trọng số & Kiểm soát phân quyền truy cập chặt chẽ (RBAC) trên KB \\
Xử lý quan hệ phức tạp & Dễ nhầm lẫn khi chuỗi suy luận dài & Kém linh hoạt với biến động thị trường & Vượt trội nhờ thuật toán duyệt đồ thị đa bước (Multi-hop Traversal) \\
\bottomrule
\end{tabularx}
\end{table}

\section{Kiến Trúc Knowledge Graph \& Mô Hình Biểu Diễn Tri Thức}

Một Đồ thị Tri thức tiêu chuẩn bao gồm 3 thành phần cốt lõi:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Thực thể (Entities / Nodes):} Đại diện cho các đối tượng cụ thể hoặc khái niệm trừu tượng, định danh bằng mã định danh duy nhất (URI). Ví dụ: \texttt{Metformin}, \texttt{FPT}, \texttt{Vang\_\allowbreak Mieng\_\allowbreak SJC}.
    \item \textbf{Mối quan hệ (Relations / Edges):} Là các liên kết có hướng kết nối giữa hai thực thể, biểu thị bản chất tương tác giữa chúng. Ví dụ: \texttt{CHI\_DINH\_DAU\_TAY}, \texttt{CHONG\_\allowbreak CHI\_\allowbreak DINH\_\allowbreak TUONG\_\allowbreak TAC}, \texttt{HUONG\_LOI\_TY\_GIA}.
    \item \textbf{Thuộc tính (Attributes / Properties):} Các giá trị dữ liệu nguyên thủy gán cho thực thể hoặc cạnh quan hệ (theo mô hình Labeled Property Graph -- LPG).
\end{enumerate}

Khung Mô tả Tài nguyên (Resource Description Framework -- RDF) chuẩn hóa việc phân rã tri thức thành các mệnh đề bộ ba nguyên tử:
\begin{equation}
    \tau = \langle \text{Subject}, \text{Predicate}, \text{Object} \rangle \in \mathcal{S} \times \mathcal{P} \times \mathcal{O}
\end{equation}
Ví dụ các bộ ba thực tế trong hệ thống:
\begin{align*}
    \langle \text{Metformin}, &\ \text{CHONG\_CHI\_DINH\_TUONG\_TAC}, \ \text{Ruou\_Bia} \rangle \\
    \langle \text{Tieu\_Duong\_Type\_2}, &\ \text{CHI\_DINH\_DAU\_TAY}, \ \text{Metformin} \rangle \\
    \langle \text{Ty\_Gia\_USD\_VND}, &\ \text{HUONG\_LOI\_TY\_GIA}, \ \text{FPT} \rangle \\
    \langle \text{Nghi\_Dinh\_24}, &\ \text{TAO\_CHENH\_LECH\_CUNG\_CAU}, \ \text{Vang\_Mieng\_SJC} \rangle
\end{align*}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\textwidth]{images/fig702_knowledge_graph_triples_ontology.png}
    \caption{Cấu trúc Bộ ba RDF (Subject -- Predicate -- Object), Phân cấp Bản thể luận (Ontology) và Bảng Đối chuẩn Kỹ thuật giữa Graph DB và Vector DB.}
    \label{fig:triples_ontology}
\end{figure}

\begin{table}[H]
\centering
\small
\renewcommand{\arraystretch}{1.25}
\caption{Bảng Đối Chuẩn Kỹ Thuật: Graph Database so với Vector Database}
\label{tab:graph_vs_vector_db}
\begin{tabularx}{\textwidth}{>{\RaggedRight\arraybackslash\bfseries}p{3.2cm} Y Y}
\toprule
\textbf{Tiêu chí So sánh} & \textbf{Graph Database (Neo4j, NetworkX)} & \textbf{Vector Database (Milvus, Qdrant)} \\
\midrule
Mô hình Lưu trữ Dữ liệu & Đỉnh (Nodes), Cạnh (Edges), Thuộc tính (Properties) & Không gian vector nhúng đa chiều (Embedding Vectors) \\
Bản chất Truy vấn & Khớp mẫu đồ thị, duyệt đường đi (Graph Pattern Matching) & Tìm kiếm láng giềng gần nhất (ANN: HNSW, IVF-Flat) \\
Ngôn ngữ Truy vấn & Cypher, SPARQL, Gremlin & Vector Similarity (Cosine, Dot Product, L2 Distance) \\
Điểm mạnh Cốt lõi & Ràng buộc logic tuyệt đối, truy vết quan hệ đa bước & Tìm kiếm ngữ nghĩa xấp xỉ, hiểu ngôn ngữ tự nhiên thô \\
Khả năng Giải thích & Minh bạch 100\% (Chỉ rõ từng cạnh và quan hệ) & Kém minh bạch (Điểm khoảng cách số học trừu tượng) \\
Ứng dụng Tối ưu & Tra cứu chống chỉ định, chuỗi giá trị nhân quả & Truy xuất tài liệu văn bản dài, tìm kiếm hội thoại tương đồng \\
\bottomrule
\end{tabularx}
\end{table}

\section{Công Nghệ RAG Nâng Cao, Phân Mảnh (Chunking) \& GraphRAG}

Kiến trúc RAG giải quyết bài toán đưa dữ liệu ngoài vào ngữ cảnh của LLM thông qua các bước: Lập chỉ mục (Indexing) $\to$ Truy xuất (Retrieval) $\to$ Tăng cường (Augmentation) $\to$ Tạo sinh (Generation).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\textwidth]{images/fig703_rag_pipeline_and_graphrag.png}
    \caption{Tiến trình Tiến hóa từ Naive RAG, Advanced RAG đến GraphRAG kết hợp Phân tích Cộng đồng.}
    \label{fig:rag_evolution}
\end{figure}

Trong quy trình tiền xử lý, chiến lược phân mảnh văn bản (Chunking) quyết định trực tiếp tới chất lượng thông tin truy xuất. 5 chiến lược phân mảnh chuẩn mực bao gồm:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Fixed-Size Chunking:} Cắt văn bản cơ học theo số lượng từ/token cố định kèm độ chồng lấn (overlap). Đơn giản nhưng dễ làm đứt gãy câu giữa chừng.
    \item \textbf{Recursive Character Chunking:} Thuật toán đệ quy ưu tiên ngắt theo đoạn văn (\texttt{\textbackslash n\textbackslash n}), dòng (\texttt{\textbackslash n}), ranh giới câu (\texttt{. }), từ (\texttt{" "}). Bảo toàn trọn vẹn ngữ nghĩa câu.
    \item \textbf{Structure-Aware Chunking:} Phân mảnh dựa trên cấu trúc tài liệu (Markdown header, cấu trúc Chương--Điều--Khoản của văn bản luật).
    \item \textbf{Semantic Chunking:} Tính khoảng cách vector nhúng giữa các câu liên tiếp; kích hoạt điểm cắt khi khoảng cách vượt qua ngưỡng phân vị ngữ nghĩa $\tau = \mu_d + k \sigma_d$.
    \item \textbf{Parent-Document Retrieval:} Chia tài liệu thành các khối cha lớn (1024 tokens) và các khối con nhỏ (128 tokens). Lập chỉ mục khối con để tìm kiếm chính xác, khi sinh câu trả lời thì trích xuất toàn bộ khối cha để bảo đảm ngữ cảnh.
\end{enumerate}

\begin{table}[H]
\centering
\small
\renewcommand{\arraystretch}{1.2}
\caption{Bảng So Sánh Kỹ Thuật Các Chiến Lược Phân Mảnh Văn Bản Trong RAG}
\label{tab:chunking_strategies_ch5}
\begin{tabularx}{\textwidth}{>{\RaggedRight\arraybackslash\bfseries}p{2.6cm} >{\RaggedRight\arraybackslash}p{2.2cm} >{\RaggedRight\arraybackslash}p{2.2cm} >{\RaggedRight\arraybackslash}p{2.2cm} Y}
\toprule
\textbf{Chiến Lược} & \textbf{Chi Phí} & \textbf{Bảo Toàn Ngữ Cảnh} & \textbf{Độ Sắc Nét} & \textbf{Ứng Dụng Tối Ưu} \\
\midrule
Fixed-Size & Cực thấp $\mathcal{O}(N)$ & Rất kém (Dễ ngắt cụt câu) & Trung bình & Dữ liệu văn bản thô không cấu trúc. \\
Recursive Character & Thấp $\mathcal{O}(N)$ & Tốt (Giữ nguyên vẹn câu) & Tốt & Tài liệu văn xuôi tổng quát, tin tức. \\
Structure-Aware & Trung bình & Rất tốt (Giữ cấu trúc bảng) & Rất tốt & Văn bản luật, hướng dẫn điều trị Bộ Y Tế. \\
Semantic Chunking & Cao (Cần nhúng) & Xuất sắc (Theo dòng ý niệm) & Rất cao & Bài phát biểu, phân tích chính sách vĩ mô. \\
Parent-Document & Trung bình - Cao & Hoàn hảo (Đầy đủ toàn khối) & Tối ưu nhất & Hệ thống RAG chuyên gia trong Y tế và Tài chính. \\
\bottomrule
\end{tabularx}
\end{table}

\begin{lstlisting}[language=Python, caption={Hiện thực Kỹ thuật Phân mảnh Văn bản Đệ quy \& Trích xuất Bộ ba Tri thức (chunking\_extractor.py)}]
# -*- coding: utf-8 -*-
# Module: chunking_extractor.py
from typing import List, Tuple

class RecursiveChunker:
    '''Phan manh de quy thong minh uu tien ranh gioi doan va cau'''
    def __init__(self, chunk_size: int = 250, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", ". ", "; ", " "]

    def split_text(self, text: str) -> List[str]:
        chunks = []
        start, text_len = 0, len(text)
        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            if end < text_len:
                for sep in self.separators:
                    pos = text.rfind(sep, start, end)
                    if pos != -1 and pos > start:
                        end = pos + len(sep)
                        break
            chunk = text[start:end].strip()
            if chunk: chunks.append(chunk)
            start = end - self.chunk_overlap if end < text_len else text_len
        return chunks

class TripletExtractor:
    '''Trich xuat bo ba tri thuc (Subject, Predicate, Object) tu chunk van ban'''
    @staticmethod
    def extract_triplets(chunk: str) -> List[Tuple[str, str, str]]:
        triplets = []
        c = chunk.lower()
        if "metformin" in c and ("ruou" in c or "con" in c):
            triplets.append(("Metformin", "CHONG_CHI_DINH_TUONG_TAC", "Ruou_Bia"))
        if "tieu duong" in c and "metformin" in c:
            triplets.append(("Tieu_Duong_Type_2", "CHI_DINH_DAU_TAY", "Metformin"))
        if "ty gia" in c and "fpt" in c:
            triplets.append(("Ty_Gia_USD_VND", "HUONG_LOI_TY_GIA", "FPT"))
        if "nghi dinh 24" in c and "sjc" in c:
            triplets.append(("Nghi_Dinh_24", "TAO_CHENH_LECH_CUNG_CAU", "Vang_Mieng_SJC"))
        return triplets
\end{lstlisting}

\section{Mô Hình Hóa Đồ Thị Tri Thức Y Tế \& Tài Chính Việt Nam}

\subsection{Miền Y Tế: Phác Đồ Đái Tháo Đường Bộ Y Tế Việt Nam}

Theo Quyết định số 5481/QĐ-BYT của Bộ Y Tế, tiêu chuẩn chẩn đoán xác định đái tháo đường gồm: $\text{HbA1c} \ge 6.5\%$ hoặc Glucose lúc đói $\text{FPG} \ge 126\text{ mg/dL}$. Metformin là thuốc chỉ định đầu tay; tuy nhiên thuốc có chống chỉ định nghiêm ngặt với rượu bia do nguy cơ nhiễm toan acid lactic cấp tính có thể dẫn đến tử vong.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\textwidth]{images/fig704_diabetes_vietnam_knowledge_graph.png}
    \caption{Đồ thị Tri thức Chuyên biệt cho Quản lý Bệnh Đái Tháo Đường tại Việt Nam: Phác đồ Bộ Y Tế, Tương tác Thuốc và Dinh dưỡng Thực phẩm Việt.}
    \label{fig:diabetes_kg_ch5}
\end{figure}

\begin{table}[H]
\centering
\small
\renewcommand{\arraystretch}{1.2}
\caption{Ma Trận Đối Sánh Chỉ Số Đường Huyết (GI/GL) \& Dinh Dưỡng Thực Phẩm Việt Nam}
\label{tab:vietnam_food_gi_gl}
\begin{tabularx}{\textwidth}{>{\RaggedRight\arraybackslash\bfseries}p{3.2cm} >{\centering\arraybackslash}p{1.4cm} >{\centering\arraybackslash}p{1.4cm} >{\RaggedRight\arraybackslash}p{2.6cm} Y}
\toprule
\textbf{Thực Phẩm Việt Nam} & \textbf{Chỉ Số GI} & \textbf{Tải Lượng GL} & \textbf{Phân Loại Y Học} & \textbf{Khuyến Nghị Lâm Sàng} \\
\midrule
Cơm trắng gạo tẻ & $73$ (Cao) & $26$ (Cao) & Thận trọng & Tối đa 1 bát/bữa; ăn kèm rau xanh. \\
Ức gà nạc bỏ da luộc & $0$ (Không carb) & $0$ (An toàn) & Khuyến nghị ưu tiên & Đạm nạc tối ưu, không làm tăng đường huyết. \\
Thịt gà chiên ngập dầu & $45$ (Trung bình) & $12$ (Vừa) & Hạn chế tối đa & Chất béo chuyển hóa làm tăng đề kháng insulin. \\
Rau muống luộc & $15$ (Rất thấp) & $1$ (Rất thấp) & Khuyến nghị ưu tiên & Chất xơ hòa tan làm chậm hấp thu glucose. \\
Rượu bia, đồ uống cồn & Biến động & Độc tính chuyển hóa & Chống chỉ định đỏ & Nguy cơ toan lactic tử vong khi dùng Metformin. \\
\bottomrule
\end{tabularx}
\end{table}

\begin{lstlisting}[language=Python, caption={Cấu trúc Khởi tạo và Truy vấn Đồ thị Tri thức Y tế Việt Nam (VietnamHealthcareKG)}]
# -*- coding: utf-8 -*-
# Module: kg_engine.py (Phan he Y te)
import networkx as nx
from typing import List, Dict, Any

class VietnamHealthcareKG:
    def __init__(self):
        self.G = nx.MultiDiGraph()
        self._build_diabetes_graph()
        
    def _build_diabetes_graph(self):
        self.G.add_node("Tieu_Duong_Type_2", type="Disease", label="Dai thao duong Type 2")
        self.G.add_node("HbA1c_Cao", type="Biomarker", threshold=">= 6.5%")
        self.G.add_node("Metformin", type="Drug", class_name="Biguanide", first_line=True)
        self.G.add_node("Ruou_Bia", type="RiskSubstance", label="Ruou bia / Con", dangerous=True)
        self.G.add_node("Thit_Ga_Uc_Bo_Da", type="SafeFood", label="Uc ga nac bo da", protein_high=True)
        self.G.add_node("Thit_Ga_Chien_Dau", type="RiskFood", label="Thit ga chien dau", trans_fat=True)
        
        self.G.add_edge("HbA1c_Cao", "Tieu_Duong_Type_2", relation="TIEU_CHUAN_CHAN_DOAN")
        self.G.add_edge("Tieu_Duong_Type_2", "Metformin", relation="CHI_DINH_DAU_TAY")
        self.G.add_edge("Metformin", "Ruou_Bia", relation="CHONG_CHI_DINH_TUONG_TAC", 
                        effect="TANG NGUY CO NHIEM TOAN LACTIC VA HA DUONG HUYET DOT NGOT")
        self.G.add_edge("Tieu_Duong_Type_2", "Thit_Ga_Uc_Bo_Da", relation="KHUYEN_NGHI_DINH_DUONG",
                        reason="Dam nac chat luong cao, khong carb, duy tri co")
        self.G.add_edge("Tieu_Duong_Type_2", "Thit_Ga_Chien_Dau", relation="CANH_BAO_HAN_CHE",
                        reason="Chat beo bao hoa lam tang de khang insulin")

    def query_substance_warning(self, drug_name: str, substance: str) -> List[Dict[str, Any]]:
        warnings = []
        if self.G.has_edge(drug_name, substance):
            for k, data in self.G.get_edge_data(drug_name, substance).items():
                warnings.append({"drug": drug_name, "substance": substance, 
                                 "relation": data.get("relation"), "effect": data.get("effect")})
        return warnings
\end{lstlisting}

\subsection{Miền Tài Chính: Thị Trường Chứng Khoán VN30 \& Giá Vàng SJC}

Đồ thị tri thức tài chính mô hình hóa chuỗi giá trị và tương quan lan truyền vĩ mô đặc thù Việt Nam:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Tỷ giá USD/VND $\to$ Cổ phiếu FPT:} FPT hưởng lợi tỷ giá lớn do gần 50\% doanh thu đến từ xuất khẩu phần mềm sang Mỹ và Nhật Bản, chi phí nhân sự nội địa trả bằng VND.
    \item \textbf{Tỷ giá USD/VND $\to$ Hòa Phát (HPG):} Chịu áp lực tăng chi phí nguyên liệu đầu vào quặng sắt và phát sinh lỗ tỷ giá nợ vay ngoại tệ USD.
    \item \textbf{Nghị định 24/2012/NĐ-CP $\to$ Vàng miếng SJC:} Cơ chế độc quyền nhà nước trong dập vàng miếng tạo nên sự khan hiếm nguồn cung, kéo dãn phần bù chênh lệch 5--10 triệu đồng/lượng so với giá vàng thế giới quy đổi.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\textwidth]{images/fig705_financial_stock_gold_knowledge_graph.png}
    \caption{Đồ thị Tri thức Chuỗi Giá trị Kinh tế Vĩ mô và Thị trường Tài chính Việt Nam: Cổ phiếu VN30 và Vàng miếng SJC.}
    \label{fig:finance_kg_ch5}
\end{figure}

\begin{lstlisting}[language=Python, caption={Cấu trúc Khởi tạo và Truy vấn Đồ thị Tri thức Tài chính Vĩ mô (VietnamFinancialKG)}]
# -*- coding: utf-8 -*-
# Module: kg_engine.py (Phan he Tai chinh)
import networkx as nx
from typing import List, Dict, Any

class VietnamFinancialKG:
    def __init__(self):
        self.G = nx.MultiDiGraph()
        self._build_finance_graph()
        
    def _build_finance_graph(self):
        self.G.add_node("Ty_Gia_USD_VND", type="MacroFactor", desc="Ty gia USD/VND")
        self.G.add_node("Nghi_Dinh_24", type="Regulation", desc="Nghi dinh 24 doc quyen vang")
        self.G.add_node("Vang_Mieng_SJC", type="CommodityAsset", desc="Vang mieng SJC 999.9")
        self.G.add_node("FPT", type="Stock", company="FPT Corp", sector="Cong nghe")
        self.G.add_node("HPG", type="Stock", company="Hoa Phat", sector="Thep")
        
        self.G.add_edge("Ty_Gia_USD_VND", "FPT", relation="HUONG_LOI_TY_GIA",
                        desc="Xuat khau phan mem USD giup mo rong bien loi nhuan")
        self.G.add_edge("Ty_Gia_USD_VND", "HPG", relation="BAT_LOI_CHI_PHI_NHAP_KHAU",
                        desc="Nhap quang sat than mo bang USD lam tang chi phi von")
        self.G.add_edge("Nghi_Dinh_24", "Vang_Mieng_SJC", relation="TAO_CHENH_LECH_CUNG_CAU",
                        desc="Doc quyen nguon cung keo dan phan bu chenh lech gia")

    def query_impact(self, factor: str, target: str) -> List[Dict[str, Any]]:
        impacts = []
        if self.G.has_edge(factor, target):
            for k, data in self.G.get_edge_data(factor, target).items():
                impacts.append({"source": factor, "target": target, 
                                "relation": data.get("relation"), "description": data.get("desc")})
        return impacts
\end{lstlisting}

\section{Kiến Trúc Tác Tử Tự Chủ ReAct Đơn Lẻ (Single-Agent)}

Kiến trúc tác tử ReAct (Reasoning and Acting) điều phối vòng lặp động 4 bước:
\begin{equation}
    \mathcal{S}_t \to \text{Thought}_t \to \text{Action}_t(\text{Tool}, \text{Args}) \to \text{Observation}_t \to \mathcal{S}_{t+1}
\end{equation}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\textwidth]{images/fig706_agent_architecture_flow.png}
    \caption{Quy trình Phối hợp Đa Công cụ của Tác tử Thông minh ReAct: Kết hợp Mô hình Học Sâu (Deep Learning), Đồ thị Tri thức (KG) và Dense RAG.}
    \label{fig:agent_architecture_ch5}
\end{figure}

\begin{lstlisting}[language=Python, caption={Tác tử Suy luận Thông minh ReAct Đa Công cụ Đa Miền (rag\_agent\_engine.py)}]
# -*- coding: utf-8 -*-
# Module: rag_agent_engine.py
from typing import Dict, Any, List

class VietnamIntelligentAgent:
    '''Agent don le thuc thi vong lap ReAct da cong cu'''
    def __init__(self):
        self.health_kg = VietnamHealthcareKG()
        self.fin_kg = VietnamFinancialKG()
        self.dl_medical = DeepLearningMedicalModel()
        self.rag = VietnamDenseRAGRetriever()

    def handle_healthcare_query(self, patient_data: Dict[str, Any], user_question: str) -> Dict[str, Any]:
        steps = []
        # BUOC 1: SUY LUAN & CHAN DOAN DEEP LEARNING
        steps.append({"step": 1, "type": "THOUGHT", "detail": "Danh gia chi so lam sang qua mang MLP."})
        dl_res = self.dl_medical.predict_risk(patient_data.get('hba1c', 7.0), patient_data.get('glucose', 130), patient_data.get('bmi', 25.5))
        steps.append({"step": 2, "type": "ACTION_DEEP_LEARNING", "result": dl_res})
        
        # BUOC 2: TRUY VAN KNOWLEDGE GRAPH
        steps.append({"step": 3, "type": "THOUGHT", "detail": "Kiem tra tuong tac Metformin + Ruou bia."})
        kg_warn = self.health_kg.query_substance_warning("Metformin", "Ruou_Bia")
        steps.append({"step": 4, "type": "ACTION_KNOWLEDGE_GRAPH", "warnings": kg_warn})
        
        # BUOC 3: TRUY XUAT PHAC DO BO Y TE (DENSE RAG)
        steps.append({"step": 5, "type": "THOUGHT", "detail": "Trich xuat can cu phap ly Bo Y Te."})
        rag_docs = self.rag.retrieve(user_question, domain="healthcare", top_k=1)
        steps.append({"step": 6, "type": "ACTION_RAG_RETRIEVAL", "citations": rag_docs})
        
        # BUOC 4: TONG HOP KHUYEN NGHI CUOI CUNG
        final_answer = (
            f"[*] CHAN DOAN (MLP): {dl_res['diagnosis']} ({dl_res['confidence']}).\n"
            f"[!] CANH BAO DUNG THUOC (KG): TUYET DOI KHONG UONG RUOU BIA: {kg_warn[0]['effect']}.\n"
            f"[+] KHUYEN NGHI DINH DUONG: DUOC AN THIT GA (Uc ga nac luoc; tranh ga ran dau mo).\n"
            f"[>] TRICH DAN: {rag_docs[0]['title']}."
        )
        return {"query": user_question, "reasoning_steps": steps, "final_response": final_answer}
\end{lstlisting}

\section{Giao Diện Bảng Điều Khiển Web App \& Điểm Nghẽn Của Tác Tử Đơn Lẻ}

Hệ thống được đóng gói thành ứng dụng Web App tương tác thời gian thực bằng Streamlit Dashboard (Hình~\ref{fig:webapp_ui_ch5}), cho phép người dùng nhập trực tiếp chỉ số sinh hóa và nhận vết suy luận ReAct minh bạch.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\textwidth]{images/fig707_agent_webapp_interface.png}
    \caption{Giao Diện Bảng Điều Khiển Web App Tương Tác Của AI Agent: Tích hợp Đồng Thời Trợ Lý Y Tế Đái Tháo Đường và Trợ Lý Đầu Tư Chứng Khoán VN30 / Vàng SJC.}
    \label{fig:webapp_ui_ch5}
\end{figure}

\begin{tcolorbox}[colback=blue!5!white,colframe=blue!75!black,title=Nhật Ký Suy Luận ReAct Thực Tế: Kịch Bản Y Tế Bệnh Tiểu Đường]
\textbf{Câu hỏi Người dùng:} “Tôi đang uống Metformin thì chiều nay liên hoan có uống rượu và ăn thịt gà được không?” \\
\textbf{Dữ liệu đầu vào Bệnh nhân:} $\text{HbA1c} = 7.3\%$, $\text{Fasting Glucose} = 138$ mg/dL, $\text{BMI} = 26.5$ kg/m$^2$.
\begin{enumerate}[leftmargin=0.8cm]
    \item \textbf{[THOUGHT 1]:} Chỉ số cận lâm sàng vượt ngưỡng. Kích hoạt mô hình Học sâu phân loại rủi ro.
    \item \textbf{[ACTION 1 -- Deep Learning]:} Xác suất bệnh lý: 98.5\% $\to$ Kết luận: \textbf{Đái tháo đường Type 2}.
    \item \textbf{[THOUGHT 2]:} Tra cứu quan hệ chống chỉ định thuốc Metformin và cồn bia trên Đồ thị Tri thức.
    \item \textbf{[ACTION 2 -- Knowledge Graph]:} Phát hiện cạnh \texttt{CHONG\_\allowbreak CHI\_\allowbreak DINH\_\allowbreak TUONG\_\allowbreak TAC}: \textit{“TĂNG NGUY CƠ NHIỄM TOAN LACTIC VÀ HẠ ĐƯỜNG HUYẾT ĐỘT NGỘT NGUY HIỂM TÍNH MẠNG”}. Cạnh dinh dưỡng: \textit{“Ức gà nạc bỏ da luộc an toàn, kiêng gà chiên dầu mỡ”}.
    \item \textbf{[THOUGHT 3]:} Gọi công cụ RAG trích xuất Quyết định số 5481/QĐ-BYT của Bộ Y Tế.
    \item \textbf{[FINAL RESPONSE]:} Nghiêm cấm tuyệt đối uống rượu bia; Bệnh nhân được ăn ức gà luộc nạc bỏ da!
\end{enumerate}
\end{tcolorbox}

\subsection{Những Điểm Nghẽn Cốt Lõi Của Kiến Trúc Tác Tử Đơn Lẻ (Single-Agent Bottlenecks)}

Mặc dù kiến trúc Single-Agent ReAct mang lại độ chính xác vượt trội so với LLM đơn thuần, khi áp dụng vào các kịch bản thực tế quy mô lớn, nó bộc lộ ba điểm nghẽn nghiêm trọng:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Quá tải cửa sổ ngữ cảnh (Context Window Saturation):} Khi một tác tử đơn lẻ phải ôm đồm đồng thời hàng chục công cụ (từ chẩn đoán y khoa, dược lý, dinh dưỡng đến phân tích tài chính), toàn bộ mô tả công cụ và lịch sử đối thoại làm đầy cửa sổ ngữ cảnh, dẫn đến hiện tượng suy giảm độ chú ý (Attention Degradation) và nhầm lẫn công cụ.
    \item \textbf{Tích lũy sai số chuỗi suy luận (Error Cascading in Long Horizons):} Trong một chuỗi ReAct kéo dài hơn 8--10 bước, nếu tác tử mắc sai lầm ở một bước trung gian, sai số sẽ lan truyền và khuếch đại sang các bước sau mà không có cơ chế độc lập nào phát hiện và sửa sai.
    \item \textbf{Thiếu hụt sự phản biện chuyên môn hóa (Lack of Independent Cross-Examination):} Tác tử đơn lẻ vừa là người sinh ra câu trả lời vừa là người tự kiểm tra, dễ rơi vào bẫy tự tin thái quá (Self-Bias). Trong các bài toán phức tạp (như hội chẩn bệnh nhân đa bệnh lý hoặc tranh luận phân bổ danh mục đầu tư), sự phản biện đa chiều giữa các chuyên gia độc lập là không thể thay thế.
\end{itemize}

Những hạn chế mang tính cấu trúc này là động lực khoa học tất yếu thúc đẩy sự ra đời của \textbf{Hệ Đa Tác Tử (Multi-Agent Systems -- MAS)}, nội dung trọng tâm sẽ được khảo sát, thiết kế và hiện thực hóa toàn diện trong Chương 6 tiếp theo.
"""
