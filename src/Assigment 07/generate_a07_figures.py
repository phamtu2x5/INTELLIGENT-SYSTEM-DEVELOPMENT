# -*- coding: utf-8 -*-
"""
Script: generate_a07_figures.py (REVISED - SPACIOUS, ELEGANT, PUBLICATION-GRADE DESIGN)
Mục đích: Thiết kế lại toàn bộ 7 biểu đồ cho Assignment 07 với:
- Giãn cách rộng rãi (Ample whitespace & breathing room)
- Bố cục thẻ rời (Floating modular cards), không dính sát viền
- Luồng mũi tên thông thoáng, trực quan, có nhãn rõ ràng
- Phối màu cao cấp, chuyên nghiệp theo phong cách IEEE / Nature Machine Intelligence
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Cấu hình font và kích thước chuẩn
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 9.5
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

OUTPUT_DIR = "Report/Assigment 07/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_fig(fig, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='#ffffff')
    plt.close(fig)
    print(f"✓ Đã lưu thành công biểu đồ thoáng đẹp: {filepath}")

# =============================================================================
# 1. FIG 701: TỔNG QUAN HỆ SINH THÁI TRI THỨC (GIÃN CÁCH THÔNG THOÁNG)
# =============================================================================
def generate_fig701():
    fig, ax = plt.subplots(figsize=(15.0, 8.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # Header Banner - Thoáng đãng
    banner = patches.FancyBboxPatch((0.05, 0.90), 0.90, 0.075, boxstyle="round,pad=0.015",
                                    facecolor='#0f172a', edgecolor='#334155', lw=1.2)
    ax.add_patch(banner)
    ax.text(0.50, 0.948, "KIẾN TRÚC TỔNG QUAN HỆ SINH THÁI TRI THỨC ĐA MIỀN TẠI VIỆT NAM", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#ffffff')
    ax.text(0.50, 0.920, "Tích hợp Knowledge Graph (KG), Dense Vector RAG và Tác tử Thông minh Multi-Tool Reasoning Agent", 
            ha='center', va='center', fontsize=9.2, color='#94a3b8')
    
    # Box 1: Nguồn tri thức thô (Left) - Giãn cách rộng
    b1 = patches.FancyBboxPatch((0.05, 0.36), 0.21, 0.48, boxstyle="round,pad=0.02", 
                                facecolor='#f0f9ff', edgecolor='#0284c7', lw=1.6)
    ax.add_patch(b1)
    # Header badge
    ax.text(0.155, 0.81, "1. NGUỒN TRI THỨC THÔ\n(Raw Knowledge)", ha='center', va='center', 
            fontsize=9.0, fontweight='bold', color='#0369a1',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#e0f2fe', edgecolor='#0284c7', lw=1.0))
    b1_txt = (
        "• Văn bản Phi cấu trúc:\n"
        "  - Quyết định 5481/QĐ-BYT\n"
        "    (Phác đồ Đái tháo đường Típ 2)\n"
        "  - Báo cáo phân tích CTCK SSI\n"
        "  - Bản tin vĩ mô NHNN & Nghị định 24\n\n"
        "• Dữ liệu Bán cấu trúc:\n"
        "  - Chỉ số lâm sàng (HbA1c, Glucose)\n"
        "  - Lịch sử khớp lệnh cổ phiếu VN30\n"
        "  - Chuỗi giá vàng miếng SJC"
    )
    ax.text(0.065, 0.72, b1_txt, ha='left', va='top', fontsize=7.8, color='#0f172a', linespacing=1.35)
    
    # Box 2A: Knowledge Graph (Center Top)
    b2a = patches.FancyBboxPatch((0.33, 0.62), 0.28, 0.22, boxstyle="round,pad=0.02", 
                                 facecolor='#f0fdf4', edgecolor='#16a34a', lw=1.6)
    ax.add_patch(b2a)
    ax.text(0.47, 0.81, "2A. KNOWLEDGE GRAPH (Biểu tượng)", ha='center', va='center', 
            fontsize=8.8, fontweight='bold', color='#166534',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#dcfce7', edgecolor='#16a34a', lw=1.0))
    b2a_txt = (
        "• Mạng lưới Bộ ba: (Subject - Predicate - Object)\n"
        "• Ràng buộc: Metformin [Chống chỉ định] Rượu bia\n"
        "• Chuỗi giá trị: USD/VND tăng -> FPT hưởng lợi DT\n"
        "• Truy vấn: Graph Traversal n-bước (Multi-hop)"
    )
    ax.text(0.345, 0.74, b2a_txt, ha='left', va='top', fontsize=7.6, color='#0f172a', linespacing=1.3)
    
    # Box 2B: Vector RAG (Center Bottom) - Tách biệt rõ ràng với 2A (khoảng trống 0.08)
    b2b = patches.FancyBboxPatch((0.33, 0.36), 0.28, 0.22, boxstyle="round,pad=0.02", 
                                 facecolor='#fffbeb', edgecolor='#d97706', lw=1.6)
    ax.add_patch(b2b)
    ax.text(0.47, 0.55, "2B. DENSE VECTOR RAG (Ngữ nghĩa)", ha='center', va='center', 
            fontsize=8.8, fontweight='bold', color='#92400e',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#fef3c7', edgecolor='#d97706', lw=1.0))
    b2b_txt = (
        "• Phân đoạn văn bản ngữ nghĩa (Semantic Chunks)\n"
        "• Vector Embeddings đa chiều (PhoBERT / BGE)\n"
        "• Tái xếp hạng (Cross-Encoder Re-Ranking)\n"
        "• Trích xuất văn bản phác đồ & tin tức thẩm quyền"
    )
    ax.text(0.345, 0.48, b2b_txt, ha='left', va='top', fontsize=7.6, color='#0f172a', linespacing=1.3)
    
    # Box 3: Multi-Tool AI Agent (Right)
    b3 = patches.FancyBboxPatch((0.68, 0.36), 0.27, 0.48, boxstyle="round,pad=0.02", 
                                facecolor='#faf5ff', edgecolor='#7e22ce', lw=1.8)
    ax.add_patch(b3)
    ax.text(0.815, 0.81, "3. TÁC TỬ THÔNG MINH (AI Agent)\nReAct Reasoning & Execution", ha='center', va='center', 
            fontsize=8.8, fontweight='bold', color='#6b21a8',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#f3e8ff', edgecolor='#7e22ce', lw=1.0))
    b3_txt = (
        "• Mô hình Học sâu (Deep Learning Tools):\n"
        "  - MLP Classifier: Chẩn đoán Đái tháo đường\n"
        "  - PyTorch BiLSTM: Dự báo chuỗi giá VN30\n"
        "• Vòng lặp Suy luận ReAct Tự chủ:\n"
        "  - Thought: Phân tích ý định & lập kế hoạch\n"
        "  - Action: Điều phối Tool DL, Tool KG, Tool RAG\n"
        "  - Observation: Cập nhật nhận thức trung gian\n"
        "• Tổng hợp Minh bạch (Fact Grounded):\n"
        "  Khuyến nghị hành động chính xác, an toàn,\n"
        "  tuyệt đối không bị ảo giác tri thức"
    )
    ax.text(0.695, 0.72, b3_txt, ha='left', va='top', fontsize=7.8, color='#0f172a', linespacing=1.35)
    
    # Bottom Box: User Interaction - Giãn cách rộng với phần trên
    b_usr = patches.FancyBboxPatch((0.05, 0.06), 0.90, 0.22, boxstyle="round,pad=0.015", 
                                   facecolor='#f8fafc', edgecolor='#475569', lw=1.4)
    ax.add_patch(b_usr)
    ax.text(0.50, 0.245, "NGƯỜI DÙNG TƯƠNG TÁC THỜI GIAN THỰC (BỆNH NHÂN & NHÀ ĐẦU TƯ VIỆT NAM)", 
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#1e293b')
    
    usr_l = (
        "[KỊCH BẢN Y TẾ]:\n"
        "\"Tôi đang dùng Metformin, HbA1c 7.3%, chiều nay liên hoan có uống rượu và ăn thịt gà được không?\"\n"
        "-> Agent: Cảnh báo đỏ TUYỆT ĐỐI CẤM rượu (Toan Lactic tử vong); Khuyên ăn ức gà luộc, cấm gà rán dầu mỡ."
    )
    usr_r = (
        "[KỊCH BẢN TÀI CHÍNH]:\n"
        "\"Tỷ giá USD/VND vượt 25,450 và giá vàng SJC lên 90 triệu, cổ phiếu FPT và HPG sẽ chịu ảnh hưởng gì?\"\n"
        "-> Agent: BiLSTM dự báo FPT tăng 1.8% (hưởng lợi xuất khẩu IT); HPG bất lợi chi phí quặng; Vàng SJC thận trọng."
    )
    ax.text(0.07, 0.17, usr_l, ha='left', va='top', fontsize=7.8, color='#0f172a', linespacing=1.3)
    ax.text(0.53, 0.17, usr_r, ha='left', va='top', fontsize=7.8, color='#0f172a', linespacing=1.3)

    # Connector Arrows - Mũi tên thanh thoát, không chạm sát mép
    arr_b = dict(arrowstyle="-|>", lw=2.0, color='#0284c7', mutation_scale=14)
    ax.annotate("", xy=(0.32, 0.73), xytext=(0.27, 0.73), arrowprops=arr_b)
    ax.annotate("", xy=(0.32, 0.47), xytext=(0.27, 0.47), arrowprops=arr_b)
    
    arr_g = dict(arrowstyle="-|>", lw=2.0, color='#16a34a', mutation_scale=14)
    ax.annotate("", xy=(0.67, 0.73), xytext=(0.62, 0.73), arrowprops=arr_g)
    
    arr_a = dict(arrowstyle="-|>", lw=2.0, color='#d97706', mutation_scale=14)
    ax.annotate("", xy=(0.67, 0.47), xytext=(0.62, 0.47), arrowprops=arr_a)
    
    arr_u = dict(arrowstyle="<|-|>", lw=2.0, color='#6366f1', linestyle='--', mutation_scale=14)
    ax.annotate("", xy=(0.815, 0.35), xytext=(0.815, 0.29), arrowprops=arr_u)

    save_fig(fig, "fig701_kg_and_rag_overview.png")

# =============================================================================
# 2. FIG 702: CẤU TRÚC BỘ BA RDF & BẢNG ĐỐI SOÁNH GRAPH DB VS VECTOR DB
# =============================================================================
def generate_fig702():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.0, 7.2), dpi=300)
    
    # Subplot 1: Visual Knowledge Graph (Thông thoáng, uốn cong mềm mại)
    ax1.axis('off')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    
    h1 = patches.FancyBboxPatch((0.04, 0.91), 0.92, 0.07, boxstyle="round,pad=0.01",
                                facecolor='#1e293b', edgecolor='#334155', lw=1.2)
    ax1.add_patch(h1)
    ax1.text(0.50, 0.945, "MÔ HÌNH BỘ BA RDF & BẢN THỂ LUẬN (ONTOLOGY)\n(Subject - Predicate - Object Triples)", 
             ha='center', va='center', fontsize=9.8, fontweight='bold', color='#ffffff')
    
    # Nodes with ample spacing
    def draw_n(ax, x, y, w, h, t, s, bg, bd, tc):
        b = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015",
                                   facecolor=bg, edgecolor=bd, lw=1.5)
        ax.add_patch(b)
        ax.text(x + w/2, y + h*0.62, t, ha='center', va='center', fontsize=8.2, fontweight='bold', color=tc)
        ax.text(x + w/2, y + h*0.30, s, ha='center', va='center', fontsize=7.0, color='#475569')
        return (x + w/2, y + h/2)

    # Center Disease
    p_dis = draw_n(ax1, 0.36, 0.48, 0.28, 0.14, "Tiểu đường Type 2", "Mã bệnh ICD-10: E11", "#fee2e2", "#dc2626", "#991b1b")
    # Left Metrics
    p_hba1c = draw_n(ax1, 0.05, 0.68, 0.22, 0.13, "HbA1c ≥ 6.5%", "Chỉ số vàng BYT", "#fef3c7", "#d97706", "#92400e")
    p_glc = draw_n(ax1, 0.05, 0.28, 0.22, 0.13, "Glucose ≥ 126 mg/dL", "Đường huyết đói 8h", "#fef3c7", "#d97706", "#92400e")
    # Right Medication & Food
    p_met = draw_n(ax1, 0.73, 0.68, 0.22, 0.13, "Thuốc Metformin", "500mg (Biguanide)", "#e0e7ff", "#4338ca", "#3730a3")
    p_alc = draw_n(ax1, 0.73, 0.28, 0.22, 0.13, "Rượu Bia / Cồn", "Chất nguy cơ cao", "#ffe4e6", "#e11d48", "#be123c")
    p_food = draw_n(ax1, 0.36, 0.12, 0.28, 0.13, "Ức Gà Nạc Bỏ Da", "Đạm tốt (GI = 0)", "#dcfce7", "#16a34a", "#166534")

    # Connectors
    def add_e(ax, p1, p2, lbl, col='#475569', is_danger=False):
        lw = 2.0 if is_danger else 1.4
        ax.annotate("", xy=p2, xytext=p1, 
                    arrowprops=dict(arrowstyle="-|>", lw=lw, color=col, mutation_scale=12))
        mx, my = (p1[0] + p2[0])/2, (p1[1] + p2[1])/2
        bg = '#fee2e2' if is_danger else '#ffffff'
        bd = '#dc2626' if is_danger else '#cbd5e1'
        tc = '#dc2626' if is_danger else col
        ax.text(mx, my, lbl, ha='center', va='center', fontsize=6.8, fontweight='bold', color=tc,
                bbox=dict(boxstyle='round,pad=0.15', facecolor=bg, edgecolor=bd, lw=0.7))

    add_e(ax1, p_hba1c, p_dis, "CHẨN ĐOÁN", '#0284c7')
    add_e(ax1, p_glc, p_dis, "XÁC NHẬN", '#0284c7')
    add_e(ax1, p_dis, p_met, "ĐIỀU TRỊ ĐẦU TAY", '#4338ca')
    add_e(ax1, p_met, p_alc, "CHỐNG CHỈ ĐỊNH\n(Toan Lactic Tử Vong)", '#e11d48', is_danger=True)
    add_e(ax1, p_dis, p_food, "KHUYẾN NGHỊ DINH DƯỠNG", '#16a34a')

    # Subplot 2: Graphic Comparison Table
    ax2.axis('off')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    
    h2 = patches.FancyBboxPatch((0.04, 0.91), 0.92, 0.07, boxstyle="round,pad=0.01",
                                facecolor='#1e293b', edgecolor='#334155', lw=1.2)
    ax2.add_patch(h2)
    ax2.text(0.50, 0.945, "ĐỐI CHUẨN KỸ THUẬT: GRAPH DB VS. VECTOR DB", 
             ha='center', va='center', fontsize=9.8, fontweight='bold', color='#ffffff')
    
    rows = [
        ("Tiêu chí Đánh giá", "Vector DB (Milvus, FAISS)", "Graph DB (Neo4j, KG)", True),
        ("Cấu trúc dữ liệu", "Dense Vectors (768-1536 dims)", "Nodes, Edges & Properties", False),
        ("Bản chất tri thức", "Tương đồng thống kê mờ (Cosine)", "Logic biểu tượng xác định 100%", False),
        ("Cơ chế truy xuất", "K-láng giềng gần nhất (HNSW)", "Duyệt đồ thị đa bước (Multi-hop)", False),
        ("Khả năng suy luận", "Kém; không suy luận bắc cầu", "Xuất sắc; suy luận quan hệ sâu", False),
        ("Rủi ro ảo giác", "Dễ ảo giác khi đoạn văn rời rạc", "Triệt tiêu ảo giác qua neo giữ thực tế", False),
        ("Tính minh bạch", "Thấp; khoảng cách vector trừu tượng", "Minh bạch 100%; có đường đi chứng cứ", False),
        ("Ứng dụng tối ưu", "Tìm kiếm tài liệu ngữ nghĩa tự do", "Tương tác thuốc, chuỗi tài chính vĩ mô", False)
    ]
    
    y = 0.84
    for title, v_val, g_val, is_hdr in rows:
        h_row = 0.065
        bg_color = '#0284c7' if is_hdr else ('#f8fafc' if y % 0.13 > 0.06 else '#ffffff')
        t_color = '#ffffff' if is_hdr else '#0f172a'
        f_weight = 'bold' if is_hdr else 'normal'
        
        r_box = patches.Rectangle((0.04, y - h_row), 0.92, h_row, facecolor=bg_color, edgecolor='#cbd5e1', lw=0.8)
        ax2.add_patch(r_box)
        
        ax2.text(0.06, y - h_row/2, title, ha='left', va='center', fontsize=7.6, fontweight='bold', color=t_color)
        ax2.text(0.36, y - h_row/2, v_val, ha='left', va='center', fontsize=7.4, fontweight=f_weight, color=t_color)
        ax2.text(0.68, y - h_row/2, g_val, ha='left', va='center', fontsize=7.4, fontweight=f_weight, color=t_color)
        y -= h_row
        
    bot_c = patches.FancyBboxPatch((0.04, 0.12), 0.92, 0.14, boxstyle="round,pad=0.015",
                                  facecolor='#ecfdf5', edgecolor='#059669', lw=1.4)
    ax2.add_patch(bot_c)
    ax2.text(0.50, 0.20, "[KẾT LUẬN KIẾN TRÚC HIỆN ĐẠI: GRAPHRAG HỢP NHẤT]", ha='center', va='center', fontsize=8.6, fontweight='bold', color='#065f46')
    ax2.text(0.50, 0.155, "Vector DB tìm kiếm nhanh các điểm neo ban đầu -> Graph DB duyệt sâu n-bước trích xuất chuỗi nhân quả hoàn chỉnh.", 
             ha='center', va='center', fontsize=7.6, color='#047857')

    plt.tight_layout()
    save_fig(fig, "fig702_knowledge_graph_triples_ontology.png")

# =============================================================================
# 3. FIG 703: TIẾN HÓA KIẾN TRÚC RAG (GIÃN CÁCH 3 CỘT RỘNG RÃI)
# =============================================================================
def generate_fig703():
    fig, ax = plt.subplots(figsize=(15.0, 8.2), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # Header Banner
    h = patches.FancyBboxPatch((0.05, 0.91), 0.90, 0.07, boxstyle="round,pad=0.015",
                               facecolor='#0f172a', edgecolor='#334155', lw=1.2)
    ax.add_patch(h)
    ax.text(0.50, 0.952, "TIẾN HÓA CÁC THẾ HỆ RETRIEVAL-AUGMENTED GENERATION (RAG)", 
            ha='center', va='center', fontsize=12.2, fontweight='bold', color='#ffffff')
    ax.text(0.50, 0.925, "Lộ trình Phát triển Kỹ thuật: Naive RAG -> Advanced RAG -> GraphRAG (Microsoft Research 2024)", 
            ha='center', va='center', fontsize=9.0, color='#94a3b8')
    
    # 3 Cột rời nhau hoàn toàn, khoảng cách giữa các cột = 0.05
    cols = [
        {
            "x": 0.05, "w": 0.27, "title": "THẾ HỆ 1: NAIVE RAG", "sub": "(RAG Cổ Điển)",
            "theme": "#dc2626", "bg": "#fef2f2",
            "steps": [
                ("1. Chunking Cơ học", "Cắt văn bản cố định 512 tokens, dễ đứt gãy câu."),
                ("2. Dense Embedding", "Nhúng đoạn văn thành vector độc lập."),
                ("3. Vector DB Search", "Tính Cosine Top-k; dễ lẫn lộn khẳng định/phủ định."),
                ("4. Nhồi Prompt LLM", "Ghép Top-k chunks vào cửa sổ ngữ cảnh sinh văn bản.")
            ],
            "verdict": "[NHƯỢC ĐIỂM NGHIÊM TRỌNG]:\nMất mát ngữ cảnh, ảo giác khi câu hỏi phức tạp; bất lực trước câu hỏi tổng hợp toàn cục."
        },
        {
            "x": 0.365, "w": 0.27, "title": "THẾ HỆ 2: ADVANCED RAG", "sub": "(RAG Tối Ưu Đa Chặng)",
            "theme": "#2563eb", "bg": "#eff6ff",
            "steps": [
                ("1. Tiền truy xuất (Pre-Retrieval)", "Tối ưu câu hỏi: Query Expansion, Multi-Query, HyDE."),
                ("2. Hybrid Retrieval", "Kết hợp tìm kiếm từ khóa BM25 + Vector Dense."),
                ("3. Hậu truy xuất (Post-Retrieval)", "Tái xếp hạng bằng Cross-Encoder (Reranker) lọc nhiễu."),
                ("4. Nén Ngữ Cảnh (Compression)", "Trích lọc câu then chốt nhằm tối ưu hóa chi phí token.")
            ],
            "verdict": "[CẢI TIẾN ĐÁNG KỂ]:\nĐộ chính xác đoạn văn cao hơn, nhưng vẫn mù mờ về mối quan hệ giữa các thực thể."
        },
        {
            "x": 0.68, "w": 0.27, "title": "THẾ HỆ 3: GRAPHRAG", "sub": "(Đồ Thị Tri Thức + LLM)",
            "theme": "#16a34a", "bg": "#f0fdf4",
            "steps": [
                ("1. Trích xuất Đồ thị (Extraction)", "LLM trích xuất Thực thể, Quan hệ và Thuộc tính."),
                ("2. Phát hiện Cộng đồng (Leiden)", "Phân cụm đồ thị phân cấp, gom các thực thể liên quan."),
                ("3. Tóm tắt Cộng đồng (Summaries)", "LLM sinh báo cáo tóm tắt cho từng cụm tri thức đa cấp."),
                ("4. Dual-Search (Local + Global)", "Duyệt đường đi đồ thị (Local) + Tóm tắt toàn cục (Global).")
            ],
            "verdict": "[ĐỘT PHÁ TOÀN DIỆN]:\nTrả lời xuất sắc câu hỏi tổng hợp bao quát; suy luận bắc cầu minh bạch; có đường dẫn chứng cứ kiểm tra được!"
        }
    ]
    
    for c in cols:
        card = patches.FancyBboxPatch((c["x"], 0.05), c["w"], 0.82, boxstyle="round,pad=0.015",
                                      facecolor=c["bg"], edgecolor=c["theme"], lw=1.8)
        ax.add_patch(card)
        
        # Header Badge
        ax.text(c["x"] + c["w"]/2, 0.82, f"{c['title']}\n{c['sub']}", ha='center', va='center', 
                fontsize=8.8, fontweight='bold', color='#ffffff',
                bbox=dict(boxstyle='round,pad=0.25', facecolor=c["theme"], edgecolor=c["theme"], lw=1.0))
        
        # Steps
        y_s = 0.72
        for s_t, s_d in c["steps"]:
            s_box = patches.FancyBboxPatch((c["x"] + 0.015, y_s - 0.075), c["w"] - 0.03, 0.08, boxstyle="round,pad=0.01",
                                           facecolor='#ffffff', edgecolor='#cbd5e1', lw=0.9)
            ax.add_patch(s_box)
            ax.text(c["x"] + 0.025, y_s - 0.015, s_t, ha='left', va='center', fontsize=7.8, fontweight='bold', color=c["theme"])
            ax.text(c["x"] + 0.025, y_s - 0.048, s_d, ha='left', va='center', fontsize=7.0, color='#334155')
            y_s -= 0.11
            
        # Verdict Box
        v_box = patches.FancyBboxPatch((c["x"] + 0.015, 0.08), c["w"] - 0.03, 0.17, boxstyle="round,pad=0.01",
                                       facecolor='#ffffff', edgecolor=c["theme"], lw=1.2)
        ax.add_patch(v_box)
        ax.text(c["x"] + 0.025, 0.165, c["verdict"], ha='left', va='center', fontsize=7.3, color='#0f172a', linespacing=1.3)

    save_fig(fig, "fig703_rag_pipeline_and_graphrag.png")

# =============================================================================
# 4. FIG 704: KNOWLEDGE GRAPH BỆNH TIỂU ĐƯỜNG (MẠNG LƯỚI THÔNG THOÁNG)
# =============================================================================
def generate_fig704():
    fig, ax = plt.subplots(figsize=(15.0, 8.8), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # Header Banner
    h = patches.FancyBboxPatch((0.05, 0.91), 0.90, 0.07, boxstyle="round,pad=0.015",
                               facecolor='#0f172a', edgecolor='#334155', lw=1.2)
    ax.add_patch(h)
    ax.text(0.50, 0.952, "ĐỒ THỊ TRI THỨC Y TẾ (KNOWLEDGE GRAPH): QUẢN LÝ ĐÁI THÁO ĐƯỜNG TẠI VIỆT NAM", 
            ha='center', va='center', fontsize=12.2, fontweight='bold', color='#ffffff')
    ax.text(0.50, 0.925, "Phác đồ Bộ Y Tế (Quyết định 5481/QĐ-BYT), Cảnh báo Tương tác Thuốc Nguy hiểm & Dinh dưỡng", 
            ha='center', va='center', fontsize=9.0, color='#94a3b8')
            
    def draw_node(x, y, w, h, t, s, bg, bd, tc):
        b = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015",
                                   facecolor=bg, edgecolor=bd, lw=1.6)
        ax.add_patch(b)
        ax.text(x + w/2, y + h*0.62, t, ha='center', va='center', fontsize=8.2, fontweight='bold', color=tc)
        ax.text(x + w/2, y + h*0.30, s, ha='center', va='center', fontsize=7.0, color='#475569')
        return (x + w/2, y + h/2)

    # 4 Tầng không gian rõ ràng với khoảng trống rộng lớn:
    # Tầng 1: Bệnh nhân & Chỉ số lâm sàng (x = 0.05)
    p_pat = draw_node(0.05, 0.50, 0.16, 0.12, "Bệnh nhân Việt Nam", "Dữ liệu Cận lâm sàng", "#f0f9ff", "#0284c7", "#0369a1")
    p_hba1c = draw_node(0.05, 0.72, 0.16, 0.11, "HbA1c ≥ 6.5%", "Chỉ số vàng BYT", "#fef3c7", "#d97706", "#b45309")
    p_glc = draw_node(0.05, 0.30, 0.16, 0.11, "Glucose ≥ 126 mg/dL", "Đường huyết đói 8h", "#fef3c7", "#d97706", "#b45309")
    p_bmi = draw_node(0.05, 0.10, 0.16, 0.11, "BMI ≥ 25.0 kg/m²", "Thừa cân WPRO châu Á", "#fef3c7", "#d97706", "#b45309")
    
    # Tầng 2: Bệnh lý (x = 0.30)
    p_dis = draw_node(0.30, 0.46, 0.20, 0.18, "ĐÁI THÁO ĐƯỜNG TYPE 2", "Mã ICD-10: E11\n(90-95% số ca bệnh)", "#fee2e2", "#dc2626", "#991b1b")
    
    # Tầng 3: Dược phẩm (x = 0.58)
    p_met = draw_node(0.58, 0.65, 0.17, 0.12, "Thuốc Metformin", "500mg (Biguanide)\nChỉ định Đầu tay", "#e0e7ff", "#4338ca", "#3730a3")
    p_gli = draw_node(0.58, 0.44, 0.17, 0.12, "Thuốc Gliclazide", "30mg (Sulfonylurea)\nPhối hợp Bậc 2", "#e0e7ff", "#4338ca", "#3730a3")
    p_ins = draw_node(0.58, 0.23, 0.17, 0.12, "Insulin Ngoại sinh", "Chỉ định khi thất bại\nthuốc uống", "#e0e7ff", "#4338ca", "#3730a3")
    
    # Tầng 4: Thực phẩm & Chất nguy cơ (x = 0.81)
    p_alc = draw_node(0.81, 0.65, 0.15, 0.14, "RƯỢU BIA / CỒN", "Thói quen liên hoan\nnam giới Việt Nam", "#ffe4e6", "#e11d48", "#9f1239")
    p_chk_s = draw_node(0.81, 0.44, 0.15, 0.12, "Ức Gà Nạc Bỏ Da", "Đạm trắng an toàn\nGI = 0, Lipid < 3%", "#dcfce7", "#16a34a", "#166534")
    p_chk_r = draw_node(0.81, 0.26, 0.15, 0.12, "Thịt Gà Chiên Dầu", "Nhiều mỡ & trans-fat\nTăng đề kháng Insulin", "#ffedd5", "#ea580c", "#9a3412")
    p_rice = draw_node(0.81, 0.08, 0.15, 0.12, "Cơm Trắng Gạo Tẻ", "GI = 73 (Cần hạn chế,\năn kèm rau xanh)", "#fef9c3", "#ca8a04", "#854d0e")

    # Mũi tên uốn lượn có khoảng cách, nhãn rõ ràng
    def add_e(p1, p2, lbl, col='#475569', is_danger=False):
        lw = 2.2 if is_danger else 1.4
        ax.annotate("", xy=p2, xytext=p1, 
                    arrowprops=dict(arrowstyle="-|>", lw=lw, color=col, mutation_scale=12))
        mx, my = (p1[0] + p2[0])/2, (p1[1] + p2[1])/2
        bg = '#fee2e2' if is_danger else '#ffffff'
        bd = '#dc2626' if is_danger else '#cbd5e1'
        tc = '#dc2626' if is_danger else col
        ax.text(mx, my, lbl, ha='center', va='center', fontsize=6.6, fontweight='bold', color=tc,
                bbox=dict(boxstyle='round,pad=0.15', facecolor=bg, edgecolor=bd, lw=0.7))

    add_e(p_pat, p_hba1c, "Đo lường", '#0284c7')
    add_e(p_pat, p_glc, "Đo lường", '#0284c7')
    add_e(p_pat, p_bmi, "Đo lường", '#0284c7')
    add_e(p_hba1c, p_dis, "Chẩn đoán vàng", '#d97706')
    add_e(p_glc, p_dis, "Xác nhận bệnh", '#d97706')
    add_e(p_bmi, p_dis, "Nguy cơ cao", '#d97706')
    
    add_e(p_dis, p_met, "Chỉ định đầu tay", '#4338ca')
    add_e(p_dis, p_gli, "Phối hợp bậc 2", '#4338ca')
    add_e(p_dis, p_ins, "Khi suy kiệt tụy", '#4338ca')
    
    add_e(p_met, p_alc, "CHỐNG CHỈ ĐỊNH ĐỎ\n(Nguy cơ Toan Lactic tử vong!)", '#e11d48', is_danger=True)
    add_e(p_dis, p_chk_s, "Khuyến nghị ưu tiên", '#16a34a')
    add_e(p_dis, p_chk_r, "Cảnh báo hạn chế", '#ea580c')
    add_e(p_dis, p_rice, "Kiểm soát lượng", '#ca8a04')

    save_fig(fig, "fig704_diabetes_vietnam_knowledge_graph.png")

# =============================================================================
# 5. FIG 705: KNOWLEDGE GRAPH TÀI CHÍNH VN30 & VÀNG SJC (3 TẦNG THOÁNG ĐÃNG)
# =============================================================================
def generate_fig705():
    fig, ax = plt.subplots(figsize=(15.0, 8.8), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # Header Banner
    h = patches.FancyBboxPatch((0.05, 0.91), 0.90, 0.07, boxstyle="round,pad=0.015",
                               facecolor='#0f172a', edgecolor='#334155', lw=1.2)
    ax.add_patch(h)
    ax.text(0.50, 0.952, "ĐỒ THỊ TRI THỨC TÀI CHÍNH VIỆT NAM (VN30 STOCKS & SJC GOLD KNOWLEDGE GRAPH)", 
            ha='center', va='center', fontsize=12.2, fontweight='bold', color='#ffffff')
    ax.text(0.50, 0.925, "Mô hình hóa Chuỗi Tác động Lan truyền giữa Biến số Vĩ mô, Nghị định 24, Vàng SJC và VN30", 
            ha='center', va='center', fontsize=9.0, color='#94a3b8')
            
    def draw_node(x, y, w, h, t, s, bg, bd, tc):
        b = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015",
                                   facecolor=bg, edgecolor=bd, lw=1.6)
        ax.add_patch(b)
        ax.text(x + w/2, y + h*0.62, t, ha='center', va='center', fontsize=8.2, fontweight='bold', color=tc)
        ax.text(x + w/2, y + h*0.30, s, ha='center', va='center', fontsize=7.0, color='#475569')
        return (x + w/2, y + h/2)

    # 3 Tầng không gian phân chia rõ ràng:
    # Tầng 1: Vĩ mô & Pháp lý (Top, y = 0.70)
    p_usd = draw_node(0.06, 0.70, 0.18, 0.14, "TỶ GIÁ USD/VND", "Biến số Vĩ mô Sống còn\n(Độ mở kinh tế 200%)", "#fef3c7", "#d97706", "#92400e")
    p_rate = draw_node(0.29, 0.70, 0.18, 0.14, "LÃI SUẤT NHNN", "Lãi suất Tái cấp vốn & OMO\n(Điều tiết thanh khoản)", "#fef3c7", "#d97706", "#92400e")
    p_xau = draw_node(0.53, 0.70, 0.18, 0.14, "GIÁ VÀNG THẾ GIỚI", "Hợp đồng XAU/USD\n(USD/Ounce giao ngay)", "#fef9c3", "#ca8a04", "#854d0e")
    p_nd24 = draw_node(0.76, 0.70, 0.18, 0.14, "NGHỊ ĐỊNH 24/2012", "Độc quyền dập vàng miếng\n(Siết chặt cung vàng SJC)", "#fee2e2", "#dc2626", "#991b1b")
    
    # Tầng 2: Tài sản Tài chính (Middle, y = 0.40) - Cách tầng 1 tới 0.30!
    p_fpt = draw_node(0.06, 0.40, 0.18, 0.15, "CỔ PHIẾU FPT (VN30)", "Công nghệ thông tin\nXuất khẩu IT Mỹ/Nhật", "#e0f2fe", "#0284c7", "#0369a1")
    p_vcb = draw_node(0.29, 0.40, 0.18, 0.15, "CỔ PHIẾU VCB (VN30)", "Ngân hàng Ngoại thương\nĐầu tàu thanh khoản tín dụng", "#dcfce7", "#16a34a", "#166534")
    p_hpg = draw_node(0.53, 0.40, 0.18, 0.15, "CỔ PHIẾU HPG (VN30)", "Tập đoàn Hòa Phát\nSản xuất Thép & Công nghiệp", "#ffe4e6", "#e11d48", "#9f1239")
    p_sjc = draw_node(0.76, 0.40, 0.18, 0.15, "VÀNG MIẾNG SJC 999.9", "Tài sản Phòng thủ\nChênh lệch cao so với TG", "#fef08a", "#eab308", "#a16207")
    
    # Tầng 3: Cơ chế kinh tế (Bottom, y = 0.10) - Cách tầng 2 tới 0.30!
    p_fpt_i = draw_node(0.06, 0.10, 0.18, 0.15, "MỞ RỘNG BIÊN LÃI", "Doanh thu USD chiếm ~50%\nChi phí trả bằng VND", "#f0fdf4", "#16a34a", "#15803d")
    p_vcb_i = draw_node(0.29, 0.10, 0.18, 0.15, "BIÊN LÃI THUẦN (NIM)", "Lãi suất tác động tới\nhuy động & cho vay", "#f8fafc", "#475569", "#334155")
    p_hpg_i = draw_node(0.53, 0.10, 0.18, 0.15, "ĐỘI CHI PHÍ NHẬP", "Nhập quặng sắt/than USD;\nLỗ chênh lệch tỷ giá nợ vay", "#fff1f2", "#be123c", "#881337")
    p_sjc_i = draw_node(0.76, 0.10, 0.18, 0.15, "CHÊNH LỆCH CUNG CẦU", "Lệch 5-18 triệu đ/lượng;\nRủi ro khi NHNN can thiệp", "#fffbeb", "#d97706", "#b45309")

    # Connectors
    def add_e(p1, p2, lbl, col='#475569'):
        ax.annotate("", xy=p2, xytext=p1, 
                    arrowprops=dict(arrowstyle="-|>", lw=1.6, color=col, mutation_scale=12))
        mx, my = (p1[0] + p2[0])/2, (p1[1] + p2[1])/2
        ax.text(mx, my, lbl, ha='center', va='center', fontsize=6.6, fontweight='bold', color=col,
                bbox=dict(boxstyle='round,pad=0.15', facecolor='#ffffff', edgecolor='#cbd5e1', lw=0.7))

    add_e(p_usd, p_fpt, "HƯỞNG LỢI NGOẠI TỆ", '#16a34a')
    add_e(p_usd, p_hpg, "BẤT LỢI CHI PHÍ VỐN", '#e11d48')
    add_e(p_usd, p_sjc, "TĂNG GIÁ GỐC NHẬP", '#d97706')
    add_e(p_rate, p_vcb, "ĐIỀU TIẾT THANH KHOẢN", '#0284c7')
    add_e(p_xau, p_sjc, "DẪN DẮT XU HƯỚNG", '#ca8a04')
    add_e(p_nd24, p_sjc, "ĐỘC QUYỀN NGUỒN CUNG", '#dc2626')
    
    add_e(p_fpt, p_fpt_i, "Tác động Doanh thu", '#16a34a')
    add_e(p_vcb, p_vcb_i, "Tác động NIM", '#0284c7')
    add_e(p_hpg, p_hpg_i, "Tác động Giá vốn", '#e11d48')
    add_e(p_sjc, p_sjc_i, "Hệ quả Thị trường", '#d97706')

    save_fig(fig, "fig705_financial_stock_gold_knowledge_graph.png")

# =============================================================================
# 6. FIG 706: QUY TRÌNH ĐIỀU PHỐI REACT AI AGENT (THIẾT KẾ MỚI: THOÁNG ĐÃNG)
# =============================================================================
def generate_fig706():
    fig, ax = plt.subplots(figsize=(15.5, 8.5), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # 1. Header Banner - Độc lập, khoảng đệm an toàn lớn
    h = patches.FancyBboxPatch((0.05, 0.91), 0.90, 0.07, boxstyle="round,pad=0.015",
                               facecolor='#0f172a', edgecolor='#334155', lw=1.2)
    ax.add_patch(h)
    ax.text(0.50, 0.952, "KIẾN TRÚC ĐIỀU PHỐI ĐA CÔNG CỤ CỦA TÁC TỬ THÔNG MINH (AI AGENT)", 
            ha='center', va='center', fontsize=12.2, fontweight='bold', color='#ffffff')
    ax.text(0.50, 0.925, "Quy trình Suy luận Chuẩn ReAct: Thought -> Action Selection -> Observation -> Synthesis", 
            ha='center', va='center', fontsize=9.0, color='#94a3b8')
            
    # 4 GIAI ĐOẠN RỜI NHAU HOÀN TOÀN, CÓ KHOẢNG TRỐNG RỘNG LỚN (BREATHING ROOM)
    
    # GIAI ĐOẠN 1: USER INPUT (x = 0.05, width = 0.18, y = 0.25, height = 0.58)
    b1 = patches.FancyBboxPatch((0.05, 0.25), 0.18, 0.58, boxstyle="round,pad=0.02",
                                facecolor='#f0f9ff', edgecolor='#0284c7', lw=1.6)
    ax.add_patch(b1)
    ax.text(0.14, 0.79, "BƯỚC 1: TIẾP NHẬN\n(User Request / Context)", ha='center', va='center', 
            fontsize=8.6, fontweight='bold', color='#0369a1',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#e0f2fe', edgecolor='#0284c7', lw=1.0))
    b1_txt = (
        "• Dữ liệu Y tế:\n"
        "  - HbA1c: 7.3%\n"
        "  - Glucose đói: 138 mg/dL\n"
        "  - BMI: 26.5 kg/m²\n"
        "  - Đang uống: Metformin 500mg\n\n"
        "• Câu hỏi Y tế:\n"
        "  \"Chiều nay liên hoan,\n"
        "  tôi uống rượu và ăn\n"
        "  thịt gà được không?\"\n\n"
        "• Câu hỏi Tài chính:\n"
        "  \"Tỷ giá USD tăng mạnh,\n"
        "  FPT và Vàng SJC ra sao?\""
    )
    ax.text(0.065, 0.71, b1_txt, ha='left', va='top', fontsize=7.6, color='#0f172a', linespacing=1.3)
    
    # GIAI ĐOẠN 2: BỘ NÃO AGENT REACT (x = 0.29, width = 0.20, y = 0.22, height = 0.64)
    # Khoảng trống giữa B1 và B2 là 0.06!
    b2 = patches.FancyBboxPatch((0.29, 0.22), 0.20, 0.64, boxstyle="round,pad=0.02",
                                facecolor='#faf5ff', edgecolor='#7e22ce', lw=1.8)
    ax.add_patch(b2)
    ax.text(0.39, 0.81, "BƯỚC 2: BỘ NÃO AGENT\n(ReAct Reasoning Planner)", ha='center', va='center', 
            fontsize=8.6, fontweight='bold', color='#6b21a8',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#f3e8ff', edgecolor='#7e22ce', lw=1.0))
    b2_txt = (
        "• [THOUGHT - SUY LUẬN]:\n"
        "  1. Phân tích ý định & triệu chứng\n"
        "  2. Nhận diện các thực thể quan trọng\n"
        "  3. Lập kế hoạch gọi công cụ\n"
        "     theo trình tự logic tối ưu\n\n"
        "• [ACTION DISPATCHER]:\n"
        "  - Điều phối Tool 1 (Học sâu)\n"
        "  - Điều phối Tool 2 (Đồ thị KG)\n"
        "  - Điều phối Tool 3 (Truy xuất RAG)\n\n"
        "• [MEMORY BUFFER]:\n"
        "  Lưu vết lịch sử hội thoại\n\n"
        "• [SAFETY GUARDRAILS]:\n"
        "  Kiểm duyệt quy tắc an toàn y tế"
    )
    ax.text(0.305, 0.73, b2_txt, ha='left', va='top', fontsize=7.6, color='#0f172a', linespacing=1.3)
    
    # GIAI ĐOẠN 3: DANH MỤC 3 CÔNG CỤ (x = 0.55, width = 0.21)
    # Khoảng trống giữa B2 và B3 là 0.06! Các Tool tách rời nhau, cách nhau 0.04!
    
    # Tool 1: Deep Learning (Top)
    t1 = patches.FancyBboxPatch((0.55, 0.64), 0.21, 0.22, boxstyle="round,pad=0.015",
                                facecolor='#fef2f2', edgecolor='#ef4444', lw=1.5)
    ax.add_patch(t1)
    ax.text(0.655, 0.82, "TOOL 1: DEEP LEARNING MODEL", ha='center', va='center', 
            fontsize=8.0, fontweight='bold', color='#b91c1c',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#fee2e2', edgecolor='#ef4444', lw=0.8))
    t1_txt = "• Medical MLP Classifier v2:\n  Chẩn đoán Tiểu đường: 98.5%\n• PyTorch BiLSTM Timeseries:\n  FPT: +1.8% | SJC: 89.8-91.5 tr"
    ax.text(0.565, 0.76, t1_txt, ha='left', va='top', fontsize=7.4, color='#0f172a', linespacing=1.25)
    
    # Tool 2: Knowledge Graph (Middle) - Cách Tool 1 là 0.04!
    t2 = patches.FancyBboxPatch((0.55, 0.38), 0.21, 0.22, boxstyle="round,pad=0.015",
                                facecolor='#f0fdf4', edgecolor='#16a34a', lw=1.5)
    ax.add_patch(t2)
    ax.text(0.655, 0.56, "TOOL 2: KNOWLEDGE GRAPH QUERY", ha='center', va='center', 
            fontsize=8.0, fontweight='bold', color='#166534',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#dcfce7', edgecolor='#16a34a', lw=0.8))
    t2_txt = "• Metformin -> Rượu bia:\n  CHỐNG CHỈ ĐỊNH TOAN LACTIC\n• Tiểu đường -> Ức gà nạc: An toàn\n• USD/VND -> FPT: Hưởng lợi DT"
    ax.text(0.565, 0.50, t2_txt, ha='left', va='top', fontsize=7.4, color='#0f172a', linespacing=1.25)
    
    # Tool 3: Dense RAG (Bottom) - Cách Tool 2 là 0.04!
    t3 = patches.FancyBboxPatch((0.55, 0.12), 0.21, 0.22, boxstyle="round,pad=0.015",
                                facecolor='#fffbeb', edgecolor='#d97706', lw=1.5)
    ax.add_patch(t3)
    ax.text(0.655, 0.30, "TOOL 3: DENSE RAG RETRIEVER", ha='center', va='center', 
            fontsize=8.0, fontweight='bold', color='#92400e',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='#fef3c7', edgecolor='#d97706', lw=0.8))
    t3_txt = "• Quyết định 5481/QĐ-BYT (Phác đồ)\n• Tháp Dinh dưỡng Viện DDQG\n• Báo cáo CTCK SSI: Xuất khẩu IT\n• Bản tin điều hành chính sách NHNN"
    ax.text(0.565, 0.24, t3_txt, ha='left', va='top', fontsize=7.4, color='#0f172a', linespacing=1.25)
    
    # GIAI ĐOẠN 4: FINAL SYNTHESIS & OUTPUT (x = 0.81, width = 0.15, y = 0.25, height = 0.58)
    # Khoảng trống giữa B3 và B4 là 0.05!
    b4 = patches.FancyBboxPatch((0.81, 0.25), 0.15, 0.58, boxstyle="round,pad=0.02",
                                facecolor='#ecfdf5', edgecolor='#059669', lw=1.8)
    ax.add_patch(b4)
    ax.text(0.885, 0.79, "BƯỚC 4: KẾT QUẢ\n(Final Synthesis)", ha='center', va='center', 
            fontsize=8.6, fontweight='bold', color='#065f46',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#d1fae5', edgecolor='#059669', lw=1.0))
    b4_txt = (
        "• Phản hồi Chuẩn:\n"
        "  1. Chẩn đoán Số học\n"
        "  2. Cảnh báo Logic KG\n"
        "  3. Dẫn chứng RAG\n"
        "  4. Khuyến nghị Rõ\n\n"
        "• Cam kết Vững chắc:\n"
        "  + Không ảo giác tri thức\n"
        "  + Minh bạch nguồn gốc\n"
        "  + Chuẩn y tế Bộ Y Tế\n"
        "  + Khách quan thị trường"
    )
    ax.text(0.825, 0.71, b4_txt, ha='left', va='top', fontsize=7.5, color='#0f172a', linespacing=1.3)

    # ĐƯỜNG NỐI VÀ MŨI TÊN THOÁNG ĐÃNG (Độ dài mũi tên 0.04-0.05, không bị dí sát viền)
    # 1 -> 2
    ax.annotate("", xy=(0.285, 0.54), xytext=(0.235, 0.54), 
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color='#0284c7', mutation_scale=14))
    ax.text(0.26, 0.565, "Gửi Input", ha='center', va='center', fontsize=6.8, fontweight='bold', color='#0284c7')
    
    # 2 -> Tools
    arr_p = dict(arrowstyle="-|>", lw=1.8, color='#7e22ce', mutation_scale=12)
    ax.annotate("", xy=(0.545, 0.75), xytext=(0.495, 0.65), arrowprops=arr_p)
    ax.annotate("", xy=(0.545, 0.49), xytext=(0.495, 0.54), arrowprops=arr_p)
    ax.annotate("", xy=(0.545, 0.23), xytext=(0.495, 0.43), arrowprops=arr_p)
    ax.text(0.52, 0.63, "Gọi Tools", ha='center', va='center', fontsize=6.8, fontweight='bold', color='#7e22ce')
    
    # Tools -> 4
    arr_g = dict(arrowstyle="-|>", lw=1.8, color='#059669', mutation_scale=12)
    ax.annotate("", xy=(0.805, 0.62), xytext=(0.765, 0.75), arrowprops=arr_g)
    ax.annotate("", xy=(0.805, 0.54), xytext=(0.765, 0.49), arrowprops=arr_g)
    ax.annotate("", xy=(0.805, 0.46), xytext=(0.765, 0.23), arrowprops=arr_g)
    ax.text(0.785, 0.57, "Tổng hợp", ha='center', va='center', fontsize=6.8, fontweight='bold', color='#059669')

    save_fig(fig, "fig706_agent_architecture_flow.png")

# =============================================================================
# 7. FIG 707: GIAO DIỆN WEB APP DASHBOARD CỦA AI AGENT (UI MOCKUP)
# =============================================================================
def generate_fig707():
    fig, ax = plt.subplots(figsize=(15.0, 8.8), dpi=300)
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # Outer Browser Window Frame
    win = patches.FancyBboxPatch((0.04, 0.04), 0.92, 0.92, boxstyle="round,pad=0.015",
                                facecolor='#0f172a', edgecolor='#334155', lw=1.8)
    ax.add_patch(win)
    
    # Browser Title Bar
    title_bar = patches.Rectangle((0.04, 0.90), 0.92, 0.06, facecolor='#1e293b')
    ax.add_patch(title_bar)
    for i, c in enumerate(['#ef4444', '#f59e0b', '#10b981']):
        btn = patches.Circle((0.06 + i*0.015, 0.93), 0.005, facecolor=c)
        ax.add_patch(btn)
        
    url_box = patches.FancyBboxPatch((0.18, 0.91), 0.65, 0.04, boxstyle="round,pad=0.008",
                                     facecolor='#0f172a', edgecolor='#475569', lw=0.9)
    ax.add_patch(url_box)
    ax.text(0.50, 0.93, "https://ai-agent.ptit.edu.vn/vietnam-copilot (Streamlit Web App)", 
            ha='center', va='center', fontsize=8.2, color='#94a3b8')

    # App Navigation Header
    nav_bar = patches.Rectangle((0.04, 0.83), 0.92, 0.07, facecolor='#0284c7')
    ax.add_patch(nav_bar)
    ax.text(0.07, 0.865, "VIETNAM AI AGENT COPILOT", ha='left', va='center', fontsize=11.0, fontweight='bold', color='#ffffff')
    ax.text(0.38, 0.865, "Trợ Lý Thông Minh Đa Miền: Y Tế Đái Tháo Đường & Tài Chính VN30 / Vàng SJC", ha='left', va='center', fontsize=8.4, color='#e0f2fe')
    ax.text(0.93, 0.865, "PTIT • B23DCCN879", ha='right', va='center', fontsize=8.8, fontweight='bold', color='#ffffff')

    # Panel Left: Healthcare Dashboard (x = 0.06, width = 0.42)
    p_left = patches.FancyBboxPatch((0.06, 0.07), 0.42, 0.73, boxstyle="round,pad=0.015",
                                    facecolor='#1e293b', edgecolor='#0284c7', lw=1.6)
    ax.add_patch(p_left)
    ax.text(0.27, 0.77, "PHÂN HỆ 1: TRỢ LÝ Y TẾ ĐÁI THÁO ĐƯỜNG", ha='center', va='center', 
            fontsize=9.0, fontweight='bold', color='#ffffff',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#0369a1', edgecolor='#0284c7', lw=1.0))
    
    # Left Metrics Cards
    metrics_l = [("HbA1c", "7.3%", "Ngưỡng ≥ 6.5%", "#dc2626"), 
                 ("Glucose Đói", "138 mg/dL", "Ngưỡng ≥ 126", "#ea580c"), 
                 ("Chỉ số BMI", "26.5 kg/m²", "Thừa cân WPRO", "#d97706")]
    for idx, (m_lbl, m_val, m_sub, m_col) in enumerate(metrics_l):
        mc = patches.FancyBboxPatch((0.075 + idx*0.13, 0.67), 0.12, 0.075, boxstyle="round,pad=0.008",
                                    facecolor='#0f172a', edgecolor=m_col, lw=1.1)
        ax.add_patch(mc)
        ax.text(0.135 + idx*0.13, 0.725, m_lbl, ha='center', va='center', fontsize=7.0, color='#94a3b8')
        ax.text(0.135 + idx*0.13, 0.70, m_val, ha='center', va='center', fontsize=9.0, fontweight='bold', color=m_col)
        ax.text(0.135 + idx*0.13, 0.68, m_sub, ha='center', va='center', fontsize=6.0, color='#64748b')

    q_box = patches.FancyBboxPatch((0.075, 0.57), 0.39, 0.08, boxstyle="round,pad=0.008",
                                   facecolor='#334155', edgecolor='#475569', lw=0.9)
    ax.add_patch(q_box)
    ax.text(0.09, 0.625, "[Bệnh nhân hỏi]:", fontsize=7.6, fontweight='bold', color='#38bdf8')
    ax.text(0.09, 0.595, "\"Tôi đang uống Metformin 500mg, chiều nay liên hoan có uống rượu và ăn thịt gà được không?\"", fontsize=7.2, color='#f8fafc')

    steps_txt = (
        "[REASONING TRACE - SUY LUẬN REACT]:\n"
        "  • Tool Deep Learning: Xác suất Đái tháo đường Type 2 = 98.5% (DƯƠNG TÍNH).\n"
        "  • Tool Knowledge Graph: Phát hiện liên kết Metformin -> Rượu bia\n"
        "    -> CẢNH BÁO ĐỎ: TĂNG NGUY CƠ NHIỄM TOAN LACTIC & HẠ ĐƯỜNG HUYẾT TỬ VONG!\n"
        "    -> Khuyến nghị Dinh dưỡng: Ức gà nạc bỏ da an toàn (GI=0); cấm gà rán dầu mỡ.\n"
        "  • Tool Dense RAG: Trích xuất Điều 4.2 Quyết định 5481/QĐ-BYT.\n\n"
        "[FINAL ANSWER - KHUYẾN NGHỊ CỦA AGENT]:\n"
        "  1. TUYỆT ĐỐI KHÔNG UỐNG RƯỢU BIA: Tương tác nguy hiểm tính mạng với Metformin!\n"
        "  2. ĐƯỢC ĂN THỊT GÀ: Ưu tiên chọn ức gà luộc/hấp bỏ da, kiêng da và gà rán chiên dầu.\n"
        "  3. GIỚI HẠN CƠM TRẮNG: Tối đa 1 bát/bữa, bổ sung nhiều rau muống / bông cải xanh."
    )
    ans_box = patches.FancyBboxPatch((0.075, 0.09), 0.39, 0.46, boxstyle="round,pad=0.01",
                                    facecolor='#0f172a', edgecolor='#10b981', lw=1.3)
    ax.add_patch(ans_box)
    ax.text(0.09, 0.52, steps_txt, ha='left', va='top', fontsize=6.9, color='#f1f5f9', linespacing=1.3)

    # Panel Right: Finance Dashboard (x = 0.52, width = 0.42) - Khoảng trống giữa 2 panel là 0.04!
    p_right = patches.FancyBboxPatch((0.52, 0.07), 0.42, 0.73, boxstyle="round,pad=0.015",
                                     facecolor='#1e293b', edgecolor='#f59e0b', lw=1.6)
    ax.add_patch(p_right)
    ax.text(0.73, 0.77, "PHÂN HỆ 2: TRỢ LÝ ĐẦU TƯ VN30 & VÀNG SJC", ha='center', va='center', 
            fontsize=9.0, fontweight='bold', color='#ffffff',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#b45309', edgecolor='#f59e0b', lw=1.0))
    
    # Right Metrics Cards
    metrics_r = [("Tỷ giá USD/VND", "25,450", "+1.2% YTD", "#10b981"), 
                 ("Vàng SJC", "90.5 tr/lượng", "Lệch TG +8.2 tr", "#eab308"), 
                 ("Mục tiêu FPT", "64.5k VNĐ", "BiLSTM +1.8%", "#38bdf8")]
    for idx, (m_lbl, m_val, m_sub, m_col) in enumerate(metrics_r):
        mc = patches.FancyBboxPatch((0.535 + idx*0.13, 0.67), 0.12, 0.075, boxstyle="round,pad=0.008",
                                    facecolor='#0f172a', edgecolor=m_col, lw=1.1)
        ax.add_patch(mc)
        ax.text(0.595 + idx*0.13, 0.725, m_lbl, ha='center', va='center', fontsize=7.0, color='#94a3b8')
        ax.text(0.595 + idx*0.13, 0.70, m_val, ha='center', va='center', fontsize=9.0, fontweight='bold', color=m_col)
        ax.text(0.595 + idx*0.13, 0.68, m_sub, ha='center', va='center', fontsize=6.0, color='#64748b')

    q_box_r = patches.FancyBboxPatch((0.535, 0.57), 0.39, 0.08, boxstyle="round,pad=0.008",
                                     facecolor='#334155', edgecolor='#475569', lw=0.9)
    ax.add_patch(q_box_r)
    ax.text(0.55, 0.625, "[Nhà đầu tư hỏi]:", fontsize=7.6, fontweight='bold', color='#fbbf24')
    ax.text(0.55, 0.595, "\"Tỷ giá USD/VND tăng mạnh và vàng SJC lên 90 triệu, cổ phiếu FPT & HPG ảnh hưởng gì?\"", fontsize=7.2, color='#f8fafc')

    steps_txt_r = (
        "[REASONING TRACE - SUY LUẬN REACT]:\n"
        "  • Tool BiLSTM Model: Dự báo FPT phiên t+1 đạt 64.5k (+1.8%, xu thế tăng);\n"
        "    Dự báo vàng SJC biên độ 89.8 - 91.5 triệu đồng/lượng.\n"
        "  • Tool Knowledge Graph: Phân tích chuỗi giá trị vĩ mô:\n"
        "    -> FPT: Hưởng lợi tỷ giá (Doanh thu USD chiếm gần 50%, chi phí trả bằng VND).\n"
        "    -> HPG: Bất lợi tỷ giá (Nhập khẩu quặng sắt & than mỡ bằng USD, lỗ tỷ giá nợ).\n"
        "    -> Vàng SJC: Nghị định 24 độc quyền tạo chênh lệch cung cầu lớn với thế giới.\n"
        "  • Tool Dense RAG: Trích dẫn Báo cáo Chiến lược CTCK SSI & Thông điệp NHNN.\n\n"
        "[FINAL ANSWER - KHUYẾN NGHỊ CỦA AGENT]:\n"
        "  1. CỔ PHIẾU FPT: TÍCH CỰC - Tiếp tục nắm giữ, hưởng lợi kép tỷ giá & AI export.\n"
        "  2. CỔ PHIẾU HPG: TRUNG LẬP - Theo dõi áp lực chi phí nguyên liệu đầu vào USD.\n"
        "  3. VÀNG SJC: THẬN TRỌNG TÍCH TRỮ - Chênh lệch giá thế giới cao, chờ đấu thầu NHNN."
    )
    ans_box_r = patches.FancyBboxPatch((0.535, 0.09), 0.39, 0.46, boxstyle="round,pad=0.01",
                                      facecolor='#0f172a', edgecolor='#f59e0b', lw=1.3)
    ax.add_patch(ans_box_r)
    ax.text(0.55, 0.52, steps_txt_r, ha='left', va='top', fontsize=6.9, color='#f1f5f9', linespacing=1.3)

    save_fig(fig, "fig707_agent_webapp_interface.png")

if __name__ == '__main__':
    print("Bắt đầu sinh 7 hình ảnh mới thoáng đãng, giãn cách rộng rãi, chuyên nghiệp...")
    generate_fig701()
    generate_fig702()
    generate_fig703()
    generate_fig704()
    generate_fig705()
    generate_fig706()
    generate_fig707()
    print("✓ Đã sinh đầy đủ 7 hình ảnh mới đạt chuẩn mỹ thuật cao cấp!")
