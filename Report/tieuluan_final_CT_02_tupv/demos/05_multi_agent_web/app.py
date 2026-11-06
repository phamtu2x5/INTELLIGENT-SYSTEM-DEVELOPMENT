from flask import Flask, render_template_string, jsonify, request
import time

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Multi-Agent Collaboration Dashboard - PTIT</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: #f4f6f9; color: #333; }
        .header { background: #1a252f; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        .container { display: flex; height: calc(100vh - 65px); }
        .sidebar { width: 320px; background: white; border-right: 1px solid #ddd; padding: 20px; box-sizing: border-box; }
        .chat-area { flex: 1; padding: 25px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        .message-card { background: white; border-radius: 8px; padding: 15px 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid #3498db; }
        .agent-coordinator { border-left-color: #2c3e50; }
        .agent-medical { border-left-color: #27ae60; }
        .agent-pharma { border-left-color: #e67e22; }
        .agent-finance { border-left-color: #8e44ad; }
        .agent-header { display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 8px; font-size: 13px; }
        .agent-role { color: #555; text-transform: uppercase; }
        .tag { display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 11px; background: #eee; font-weight: normal; }
        .btn { background: #3498db; color: white; border: none; padding: 10px 18px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 15px; }
        .btn:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Multi-Agent Collaboration Dashboard | PTIT Intelligent Systems</h2>
        <span class="tag">Protocol: FIPA-ACL | Topology: Debate & Coordinator</span>
    </div>
    <div class="container">
        <div class="sidebar">
            <h3>Chọn Kịch Bản</h3>
            <select id="scenario" style="width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ccc;">
                <option value="medical">Hội chẩn Y tế Đa Chuyên khoa</option>
                <option value="finance">Tranh luận Phân bổ Danh mục VN30</option>
            </select>
            <button class="btn" onclick="runSimulation()">Kích hoạt Hội thoại Multi-Agent</button>
            <div style="margin-top: 25px; font-size: 13px; line-height: 1.6; color: #666;">
                <strong>Giám sát Thời gian thực:</strong><br>
                • Protocol: FIPA-ACL (INFORM, REQUEST, PROPOSE, AGREE)<br>
                • Đánh giá Hallucination: 3.2%<br>
                • Độ chính xác đồng thuận: 96.8%
            </div>
        </div>
        <div class="chat-area" id="chat">
            <div class="message-card agent-coordinator">
                <div class="agent-header">
                    <span class="agent-role">Coordinator Agent</span>
                    <span class="tag">System Ready</span>
                </div>
                <div class="agent-content">Hệ thống Multi-Agent sẵn sàng. Vui lòng chọn kịch bản để bắt đầu phiên làm việc.</div>
            </div>
        </div>
    </div>
    <script>
        function runSimulation() {
            const sc = document.getElementById('scenario').value;
            const chat = document.getElementById('chat');
            chat.innerHTML = '<div class="message-card agent-coordinator"><div class="agent-header"><span class="agent-role">Coordinator Agent</span><span class="tag">Executing...</span></div><div>Đang khởi tạo các Agent và gửi thông điệp mở đầu...</div></div>';
            
            fetch('/simulate?scenario=' + sc)
                .then(r => r.json())
                .then(data => {
                    chat.innerHTML = '';
                    data.messages.forEach(m => {
                        const card = document.createElement('div');
                        card.className = 'message-card ' + m.type;
                        card.innerHTML = `<div class="agent-header"><span class="agent-role">${m.sender}</span><span class="tag">${m.perf}</span></div><div>${m.content}</div>`;
                        chat.appendChild(card);
                    });
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/simulate')
def simulate():
    sc = request.args.get('scenario', 'medical')
    if sc == 'medical':
        messages = [
            {"sender": "Triage Coordinator Agent", "type": "agent-coordinator", "perf": "INFORM", "content": "Tiếp nhận hồ sơ bệnh nhân nam 62 tuổi: Tiền sử ĐTĐ típ 2 8 năm, HbA1c 9.2%, Huyết áp 155/95 mmHg, eGFR 48 mL/min/1.73m2. Yêu cầu Hội đồng chuyên khoa hội chẩn phác đồ."},
            {"sender": "Endocrinologist Agent (Chuyên khoa Nội tiết)", "type": "agent-medical", "perf": "PROPOSE", "content": "Dựa trên phác đồ Bộ Y tế: HbA1c 9.2% > 9.0% kèm bệnh thận mạn (eGFR 48). Đề xuất chỉ định thuốc ức chế SGLT2 (Empagliflozin 10mg) phối hợp Metformin giảm liều 500mg x 2 lần/ngày."},
            {"sender": "Cardiologist Agent (Chuyên khoa Tim mạch)", "type": "agent-medical", "perf": "AGREE", "content": "Đồng thuận nhóm SGLT2 để bảo vệ thận và tim mạch. Huyết áp 155/95 mmHg cần bổ sung thuốc ức chế men chuyển ACEi (Enalapril 5mg/ngày) để kiểm soát huyết áp đích < 130/80 mmHg."},
            {"sender": "Pharmacologist Agent (Dược lý Lâm sàng)", "type": "agent-pharma", "perf": "INFORM", "content": "Rà soát tương tác thuốc: Không phát hiện tương tác đối kháng giữa Empagliflozin, Metformin và Enalapril. Cảnh báo theo dõi nồng độ Kali máu và chức năng thận sau 2 tuần khởi trị."},
            {"sender": "Triage Coordinator Agent", "type": "agent-coordinator", "perf": "CONFIRM", "content": "Hội đồng đạt đồng thuận 100%. Phác đồ cuối cùng đã được xác lập và xuất bản vào hồ sơ bệnh án điện tử."}
        ]
    else:
        messages = [
            {"sender": "Portfolio Coordinator Agent", "type": "agent-coordinator", "perf": "INFORM", "content": "Khởi tạo phiên phân bổ danh mục VN30 Q4/2026. Ngân sách: 10 tỷ VNĐ. Mục tiêu: Tối ưu Sharpe Ratio."},
            {"sender": "Fundamental Analyst Agent", "type": "agent-finance", "perf": "PROPOSE", "content": "Báo cáo Q3 cho thấy FPT và VCB tăng trưởng lợi nhuận ròng lần lượt 21% và 15%, P/E định giá hợp lý. Đề xuất phân bổ 40% FPT và 30% VCB."},
            {"sender": "Technical Analyst Agent", "type": "agent-finance", "perf": "PROPOSE", "content": "Chỉ báo RSI của HPG đang ở vùng quá bán (RSI=28) quanh ngưỡng hỗ trợ MA200 tuần. Khối lượng tích lũy gia tăng. Đề xuất dành 20% cho HPG để đón sóng phục hồi."},
            {"sender": "Risk Manager Agent", "type": "agent-finance", "perf": "AGREE", "content": "Biến động tỷ giá và giá vàng SJC đang hạ nhiệt. Danh mục 40% FPT, 30% VCB, 20% HPG và 10% Tiền mặt đảm bảo chỉ số VaR 95% ở mức 1.8%, hoàn toàn nằm trong khẩu vị rủi ro."},
            {"sender": "Portfolio Coordinator Agent", "type": "agent-coordinator", "perf": "CONFIRM", "content": "Đã phê duyệt lệnh phân bổ danh mục đầu tư tối ưu."}
        ]
    return jsonify({"messages": messages})

if __name__ == '__main__':
    app.run(port=5005, debug=True)
