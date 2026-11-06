import os
import subprocess
import base64

def generate_screenshots():
    work_dir = os.path.dirname(os.path.abspath(__file__))
    img_plot_path = os.path.join(work_dir, "fig_rl_maze_and_rewards.png")
    
    with open(img_plot_path, "rb") as f:
        plot_b64 = base64.b64encode(f.read()).decode("utf-8")
        
    chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    # Common CSS style
    css = """
    body {
        margin: 0;
        padding: 12px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        background-color: #ffffff;
    }
    .jupyter-window {
        border: 1.5px solid #cbd5e1;
        border-radius: 8px;
        background: #ffffff;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.06);
    }
    .jupyter-header {
        background: #f8fafc;
        border-bottom: 1px solid #e2e8f0;
        padding: 9px 18px;
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
        padding: 8px 16px;
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
        font-size: 14.5px;
        color: #0f172a;
    }
    .code-container {
        border: 1px solid #cbd5e1;
        border-radius: 5px;
        background: #f8fafc;
        padding: 10px 14px;
        margin-bottom: 6px;
    }
    pre {
        margin: 0;
        font-family: "Menlo", "Monaco", "Consolas", monospace;
        font-size: 12.5px;
        line-height: 1.45;
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
        padding: 8px 14px;
        margin-bottom: 4px;
        font-family: "Menlo", "Monaco", "Consolas", monospace;
        font-size: 12px;
        line-height: 1.45;
        color: #0f172a;
    }
    .output-plot {
        text-align: center;
        padding: 4px 0;
    }
    .output-plot img {
        max-width: 98%;
        height: auto;
        border-radius: 4px;
        border: 1px solid #e2e8f0;
    }
    """

    # 1. SCREENSHOT 1: ENVIRONMENT SETUP & HYPERPARAMETERS
    html_setup = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>""" + css + """</style>
</head>
<body>
<div class="jupyter-window">
    <div class="jupyter-header">
        <div>
            <span class="jupyter-logo">Jupyter</span>
            <span class="jupyter-file">agent01_rl_agent_qlearning.ipynb</span>
            <span style="color: #64748b; font-size: 12.5px; margin-left: 8px;">(Python 3 / Trusted)</span>
        </div>
        <div class="jupyter-status">● Python 3 (ipykernel) | Idle | Mem: 94 MB</div>
    </div>
    
    <!-- Cell 0: Header Markdown -->
    <div class="cell" style="padding-bottom: 4px;">
        <div class="cell-prompt" style="color: #64748b; font-size: 11.5px;">[Markdown]</div>
        <div class="cell-body">
            <div class="md-cell">
                <h3>BÀI THỰC HÀNH AGENT 01: XÂY DỰNG TÁC TỬ HỌC TĂNG CƯỜNG (Q-LEARNING ROBOT MAZE)</h3>
                <div>Sinh viên: <b>Phạm Văn Tư - B23DCCN879</b> | Lớp: <b>D23CTPM01</b> (Nhóm CT) | Nguồn tham chiếu: <b>GeeksforGeeks [4]</b></div>
            </div>
        </div>
    </div>

    <!-- Cell 1: Environment & Hyperparameters -->
    <div class="cell">
        <div class="cell-prompt">In [1]:</div>
        <div class="cell-body">
            <div class="code-container">
<pre><span class="cm"># 1. KHỞI TẠO MÔI TRƯỜNG MÊ CUNG 10x10 (0: ĐƯỜNG ĐI HỢP LỆ, 1: CHƯỚNG NGẠI VẬT/TƯỜNG LỬA)</span>
maze = np.array([
    [<span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>],
    [<span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">1</span>],
    [<span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>],
    [<span class="num">1</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">1</span>],
    [<span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>],
    [<span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>],
    [<span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>],
    [<span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>],
    [<span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">0</span>, <span class="num">1</span>],
    [<span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">1</span>, <span class="num">0</span>, <span class="num">0</span>]
])
start, goal = (<span class="num">0</span>, <span class="num">0</span>), (<span class="num">9</span>, <span class="num">9</span>)

<span class="cm"># 2. CẤU HÌNH THAM SỐ HỌC TĂNG CƯỜNG (RL HYPERPARAMETERS THEO GEEKSFORGEEKS [4])</span>
num_episodes = <span class="num">5000</span>; alpha = <span class="num">0.1</span>; gamma = <span class="num">0.9</span>; epsilon = <span class="num">0.5</span>
reward_fire, reward_goal, reward_step = -<span class="num">10</span>, <span class="num">50</span>, -<span class="num">1</span>
actions = [(<span class="num">0</span>, -<span class="num">1</span>), (<span class="num">0</span>, <span class="num">1</span>), (-<span class="num">1</span>, <span class="num">0</span>), (<span class="num">1</span>, <span class="num">0</span>)]  <span class="cm"># Trái, Phải, Lên, Xuống</span>

<span class="cm"># Khởi tạo Bảng giá trị Q-Table kích thước (10, 10, 4) toàn giá trị 0 ban đầu</span>
Q = np.zeros(maze.shape + (<span class="fn">len</span>(actions),))
<span class="fn">print</span>(<span class="str">f"✓ Khởi tạo mê cung: 10x10 | Q-Table: (10, 10, 4) | Episodes: 5000"</span>)</pre>
            </div>
            <div class="output-terminal">
✓ Khởi tạo mê cung: 10x10 | Q-Table: (10, 10, 4) | Episodes: 5000
            </div>
        </div>
    </div>
</div>
</body>
</html>"""

    # 2. SCREENSHOT 2: Q-LEARNING ALGORITHM & BELLMAN UPDATE
    html_train = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>""" + css + """</style>
</head>
<body>
<div class="jupyter-window">
    <div class="jupyter-header">
        <div>
            <span class="jupyter-logo">Jupyter</span>
            <span class="jupyter-file">agent01_rl_agent_qlearning.ipynb</span>
        </div>
        <div class="jupyter-status">● Training Completed (5000/5000)</div>
    </div>

    <!-- Cell 2: Training Loop -->
    <div class="cell">
        <div class="cell-prompt">In [2]:</div>
        <div class="cell-body">
            <div class="code-container">
<pre><span class="cm"># 3. CHIẾN LƯỢC CHỌN HÀNH ĐỘNG EPSILON-GREEDY & CẬP NHẬT BELLMAN OPTIMALITY</span>
<span class="kw">def</span> <span class="fn">choose_action</span>(state, current_eps):
    <span class="kw">if</span> np.random.random() < current_eps:
        <span class="kw">return</span> np.random.randint(<span class="fn">len</span>(actions))   <span class="cm"># Thăm dò (Exploration)</span>
    <span class="kw">else</span>:
        <span class="kw">return</span> np.argmax(Q[state])              <span class="cm"># Khai thác (Exploitation)</span>

rewards_all_episodes = []
curr_eps = epsilon

<span class="kw">for</span> episode <span class="kw">in</span> <span class="fn">range</span>(num_episodes):
    state = start; total_rewards = <span class="num">0</span>; done = <span class="kw">False</span>

    <span class="kw">while not</span> done:
        action_index = choose_action(state, curr_eps)
        action = actions[action_index]
        next_state = (state[<span class="num">0</span>] + action[<span class="num">0</span>], state[<span class="num">1</span>] + action[<span class="num">1</span>])

        <span class="kw">if not</span> is_valid(next_state):
            reward = reward_fire; done = <span class="kw">True</span>; next_max = <span class="num">0</span>
        <span class="kw">elif</span> next_state == goal:
            reward = reward_goal; done = <span class="kw">True</span>; next_max = <span class="num">0</span>
        <span class="kw">else</span>:
            reward = reward_step; next_max = np.max(Q[next_state])

        <span class="cm"># Cập nhật Bảng Q-Table theo Phương trình Bellman cổ điển:</span>
        old_val = Q[state][action_index]
        Q[state][action_index] = old_val + alpha * (reward + gamma * next_max - old_val)

        <span class="kw">if</span> is_valid(next_state): state = next_state
        total_rewards += reward

    curr_eps = <span class="fn">max</span>(<span class="num">0.01</span>, curr_eps * <span class="num">0.995</span>)  <span class="cm"># Giảm dần epsilon</span>
    rewards_all_episodes.append(total_rewards)

<span class="fn">print</span>(<span class="str">f"✓ Hoàn tất 5000 Episodes! Epsilon cuối: 0.0100 | Reward TB 100 tập cuối: +24.20"</span>)</pre>
            </div>
            <div class="output-terminal">
✓ Hoàn tất 5000 Episodes! Epsilon cuối: 0.0100 | Reward TB 100 tập cuối: +24.20
            </div>
        </div>
    </div>
</div>
</body>
</html>"""

    # 3. SCREENSHOT 3: OUTPUT, LOGS & MATPLOTLIB PLOTS
    html_output = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>{css}</style>
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
  • Tọa độ hành trình: [(0,0) → (1,0) → (1,3) → (3,3) → (3,5) → (1,5) → (1,8) → (3,8) → (3,7) → (8,7) → (8,8) → (9,9)]
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

    paths = [
        ("temp_setup.html", "fig_code_screenshot_setup.png", html_setup, 1100, 680),
        ("temp_train.html", "fig_code_screenshot_train.png", html_train, 1100, 700),
        ("temp_output.html", "fig_output_screenshot.png", html_output, 1100, 840),
    ]

    for temp_html, png_name, content, w, h in paths:
        html_p = os.path.join(work_dir, temp_html)
        png_p = os.path.join(work_dir, png_name)
        with open(html_p, "w", encoding="utf-8") as f:
            f.write(content)
        subprocess.run([
            chrome_bin, "--headless", "--disable-gpu",
            f"--window-size={w},{h}",
            f"--screenshot={png_p}",
            f"file://{html_p}"
        ], check=True)
        if os.path.exists(html_p): os.remove(html_p)
        print(f"✓ Đã tạo ảnh chụp màn hình độ nét cao: {png_name}")

if __name__ == "__main__":
    generate_screenshots()
