import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

# -------------------------------------------------------------------------
# 1. FIG 1: KIẾN TRÚC NHẬN THỨC CỦA HỆ TÁC TỬ THÔNG MINH (AI AGENT)
# -------------------------------------------------------------------------
def make_ai_agent_architecture(out_path):
    fig, ax = plt.subplots(figsize=(12, 5.2), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Main Diagram Title
    ax.text(50, 96, "KIẾN TRÚC NHẬN THỨC TOÀN DIỆN CỦA HỆ TÁC TỬ THÔNG MINH (AI AGENT COGNITIVE ARCHITECTURE)", 
            fontsize=12, fontweight='bold', color='#0f172a', ha='center')

    # Environment Banner (Top)
    ax.add_patch(patches.FancyBboxPatch((4, 79), 92, 12, boxstyle="round,pad=0.5",
                                        facecolor='#f0f9ff', edgecolor='#0284c7', linewidth=1.8))
    ax.text(50, 86.5, "MÔI TRƯỜNG DOANH NGHIỆP BÊN NGOÀI (ENTERPRISE ENVIRONMENT)", 
            fontsize=10.5, fontweight='bold', color='#0369a1', ha='center')
    ax.text(50, 82.0, "Người dùng (User Goal) • Cơ sở dữ liệu nội bộ • Hệ thống API dịch vụ • Mạng Web • Phần mềm ERP/CRM", 
            fontsize=9.0, color='#0284c7', ha='center')

    # Perception & Action Links
    ax.annotate("", xy=(23, 70), xytext=(23, 79),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=2.2))
    ax.text(24.5, 74.5, "Sensors / Perception (Tiếp nhận Goal)", fontsize=8.8, fontweight='bold', color="#0369a1", va='center')

    ax.annotate("", xy=(77, 79), xytext=(77, 70),
                arrowprops=dict(arrowstyle="->", color="#16a34a", lw=2.2))
    ax.text(78.5, 74.5, "Actuators / Actions (Thực thi Công cụ)", fontsize=8.8, fontweight='bold', color="#15803d", va='center')

    # Big Agent Core Box
    ax.add_patch(patches.FancyBboxPatch((4, 5), 92, 65, boxstyle="round,pad=0.6",
                                        facecolor='#f8fafc', edgecolor='#475569', linewidth=2.0))
    ax.text(50, 66.5, "LÕI SUY LUẬN TỰ TRỊ CỦA TÁC TỬ (AGENT CORE - POWERED BY FOUNDATION LLM)", 
            fontsize=11, fontweight='bold', color='#0f172a', ha='center')

    # 3 Distinct Component Cards
    cards = [
        (6.5, "1. PLANNING & REASONING", "#d97706", "#fffbeb", "#f59e0b", 
         ["• Phân rã mục tiêu (Goal Decomposition)", 
          "• Lập kế hoạch đa bước (Sub-goals)", 
          "• Vòng lặp ReAct (Thought - Action)", 
          "• Cơ chế ReWOO (Lập kế hoạch trước)"]),
        (37.5, "2. MEMORY MANAGEMENT", "#4f46e5", "#eef2ff", "#6366f1",
         ["• Ngữ cảnh ngắn hạn (Context Prompt)", 
          "• Bộ nhớ dài hạn (Vector DB / RAG)", 
          "• Đồ thị tri thức (Knowledge Graph)", 
          "• Theo dõi trạng thái (State Trace)"]),
        (68.5, "3. TOOL USE & EXECUTION", "#16a34a", "#f0fdf4", "#22c55e",
         ["• Gọi hàm ngoại vi (Function Calling)", 
          "• Truy vấn CSDL nội bộ (SQL/API)", 
          "• Thực thi mã lệnh an toàn (Python/Bash)", 
          "• Thu nhận & phân tích kết quả (Observation)"])
    ]

    for x, header, col_head, col_body, col_border, bullets in cards:
        # Card Body
        ax.add_patch(patches.FancyBboxPatch((x, 23), 25, 38, boxstyle="round,pad=0.4",
                                            facecolor=col_body, edgecolor=col_border, linewidth=1.6))
        # Card Header
        ax.add_patch(patches.FancyBboxPatch((x, 54.5), 25, 6.5, boxstyle="round,pad=0.2",
                                            facecolor=col_head, edgecolor='none'))
        ax.text(x + 12.5, 57.7, header, fontsize=9.2, fontweight='bold', color='#ffffff', ha='center', va='center')
        
        # Bullets
        by = 50.0
        for b in bullets:
            ax.text(x + 1.2, by, b, fontsize=8.4, color='#1e293b', va='center')
            by -= 7.2

    # Horizontal interaction arrows
    ax.annotate("", xy=(36.5, 42), xytext=(32.5, 42),
                arrowprops=dict(arrowstyle="<->", color="#475569", lw=2.2))
    ax.annotate("", xy=(67.5, 42), xytext=(63.5, 42),
                arrowprops=dict(arrowstyle="<->", color="#475569", lw=2.2))

    # Bottom Safety & Guardrails Banner
    ax.add_patch(patches.FancyBboxPatch((6.5, 8), 87, 11, boxstyle="round,pad=0.4",
                                        facecolor='#fef2f2', edgecolor='#ef4444', linewidth=1.6))
    ax.text(50, 15.0, "QUẢN TRỊ AN TOÀN, PHẢN HỒI VÀ KIỂM TOÁN (IBM & MCKINSEY BEST PRACTICES)", 
            fontsize=9.5, fontweight='bold', color='#991b1b', ha='center')
    ax.text(50, 10.8, "Tự phản chiếu (Self-reflection) • Con người can thiệp (HITL) • Nhật ký kiểm toán (Audit Trail) • Rào chắn Max Iterations", 
            fontsize=8.5, color='#7f1d1d', ha='center')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Hoàn tất: {out_path}")

# -------------------------------------------------------------------------
# 2. FIG 2: TIẾN HÓA CÔNG NGHỆ TỪ CHATBOT ĐẾN AGENTIC MESH
# -------------------------------------------------------------------------
def make_evolution_mesh(out_path):
    fig, ax = plt.subplots(figsize=(12, 4.5), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 95, "LỘ TRÌNH TIẾN HÓA: TỪ CHATBOT THỤ ĐỘNG ĐẾN MẠNG LƯỚI TÁC TỬ (AGENTIC MESH)", 
            fontsize=12, fontweight='bold', color='#0f172a', ha='center')

    stages = [
        ("GIAI ĐOẠN 1\nCHATBOT THỤ ĐỘNG", "#475569", "#f8fafc", "#cbd5e1",
         ["• Non-agentic LLM",
          "• Phản hồi prompt thụ động",
          "• Không có công cụ ngoài",
          "• Không lưu giữ trạng thái",
          "• Dễ xảy ra ảo giác (Hallucination)"]),
        ("GIAI ĐOẠN 2\nTRỢ LÝ COPILOT", "#1d4ed8", "#eff6ff", "#bfdbfe",
         ["• Tool-augmented LLM",
          "• Con người dẫn dắt từng bước",
          "• Gọi API theo yêu cầu",
          "• Sinh mã / Tóm tắt văn bản",
          "• Chưa thể tự động sửa sai"]),
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
        ax.add_patch(patches.FancyBboxPatch((x, 6), 21.5, 78, boxstyle="round,pad=0.4",
                                            facecolor=body_col, edgecolor=border_col, linewidth=1.6))
        # Card Header
        ax.add_patch(patches.FancyBboxPatch((x, 67), 21.5, 17, boxstyle="round,pad=0.2",
                                            facecolor=header_col, edgecolor='none'))
        ax.text(x + 10.75, 75.5, title, fontsize=8.8, fontweight='bold', color='#ffffff', ha='center', va='center')

        # Bullets
        by = 59.5
        for b in bullets:
            ax.text(x + 1.2, by, b, fontsize=8.0, color='#1e293b', va='center')
            by -= 10.8

    # Inter-stage arrows
    for x in [24.0, 49.0, 74.0]:
        ax.annotate("", xy=(x + 2.6, 45), xytext=(x - 0.2, 45),
                    arrowprops=dict(arrowstyle="->", color="#0284c7", lw=3.0))

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Hoàn tất: {out_path}")

# -------------------------------------------------------------------------
# 3. FIG 3: REACT VS REWOO REASONING
# -------------------------------------------------------------------------
def make_react_vs_rewoo(out_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.0), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    for ax in [ax1, ax2]:
        ax.set_facecolor('#ffffff')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')

    # Subplot 1: ReAct
    ax1.text(50, 96, "Mô hình ReAct (Reasoning + Acting)", fontsize=11.5, fontweight='bold', color='#1e3a8a', ha='center')
    ax1.text(50, 91.5, "[Vòng lặp suy nghĩ và hành động từng bước liên tục]", fontsize=9.0, color='#3b82f6', ha='center')

    react_nodes = [
        ("1. User Goal (Mục tiêu người dùng)", "#f1f5f9", "#475569", 83),
        ("2. THOUGHT: Suy luận trạng thái & bước đi", "#dbeafe", "#1d4ed8", 68),
        ("3. ACTION: Chọn công cụ & sinh tham số", "#f3e8ff", "#7e22ce", 53),
        ("4. OBSERVATION: Thu nhận kết quả từ Tools", "#dcfce7", "#15803d", 38),
        ("5. THOUGHT TIẾP THEO (Đánh giá dữ liệu)", "#dbeafe", "#1d4ed8", 23),
        ("6. FINAL ANSWER: Xuất kết quả hoàn tất", "#fee2e2", "#b91c1c", 8),
    ]

    for title, bg, border, y in react_nodes:
        ax1.add_patch(patches.FancyBboxPatch((6, y-4.2), 76, 8.4, boxstyle="round,pad=0.3",
                                             facecolor=bg, edgecolor=border, linewidth=1.4))
        ax1.text(44, y, title, fontsize=8.6, fontweight='bold', color=border, ha='center', va='center')

    for y_top, y_bot in [(78.8, 72.2), (63.8, 57.2), (48.8, 42.2), (33.8, 27.2), (18.8, 12.2)]:
        ax1.annotate("", xy=(44, y_bot), xytext=(44, y_top),
                     arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.8))

    # Curved loopback arrow on right side
    ax1.annotate("", xy=(83, 68), xytext=(83, 38),
                 arrowprops=dict(arrowstyle="->", color="#ea580c", lw=2.2, connectionstyle="arc3,rad=-0.45"))
    ax1.text(93, 53, "Vòng lặp\nReAct\n(N bước)", fontsize=8.5, fontweight='bold', color="#c2410c", ha='center', va='center')

    # Subplot 2: ReWOO
    ax2.text(50, 96, "Mô hình ReWOO (Reasoning Without Observation)", fontsize=11.5, fontweight='bold', color='#065f46', ha='center')
    ax2.text(50, 91.5, "[Lập toàn bộ kế hoạch trước, thực thi công cụ song song]", fontsize=9.0, color='#059669', ha='center')

    rewoo_nodes = [
        ("1. User Goal (Mục tiêu người dùng)", "#f1f5f9", "#475569", 83, 8.4),
        ("2. PLANNER (LLM): Lập toàn bộ chuỗi kế hoạch gọi Tools\n[Plan 1: Tool A → Plan 2: Tool B → Plan 3: Tool C]", "#fef3c7", "#d97706", 65, 11.5),
        ("3. WORKER: Thực thi hàng loạt công cụ ngoại vi\n(Gọi song song các API/CSDL, tiết kiệm độ trễ tối đa)", "#dcfce7", "#16a34a", 45, 11.5),
        ("4. SOLVER (LLM): Đọc toàn bộ kết quả để tổng hợp\n(Chỉ 2 lần gọi LLM: lúc lập kế hoạch và lúc kết luận)", "#e0e7ff", "#4338ca", 25, 11.5),
        ("5. FINAL ANSWER: Kết quả tối ưu chi phí & Token", "#fee2e2", "#b91c1c", 8, 8.4),
    ]

    for title, bg, border, y, h in rewoo_nodes:
        ax2.add_patch(patches.FancyBboxPatch((6, y-h/2), 88, h, boxstyle="round,pad=0.3",
                                             facecolor=bg, edgecolor=border, linewidth=1.4))
        ax2.text(50, y, title, fontsize=8.6, fontweight='bold', color=border, ha='center', va='center')

    for y_top, y_bot in [(78.8, 70.8), (59.2, 50.8), (39.2, 30.8), (19.2, 12.2)]:
        ax2.annotate("", xy=(50, y_bot), xytext=(50, y_top),
                     arrowprops=dict(arrowstyle="->", color="#059669", lw=2.0))

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Hoàn tất: {out_path}")

# -------------------------------------------------------------------------
# 4. FIG 4: KIẾN TRÚC TỔNG QUÁT CỦA TÁC TỬ HỌC MÁY (RUSSELL & NORVIG)
# -------------------------------------------------------------------------
def make_learning_agent_architecture(out_path):
    fig, ax = plt.subplots(figsize=(12, 4.8), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 96, 'KIẾN TRÚC TỔNG QUÁT CỦA TÁC TỬ HỌC MÁY (LEARNING AGENT ARCHITECTURE)',
            fontsize=12, fontweight='bold', ha='center', va='center', color='#0f172a')
    ax.text(50, 91.5, 'Theo chuẩn lý thuyết kinh điển của Stuart Russell & Peter Norvig (AIMA 4th Edition)',
            fontsize=9.5, fontstyle='italic', ha='center', va='center', color='#475569')

    # Outer Agent Boundary Box
    ax.add_patch(patches.FancyBboxPatch((18, 8), 65, 78, boxstyle='round,pad=0.8',
                                        facecolor='#f8fafc', edgecolor='#3b82f6', linewidth=2.0, linestyle='--'))
    ax.text(50.5, 82.5, 'Ranh giới Tác tử Thông minh (Agent Boundary)', fontsize=10.5, fontweight='bold',
            color='#1d4ed8', ha='center', va='center')

    # Component 1: Performance Element
    ax.add_patch(patches.FancyBboxPatch((50, 18), 30, 24, boxstyle='round,pad=0.6',
                                        facecolor='#dbeafe', edgecolor='#2563eb', linewidth=1.8))
    ax.text(65, 36.5, 'PERFORMANCE ELEMENT', fontsize=10, fontweight='bold', color='#1e40af', ha='center')
    ax.text(65, 31.0, '(Thành phần Thực thi & Hành động)', fontsize=8.5, fontstyle='italic', color='#1e3a8a', ha='center')
    ax.text(65, 24.5, '• Tiếp nhận trạng thái từ Sensors\n• Chọn hành động tối ưu theo Policy hiện tại',
            fontsize=8.5, color='#1e293b', ha='center')

    # Component 2: Critic
    ax.add_patch(patches.FancyBboxPatch((21, 52), 26, 23, boxstyle='round,pad=0.6',
                                        facecolor='#fef3c7', edgecolor='#d97706', linewidth=1.8))
    ax.text(34, 69.5, 'CRITIC (Bộ Phê Phán)', fontsize=10, fontweight='bold', color='#92400e', ha='center')
    ax.text(34, 64.0, '(Đánh giá mức độ thành công)', fontsize=8.5, fontstyle='italic', color='#78350f', ha='center')
    ax.text(34, 57.5, '• Đối chiếu kết quả với Tiêu chuẩn\n• Sinh tín hiệu phản hồi (Reward/Penalty)',
            fontsize=8.5, color='#1e293b', ha='center')

    # Component 3: Learning Element
    ax.add_patch(patches.FancyBboxPatch((52, 52), 28, 23, boxstyle='round,pad=0.6',
                                        facecolor='#dcfce7', edgecolor='#16a34a', linewidth=1.8))
    ax.text(66, 69.5, 'LEARNING ELEMENT', fontsize=10, fontweight='bold', color='#166534', ha='center')
    ax.text(66, 64.0, '(Bộ phận Học tập thích nghi)', fontsize=8.5, fontstyle='italic', color='#14532d', ha='center')
    ax.text(66, 57.5, '• Cập nhật tri thức Q-Table / Trọng số\n• Đề xuất cải tiến mục tiêu cho Performance',
            fontsize=8.5, color='#1e293b', ha='center')

    # Component 4: Problem Generator
    ax.add_patch(patches.FancyBboxPatch((21, 18), 26, 24, boxstyle='round,pad=0.6',
                                        facecolor='#f3e8ff', edgecolor='#9333ea', linewidth=1.8))
    ax.text(34, 36.5, 'PROBLEM GENERATOR', fontsize=9.8, fontweight='bold', color='#6b21a8', ha='center')
    ax.text(34, 31.0, '(Bộ kích thích Khám phá)', fontsize=8.5, fontstyle='italic', color='#581c87', ha='center')
    ax.text(34, 24.5, '• Gợi ý hành động trải nghiệm mới\n• Chiến lược Exploration (epsilon-greedy)',
            fontsize=8.5, color='#1e293b', ha='center')

    # External Environment (Left side)
    ax.add_patch(patches.FancyBboxPatch((1, 16), 13, 62, boxstyle='round,pad=0.6',
                                        facecolor='#f1f5f9', edgecolor='#475569', linewidth=1.8))
    ax.text(7.5, 47, 'MÔI TRƯỜNG\nBÊN NGOÀI\n(Environment)', fontsize=9.5, fontweight='bold', color='#334155', ha='center', va='center')

    # Sensors (S) and Actuators (A)
    ax.add_patch(patches.Rectangle((18, 59), 3.0, 9, facecolor='#64748b', edgecolor='none'))
    ax.text(19.5, 63.5, 'S', color='#ffffff', fontweight='bold', ha='center', va='center', fontsize=9.5)
    ax.text(19.5, 71, 'Sensors', color='#1e293b', fontsize=8.5, fontweight='bold', ha='center')

    ax.add_patch(patches.Rectangle((80, 25.5), 3.0, 9, facecolor='#ea580c', edgecolor='none'))
    ax.text(81.5, 30.0, 'A', color='#ffffff', fontweight='bold', ha='center', va='center', fontsize=9.5)
    ax.text(81.5, 37.5, 'Actuators', color='#c2410c', fontsize=8.5, fontweight='bold', ha='center')

    # Interconnecting Arrows
    # Environment -> Sensors
    ax.annotate('', xy=(18, 63.5), xytext=(14, 63.5), arrowprops=dict(arrowstyle='->', lw=2.2, color='#475569'))
    ax.text(16, 66, 'Percepts', fontsize=8.5, fontweight='bold', ha='center', color='#475569')

    # Sensors -> Critic & Performance Element
    ax.annotate('', xy=(21, 63.5), xytext=(20.5, 63.5), arrowprops=dict(arrowstyle='->', lw=2.0, color='#2563eb'))
    ax.annotate('', xy=(50, 32), xytext=(21, 60), arrowprops=dict(arrowstyle='->', lw=2.0, color='#2563eb'))

    # Critic -> Learning Element (Feedback signal)
    ax.annotate('', xy=(52, 63.5), xytext=(47, 63.5), arrowprops=dict(arrowstyle='->', lw=2.2, color='#16a34a'))
    ax.text(49.5, 66, 'Feedback (Reward)', fontsize=8.5, fontweight='bold', ha='center', color='#16a34a')

    # Learning Element -> Problem Generator
    ax.annotate('', xy=(34, 42), xytext=(57, 52), arrowprops=dict(arrowstyle='->', lw=2.0, color='#9333ea'))
    ax.text(43, 48.5, 'Learning Goals', fontsize=8.5, fontweight='bold', ha='center', color='#9333ea')

    # Problem Generator -> Performance Element
    ax.annotate('', xy=(50, 27.5), xytext=(47, 27.5), arrowprops=dict(arrowstyle='->', lw=2.0, color='#9333ea'))
    ax.text(48.5, 30.5, 'Explore', fontsize=8.5, fontweight='bold', ha='center', color='#9333ea')

    # Learning Element -> Performance Element (Policy Update)
    ax.annotate('', xy=(66, 42), xytext=(66, 52), arrowprops=dict(arrowstyle='->', lw=2.2, color='#16a34a'))
    ax.text(68, 47, 'Policy Update', fontsize=8.5, fontweight='bold', ha='left', color='#16a34a')

    # Performance Element -> Actuators -> Environment
    ax.annotate('', xy=(80, 30), xytext=(79.5, 30), arrowprops=dict(arrowstyle='->', lw=2.2, color='#ea580c'))
    ax.annotate('', xy=(14, 25), xytext=(83, 25), arrowprops=dict(arrowstyle='->', lw=2.2, color='#ea580c', connectionstyle='arc3,rad=-0.38'))
    ax.text(50, 2.0, 'Actions tác động trở lại Môi trường (Environment Feedback Loop)', fontsize=9.5, fontweight='bold', ha='center', color='#ea580c')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Hoàn tất: {out_path}")

if __name__ == "__main__":
    out_dir = "Report/agent01_CT_02_tupv/images"
    make_ai_agent_architecture(f"{out_dir}/fig_ai_agent_architecture.png")
    make_evolution_mesh(f"{out_dir}/fig_evolution_mesh.png")
    make_react_vs_rewoo(f"{out_dir}/fig_react_vs_rewoo.png")
    make_learning_agent_architecture(f"{out_dir}/fig_learning_agent_architecture.png")
    print("✓ Toàn bộ 4 sơ đồ lý thuyết đã được tối ưu hóa độ nét, tỷ lệ và độ lớn phông chữ!")
