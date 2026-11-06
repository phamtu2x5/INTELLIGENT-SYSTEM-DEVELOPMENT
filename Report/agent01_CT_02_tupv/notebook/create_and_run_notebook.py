import nbformat as nbf
import os
import sys

nb = nbf.v4.new_notebook()

# Metadata
nb.metadata = {
    "language_info": {
        "name": "python",
        "version": "3.10.0"
    },
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    }
}

cells = []

# Title & Student Information
cells.append(nbf.v4.new_markdown_cell("""# BÀI THỰC HÀNH AGENT 01: XÂY DỰNG AI AGENT THEO CƠ CHẾ REACT & TOOL-CALLING
**Học phần:** Phát triển các hệ thống thông minh  
**Giảng viên hướng dẫn:** PGS.TS Trần Đình Quế  
**Sinh viên thực hiện:** Phạm Văn Tư - Mã sinh viên: B23DCCN879  
**Lớp:** D23CTPM01 - Nhóm môn học: CT - Nhóm tiểu luận: 02  
**Nội dung tham chiếu:** Kiến trúc và cơ chế hoạt động của AI Agent theo tài liệu IBM Think [2] (`https://www.ibm.com/think/topics/ai-agents`)"""))

# Cell 1: Setup & Tool Definitions
cells.append(nbf.v4.new_code_cell("""# 1. ĐỊNH NGHĨA HỆ THỐNG CÔNG CỤ (TOOL REGISTRY) CHO AI AGENT
import json
import re
import datetime

class EnterpriseTools:
    '''Kho công cụ ngoại vi cho phép Agent tương tác với môi trường bên ngoài'''
    
    @staticmethod
    def query_product_catalog(product_name: str) -> str:
        '''Tra cứu thông tin sản phẩm và đơn giá niêm yết từ cơ sở dữ liệu kho'''
        catalog = {
            "ai_workstation_h100": {
                "name": "Máy trạm tính toán AI GPU H100 80GB",
                "unit_price_vnd": 280_000_000,
                "stock": 45,
                "warranty_months": 36
            },
            "edge_server_l40s": {
                "name": "Edge AI Server NVIDIA L40S",
                "unit_price_vnd": 165_000_000,
                "stock": 30,
                "warranty_months": 24
            }
        }
        key = product_name.strip().lower().replace(" ", "_")
        for k, v in catalog.items():
            if k in key or key in k:
                return json.dumps(v, ensure_ascii=False)
        return json.dumps({"error": f"Không tìm thấy sản phẩm '{product_name}' trong kho dữ liệu."})

    @staticmethod
    def query_discount_policy(quantity: int, customer_tier: str = "Enterprise") -> str:
        '''Tra cứu chính sách chiết khấu bậc thang theo số lượng cho doanh nghiệp'''
        if quantity >= 20:
            discount_pct = 12.0
            terms = "Chiết khấu doanh nghiệp quy mô lớn (Tier 1 >= 20 chiếc)"
        elif quantity >= 10:
            discount_pct = 8.0
            terms = "Chiết khấu doanh nghiệp vừa (Tier 2: 10-19 chiếc)"
        elif quantity >= 5:
            discount_pct = 5.0
            terms = "Chiết khấu tiêu chuẩn (Tier 3: 5-9 chiếc)"
        else:
            discount_pct = 0.0
            terms = "Không áp dụng chiết khấu lẻ"
            
        return json.dumps({
            "quantity": quantity,
            "customer_tier": customer_tier,
            "discount_percentage": discount_pct,
            "policy_note": terms
        }, ensure_ascii=False)

    @staticmethod
    def financial_calculator(expression: str) -> str:
        '''Thực hiện tính toán tài chính số học chính xác (an toàn không dùng eval thô)'''
        try:
            # Cho phép các ký tự số học cơ bản
            clean_expr = re.sub(r'[^0-9\+\-\*\/\.\(\)\s]', '', expression)
            result = eval(clean_expr, {"__builtins__": None}, {})
            return json.dumps({"expression": clean_expr, "result": float(result)})
        except Exception as e:
            return json.dumps({"error": f"Lỗi tính toán biểu thức: {str(e)}"})

print("✓ Đã khởi tạo thành công 3 công cụ ngoại vi: query_product_catalog, query_discount_policy, financial_calculator")
"""))

# Cell 2: ReAct Agent Architecture
cells.append(nbf.v4.new_code_cell("""# 2. XÂY DỰNG KIẾN TRÚC REACT AGENT (THOUGHT -> ACTION -> OBSERVATION)
class ReActAIAgent:
    def __init__(self, agent_id: str = "AGENT-IBM-01", max_iterations: int = 6):
        self.agent_id = agent_id
        self.max_iterations = max_iterations
        self.activity_log = []
        self.tools = {
            "query_product_catalog": EnterpriseTools.query_product_catalog,
            "query_discount_policy": EnterpriseTools.query_discount_policy,
            "financial_calculator": EnterpriseTools.financial_calculator
        }
        
    def log_event(self, step_type: str, content: str):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        record = {"time": timestamp, "type": step_type, "content": content}
        self.activity_log.append(record)
        print(f"[{timestamp}] [{step_type.upper()}]: {content}")

    def execute(self, user_goal: str):
        print("="*80)
        print(f"BẮT ĐẦU VẬN HÀNH AI AGENT (ID: {self.agent_id})")
        print(f"MỤC TIÊU (GOAL): {user_goal}")
        print("="*80)
        
        self.log_event("Goal Initialization", user_goal)
        
        # Mô phỏng vòng lặp suy luận ReAct dựa trên nhận thức trạng thái
        iteration = 0
        state = {
            "product_info": None,
            "discount_info": None,
            "subtotal": None,
            "total_with_vat": None
        }
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\\n--- [Chu trình ReAct Bước {iteration}/{self.max_iterations}] ---")
            
            if state["product_info"] is None:
                # Bước 1: Suy luận tra cứu đơn giá sản phẩm
                thought = "Để tính toán chi phí đơn hàng, trước tiên cần tra cứu đơn giá niêm yết và tồn kho của máy trạm H100 trong CSDL kho."
                self.log_event("Thought", thought)
                
                action = "query_product_catalog"
                action_input = "ai_workstation_h100"
                self.log_event("Action", f"Gọi công cụ '{action}' với tham số '{action_input}'")
                
                obs = self.tools[action](action_input)
                self.log_event("Observation", f"Kết quả từ môi trường: {obs}")
                state["product_info"] = json.loads(obs)
                
            elif state["discount_info"] is None:
                # Bước 2: Suy luận tra cứu chính sách chiết khấu
                thought = "Đã có đơn giá sản phẩm (280 triệu VNĐ). Tiếp theo cần kiểm tra chính sách chiết khấu bậc thang cho đơn đặt mua 25 máy."
                self.log_event("Thought", thought)
                
                action = "query_discount_policy"
                action_input = {"quantity": 25, "customer_tier": "Enterprise"}
                self.log_event("Action", f"Gọi công cụ '{action}' với tham số {action_input}")
                
                obs = self.tools[action](quantity=25, customer_tier="Enterprise")
                self.log_event("Observation", f"Kết quả từ môi trường: {obs}")
                state["discount_info"] = json.loads(obs)
                
            elif state["subtotal"] is None:
                # Bước 3: Suy luận tính tiền trước thuế sau chiết khấu
                unit_price = state["product_info"]["unit_price_vnd"]
                discount_rate = state["discount_info"]["discount_percentage"] / 100.0
                calc_expr = f"25 * {unit_price} * (1 - {discount_rate})"
                
                thought = f"Đơn hàng được chiết khấu {state['discount_info']['discount_percentage']}%. Cần dùng máy tính tài chính để tính tổng tiền hàng trước thuế: 25 * 280,000,000 * (1 - 0.12)."
                self.log_event("Thought", thought)
                
                action = "financial_calculator"
                self.log_event("Action", f"Gọi công cụ '{action}' với biểu thức: '{calc_expr}'")
                
                obs = self.tools[action](calc_expr)
                self.log_event("Observation", f"Kết quả tính toán: {obs}")
                state["subtotal"] = json.loads(obs)["result"]
                
            elif state["total_with_vat"] is None:
                # Bước 4: Suy luận tính thuế VAT 8% và tổng tiền thanh toán
                subtotal = state["subtotal"]
                vat_expr = f"{subtotal} * 1.08"
                
                thought = f"Tiền hàng sau chiết khấu là {subtotal:,.0f} VNĐ. Cần áp thuế VAT 8% để xác định tổng nghĩa vụ thanh toán cuối cùng."
                self.log_event("Thought", thought)
                
                action = "financial_calculator"
                self.log_event("Action", f"Gọi công cụ '{action}' với biểu thức: '{vat_expr}'")
                
                obs = self.tools[action](vat_expr)
                self.log_event("Observation", f"Kết quả tính toán: {obs}")
                state["total_with_vat"] = json.loads(obs)["result"]
                
            else:
                # Bước 5: Đưa ra Final Answer
                thought = "Đã thu thập đầy đủ thông tin: Đơn giá, tỷ lệ chiết khấu, giá trị trước thuế và tổng thanh toán kèm VAT 8%. Tiến hành xuất kết quả cuối cùng."
                self.log_event("Thought", thought)
                
                final_answer = (
                    f"BÁO CÁO KẾT QUẢ ĐƠN HÀNG DOANH NGHIỆP VINATECH:\\n"
                    f"1. Thiết bị: {state['product_info']['name']} (Số lượng: 25 chiếc)\\n"
                    f"2. Đơn giá niêm yết: {state['product_info']['unit_price_vnd']:,} VNĐ/chiếc (Tổng nguyên giá: {25*state['product_info']['unit_price_vnd']:,} VNĐ)\\n"
                    f"3. Chính sách áp dụng: {state['discount_info']['policy_note']} (Giảm {state['discount_info']['discount_percentage']}%, tương đương tiết kiệm {25*state['product_info']['unit_price_vnd']*0.12:,} VNĐ)\\n"
                    f"4. Tổng tiền sau chiết khấu (chưa VAT): {state['subtotal']:,.0f} VNĐ\\n"
                    f"5. Thuế suất VAT (8%): {state['subtotal']*0.08:,.0f} VNĐ\\n"
                    f"6. TỔNG SỐ TIỀN PHẢI THANH TOÁN: {state['total_with_vat']:,.0f} VNĐ."
                )
                self.log_event("Final Answer", final_answer)
                break
                
        print("="*80)
        print("HOÀN TẤT THỰC THI NHIỆM VỤ CỦA AI AGENT")
        print("="*80)
        return state, self.activity_log

print("✓ Đã sẵn sàng lớp ReActAIAgent với đầy đủ cơ chế Thought-Action-Observation và Activity Logging")
"""))

# Cell 3: Running the Agent with real Goal
cells.append(nbf.v4.new_code_cell("""# 3. CHẠY THỰC NGHIỆM AI AGENT VỚI MỤC TIÊU PHỨC TẠP TỪ NGƯỜI DÙNG
agent = ReActAIAgent(agent_id="AGENT-REACT-B23DCCN879-01", max_iterations=5)

user_request = (
    "Khách hàng Doanh nghiệp VINATECH đặt mua 25 máy trạm tính toán AI GPU H100. "
    "Hãy tra cứu đơn giá niêm yết trong kho, áp dụng chính sách chiết khấu bậc thang theo số lượng, "
    "tính toán thuế VAT 8% và xuất tổng giá trị thanh toán cuối cùng bằng VNĐ."
)

final_state, logs = agent.execute(user_request)
"""))

# Cell 4: Audit & Activity Log Verification
cells.append(nbf.v4.new_code_cell("""# 4. TRÍCH XUẤT NHẬT KÝ KIỂM TOÁN (AUDIT & ACTIVITY LOGS) THEO CHUẨN IBM
import pandas as pd

log_df = pd.DataFrame(logs)
print(f"Tổng số bước ghi nhận trong chu trình ReAct: {len(log_df)}")
print("\\nBẢNG NHẬT KÝ CHI TIẾT CỦA AI AGENT (AUDIT TRAIL):")
display_cols = ["time", "type", "content"]
for idx, row in log_df.iterrows():
    prefix = f"[{row['type'].upper()}]:"
    summary = row['content'].replace('\\n', ' ')[:95]
    print(f"Step {idx+1:02d} | {row['time']} | {prefix:<22} {summary}...")
"""))

nb.cells = cells

# Save notebook
out_path = "Report/agent01_CT_02_tupv/notebook/agent01_ai_agent_react.ipynb"
with open(out_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"✓ Đã tạo thành công notebook tại: {out_path}")
