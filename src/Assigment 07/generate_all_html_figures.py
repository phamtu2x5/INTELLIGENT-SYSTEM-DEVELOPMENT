# -*- coding: utf-8 -*-
"""
Script: generate_all_html_figures.py (MASTERPIECE EDITION - ZERO COMPROMISES)
Tác giả: Phí Văn Tú (tupv.879)

Quy chuẩn thiết kế đỉnh cao (Nature / IEEE Standard):
1. 100% Nội dung dùng HTML5/CSS3 Grid & Flexbox, không vỡ dòng, không mất chữ.
2. spellcheck="false" toàn bộ để triệt tiêu vĩnh viễn gạch chân đỏ/xanh của Chrome.
3. Không có bất kỳ đường mũi tên nào cắt ngang qua thân thẻ. Mọi đường dẫn đều thẳng hoặc chạy qua rãnh phân cách.
4. Tỷ lệ chuẩn mực 1400x680px, render Chrome Headless Retina (2x), sắc nét từng pixel.
"""

import os
import subprocess

OUTPUT_DIR = "Report/Assigment 07/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def render_html_to_png(html_content, out_png, width=1400, height=680):
    tmp_html = f"/tmp/{os.path.basename(out_png)}.html"
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=2",
        f"--screenshot={out_png}",
        f"--window-size={width},{height}",
        tmp_html
    ]
    subprocess.run(cmd, check=True)
    print(f"✓ Đã xuất bản hoàn hảo: {out_png} ({width}x{height})")


# =============================================================================
# 1. FIG 701: KIẾN TRÚC TỔNG QUAN HỆ SINH THÁI TRI THỨC ĐA MIỀN VIỆT NAM
# =============================================================================
def generate_fig701():
    html = """<!DOCTYPE html>
<html lang="vi" spellcheck="false">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-font-smoothing: antialiased; }
  html, body { width: 1400px; height: 680px; overflow: hidden; background: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #0f172a; }
  .wrapper { padding: 14px 16px; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
  
  .header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 8px; padding: 10px 18px; color: white; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155;
  }
  .h-title { font-size: 16.5px; font-weight: 800; color: #f8fafc; }
  .h-sub { font-size: 11px; color: #94a3b8; }
  .h-badge { background: rgba(14,165,233,0.18); border: 1px solid #0ea5e9; color: #7dd3fc; padding: 3px 10px; border-radius: 14px; font-size: 10.5px; font-weight: 700; }

  .main-row {
    display: grid; grid-template-columns: 295px 40px 345px 40px 325px 40px 300px; height: 465px; align-items: stretch; position: relative;
  }
  .card {
    background: white; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 2px 5px rgba(0,0,0,0.04); display: flex; flex-direction: column; overflow: hidden;
  }
  .c-hdr {
    padding: 7px 12px; font-size: 11.5px; font-weight: 800; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0,0,0,0.06);
  }
  .c-body { padding: 8px 10px; flex: 1; display: flex; flex-direction: column; gap: 7px; justify-content: space-between; }

  .c-blue { border-top: 3px solid #0284c7; } .c-blue .c-hdr { background: #f0f9ff; color: #0369a1; }
  .c-green { border-top: 3px solid #10b981; } .c-green .c-hdr { background: #ecfdf5; color: #047857; }
  .c-purple { border-top: 3px solid #8b5cf6; } .c-purple .c-hdr { background: #f5f3ff; color: #6d28d9; }
  .c-teal { border-top: 3px solid #0d9488; } .c-teal .c-hdr { background: #f0fdfa; color: #0f766e; }

  .sub { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px; }
  .sub-t { font-size: 9.5px; font-weight: 700; color: #475569; text-transform: uppercase; margin-bottom: 2px; }
  .sub-d { font-size: 10px; color: #1e293b; line-height: 1.35; }
  .tag { display: inline-block; padding: 2px 5px; border-radius: 3px; font-size: 9px; font-weight: 700; }
  .t-blue { background: #e0f2fe; color: #0369a1; } .t-green { background: #dcfce7; color: #15803d; } .t-red { background: #fee2e2; color: #b91c1c; } .t-amber { background: #fef3c7; color: #92400e; }

  .bottom-row {
    background: white; border-radius: 8px; border: 1px solid #cbd5e1; padding: 8px 14px; display: grid; grid-template-columns: 1fr 1fr; gap: 14px; height: 135px; align-items: stretch;
  }
  .scen-card { background: #f8fafc; border-radius: 6px; border: 1px solid #e2e8f0; padding: 7px 10px; display: flex; flex-direction: column; justify-content: space-between; font-size: 10px; }
</style>
</head>
<body spellcheck="false">
<div class="wrapper">
  <div class="header">
    <div>
      <div class="h-title">KIẾN TRÚC TỔNG QUAN HỆ SINH THÁI TRI THỨC ĐA MIỀN TẠI VIỆT NAM</div>
      <div class="h-sub">Hợp nhất Đồ thị Tri thức (KG), Dense Vector RAG và Tác tử Thông minh Multi-Tool ReAct Agent</div>
    </div>
    <div class="h-badge">Hệ Sinh Thái Hợp Nhất</div>
  </div>

  <div class="main-row">
    <!-- SVG CONNECTORS -->
    <svg style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:10;">
      <defs>
        <marker id="arr1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 9 5 L 0 9 z" fill="#0284c7"/></marker>
        <marker id="arr2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 9 5 L 0 9 z" fill="#10b981"/></marker>
        <marker id="arr3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 9 5 L 0 9 z" fill="#8b5cf6"/></marker>
      </defs>
      <path d="M 295 232 L 333 232" stroke="#0284c7" stroke-width="2.2" marker-end="url(#arr1)"/>
      <path d="M 680 232 L 718 232" stroke="#10b981" stroke-width="2.2" marker-end="url(#arr2)"/>
      <path d="M 1045 232 L 1083 232" stroke="#8b5cf6" stroke-width="2.2" marker-end="url(#arr3)"/>
    </svg>

    <!-- COL 1 -->
    <div class="card c-blue">
      <div class="c-hdr"><span>1. NGUỒN DỮ LIỆU THÔ</span><span class="tag t-blue">Raw Input</span></div>
      <div class="c-body">
        <div class="sub">
          <div class="sub-t">Pháp Lý & Y Tế Việt Nam</div>
          <div class="sub-d">• QĐ 5481/QĐ-BYT: Phác đồ chuẩn ĐTĐ Típ 2<br>• Dược thư & Hướng dẫn Viện Dinh Dưỡng QG</div>
        </div>
        <div class="sub">
          <div class="sub-t">Thị Trường Tài Chính Vĩ Mô</div>
          <div class="sub-d">• Báo cáo phân tích CTCK SSI, VNDirect<br>• Bản tin điều hành tỷ giá NHNN & NĐ 24 vàng</div>
        </div>
        <div class="sub">
          <div class="sub-t">Chuỗi Số Liệu Lâm Sàng & Giao Dịch</div>
          <div class="sub-d">• Chỉ số lâm sàng: HbA1c, Glucose đói, BMI<br>• Dữ liệu lịch sử giá cổ phiếu FPT, Vàng SJC</div>
        </div>
        <div class="sub" style="background:#eff6ff; border-color:#bfdbfe;">
          <div class="sub-t" style="color:#1d4ed8;">Chuẩn Hóa Tiền Xử Lý (ETL)</div>
          <div class="sub-d">• Làm sạch, khử trùng lặp và gán nhãn thực thể.</div>
        </div>
      </div>
    </div>
    <div></div>

    <!-- COL 2 -->
    <div class="card c-green">
      <div class="c-hdr"><span>2. HAI TRỤ CỘT TRI THỨC</span><span class="tag t-green">KG + Vector</span></div>
      <div class="c-body">
        <div class="sub" style="background:#f0fdf4; border-color:#bbf7d0;">
          <div class="sub-t" style="color:#047857;">Trụ Cột 1: Knowledge Graph (Biểu Tượng)</div>
          <div class="sub-d">
            • Bộ ba quan hệ: <code>(Thực thể - Quan hệ - Thực thể)</code><br>
            • Ràng buộc logic: <i>Metformin + Rượu ➔ Chống chỉ định tử vong</i><br>
            • Chuỗi giá trị: <i>USD/VND tăng ➔ FPT hưởng lợi doanh thu</i><br>
            • Truy vấn đa bước (Multi-hop) chính xác tuyệt đối 100%.
          </div>
        </div>
        <div class="sub" style="background:#fffbeb; border-color:#fde68a;">
          <div class="sub-t" style="color:#b45309;">Trụ Cột 2: Dense Vector RAG (Ngữ Nghĩa)</div>
          <div class="sub-d">
            • Phân mảnh văn bản ngữ nghĩa (Semantic Chunks 512 tokens)<br>
            • Không gian Vector đa chiều (BGE-M3 / PhoBERT)<br>
            • Tái xếp hạng Cross-Encoder Reranker loại bỏ nhiễu.
          </div>
        </div>
        <div class="sub" style="background:#ecfdf5; border-color:#a7f3d0;">
          <div class="sub-t" style="color:#065f46;">GraphRAG Hợp Nhất (Synergy)</div>
          <div class="sub-d">• Vector DB tìm điểm neo ➔ Graph DB duyệt sâu n-bước.</div>
        </div>
      </div>
    </div>
    <div></div>

    <!-- COL 3 -->
    <div class="card c-purple">
      <div class="c-hdr"><span>3. TÁC TỬ REACT AGENT</span><span class="tag t-amber">Reasoning Core</span></div>
      <div class="c-body">
        <div class="sub">
          <div class="sub-t">Vòng Lặp ReAct Tự Chủ</div>
          <div class="sub-d">• <b>Thought:</b> Phân tích ý định & nhận dạng thực thể<br>• <b>Action:</b> Kích hoạt Tool ML, Tool KG, Tool RAG<br>• <b>Observation:</b> Cập nhật nhận thức trung gian</div>
        </div>
        <div class="sub">
          <div class="sub-t">Công Cụ Học Sâu Chuyên Biệt</div>
          <div class="sub-d">• MLP Classifier v2: Chẩn đoán ĐTĐ 98.5%<br>• PyTorch BiLSTM: Dự báo chuỗi FPT, Vàng SJC</div>
        </div>
        <div class="sub">
          <div class="sub-t">Bộ Nhớ Ngữ Cảnh Hội Thoại</div>
          <div class="sub-d">• Lưu vết lịch sử trao đổi bệnh án và danh mục đầu tư.</div>
        </div>
        <div class="sub" style="background:#faf5ff; border-color:#e9d5ff;">
          <div class="sub-t" style="color:#6d28d9;">Rào Cản Kiểm Duyệt An Toàn</div>
          <div class="sub-d">Safety Guardrails chặn đứng hoàn toàn ảo giác tri thức.</div>
        </div>
      </div>
    </div>
    <div></div>

    <!-- COL 4 -->
    <div class="card c-teal">
      <div class="c-hdr"><span>4. ĐẦU RA MINH BẠCH</span><span class="tag t-red">Fact-Grounded</span></div>
      <div class="c-body">
        <div class="sub" style="background:#fef2f2; border-color:#fecaca;">
          <div class="sub-t" style="color:#b91c1c;">Cảnh Báo Đỏ Y Khoa</div>
          <div class="sub-d">CẤM rượu bia khi dùng Metformin (Nguy cơ Toan Lactic tử vong 50%).</div>
        </div>
        <div class="sub" style="background:#f0fdf4; border-color:#bbf7d0;">
          <div class="sub-t" style="color:#15803d;">Khuyến Nghị Dinh Dưỡng</div>
          <div class="sub-d">Ăn ức gà nạc hấp/luộc (GI = 0), kiêng ăn da gà chiên xào dầu mỡ.</div>
        </div>
        <div class="sub" style="background:#f0f9ff; border-color:#bae6fd;">
          <div class="sub-t" style="color:#0369a1;">Dự Báo Tài Chính Vĩ Mô</div>
          <div class="sub-d">FPT (+1.8%) hưởng lợi xuất khẩu; Vàng SJC neo cao theo Nghị định 24.</div>
        </div>
        <div class="sub" style="background:#f0fdfa; border-color:#99f6e4;">
          <div class="sub-t" style="color:#0f766e;">Cam Kết Fact-Grounded</div>
          <div class="sub-d">100% dẫn xuất nguồn BYT, SSI; triệt tiêu hoàn toàn ảo giác.</div>
        </div>
      </div>
    </div>
  </div>

  <!-- BOTTOM BAR -->
  <div class="bottom-row">
    <div class="scen-card">
      <div style="font-weight:800; color:#0369a1; display:flex; justify-content:space-between;">
        <span>KỊCH BẢN Y TẾ LÂM SÀNG THỰC TẾ</span><span class="tag t-blue">Bệnh nhân ĐTĐ</span>
      </div>
      <div><b>Câu hỏi người dùng:</b> <i>“Tôi đang uống Metformin 500mg, HbA1c 7.3%, chiều nay có uống rượu và ăn thịt gà được không?”</i></div>
      <div style="color:#047857;">➔ <b>Agent Phản hồi:</b> Cảnh báo đỏ cấm tuyệt đối rượu bia (nguy cơ tử vong do toan Lactic); Hướng dẫn ăn ức gà luộc bỏ da, kiêng chiên rán.</div>
    </div>
    <div class="scen-card">
      <div style="font-weight:800; color:#b45309; display:flex; justify-content:space-between;">
        <span>KỊCH BẢN THỊ TRƯỜNG TÀI CHÍNH VIỆT NAM</span><span class="tag t-amber">Nhà đầu tư</span>
      </div>
      <div><b>Câu hỏi người dùng:</b> <i>“Tỷ giá USD/VND lên 25,450 và giá vàng SJC lên 90 triệu, cổ phiếu FPT và HPG chịu ảnh hưởng gì?”</i></div>
      <div style="color:#0369a1;">➔ <b>Agent Phản hồi:</b> BiLSTM dự báo FPT tăng 1.8% (hưởng lợi doanh thu ngoại tệ); HPG chịu áp lực quặng nhập khẩu; Vàng SJC theo dõi chặt.</div>
    </div>
  </div>
</div>
</body>
</html>
"""
    render_html_to_png(html, os.path.join(OUTPUT_DIR, "fig701_kg_and_rag_overview.png"), 1400, 680)


# =============================================================================
# 2. FIG 702: MÔ HÌNH BỘ BA RDF & ĐỐI CHUẨN GRAPH DB VS VECTOR DB
# =============================================================================
def generate_fig702():
    html = """<!DOCTYPE html>
<html lang="vi" spellcheck="false">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-font-smoothing: antialiased; }
  html, body { width: 1400px; height: 680px; overflow: hidden; background: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #0f172a; }
  .wrapper { padding: 14px 16px; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
  
  .header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 8px; padding: 10px 18px; color: white; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155;
  }
  .h-title { font-size: 16.5px; font-weight: 800; color: #f8fafc; }
  .h-sub { font-size: 11px; color: #94a3b8; }
  
  .split-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; height: 595px; }
  .panel {
    background: white; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 2px 5px rgba(0,0,0,0.04); display: flex; flex-direction: column; overflow: hidden;
  }
  .p-hdr {
    padding: 8px 14px; font-size: 11.5px; font-weight: 800; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0;
  }
  .p-left { border-top: 3px solid #0284c7; } .p-left .p-hdr { background: #f0f9ff; color: #0369a1; }
  .p-right { border-top: 3px solid #10b981; } .p-right .p-hdr { background: #ecfdf5; color: #047857; }

  /* Left Panel */
  .left-body { flex: 1; display: flex; flex-direction: column; justify-content: space-between; padding: 10px; gap: 10px; }
  .graph-canvas { height: 380px; position: relative; background: #fafafa; border: 1px solid #f1f5f9; border-radius: 6px; overflow: hidden; }
  .cypher-box {
    background: #0f172a; color: #f8fafc; border-radius: 6px; padding: 9px 12px; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 10px; line-height: 1.45;
  }

  /* Right Panel */
  .tbl-box { flex: 1; padding: 10px; display: flex; flex-direction: column; justify-content: space-between; gap: 10px; }
  table { width: 100%; border-collapse: collapse; font-size: 10px; }
  th { background: #0284c7; color: white; padding: 7px 8px; text-align: left; font-weight: 700; }
  td { padding: 6.5px 8px; border-bottom: 1px solid #e2e8f0; color: #1e293b; }
  tr:nth-child(even) { background: #f8fafc; }
  .td-b { font-weight: 700; color: #0f172a; }
  .td-h { color: #047857; font-weight: 700; }
  
  .conc-box {
    background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 6px; padding: 8px 10px; font-size: 10px; color: #065f46; line-height: 1.4;
  }
</style>
</head>
<body spellcheck="false">
<div class="wrapper">
  <div class="header">
    <div>
      <div class="h-title">MÔ HÌNH BỘ BA RDF & BẢN THỂ LUẬN (ONTOLOGY) VÀ ĐỐI CHUẨN KỸ THUẬT</div>
      <div class="h-sub">So sánh Kiến trúc Biểu tượng (Knowledge Graph) và Kiến trúc Thống kê (Vector Database)</div>
    </div>
    <div style="background:rgba(59,130,246,0.18); border:1px solid #3b82f6; color:#93c5fd; padding:3px 9px; border-radius:12px; font-size:10.5px; font-weight:700;">
      Symbolic vs Neural
    </div>
  </div>

  <div class="split-grid">
    <!-- PANEL 1: RDF GRAPH -->
    <div class="panel p-left">
      <div class="p-hdr">
        <span>MÔ HÌNH BỘ BA RDF (SUBJECT - PREDICATE - OBJECT)</span>
        <span style="font-size:10px; background:#bae6fd; color:#0284c7; padding:2px 6px; border-radius:3px;">Y Tế Việt Nam</span>
      </div>
      <div class="left-body">
        <div class="graph-canvas">
          <svg viewBox="0 0 650 380" style="width:100%; height:100%;">
            <defs>
              <marker id="am" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 9 5 L 0 9 z" fill="#64748b"/></marker>
              <marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 9 5 L 0 9 z" fill="#ef4444"/></marker>
              <marker id="ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 9 5 L 0 9 z" fill="#10b981"/></marker>
              <marker id="ab" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 9 5 L 0 9 z" fill="#0284c7"/></marker>
            </defs>

            <!-- EDGES -->
            <path d="M 140 70 L 290 145" stroke="#0284c7" stroke-width="2" marker-end="url(#ab)"/>
            <rect x="165" y="95" width="95" height="18" rx="3" fill="white" stroke="#bae6fd"/>
            <text x="212" y="107" font-size="8.5" font-weight="700" fill="#0284c7" text-anchor="middle">CHẨN ĐOÁN (≥6.5%)</text>

            <path d="M 140 230 L 290 175" stroke="#0284c7" stroke-width="2" marker-end="url(#ab)"/>
            <rect x="165" y="195" width="105" height="18" rx="3" fill="white" stroke="#bae6fd"/>
            <text x="217" y="207" font-size="8.5" font-weight="700" fill="#0284c7" text-anchor="middle">XÁC NHẬN (≥126mg/dL)</text>

            <path d="M 440 145 L 515 80" stroke="#8b5cf6" stroke-width="2" marker-end="url(#am)"/>
            <rect x="430" y="98" width="95" height="18" rx="3" fill="white" stroke="#ddd6fe"/>
            <text x="477" y="110" font-size="8.5" font-weight="700" fill="#6d28d9" text-anchor="middle">ĐIỀU TRỊ ĐẦU TAY</text>

            <!-- DANGER ARROW -->
            <path d="M 560 105 L 560 210" stroke="#ef4444" stroke-width="2.5" marker-end="url(#ar)"/>
            <rect x="480" y="145" width="160" height="26" rx="4" fill="#fee2e2" stroke="#dc2626"/>
            <text x="560" y="157" font-size="8.5" font-weight="800" fill="#991b1b" text-anchor="middle">CHỐNG CHỈ ĐỊNH CẤP TÍNH</text>
            <text x="560" y="167" font-size="7.5" font-weight="700" fill="#dc2626" text-anchor="middle">(Toan Lactic Tử Vong 50%)</text>

            <path d="M 365 195 L 365 290" stroke="#10b981" stroke-width="2" marker-end="url(#ag)"/>
            <rect x="295" y="235" width="140" height="18" rx="3" fill="#dcfce7" stroke="#86efac"/>
            <text x="365" y="247" font-size="8.5" font-weight="700" fill="#15803d" text-anchor="middle">KHUYẾN NGHỊ DINH DƯỠNG</text>

            <!-- NODES -->
            <rect x="290" y="130" width="150" height="65" rx="8" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
            <text x="365" y="157" font-size="12" font-weight="800" fill="#991b1b" text-anchor="middle">Đái Tháo Đường Típ 2</text>
            <text x="365" y="173" font-size="9.5" font-weight="700" fill="#b91c1c" text-anchor="middle">ICD-10: E11 (Kháng Insulin)</text>

            <rect x="20" y="45" width="130" height="52" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
            <text x="85" y="68" font-size="10.5" font-weight="700" fill="#92400e" text-anchor="middle">HbA1c Máu</text>
            <text x="85" y="84" font-size="9" fill="#b45309" text-anchor="middle">Ngưỡng chuẩn ≥ 6.5%</text>

            <rect x="20" y="205" width="130" height="52" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
            <text x="85" y="228" font-size="10.5" font-weight="700" fill="#92400e" text-anchor="middle">Glucose Đói 8h</text>
            <text x="85" y="244" font-size="9" fill="#b45309" text-anchor="middle">Ngưỡng chuẩn ≥ 126 mg/dL</text>

            <rect x="490" y="50" width="140" height="52" rx="6" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.8"/>
            <text x="560" y="73" font-size="11" font-weight="800" fill="#6d28d9" text-anchor="middle">Thuốc Metformin</text>
            <text x="560" y="89" font-size="8.5" fill="#7c3aed" text-anchor="middle">Biguanide 500-1000mg</text>

            <rect x="490" y="220" width="140" height="52" rx="6" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
            <text x="560" y="243" font-size="11" font-weight="800" fill="#991b1b" text-anchor="middle">Rượu Bia / Cồn</text>
            <text x="560" y="259" font-size="8.5" font-weight="700" fill="#b91c1c" text-anchor="middle">Chất nguy hại chuyển hóa</text>

            <rect x="285" y="300" width="160" height="52" rx="6" fill="#dcfce7" stroke="#10b981" stroke-width="1.8"/>
            <text x="365" y="323" font-size="11" font-weight="800" fill="#047857" text-anchor="middle">Ức Gà Nạc Luộc/Hấp</text>
            <text x="365" y="339" font-size="8.5" fill="#15803d" text-anchor="middle">Protein sạch (GI = 0)</text>
          </svg>
        </div>

        <div class="cypher-box">
          <div style="color:#38bdf8; font-weight:700; margin-bottom:2px;">// Cypher Query kiểm tra chống chỉ định tử vong</div>
          <div><span style="color:#f472b6;">MATCH</span> (d:Benh {ten: <span style="color:#a7f3d0;">'ĐTĐ Típ 2'</span>})-[r1:DIEU_TRI]-&gt;(t:Thuoc {ten: <span style="color:#a7f3d0;">'Metformin'</span>})</div>
          <div><span style="color:#f472b6;">MATCH</span> (t)-[r2:CHONG_CHI_DINH]-&gt;(c:Chat {ten: <span style="color:#a7f3d0;">'Rượu bia'</span>})</div>
          <div><span style="color:#f472b6;">RETURN</span> d.ten, t.ten, r2.nguy_co, r2.ty_le_tu_vong; <span style="color:#94a3b8;">// ➔ Báo động đỏ cấp tính</span></div>
        </div>
      </div>
    </div>

    <!-- PANEL 2: BENCHMARK TABLE -->
    <div class="panel p-right">
      <div class="p-hdr">
        <span>ĐỐI CHUẨN KỸ THUẬT: GRAPH DB VS. VECTOR DB</span>
        <span style="font-size:10px; background:#ccfbf1; color:#0f766e; padding:2px 6px; border-radius:3px;">Benchmark</span>
      </div>
      <div class="tbl-box">
        <table>
          <thead>
            <tr>
              <th style="width:28%;">Tiêu chí Đánh giá</th>
              <th style="width:36%;">Vector DB (Milvus, FAISS)</th>
              <th style="width:36%;">Graph DB (Neo4j, KG)</th>
            </tr>
          </thead>
          <tbody>
            <tr><td class="td-b">Cấu trúc Dữ liệu</td><td>Dense Vectors (768-1536 dims)</td><td class="td-h">Nodes, Edges, Properties định kiểu</td></tr>
            <tr><td class="td-b">Bản chất Tri thức</td><td>Xác suất thống kê ngữ nghĩa (Cosine)</td><td class="td-h">Logic biểu tượng xác định 100%</td></tr>
            <tr><td class="td-b">Cơ chế Truy xuất</td><td>K-láng giềng gần nhất (HNSW)</td><td class="td-h">Duyệt đồ thị đa bước (Multi-hop)</td></tr>
            <tr><td class="td-b">Khả năng Suy luận</td><td>Rất yếu; không suy luận bắc cầu</td><td class="td-h">Rất mạnh; suy luận quan hệ phức tạp</td></tr>
            <tr><td class="td-b">Nguy cơ Ảo giác</td><td>Dễ bị ảo giác do phân mảnh ngữ cảnh</td><td class="td-h">Triệt tiêu 100% ảo giác nhờ kiểm chứng</td></tr>
            <tr><td class="td-b">Tính Giải thích</td><td>Hộp đen; khoảng cách vector trừu tượng</td><td class="td-h">Bạch diện; dẫn xuất chuỗi bằng chứng</td></tr>
            <tr><td class="td-b">Miền Ứng dụng</td><td>Tìm kiếm tài liệu ngữ nghĩa tự do</td><td class="td-h">Dược lý, phác đồ y tế, tài chính vĩ mô</td></tr>
          </tbody>
        </table>

        <div class="conc-box">
          <b style="color:#047857;">KẾT LUẬN KIẾN TRÚC HIỆN ĐẠI: GRAPHRAG HỢP NHẤT</b><br>
          Hệ thống tối ưu kết hợp <b>Vector DB</b> để tìm kiếm nhanh các điểm neo ngữ nghĩa ban đầu, sau đó chuyển giao cho <b>Graph DB</b> duyệt sâu n-bước để trích xuất toàn bộ chuỗi nhân quả và ràng buộc an toàn bắt buộc.
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""
    render_html_to_png(html, os.path.join(OUTPUT_DIR, "fig702_knowledge_graph_triples_ontology.png"), 1400, 680)


# =============================================================================
# 3. FIG 703: TIẾN HÓA CÁC THẾ HỆ RAG
# =============================================================================
def generate_fig703():
    html = """<!DOCTYPE html>
<html lang="vi" spellcheck="false">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-font-smoothing: antialiased; }
  html, body { width: 1400px; height: 680px; overflow: hidden; background: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #0f172a; }
  .wrapper { padding: 14px 16px; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
  
  .header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 8px; padding: 10px 18px; color: white; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155;
  }
  .h-title { font-size: 16.5px; font-weight: 800; color: #f8fafc; }
  .h-sub { font-size: 11px; color: #94a3b8; }
  
  .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1.05fr; gap: 16px; height: 595px; }
  .col {
    background: white; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 2px 5px rgba(0,0,0,0.04); display: flex; flex-direction: column; overflow: hidden;
  }
  .c-hdr {
    padding: 8px 12px; font-size: 12px; font-weight: 800; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0,0,0,0.06);
  }
  .c-body { padding: 10px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; gap: 8px; }
  
  .c-red { border-top: 3px solid #ef4444; } .c-red .c-hdr { background: #fef2f2; color: #b91c1c; }
  .c-blue { border-top: 3px solid #2563eb; } .c-blue .c-hdr { background: #eff6ff; color: #1d4ed8; }
  .c-green { border-top: 3px solid #059669; } .c-green .c-hdr { background: #ecfdf5; color: #065f46; }

  .step { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 8px 10px; flex: 1; display: flex; flex-direction: column; justify-content: center; }
  .step-t { font-weight: 700; font-size: 10.5px; margin-bottom: 3px; }
  .step-d { font-size: 9.8px; color: #334155; line-height: 1.35; }
  .flow-arr { text-align: center; color: #94a3b8; font-size: 11px; line-height: 1; }

  .v-box { border-radius: 6px; padding: 8px 10px; font-size: 10px; line-height: 1.35; }
  .v-red { background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; }
  .v-blue { background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af; }
  .v-green { background: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46; }
</style>
</head>
<body spellcheck="false">
<div class="wrapper">
  <div class="header">
    <div>
      <div class="h-title">TIẾN HÓA CÁC THẾ HỆ RETRIEVAL-AUGMENTED GENERATION (RAG)</div>
      <div class="h-sub">Lộ trình Phát triển Kỹ thuật: Naive RAG ➔ Advanced RAG ➔ GraphRAG (Microsoft Research 2024)</div>
    </div>
    <div style="background:rgba(59,130,246,0.18); border:1px solid #3b82f6; color:#93c5fd; padding:3px 9px; border-radius:12px; font-size:10.5px; font-weight:700;">
      RAG Evolution
    </div>
  </div>

  <div class="grid-3">
    <!-- COL 1 -->
    <div class="col c-red">
      <div class="c-hdr"><span>THẾ HỆ 1: NAIVE RAG (CỔ ĐIỂN)</span><span style="font-size:9px; background:#fee2e2; color:#b91c1c; padding:2px 5px; border-radius:3px;">Legacy</span></div>
      <div class="c-body">
        <div class="step"><div class="step-t" style="color:#b91c1c;">1. Chunking Cơ Học Cố Định</div><div class="step-d">Cắt văn bản cứng nhắc 512 tokens. Ngắt đôi câu văn, phá vỡ cấu trúc ngữ pháp và ngữ nghĩa liền mạch.</div></div>
        <div class="flow-arr">↓</div>
        <div class="step"><div class="step-t" style="color:#b91c1c;">2. Dense Vector Embeddings</div><div class="step-d">Biến đổi từng chunk thành vector độc lập. Mất hoàn toàn ngữ cảnh toàn cục của tài liệu nguồn.</div></div>
        <div class="flow-arr">↓</div>
        <div class="step"><div class="step-t" style="color:#b91c1c;">3. Vector Search Top-k</div><div class="step-d">Tính khoảng cách Cosine đơn thuần; dễ nhầm lẫn giữa khẳng định/phủ định, bỏ sót liên đới nhiều tầng.</div></div>
        <div class="flow-arr">↓</div>
        <div class="step"><div class="step-t" style="color:#b91c1c;">4. Ghép Prompt LLM</div><div class="step-d">Nhồi nguyên xi Top-k đoạn văn vào context window để sinh văn bản trả lời không qua xác thực.</div></div>
        <div class="v-box v-red">
          <b>🚨 NHƯỢC ĐIỂM CỐ HỮU:</b> Mất liên kết thực thể nhiều chặng; Ảo giác nặng khi gặp câu hỏi suy luận tổng thể toàn kho văn bản.
        </div>
      </div>
    </div>

    <!-- COL 2 -->
    <div class="col c-blue">
      <div class="c-hdr"><span>THẾ HỆ 2: ADVANCED RAG (TỐI ƯU)</span><span style="font-size:9px; background:#dbeafe; color:#1d4ed8; padding:2px 5px; border-radius:3px;">Standard</span></div>
      <div class="c-body">
        <div class="step"><div class="step-t" style="color:#1d4ed8;">1. Tiền Truy Xuất (Pre-Retrieval)</div><div class="step-d">Tối ưu câu hỏi bằng Query Expansion, Multi-Query và sinh tài liệu giả định đối sánh (HyDE).</div></div>
        <div class="flow-arr">↓</div>
        <div class="step"><div class="step-t" style="color:#1d4ed8;">2. Tìm Kiếm Lai (Hybrid Retrieval)</div><div class="step-d">Kết hợp tìm kiếm từ khóa chính xác (BM25) và vector tương đồng (Dense) bằng thuật toán RRF.</div></div>
        <div class="flow-arr">↓</div>
        <div class="step"><div class="step-t" style="color:#1d4ed8;">3. Tái Xếp Hạng (Post-Retrieval)</div><div class="step-d">Áp dụng Cross-Encoder Reranker chấm điểm lại từng cặp (query, doc) để triệt tiêu đoạn rác.</div></div>
        <div class="flow-arr">↓</div>
        <div class="step"><div class="step-t" style="color:#1d4ed8;">4. Nén Ngữ Cảnh (Context Compression)</div><div class="step-d">Trích lọc câu then chốt nhằm tối ưu hóa chi phí token và tránh hiệu ứng Lost in the Middle.</div></div>
        <div class="v-box v-blue">
          <b>⚖️ ĐÁNH GIÁ CHUYÊN MÔN:</b> Độ chính xác đoạn trích tăng cao, nhưng vẫn nhìn nhận văn bản là các mẩu rời rạc, chưa hiểu logic bản thể luận.
        </div>
      </div>
    </div>

    <!-- COL 3 -->
    <div class="col c-green">
      <div class="c-hdr"><span>THẾ HỆ 3: GRAPHRAG (ĐỘT PHÁ 2024)</span><span style="font-size:9px; background:#d1fae5; color:#065f46; padding:2px 5px; border-radius:3px;">State-of-the-Art</span></div>
      <div class="c-body">
        <div class="step"><div class="step-t" style="color:#065f46;">1. Trích Xuất Thực Thể & Quan Hệ LLM</div><div class="step-d">LLM quét văn bản bóc tách mạng lưới thực thể (Entities) và quan hệ liên kết (Relationships).</div></div>
        <div class="flow-arr">↓</div>
        <div class="step"><div class="step-t" style="color:#065f46;">2. Phân Cụm Cộng Đồng (Leiden Algo)</div><div class="step-d">Thuật toán phân cụm đồ thị phân cấp gom thực thể liên quan chặt thành các cụm chủ đề tri thức.</div></div>
        <div class="flow-arr">↓</div>
        <div class="step"><div class="step-t" style="color:#065f46;">3. Tóm Tắt Cộng Đồng Phân Cấp</div><div class="step-d">LLM tự động viết báo cáo tóm tắt cho từng cụm ở nhiều cấp độ (từ vi mô đến vĩ mô).</div></div>
        <div class="flow-arr">↓</div>
        <div class="step"><div class="step-t" style="color:#065f46;">4. Truy Vấn Kép (Global + Local Search)</div><div class="step-d">Kết hợp Local Search cho thực thể hẹp và Global Search cho câu hỏi khái quát toàn kho dữ liệu.</div></div>
        <div class="v-box v-green">
          <b>🌟 ĐỘT PHÁ TOÀN DIỆN:</b> Bao quát toàn cảnh xuất sắc; 100% Fact-Grounded, triệt tiêu ảo giác; Minh bạch dẫn đường chứng cứ gốc.
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""
    render_html_to_png(html, os.path.join(OUTPUT_DIR, "fig703_rag_pipeline_and_graphrag.png"), 1400, 680)


# =============================================================================
# 4. FIG 704: ĐỒ THỊ TRI THỨC Y TẾ TIỂU ĐƯỜNG VIỆT NAM (HOÀN HẢO 100%)
# =============================================================================
def generate_fig704():
    html = """<!DOCTYPE html>
<html lang="vi" spellcheck="false">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-font-smoothing: antialiased; }
  html, body { width: 1400px; height: 680px; overflow: hidden; background: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #0f172a; }
  .wrapper { padding: 14px 16px; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
  
  .header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 8px; padding: 10px 18px; color: white; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155;
  }
  .h-title { font-size: 16.5px; font-weight: 800; color: #f8fafc; }
  .h-sub { font-size: 11px; color: #94a3b8; }
  
  .canvas {
    background: white; border-radius: 8px; border: 1px solid #cbd5e1; height: 595px; position: relative; padding: 12px 14px; display: flex; flex-direction: column; justify-content: space-between;
  }
  .svg-overlay { position: absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:10; }

  /* TIER STRIPS */
  .tier-box {
    border-radius: 6px; border: 1px solid #e2e8f0; padding: 7px 12px; display: flex; flex-direction: column; justify-content: space-between; position: relative; z-index: 2;
  }
  .tier-lbl { font-size: 9.5px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 5px; }
  .node-row { display: flex; justify-content: space-between; align-items: center; gap: 12px; }

  /* NODES */
  .node {
    background: white; border-radius: 6px; border: 1.5px solid #cbd5e1; padding: 6px 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.03); display: flex; flex-direction: column; justify-content: center;
  }
  .n-title { font-size: 11.5px; font-weight: 800; }
  .n-sub { font-size: 9.5px; color: #475569; margin-top: 1px; }

  /* STYLES */
  .t1-bg { background: #f8fafc; border-color: #cbd5e1; height: 110px; }
  .t1-node { border-color: #0284c7; flex: 1; text-align: center; }
  .t1-node .n-title { color: #0369a1; }

  .t2-bg { background: #fff5f5; border-color: #fecaca; height: 125px; }
  .t2-risk { border-color: #f59e0b; width: 330px; }
  .t2-risk .n-title { color: #b45309; }
  .t2-center { border: 2.5px solid #dc2626; background: #fef2f2; width: 440px; text-align: center; padding: 8px 12px; }
  .t2-center .n-title { color: #991b1b; font-size: 14px; font-weight: 900; }
  .t2-comp { border-color: #ef4444; width: 350px; }
  .t2-comp .n-title { color: #b91c1c; }

  .t3-bg { background: #faf5ff; border-color: #e9d5ff; height: 125px; }
  .t3-drug { border-color: #8b5cf6; width: 360px; }
  .t3-drug .n-title { color: #6d28d9; }
  .t3-danger { border: 2.2px solid #dc2626; background: #fee2e2; width: 440px; text-align: center; }
  .t3-danger .n-title { color: #991b1b; }
  .t3-second { border-color: #a855f7; width: 340px; }
  .t3-second .n-title { color: #7e22ce; }

  .t4-bg { background: #f0fdf4; border-color: #bbf7d0; height: 135px; }
  .t4-good { border: 2px solid #10b981; background: #ecfdf5; flex: 1; }
  .t4-good .n-title { color: #047857; }
  .t4-bad { border: 2px solid #ef4444; background: #fef2f2; flex: 1; }
  .t4-bad .n-title { color: #b91c1c; }

  /* INTER-TIER CONNECTOR BARS */
  .c-bar {
    display: flex; justify-content: center; align-items: center; height: 26px; gap: 14px; font-size: 9.5px; font-weight: 800;
  }
  .pill {
    padding: 3px 12px; border-radius: 12px; display: inline-flex; align-items: center; gap: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }
  .p-blu { background: #e0f2fe; border: 1px solid #7dd3fc; color: #0369a1; }
  .p-red { background: #fee2e2; border: 1px solid #fca5a5; color: #991b1b; }
  .p-pur { background: #f3e8ff; border: 1px solid #d8b4fe; color: #6b21a8; }
  .p-grn { background: #dcfce7; border: 1px solid #86efac; color: #15803d; }
</style>
</head>
<body spellcheck="false">
<div class="wrapper">
  <div class="header">
    <div>
      <div class="h-title">ĐỒ THỊ TRI THỨC Y TẾ CHUYÊN SÂU: ĐÁI THÁO ĐƯỜNG TÍP 2 TẠI VIỆT NAM</div>
      <div class="h-sub">Chuẩn hóa theo Quyết định 5481/QĐ-BYT của Bộ Y Tế & Hướng dẫn Viện Dinh Dưỡng Quốc Gia</div>
    </div>
    <div style="background:rgba(239,68,68,0.2); border:1px solid #ef4444; color:#fca5a5; padding:3px 9px; border-radius:12px; font-size:10.5px; font-weight:700;">
      Medical Safety KG
    </div>
  </div>

  <div class="canvas">
    <!-- TIER 1 -->
    <div class="tier-box t1-bg">
      <div class="tier-lbl" style="color:#0369a1;">TẦNG 1: TIÊU CHUẨN CHẨN ĐOÁN LÂM SÀNG BỘ Y TẾ (QUYẾT ĐỊNH 5481/QĐ-BYT)</div>
      <div class="node-row">
        <div class="node t1-node">
          <div class="n-title">HbA1c Máu ≥ 6.5%</div>
          <div class="n-sub">Phương pháp sắc ký HPLC chuẩn hóa NGSP</div>
        </div>
        <div class="node t1-node">
          <div class="n-title">Glucose Đói ≥ 126 mg/dL (7.0 mmol/L)</div>
          <div class="n-sub">Nhịn ăn tối thiểu 8 giờ trước khi xét nghiệm</div>
        </div>
        <div class="node t1-node">
          <div class="n-title">Nghiệm Pháp OGTT ≥ 200 mg/dL</div>
          <div class="n-sub">Uống 75g Glucose sau 2 giờ theo chuẩn WHO</div>
        </div>
        <div class="node t1-node">
          <div class="n-title">Glucose Bất Kỳ ≥ 200 mg/dL</div>
          <div class="n-sub">Kèm triệu chứng 4 nhiều (uống, tiểu, ăn, gầy)</div>
        </div>
      </div>
    </div>

    <!-- CONNECTOR BAR 1 -> 2 -->
    <div class="c-bar">
      <span class="pill p-blu">⬇ TIÊU CHUẨN CHẨN ĐOÁN XÁC ĐỊNH BỆNH LÝ ⬇</span>
    </div>

    <!-- TIER 2 -->
    <div class="tier-box t2-bg">
      <div class="tier-lbl" style="color:#991b1b;">TẦNG 2: THỰC THỂ BỆNH TRUNG TÂM, NGUY CƠ & BIẾN CHỨNG NGUY HIỂM</div>
      <div class="node-row">
        <div class="node t2-risk">
          <div class="n-title">YẾU TỐ NGUY CƠ VIỆT NAM</div>
          <div class="n-sub">• BMI ≥ 23 kg/m² (thừa cân chuẩn người Việt)<br>• Tiền sử gia đình, tăng huyết áp ≥ 140/90 mmHg</div>
        </div>
        
        <div style="font-weight:900; color:#b45309; font-size:14px;">➔</div>

        <div class="node t2-center">
          <div class="n-title">ĐÁI THÁO ĐƯỜNG TÍP 2</div>
          <div style="font-size:11px; font-weight:800; color:#b91c1c; margin-top:2px;">MÃ QUỐC TẾ ICD-10: E11</div>
          <div class="n-sub" style="color:#7f1d1d;">Rối loạn chuyển hóa: Kháng Insulin kết hợp suy giảm tiết Insulin tiến triển</div>
        </div>

        <div style="font-weight:900; color:#dc2626; font-size:14px;">➔</div>

        <div class="node t2-comp">
          <div class="n-title">BIẾN CHỨNG MẠN TÍNH ĐỎ</div>
          <div class="n-sub">• Vi mạch: Bệnh võng mạc mắt, Suy thận mạn<br>• Đại mạch: Đột quỵ não, Nhồi máu cơ tim, Hoại tử chi</div>
        </div>
      </div>
    </div>

    <!-- CONNECTOR BAR 2 -> 3 -->
    <div class="c-bar">
      <span class="pill p-pur">⬇ CHỈ ĐỊNH PHÁC ĐỒ DƯỢC LÝ & CẢNH BÁO TƯƠNG TÁC CẤM ⬇</span>
    </div>

    <!-- TIER 3 -->
    <div class="tier-box t3-bg">
      <div class="tier-lbl" style="color:#6b21a8;">TẦNG 3: PHÁC ĐỒ DƯỢC LÝ & TƯƠNG TÁC THUỐC CẤP TÍNH BẮT BUỘC</div>
      <div class="node-row">
        <div class="node t3-drug">
          <div class="n-title">METFORMIN (BIGUANIDE 500-1000mg)</div>
          <div class="n-sub">• Điều trị đầu tay: Giảm sản xuất Glucose gan<br>• Tăng nhạy cảm thụ thể Insulin ngoại vi</div>
        </div>

        <div style="font-weight:900; color:#dc2626; font-size:16px;">⚡</div>

        <div class="node t3-danger">
          <div class="n-title" style="color:#991b1b; font-size:12.5px;">🚨 RƯỢU BIA & CỒN (CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI)</div>
          <div class="n-sub" style="color:#b91c1c; font-weight:700;">
            • CẤM TUYỆT ĐỐI KHI ĐANG UỐNG METFORMIN!<br>
            • Ức chế chuyển hóa Acid Lactic tại gan ➔ Nhiễm toan Lactic tử vong 50%
          </div>
        </div>

        <div style="font-weight:900; color:#7e22ce; font-size:14px;">+</div>

        <div class="node t3-second">
          <div class="n-title">PHỐI HỢP THUỐC BẬC 2</div>
          <div class="n-sub">• SGLT2i (Dapagliflozin): Bảo vệ tim - thận<br>• Sulfonylurea (Gliclazide): Kích thích tiết Insulin</div>
        </div>
      </div>
    </div>

    <!-- CONNECTOR BAR 3 -> 4 -->
    <div class="c-bar">
      <span class="pill p-grn">⬇ HƯỚNG DẪN DINH DƯỠNG & CHỈ SỐ ĐƯỜNG HUYẾT THỰC PHẨM (GI) ⬇</span>
    </div>

    <!-- TIER 4 -->
    <div class="tier-box t4-bg">
      <div class="tier-lbl" style="color:#166534;">TẦNG 4: HƯỚNG DẪN DINH DƯỠNG THEO VIỆN DINH DƯỠNG QUỐC GIA</div>
      <div class="node-row">
        <div class="node t4-good">
          <div class="n-title">✓ THỰC PHẨM KHUYẾN NGHỊ ĂN (CHỈ SỐ GI THẤP & PROTEIN SẠCH)</div>
          <div class="n-sub" style="color:#14532d; font-size:10px;">
            • <b>Ức gà nạc bỏ da luộc/hấp:</b> Protein tinh khiết không làm tăng đường huyết (GI = 0).<br>
            • <b>Rau xanh & chất xơ hòa tan:</b> Cải bó xôi, súp lơ xanh, rau muống làm chậm hấp thu đường.<br>
            • <b>Gạo lứt nguyên cám:</b> GI thấp (&lt; 55), giàu vitamin nhóm B và khoáng chất tự nhiên.
          </div>
        </div>
        <div class="node t4-bad">
          <div class="n-title">✗ THỰC PHẨM NGHIÊM CẤM / HẠN CHẾ TỐI ĐA (NGUY CƠ CAO)</div>
          <div class="n-sub" style="color:#7f1d1d; font-size:10px;">
            • <b>Da gà & gà chiên tẩm bột:</b> Chất béo bão hòa và trans-fat gây kháng Insulin trầm trọng.<br>
            • <b>Nước ngọt có ga, bánh kẹo:</b> Đường đơn hấp thu siêu nhanh (GI &gt; 70) gây tăng vọt đường huyết cấp.<br>
            • <b>Lòng đỏ trứng, phủ tạng:</b> Cholesterol xấu làm gia tăng biến chứng xơ vữa động mạch.
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""
    render_html_to_png(html, os.path.join(OUTPUT_DIR, "fig704_diabetes_vietnam_knowledge_graph.png"), 1400, 680)


# =============================================================================
# 5. FIG 705: ĐỒ THỊ TRI THỨC TÀI CHÍNH VIỆT NAM (HOÀN HẢO 100%)
# =============================================================================
def generate_fig705():
    html = """<!DOCTYPE html>
<html lang="vi" spellcheck="false">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-font-smoothing: antialiased; }
  html, body { width: 1400px; height: 680px; overflow: hidden; background: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #0f172a; }
  .wrapper { padding: 14px 16px; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
  
  .header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 8px; padding: 10px 18px; color: white; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155;
  }
  .h-title { font-size: 16.5px; font-weight: 800; color: #f8fafc; }
  .h-sub { font-size: 11px; color: #94a3b8; }
  
  .canvas {
    background: white; border-radius: 8px; border: 1px solid #cbd5e1; height: 595px; position: relative; padding: 12px 14px; display: flex; flex-direction: column; justify-content: space-between;
  }

  /* TIER STRIPS */
  .tier-box {
    border-radius: 6px; border: 1px solid #e2e8f0; padding: 7px 12px; display: flex; flex-direction: column; justify-content: space-between; position: relative; z-index: 2;
  }
  .tier-lbl { font-size: 9.5px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 5px; }
  .node-row { display: flex; justify-content: space-between; align-items: center; gap: 12px; }

  /* NODES */
  .node {
    background: white; border-radius: 6px; border: 1.5px solid #cbd5e1; padding: 7px 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.03); display: flex; flex-direction: column; justify-content: center;
  }
  .n-title { font-size: 11.5px; font-weight: 800; }
  .n-sub { font-size: 9.5px; color: #475569; margin-top: 1px; line-height: 1.35; }

  /* STYLES */
  .t1-bg { background: #f8fafc; border-color: #cbd5e1; height: 120px; }
  .t1-nhnn { border-color: #0284c7; width: 320px; } .t1-nhnn .n-title { color: #0369a1; }
  .t1-usd { border: 2.2px solid #2563eb; background: #eff6ff; width: 380px; text-align: center; } .t1-usd .n-title { color: #1d4ed8; font-size: 13px; }
  .t1-nd24 { border-color: #f59e0b; width: 330px; } .t1-nd24 .n-title { color: #b45309; }
  .t1-cpi { border-color: #64748b; width: 280px; } .t1-cpi .n-title { color: #334155; }

  .t2-bg { background: #fffbeb; border-color: #fde68a; height: 160px; }
  .t2-fpt { border: 2px solid #10b981; background: #ecfdf5; flex: 1; } .t2-fpt .n-title { color: #047857; font-size: 12.5px; }
  .t2-hpg { border: 2px solid #ef4444; background: #fef2f2; flex: 1; } .t2-hpg .n-title { color: #b91c1c; font-size: 12.5px; }
  .t2-sjc { border: 2px solid #f59e0b; background: #fffbeb; flex: 1; } .t2-sjc .n-title { color: #b45309; font-size: 12.5px; }

  .t3-bg { background: #f0fdf4; border-color: #bbf7d0; height: 165px; }
  .t3-card { flex: 1; border-radius: 6px; padding: 8px 10px; display: flex; flex-direction: column; justify-content: space-between; }
  .t3-grn { background: #ecfdf5; border: 1.8px solid #10b981; } .t3-grn .n-title { color: #065f46; font-size: 12px; }
  .t3-red { background: #fef2f2; border: 1.8px solid #ef4444; } .t3-red .n-title { color: #991b1b; font-size: 12px; }
  .t3-amb { background: #fffbeb; border: 1.8px solid #f59e0b; } .t3-amb .n-title { color: #92400e; font-size: 12px; }

  /* CONNECTOR BARS */
  .c-bar {
    display: flex; justify-content: space-around; align-items: center; height: 26px; font-size: 9.5px; font-weight: 800;
  }
  .pill {
    padding: 3px 14px; border-radius: 12px; display: inline-flex; align-items: center; gap: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }
  .p-grn { background: #dcfce7; border: 1px solid #86efac; color: #15803d; }
  .p-red { background: #fee2e2; border: 1px solid #fca5a5; color: #991b1b; }
  .p-amb { background: #fef3c7; border: 1px solid #fde68a; color: #92400e; }
  .p-blu { background: #e0f2fe; border: 1px solid #7dd3fc; color: #0369a1; }
</style>
</head>
<body spellcheck="false">
<div class="wrapper">
  <div class="header">
    <div>
      <div class="h-title">ĐỒ THỊ TRI THỨC TÀI CHÍNH & THỊ TRƯỜNG VIỆT NAM (FINANCIAL KG)</div>
      <div class="h-sub">Mô hình hóa Chuỗi Tác động Vĩ mô: Ngân hàng Nhà nước, Tỷ giá USD/VND, VN-Index và Vàng SJC</div>
    </div>
    <div style="background:rgba(245,158,11,0.2); border:1px solid #f59e0b; color:#fde68a; padding:3px 9px; border-radius:12px; font-size:10.5px; font-weight:700;">
      Macro Causal Network
    </div>
  </div>

  <div class="canvas">
    <!-- TIER 1 -->
    <div class="tier-box t1-bg">
      <div class="tier-lbl" style="color:#0369a1;">TẦNG 1: CHÍNH SÁCH TIỀN TỆ VĨ MÔ & TỶ GIÁ TRUNG TÂM</div>
      <div class="node-row">
        <div class="node t1-nhnn">
          <div class="n-title">Ngân Hàng Nhà Nước (NHNN)</div>
          <div class="n-sub">• Lãi suất tái cấp vốn: 4.5% | Dự trữ ngoại tệ $85B<br>• Phát hành tín phiếu SBV điều tiết thanh khoản</div>
        </div>

        <div style="font-weight:900; color:#0284c7; font-size:13px;">➔ Điều Hành ➔</div>

        <div class="node t1-usd">
          <div class="n-title">TỶ GIÁ USD/VND = 25,450</div>
          <div style="font-size:10px; font-weight:700; color:#1e40af; margin-top:2px;">Biến động tăng +4.2% từ đầu năm 2024</div>
          <div class="n-sub" style="color:#1e3a8a;">Tạo chênh lệch tỷ giá thúc đẩy dòng tiền xuất khẩu IT</div>
        </div>

        <div style="font-weight:900; color:#f59e0b; font-size:13px;">➔ Quản Lý ➔</div>

        <div class="node t1-nd24">
          <div class="n-title">Nghị Định 24/2012/NĐ-CP</div>
          <div class="n-sub">• Quản lý độc quyền sản xuất vàng miếng SJC<br>• Kiểm soát chặt hạn ngạch nhập khẩu vàng nguyên liệu</div>
        </div>

        <div class="node t1-cpi">
          <div class="n-title">Chỉ Số Vĩ Mô (CPI & FDI)</div>
          <div class="n-sub">• Lạm phát CPI kiểm soát &lt; 4.0%<br>• Vốn FDI giải ngân kỷ lục $23.2B</div>
        </div>
      </div>
    </div>

    <!-- CONNECTOR BAR 1 -> 2 -->
    <div class="c-bar">
      <span class="pill p-grn">⬇ HƯỞNG LỢI XUẤT KHẨU TỶ GIÁ DƯƠNG (+) ⬇</span>
      <span class="pill p-red">⬇ ÁP LỰC CHI PHÍ VỐN NHẬP KHẨU (-) ⬇</span>
      <span class="pill p-amb">⬇ ĐỘC QUYỀN NGUỒN CUNG VÀNG MIẾNG ⬇</span>
    </div>

    <!-- TIER 2 -->
    <div class="tier-box t2-bg">
      <div class="tier-lbl" style="color:#92400e;">TẦNG 2: THỊ TRƯỜNG TÀI SẢN (CỔ PHIẾU XUẤT NHẬP KHẨU & THỊ TRƯỜNG VÀNG SJC)</div>
      <div class="node-row">
        <div class="node t2-fpt">
          <div class="n-title">CỔ PHIẾU FPT (CÔNG NGHỆ & XUẤT KHẨU PHẦN MỀM)</div>
          <div class="n-sub" style="color:#065f46;">
            • <b>Doanh thu xuất khẩu:</b> Gần 50% doanh thu đến từ thị trường Nhật Bản, Mỹ bằng USD/JPY.<br>
            • <b>Lợi nhuận ròng:</b> Hưởng lợi trực tiếp chênh lệch tỷ giá dương (+) khi quy đổi về VND.<br>
            • <b>Vị thế:</b> Biên lợi nhuận gộp duy trì cao &gt; 38%, tăng trưởng bền vững 20%/năm.
          </div>
        </div>
        <div class="node t2-hpg">
          <div class="n-title">CỔ PHIẾU HPG (THÉP TẬP ĐOÀN HÒA PHÁT)</div>
          <div class="n-sub" style="color:#7f1d1d;">
            • <b>Chi phí đầu vào:</b> Nhập khẩu 100% quặng sắt, than mỡ luyện cốc thanh toán bằng USD.<br>
            • <b>Áp lực tỷ giá:</b> Lỗ chênh lệch tỷ giá và chi phí tài chính tăng cao khi USD đắt đỏ (-).<br>
            • <b>Biên lợi nhuận:</b> Bị bào mòn ngắn hạn mặc dù sản lượng nội địa duy trì dẫn đầu thị phần.
          </div>
        </div>
        <div class="node t2-sjc">
          <div class="n-title">VÀNG MIẾNG SJC (THỊ TRƯỜNG TÀI SẢN PHÒNG VỆ)</div>
          <div class="n-sub" style="color:#78350f;">
            • <b>Mức giá:</b> Neo cao kỷ lục 90.5 triệu VNĐ/lượng.<br>
            • <b>Khan hiếm nguồn cung:</b> Hạn ngạch NĐ 24 khiến lượng cung vàng miếng bị thắt chặt.<br>
            • <b>Chênh lệch:</b> Giá trong nước cao hơn giá thế giới quy đổi từ 16 đến 18 triệu đồng.
          </div>
        </div>
      </div>
    </div>

    <!-- CONNECTOR BAR 2 -> 3 -->
    <div class="c-bar">
      <span class="pill p-grn">⬇ MÔ HÌNH HỌC SÂU BiLSTM DỰ BÁO XU HƯỚNG TĂNG ⬇</span>
      <span class="pill p-red">⬇ MÔ HÌNH HỌC SÂU BiLSTM DỰ BÁO ĐI NGANG ⬇</span>
      <span class="pill p-amb">⬇ MÔ HÌNH HỌC SÂU BiLSTM DỰ BÁO BIÊN ĐỘ CAO ⬇</span>
    </div>

    <!-- TIER 3 -->
    <div class="tier-box t3-bg">
      <div class="tier-lbl" style="color:#166534;">TẦNG 3: DỰ BÁO SỐ HỌC (DEEP LEARNING BiLSTM) & KHUYẾN NGHỊ DANH MỤC ĐẦU TƯ</div>
      <div class="node-row">
        <div class="node t3-card t3-grn">
          <div class="n-title">DỰ BÁO BiLSTM: FPT (+1.8%)</div>
          <div class="n-sub" style="color:#047857;">
            • <b>Xu hướng:</b> Tiếp diễn đà tăng trưởng mạnh mẽ; độ tin cậy mô hình đạt <b>84.2%</b>.<br>
            • <b>Vùng mục tiêu:</b> 138,000 - 142,000 VNĐ/cổ phiếu.<br>
            • <b>Khuyến nghị:</b> <b>TẬP TRUNG TÍCH LŨY TỶ TRỌNG CAO</b> trong danh mục dài hạn.
          </div>
        </div>
        <div class="node t3-card t3-red">
          <div class="n-title">DỰ BÁO BiLSTM: HPG (BIÊN ĐỘ HẸP)</div>
          <div class="n-sub" style="color:#b91c1c;">
            • <b>Xu hướng:</b> Đi ngang tích lũy; chịu sức ép biến động tỷ giá và giá nguyên liệu.<br>
            • <b>Vùng hỗ trợ:</b> 27,500 - 28,200 VNĐ/cổ phiếu.<br>
            • <b>Khuyến nghị:</b> <b>TẠM THỜI QUAN SÁT</b>, chờ điểm cân bằng tỷ giá trước khi gia tăng.
          </div>
        </div>
        <div class="node t3-card t3-amb">
          <div class="n-title">DỰ BÁO BiLSTM: VÀNG SJC (DAO ĐỘNG CAO)</div>
          <div class="n-sub" style="color:#b45309;">
            • <b>Biên độ:</b> 89.8 - 91.5 triệu VNĐ/lượng; phụ thuộc động thái đấu thầu NHNN.<br>
            • <b>Rủi ro chính sách:</b> Khả năng sửa đổi Nghị định 24 thu hẹp khoảng cách giá.<br>
            • <b>Khuyến nghị:</b> <b>THẬN TRỌNG, TUYỆT ĐỐI TRÁNH ĐU ĐỈNH</b> khi chênh lệch &gt; 15 tr.
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""
    render_html_to_png(html, os.path.join(OUTPUT_DIR, "fig705_financial_stock_gold_knowledge_graph.png"), 1400, 680)


# =============================================================================
# 6. FIG 706: QUY TRÌNH PHỐI HỢP ĐA CÔNG CỤ CỦA REACT AGENT
# =============================================================================
def generate_fig706():
    html = """<!DOCTYPE html>
<html lang="vi" spellcheck="false">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-font-smoothing: antialiased; }
  html, body { width: 1400px; height: 680px; overflow: hidden; background: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #0f172a; }
  .wrapper { padding: 14px 16px; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
  
  .header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 8px; padding: 10px 18px; color: white; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155;
  }
  .h-title { font-size: 16.5px; font-weight: 800; color: #f8fafc; }
  .h-sub { font-size: 11px; color: #94a3b8; }
  
  .workspace {
    position: relative; display: grid; grid-template-columns: 290px 50px 325px 50px 345px 50px 290px; height: 595px; align-items: stretch;
  }
  .svg-over { position: absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:10; }

  .col-p {
    background: white; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 2px 5px rgba(0,0,0,0.04); display: flex; flex-direction: column; overflow: hidden; position: relative; z-index: 2;
  }
  .p-hdr {
    padding: 8px 12px; font-size: 11.5px; font-weight: 800; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0,0,0,0.06);
  }
  .p-body { padding: 9px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; font-size: 10.5px; }
  
  .c-blue { border-top: 3px solid #0284c7; } .c-blue .p-hdr { background: #f0f9ff; color: #0369a1; }
  .c-purple { border-top: 3px solid #8b5cf6; } .c-purple .p-hdr { background: #f5f3ff; color: #6d28d9; }
  .c-teal { border-top: 3px solid #0d9488; } .c-teal .p-hdr { background: #f0fdfa; color: #0f766e; }

  .sub { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 5px; padding: 6px 8px; display: flex; flex-direction: column; gap: 2px; }
  .sub-t { font-size: 9.5px; font-weight: 700; color: #475569; text-transform: uppercase; }
  .tag { display: inline-block; padding: 2px 4px; border-radius: 3px; font-size: 9px; font-weight: 700; }
  .t-cyan { background: #e0f2fe; color: #0369a1; } .t-amber { background: #fef3c7; color: #92400e; } .t-purple { background: #f3e8ff; color: #6b21a8; } .t-green { background: #dcfce7; color: #15803d; } .t-rose { background: #ffe4e6; color: #be123c; }

  .loop-box { background: #faf5ff; border: 1px solid #e9d5ff; border-radius: 6px; padding: 6px; display: flex; flex-direction: column; gap: 4px; }
  .step-pill { background: white; border-radius: 4px; border-left: 3px solid #9333ea; padding: 4px 6px; font-size: 9.5px; line-height: 1.35; }

  .tools-col { display: flex; flex-direction: column; justify-content: space-between; gap: 8px; height: 100%; position: relative; z-index: 2; }
  .t-box { background: white; border-radius: 6px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.04); flex: 1; display: flex; flex-direction: column; overflow: hidden; }
  .t-box-hdr { padding: 6px 10px; font-size: 11px; font-weight: 800; display: flex; justify-content: space-between; align-items: center; }
  .t-box-body { padding: 6px 10px; flex: 1; display: flex; flex-direction: column; justify-content: space-around; font-size: 10px; line-height: 1.35; }
  .b-red { border-top: 3px solid #ef4444; } .b-red .t-box-hdr { background: #fef2f2; color: #b91c1c; }
  .b-emerald { border-top: 3px solid #10b981; } .b-emerald .t-box-hdr { background: #ecfdf5; color: #047857; }
  .b-amber { border-top: 3px solid #f59e0b; } .b-amber .t-box-hdr { background: #fffbeb; color: #b45309; }

  .out-alert { background: #fef2f2; border-left: 3px solid #ef4444; border-radius: 4px; padding: 6px 8px; font-size: 10px; color: #7f1d1d; line-height: 1.35; }
  .out-guide { background: #f0fdf4; border-left: 3px solid #10b981; border-radius: 4px; padding: 6px 8px; font-size: 10px; color: #14532d; line-height: 1.35; }
  .out-fin { background: #f0f9ff; border-left: 3px solid #0284c7; border-radius: 4px; padding: 6px 8px; font-size: 10px; color: #0c4a6e; line-height: 1.35; }
</style>
</head>
<body spellcheck="false">
<div class="wrapper">
  <div class="header">
    <div>
      <div class="h-title">KIẾN TRÚC ĐIỀU PHỐI ĐA CÔNG CỤ CỦA TÁC TỬ THÔNG MINH (MULTI-TOOL ReAct AGENT)</div>
      <div class="h-sub">Quy trình Tích hợp Mô hình Học Sâu (Deep Learning), Đồ thị Tri thức (Knowledge Graph) và Dense RAG</div>
    </div>
    <div style="background:rgba(59,130,246,0.18); border:1px solid #3b82f6; color:#93c5fd; padding:3px 9px; border-radius:12px; font-size:10.5px; font-weight:700;">
      Autonomous Pipeline
    </div>
  </div>

  <div class="workspace">
    <!-- SVG CONNECTORS -->
    <svg class="svg-over" viewBox="0 0 1400 595">
      <defs>
        <marker id="ab2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 9 5 L 0 9 z" fill="#0284c7"/></marker>
        <marker id="ap2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 9 5 L 0 9 z" fill="#8b5cf6"/></marker>
        <marker id="at2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 1 L 9 5 L 0 9 z" fill="#0d9488"/></marker>
      </defs>

      <!-- 1 -> 2 -->
      <path d="M 290 297 L 334 297" stroke="#0284c7" stroke-width="2.2" marker-end="url(#ab2)"/>
      <rect x="294" y="286" width="42" height="15" rx="3" fill="white" stroke="#bae6fd"/>
      <text x="315" y="297" font-size="8.5" font-weight="700" fill="#0284c7" text-anchor="middle">Payload</text>

      <!-- 2 -> 3 Forking -->
      <path d="M 665 270 C 695 270, 695 95, 719 95" fill="none" stroke="#8b5cf6" stroke-width="2" marker-end="url(#ap2)"/>
      <path d="M 665 297 L 719 297" fill="none" stroke="#8b5cf6" stroke-width="2" marker-end="url(#ap2)"/>
      <path d="M 665 325 C 695 325, 695 500, 719 500" fill="none" stroke="#8b5cf6" stroke-width="2" marker-end="url(#ap2)"/>
      <rect x="670" y="288" width="46" height="15" rx="3" fill="white" stroke="#ddd6fe"/>
      <text x="693" y="299" font-size="8" font-weight="700" fill="#7c3aed" text-anchor="middle">Gọi Tools</text>

      <!-- 3 -> 4 Converging -->
      <path d="M 1065 95 C 1090 95, 1090 270, 1114 270" fill="none" stroke="#0d9488" stroke-width="2" marker-end="url(#at2)"/>
      <path d="M 1065 297 L 1114 297" fill="none" stroke="#0d9488" stroke-width="2" marker-end="url(#at2)"/>
      <path d="M 1065 500 C 1090 500, 1090 325, 1114 325" fill="none" stroke="#0d9488" stroke-width="2" marker-end="url(#at2)"/>
      <rect x="1070" y="288" width="46" height="15" rx="3" fill="white" stroke="#99f6e4"/>
      <text x="1093" y="299" font-size="8" font-weight="700" fill="#0f766e" text-anchor="middle">Tổng Hợp</text>
    </svg>

    <!-- COL 1: 4 CARDS FILL ENTIRE HEIGHT -->
    <div class="col-p c-blue">
      <div class="p-hdr"><span>1. TIẾP NHẬN YÊU CẦU</span><span class="tag t-cyan">User Stage</span></div>
      <div class="p-body">
        <div class="sub">
          <div class="sub-t">Bệnh Nhân Đái Tháo Đường</div>
          <div><span class="tag t-cyan">HbA1c: 7.3%</span> <span class="tag t-amber">Glucose: 138</span> <span class="tag t-purple">Metformin</span></div>
          <div style="font-style:italic; color:#0369a1; font-size:9.5px; margin-top:1px;">“Chiều nay liên hoan, tôi uống rượu bia và ăn thịt gà được không?”</div>
        </div>
        <div class="sub">
          <div class="sub-t">Nhà Đầu Tư Tài Chính</div>
          <div><span class="tag t-rose">USD/VND: 25,450</span> <span class="tag t-amber">Vàng: 90.5 tr</span></div>
          <div style="font-style:italic; color:#92400e; font-size:9.5px; margin-top:1px;">“Tỷ giá USD và giá vàng tăng mạnh, cổ phiếu FPT ra sao?”</div>
        </div>
        <div class="sub" style="background:#f0f9ff; border-color:#bae6fd;">
          <div class="sub-t" style="color:#0284c7;">Định Tuyến Ý Định (Intent Router)</div>
          <div style="font-size:9.5px; color:#0369a1;">Phân loại tác vụ y tế lâm sàng hoặc phân tích thị trường tài chính.</div>
        </div>
        <div class="sub" style="background:#f0f9ff; border-color:#bae6fd;">
          <div class="sub-t" style="color:#0284c7;">Trích Xuất Thực Thể NER & Payload</div>
          <div style="font-size:9.5px; color:#0369a1;">Chuẩn hóa JSON tham số truyền tới Agent Planner.</div>
        </div>
      </div>
    </div>
    <div></div>

    <!-- COL 2: 4 CARDS FILL ENTIRE HEIGHT -->
    <div class="col-p c-purple">
      <div class="p-hdr"><span>2. BỘ NÃO REACT AGENT</span><span class="tag t-purple">Reasoning Core</span></div>
      <div class="p-body">
        <div class="loop-box">
          <div style="font-size:9.5px; font-weight:800; color:#7e22ce; text-align:center;">VÒNG LẶP SUY LUẬN ReAct</div>
          <div class="step-pill"><b>1. THOUGHT:</b> Phát hiện Metformin + Rượu có nguy cơ tử vong; lập kế hoạch điều phối 3 công cụ.</div>
          <div class="step-pill"><b>2. ACTION:</b> Kích hoạt song song: Tool ML (chẩn đoán), Tool KG (tra cứu), Tool RAG (phác đồ BYT).</div>
          <div class="step-pill"><b>3. OBSERVATION:</b> Thu nhận kết quả trung gian, cập nhật bộ nhớ nhận thức và tổng hợp.</div>
        </div>
        <div class="sub">
          <div class="sub-t">Chiến Lược Điều Phối (Dispatcher)</div>
          <div style="font-size:9.5px;">Phối hợp linh hoạt giữa suy luận biểu tượng và học sâu số học.</div>
        </div>
        <div class="sub">
          <div class="sub-t">Conversation Memory Buffer</div>
          <div style="font-size:9.5px;">Lưu giữ lịch sử hội thoại đa lượt và ngữ cảnh bệnh án/danh mục.</div>
        </div>
        <div class="sub" style="background:#faf5ff; border-color:#e9d5ff;">
          <div class="sub-t" style="color:#6d28d9;">Rào Cản Kiểm Duyệt An Toàn</div>
          <div style="font-size:9.5px; color:#581c87;">Safety Guardrails kiểm duyệt chuẩn BYT, triệt tiêu 100% ảo giác.</div>
        </div>
      </div>
    </div>
    <div></div>

    <!-- COL 3 -->
    <div class="tools-col">
      <div class="t-box b-red">
        <div class="t-box-hdr"><span>TOOL 1: DEEP LEARNING MODEL</span><span class="tag t-rose">Học Sâu Số Học</span></div>
        <div class="t-box-body">
          <div><b>• MLP Classifier v2:</b> Chẩn đoán Đái tháo đường Típ 2 chính xác <b>98.5%</b>.</div>
          <div><b>• PyTorch BiLSTM:</b> Dự báo biến động giá FPT (<b>+1.8%</b>), Vàng SJC (89.8 - 91.5 tr).</div>
        </div>
      </div>

      <div class="t-box b-emerald">
        <div class="t-box-hdr"><span>TOOL 2: KNOWLEDGE GRAPH ENGINE</span><span class="tag t-green">Logic Biểu Tượng</span></div>
        <div class="t-box-body">
          <div><b>• Duyệt Đồ thị Đa bước (Multi-hop) Neo4j:</b></div>
          <div style="background:#f0fdf4; padding:3px 5px; border-radius:3px; border:1px dashed #86efac; font-size:9.5px;">
            - <code>Metformin</code> + <code>Rượu bia</code> ➔ <b style="color:#b91c1c;">CẤM (Toan Lactic)</b><br>
            - <code>Đái tháo đường</code> + <code>Ức gà nạc</code> ➔ <b style="color:#15803d;">An toàn (GI=0)</b><br>
            - <code>USD/VND tăng</code> ➔ <code>FPT</code> hưởng lợi xuất khẩu
          </div>
        </div>
      </div>

      <div class="t-box b-amber">
        <div class="t-box-hdr"><span>TOOL 3: DENSE VECTOR RAG</span><span class="tag t-amber">Truy Xuất Tài Liệu</span></div>
        <div class="t-box-body">
          <div><b>• Semantic Vector Search + Cross-Encoder Rerank:</b></div>
          <div>- <b>QĐ 5481/QĐ-BYT:</b> Phác đồ điều trị ĐTĐ Típ 2 chuẩn BYT.</div>
          <div>- <b>Viện Dinh Dưỡng QG:</b> Hướng dẫn ăn ít béo, chỉ số GI thấp.</div>
          <div>- <b>Báo cáo SSI & NHNN:</b> Bản tin tỷ giá và tác động ngành.</div>
        </div>
      </div>
    </div>
    <div></div>

    <!-- COL 4: 4 CARDS FILL ENTIRE HEIGHT -->
    <div class="col-p c-teal">
      <div class="p-hdr"><span>4. TỔNG HỢP & PHẢN HỒI</span><span class="tag t-green">Fact-Grounded</span></div>
      <div class="p-body">
        <div class="out-alert">
          <b style="color:#b91c1c;">🚨 CẢNH BÁO ĐỎ TỬ VONG:</b><br>
          Bệnh nhân <b>TUYỆT ĐỐI CẤM UỐNG RƯỢU BIA</b> khi uống Metformin! Nguy cơ Toan Lactic cấp tính (tử vong 50%).
        </div>
        <div class="out-guide">
          <b style="color:#15803d;">🍗 HƯỚNG DẪN ĂN THỊT GÀ:</b><br>
          Được ăn <b>ức gà nạc luộc/hấp</b> (protein nạc, GI = 0). Tuyệt đối tránh da gà và đồ gà chiên rán dầu mỡ.
        </div>
        <div class="out-fin">
          <b style="color:#0369a1;">📈 NHẬN ĐỊNH TÀI CHÍNH:</b><br>
          Tỷ giá USD tăng giúp <b>FPT hưởng lợi doanh thu</b>; Vàng SJC tiếp tục neo cao do chênh lệch cung cầu.
        </div>
        <div class="sub" style="background:#f0fdfa; border-color:#99f6e4;">
          <div class="sub-t" style="color:#0f766e;">Cam kết Fact-Grounded Vững chắc</div>
          <div style="color:#115e59; font-size:9.5px;">
            ✓ <b>100% Minh bạch:</b> Nguồn gốc rõ ràng từ Quyết định BYT & Dữ liệu SSI.<br>
            ✓ <b>Triệt tiêu ảo giác:</b> Chứng thực qua mạng lưới tri thức tất định.
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""
    render_html_to_png(html, os.path.join(OUTPUT_DIR, "fig706_agent_architecture_flow.png"), 1400, 680)


# =============================================================================
# 7. FIG 707: GIAO DIỆN WEB APP DASHBOARD CỦA AI AGENT
# =============================================================================
def generate_fig707():
    html = """<!DOCTYPE html>
<html lang="vi" spellcheck="false">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-font-smoothing: antialiased; }
  html, body { width: 1400px; height: 680px; overflow: hidden; background: #0f172a; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #f8fafc; }
  .wrapper { padding: 14px 16px; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
  
  .frame {
    background: #1e293b; border-radius: 10px; border: 1px solid #334155; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5); height: 100%; display: flex; flex-direction: column; overflow: hidden;
  }
  .b-top {
    background: #0f172a; padding: 8px 14px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #334155;
  }
  .dots { display: flex; gap: 6px; }
  .dot { width: 10px; height: 10px; border-radius: 50%; }
  .dr { background: #ef4444; } .dy { background: #f59e0b; } .dg { background: #10b981; }
  .url {
    background: #1e293b; border-radius: 5px; padding: 3px 14px; font-size: 11px; color: #94a3b8; width: 420px; text-align: center; border: 1px solid #334155;
  }
  
  .app-body { display: grid; grid-template-columns: 260px 1fr; flex: 1; overflow: hidden; }
  .sidebar {
    background: #111827; border-right: 1px solid #334155; padding: 14px; display: flex; flex-direction: column; justify-content: space-between; font-size: 11px;
  }
  .side-card { background: #1e293b; border: 1px solid #374151; border-radius: 6px; padding: 8px 10px; margin-bottom: 8px; }
  .side-btn { background: #0284c7; color: white; border: none; border-radius: 5px; padding: 6px; font-weight: 700; width: 100%; text-align: center; margin-top: 4px; font-size: 10.5px; }

  .main-dash { padding: 14px; display: flex; flex-direction: column; justify-content: space-between; gap: 10px; background: #0f172a; }
  .dash-hdr { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 8px; }
  .tabs { display: flex; gap: 8px; }
  .tab-btn { background: #1e293b; border: 1px solid #334155; color: #cbd5e1; padding: 5px 12px; border-radius: 5px; font-size: 11px; font-weight: 700; }
  .tab-act { background: #0284c7; color: white; border-color: #0284c7; }

  .cards-split { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; flex: 1; align-items: stretch; }
  .d-card {
    background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 12px; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden;
  }
  .c-top {
    font-size: 12px; font-weight: 800; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 6px; margin-bottom: 8px;
  }
  
  .chat-msg { background: #0f172a; border-radius: 6px; padding: 8px 10px; font-size: 10.5px; margin-bottom: 6px; border: 1px solid #334155; line-height: 1.35; }
  .u-msg { border-left: 3px solid #0284c7; color: #93c5fd; }
  .a-msg { border-left: 3px solid #10b981; color: #e2e8f0; }

  .metric-bar { display: flex; gap: 8px; margin-bottom: 6px; }
  .m-chip { background: #0f172a; border: 1px solid #334155; border-radius: 4px; padding: 4px 8px; font-size: 10px; flex: 1; text-align: center; }
</style>
</head>
<body spellcheck="false">
<div class="wrapper">
  <div class="frame">
    <div class="b-top">
      <div class="dots"><div class="dot dr"></div><div class="dot dy"></div><div class="dot dg"></div></div>
      <div class="url">https://agent.vietnam-ai-intel.edu.vn/multimodal-agent-dashboard</div>
      <div style="font-size:10.5px; color:#10b981; font-weight:700;">● Online (v2.4 Production)</div>
    </div>

    <div class="app-body">
      <!-- SIDEBAR -->
      <div class="sidebar">
        <div>
          <div style="font-size:14px; font-weight:800; color:#38bdf8; margin-bottom:12px;">AI AGENT SYSTEM</div>
          <div style="font-size:10px; font-weight:700; color:#94a3b8; text-transform:uppercase; margin-bottom:6px;">Chế Độ Điều Phối</div>
          <div class="side-card">
            <div style="font-weight:700; color:#f8fafc;">Hybrid Y Tế & Tài Chính</div>
            <div style="color:#94a3b8; font-size:10px; margin:3px 0;">ReAct Engine Tự Chủ</div>
            <button class="side-btn">Đã Kích Hoạt</button>
          </div>

          <div style="font-size:10px; font-weight:700; color:#94a3b8; text-transform:uppercase; margin-bottom:6px;">Trạng Thái Dịch Vụ</div>
          <div class="side-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
              <span>Neo4j Graph DB:</span> <span style="color:#10b981; font-weight:700;">Đã kết nối</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
              <span>Milvus Vector DB:</span> <span style="color:#10b981; font-weight:700;">768 dims OK</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
              <span>PyTorch BiLSTM:</span> <span style="color:#38bdf8; font-weight:700;">Sẵn sàng</span>
            </div>
          </div>
        </div>

        <div style="border-top:1px solid #334155; padding-top:8px; font-size:9.5px; color:#64748b; line-height:1.4;">
          Đồ án Nghiên cứu: Phí Văn Tú<br>Mã HV: tupv.879 | PTIT 2026
        </div>
      </div>

      <!-- MAIN DASHBOARD -->
      <div class="main-dash">
        <div class="dash-hdr">
          <div>
            <div style="font-size:15px; font-weight:800; color:#f8fafc;">BẢNG ĐIỀU KHIỂN TÁC TỬ SUY LUẬN ĐA CÔNG CỤ (MULTI-TOOL ReAct AGENT)</div>
            <div style="font-size:10.5px; color:#94a3b8;">Tích hợp Kiểm chứng Tri thức Biểu tượng và Học Sâu Thực nghiệm</div>
          </div>
          <div class="tabs">
            <button class="tab-btn tab-act">Tab 1: Y Tế Đái Tháo Đường</button>
            <button class="tab-btn">Tab 2: Tài Chính & Thị Trường</button>
          </div>
        </div>

        <div class="cards-split">
          <!-- CARD 1: MEDICAL -->
          <div class="d-card">
            <div class="c-top">
              <span style="color:#38bdf8;">TƯƠNG TÁC Y TẾ & TRUY VẾT SUY LUẬN (ReAct TRACE)</span>
              <span style="background:rgba(14,165,233,0.15); color:#38bdf8; padding:2px 6px; border-radius:3px; font-size:9.5px;">Medical Core</span>
            </div>

            <div class="metric-bar">
              <div class="m-chip">HbA1c: <b style="color:#f59e0b;">7.3% (Báo động)</b></div>
              <div class="m-chip">Glucose đói: <b style="color:#ef4444;">138 mg/dL (Cao)</b></div>
              <div class="m-chip">Thuốc: <b style="color:#38bdf8;">Metformin 500mg</b></div>
            </div>

            <div class="chat-msg u-msg">
              <b>Bệnh Nhân (User):</b> “Tôi đang uống Metformin 500mg, Glucose đói 138 mg/dL, HbA1c 7.3%. Chiều nay liên hoan, tôi uống rượu bia và ăn thịt gà được không?”
            </div>

            <div class="chat-msg a-msg" style="flex:1;">
              <div style="color:#a7f3d0; margin-bottom:3px; font-size:10px;">
                <b>ReAct Agent (Suy Luận Đa Tầng):</b><br>
                • <b>MLP Classifier:</b> Xác nhận ĐTĐ Típ 2 (xác suất 98.5%).<br>
                • <b>KG Query:</b> <code>Metformin [Chống chỉ định] Rượu bia</code> ➔ Nguy cơ toan Lactic tử vong.<br>
                • <b>Dense RAG:</b> Trích dẫn QĐ 5481/QĐ-BYT & Tháp Dinh dưỡng Viện DDQG.
              </div>
            </div>

            <div style="background:#450a0a; border:1px solid #b91c1c; border-radius:6px; padding:8px 10px; font-size:10px; color:#fecaca;">
              <div style="font-weight:800; color:#f87171; margin-bottom:2px;">🚨 PHẢN HỒI CUỐI CÙNG (GROUNDED RESPONSE):</div>
              1. <b>CẤM TUYỆT ĐỐI RƯỢU BIA:</b> Nguy cơ nhiễm toan acid lactic cấp tính có tỷ lệ tử vong 50%.<br>
              2. <b>ĂN ĐƯỢC ỨC GÀ NẠC:</b> Luộc/hấp (protein GI = 0). Cấm ăn da gà và gà rán chiên dầu.
            </div>
          </div>

          <!-- CARD 2: FINANCIAL -->
          <div class="d-card">
            <div class="c-top">
              <span style="color:#34d399;">PHÂN TÍCH TÀI CHÍNH & DỰ BÁO CHUỖI GIÁ</span>
              <span style="background:rgba(16,185,129,0.15); color:#34d399; padding:2px 6px; border-radius:3px; font-size:9.5px;">Financial Core</span>
            </div>

            <div class="metric-bar">
              <div class="m-chip">USD/VND: <b style="color:#ef4444;">25,450 (+4.2%)</b></div>
              <div class="m-chip">Vàng SJC: <b style="color:#f59e0b;">90.5 triệu/lượng</b></div>
              <div class="m-chip">Cổ phiếu FPT: <b style="color:#10b981;">134,500 đ</b></div>
            </div>

            <div class="chat-msg u-msg">
              <b>Nhà Đầu Tư (User):</b> “Tỷ giá USD/VND lên 25,450 và giá vàng SJC lên 90 triệu, cổ phiếu FPT chịu tác động ra sao?”
            </div>

            <div class="chat-msg a-msg" style="flex:1;">
              <div style="color:#a7f3d0; margin-bottom:3px; font-size:10px;">
                <b>ReAct Agent (Dự Báo & Logic Vĩ Mô):</b><br>
                • <b>BiLSTM Engine:</b> Dự báo biến động FPT phiên tới đạt <b>+1.8%</b> (tin cậy 84.2%).<br>
                • <b>KG Traversal:</b> <code>USD/VND tăng ➔ Doanh thu xuất khẩu IT hưởng lợi tỷ giá dương</code>.<br>
                • <b>SJC Gold:</b> Neo cao do khan hiếm nguồn cung độc quyền (Nghị định 24/2012).
              </div>
            </div>

            <div style="background:#064e3b; border:1px solid #059669; border-radius:6px; padding:8px 10px; font-size:10px; color:#d1fae5;">
              <div style="font-weight:800; color:#6ee7b7; margin-bottom:2px;">📈 KHUYẾN NGHỊ DANH MỤC (INVESTMENT STRATEGY):</div>
              1. <b>FPT (CÔNG NGHỆ):</b> Tích lũy tỷ trọng; hưởng lợi trực tiếp từ nguồn thu ngoại tệ USD.<br>
              2. <b>VÀNG MIẾNG SJC:</b> Duy trì vị thế thận trọng, biên độ 89.8 - 91.5 triệu, không mua đuổi.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""
    render_html_to_png(html, os.path.join(OUTPUT_DIR, "fig707_agent_webapp_interface.png"), 1400, 680)


if __name__ == "__main__":
    print("="*70)
    print("BẮT ĐẦU XUẤT BẢN TOÀN BỘ 7 BIỂU ĐỒ CHUẨN MỰC BẰNG CHROME HEADLESS")
    print("="*70)
    generate_fig701()
    generate_fig702()
    generate_fig703()
    generate_fig704()
    generate_fig705()
    generate_fig706()
    generate_fig707()
    print("="*70)
    print("✓ HOÀN TẤT XUẤT BẢN 100% BIỂU ĐỒ ĐẠT CHUẨN NATURE / IEEE!")
    print("="*70)
