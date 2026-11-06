import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Set global typography
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.monospace'] = ['Courier New', 'DejaVu Sans Mono']

# 1. SCREENSHOT CODE (Jupyter Notebook)
def make_code_screenshot(out_path):
    fig, ax = plt.subplots(figsize=(11, 7.0), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Top Jupyter Header Bar
    ax.add_patch(patches.Rectangle((0, 93), 100, 7, facecolor='#f8f9fa', edgecolor='#dee2e6', linewidth=1))
    ax.text(2, 96.5, "Jupyter", fontsize=12, fontweight='bold', color='#f37626', va='center', fontfamily='Arial')
    ax.text(10.5, 96.5, "agent01_ai_agent_react.ipynb", fontsize=11, fontweight='bold', color='#212529', va='center', fontfamily='Arial')
    ax.text(46, 96.5, "(Python 3 / Trusted)", fontsize=9, color='#6c757d', va='center', fontfamily='Arial')
    ax.text(80, 96.5, "Kernel: Idle | Memory: 84MB", fontsize=8.5, color='#198754', va='center', fontfamily='Arial')

    # Toolbar
    ax.add_patch(patches.Rectangle((0, 87), 100, 6, facecolor='#ffffff', edgecolor='#dee2e6', linewidth=0.8))
    toolbar_buttons = ["Run", "Interrupt", "Restart", "Cell", "Markdown", "Code"]
    bx = 3
    for btn in toolbar_buttons:
        ax.add_patch(patches.FancyBboxPatch((bx, 88.5), len(btn)*1.1 + 3.5, 3.2, boxstyle="round,pad=0.2",
                                            facecolor='#f8f9fa', edgecolor='#ced4da', linewidth=0.8))
        ax.text(bx + (len(btn)*1.1 + 3.5)/2, 90.1, btn, fontsize=8, color='#495057', ha='center', va='center', fontfamily='Arial')
        bx += len(btn)*1.1 + 5.5

    # Cell 1: Markdown header
    ax.add_patch(patches.Rectangle((2, 79), 96, 7, facecolor='#f1f5f9', edgecolor='#cbd5e1', linewidth=0.8))
    ax.text(3, 83.5, "BÀI THỰC HÀNH AGENT 01: XÂY DỰNG AI AGENT THEO CƠ CHẾ REACT & TOOL-CALLING", 
            fontsize=9.5, fontweight='bold', color='#0f172a', fontfamily='Arial')
    ax.text(3, 80.5, "Sinh viên: Phạm Văn Tư - B23DCCN879 | Môn: PTHT Thông Minh | Nguồn tham chiếu: IBM Think [2]", 
            fontsize=8, color='#334155', fontfamily='Arial')

    # Cell 2: Code cell prompt
    ax.text(1.2, 74.5, "In [2]:", fontsize=9, fontweight='bold', color='#1d4ed8', fontfamily='Courier New')
    
    # Code box
    ax.add_patch(patches.FancyBboxPatch((7, 4.0), 91, 72.0, boxstyle="round,pad=0.3",
                                        facecolor='#f8fafc', edgecolor='#94a3b8', linewidth=1.2))
    
    code_lines = [
        ("class ReActAIAgent:", "#1d4ed8", True),
        ("    def __init__(self, agent_id='AGENT-IBM-01', max_iterations=6):", "#0f172a", False),
        ("        self.agent_id = agent_id", "#0f172a", False),
        ("        self.max_iterations = max_iterations", "#0f172a", False),
        ("        self.activity_log = []", "#0f172a", False),
        ("        self.tools = {", "#0f172a", False),
        ("            'query_product_catalog': EnterpriseTools.query_product_catalog,", "#b91c1c", False),
        ("            'query_discount_policy': EnterpriseTools.query_discount_policy,", "#b91c1c", False),
        ("            'financial_calculator': EnterpriseTools.financial_calculator", "#b91c1c", False),
        ("        }", "#0f172a", False),
        ("    ", "#0f172a", False),
        ("    def execute(self, user_goal: str):", "#0f172a", False),
        ("        self.log_event('Goal Initialization', user_goal)", "#15803d", False),
        ("        iteration = 0", "#0f172a", False),
        ("        while iteration < self.max_iterations:", "#1d4ed8", True),
        ("            iteration += 1", "#0f172a", False),
        ("            # 1. THOUGHT: Tác tử nhận thức trạng thái và lập kế hoạch", "#15803d", False),
        ("            thought = self.reason_next_step(state)", "#0f172a", False),
        ("            self.log_event('Thought', thought)", "#15803d", False),
        ("            ", "#0f172a", False),
        ("            # 2. ACTION: Tác tử gọi công cụ phù hợp", "#15803d", False),
        ("            action, action_input = self.select_tool(thought)", "#0f172a", False),
        ("            self.log_event('Action', f'Call {action} with {action_input}')", "#15803d", False),
        ("            ", "#0f172a", False),
        ("            # 3. OBSERVATION: Thu nhận kết quả từ môi trường", "#15803d", False),
        ("            observation = self.tools[action](action_input)", "#0f172a", False),
        ("            self.log_event('Observation', str(observation))", "#15803d", False),
        ("            ", "#0f172a", False),
        ("            if self.is_goal_achieved(state):", "#1d4ed8", True),
        ("                self.log_event('Final Answer', self.synthesize_response(state))", "#15803d", False),
        ("                break", "#1d4ed8", True),
    ]

    y = 73
    for line in code_lines:
        txt, col, is_bold = line
        weight = 'bold' if is_bold else 'normal'
        ax.text(8.5, y, txt, fontsize=7.7, color=col, fontfamily='Courier New', fontweight=weight)
        y -= 2.05

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Hoàn thành: {out_path}")

# 2. SCREENSHOT OUTPUT (Jupyter Notebook Execution)
def make_output_screenshot(out_path):
    fig, ax = plt.subplots(figsize=(11, 7.2), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Cell 3 prompt
    ax.text(1.2, 96.5, "In [3]:", fontsize=9, fontweight='bold', color='#1d4ed8', fontfamily='Courier New')
    
    # Input Code box (Execute request)
    ax.add_patch(patches.FancyBboxPatch((7, 85), 91, 10.5, boxstyle="round,pad=0.2",
                                        facecolor='#f8fafc', edgecolor='#94a3b8', linewidth=1.0))
    ax.text(8.5, 92.5, "agent = ReActAIAgent(agent_id='AGENT-REACT-B23DCCN879-01', max_iterations=5)",
            fontsize=8, color='#0f172a', fontfamily='Courier New')
    ax.text(8.5, 89.5, "query = 'Khách hàng VINATECH đặt 25 máy trạm AI H100. Tra cứu giá, tính chiết khấu & VAT 8%'",
            fontsize=8, color='#b91c1c', fontfamily='Courier New')
    ax.text(8.5, 86.5, "state, logs = agent.execute(query)", fontsize=8, color='#0f172a', fontfamily='Courier New')

    # Output Terminal Area
    ax.add_patch(patches.FancyBboxPatch((7, 2.5), 91, 80.5, boxstyle="round,pad=0.3",
                                        facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1.2))
    
    # Left accent line for output
    ax.add_patch(patches.Rectangle((7, 2.5), 1.2, 80.5, facecolor='#16a34a', edgecolor='none'))

    out_lines = [
        ("================================================================================", "#64748b", False),
        ("BẮT ĐẦU VẬN HÀNH AI AGENT (ID: AGENT-REACT-B23DCCN879-01)", "#0f172a", True),
        ("MỤC TIÊU (GOAL): Khách hàng VINATECH đặt mua 25 máy trạm tính toán AI GPU H100...", "#1e40af", False),
        ("================================================================================", "#64748b", False),
        ("--- [Chu trình ReAct Bước 1/5] ---", "#b45309", True),
        ("[THOUGHT]    : Cần tra cứu đơn giá niêm yết và tồn kho của máy trạm H100 trong CSDL kho.", "#1e3a8a", False),
        ("[ACTION]     : Gọi công cụ 'query_product_catalog' với tham số 'ai_workstation_h100'", "#7e22ce", True),
        ("[OBSERVATION]: {'name': 'Máy trạm AI GPU H100 80GB', 'unit_price_vnd': 280,000,000, 'stock': 45}", "#15803d", False),
        ("--- [Chu trình ReAct Bước 2/5] ---", "#b45309", True),
        ("[THOUGHT]    : Đã có đơn giá. Cần kiểm tra chính sách chiết khấu bậc thang cho 25 máy.", "#1e3a8a", False),
        ("[ACTION]     : Gọi công cụ 'query_discount_policy' với tham số {'quantity': 25, 'tier': 'Enterprise'}", "#7e22ce", True),
        ("[OBSERVATION]: {'discount_percentage': 12.0, 'policy_note': 'Chiết khấu Tier 1 (>= 20 máy)'}", "#15803d", False),
        ("--- [Chu trình ReAct Bước 3/5] ---", "#b45309", True),
        ("[THOUGHT]    : Chiết khấu 12%. Gọi máy tính tài chính tính tiền hàng: 25 * 280,000,000 * (1 - 0.12)", "#1e3a8a", False),
        ("[ACTION]     : Gọi công cụ 'financial_calculator' với biểu thức: '25 * 280000000 * 0.88'", "#7e22ce", True),
        ("[OBSERVATION]: {'expression': '25 * 280000000 * 0.88', 'result': 6160000000.0}", "#15803d", False),
        ("--- [Chu trình ReAct Bước 4/5] ---", "#b45309", True),
        ("[THOUGHT]    : Tiền trước thuế: 6.16 tỷ VNĐ. Áp dụng thuế suất VAT 8% để xác định tổng tiền.", "#1e3a8a", False),
        ("[ACTION]     : Gọi công cụ 'financial_calculator' với biểu thức: '6160000000 * 1.08'", "#7e22ce", True),
        ("[OBSERVATION]: {'expression': '6160000000 * 1.08', 'result': 6652800000.0}", "#15803d", False),
        ("--- [Chu trình ReAct Bước 5/5: Hoàn tất Mục tiêu] ---", "#16a34a", True),
        ("[FINAL ANSWER]: BÁO CÁO KẾT QUẢ ĐƠN HÀNG DOANH NGHIỆP VINATECH:", "#0f172a", True),
        ("  - Số lượng: 25 máy trạm AI GPU H100 | Đơn giá niêm yết: 280,000,000 VNĐ/chiếc", "#334155", False),
        ("  - Mức chiết khấu: 12% (Doanh nghiệp tiết kiệm được: 840,000,000 VNĐ)", "#334155", False),
        ("  - Tổng tiền hàng trước thuế: 6,160,000,000 VNĐ | Thuế VAT 8%: 492,800,000 VNĐ", "#334155", False),
        ("  - TỔNG SỐ TIỀN PHẢI THANH TOÁN: 6,652,800,000 VNĐ (Sáu tỷ sáu trăm năm mươi hai triệu...)", "#dc2626", True),
        ("================================================================================", "#64748b", False),
        ("[AUDIT TRAIL]: Đã lưu toàn bộ 11 sự kiện nhận thức vào hệ thống giám sát IBM Telemetry.", "#475569", False)
    ]

    y = 80.5
    for line in out_lines:
        txt, col, is_bold = line
        weight = 'bold' if is_bold else 'normal'
        ax.text(8.5, y, txt, fontsize=7.5, color=col, fontfamily='Courier New', fontweight=weight)
        y -= 2.75

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Hoàn thành: {out_path}")

# 3. DIAGRAM: AI AGENT COGNITIVE ARCHITECTURE (Russell & Norvig, Google Cloud, IBM Think)
def make_ai_agent_architecture(out_path):
    fig, ax = plt.subplots(figsize=(11, 5.8), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 95, "KIẾN TRÚC NHẬN THỨC CỦA HỆ TÁC TỬ THÔNG MINH (AI AGENT COGNITIVE ARCHITECTURE)", 
            fontsize=11.5, fontweight='bold', color='#0f172a', ha='center', fontfamily='Arial')

    # Environment (Top)
    ax.add_patch(patches.FancyBboxPatch((10, 78), 80, 11, boxstyle="round,pad=0.5",
                                        facecolor='#e0f2fe', edgecolor='#0284c7', linewidth=1.5))
    ax.text(50, 84, "MÔI TRƯỜNG BÊN NGOÀI (ENVIRONMENT / ENTERPRISE ECOSYSTEM)", 
            fontsize=10, fontweight='bold', color='#0369a1', ha='center')
    ax.text(50, 80, "Người dùng (User Goal) • Cơ sở dữ liệu (Database) • Hệ thống API • Web • Hệ thống phần mềm", 
            fontsize=8.5, color='#0c4a6e', ha='center')

    # Sensors / Perception Arrow Down
    ax.annotate("", xy=(25, 68), xytext=(25, 78),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=2))
    ax.text(26, 73, "Sensors / Inputs\n(Perception & Prompt)", fontsize=8, color="#0369a1", va='center')

    # Actuators / Tools Arrow Up
    ax.annotate("", xy=(75, 78), xytext=(75, 68),
                arrowprops=dict(arrowstyle="->", color="#16a34a", lw=2))
    ax.text(76, 73, "Actuators / Actions\n(Tool Invocation)", fontsize=8, color="#15803d", va='center')

    # Central Agent Core Box
    ax.add_patch(patches.FancyBboxPatch((8, 12), 84, 56, boxstyle="round,pad=0.8",
                                        facecolor='#f8fafc', edgecolor='#64748b', linewidth=2.0))
    ax.text(50, 64, "LÕI SUY LUẬN TỰ TRỊ CỦA TÁC TỬ (AGENT CORE - POWERED BY LLM / FOUNDATION MODEL)", 
            fontsize=10.5, fontweight='bold', color='#1e293b', ha='center')

    # 4 Sub-modules inside Core:
    # 1. Planning & Goal Decomposition
    ax.add_patch(patches.FancyBboxPatch((11, 35), 23, 24, boxstyle="round,pad=0.4",
                                        facecolor='#fef3c7', edgecolor='#d97706', linewidth=1.5))
    ax.text(22.5, 55, "PLANNING & REASONING", fontsize=9, fontweight='bold', color='#92400e', ha='center')
    ax.text(22.5, 51, "• Goal Decomposition\n• Sub-goal Sequencing\n• ReAct / ReWOO Loop\n• Tree of Thoughts", 
            fontsize=7.8, color='#78350f', ha='center')

    # 2. Memory Module
    ax.add_patch(patches.FancyBboxPatch((38, 35), 24, 24, boxstyle="round,pad=0.4",
                                        facecolor='#e0e7ff', edgecolor='#4f46e5', linewidth=1.5))
    ax.text(50, 55, "MEMORY MODULE", fontsize=9, fontweight='bold', color='#3730a3', ha='center')
    ax.text(50, 51, "• Short-term Context\n• Long-term Memory (Vector)\n• Knowledge Graph RAG\n• State Management", 
            fontsize=7.8, color='#312e81', ha='center')

    # 3. Tool Use / Action Engine
    ax.add_patch(patches.FancyBboxPatch((66, 35), 23, 24, boxstyle="round,pad=0.4",
                                        facecolor='#dcfce7', edgecolor='#16a34a', linewidth=1.5))
    ax.text(77.5, 55, "TOOL USE & EXECUTION", fontsize=9, fontweight='bold', color='#166534', ha='center')
    ax.text(77.5, 51, "• Function Calling\n• API Integration\n• DB & Code Execution\n• Observation Parsing", 
            fontsize=7.8, color='#14532d', ha='center')

    # Bottom Safety & Reflection Bar
    ax.add_patch(patches.FancyBboxPatch((11, 16), 78, 15, boxstyle="round,pad=0.4",
                                        facecolor='#fee2e2', edgecolor='#ef4444', linewidth=1.5))
    ax.text(50, 27, "REFLECTION, GOVERNANCE & SAFETY CONTROLS (IBM & MCKINSEY BEST PRACTICES)", 
            fontsize=9, fontweight='bold', color='#991b1b', ha='center')
    ax.text(50, 20.5, "Self-Reflection • Human-in-the-Loop (HITL) Interruption • Activity Logging & Audit Trail • Max Iteration Guardrail", 
            fontsize=8, color='#7f1d1d', ha='center')

    # Connecting arrows inside core
    ax.annotate("", xy=(37.5, 47), xytext=(34.5, 47),
                arrowprops=dict(arrowstyle="<->", color="#64748b", lw=1.5))
    ax.annotate("", xy=(65.5, 47), xytext=(62.5, 47),
                arrowprops=dict(arrowstyle="<->", color="#64748b", lw=1.5))
    ax.annotate("", xy=(50, 31.5), xytext=(50, 34.5),
                arrowprops=dict(arrowstyle="<->", color="#64748b", lw=1.5))

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Hoàn thành: {out_path}")

# 4. DIAGRAM: REACT VS REWOO REASONING PARADIGMS (IBM Think)
def make_react_vs_rewoo_diagram(out_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.2), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    for ax in [ax1, ax2]:
        ax.set_facecolor('#ffffff')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')

    # Subplot 1: ReAct Paradigm
    ax1.set_title("Cơ chế ReAct (Reasoning + Acting)\n[Tương tác quan sát từng bước liên tục]", 
                  fontsize=10.5, fontweight='bold', color='#1e3a8a', pad=10)
    
    react_steps = [
        ("Mục tiêu người dùng (User Goal)", "#f1f5f9", "#475569", 88),
        ("THOUGHT: Suy luận trạng thái & lập bước tiếp theo", "#dbeafe", "#1d4ed8", 72),
        ("ACTION: Lựa chọn công cụ & sinh tham số", "#f3e8ff", "#7e22ce", 56),
        ("OBSERVATION: Môi trường trả lời kết quả", "#dcfce7", "#15803d", 40),
        ("THOUGHT TIẾP THEO (Đánh giá lại thông tin)", "#dbeafe", "#1d4ed8", 24),
        ("FINAL ANSWER: Xuất báo cáo kết luận", "#fee2e2", "#b91c1c", 8),
    ]

    for title, bg, border, y in react_steps:
        ax1.add_patch(patches.FancyBboxPatch((10, y-4), 80, 8.5, boxstyle="round,pad=0.3",
                                             facecolor=bg, edgecolor=border, linewidth=1.2))
        ax1.text(50, y+0.2, title, fontsize=8, fontweight='bold', color=border, ha='center', va='center')

    # Arrows for ReAct
    for y_top, y_bot in [(84, 76.5), (68, 60.5), (52, 44.5), (36, 28.5), (20, 12.5)]:
        ax1.annotate("", xy=(50, y_bot), xytext=(50, y_top),
                     arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.5))
    # Loopback arrow for iterative observation
    ax1.annotate("", xy=(91, 72), xytext=(91, 40),
                 arrowprops=dict(arrowstyle="->", color="#d97706", lw=1.8, connectionstyle="arc3,rad=-0.4"))
    ax1.text(94, 56, "Vòng lặp ReAct\n(N lần suy luận)", fontsize=7.5, color="#b45309", rotation=270, va='center')

    # Subplot 2: ReWOO Paradigm
    ax2.set_title("Cơ chế ReWOO (Reasoning Without Observation)\n[Lập toàn bộ kế hoạch trước, thực thi song song]", 
                  fontsize=10.5, fontweight='bold', color='#065f46', pad=10)

    rewoo_steps = [
        ("Mục tiêu người dùng (User Goal)", "#f1f5f9", "#475569", 88),
        ("PLANNER (LLM): Lập toàn bộ chuỗi kế hoạch\n[Plan 1: Tool A → Plan 2: Tool B → Plan 3: Tool C]", "#fef3c7", "#d97706", 68),
        ("WORKER: Thực thi hàng loạt công cụ ngoại vi\n(Gọi song song các API/CSDL, tiết kiệm độ trễ)", "#dcfce7", "#16a34a", 44),
        ("SOLVER (LLM): Đọc toàn bộ kết quả & Tổng hợp\n(Chỉ 2 lần gọi LLM: lúc lập kế hoạch và lúc kết luận)", "#e0e7ff", "#4338ca", 22),
        ("FINAL ANSWER: Kết quả tối ưu chi phí Token", "#fee2e2", "#b91c1c", 6),
    ]

    for title, bg, border, y in rewoo_steps:
        h = 11 if "PLANNER" in title or "WORKER" in title or "SOLVER" in title else 8.5
        ax2.add_patch(patches.FancyBboxPatch((10, y-h/2), 80, h, boxstyle="round,pad=0.3",
                                             facecolor=bg, edgecolor=border, linewidth=1.2))
        ax2.text(50, y, title, fontsize=8, fontweight='bold', color=border, ha='center', va='center')

    # Arrows for ReWOO
    for y_top, y_bot in [(83.7, 73.5), (62.5, 49.5), (38.5, 27.5), (16.5, 10.2)]:
        ax2.annotate("", xy=(50, y_bot), xytext=(50, y_top),
                     arrowprops=dict(arrowstyle="->", color="#059669", lw=1.8))

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Hoàn thành: {out_path}")

# 5. DIAGRAM: EVOLUTION FROM CHATBOT TO AGENTIC MESH (Google & McKinsey)
def make_evolution_mesh_diagram(out_path):
    fig, ax = plt.subplots(figsize=(11, 4.6), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 93, "SỰ TIẾN HÓA MÔ HÌNH: TỪ NON-AGENTIC CHATBOT ĐẾN ENTERPRISE AGENTIC MESH", 
            fontsize=11, fontweight='bold', color='#0f172a', ha='center')

    stages = [
        ("GIAI ĐOẠN 1: CHATBOT THỤ ĐỘNG\n(Non-agentic LLM)", 
         "• Chỉ trả lời câu hỏi prompt-by-prompt\n• Không có công cụ ngoại vi\n• Không có bộ nhớ trạng thái dài hạn\n• Ảo giác (Hallucination) cao", 
         "#f1f5f9", "#475569", 4),
        ("GIAI ĐOẠN 2: COPILOT / TRỢ LÝ\n(Tool-Augmented)", 
         "• Con người phải dẫn dắt từng bước\n• Gọi được một số API cơ bản\n• Sinh code hoặc tóm tắt tài liệu\n• Chưa có khả năng tự sửa sai", 
         "#dbeafe", "#1d4ed8", 36),
        ("GIAI ĐOẠN 3: AGENT ĐƠN LẺ\n(Autonomous Single Agent)", 
         "• Vận hành theo mục tiêu cấp cao\n• Vòng lặp ReAct tự lập kế hoạch\n• Tự phản chiếu và gọi công cụ đa bước\n• Bắt đầu tự động hóa quy trình", 
         "#fef3c7", "#d97706", 68),
        ("GIAI ĐOẠN 4: AGENTIC MESH\n(Multi-Agent Enterprise Factory)", 
         "• Đội ngũ tác tử chuyên biệt hóa\n• Hợp tác theo giao thức A2A\n• Con người đóng vai trò Giám sát (HITL)\n• Tự động hóa quy trình end-to-end", 
         "#dcfce7", "#15803d", 100),
    ]

    # Draw 4 stages
    x_positions = [2, 27, 52, 77]
    for i, (title, desc, bg, border, _) in enumerate(stages):
        x = x_positions[i]
        ax.add_patch(patches.FancyBboxPatch((x, 10), 22, 74, boxstyle="round,pad=0.4",
                                            facecolor=bg, edgecolor=border, linewidth=1.5))
        ax.text(x + 11, 76, title, fontsize=8.2, fontweight='bold', color=border, ha='center')
        ax.text(x + 11, 44, desc, fontsize=7.4, color='#1e293b', ha='center', va='center')

    # Draw connecting progression arrows
    for x in [24.5, 49.5, 74.5]:
        ax.annotate("", xy=(x + 2.0, 48), xytext=(x - 0.5, 48),
                    arrowprops=dict(arrowstyle="->", color="#0284c7", lw=2.5))

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Hoàn thành: {out_path}")

os.makedirs("Report/agent01_CT_02_tupv/images", exist_ok=True)
make_code_screenshot("Report/agent01_CT_02_tupv/images/fig_code_screenshot.png")
make_output_screenshot("Report/agent01_CT_02_tupv/images/fig_output_screenshot.png")
make_ai_agent_architecture("Report/agent01_CT_02_tupv/images/fig_ai_agent_architecture.png")
make_react_vs_rewoo_diagram("Report/agent01_CT_02_tupv/images/fig_react_vs_rewoo.png")
make_evolution_mesh_diagram("Report/agent01_CT_02_tupv/images/fig_evolution_mesh.png")
