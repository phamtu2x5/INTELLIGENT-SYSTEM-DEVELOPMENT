import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import textwrap
import os

os.makedirs('Report/tieuluan01_CT_02_tupv/images', exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# =========================================================================
# 1. FIGURE 1.1: REDESIGNED TIMELINE (BALANCED, WELL-FILLED CARDS, READABLE TEXT)
# =========================================================================
def create_figure_1_1():
    fig, ax = plt.subplots(figsize=(22, 10.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    # Title Banner with generous breathing room
    ax.text(0.5, 0.968, "TIẾN TRÌNH LỊCH SỬ PHÁT TRIỂN TRÍ TUỆ NHÂN TẠO (1950 – 2026)",
            fontsize=21, fontweight='bold', color='#0f172a', ha='center', va='top')
    ax.text(0.5, 0.930, "Các bước ngoặt lý thuyết cốt lõi, thăng trầm lịch sử và các cuộc cách mạng mô hình tính toán",
            fontsize=13, fontstyle='italic', color='#475569', ha='center', va='top')

    # Row 1: 1950 to 1986 (7 milestones, Left to Right)
    row1_items = [
        {"year": "1950", "title": "Phép Thử Turing", "author": "Alan Turing",
         "desc": "Đặt câu hỏi lịch sử: 'Máy tính có thể tư duy không?' Thiết lập bài thử nghiệm Turing Test nền tảng.",
         "theme": "#2563eb", "bg": "#eff6ff"},
        {"year": "1956", "title": "Hội Thảo Dartmouth", "author": "J. McCarthy, M. Minsky",
         "desc": "Chính thức khai sinh thuật ngữ Artificial Intelligence. Mở ra kỷ nguyên AI Logic biểu tượng.",
         "theme": "#0284c7", "bg": "#f0f9ff"},
        {"year": "1958", "title": "Mạng Perceptron", "author": "Frank Rosenblatt",
         "desc": "Mô hình mạng nơ-ron học trọng số đầu tiên. Đặt cơ sở cho học có giám sát từ dữ liệu mẫu.",
         "theme": "#0d9488", "bg": "#f0fdfa"},
        {"year": "1969", "title": "Giới Hạn XOR", "author": "Minsky & Papert",
         "desc": "Sách Perceptrons chứng minh không giải được hàm phi tuyến XOR. Đình trệ nghiên cứu mạng nơ-ron.",
         "theme": "#e11d48", "bg": "#fff1f2"},
        {"year": "1973", "title": "Mùa Đông AI Lần 1", "author": "Báo cáo Lighthill",
         "desc": "Chính phủ Anh & DARPA cắt giảm mạnh ngân sách trước vấn đề bùng nổ tổ hợp thuật toán.",
         "theme": "#dc2626", "bg": "#fef2f2"},
        {"year": "1980", "title": "Hệ Chuyên Gia", "author": "Hệ thống XCON / R1",
         "desc": "Kỷ nguyên thương mại hóa luật tri thức chuyên gia. Gặt hái thành công lớn trong công nghiệp.",
         "theme": "#16a34a", "bg": "#f0fdf4"},
        {"year": "1986", "title": "Lan Truyền Ngược", "author": "Rumelhart & Hinton",
         "desc": "Phổ biến giải thuật Backpropagation cho mạng nhiều tầng, giải quyết dứt điểm bài toán XOR.",
         "theme": "#059669", "bg": "#ecfdf5"}
    ]

    # Row 2: 1987 to 2026 (7 milestones, Left to Right)
    row2_items = [
        {"year": "1987", "title": "Mùa Đông AI Lần 2", "author": "Khủng hoảng Lisp",
         "desc": "Sụp đổ thị trường Lisp Machine, luật tri thức khó bảo trì. Nguồn tài trợ bị đóng băng diện rộng.",
         "theme": "#b91c1c", "bg": "#fef2f2"},
        {"year": "1995", "title": "Học Máy Thống Kê", "author": "V. Vapnik, C. Cortes",
         "desc": "Thời kỳ hoàng kim của SVM, Random Forest, AdaBoost dựa trên nền tảng toán học tối ưu lồi chặt chẽ.",
         "theme": "#4f46e5", "bg": "#eef2ff"},
        {"year": "1998", "title": "Mạng LeNet-5", "author": "Yann LeCun et al.",
         "desc": "Mạng nơ-ron tích chập (CNN) thương mại đầu tiên, ứng dụng nhận diện chữ số séc ngân hàng.",
         "theme": "#7c3aed", "bg": "#f5f3ff"},
        {"year": "2012", "title": "AlexNet & ImageNet", "author": "Krizhevsky & Hinton",
         "desc": "Khai phá kỷ nguyên Học sâu (Deep Learning) nhờ điện toán GPU song song, ReLU và Dropout.",
         "theme": "#d97706", "bg": "#fffbeb"},
        {"year": "2017", "title": "Transformer", "author": "Vaswani et al. (Google)",
         "desc": "Cơ chế Self-Attention thay thế hoàn toàn mạng hồi quy tuần tự, mở đường cho kỷ nguyên mô hình lớn.",
         "theme": "#ea580c", "bg": "#fff7ed"},
        {"year": "2022", "title": "ChatGPT & GenAI", "author": "OpenAI / Google",
         "desc": "Mô hình ngôn ngữ lớn (LLMs), AI Tạo sinh bùng nổ với khả năng suy luận ngữ cảnh vượt bậc.",
         "theme": "#9333ea", "bg": "#faf5ff"},
        {"year": "2024–2026", "title": "Agentic AI & Graph", "author": "Hệ Đa Tác Tử",
         "desc": "Tác tử tự trị (Agents), Knowledge Graph và RAG phối hợp suy luận đa bước giải bài toán phức hợp.",
         "theme": "#0f172a", "bg": "#f8fafc"}
    ]

    card_w = 0.120
    card_h = 0.285
    spacing = 0.138
    x_start = (1.0 - (6 * spacing + card_w)) / 2  # 0.026

    # Row 1 coordinates:
    card_top1 = 0.875
    cy1 = card_top1 - card_h  # 0.590
    bar_y1 = 0.550

    # Draw Timeline Guide Bar for Row 1
    ax.add_patch(patches.Rectangle((0.02, bar_y1), 0.96, 0.006, facecolor='#cbd5e1', zorder=1))
    
    # Draw Row 1 Cards
    for i, item in enumerate(row1_items):
        cx = x_start + i * spacing
        
        # Main Card Box
        box = patches.FancyBboxPatch((cx, cy1), card_w, card_h,
                                     boxstyle=patches.BoxStyle("Round", pad=0.007, rounding_size=0.014),
                                     facecolor=item['bg'], edgecolor=item['theme'], lw=2.2, zorder=2)
        ax.add_patch(box)
        
        # Header Badge for Year
        badge_h = 0.052
        badge = patches.FancyBboxPatch((cx, cy1 + card_h - badge_h), card_w, badge_h,
                                       boxstyle=patches.BoxStyle("Round", pad=0.004, rounding_size=0.010),
                                       facecolor=item['theme'], edgecolor='none', zorder=3)
        ax.add_patch(badge)
        ax.text(cx + card_w / 2, cy1 + card_h - badge_h / 2, item['year'],
                fontsize=13.5, fontweight='bold', color='#ffffff', ha='center', va='center', zorder=4)
        
        # Card Content - well distributed vertically
        ax.text(cx + card_w / 2, cy1 + card_h - badge_h - 0.024, item['title'],
                fontsize=11.5, fontweight='bold', color=item['theme'], ha='center', va='top', zorder=4)
        ax.text(cx + card_w / 2, cy1 + card_h - badge_h - 0.062, f"({item['author']})",
                fontsize=9.6, fontstyle='italic', color='#475569', ha='center', va='top', zorder=4)
        
        wrapped_desc = textwrap.fill(item['desc'], width=19)
        ax.text(cx + card_w / 2, cy1 + card_h - badge_h - 0.098, wrapped_desc,
                fontsize=9.0, color='#1e293b', ha='center', va='top', zorder=4, linespacing=1.32)

        # Connector to guide bar
        ax.plot([cx + card_w / 2, cx + card_w / 2], [cy1, bar_y1], color=item['theme'], lw=2.0, ls='--', zorder=1)
        ax.scatter([cx + card_w / 2], [bar_y1 + 0.003], color=item['theme'], s=45, zorder=5)

    # Middle transition zone:
    bar_y2 = 0.450
    mid_y = (bar_y1 + bar_y2) / 2  # 0.500

    # Connecting Arrow from Row 1 end to Row 2 start
    ax.annotate("", xy=(0.032, bar_y2), xytext=(0.968, bar_y1),
                arrowprops=dict(arrowstyle="->,head_width=0.55,head_length=0.75",
                                color="#64748b", lw=2.6, connectionstyle="arc3,rad=-0.14"), zorder=2)
    ax.text(0.50, mid_y, "Tiến trình chuyển dịch sang Kỷ nguyên Hiện đại (1987 – 2026) ➔",
            fontsize=12, fontweight='bold', fontstyle='italic', color='#334155', ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.4", fc="#f8fafc", ec="#94a3b8", lw=1.5), zorder=3)

    # Draw Timeline Guide Bar for Row 2
    ax.add_patch(patches.Rectangle((0.02, bar_y2), 0.96, 0.006, facecolor='#cbd5e1', zorder=1))

    # Row 2 coordinates:
    card_top2 = bar_y2 - 0.040  # 0.410
    cy2 = card_top2 - card_h    # 0.125

    # Draw Row 2 Cards
    for i, item in enumerate(row2_items):
        cx = x_start + i * spacing
        
        # Main Card Box
        box = patches.FancyBboxPatch((cx, cy2), card_w, card_h,
                                     boxstyle=patches.BoxStyle("Round", pad=0.007, rounding_size=0.014),
                                     facecolor=item['bg'], edgecolor=item['theme'], lw=2.2, zorder=2)
        ax.add_patch(box)
        
        # Header Badge for Year
        badge_h = 0.052
        badge = patches.FancyBboxPatch((cx, cy2 + card_h - badge_h), card_w, badge_h,
                                       boxstyle=patches.BoxStyle("Round", pad=0.004, rounding_size=0.010),
                                       facecolor=item['theme'], edgecolor='none', zorder=3)
        ax.add_patch(badge)
        ax.text(cx + card_w / 2, cy2 + card_h - badge_h / 2, item['year'],
                fontsize=13.0, fontweight='bold', color='#ffffff', ha='center', va='center', zorder=4)
        
        # Card Content - well distributed vertically
        ax.text(cx + card_w / 2, cy2 + card_h - badge_h - 0.024, item['title'],
                fontsize=11.5, fontweight='bold', color=item['theme'], ha='center', va='top', zorder=4)
        ax.text(cx + card_w / 2, cy2 + card_h - badge_h - 0.062, f"({item['author']})",
                fontsize=9.6, fontstyle='italic', color='#475569', ha='center', va='top', zorder=4)
        
        wrapped_desc = textwrap.fill(item['desc'], width=19)
        ax.text(cx + card_w / 2, cy2 + card_h - badge_h - 0.098, wrapped_desc,
                fontsize=9.0, color='#1e293b', ha='center', va='top', zorder=4, linespacing=1.32)

        # Connector to guide bar
        ax.plot([cx + card_w / 2, cx + card_w / 2], [card_top2, bar_y2], color=item['theme'], lw=2.0, ls='--', zorder=1)
        ax.scatter([cx + card_w / 2], [bar_y2 + 0.003], color=item['theme'], s=45, zorder=5)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    fig.savefig('Report/tieuluan01_CT_02_tupv/images/fig101_ai_evolution_timeline.png', bbox_inches='tight')
    plt.close(fig)
    print("✓ Đã vẽ lại fig101: Tỉ lệ thẻ hoàn hảo, nội dung phân bố đều, không khoảng trống thừa!")

# =========================================================================
# 2. FIGURE 1.2: REDESIGNED AI WINTERS AND HYPE CYCLES (CLEAR LABELS)
# =========================================================================
def create_figure_1_2():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8fafc')

    # Years from 1950 to 2026
    x = np.linspace(1950, 2026, 600)

    # Smooth multi-peak curve
    def hype_func(t):
        peak1 = 85 * np.exp(-((t - 1965)**2) / (2 * 4.5**2))
        winter1 = -40 * np.exp(-((t - 1976)**2) / (2 * 2.5**2))
        peak2 = 105 * np.exp(-((t - 1984)**2) / (2 * 3.5**2))
        winter2 = -55 * np.exp(-((t - 1990)**2) / (2 * 2.8**2))
        recovery = 65 / (1 + np.exp(-(t - 1998) / 3.5))
        boom_dl = 120 / (1 + np.exp(-(t - 2012) / 2.5))
        boom_genai = 95 / (1 + np.exp(-(t - 2022) / 1.5))
        base = 25
        return base + peak1 + winter1 + peak2 + winter2 + recovery + boom_dl + boom_genai

    y = hype_func(x)
    y_clamped = np.clip(y, 10, 310)

    # Grid
    ax.grid(True, linestyle='--', alpha=0.5, color='#94a3b8')

    # Winter 1 Shaded Area (1973.5 - 1980.5)
    ax.axvspan(1973.5, 1980.5, color='#fee2e2', alpha=0.85, zorder=1)
    ax.axvline(1973.5, color='#ef4444', linestyle='--', lw=2, zorder=2)
    ax.axvline(1980.5, color='#ef4444', linestyle='--', lw=2, zorder=2)

    # Winter 2 Shaded Area (1987.0 - 1993.5)
    ax.axvspan(1987.0, 1993.5, color='#fee2e2', alpha=0.85, zorder=1)
    ax.axvline(1987.0, color='#ef4444', linestyle='--', lw=2, zorder=2)
    ax.axvline(1993.5, color='#ef4444', linestyle='--', lw=2, zorder=2)

    # Fill under curve
    ax.fill_between(x, y_clamped, 0, color='#3b82f6', alpha=0.10, zorder=2)
    # Plot curve
    ax.plot(x, y_clamped, color='#1d4ed8', lw=4.0, zorder=3)

    # Labels for AI Winter 1 (Compact Box centered on 1975)
    w1_text = (
        "MÙA ĐÔNG AI I (1974 – 1980)\n"
        "• Báo cáo Lighthill (1973)\n"
        "• Giới hạn toán học XOR\n"
        "• DARPA cắt giảm tài trợ\n"
        "• Bế tắc bùng nổ tổ hợp"
    )
    ax.text(1975.2, 265, w1_text, fontsize=9.8, fontweight='bold', color='#991b1b',
            ha='center', va='top', bbox=dict(boxstyle="round,pad=0.5", fc="#ffffff", ec="#ef4444", lw=2.2), zorder=5)

    # Labels for AI Winter 2 (Compact Box centered on 1992)
    w2_text = (
        "MÙA ĐÔNG AI II (1987 – 1993)\n"
        "• Khủng hoảng Lisp Machine\n"
        "• Điểm nghẽn bảo trì tri thức\n"
        "• Chi phí chuyên gia đắt đỏ\n"
        "• Kỳ vọng thương mại đổ vỡ"
    )
    ax.text(1992.5, 265, w2_text, fontsize=9.8, fontweight='bold', color='#991b1b',
            ha='center', va='top', bbox=dict(boxstyle="round,pad=0.5", fc="#ffffff", ec="#ef4444", lw=2.2), zorder=5)

    # Annotate Peaks
    # Peak 1: 1965
    ax.annotate("KỲ VỌNG BAN ĐẦU (1956–1968)\n(Logic hình thức & Perceptron)",
                xy=(1965, 110), xytext=(1958, 175),
                arrowprops=dict(arrowstyle="->", color='#0369a1', lw=2.0),
                fontsize=10.0, fontweight='bold', color='#0369a1', ha='center',
                bbox=dict(boxstyle="round,pad=0.4", fc="#f0f9ff", ec="#0284c7", lw=1.8), zorder=5)

    # Peak 2: 1984 - right in the middle between the two winter boxes
    ax.annotate("KỶ NGUYÊN HỆ CHUYÊN GIA (1980–1987)\n(Thương mại hóa XCON & Expert Systems)",
                xy=(1984, 128), xytext=(1984, 185),
                arrowprops=dict(arrowstyle="->", color='#15803d', lw=2.0),
                fontsize=9.8, fontweight='bold', color='#15803d', ha='center',
                bbox=dict(boxstyle="round,pad=0.4", fc="#f0fdf4", ec="#16a34a", lw=1.8), zorder=5)

    # Peak 3: 2005
    ax.annotate("HỌC MÁY THỰC CHỨNG (1995–2010)\n(SVM, Random Forest, AdaBoost)",
                xy=(2004, 90), xytext=(2002, 140),
                arrowprops=dict(arrowstyle="->", color='#4338ca', lw=2.0),
                fontsize=10.0, fontweight='bold', color='#4338ca', ha='center',
                bbox=dict(boxstyle="round,pad=0.4", fc="#eef2ff", ec="#4f46e5", lw=1.8), zorder=5)

    # Peak 4: 2017
    ax.annotate("BÙNG NỔ HỌC SÂU (2012–2020)\n(AlexNet, CNN, RNN, GPU, Big Data)",
                xy=(2017, 210), xytext=(2011, 270),
                arrowprops=dict(arrowstyle="->", color='#b45309', lw=2.0),
                fontsize=10.5, fontweight='bold', color='#b45309', ha='center',
                bbox=dict(boxstyle="round,pad=0.4", fc="#fffbeb", ec="#d97706", lw=1.8), zorder=5)

    # Peak 5: 2024
    ax.annotate("KỶ NGUYÊN GENAI & AGENT (2020–2026)\n(LLMs, Transformer, Hệ Đa Tác Tử)",
                xy=(2025, 305), xytext=(2021, 335),
                arrowprops=dict(arrowstyle="->", color='#7e22ce', lw=2.0),
                fontsize=10.8, fontweight='bold', color='#7e22ce', ha='right',
                bbox=dict(boxstyle="round,pad=0.4", fc="#faf5ff", ec="#9333ea", lw=2.0), zorder=5)

    ax.set_xlim(1948, 2028)
    ax.set_ylim(0, 360)
    ax.set_xlabel("Trục Thời Gian (Năm)", fontsize=13.0, fontweight='bold', labelpad=10, color='#0f172a')
    ax.set_ylabel("Chỉ Số Kỳ Vọng / Ngân Sách Đầu Tư / Ứng Dụng Thực Tiễn", fontsize=12.5, fontweight='bold', labelpad=10, color='#0f172a')
    ax.set_title("CHU KỲ KỲ VỌNG VÀ HAI THỜI KỲ “MÙA ĐÔNG AI” (AI WINTERS) TRONG LỊCH SỬ 75 NĂM",
                 fontsize=15.0, fontweight='bold', pad=15, color='#0f172a')

    plt.tight_layout()
    fig.savefig('Report/tieuluan01_CT_02_tupv/images/fig102_ai_winters_and_hype_cycles.png', bbox_inches='tight')
    plt.close(fig)
    print("✓ Đã vẽ lại fig102 không còn chồng lấn hộp chữ!")

if __name__ == '__main__':
    create_figure_1_1()
    create_figure_1_2()
