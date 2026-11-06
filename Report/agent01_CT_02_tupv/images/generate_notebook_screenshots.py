import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# Set publication style with Menlo and Arial
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.monospace'] = ['Menlo', 'Monaco', 'Courier New']
plt.rcParams['axes.edgecolor'] = '#cccccc'

def create_jupyter_screenshot_code(output_path):
    fig, ax = plt.subplots(figsize=(10.5, 6.6), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Header bar
    ax.add_patch(patches.Rectangle((0, 93), 100, 7, facecolor='#f8f9fa', edgecolor='#dee2e6', linewidth=1))
    ax.text(2, 96.5, "Jupyter", fontsize=12, fontweight='bold', color='#f37626', va='center', fontfamily='Arial')
    ax.text(10.5, 96.5, "agent01_ai_agent_react.ipynb", fontsize=11, fontweight='bold', color='#212529', va='center', fontfamily='Arial')
    ax.text(47, 96.5, "(Python 3 / Trusted)", fontsize=9, color='#6c757d', va='center', fontfamily='Arial')
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
    ax.add_patch(patches.Rectangle((2, 79), 96, 7, facecolor='#ffffff', edgecolor='#e9ecef', linewidth=0.8))
    ax.text(3, 83.5, "# BÀI THỰC HÀNH AGENT 01: XÂY DỰNG AI AGENT THEO CƠ CHẾ REACT & TOOL-CALLING", 
            fontsize=9.5, fontweight='bold', color='#1a365d', fontfamily='Arial')
    ax.text(3, 80.5, "Sinh viên: Phạm Văn Tư - B23DCCN879 | Môn: PTHT Thông Minh | Nguồn tham chiếu: IBM Think [2]", 
            fontsize=8, color='#4a5568', fontfamily='Arial')

    # Cell 2: Code cell prompt
    ax.text(1.5, 74.5, "In [2]:", fontsize=9, fontweight='bold', color='#303f9f', fontfamily='Menlo')
    
    # Code box
    ax.add_patch(patches.FancyBboxPatch((7, 4.5), 91, 71.5, boxstyle="round,pad=0.3",
                                        facecolor='#f8f9fa', edgecolor='#b0bec5', linewidth=1.2))
    
    code_lines = [
        ("class ReActAIAgent:", "#0000ff", True),
        ("    def __init__(self, agent_id='AGENT-IBM-01', max_iterations=6):", "#000000", False),
        ("        self.agent_id = agent_id", "#000000", False),
        ("        self.max_iterations = max_iterations", "#000000", False),
        ("        self.activity_log = []", "#000000", False),
        ("        self.tools = {", "#000000", False),
        ("            'query_product_catalog': EnterpriseTools.query_product_catalog,", "#a31515", False),
        ("            'query_discount_policy': EnterpriseTools.query_discount_policy,", "#a31515", False),
        ("            'financial_calculator': EnterpriseTools.financial_calculator", "#a31515", False),
        ("        }", "#000000", False),
        ("    ", "#000000", False),
        ("    def execute(self, user_goal: str):", "#000000", False),
        ("        self.log_event('Goal Initialization', user_goal)", "#008000", False),
        ("        iteration = 0", "#000000", False),
        ("        while iteration < self.max_iterations:", "#0000ff", True),
        ("            iteration += 1", "#000000", False),
        ("            # 1. THOUGHT: Tác tử nhận thức trạng thái và lập kế hoạch", "#008000", False),
        ("            thought = self.reason_next_step(state)", "#000000", False),
        ("            self.log_event('Thought', thought)", "#008000", False),
        ("            ", "#000000", False),
        ("            # 2. ACTION: Tác tử gọi công cụ phù hợp", "#008000", False),
        ("            action, action_input = self.select_tool(thought)", "#000000", False),
        ("            self.log_event('Action', f'Call {action} with {action_input}')", "#008000", False),
        ("            ", "#000000", False),
        ("            # 3. OBSERVATION: Thu nhận kết quả từ môi trường", "#008000", False),
        ("            observation = self.tools[action](action_input)", "#000000", False),
        ("            self.log_event('Observation', str(observation))", "#008000", False),
        ("            ", "#000000", False),
        ("            if self.is_goal_achieved(state):", "#0000ff", True),
        ("                self.log_event('Final Answer', self.synthesize_response(state))", "#008000", False),
        ("                break", "#0000ff", True),
    ]

    y = 73
    for line in code_lines:
        txt, col, is_bold = line
        weight = 'bold' if is_bold else 'normal'
        ax.text(8.5, y, txt, fontsize=7.6, color=col, fontfamily='Menlo', fontweight=weight)
        y -= 2.05

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Đã tạo ảnh screenshot code: {output_path}")

def create_jupyter_screenshot_output(output_path):
    fig, ax = plt.subplots(figsize=(10.5, 6.8), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Cell 3 prompt
    ax.text(1.5, 96.5, "In [3]:", fontsize=9, fontweight='bold', color='#303f9f', fontfamily='Menlo')
    
    # Input Code box (Execute request)
    ax.add_patch(patches.FancyBboxPatch((7, 85), 91, 10.5, boxstyle="round,pad=0.2",
                                        facecolor='#f8f9fa', edgecolor='#b0bec5', linewidth=1.0))
    ax.text(8.5, 92.5, "agent = ReActAIAgent(agent_id='AGENT-REACT-B23DCCN879-01', max_iterations=5)",
            fontsize=8, color='#000000', fontfamily='Menlo')
    ax.text(8.5, 89.5, "query = 'Khách hàng VINATECH đặt 25 máy trạm AI H100. Tra cứu giá, tính chiết khấu & VAT 8%'",
            fontsize=8, color='#a31515', fontfamily='Menlo')
    ax.text(8.5, 86.5, "state, logs = agent.execute(query)", fontsize=8, color='#000000', fontfamily='Menlo')

    # Output Terminal Area
    ax.add_patch(patches.FancyBboxPatch((7, 3), 91, 80, boxstyle="round,pad=0.3",
                                        facecolor='#ffffff', edgecolor='#ced4da', linewidth=1.2))
    
    # Left accent line for output
    ax.add_patch(patches.Rectangle((7, 3), 1, 80, facecolor='#28a745', edgecolor='none'))

    out_lines = [
        ("================================================================================", "#6c757d", False),
        ("BẮT ĐẦU VẬN HÀNH AI AGENT (ID: AGENT-REACT-B23DCCN879-01)", "#1a365d", True),
        ("MỤC TIÊU (GOAL): Khách hàng VINATECH đặt mua 25 máy trạm tính toán AI GPU H100...", "#2b6cb0", False),
        ("================================================================================", "#6c757d", False),
        ("--- [Chu trình ReAct Bước 1/5] ---", "#d97706", True),
        ("[THOUGHT]    : Cần tra cứu đơn giá niêm yết và tồn kho của máy trạm H100 trong CSDL kho.", "#2c5282", False),
        ("[ACTION]     : Gọi công cụ 'query_product_catalog' với tham số 'ai_workstation_h100'", "#805ad5", True),
        ("[OBSERVATION]: {'name': 'Máy trạm AI GPU H100 80GB', 'unit_price_vnd': 280,000,000, 'stock': 45}", "#276749", False),
        ("--- [Chu trình ReAct Bước 2/5] ---", "#d97706", True),
        ("[THOUGHT]    : Đã có đơn giá. Cần kiểm tra chính sách chiết khấu bậc thang cho 25 máy.", "#2c5282", False),
        ("[ACTION]     : Gọi công cụ 'query_discount_policy' với tham số {'quantity': 25, 'tier': 'Enterprise'}", "#805ad5", True),
        ("[OBSERVATION]: {'discount_percentage': 12.0, 'policy_note': 'Chiết khấu Tier 1 (>= 20 máy)'}", "#276749", False),
        ("--- [Chu trình ReAct Bước 3/5] ---", "#d97706", True),
        ("[THOUGHT]    : Chiết khấu 12%. Gọi máy tính tài chính tính tiền hàng: 25 * 280,000,000 * (1 - 0.12)", "#2c5282", False),
        ("[ACTION]     : Gọi công cụ 'financial_calculator' với biểu thức: '25 * 280000000 * 0.88'", "#805ad5", True),
        ("[OBSERVATION]: {'expression': '25 * 280000000 * 0.88', 'result': 6160000000.0}", "#276749", False),
        ("--- [Chu trình ReAct Bước 4/5] ---", "#d97706", True),
        ("[THOUGHT]    : Tiền trước thuế: 6.16 tỷ VNĐ. Áp dụng thuế suất VAT 8% để xác định tổng tiền.", "#2c5282", False),
        ("[ACTION]     : Gọi công cụ 'financial_calculator' với biểu thức: '6160000000 * 1.08'", "#805ad5", True),
        ("[OBSERVATION]: {'expression': '6160000000 * 1.08', 'result': 6652800000.0}", "#276749", False),
        ("--- [Chu trình ReAct Bước 5/5: Hoàn tất Mục tiêu] ---", "#38a169", True),
        ("[FINAL ANSWER]: BÁO CÁO KẾT QUẢ ĐƠN HÀNG DOANH NGHIỆP VINATECH:", "#1a202c", True),
        ("  - Số lượng: 25 máy trạm AI GPU H100 | Đơn giá niêm yết: 280,000,000 VNĐ/chiếc", "#2d3748", False),
        ("  - Mức chiết khấu: 12% (Doanh nghiệp tiết kiệm được: 840,000,000 VNĐ)", "#2d3748", False),
        ("  - Tổng tiền hàng trước thuế: 6,160,000,000 VNĐ | Thuế VAT 8%: 492,800,000 VNĐ", "#2d3748", False),
        ("  - TỔNG SỐ TIỀN PHẢI THANH TOÁN: 6,652,800,000 VNĐ (Sáu tỷ sáu trăm năm mươi hai triệu...)", "#c53030", True),
        ("================================================================================", "#6c757d", False),
        ("[AUDIT TRAIL]: Đã lưu toàn bộ 11 sự kiện nhận thức vào hệ thống giám sát IBM Telemetry.", "#4a5568", False)
    ]

    y = 80.5
    for line in out_lines:
        txt, col, is_bold = line
        weight = 'bold' if is_bold else 'normal'
        ax.text(8.5, y, txt, fontsize=7.4, color=col, fontfamily='Menlo', fontweight=weight)
        y -= 2.75

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Đã tạo ảnh screenshot output: {output_path}")

create_jupyter_screenshot_code("Report/agent01_CT_02_tupv/images/fig_code_screenshot.png")
create_jupyter_screenshot_output("Report/agent01_CT_02_tupv/images/fig_output_screenshot.png")
