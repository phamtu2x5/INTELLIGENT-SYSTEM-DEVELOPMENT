import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

os.makedirs('Report/tieuluan01_CT_02_tupv/images', exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# =========================================================================
# FIGURE 1.3: TAXONOMY OF AI, ML, DL, GENAI (CLEAN STACK OF TIERS)
# =========================================================================
fig, ax = plt.subplots(figsize=(15, 10.5), dpi=300)
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#ffffff')

# 4 Tier Cards stacked vertically with hierarchy connectors
tiers = [
    ("TẦNG 1: TRÍ TUỆ NHÂN TẠO (ARTIFICIAL INTELLIGENCE - 1950s)",
     "Phạm vi bao trùm toàn bộ: Khái niệm rộng lớn nhất nhằm xây dựng các hệ thống mô phỏng trí tuệ con người.",
     "• Phương pháp suy diễn: Logic hình thức (First-Order Logic), Hệ chuyên gia (Rule-based Expert Systems), Tìm kiếm Heuristic (A*, Minimax).\n• Đặc điểm: Dựa trên tri thức tiền nghiệm (hard-coded rules), không có khả năng tự trích xuất đặc trưng từ dữ liệu thô.",
     "#1e3a8a", "#eff6ff", 0.76),

    ("TẦNG 2: HỌC MÁY (MACHINE LEARNING - 1980s)",
     "Tập con của AI: Cho phép hệ thống tự động học quy luật thống kê từ tập dữ liệu quan sát mà không cần lập trình cứng quy tắc.",
     "• Thuật toán tiêu biểu: Hồi quy tuyến tính/Logistic, Cây quyết định (Decision Tree), Rừng ngẫu nhiên (Random Forest), SVM, K-Means, PCA.\n• Đặc điểm: Phụ thuộc lớn vào kỹ nghệ đặc trưng thủ công (Feature Engineering), hiệu năng phụ thuộc chất lượng trích xuất đặc trưng.",
     "#047857", "#ecfdf5", 0.52),

    ("TẦNG 3: HỌC SÂU (DEEP LEARNING - 2010s)",
     "Tập con của ML: Sử dụng mạng nơ-ron sâu nhiều tầng để tự động học biểu diễn đặc trưng phân cấp từ dữ liệu thô.",
     "• Kiến trúc tiêu biểu: Mạng truyền thẳng đa tầng (MLP), Mạng tích chập (CNN: ResNet, VGG, MobileNet), Mạng hồi quy (RNN, LSTM, GRU).\n• Đặc điểm: Tự động học đặc trưng từ mức thấp (cạnh, vân bề mặt) đến mức ngữ nghĩa cao (bộ phận, vật thể); yêu cầu dữ liệu lớn & GPU.",
     "#b45309", "#fffbeb", 0.28),

    ("TẦNG 4: AI TẠO SINH & HỆ ĐA AGENT (GENERATIVE AI & AGENTIC AI - 2020s)",
     "Đỉnh cao hiện đại của AI & DL: Mô hình hóa phân bố xác suất sinh dữ liệu mới và phối hợp các tác tử thông minh tự chủ.",
     "• Công nghệ tiêu biểu: Mô hình ngôn ngữ lớn (LLMs: GPT-4, Llama, Gemini), Diffusion Models, RAG (Retrieval-Augmented Gen), Hệ Đa Agent.\n• Đặc điểm: Khả năng khái quát hóa cực cao qua vài ví dụ (Few-shot learning), suy luận đa bước, lập kế hoạch và phối hợp tác tử giải quyết vấn đề.",
     "#6d28d9", "#faf5ff", 0.04)
]

for title, sub, bullets, border_c, bg_c, y_pos in tiers:
    card_h = 0.20
    p = patches.FancyBboxPatch((0.05, y_pos), 0.90, card_h,
                               boxstyle=patches.BoxStyle("Round", pad=0.015, rounding_size=0.02),
                               facecolor=bg_c, edgecolor=border_c, lw=2.2, zorder=2)
    ax.add_patch(p)
    
    # Title
    ax.text(0.08, y_pos + card_h - 0.04, title, fontsize=12.5, fontweight='bold', color=border_c, zorder=3)
    # Subtitle
    ax.text(0.08, y_pos + card_h - 0.075, sub, fontsize=10, fontstyle='italic', color='#334155', zorder=3)
    # Bullets
    ax.text(0.08, y_pos + card_h - 0.115, bullets, fontsize=9.2, color='#1e293b', va='top', zorder=3, linespacing=1.45)
    
    # Hierarchy connector arrow pointing DOWNwards to next sub-tier
    if y_pos > 0.10:
        ax.annotate("", xy=(0.50, y_pos - 0.038), xytext=(0.50, y_pos - 0.002),
                    arrowprops=dict(arrowstyle="->,head_width=0.45,head_length=0.6", color='#64748b', lw=2.5, ls=':'), zorder=4)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
plt.tight_layout()
fig.savefig('Report/tieuluan01_CT_02_tupv/images/fig103_ai_ml_dl_taxonomy.png', bbox_inches='tight')
plt.close(fig)
print("✓ Đã vẽ lại fig103: Mũi tên phân cấp hướng xuống chuẩn xác!")
