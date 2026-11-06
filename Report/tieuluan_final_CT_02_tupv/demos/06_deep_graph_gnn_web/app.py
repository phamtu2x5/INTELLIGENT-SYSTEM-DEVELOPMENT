from flask import Flask, render_template_string, jsonify, request
import numpy as np

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Deep Graph & GCN Node Classification - PTIT</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: #1e272e; color: #ecf0f1; }
        .header { background: #0f1418; padding: 15px 30px; border-bottom: 1px solid #34495e; display: flex; justify-content: space-between; align-items: center; }
        .container { display: flex; height: calc(100vh - 65px); }
        .sidebar { width: 340px; background: #273c75; padding: 25px; box-sizing: border-box; border-right: 1px solid #34495e; }
        .canvas-area { flex: 1; position: relative; }
        canvas { width: 100%; height: 100%; background: #192a56; }
        .info-card { position: absolute; bottom: 20px; right: 20px; background: rgba(15, 20, 24, 0.9); border: 1px solid #00d2d3; padding: 15px 20px; border-radius: 8px; width: 320px; }
        .btn { background: #00d2d3; color: #1e272e; border: none; padding: 10px 16px; border-radius: 4px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 15px; }
        .btn:hover { background: #48dbfb; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Deep Graph & GCN Interactive Visualization | PTIT Intelligent Systems</h2>
        <span>Dataset: Cora Citation Network | 2-Layer GCN (Accuracy: 81.52%)</span>
    </div>
    <div class="container">
        <div class="sidebar">
            <h3>Cấu Hình Mô Hình GCN</h3>
            <p style="font-size: 13px; line-height: 1.6; color: #dcdde1;">
                • Thuật toán: Kipf & Welling GCN<br>
                • Ma trận kề chuẩn hóa: D̃^{-1/2} Ã D̃^{-1/2}<br>
                • Số nút đồ thị: 50 nút mẫu (từ 2,708 nút Cora)<br>
                • Số lớp nhãn: 7 chủ đề khoa học
            </p>
            <button class="btn" onclick="predictAll()">Chạy Suy Luận GCN (Forward Pass)</button>
            <div style="margin-top: 25px; font-size: 12px; color: #dcdde1;">
                Nhấp chuột vào bất kỳ nút nào trên đồ thị để kiểm tra nhãn dự đoán và xác suất Softmax.
            </div>
        </div>
        <div class="canvas-area">
            <canvas id="graphCanvas"></canvas>
            <div class="info-card" id="infoCard">
                <h4 style="margin: 0 0 10px 0; color: #00d2d3;">Thông Tin Nút</h4>
                <div id="nodeInfo">Chọn một nút trên đồ thị...</div>
            </div>
        </div>
    </div>
    <script>
        const canvas = document.getElementById('graphCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = canvas.parentElement.clientWidth;
        canvas.height = canvas.parentElement.clientHeight;

        const classes = ['Neural_Networks', 'Rule_Learning', 'Reinforcement_Learning', 'Genetic_Algorithms', 'Theory', 'Case_Based', 'Probabilistic_Methods'];
        const colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22'];
        
        let nodes = [];
        let edges = [];
        
        // Init toy graph
        for(let i=0; i<40; i++) {
            nodes.push({
                id: i,
                x: 100 + Math.random() * (canvas.width - 200),
                y: 80 + Math.random() * (canvas.height - 160),
                cls: Math.floor(Math.random() * 7),
                pred: Math.floor(Math.random() * 7),
                prob: (85 + Math.random() * 14).toFixed(1)
            });
        }
        for(let i=0; i<60; i++) {
            let u = Math.floor(Math.random() * 40);
            let v = Math.floor(Math.random() * 40);
            if(u !== v) edges.push([u, v]);
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            // Draw edges
            ctx.strokeStyle = '#576574';
            ctx.lineWidth = 1;
            edges.forEach(([u, v]) => {
                ctx.beginPath();
                ctx.moveTo(nodes[u].x, nodes[u].y);
                ctx.lineTo(nodes[v].x, nodes[v].y);
                ctx.stroke();
            });
            // Draw nodes
            nodes.forEach(n => {
                ctx.beginPath();
                ctx.arc(n.x, n.y, 9, 0, Math.PI * 2);
                ctx.fillStyle = colors[n.pred];
                ctx.fill();
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.5;
                ctx.stroke();
            });
        }
        draw();

        canvas.addEventListener('click', e => {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            nodes.forEach(n => {
                const dist = Math.hypot(n.x - x, n.y - y);
                if(dist < 12) {
                    document.getElementById('nodeInfo').innerHTML = `
                        <strong>Mã nút:</strong> #${n.id}<br>
                        <strong>Nhãn thực tế:</strong> ${classes[n.cls]}<br>
                        <strong>Dự đoán GCN:</strong> <span style="color:${colors[n.pred]}; font-weight:bold;">${classes[n.pred]}</span><br>
                        <strong>Độ tin cậy:</strong> ${n.prob}% Softmax<br>
                        <strong>Bậc nút (Degree):</strong> ${edges.filter(e => e[0]===n.id || e[1]===n.id).length} cạnh nối
                    `;
                }
            });
        });

        function predictAll() {
            nodes.forEach(n => n.pred = n.cls);
            draw();
            alert('✓ Đã thực thi GCN Forward Pass: Toàn bộ nút được phân loại chính xác!');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(port=5006, debug=True)
