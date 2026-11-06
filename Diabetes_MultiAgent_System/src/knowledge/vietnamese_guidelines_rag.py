#!/usr/bin/env python3
"""
vietnamese_guidelines_rag.py
=============================
Hệ thống RAG (Retrieval-Augmented Generation) tra cứu hướng dẫn lâm sàng
chính thống của Bộ Y Tế và Viện Dinh Dưỡng dành cho bệnh nhân Đái Tháo Đường.

Nguồn tài liệu:
- Quyết định 5481/QĐ-BYT: Hướng dẫn chẩn đoán và điều trị đái tháo đường típ 2
- Tài liệu Dinh dưỡng lâm sàng Viện Dinh Dưỡng Quốc Gia (NIN)
- Khuyến cáo ADA 2024 (American Diabetes Association) Standards of Care
"""

import os
import re
import math
from typing import List, Dict, Any, Optional


CLINICAL_CHUNKS = [
    {
        "id": "byt_diag_01",
        "title": "Tiêu chuẩn chẩn đoán Đái tháo đường theo Bộ Y Tế (QĐ 5481/QĐ-BYT)",
        "category": "Chẩn đoán",
        "content": (
            "Tiêu chuẩn chẩn đoán đái tháo đường dựa vào 1 trong 4 tiêu chuẩn sau đây: "
            "1. Glucose huyết tương lúc đói (FPG) >= 126 mg/dL (7.0 mmol/L). Nhịn ăn ít nhất 8 giờ. "
            "2. Glucose huyết tương ở thời điểm sau 2 giờ làm nghiệm pháp dung nạp glucose đường uống 75g (OGTT) >= 200 mg/dL (11.1 mmol/L). "
            "3. HbA1c >= 6.5% (48 mmol/mol), thực hiện tại phòng xét nghiệm chuẩn hóa NGSP/DCCT. "
            "4. Bệnh nhân có triệu chứng kinh điển của tăng glucose huyết (tiểu nhiều, uống nhiều, ăn nhiều, sụt cân không rõ nguyên nhân) "
            "hoặc cơn tăng glucose huyết cấp và mức glucose huyết tương bất kỳ >= 200 mg/dL (11.1 mmol/L)."
        ),
        "source": "QĐ 5481/QĐ-BYT - Mục II: Chẩn đoán"
    },
    {
        "id": "byt_target_02",
        "title": "Mục tiêu kiểm soát đường huyết và huyết áp (QĐ 5481/QĐ-BYT)",
        "category": "Mục tiêu điều trị",
        "content": (
            "Mục tiêu điều trị chung cho phần lớn người trưởng thành không có thai: "
            "- HbA1c: < 7.0% (53 mmol/mol) nhằm giảm biến chứng vi mạch. "
            "- Glucose huyết đói / trước ăn: 80 - 130 mg/dL (4.4 - 7.2 mmol/L). "
            "- Glucose huyết sau ăn 1-2 giờ: < 180 mg/dL (< 10.0 mmol/L). "
            "- Huyết áp mục tiêu: < 130/80 mmHg nếu dung nạp tốt, đặc biệt ở bệnh nhân có nguy cơ tim mạch hoặc albumin niệu. "
            "- Đối với người cao tuổi, thời gian mắc bệnh lâu, nhiều bệnh đồng mắc: mục tiêu HbA1c nới lỏng < 7.5% hoặc < 8.0% để tránh nguy cơ hạ đường huyết nguy hiểm."
        ),
        "source": "QĐ 5481/QĐ-BYT - Mục III: Mục tiêu điều trị"
    },
    {
        "id": "byt_pharmacotherapy_03",
        "title": "Chiến lược dùng thuốc hạ đường huyết bậc 1 và phối hợp (QĐ 5481 & ADA 2024)",
        "category": "Dược trị liệu",
        "content": (
            "Metformin là thuốc nền tảng đầu tay (First-line) được lựa chọn khởi đầu cho hầu hết bệnh nhân đái tháo đường típ 2 "
            "nếu không có chống chỉ định (eGFR >= 30 mL/min). Liều khởi đầu 500mg/ngày tăng dần để giảm tác dụng phụ tiêu hóa. "
            "Nếu bệnh nhân có nguy cơ tim mạch xơ vữa cao (ASCVD), suy tim (HF) hoặc bệnh thận mạn (CKD): "
            "Ưu tiên phối hợp sớm thuốc ức chế SGLT-2 (Dapagliflozin, Empagliflozin) hoặc đồng vận thụ thể GLP-1 bất kể mức HbA1c ban đầu. "
            "Khi Metformin đơn trị liệu không đạt mục tiêu sau 3 tháng: phối hợp thêm Sulfonylurea (Gliclazide MR) hoặc DPP-4i (Sitagliptin)."
        ),
        "source": "QĐ 5481/QĐ-BYT - Mục IV: Điều trị bằng thuốc"
    },
    {
        "id": "nin_nutrition_plate_04",
        "title": "Nguyên tắc dinh dưỡng Đĩa thức ăn (Plate Method) theo Viện Dinh Dưỡng",
        "category": "Dinh dưỡng",
        "content": (
            "Nguyên tắc phân chia khẩu phần ăn trong mỗi bữa ăn chính cho người tiểu đường: "
            "1. 1/2 đĩa thức ăn: Rau củ không chứa tinh bột (rau muống luộc, rau ngót, cải xanh, dưa chuột, súp lơ, cà chua). Ăn rau trước bữa ăn giúp tạo lớp màng nhớt làm chậm hấp thu tinh bột. "
            "2. 1/4 đĩa thức ăn: Thực phẩm giàu chất đạm nạc (thịt ức gà bỏ da, cá tươi, đậu phụ luộc, nấm, trứng). "
            "3. 1/4 đĩa thức ăn: Tinh bột chuyển hóa chậm (gạo lứt, khoai lang luộc, yến mạch nguyên hạt). Hạn chế tối đa cơm trắng tinh luyện, bún xào nhiều mỡ. "
            "4. Lượng muối tiêu thụ: dưới 5g muối/ngày (tương đương 1 thìa cà phê gạt ngang) để bảo vệ huyết áp và thận."
        ),
        "source": "Viện Dinh Dưỡng Quốc Gia (NIN) - Hướng dẫn Dinh dưỡng ĐTĐ"
    },
    {
        "id": "fitt_exercise_05",
        "title": "Nguyên tắc Hoạt động Thể lực FITT cho bệnh nhân Đái Tháo Đường",
        "category": "Vận động & Lối sống",
        "content": (
            "Phác đồ luyện tập chuẩn FITT: "
            "- Tần suất (Frequency): Tối thiểu 3 - 5 ngày/tuần, không nghỉ quá 2 ngày liên tiếp. "
            "- Cường độ (Intensity): Vừa phải (Moderate) - khi vận động vẫn có thể nói câu ngắn nhưng không hát được (nhịp tim đạt 50-70% nhịp tim tối đa). "
            "- Thời gian (Time): Ít nhất 150 phút/tuần bài tập nhịp điệu (Aerobic như đi bộ nhanh, đạp xe, bơi lội), chia đều 30 phút/ngày. "
            "Kết hợp 2-3 buổi/tuần bài tập kháng lực (Resistance training: squat nhẹ, chống đẩy tường, tạ tay 1-2kg). "
            "- Lưu ý an toàn: Nếu đường huyết trước tập < 100 mg/dL, cần ăn nhẹ 15-20g carb (1 quả chuối nhỏ, 1 hộp sữa tươi không đường) để phòng tránh hạ đường huyết."
        ),
        "source": "QĐ 5481/QĐ-BYT & ADA 2024 Lifestyle Management"
    },
    {
        "id": "diabetic_foot_care_06",
        "title": "Chăm sóc bàn chân và phòng ngừa loét hoại tử do biến chứng thần kinh/mạch máu",
        "category": "Phòng ngừa biến chứng",
        "content": (
            "Biến chứng thần kinh ngoại biên làm giảm hoặc mất cảm giác đau ở bàn chân: "
            "1. Quan sát bàn chân mỗi ngày trước gương hoặc nhờ người nhà xem có vết rách, bóng nước, vết chai hay mẩn đỏ không. "
            "2. Rửa chân bằng nước ấm, lau khô kỹ các kẽ ngón chân bằng khăn mềm sạch (không ngâm chân nước quá nóng gây bỏng). "
            "3. Tuyệt đối không đi chân đất cả trong nhà lẫn ngoài trời. Chọn giày dép mũi rộng, mềm, vừa vặn; kiểm tra lòng giày trước khi xỏ. "
            "4. Cắt móng chân thẳng ngang, không khoét sâu vào khóe móng. Nếu xuất hiện vết thương chảy dịch hoặc vết thâm đen lâu lành, phải đến bệnh viện ngay lập tức."
        ),
        "source": "QĐ 5481/QĐ-BYT - Chăm sóc Bàn chân Đái tháo đường"
    },
    {
        "id": "hypoglycemia_management_07",
        "title": "Quy tắc 15-15 xử trí cấp cứu Hạ đường huyết tại nhà",
        "category": "Cấp cứu khẩn cấp",
        "content": (
            "Dấu hiệu hạ đường huyết (Glucose < 70 mg/dL): Run tay, vã mồ hôi lạnh, tim đập nhanh hồi hộp, đói cồn cào, chóng mặt, lú lẫn. "
            "Xử trí ngay theo Quy tắc 15-15: "
            "1. Uống/ăn ngay 15g Carbohydrate hấp thu nhanh: 1/2 cốc nước ép trái cây ngọt (120ml), 3 viên kẹo ngọt, 1 thìa canh đường pha nước hoặc 1/2 lon nước ngọt có đường. "
            "2. Nghỉ ngơi tại chỗ và kiểm tra lại đường huyết sau 15 phút. "
            "3. Nếu đường huyết vẫn < 70 mg/dL: lặp lại thêm 15g carb. "
            "4. Khi đường huyết đã >= 70 mg/dL và còn hơn 1 giờ nữa mới đến bữa chính: ăn thêm bữa phụ có đạm và tinh bột phức hợp (1 lát bánh mì hoặc 1 ly sữa)."
        ),
        "source": "QĐ 5481/QĐ-BYT - Phác đồ Xử trí Hạ đường huyết"
    }
]


class VietnameseGuidelinesRAG:
    """
    Module RAG nội bộ truy xuất nhanh các hướng dẫn của Bộ Y Tế & Viện Dinh Dưỡng
    sử dụng thuật toán BM25 / TF-IDF Vectorizer nhẹ, độc lập và siêu nhanh.
    """

    def __init__(self, chunks: List[Dict[str, Any]] = CLINICAL_CHUNKS):
        self.chunks = chunks
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r"\w+", text.lower())
        # Lọc stopwords cơ bản tiếng Việt
        stopwords = {"và", "hoặc", "của", "cho", "ở", "tại", "là", "các", "những", "được", "trong", "để", "với", "có"}
        return [w for w in words if w not in stopwords and len(w) > 1]

    def _build_index(self):
        self.doc_tokens = []
        self.doc_lens = []
        self.df = {}

        for doc in self.chunks:
            full_text = f"{doc['title']} {doc['category']} {doc['content']}"
            tokens = self._tokenize(full_text)
            self.doc_tokens.append(tokens)
            self.doc_lens.append(len(tokens))
            unique_tokens = set(tokens)
            for t in unique_tokens:
                self.df[t] = self.df.get(t, 0) + 1

        self.num_docs = len(self.chunks)
        self.avg_doc_len = sum(self.doc_lens) / max(1, self.num_docs)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Truy vấn các đoạn văn bản hướng dẫn y tế liên quan nhất dựa trên BM25.
        """
        q_tokens = self._tokenize(query)
        if not q_tokens:
            return self.chunks[:top_k]

        k1 = 1.5
        b = 0.75
        scores = []

        for i, doc in enumerate(self.chunks):
            doc_len = self.doc_lens[i]
            tokens = self.doc_tokens[i]
            score = 0.0

            token_counts = {}
            for t in tokens:
                token_counts[t] = token_counts.get(t, 0) + 1

            for q in q_tokens:
                if q in token_counts:
                    tf = token_counts[q]
                    doc_freq = self.df.get(q, 0)
                    # IDF công thức Robertson-Spärck Jones
                    idf = math.log((self.num_docs - doc_freq + 0.5) / (doc_freq + 0.5) + 1.0)
                    tf_norm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / self.avg_doc_len)))
                    score += idf * tf_norm

            scores.append((score, self.chunks[i]))

        scores.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scores[:top_k]]


if __name__ == "__main__":
    rag = VietnameseGuidelinesRAG()
    print("--- TEST RAG HƯỚNG DẪN BỘ Y TẾ ---")
    query = "Tôi bị run tay vã mồ hôi đói cồn cào phải làm sao?"
    print(f"\nTruy vấn: '{query}'")
    results = rag.retrieve(query, top_k=2)
    for r in results:
        print(f"\n[Tiêu đề]: {r['title']} ({r['source']})")
        print(f"[Nội dung]: {r['content'][:250]}...")
