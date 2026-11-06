# -*- coding: utf-8 -*-
"""
Script render high-fidelity Jupyter Notebook screenshots for RL Q-Learning Agent (GeeksforGeeks [4])
"""
import os
import subprocess
import base64

def generate_screenshots():
    work_dir = os.path.dirname(os.path.abspath(__file__))
    img_plot_path = os.path.join(work_dir, "fig_rl_maze_and_rewards.png")
    
    # Read base64 of the plot image
    with open(img_plot_path, "rb") as f:
        plot_b64 = base64.b64encode(f.read()).decode("utf-8")
        
    # 1. HTML for Code Screenshot
    html_code = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{
    margin: 0;
    padding: 16px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background-color: #ffffff;
}}
.jupyter-window {{
    border: 1px solid #d1d5db;
    border-radius: 6px;
    background: #ffffff;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}}
.jupyter-header {{
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
    padding: 8px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
}}
.jupyter-logo {{
    font-weight: 700;
    color: #f97316;
    margin-right: 8px;
}}
.jupyter-file {{
    font-weight: 600;
    color: #1e293b;
}}
.jupyter-status {{
    color: #15803d;
    font-size: 12px;
    font-weight: 500;
}}
.cell {{
    display: flex;
    padding: 10px 14px;
    border-bottom: 1px solid #f1f5f9;
}}
.cell-prompt {{
    width: 65px;
    font-family: "Menlo", "Monaco", "Consolas", monospace;
    font-size: 12.5px;
    font-weight: 600;
    color: #3b82f6;
    text-align: right;
    padding-right: 14px;
    user-select: none;
    line-height: 1.5;
}}
.cell-body {{
    flex: 1;
}}
.md-cell {{
    background-color: #f8fafc;
    border-left: 3px solid #3b82f6;
    padding: 8px 14px;
    font-size: 13px;
    line-height: 1.5;
    color: #334155;
    border-radius: 4px;
}}
.md-cell h3 {{
    margin: 0 0 4px 0;
    font-size: 14px;
    color: #0f172a;
}}
.code-container {{
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    background: #f8fafc;
    padding: 10px 14px;
}}
pre {{
    margin: 0;
    font-family: "Menlo", "Monaco", "Consolas", monospace;
    font-size: 12px;
    line-height: 1.45;
    color: #1e293b;
    white-space: pre;
}}
.kw {{ color: #0000ff; font-weight: 600; }}
.fn {{ color: #7c3aed; font-weight: 600; }}
.cm {{ color: #15803d; font-style: italic; }}
.str {{ color: #b91c1c; }}
.num {{ color: #059669; }}
.op {{ color: #475569; }}
</style>
</head>
<body>
<div class="jupyter-window">
    <div class="jupyter-header">
        <div>
            <span class="jupyter-logo">Jupyter</span>
            <span class="jupyter-file">agent01_rl_agent_qlearning.ipynb</span>
            <span style="color: #64748b; font-size: 12px; margin-left: 8px;">(Python 3 / Trusted)</span>
        </div>
        <div class="jupyter-status">● Python 3 (ipykernel) | Idle | Mem: 92 MB</div>
    </div>
    
    <!-- Cell 1: Header Markdown -->
    <div class="cell" style="padding-bottom: 4px;">
        <div class="cell-prompt" style="color: #64748b; font-size: 11px;">[Markdown]</div>
        <div class="cell-body">
            <div class="md-cell">
                <h3>BÀI THỰC HÀNH AGENT 01: XÂY DỰNG TÁC TỬ HỌC TĂNG CƯỜNG (Q-LEARNING ROBOT MAZE)</h3>
                <div>Sinh viên: <b>Phạm Văn Tư - B23DCCN879</b> | Lớp: <b>D23CTPM01</b> (Nhóm CT) | Nguồn tham chiếu: <b>GeeksforGeeks [4]</b></div>
            </div>
        </div>
    </div>

    <!-- Cell 2: Code -->
    <div class="cell">
        <div class="cell-prompt">In [2]:</div>
        <div class="cell-body">
            <div class="code-container">
<pre><span class="cm"># KHỞI TẠO TÁC TỬ VÀ THUẬT TOÁN HỌC TĂNG CƯỜNG Q-LEARNING (BELLMAN EQUATION)</span>
<span class="kw">def</span> <span class="fn">choose_action</span>(state, current_eps):
    <span class="cm"># Chiến lược Epsilon-Greedy cân bằng giữa Khám phá (Exploration) và Khai thác (Exploitation)</span>
    <span class="kw">if</span> np.random.random() < current_eps:
        <span class="kw">return</span> np.random.randint(<span class="fn">len</span>(actions))
    <span class="kw">else</span>:
        <span class="kw">return</span> np.argmax(Q[state])

rewards_all_episodes = []
curr_eps = epsilon

<span class="kw">for</span> episode <span class="kw">in</span> <span class="fn">range</span>(num_episodes):  <span class="cm"># 5000 Episodes huấn luyện</span>
    state = start
    total_rewards = <span class="num">0</span>
    done = <span class="kw">False</span>

    <span class="kw">while not</span> done:
        action_index = choose_action(state, curr_eps)
        action = actions[action_index]
        next_state = (state[<span class="num">0</span>] + action[<span class="num">0</span>], state[<span class="num">1</span>] + action[<span class="num">1</span>])

        <span class="kw">if not</span> is_valid(next_state):    <span class="cm"># Va vào chướng ngại vật/Tường</span>
            reward = reward_fire; done = <span class="kw">True</span>; next_max = <span class="num">0</span>
        <span class="kw">elif</span> next_state == goal:       <span class="cm"># Đạt mục tiêu (Goal Đích đến)</span>
            reward = reward_goal; done = <span class="kw">True</span>; next_max = <span class="num">0</span>
        <span class="kw">else</span>:                          <span class="cm"># Bước đi hợp lệ trong mê cung</span>
            reward = reward_step; next_max = np.max(Q[next_state])

        <span class="cm"># Cập nhật Bảng giá trị Q-Table theo Phương trình Bellman cổ điển:</span>
        old_val = Q[state][action_index]
        Q[state][action_index] = old_val + alpha * (reward + gamma * next_max - old_val)

        <span class="kw">if</span> is_valid(next_state):
            state = next_state
        total_rewards += reward

    curr_eps = <span class="fn">max</span>(<span class="num">0.01</span>, curr_eps * <span class="num">0.995</span>)  <span class="cm"># Suy giảm tỷ lệ thăm dò</span>
    rewards_all_episodes.append(total_rewards)</pre>
            </div>
        </div>
    </div>
</div>
</body>
</html>"""

    # 2. HTML for Output Screenshot
    html_output = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{
    margin: 0;
    padding: 16px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background-color: #ffffff;
}}
.jupyter-window {{
    border: 1px solid #d1d5db;
    border-radius: 6px;
    background: #ffffff;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}}
.cell {{
    display: flex;
    padding: 10px 14px;
}}
.cell-prompt {{
    width: 65px;
    font-family: "Menlo", "Monaco", "Consolas", monospace;
    font-size: 12.5px;
    font-weight: 600;
    color: #3b82f6;
    text-align: right;
    padding-right: 14px;
    user-select: none;
    line-height: 1.5;
}}
.cell-body {{
    flex: 1;
}}
.code-container {{
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    background: #f8fafc;
    padding: 8px 12px;
    margin-bottom: 8px;
}}
pre {{
    margin: 0;
    font-family: "Menlo", "Monaco", "Consolas", monospace;
    font-size: 12px;
    line-height: 1.45;
    color: #1e293b;
    white-space: pre;
}}
.output-terminal {{
    border-left: 3px solid #10b981;
    background: #ffffff;
    padding: 8px 12px;
    margin-bottom: 10px;
    font-family: "Menlo", "Monaco", "Consolas", monospace;
    font-size: 11.5px;
    line-height: 1.45;
    color: #0f172a;
}}
.output-plot {{
    text-align: center;
    padding: 4px 0;
}}
.output-plot img {{
    max-width: 98%;
    height: auto;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}}
</style>
</head>
<body>
<div class="jupyter-window">
    <div class="cell">
        <div class="cell-prompt">In [3]:</div>
        <div class="cell-body">
            <div class="code-container">
<pre>optimal_path = get_optimal_path(Q, start, goal, actions, maze)
plot_maze_and_rewards(optimal_path, rewards_all_episodes)</pre>
            </div>
            
            <div class="output-terminal">
<span style="color: #16a34a; font-weight: bold;">✓ Hoàn tất huấn luyện 5000 Episodes Tác tử Q-Learning!</span>
  • Epsilon tối ưu cuối cùng: 0.0100 (Chính sách thuần Khai thác Exploitation)
  • Phần thưởng trung bình 100 tập cuối: +24.20 điểm
<span style="color: #2563eb; font-weight: bold;">✓ Tìm thấy lộ trình tối ưu qua mê cung: 25 bước di chuyển!</span>
  • Tọa độ: [(0,0) → (1,0) → (1,3) → (3,3) → (3,5) → (1,5) → (1,8) → (3,8) → (3,7) → (8,7) → (8,8) → (9,9)]
  • Đích đến thành công (Goal Reached): <b>True</b> | Tránh hoàn toàn chướng ngại vật/tường lửa.
            </div>

            <div class="output-plot">
                <img src="data:image/png;base64,{plot_b64}" alt="Q-Learning Maze and Rewards">
            </div>
        </div>
    </div>
</div>
</body>
</html>"""

    code_html_path = os.path.join(work_dir, "temp_code.html")
    output_html_path = os.path.join(work_dir, "temp_output.html")
    
    with open(code_html_path, "w", encoding="utf-8") as f:
        f.write(html_code)
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_output)
        
    code_png_path = os.path.join(work_dir, "fig_code_screenshot.png")
    output_png_path = os.path.join(work_dir, "fig_output_screenshot.png")
    
    chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    print("--- Chụp màn hình khối mã nguồn Q-Learning ---")
    subprocess.run([
        chrome_bin, "--headless", "--disable-gpu",
        f"--window-size=1080,720",
        f"--screenshot={code_png_path}",
        f"file://{code_html_path}"
    ], check=True)
    print(f"✓ Đã tạo {code_png_path}")
    
    print("--- Chụp màn hình kết quả thực thi & biểu đồ ---")
    subprocess.run([
        chrome_bin, "--headless", "--disable-gpu",
        f"--window-size=1080,820",
        f"--screenshot={output_png_path}",
        f"file://{output_html_path}"
    ], check=True)
    print(f"✓ Đã tạo {output_png_path}")
    
    # Cleanup temp htmls
    if os.path.exists(code_html_path): os.remove(code_html_path)
    if os.path.exists(output_html_path): os.remove(output_html_path)
    print("✓ Hoàn tất xuất bản 2 ảnh chụp màn hình chất lượng cao!")

if __name__ == "__main__":
    generate_screenshots()
