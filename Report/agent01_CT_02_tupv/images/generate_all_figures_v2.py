import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import os
import subprocess

# Global font setup
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

# =========================================================================
# 1. FIG 1: AI AGENT COGNITIVE ARCHITECTURE (FIX ALL OVERLAPS)
# =========================================================================
def make_ai_agent_architecture_fixed(out_path):
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Main Diagram Title
    ax.text(50, 96, "KIẾN TRÚC NHẬN THỨC CỦA HỆ TÁC TỬ THÔNG MINH (AI AGENT COGNITIVE ARCHITECTURE)", 
            fontsize=11.5, fontweight='bold', color='#0f172a', ha='center')

    # Environment Banner (Top)
    ax.add_patch(patches.FancyBboxPatch((8, 80), 84, 11, boxstyle="round,pad=0.4",
                                        facecolor='#f0f9ff', edgecolor='#0284c7', linewidth=1.5))
    ax.text(50, 86.5, "MÔI TRƯỜNG DOANH NGHIỆP BÊN NGOÀI (ENTERPRISE ENVIRONMENT)", 
            fontsize=9.5, fontweight='bold', color='#0369a1', ha='center')
    ax.text(50, 82.5, "Người dùng (User Goal) • Cơ sở dữ liệu • Hệ thống API • Mạng Web • Phần mềm ERP/CRM", 
            fontsize=8.5, color='#0284c7', ha='center')

    # Downward & Upward Arrows
    ax.annotate("", xy=(25, 71), xytext=(25, 80),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=2))
    ax.text(26, 75.5, "Sensors / Perception\n(Tiếp nhận Goal)", fontsize=7.8, color="#0369a1", va='center')

    ax.annotate("", xy=(75, 80), xytext=(75, 71),
                arrowprops=dict(arrowstyle="->", color="#16a34a", lw=2))
    ax.text(76, 75.5, "Actuators / Actions\n(Thực thi Công cụ)", fontsize=7.8, color="#15803d", va='center')

    # Big Agent Core Box
    ax.add_patch(patches.FancyBboxPatch((6, 7), 88, 64, boxstyle="round,pad=0.6",
                                        facecolor='#f8fafc', edgecolor='#475569', linewidth=2.0))
    ax.text(50, 67, "LÕI SUY LUẬN TỰ TRỊ CỦA TÁC TỬ (AGENT CORE - POWERED BY FOUNDATION LLM)", 
            fontsize=10.5, fontweight='bold', color='#0f172a', ha='center')

    # 3 Distinct Component Cards (No overlapping!)
    cards = [
        # (x, title, color_header, color_body, border_color, bullet_lines)
        (9, "1. PLANNING & REASONING", "#d97706", "#fffbeb", "#f59e0b", 
         ["• Phân rã mục tiêu (Goal Decomposition)", 
          "• Lập kế hoạch đa bước (Sub-goals)", 
          "• Cơ chế ReAct (Thought-Action)", 
          "• Cơ chế ReWOO (Kế hoạch trước)"]),
        (37, "2. MEMORY MANAGEMENT", "#4f46e5", "#eef2ff", "#6366f1",
         ["• Ngữ cảnh ngắn hạn (Context Prompt)", 
          "• Bộ nhớ dài hạn (Vector DB / RAG)", 
          "• Đồ thị tri thức (Knowledge Graph)", 
          "• Theo dõi trạng thái (State Trace)"]),
        (65, "3. TOOL USE & EXECUTION", "#16a34a", "#f0fdf4", "#22c55e",
         ["• Gọi hàm ngoại vi (Function Calling)", 
          "• Truy vấn CSDL nội bộ (SQL/API)", 
          "• Thực thi code an toàn (Calculator)", 
          "• Thu nhận & phân tích kết quả (Observation)"])
    ]

    for x, header, col_head, col_body, col_border, bullets in cards:
        # Card Body
        ax.add_patch(patches.FancyBboxPatch((x, 26), 26, 36, boxstyle="round,pad=0.3",
                                            facecolor=col_body, edgecolor=col_border, linewidth=1.5))
        # Card Header Banner
        ax.add_patch(patches.FancyBboxPatch((x, 56.5), 26, 5.5, boxstyle="round,pad=0.2",
                                            facecolor=col_head, edgecolor='none'))
        ax.text(x + 13, 59.2, header, fontsize=8.2, fontweight='bold', color='#ffffff', ha='center', va='center')
        
        # Bullet Points
        by = 52.0
        for b in bullets:
            ax.text(x + 1.8, by, b, fontsize=7.5, color='#1e293b', va='center')
            by -= 6.5

    # Interaction Arrows between the 3 modules
    ax.annotate("", xy=(36.5, 44), xytext=(35.2, 44),
                arrowprops=dict(arrowstyle="<->", color="#64748b", lw=2))
    ax.annotate("", xy=(64.5, 44), xytext=(63.2, 44),
                arrowprops=dict(arrowstyle="<->", color="#64748b", lw=2))

    # Bottom Safety & Guardrails Banner
    ax.add_patch(patches.FancyBboxPatch((9, 10.5), 82, 12, boxstyle="round,pad=0.4",
                                        facecolor='#fef2f2', edgecolor='#ef4444', linewidth=1.5))
    ax.text(50, 18.5, "QUẢN TRỊ AN TOÀN, PHẢN HỒI VÀ KIỂM TOÁN (IBM & MCKINSEY BEST PRACTICES)", 
            fontsize=8.8, fontweight='bold', color='#991b1b', ha='center')
    ax.text(50, 14.0, "Tự phản chiếu (Self-reflection) • Can thiệp người dùng (HITL) • Nhật ký kiểm toán (Audit Trail) • Rào chắn Max Iterations", 
            fontsize=7.8, color='#7f1d1d', ha='center')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Hoàn thành sửa lỗi kiến trúc: {out_path}")

# =========================================================================
# 2. FIG 2: REACT VS REWOO REASONING PARADIGMS
# =========================================================================
def make_react_vs_rewoo_fixed(out_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.0), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    for ax in [ax1, ax2]:
        ax.set_facecolor('#ffffff')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')

    # Subplot 1: ReAct
    ax1.text(50, 96, "Mô hình ReAct (Reasoning + Acting)", fontsize=10.5, fontweight='bold', color='#1e3a8a', ha='center')
    ax1.text(50, 91.5, "[Vòng lặp suy nghĩ và hành động từng bước liên tục]", fontsize=8.2, color='#3b82f6', ha='center')

    react_nodes = [
        ("1. User Goal (Mục tiêu người dùng)", "#f1f5f9", "#475569", 83),
        ("2. THOUGHT: Suy luận trạng thái & bước đi", "#dbeafe", "#1d4ed8", 68),
        ("3. ACTION: Chọn công cụ & sinh tham số", "#f3e8ff", "#7e22ce", 53),
        ("4. OBSERVATION: Thu nhận kết quả từ Tools", "#dcfce7", "#15803d", 38),
        ("5. THOUGHT TIẾP THEO (Đánh giá dữ liệu)", "#dbeafe", "#1d4ed8", 23),
        ("6. FINAL ANSWER: Xuất kết quả hoàn tất", "#fee2e2", "#b91c1c", 8),
    ]

    for title, bg, border, y in react_nodes:
        ax1.add_patch(patches.FancyBboxPatch((8, y-4), 74, 8, boxstyle="round,pad=0.3",
                                             facecolor=bg, edgecolor=border, linewidth=1.2))
        ax1.text(45, y, title, fontsize=7.8, fontweight='bold', color=border, ha='center', va='center')

    for y_top, y_bot in [(79, 72), (64, 57), (49, 42), (34, 27), (19, 12)]:
        ax1.annotate("", xy=(45, y_bot), xytext=(45, y_top),
                     arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.5))

    # Elegant curved loopback arrow on right side
    ax1.annotate("", xy=(82, 68), xytext=(82, 38),
                 arrowprops=dict(arrowstyle="->", color="#ea580c", lw=2, connectionstyle="arc3,rad=-0.45"))
    ax1.text(93, 53, "Vòng lặp\nReAct\n(N bước)", fontsize=7.5, fontweight='bold', color="#c2410c", ha='center', va='center')

    # Subplot 2: ReWOO
    ax2.text(50, 96, "Mô hình ReWOO (Reasoning Without Observation)", fontsize=10.5, fontweight='bold', color='#065f46', ha='center')
    ax2.text(50, 91.5, "[Lập toàn bộ kế hoạch trước, thực thi công cụ song song]", fontsize=8.2, color='#059669', ha='center')

    rewoo_nodes = [
        ("1. User Goal (Mục tiêu người dùng)", "#f1f5f9", "#475569", 83, 8),
        ("2. PLANNER (LLM): Lập toàn bộ chuỗi kế hoạch gọi Tools\n[Plan 1: Tool A → Plan 2: Tool B → Plan 3: Tool C]", "#fef3c7", "#d97706", 66, 11),
        ("3. WORKER: Thực thi hàng loạt công cụ ngoại vi\n(Gọi song song các API/CSDL, tiết kiệm độ trễ tối đa)", "#dcfce7", "#16a34a", 46, 11),
        ("4. SOLVER (LLM): Đọc toàn bộ kết quả để tổng hợp\n(Chỉ 2 lần gọi LLM: lúc lập kế hoạch và lúc kết luận)", "#e0e7ff", "#4338ca", 26, 11),
        ("5. FINAL ANSWER: Kết quả tối ưu chi phí & Token", "#fee2e2", "#b91c1c", 8, 8),
    ]

    for title, bg, border, y, h in rewoo_nodes:
        ax2.add_patch(patches.FancyBboxPatch((8, y-h/2), 84, h, boxstyle="round,pad=0.3",
                                             facecolor=bg, edgecolor=border, linewidth=1.2))
        ax2.text(50, y, title, fontsize=7.8, fontweight='bold', color=border, ha='center', va='center')

    for y_top, y_bot in [(79, 71.5), (60.5, 51.5), (40.5, 31.5), (20.5, 12)]:
        ax2.annotate("", xy=(50, y_bot), xytext=(50, y_top),
                     arrowprops=dict(arrowstyle="->", color="#059669", lw=1.8))

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Hoàn thành ReAct vs ReWOO: {out_path}")

# =========================================================================
# 3. FIG 3: EVOLUTION TO AGENTIC MESH (BALANCED MODERN CARDS)
# =========================================================================
def make_evolution_mesh_fixed(out_path):
    fig, ax = plt.subplots(figsize=(11, 4.6), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 94, "LỘ TRÌNH TIẾN HÓA: TỪ CHATBOT THỤ ĐỘNG ĐẾN MẠNG LƯỚI TÁC TỬ (AGENTIC MESH)", 
            fontsize=11, fontweight='bold', color='#0f172a', ha='center')

    stages = [
        ("GIAI ĐOẠN 1\nCHATBOT THỤ ĐỘNG", "#475569", "#f8fafc", "#cbd5e1",
         ["• Non-agentic LLM",
          "• Phản hồi prompt thụ động",
          "• Không có công cụ ngoài",
          "• Không nhớ trạng thái",
          "• Dễ xảy ra ảo giác (Hallucination)"]),
        ("GIAI ĐOẠN 2\nTRỢ LÝ COPILOT", "#1d4ed8", "#eff6ff", "#bfdbfe",
         ["• Tool-augmented LLM",
          "• Con người dẫn dắt từng bước",
          "• Gọi được một số API cơ bản",
          "• Sinh code / Tóm tắt văn bản",
          "• Chưa thể tự động sửa lỗi"]),
        ("GIAI ĐOẠN 3\nAGENT ĐƠN LẺ TỰ TRỊ", "#d97706", "#fffbeb", "#fde68a",
         ["• Autonomous Single Agent",
          "• Tự nhận diện mục tiêu cấp cao",
          "• Vòng lặp ReAct lập kế hoạch",
          "• Gọi nhiều công cụ tuần tự",
          "• Tự phản chiếu và thử lại"]),
        ("GIAI ĐOẠN 4\nAGENTIC MESH", "#15803d", "#f0fdf4", "#bbf7d0",
         ["• Multi-Agent Enterprise",
          "• Mạng lưới tác tử chuyên biệt",
          "• Phối hợp qua giao thức A2A",
          "• Tự động hóa end-to-end",
          "• Con người đóng vai trò Giám sát"])
    ]

    x_coords = [2, 27, 52, 77]
    for i, (title, header_col, body_col, border_col, bullets) in enumerate(stages):
        x = x_coords[i]
        # Main Card
        ax.add_patch(patches.FancyBboxPatch((x, 8), 21.5, 76, boxstyle="round,pad=0.3",
                                            facecolor=body_col, edgecolor=border_col, linewidth=1.5))
        # Card Header
        ax.add_patch(patches.FancyBboxPatch((x, 68), 21.5, 16, boxstyle="round,pad=0.2",
                                            facecolor=header_col, edgecolor='none'))
        ax.text(x + 10.75, 76, title, fontsize=8.0, fontweight='bold', color='#ffffff', ha='center', va='center')

        # Bullets
        by = 61.0
        for b in bullets:
            ax.text(x + 1.2, by, b, fontsize=7.2, color='#1e293b', va='center')
            by -= 10.5

    # Inter-stage arrows
    for x in [24.0, 49.0, 74.0]:
        ax.annotate("", xy=(x + 2.5, 46), xytext=(x - 0.2, 46),
                    arrowprops=dict(arrowstyle="->", color="#0284c7", lw=2.5))

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Hoàn thành Evolution Mesh: {out_path}")

os.makedirs("Report/agent01_CT_02_tupv/images", exist_ok=True)
make_ai_agent_architecture_fixed("Report/agent01_CT_02_tupv/images/fig_ai_agent_architecture.png")
make_react_vs_rewoo_fixed("Report/agent01_CT_02_tupv/images/fig_react_vs_rewoo.png")
make_evolution_mesh_fixed("Report/agent01_CT_02_tupv/images/fig_evolution_mesh.png")
