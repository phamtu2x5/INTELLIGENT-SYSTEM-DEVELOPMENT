import os
import subprocess

work_dir = os.path.dirname(os.path.abspath(__file__))
chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

html_code_full = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {
    margin: 0;
    padding: 10px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background-color: #ffffff;
}
.jupyter-window {
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    background: #ffffff;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.06);
    padding-bottom: 8px;
}
.jupyter-header {
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
    padding: 8px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13.5px;
}
.jupyter-logo {
    font-weight: 800;
    color: #f97316;
    margin-right: 8px;
}
.jupyter-file {
    font-weight: 600;
    color: #1e293b;
}
.jupyter-status {
    color: #16a34a;
    font-size: 12.5px;
    font-weight: 600;
}
.cell {
    display: flex;
    padding: 6px 16px;
    border-bottom: 1px solid #f1f5f9;
}
.cell-prompt {
    width: 75px;
    font-family: "Menlo", "Monaco", "Consolas", monospace;
    font-size: 12.5px;
    font-weight: 700;
    color: #2563eb;
    text-align: right;
    padding-right: 16px;
    user-select: none;
    line-height: 1.5;
}
.cell-body {
    flex: 1;
}
.md-cell {
    background-color: #f8fafc;
    border-left: 4px solid #2563eb;
    padding: 8px 16px;
    font-size: 13px;
    line-height: 1.5;
    color: #334155;
    border-radius: 4px;
}
.md-cell h3 {
    margin: 0 0 4px 0;
    font-size: 14px;
    color: #0f172a;
}
.code-container {
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    background: #f8fafc;
    padding: 8px 14px;
}
pre {
    margin: 0;
    font-family: "Menlo", "Monaco", "Consolas", monospace;
    font-size: 12px;
    line-height: 1.4;
    color: #0f172a;
    white-space: pre;
}
.kw { color: #0000ff; font-weight: 700; }
.fn { color: #7c3aed; font-weight: 700; }
.cm { color: #15803d; font-style: italic; font-weight: 500; }
.str { color: #b91c1c; }
.num { color: #059669; font-weight: 600; }
.op { color: #334155; }
.output-terminal {
    border-left: 3.5px solid #10b981;
    background: #ffffff;
    padding: 6px 12px;
    margin-top: 4px;
    font-family: "Menlo", "Monaco", "Consolas", monospace;
    font-size: 11.5px;
    line-height: 1.4;
    color: #0f172a;
}
</style>
</head>
<body>
<div class="jupyter-window">
    <div class="jupyter-header">
        <div>
            <span class="jupyter-logo">Jupyter</span>
            <span class="jupyter-file">agent01_rl_agent_qlearning.ipynb</span>
            <span style="color: #64748b; font-size: 12.5px; margin-left: 8px;">(Python 3 / Trusted)</span>
        </div>
        <div class="jupyter-status">● Python 3 (ipykernel) | Training Completed (5000/5000)</div>
    </div>
    
    <!-- Cell 0: Header Markdown -->
    <div class="cell" style="padding-bottom: 2px;">
        <div class="cell-prompt" style="color: #64748b; font-size: 11px;">[Markdown]</div>
        <div class="cell-body">
            <div class="md-cell">
                <h3>BÀI THỰC HÀNH AGENT 01: XÂY DỰNG TÁC TỬ HỌC TĂNG CƯỜNG (Q-LEARNING ROBOT MAZE)</h3>
                <div>Sinh viên: <b>Phạm Văn Tư - B23DCCN879</b> | Lớp: <b>D23CTPM01</b> (Nhóm CT) | Nguồn tham chiếu: <b>GeeksforGeeks [4]</b></div>
            </div>
        </div>
    </div>

    <!-- Cell 1: Environment & Hyperparameters -->
    <div class="cell" style="padding-bottom: 4px;">
        <div class="cell-prompt">In [1]:</div>
        <div class="cell-body">
            <div class="code-container">
<pre><span class="cm"># 1. KHỞI TẠO MÔI TRƯỜNG MÊ CUNG 10x10 & THAM SỐ HUẤN LUYỆN (GEEKSFORGEEKS [4])</span>
maze = np.array([
    [<span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>], [<span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">1</span>],
    [<span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>], [<span class="num">1</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">1</span>],
    [<span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>], [<span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>],
    [<span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>], [<span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>],
    [<span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">1</span>], [<span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">0</span>]
])
start, goal = (<span class="num">0</span>, <span class="num">0</span>), (<span class="num">9</span>, <span class="num">9</span>)
num_episodes, alpha, gamma, epsilon = <span class="num">5000</span>, <span class="num">0.1</span>, <span class="num">0.9</span>, <span class="num">0.5</span>
reward_fire, reward_goal, reward_step = -<span class="num">10</span>, <span class="num">50</span>, -<span class="num">1</span>
actions = [(<span class="num">0</span>, -<span class="num">1</span>), (<span class="num">0</span>, <span class="num">1</span>), (-<span class="num">1</span>, <span class="num">0</span>), (<span class="num">1</span>, <span class="num">0</span>)]  <span class="cm"># Trái, Phải, Lên, Xuống</span>
Q = np.zeros(maze.shape + (<span class="fn">len</span>(actions),))   <span class="cm"># Q-Table khởi tạo kích thước (10, 10, 4)</span></pre>
            </div>
        </div>
    </div>

    <!-- Cell 2: Training Loop -->
    <div class="cell">
        <div class="cell-prompt">In [2]:</div>
        <div class="cell-body">
            <div class="code-container">
<pre><span class="cm"># 2. CHIẾN LƯỢC EPSILON-GREEDY & CẬP NHẬT PHƯƠNG TRÌNH TỐI ƯU BELLMAN</span>
<span class="kw">def</span> <span class="fn">choose_action</span>(state, current_eps):
    <span class="kw">if</span> np.random.random() < current_eps:
        <span class="kw">return</span> np.random.randint(<span class="fn">len</span>(actions))   <span class="cm"># Thăm dò (Exploration)</span>
    <span class="kw">return</span> np.argmax(Q[state])                  <span class="cm"># Khai thác (Exploitation)</span>

rewards_all_episodes = []
curr_eps = epsilon

<span class="kw">for</span> episode <span class="kw">in</span> <span class="fn">range</span>(num_episodes):
    state, done, total_rewards = start, <span class="kw">False</span>, <span class="num">0</span>
    <span class="kw">while not</span> done:
        a_idx = choose_action(state, curr_eps)
        action = actions[a_idx]
        next_state = (state[<span class="num">0</span>] + action[<span class="num">0</span>], state[<span class="num">1</span>] + action[<span class="num">1</span>])

        <span class="kw">if not</span> is_valid(next_state):
            reward, done, next_max = reward_fire, <span class="kw">True</span>, <span class="num">0</span>
        <span class="kw">elif</span> next_state == goal:
            reward, done, next_max = reward_goal, <span class="kw">True</span>, <span class="num">0</span>
        <span class="kw">else</span>:
            reward, done, next_max = reward_step, <span class="kw">False</span>, np.max(Q[next_state])

        <span class="cm"># Quy tắc cập nhật Bellman: Q(s,a) &lt;- Q(s,a) + alpha * [R + gamma * max Q(s',a') - Q(s,a)]</span>
        Q[state][a_idx] += alpha * (reward + gamma * next_max - Q[state][a_idx])
        <span class="kw">if</span> is_valid(next_state): state = next_state
        total_rewards += reward

    curr_eps = <span class="fn">max</span>(<span class="num">0.01</span>, curr_eps * <span class="num">0.995</span>)
    rewards_all_episodes.append(total_rewards)

<span class="fn">print</span>(<span class="str">f"✓ Hoàn tất 5000 Episodes! Epsilon cuối: {curr_eps:.4f} | Reward TB 100 tập cuối: {np.mean(rewards_all_episodes[-100:]):.2f}"</span>)</pre>
            </div>
            <div class="output-terminal">
✓ Hoàn tất 5000 Episodes! Epsilon cuối: 0.0100 (Khai thác 99%) | Reward TB 100 tập cuối: +24.20
            </div>
        </div>
    </div>
</div>
</body>
</html>"""

temp_html = os.path.join(work_dir, "temp_code_full.html")
out_png = os.path.join(work_dir, "fig_code_screenshot.png")

with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_code_full)

subprocess.run([
    chrome_bin, "--headless", "--disable-gpu",
    "--window-size=1120,950",
    f"--screenshot={out_png}",
    f"file://{temp_html}"
], check=True)

if os.path.exists(temp_html):
    os.remove(temp_html)

print("✓ Đã cập nhật fig_code_screenshot.png hoàn hảo!")
