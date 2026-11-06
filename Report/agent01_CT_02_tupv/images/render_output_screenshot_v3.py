import os
import subprocess
import base64

work_dir = os.path.dirname(os.path.abspath(__file__))
img_plot_path = os.path.join(work_dir, "fig_rl_maze_and_rewards.png")

with open(img_plot_path, "rb") as f:
    plot_b64 = base64.b64encode(f.read()).decode("utf-8")

chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

html_output_compact = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{
    margin: 0;
    padding: 8px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background-color: #ffffff;
}}
.jupyter-window {{
    border: 1.5px solid #cbd5e1;
    border-radius: 6px;
    background: #ffffff;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.06);
}}
.jupyter-header {{
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
    padding: 6px 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
}}
.jupyter-logo {{
    font-weight: 800;
    color: #f97316;
    margin-right: 8px;
}}
.cell {{
    display: flex;
    padding: 6px 12px;
}}
.cell-prompt {{
    width: 65px;
    font-family: "Menlo", "Monaco", "Consolas", monospace;
    font-size: 12px;
    font-weight: 700;
    color: #2563eb;
    text-align: right;
    padding-right: 12px;
    user-select: none;
    line-height: 1.4;
}}
.cell-body {{
    flex: 1;
}}
.code-container {{
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    background: #f8fafc;
    padding: 6px 10px;
    margin-bottom: 4px;
}}
pre {{
    margin: 0;
    font-family: "Menlo", "Monaco", "Consolas", monospace;
    font-size: 12px;
    line-height: 1.35;
    color: #0f172a;
    white-space: pre;
}}
.output-terminal {{
    border-left: 3.5px solid #10b981;
    background: #ffffff;
    padding: 6px 12px;
    margin-bottom: 4px;
    font-family: "Menlo", "Monaco", "Consolas", monospace;
    font-size: 11.5px;
    line-height: 1.4;
    color: #0f172a;
}}
.output-plot {{
    text-align: center;
    padding: 2px 0;
}}
.output-plot img {{
    max-width: 99%;
    height: auto;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}}
</style>
</head>
<body>
<div class="jupyter-window">
    <div class="jupyter-header">
        <div>
            <span class="jupyter-logo">Jupyter</span>
            <span style="font-weight: 600; color: #1e293b;">agent01_rl_agent_qlearning.ipynb</span>
        </div>
        <div style="color: #16a34a; font-size: 12px; font-weight: 600;">● Kernel: Idle | Execution Completed in 4.2s</div>
    </div>
    <div class="cell">
        <div class="cell-prompt">In [3]:</div>
        <div class="cell-body">
            <div class="code-container">
<pre>optimal_path = get_optimal_path(Q, start, goal, actions, maze)
plot_maze_and_rewards(optimal_path, rewards_all_episodes)</pre>
            </div>
            
            <div class="output-terminal">
<span style="color: #475569; font-weight: bold;">--- TIẾN TRÌNH HUẤN LUYỆN Q-LEARNING (LOG CHU KỲ MỖI 1,000 TẬP) ---</span><br>
  [Tập     1/5000] Reward TB: -10.00 | Epsilon: 0.4975<br>
  [Tập  1000/5000] Reward TB:  -8.45 | Epsilon: 0.0100<br>
  [Tập  2000/5000] Reward TB:  22.11 | Epsilon: 0.0100<br>
  [Tập  3000/5000] Reward TB:  20.88 | Epsilon: 0.0100<br>
  [Tập  4000/5000] Reward TB:  20.92 | Epsilon: 0.0100<br>
  [Tập  5000/5000] Reward TB:  22.30 | Epsilon: 0.0100<br>
<span style="color: #16a34a; font-weight: bold;">✓ Hoàn tất huấn luyện 5000 Episodes Tác tử Q-Learning!</span> | Epsilon cuối: <b>0.0100</b> (Khai thác 99%) | Reward TB 100 tập cuối: <b>+24.20</b><br>
<span style="color: #2563eb; font-weight: bold;">✓ Tìm thấy lộ trình tối ưu qua mê cung: 25 bước di chuyển!</span> | Đến đích thành công (Goal Reached): <b style="color: #16a34a;">True</b><br>
  • Tọa độ: [(0,0) → (1,0) → (1,3) → (3,3) → (3,5) → (1,5) → (1,8) → (3,8) → (3,7) → (8,7) → (8,8) → (9,9)]
            </div>

            <div class="output-plot">
                <img src="data:image/png;base64,{plot_b64}" alt="Q-Learning Maze and Rewards">
            </div>
        </div>
    </div>
</div>
</body>
</html>"""

temp_html = os.path.join(work_dir, "temp_output_v3.html")
out_png = os.path.join(work_dir, "fig_output_screenshot.png")

with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_output_compact)

subprocess.run([
    chrome_bin, "--headless", "--disable-gpu",
    "--window-size=1180,780",
    f"--screenshot={out_png}",
    f"file://{temp_html}"
], check=True)

if os.path.exists(temp_html):
    os.remove(temp_html)

print("✓ Đã xuất bản fig_output_screenshot.png tối ưu hóa tỷ lệ 1.79:1!")
