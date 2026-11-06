#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

work_dir = Path(__file__).resolve().parent
chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {
    margin: 0;
    padding: 12px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background-color: #ffffff;
}
.window {
    border: 1px solid #1e293b;
    border-radius: 8px;
    background: #0f172a;
    overflow: hidden;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
    color: #e2e8f0;
}
.titlebar {
    background: #1e293b;
    padding: 8px 14px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #334155;
}
.dots {
    display: flex;
    gap: 6px;
    margin-right: 14px;
}
.dot {
    width: 11px;
    height: 11px;
    border-radius: 50%;
}
.dot-red { background: #ef4444; }
.dot-yellow { background: #eab308; }
.dot-green { background: #22c55e; }
.title {
    font-size: 12px;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    color: #94a3b8;
    flex-grow: 1;
    text-align: center;
}
.main-body {
    display: flex;
    flex-direction: row;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 11px;
    line-height: 1.45;
}
.code-pane {
    width: 55%;
    padding: 12px 16px;
    background: #090d16;
    border-right: 1px solid #1e293b;
    overflow: hidden;
}
.terminal-pane {
    width: 45%;
    padding: 12px 16px;
    background: #050811;
    overflow: hidden;
}
.kw { color: #f43f5e; font-weight: bold; }
.fn { color: #38bdf8; }
.cls { color: #fbbf24; font-weight: bold; }
.str { color: #a3e635; }
.num { color: #c084fc; }
.cm { color: #64748b; font-style: italic; }
.term-head {
    color: #38bdf8;
    font-weight: bold;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 6px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
}
.term-line {
    color: #cbd5e1;
    margin-bottom: 3px;
}
.term-cmd { color: #4ade80; font-weight: bold; }
.term-val { color: #f59e0b; font-weight: bold; }
.term-suc { color: #34d399; font-weight: bold; }
.term-info { color: #60a5fa; }
</style>
</head>
<body>
<div class="window">
    <div class="titlebar">
        <div class="dots">
            <div class="dot dot-red"></div>
            <div class="dot dot-yellow"></div>
            <div class="dot dot-green"></div>
        </div>
        <div class="title">VS Code &mdash; agent02_experiment_improved.py &mdash; Intelligent System Lab 02</div>
    </div>
    <div class="main-body">
        <div class="code-pane">
            <span class="cm"># Improved Double Q-Learning & Markov Environment Core</span><br>
            <span class="kw">class</span> <span class="cls">DoubleQLearningAgent</span>:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">def</span> <span class="fn">__init__</span>(<span class="kw">self</span>, alpha=<span class="num">0.10</span>, gamma=<span class="num">0.90</span>, epsilon=<span class="num">0.20</span>):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">self</span>.q1 = np.zeros((<span class="num">2</span>, <span class="num">2</span>, <span class="num">2</span>))<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">self</span>.q2 = np.zeros((<span class="num">2</span>, <span class="num">2</span>, <span class="num">2</span>))<br>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">def</span> <span class="fn">learn</span>(<span class="kw">self</span>, state, action, reward, next_state, terminal):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;d, c = state; next_d, next_c = next_state<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">if</span> <span class="kw">self</span>.rng.random() &lt; <span class="num">0.5</span>:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;best_act = np.argmax(<span class="kw">self</span>.q1[next_d, next_c])<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;target = reward <span class="kw">if</span> terminal <span class="kw">else</span> reward + <span class="kw">self</span>.gamma * <span class="kw">self</span>.q2[next_d, next_c, best_act]<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">self</span>.q1[d, c, action] += <span class="kw">self</span>.alpha * (target - <span class="kw">self</span>.q1[d, c, action])<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">else</span>:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;best_act = np.argmax(<span class="kw">self</span>.q2[next_d, next_c])<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;target = reward <span class="kw">if</span> terminal <span class="kw">else</span> reward + <span class="kw">self</span>.gamma * <span class="kw">self</span>.q1[next_d, next_c, best_act]<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">self</span>.q2[d, c, action] += <span class="kw">self</span>.alpha * (target - <span class="kw">self</span>.q2[d, c, action])<br>
            <br>
            <span class="kw">class</span> <span class="cls">ECommerceEnvironment</span>:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">def</span> <span class="fn">step</span>(<span class="kw">self</span>, actions):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;conversion = clip(<span class="num">0.30</span> + <span class="num">0.25</span>*d + <span class="num">0.15</span>*a_i - <span class="num">0.10</span>*a_comp, <span class="num">0.05</span>, <span class="num">0.95</span>)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sales = rng.binomial(customers, conversion)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;profit = sales * (price * (<span class="num">1.0</span> - discount*a_i) - unit_cost)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">if</span> <span class="kw">self</span>.markov_demand <span class="kw">and</span> rng.random() &gt; <span class="num">0.80</span>: <span class="kw">self</span>.demand = <span class="num">1</span> - <span class="kw">self</span>.demand
        </div>
        <div class="terminal-pane">
            <div class="term-head">
                <span>TERMINAL (zsh &mdash; conda env)</span>
                <span>Python 3.10.12</span>
            </div>
            <div class="term-line"><span class="term-cmd">$ python3 agent02_experiment_improved.py</span></div>
            <div class="term-line" style="color: #64748b;">[EXPERIMENT 1: BASELINE EVALUATION (500 eps)]</div>
            <div class="term-line">RL Agent   : Mean Reward = <span class="term-val">35.1275 $</span> | Disc Rate = 0.000</div>
            <div class="term-line">Rule-Based : Mean Reward = <span class="term-val">34.9685 $</span> | Disc Rate = 0.000</div>
            <div class="term-line" style="color: #64748b;">[EXPERIMENT 4: MULTI-SEED STATISTICAL (N=10)]</div>
            <div class="term-line">RL Agent   : Mean = <span class="term-val">34.4372 $</span> &plusmn; <span class="term-info">1.2660</span> (SE=0.4003)</div>
            <div class="term-line">Rule-Based : Mean = <span class="term-val">33.9870 $</span> &plusmn; <span class="term-info">2.1632</span> (SE=0.6841)</div>
            <div class="term-line" style="color: #64748b;">[EXPERIMENT 6: DOUBLE Q-LEARNING vs STANDARD Q]</div>
            <div class="term-line">Avg Overestimation Bias Mitigated: <span class="term-val">+19.2325 $</span></div>
            <div class="term-line" style="color: #64748b;">[EXPERIMENT 7: MULTI-AGENT CO-LEARNING (QL vs QL)]</div>
            <div class="term-line">Agent 1 Reward = <span class="term-val">32.5668 $</span> | Discount = 0.286</div>
            <div class="term-line">Agent 2 Reward = <span class="term-val">32.6156 $</span> | Discount = 0.322</div>
            <div class="term-line"><span class="term-suc">&check; All 7 experiments completed successfully!</span></div>
        </div>
    </div>
</div>
</body>
</html>
"""

html_path = work_dir / "temp_code_card.html"
png_path = work_dir / "fig_code_screenshot.png"

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

cmd = [
    chrome_bin,
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--window-size=1250,480",
    f"--screenshot={png_path}",
    str(html_path)
]
subprocess.run(cmd, check=True)
if html_path.exists():
    html_path.unlink()
print(f"Code screenshot generated at: {png_path}")
