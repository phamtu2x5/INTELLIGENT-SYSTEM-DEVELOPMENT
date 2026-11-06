#!/usr/bin/env python3
"""
AGENT02: Comprehensive Intelligent System Experiment
Reinforcement-Learning-Based Agents vs. Rule-Based Agents (Enhanced & Extended)

Author: Pham Van Tu (B23DCCN879) - Class D23CTPM01
Course: Intelligent System Development, PTIT
Supervisor: Assoc. Prof. Tran Dinh Que

This script implements:
1. Standard E-Commerce Environment (i.i.d demand) & Markovian E-Commerce Environment (Demand persistence / Markov shocks)
2. Tabular Q-Learning Agent (Standard baseline)
3. Double Q-Learning Agent (Mitigating maximization overestimation bias)
4. Softmax / Boltzmann Q-Learning Agent (Adaptive exploration)
5. Fixed Rule-Based Agent
6. Multi-Agent Co-learning Simulation (Independent Q-Learning: QL vs QL non-stationarity analysis)
7. Full suite of 7 controlled experiments generating comprehensive CSVs and publication-grade 300-DPI charts.
"""

import os
import sys
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional

import numpy as np
import matplotlib.pyplot as plt

# Set aesthetic publication defaults for Matplotlib
plt.rcParams.update({
    'font.sans-serif': 'DejaVu Sans',
    'font.family': 'sans-serif',
    'figure.autolayout': True,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 13
})

State = Tuple[int, int]  # (demand, competitor_previous_action)

# ============================================================
# 1. CONFIGURATION
# ============================================================

@dataclass
class Config:
    episodes: int = 5000
    steps_per_episode: int = 20

    alpha: float = 0.10
    gamma: float = 0.90

    epsilon_start: float = 0.20
    epsilon_min: float = 0.02
    epsilon_decay: float = 0.995

    price: float = 10.0
    unit_cost: float = 5.0
    discount_rate: float = 0.20

    low_demand_customers: int = 10
    high_demand_customers: int = 20

    seed: int = 42
    evaluation_episodes: int = 500

    output_dir: str = "results"
    image_dir: str = "images"

    # Enhanced Markov Demand parameters (for Question 9)
    demand_persistence: float = 0.80  # P(d_{t+1}=s | d_t=s)


# ============================================================
# 2. E-COMMERCE ENVIRONMENTS
# ============================================================

class ECommerceEnvironment:
    """
    Simulated Duopoly E-Commerce Market Environment.
    State for Agent i: (demand, competitor_previous_action)
    Demand: 0 = low, 1 = high
    Competitor previous action: 0 = no discount, 1 = discount
    Action: 0 = no discount, 1 = discount
    """
    def __init__(self, config: Config, seed: Optional[int] = None, markov_demand: bool = False):
        self.config = config
        actual_seed = config.seed if seed is None else seed
        self.rng = np.random.default_rng(actual_seed)
        self.markov_demand = markov_demand
        self.demand = 0
        self.previous_actions = [0, 0]

    def reset(self) -> List[State]:
        self.demand = int(self.rng.integers(0, 2))
        self.previous_actions = [0, 0]
        return self.get_states()

    def get_states(self) -> List[State]:
        return [
            (self.demand, self.previous_actions[1]),
            (self.demand, self.previous_actions[0])
        ]

    def step(self, actions: List[int]) -> Tuple[List[State], List[float], Dict[str, Any]]:
        if len(actions) != 2:
            raise ValueError("Exactly two actions are required.")
        if any(a not in (0, 1) for a in actions):
            raise ValueError("Actions must be 0 or 1.")

        rewards = []
        sales_list = []
        conversion_list = []

        customers = (
            self.config.low_demand_customers
            if self.demand == 0
            else self.config.high_demand_customers
        )

        for i in range(2):
            own_action = actions[i]
            competitor_action = actions[1 - i]

            # Conversion probability formula
            conversion = (
                0.30
                + 0.25 * self.demand
                + 0.15 * own_action
                - 0.10 * competitor_action
            )
            conversion = float(np.clip(conversion, 0.05, 0.95))

            # Stochastic binomial sales
            sales = int(self.rng.binomial(customers, conversion))

            # Profit calculation
            effective_price = self.config.price * (1.0 - self.config.discount_rate * own_action)
            profit_per_sale = effective_price - self.config.unit_cost
            profit = float(sales * profit_per_sale)

            rewards.append(profit)
            sales_list.append(sales)
            conversion_list.append(conversion)

        # Update previous actions
        self.previous_actions = list(actions)

        # Demand transition
        if self.markov_demand:
            # 2-state Markov chain: persistent demand shocks
            p_stay = self.config.demand_persistence
            if self.rng.random() > p_stay:
                self.demand = 1 - self.demand
        else:
            # i.i.d. uniform demand
            self.demand = int(self.rng.integers(0, 2))

        next_states = self.get_states()
        info = {
            "sales": sales_list,
            "conversion": conversion_list,
            "customers": customers,
            "demand": self.demand
        }
        return next_states, rewards, info


# ============================================================
# 3. AGENT DEFINITIONS
# ============================================================

class QLearningAgent:
    """Standard Tabular Q-Learning Agent."""
    def __init__(self, alpha: float = 0.10, gamma: float = 0.90, epsilon: float = 0.20, seed: int = 123):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.rng = np.random.default_rng(seed)
        self.q = np.zeros((2, 2, 2), dtype=float)

    def act(self, state: State, explore: bool = True) -> int:
        demand, comp_action = state
        if explore and self.rng.random() < self.epsilon:
            return int(self.rng.integers(0, 2))
        values = self.q[demand, comp_action]
        best_actions = np.flatnonzero(np.isclose(values, np.max(values)))
        return int(self.rng.choice(best_actions))

    def learn(self, state: State, action: int, reward: float, next_state: State, terminal: bool = False):
        demand, comp_action = state
        next_d, next_c = next_state
        old_val = self.q[demand, comp_action, action]
        if terminal:
            target = reward
        else:
            best_future = np.max(self.q[next_d, next_c])
            target = reward + self.gamma * best_future
        self.q[demand, comp_action, action] = old_val + self.alpha * (target - old_val)

    def greedy_policy(self) -> Dict[State, int]:
        policy = {}
        for d in range(2):
            for c in range(2):
                policy[(d, c)] = int(np.argmax(self.q[d, c]))
        return policy


class DoubleQLearningAgent:
    """
    Double Q-Learning Agent.
    Maintains two separate Q-tables (Q1 and Q2) to decouple action selection
    from action evaluation, eliminating maximization overestimation bias.
    """
    def __init__(self, alpha: float = 0.10, gamma: float = 0.90, epsilon: float = 0.20, seed: int = 123):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.rng = np.random.default_rng(seed)
        self.q1 = np.zeros((2, 2, 2), dtype=float)
        self.q2 = np.zeros((2, 2, 2), dtype=float)

    @property
    def q(self) -> np.ndarray:
        return (self.q1 + self.q2) / 2.0

    def act(self, state: State, explore: bool = True) -> int:
        demand, comp_action = state
        if explore and self.rng.random() < self.epsilon:
            return int(self.rng.integers(0, 2))
        # Use average Q-values for action selection
        values = self.q[demand, comp_action]
        best_actions = np.flatnonzero(np.isclose(values, np.max(values)))
        return int(self.rng.choice(best_actions))

    def learn(self, state: State, action: int, reward: float, next_state: State, terminal: bool = False):
        demand, comp_action = state
        next_d, next_c = next_state

        if self.rng.random() < 0.5:
            # Update Q1 using Q2 for value evaluation
            old_val = self.q1[demand, comp_action, action]
            if terminal:
                target = reward
            else:
                best_action = np.argmax(self.q1[next_d, next_c])
                target = reward + self.gamma * self.q2[next_d, next_c, best_action]
            self.q1[demand, comp_action, action] = old_val + self.alpha * (target - old_val)
        else:
            # Update Q2 using Q1 for value evaluation
            old_val = self.q2[demand, comp_action, action]
            if terminal:
                target = reward
            else:
                best_action = np.argmax(self.q2[next_d, next_c])
                target = reward + self.gamma * self.q1[next_d, next_c, best_action]
            self.q2[demand, comp_action, action] = old_val + self.alpha * (target - old_val)

    def greedy_policy(self) -> Dict[State, int]:
        policy = {}
        for d in range(2):
            for c in range(2):
                policy[(d, c)] = int(np.argmax(self.q[d, c]))
        return policy


class SoftmaxQLearningAgent:
    """
    Softmax / Boltzmann Exploration Q-Learning Agent.
    Selects actions probabilistically based on Gibbs/Boltzmann distribution:
    P(a|s) = exp(Q(s, a) / tau) / sum(exp(Q(s, b) / tau))
    """
    def __init__(self, alpha: float = 0.10, gamma: float = 0.90, tau_start: float = 2.0, tau_min: float = 0.1, tau_decay: float = 0.998, seed: int = 123):
        self.alpha = alpha
        self.gamma = gamma
        self.tau = tau_start
        self.tau_min = tau_min
        self.tau_decay = tau_decay
        self.rng = np.random.default_rng(seed)
        self.q = np.zeros((2, 2, 2), dtype=float)

    def act(self, state: State, explore: bool = True) -> int:
        demand, comp_action = state
        values = self.q[demand, comp_action]
        if not explore or self.tau < 1e-4:
            best_actions = np.flatnonzero(np.isclose(values, np.max(values)))
            return int(self.rng.choice(best_actions))
        
        # Softmax probabilities with numerical stability (subtract max)
        exp_v = np.exp((values - np.max(values)) / self.tau)
        probs = exp_v / np.sum(exp_v)
        return int(self.rng.choice([0, 1], p=probs))

    def learn(self, state: State, action: int, reward: float, next_state: State, terminal: bool = False):
        demand, comp_action = state
        next_d, next_c = next_state
        old_val = self.q[demand, comp_action, action]
        if terminal:
            target = reward
        else:
            best_future = np.max(self.q[next_d, next_c])
            target = reward + self.gamma * best_future
        self.q[demand, comp_action, action] = old_val + self.alpha * (target - old_val)

    def decay_tau(self):
        self.tau = max(self.tau_min, self.tau * self.tau_decay)

    def greedy_policy(self) -> Dict[State, int]:
        policy = {}
        for d in range(2):
            for c in range(2):
                policy[(d, c)] = int(np.argmax(self.q[d, c]))
        return policy


class RuleBasedAgent:
    """
    Rule-Based Decision Policy:
    Rule 1: Low demand -> No discount (0)
    Rule 2: High demand & Competitor discounted -> Discount (1)
    Rule 3: High demand & Competitor did not discount -> No discount (0)
    """
    def act(self, state: State) -> int:
        demand, competitor_previous_action = state
        if demand == 0:
            return 0
        elif demand == 1 and competitor_previous_action == 1:
            return 1
        else:
            return 0


# ============================================================
# 4. TRAINING & EVALUATION ROUTINES
# ============================================================

def train_rl_against_rule(
    config: Config,
    seed: int,
    alpha: Optional[float] = None,
    epsilon_start: Optional[float] = None,
    epsilon_min: Optional[float] = None,
    epsilon_decay: Optional[float] = None,
    agent_type: str = "standard_q",
    markov_demand: bool = False
):
    alpha = config.alpha if alpha is None else alpha
    epsilon_start = config.epsilon_start if epsilon_start is None else epsilon_start
    epsilon_min = config.epsilon_min if epsilon_min is None else epsilon_min
    epsilon_decay = config.epsilon_decay if epsilon_decay is None else epsilon_decay

    env = ECommerceEnvironment(config, seed=seed, markov_demand=markov_demand)

    if agent_type == "double_q":
        rl_agent = DoubleQLearningAgent(alpha=alpha, gamma=config.gamma, epsilon=epsilon_start, seed=seed + 10_000)
    elif agent_type == "softmax_q":
        rl_agent = SoftmaxQLearningAgent(alpha=alpha, gamma=config.gamma, tau_start=2.0, seed=seed + 10_000)
    else:
        rl_agent = QLearningAgent(alpha=alpha, gamma=config.gamma, epsilon=epsilon_start, seed=seed + 10_000)

    rule_agent = RuleBasedAgent()
    episode_results = []

    for episode in range(config.episodes):
        if agent_type in ("standard_q", "double_q"):
            rl_agent.epsilon = max(epsilon_min, epsilon_start * (epsilon_decay ** episode))
        elif agent_type == "softmax_q":
            rl_agent.decay_tau()

        states = env.reset()
        episode_rewards = [0.0, 0.0]

        for step in range(config.steps_per_episode):
            rl_action = rl_agent.act(states[0], explore=True)
            rule_action = rule_agent.act(states[1])
            actions = [rl_action, rule_action]

            next_states, rewards, info = env.step(actions)
            terminal = (step == config.steps_per_episode - 1)

            rl_agent.learn(
                state=states[0],
                action=rl_action,
                reward=rewards[0],
                next_state=next_states[0],
                terminal=terminal
            )

            episode_rewards[0] += rewards[0]
            episode_rewards[1] += rewards[1]
            states = next_states

        episode_results.append({
            "episode": episode + 1,
            "rl_episode_reward": episode_rewards[0],
            "rule_episode_reward": episode_rewards[1],
            "rl_mean_reward_per_step": episode_rewards[0] / config.steps_per_episode,
            "rule_mean_reward_per_step": episode_rewards[1] / config.steps_per_episode,
            "epsilon": getattr(rl_agent, 'epsilon', getattr(rl_agent, 'tau', 0.0)),
            "alpha": alpha
        })

        if (episode + 1) % 1000 == 0 or (episode + 1) == 1:
            w = min(episode + 1, 1000)
            recent_rl_r = np.mean([r["rl_mean_reward_per_step"] for r in episode_results[-w:]])
            recent_rule_r = np.mean([r["rule_mean_reward_per_step"] for r in episode_results[-w:]])
            eps_val = getattr(rl_agent, 'epsilon', getattr(rl_agent, 'tau', 0.0))
            print(f"    [Tập {episode+1:5d}/{config.episodes}] RL Reward TB: {recent_rl_r:6.2f} $ | Rule Reward TB: {recent_rule_r:6.2f} $ | Epsilon: {eps_val:.4f}")

    return rl_agent, episode_results


def train_colearning_agents(config: Config, seed: int):
    """Two RL agents learning simultaneously (Independent Q-Learning: Multi-Agent Non-stationarity)."""
    env = ECommerceEnvironment(config, seed=seed)
    agent1 = QLearningAgent(alpha=config.alpha, gamma=config.gamma, epsilon=config.epsilon_start, seed=seed + 10_000)
    agent2 = QLearningAgent(alpha=config.alpha, gamma=config.gamma, epsilon=config.epsilon_start, seed=seed + 20_000)

    history = []

    for episode in range(config.episodes):
        eps = max(config.epsilon_min, config.epsilon_start * (config.epsilon_decay ** episode))
        agent1.epsilon = eps
        agent2.epsilon = eps

        states = env.reset()
        ep_rewards = [0.0, 0.0]
        action_counts = [0, 0]

        for step in range(config.steps_per_episode):
            a1 = agent1.act(states[0], explore=True)
            a2 = agent2.act(states[1], explore=True)
            actions = [a1, a2]

            next_states, rewards, info = env.step(actions)
            terminal = (step == config.steps_per_episode - 1)

            agent1.learn(states[0], a1, rewards[0], next_states[0], terminal)
            agent2.learn(states[1], a2, rewards[1], next_states[1], terminal)

            ep_rewards[0] += rewards[0]
            ep_rewards[1] += rewards[1]
            action_counts[0] += a1
            action_counts[1] += a2
            states = next_states

        history.append({
            "episode": episode + 1,
            "a1_reward_per_step": ep_rewards[0] / config.steps_per_episode,
            "a2_reward_per_step": ep_rewards[1] / config.steps_per_episode,
            "a1_discount_rate": action_counts[0] / config.steps_per_episode,
            "a2_discount_rate": action_counts[1] / config.steps_per_episode,
        })

        if (episode + 1) % 1000 == 0 or (episode + 1) == 1:
            w = min(episode + 1, 1000)
            r1_recent = np.mean([h["a1_reward_per_step"] for h in history[-w:]])
            r2_recent = np.mean([h["a2_reward_per_step"] for h in history[-w:]])
            d1_recent = np.mean([h["a1_discount_rate"] for h in history[-w:]]) * 100
            d2_recent = np.mean([h["a2_discount_rate"] for h in history[-w:]]) * 100
            print(f"    [Tập {episode+1:5d}/{config.episodes}] Agent 1: {r1_recent:6.2f} $ (Giảm: {d1_recent:4.1f}%) | Agent 2: {r2_recent:6.2f} $ (Giảm: {d2_recent:4.1f}%) | Eps: {eps:.4f}")

    return agent1, agent2, history


def evaluate_pair(config: Config, rl_agent, episodes: Optional[int] = None, seed: int = 900_000, markov_demand: bool = False):
    """
    Isolated greedy policy evaluation:
    - Exploration is disabled (explore=False).
    - Q-tables are completely frozen.
    - Uses independent seeds.
    """
    if episodes is None:
        episodes = config.evaluation_episodes

    env = ECommerceEnvironment(config, seed=seed, markov_demand=markov_demand)
    rule_agent = RuleBasedAgent()

    total_rewards = np.zeros(2, dtype=float)
    action_counts = np.zeros((2, 2), dtype=int)
    episode_results = []

    for episode in range(episodes):
        states = env.reset()
        rewards_this_ep = [0.0, 0.0]

        for _ in range(config.steps_per_episode):
            rl_action = rl_agent.act(states[0], explore=False)
            rule_action = rule_agent.act(states[1])
            actions = [rl_action, rule_action]

            next_states, rewards, info = env.step(actions)

            for i in range(2):
                total_rewards[i] += rewards[i]
                rewards_this_ep[i] += rewards[i]
                action_counts[i, actions[i]] += 1

            states = next_states

        episode_results.append({
            "episode": episode + 1,
            "rl_reward": rewards_this_ep[0],
            "rule_reward": rewards_this_ep[1],
            "rl_mean_reward_per_step": rewards_this_ep[0] / config.steps_per_episode,
            "rule_mean_reward_per_step": rewards_this_ep[1] / config.steps_per_episode
        })

    total_steps = episodes * config.steps_per_episode
    summary = []
    for i, name in enumerate(["RL", "Rule-based"]):
        summary.append({
            "agent": name,
            "total_reward": total_rewards[i],
            "mean_reward_per_step": total_rewards[i] / total_steps,
            "no_discount_actions": int(action_counts[i, 0]),
            "discount_actions": int(action_counts[i, 1]),
            "discount_action_rate": action_counts[i, 1] / total_steps
        })

    return summary, episode_results


# ============================================================
# 5. UTILITIES: CSV, Q-TABLE, PLOTTING
# ============================================================

def write_csv(filepath: Path, rows: List[Dict[str, Any]]):
    if not rows:
        return
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def save_q_table(filepath: Path, agent):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("Q-table: Q[demand, competitor_previous_action, action]\n")
        f.write("Action 0 = No Discount | Action 1 = Discount\n\n")
        for d in range(2):
            for c in range(2):
                q0 = agent.q[d, c, 0]
                q1 = agent.q[d, c, 1]
                best_action = int(np.argmax(agent.q[d, c]))
                f.write(f"State=(d={d}, c={c}) | Q0={q0:.6f} | Q1={q1:.6f} | Greedy={best_action}\n")


def moving_average(values: np.ndarray, window: int = 100) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    if len(values) < window:
        return values
    kernel = np.ones(window) / window
    return np.convolve(values, kernel, mode="valid")


# ============================================================
# 6. EXPERIMENTAL RUNS & ADVANCED COMPARISONS
# ============================================================

def run_experiment_1_baseline(config: Config, output_dir: Path, image_dir: Path):
    print("\n" + "=" * 70)
    print("EXPERIMENT 1: BASELINE (STANDARD Q-LEARNING VS RULE-BASED)")
    print("=" * 70)

    agent, training_rows = train_rl_against_rule(config, seed=config.seed)
    write_csv(output_dir / "baseline_episode_rewards.csv", training_rows)
    save_q_table(output_dir / "q_tables.txt", agent)

    # Evaluation
    summary, eval_rows = evaluate_pair(config, agent, episodes=config.evaluation_episodes, seed=config.seed + 500_000)
    write_csv(output_dir / "baseline_evaluation.csv", summary)
    write_csv(output_dir / "baseline_evaluation_episodes.csv", eval_rows)

    # Plot baseline training
    episodes = [r["episode"] for r in training_rows]
    rl_rewards = [r["rl_mean_reward_per_step"] for r in training_rows]
    rule_rewards = [r["rule_mean_reward_per_step"] for r in training_rows]

    fig, ax = plt.subplots(figsize=(9, 4.2), dpi=300)
    ax.plot(episodes, rl_rewards, color='#1f77b4', alpha=0.15, label="RL Raw Episode Reward")
    ax.plot(episodes, rule_rewards, color='#ff7f0e', alpha=0.15, label="Rule-Based Raw Reward")

    window = 100
    ma_rl = moving_average(rl_rewards, window)
    ma_rule = moving_average(rule_rewards, window)
    ax.plot(episodes[window - 1:], ma_rl, color='#084594', linewidth=2.0, label=f"RL Moving Average (W={window})")
    ax.plot(episodes[window - 1:], ma_rule, color='#d94801', linewidth=2.0, label=f"Rule Moving Average (W={window})")

    ax.set_xlabel("Training Episode", fontweight='bold')
    ax.set_ylabel("Mean Reward per Step ($)", fontweight='bold')
    ax.set_title("Experiment 1: Baseline RL vs Rule-Based Training Dynamics (5,000 Episodes)", fontweight='bold', pad=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='lower right', framealpha=0.9)
    plt.tight_layout()
    fig.savefig(image_dir / "fig_baseline_training.png")
    plt.close()

    print("Baseline Evaluation Results:")
    for row in summary:
        print(f"  {row['agent']:12s} | Mean Reward/Step = {row['mean_reward_per_step']:.4f} | Discount Action Rate = {row['discount_action_rate']:.3f}")
    print("Learned Greedy Policy:")
    for state, act in agent.greedy_policy().items():
        print(f"  State {state}: {'DISCOUNT (1)' if act == 1 else 'NO DISCOUNT (0)'}")

    return agent, summary


def run_experiment_2_learning_rate(config: Config, output_dir: Path, image_dir: Path):
    print("\n" + "=" * 70)
    print("EXPERIMENT 2: EFFECT OF LEARNING RATE (alpha in {0.01, 0.10, 0.50})")
    print("=" * 70)

    alphas = [0.01, 0.10, 0.50]
    results = []
    curves = {}

    for alpha in alphas:
        agent, training_rows = train_rl_against_rule(config, seed=config.seed + 1000, alpha=alpha)
        summary, _ = evaluate_pair(config, agent, episodes=config.evaluation_episodes, seed=config.seed + 600_000)
        rl_eval = next(r for r in summary if r["agent"] == "RL")
        results.append({
            "alpha": alpha,
            "rl_mean_reward_per_step": rl_eval["mean_reward_per_step"],
            "rl_discount_action_rate": rl_eval["discount_action_rate"]
        })
        curves[alpha] = [r["rl_mean_reward_per_step"] for r in training_rows]
        print(f"  alpha = {alpha:.2f} | Eval Reward/Step = {rl_eval['mean_reward_per_step']:.4f} | Discount Rate = {rl_eval['discount_action_rate']:.3f}")

    write_csv(output_dir / "learning_rate_comparison.csv", results)

    # Plot Comparison (Combined Subplots: Convergence curve + Bar Chart)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=300, gridspec_kw={'width_ratios': [1.8, 1]})
    colors = {0.01: '#2ca02c', 0.10: '#1f77b4', 0.50: '#d62728'}

    window = 120
    episodes = range(1, config.episodes + 1)
    for alpha in alphas:
        ma = moving_average(curves[alpha], window)
        ax1.plot(episodes[window - 1:], ma, color=colors[alpha], linewidth=1.8, label=f"alpha = {alpha:.2f}")

    ax1.set_xlabel("Training Episode", fontweight='bold')
    ax1.set_ylabel(f"RL Moving Average Reward (W={window})", fontweight='bold')
    ax1.set_title("Training Reward Trajectories Across Learning Rates", fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='lower right')

    labels = [f"alpha={r['alpha']:.2f}" for r in results]
    vals = [r["rl_mean_reward_per_step"] for r in results]
    bars = ax2.bar(labels, vals, color=['#2ca02c', '#1f77b4', '#d62728'], alpha=0.85, width=0.55)
    ax2.set_ylabel("Evaluation Mean Reward / Step ($)", fontweight='bold')
    ax2.set_title("Policy Evaluation Reward", fontweight='bold')
    ax2.grid(True, axis='y', linestyle='--', alpha=0.5)
    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f"{h:.3f}", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 3),
                     textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax2.set_ylim(min(vals) * 0.90, max(vals) * 1.08)

    plt.tight_layout()
    fig.savefig(image_dir / "fig_learning_rate.png")
    plt.close()
    return results


def run_experiment_3_exploration(config: Config, output_dir: Path, image_dir: Path):
    print("\n" + "=" * 70)
    print("EXPERIMENT 3: EFFECT OF EXPLORATION SCHEDULE")
    print("=" * 70)

    settings = [
        ("Low Exploration", 0.05, 0.02, 0.999),
        ("Baseline", 0.20, 0.02, 0.995),
        ("High Exploration", 0.50, 0.05, 0.995)
    ]
    results = []
    curves = {}

    for name, eps_start, eps_min, eps_decay in settings:
        agent, training_rows = train_rl_against_rule(
            config, seed=config.seed + 2000,
            epsilon_start=eps_start, epsilon_min=eps_min, epsilon_decay=eps_decay
        )
        summary, _ = evaluate_pair(config, agent, episodes=config.evaluation_episodes, seed=config.seed + 700_000)
        rl_eval = next(r for r in summary if r["agent"] == "RL")
        results.append({
            "exploration_setting": name,
            "epsilon_start": eps_start,
            "epsilon_min": eps_min,
            "epsilon_decay": eps_decay,
            "rl_mean_reward_per_step": rl_eval["mean_reward_per_step"],
            "rl_discount_action_rate": rl_eval["discount_action_rate"]
        })
        curves[name] = [r["rl_mean_reward_per_step"] for r in training_rows]
        print(f"  {name:18s} | Eval Reward = {rl_eval['mean_reward_per_step']:.4f} | Discount Rate = {rl_eval['discount_action_rate']:.3f}")

    write_csv(output_dir / "exploration_comparison.csv", results)

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=300, gridspec_kw={'width_ratios': [1.8, 1]})
    colors = {"Low Exploration": '#9467bd', "Baseline": '#1f77b4', "High Exploration": '#e377c2'}

    window = 120
    episodes = range(1, config.episodes + 1)
    for name, _, _, _ in settings:
        ma = moving_average(curves[name], window)
        ax1.plot(episodes[window - 1:], ma, color=colors[name], linewidth=1.8, label=name)

    ax1.set_xlabel("Training Episode", fontweight='bold')
    ax1.set_ylabel(f"RL Moving Average Reward (W={window})", fontweight='bold')
    ax1.set_title("Training Reward Trajectories Under Different Exploration", fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='lower right')

    labels = ["Low", "Baseline", "High"]
    vals = [r["rl_mean_reward_per_step"] for r in results]
    bars = ax2.bar(labels, vals, color=['#9467bd', '#1f77b4', '#e377c2'], alpha=0.85, width=0.55)
    ax2.set_ylabel("Evaluation Mean Reward / Step ($)", fontweight='bold')
    ax2.set_title("Policy Evaluation Reward", fontweight='bold')
    ax2.grid(True, axis='y', linestyle='--', alpha=0.5)
    for bar in bars:
        h = bar.get_height()
        ax2.annotate(f"{h:.3f}", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 3),
                     textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax2.set_ylim(min(vals) * 0.90, max(vals) * 1.08)

    plt.tight_layout()
    fig.savefig(image_dir / "fig_exploration.png")
    plt.close()
    return results


def run_experiment_4_multi_seed(config: Config, output_dir: Path, image_dir: Path):
    print("\n" + "=" * 70)
    print("EXPERIMENT 4: MULTI-SEED STATISTICAL STABILITY (10 INDEPENDENT SEEDS)")
    print("=" * 70)

    seeds = [11, 22, 33, 44, 55, 66, 77, 88, 99, 100]
    results = []

    for s in seeds:
        agent, _ = train_rl_against_rule(config, seed=s)
        summary, _ = evaluate_pair(config, agent, episodes=config.evaluation_episodes, seed=s + 800_000)
        for row in summary:
            results.append({
                "seed": s,
                "agent": row["agent"],
                "mean_reward_per_step": row["mean_reward_per_step"],
                "discount_action_rate": row["discount_action_rate"]
            })

    write_csv(output_dir / "multi_seed_summary.csv", results)

    rl_vals = [r["mean_reward_per_step"] for r in results if r["agent"] == "RL"]
    rule_vals = [r["mean_reward_per_step"] for r in results if r["agent"] == "Rule-based"]

    print("Multi-Seed Summary Statistics (N=10):")
    print(f"  RL Agent   : Mean = {np.mean(rl_vals):.4f} | Std = {np.std(rl_vals, ddof=1):.4f} | SE = {np.std(rl_vals, ddof=1)/np.sqrt(len(rl_vals)):.4f}")
    print(f"  Rule-Based : Mean = {np.mean(rule_vals):.4f} | Std = {np.std(rule_vals, ddof=1):.4f} | SE = {np.std(rule_vals, ddof=1)/np.sqrt(len(rule_vals)):.4f}")

    # Plot Multi-seed Distribution / Comparison with Error Bars
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=300)
    agents = ["RL Agent (Q-Learning)", "Rule-Based Agent"]
    means = [np.mean(rl_vals), np.mean(rule_vals)]
    stds = [np.std(rl_vals, ddof=1), np.std(rule_vals, ddof=1)]

    bars = ax.bar(agents, means, yerr=stds, capsize=8, color=['#1f77b4', '#ff7f0e'], alpha=0.85, width=0.45, edgecolor='black', linewidth=1.2)
    ax.set_ylabel("Evaluation Mean Reward / Step ($)", fontweight='bold')
    ax.set_title("Multi-Seed Robustness: Mean +/- Standard Deviation Across 10 Independent Seeds", fontweight='bold', pad=10)
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)

    for i, bar in enumerate(bars):
        h = bar.get_height()
        s = stds[i]
        ax.annotate(f"Mean: {h:.3f}\nStd: {s:.3f}", xy=(bar.get_x() + bar.get_width() / 2, h / 2),
                    ha='center', va='center', color='white', fontweight='bold', fontsize=10)

    # Plot individual seed points
    x_pos = [0, 1]
    ax.scatter([0]*len(rl_vals), rl_vals, color='navy', zorder=5, alpha=0.7, edgecolors='white', s=50, label="Individual RL Seeds")
    ax.scatter([1]*len(rule_vals), rule_vals, color='darkred', zorder=5, alpha=0.7, edgecolors='white', s=50, label="Individual Rule Seeds")
    ax.legend(loc='lower right')

    plt.tight_layout()
    fig.savefig(image_dir / "fig_multiseed_robustness.png")
    plt.close()

    return results


def run_experiment_5_markov_demand_improvement(config: Config, output_dir: Path, image_dir: Path):
    """IMPROVEMENT FOR QUESTION 9: MARKOVIAN DEMAND PERSISTENCE VS I.I.D DEMAND."""
    print("\n" + "=" * 70)
    print("EXPERIMENT 5 (QUESTION 9): MARKOVIAN DEMAND PERSISTENCE VS I.I.D. DEMAND")
    print("=" * 70)

    # Train under i.i.d demand
    agent_iid, train_iid = train_rl_against_rule(config, seed=config.seed, markov_demand=False)
    summary_iid, _ = evaluate_pair(config, agent_iid, episodes=config.evaluation_episodes, seed=config.seed + 500_000, markov_demand=False)

    # Train under Markov demand (persistence = 0.80)
    agent_markov, train_markov = train_rl_against_rule(config, seed=config.seed, markov_demand=True)
    summary_markov, _ = evaluate_pair(config, agent_markov, episodes=config.evaluation_episodes, seed=config.seed + 500_000, markov_demand=True)

    rl_iid = next(r for r in summary_iid if r["agent"] == "RL")
    rule_iid = next(r for r in summary_iid if r["agent"] == "Rule-based")
    rl_markov = next(r for r in summary_markov if r["agent"] == "RL")
    rule_markov = next(r for r in summary_markov if r["agent"] == "Rule-based")

    results = [
        {"model": "I.I.D. Demand", "rl_reward": rl_iid["mean_reward_per_step"], "rule_reward": rule_iid["mean_reward_per_step"], "rl_discount_rate": rl_iid["discount_action_rate"]},
        {"model": "Markov Demand (P=0.8)", "rl_reward": rl_markov["mean_reward_per_step"], "rule_reward": rule_markov["mean_reward_per_step"], "rl_discount_rate": rl_markov["discount_action_rate"]}
    ]
    write_csv(output_dir / "markov_demand_comparison.csv", results)

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=300)
    x = np.arange(2)
    w = 0.35

    rl_vals = [r["rl_reward"] for r in results]
    rule_vals = [r["rule_reward"] for r in results]

    b1 = ax1.bar(x - w/2, rl_vals, w, label="RL Agent", color='#1f77b4', alpha=0.85)
    b2 = ax1.bar(x + w/2, rule_vals, w, label="Rule-Based", color='#ff7f0e', alpha=0.85)
    ax1.set_xticks(x)
    ax1.set_xticklabels([r["model"] for r in results], fontweight='bold')
    ax1.set_ylabel("Evaluation Mean Reward / Step ($)", fontweight='bold')
    ax1.set_title("Performance Impact of Demand Autocorrelation", fontweight='bold')
    ax1.legend()
    ax1.grid(True, axis='y', linestyle='--', alpha=0.5)

    # Moving average convergence
    window = 100
    episodes = range(1, config.episodes + 1)
    ax2.plot(episodes[window - 1:], moving_average([r["rl_mean_reward_per_step"] for r in train_iid], window),
             label="RL (I.I.D. Demand)", color='#1f77b4', linewidth=1.8)
    ax2.plot(episodes[window - 1:], moving_average([r["rl_mean_reward_per_step"] for r in train_markov], window),
             label="RL (Markov Demand P=0.8)", color='#2ca02c', linewidth=1.8, linestyle='--')
    ax2.set_xlabel("Training Episode", fontweight='bold')
    ax2.set_ylabel("RL Mean Reward / Step ($)", fontweight='bold')
    ax2.set_title("Training Trajectory: I.I.D. vs Markov Demand", fontweight='bold')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    fig.savefig(image_dir / "fig_markov_demand_impact.png")
    plt.close()

    print(f"Markov Experiment Results:")
    print(f"  I.I.D Demand    : RL = {rl_iid['mean_reward_per_step']:.4f} | Rule = {rule_iid['mean_reward_per_step']:.4f}")
    print(f"  Markov Demand   : RL = {rl_markov['mean_reward_per_step']:.4f} | Rule = {rule_markov['mean_reward_per_step']:.4f}")
    return results


def run_experiment_6_double_q_learning_improvement(config: Config, output_dir: Path, image_dir: Path):
    """IMPROVEMENT FOR QUESTION 10: DOUBLE Q-LEARNING VS STANDARD Q-LEARNING (OVERESTIMATION BIAS)."""
    print("\n" + "=" * 70)
    print("EXPERIMENT 6 (QUESTION 10): DOUBLE Q-LEARNING VS STANDARD Q-LEARNING")
    print("=" * 70)

    # Standard Q-learning
    std_agent, std_train = train_rl_against_rule(config, seed=config.seed, agent_type="standard_q")
    std_summary, _ = evaluate_pair(config, std_agent, episodes=config.evaluation_episodes, seed=config.seed + 500_000)

    # Double Q-learning
    double_agent, double_train = train_rl_against_rule(config, seed=config.seed, agent_type="double_q")
    double_summary, _ = evaluate_pair(config, double_agent, episodes=config.evaluation_episodes, seed=config.seed + 500_000)

    std_eval = next(r for r in std_summary if r["agent"] == "RL")
    double_eval = next(r for r in double_summary if r["agent"] == "RL")

    # Q-values comparison to quantify overestimation bias
    states_list = [(0, 0), (0, 1), (1, 0), (1, 1)]
    q_comparison = []
    for d, c in states_list:
        for a in [0, 1]:
            std_val = std_agent.q[d, c, a]
            dbl_val = double_agent.q[d, c, a]
            q_comparison.append({
                "demand": d,
                "competitor_action": c,
                "action": a,
                "standard_q": std_val,
                "double_q": dbl_val,
                "overestimation_diff": std_val - dbl_val
            })
    write_csv(output_dir / "double_q_values_comparison.csv", q_comparison)

    # Plot: Convergence and Q-Value Comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=300)

    window = 100
    episodes = range(1, config.episodes + 1)
    std_ma = moving_average([r["rl_mean_reward_per_step"] for r in std_train], window)
    dbl_ma = moving_average([r["rl_mean_reward_per_step"] for r in double_train], window)

    ax1.plot(episodes[window - 1:], std_ma, color='#1f77b4', linewidth=1.8, label="Standard Q-Learning")
    ax1.plot(episodes[window - 1:], dbl_ma, color='#2ca02c', linewidth=2.0, label="Double Q-Learning (Improved)")
    ax1.set_xlabel("Training Episode", fontweight='bold')
    ax1.set_ylabel(f"Moving Average Reward (W={window})", fontweight='bold')
    ax1.set_title("Training Stability: Standard Q vs Double Q", fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='lower right')

    # Bar chart of Q-values across 8 state-action pairs
    labels = [f"({r['demand']},{r['competitor_action']}) a={r['action']}" for r in q_comparison]
    std_q_vals = [r["standard_q"] for r in q_comparison]
    dbl_q_vals = [r["double_q"] for r in q_comparison]

    x = np.arange(len(labels))
    w = 0.38
    ax2.bar(x - w/2, std_q_vals, w, label="Standard Q-Values", color='#1f77b4', alpha=0.85)
    ax2.bar(x + w/2, dbl_q_vals, w, label="Double Q-Values", color='#2ca02c', alpha=0.85)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)
    ax2.set_ylabel("Learned Q-Value", fontweight='bold')
    ax2.set_title("Mitigation of Maximization Bias in Q-Values", fontweight='bold')
    ax2.legend()
    ax2.grid(True, axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    fig.savefig(image_dir / "fig_double_q_learning.png")
    plt.close()

    print("Double Q-Learning Results:")
    print(f"  Standard Q Eval Reward: {std_eval['mean_reward_per_step']:.4f}")
    print(f"  Double Q Eval Reward  : {double_eval['mean_reward_per_step']:.4f}")
    print(f"  Average Q-Value Overestimation: {np.mean([r['overestimation_diff'] for r in q_comparison]):.4f}")
    return q_comparison


def run_experiment_7_multiagent_nonstationarity(config: Config, output_dir: Path, image_dir: Path):
    """QUESTION 8: MULTI-AGENT INTERACTION & ENVIRONMENT NON-STATIONARITY (CO-LEARNING RL VS RL)."""
    print("\n" + "=" * 70)
    print("EXPERIMENT 7 (QUESTION 8): MULTI-AGENT CO-LEARNING & NON-STATIONARITY (QL VS QL)")
    print("=" * 70)

    agent1, agent2, history = train_colearning_agents(config, seed=config.seed + 3000)
    write_csv(output_dir / "colearning_history.csv", history)

    # Plot Co-learning Dynamics
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=300)
    window = 100
    episodes = range(1, config.episodes + 1)

    a1_rew_ma = moving_average([h["a1_reward_per_step"] for h in history], window)
    a2_rew_ma = moving_average([h["a2_reward_per_step"] for h in history], window)
    a1_disc_ma = moving_average([h["a1_discount_rate"] for h in history], window)
    a2_disc_ma = moving_average([h["a2_discount_rate"] for h in history], window)

    ax1.plot(episodes[window - 1:], a1_rew_ma, color='#1f77b4', linewidth=1.8, label="RL Agent 1 Reward")
    ax1.plot(episodes[window - 1:], a2_rew_ma, color='#d62728', linewidth=1.8, linestyle='--', label="RL Agent 2 Reward")
    ax1.set_xlabel("Training Episode", fontweight='bold')
    ax1.set_ylabel(f"Reward per Step (W={window})", fontweight='bold')
    ax1.set_title("Co-Learning Reward Trajectories (Non-Stationary)", fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend()

    ax2.plot(episodes[window - 1:], a1_disc_ma, color='#1f77b4', linewidth=1.8, label="RL Agent 1 Discount Rate")
    ax2.plot(episodes[window - 1:], a2_disc_ma, color='#d62728', linewidth=1.8, linestyle='--', label="RL Agent 2 Discount Rate")
    ax2.set_xlabel("Training Episode", fontweight='bold')
    ax2.set_ylabel(f"Empirical Discount Rate (W={window})", fontweight='bold')
    ax2.set_title("Competitive Price War & Strategic Interaction", fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend()

    plt.tight_layout()
    fig.savefig(image_dir / "fig_multiagent_nonstationarity.png")
    plt.close()

    print("Co-learning Completed:")
    print(f"  Final 500-ep Mean Reward A1: {np.mean([h['a1_reward_per_step'] for h in history[-500:]]):.4f}")
    print(f"  Final 500-ep Mean Reward A2: {np.mean([h['a2_reward_per_step'] for h in history[-500:]]):.4f}")
    print(f"  Final Discount Rate A1: {np.mean([h['a1_discount_rate'] for h in history[-500:]]):.3f}")
    print(f"  Final Discount Rate A2: {np.mean([h['a2_discount_rate'] for h in history[-500:]]):.3f}")
    return history


def generate_architecture_diagrams(image_dir: Path):
    """Generate high-resolution architecture diagrams for MDP and Duopoly Game Theory."""
    print("\nGenerating Architecture & Theoretical Visualizations...")

    # Figure 1: MDP State Transition & Interaction Diagram
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Draw Environment Box
    env_box = plt.Rectangle((3.5, 0.8), 3.0, 4.4, facecolor='#e6f2ff', edgecolor='#004085', linewidth=2.0, linestyle='-', zorder=1)
    ax.add_patch(env_box)
    ax.text(5.0, 4.8, "E-COMMERCE ENVIRONMENT", ha='center', va='center', fontweight='bold', fontsize=11, color='#004085')
    ax.text(5.0, 3.8, "Demand State:\nd_t in {0: Low (N=10), 1: High (N=20)}", ha='center', va='center', fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#004085"))
    ax.text(5.0, 2.5, "Conversion Dynamics:\np_i(t) = clip(0.30 + 0.25*d + 0.15*a_i - 0.10*a_-i)\nSales S_i ~ Binomial(N_t, p_i)", ha='center', va='center', fontsize=8.5, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#004085"))
    ax.text(5.0, 1.2, "Reward Function:\nr_i = S_i * (P_i - C)", ha='center', va='center', fontsize=9, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#004085"))

    # Agent 1 (Left)
    ag1_box = plt.Rectangle((0.3, 1.8), 2.2, 2.8, facecolor='#e2f0d9', edgecolor='#385723', linewidth=2.0, zorder=1)
    ax.add_patch(ag1_box)
    ax.text(1.4, 4.2, "AGENT A (RL)", ha='center', va='center', fontweight='bold', fontsize=11, color='#385723')
    ax.text(1.4, 3.3, "Tabular Q-Learning\nDouble Q-Learning\nSoftmax Exploration", ha='center', va='center', fontsize=8.5)
    ax.text(1.4, 2.2, "State: s_A = (d_t, c_A)\nAction: a_A in {0, 1}", ha='center', va='center', fontsize=8.5, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#385723"))

    # Agent 2 (Right)
    ag2_box = plt.Rectangle((7.5, 1.8), 2.2, 2.8, facecolor='#fff2cc', edgecolor='#b25900', linewidth=2.0, zorder=1)
    ax.add_patch(ag2_box)
    ax.text(8.6, 4.2, "AGENT B (Rule/RL)", ha='center', va='center', fontweight='bold', fontsize=11, color='#b25900')
    ax.text(8.6, 3.3, "Rule-Based Policy\nor Co-Learning RL\n(3 Fixed Heuristic Rules)", ha='center', va='center', fontsize=8.5)
    ax.text(8.6, 2.2, "State: s_B = (d_t, c_B)\nAction: a_B in {0, 1}", ha='center', va='center', fontsize=8.5, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#b25900"))

    # Arrows between Agent 1 and Environment
    ax.annotate("Action a_A(t)", xy=(3.5, 3.8), xytext=(2.5, 3.8),
                arrowprops=dict(arrowstyle="->", color='#385723', lw=1.8), fontweight='bold', fontsize=9, color='#385723', ha='center', va='bottom')
    ax.annotate("State s_A, Reward r_A", xy=(2.5, 2.6), xytext=(3.5, 2.6),
                arrowprops=dict(arrowstyle="->", color='#004085', lw=1.8), fontweight='bold', fontsize=9, color='#004085', ha='center', va='bottom')

    # Arrows between Agent 2 and Environment
    ax.annotate("Action a_B(t)", xy=(6.5, 3.8), xytext=(7.5, 3.8),
                arrowprops=dict(arrowstyle="->", color='#b25900', lw=1.8), fontweight='bold', fontsize=9, color='#b25900', ha='center', va='bottom')
    ax.annotate("State s_B, Reward r_B", xy=(7.5, 2.6), xytext=(6.5, 2.6),
                arrowprops=dict(arrowstyle="->", color='#004085', lw=1.8), fontweight='bold', fontsize=9, color='#004085', ha='center', va='bottom')

    plt.tight_layout()
    fig.savefig(image_dir / "fig_mdp_model.png")
    plt.close()

    # Figure 2: Game-Theoretic Payoff Matrix Representation
    fig, ax = plt.subplots(figsize=(9, 4.0), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    # Draw Matrix Table
    ax.text(5.0, 4.6, "DUOPOLY PRICING GAME PAYOFF MATRIX (EXPECTED PROFIT $ PER STEP)", ha='center', va='center', fontweight='bold', fontsize=12)

    # Subheaders
    ax.text(3.5, 3.9, "Competitor: No Discount (0)", ha='center', va='center', fontweight='bold', fontsize=10, color='#b25900')
    ax.text(7.5, 3.9, "Competitor: Discount (1)", ha='center', va='center', fontweight='bold', fontsize=10, color='#b25900')
    ax.text(0.8, 2.8, "Agent A:\nNo Discount (0)", ha='center', va='center', fontweight='bold', fontsize=10, color='#385723')
    ax.text(0.8, 1.2, "Agent A:\nDiscount (1)", ha='center', va='center', fontweight='bold', fontsize=10, color='#385723')

    # Cell (0, 0): Both No Discount
    rect00 = plt.Rectangle((2.0, 2.0), 3.0, 1.6, facecolor='#f2f4f8', edgecolor='#333333', linewidth=1.5)
    ax.add_patch(rect00)
    ax.text(3.5, 3.1, "Cooperative High Margin", ha='center', va='center', fontsize=9, color='#084594', fontweight='bold')
    ax.text(3.5, 2.6, "Low Demand: (15.0$, 15.0$)", ha='center', va='center', fontsize=8.5)
    ax.text(3.5, 2.2, "High Demand: (55.0$, 55.0$)", ha='center', va='center', fontsize=8.5)

    # Cell (0, 1): Agent A No Disc, Comp Disc
    rect01 = plt.Rectangle((6.0, 2.0), 3.0, 1.6, facecolor='#fee8e8', edgecolor='#333333', linewidth=1.5)
    ax.add_patch(rect01)
    ax.text(7.5, 3.1, "Under-cut Penalty", ha='center', va='center', fontsize=9, color='#a50f15', fontweight='bold')
    ax.text(7.5, 2.6, "Low Demand: (10.0$, 10.5$)", ha='center', va='center', fontsize=8.5)
    ax.text(7.5, 2.2, "High Demand: (45.0$, 36.0$)", ha='center', va='center', fontsize=8.5)

    # Cell (1, 0): Agent A Disc, Comp No Disc
    rect10 = plt.Rectangle((2.0, 0.4), 3.0, 1.6, facecolor='#eafaf1', edgecolor='#333333', linewidth=1.5)
    ax.add_patch(rect10)
    ax.text(3.5, 1.5, "Aggressive Steal", ha='center', va='center', fontsize=9, color='#1e8449', fontweight='bold')
    ax.text(3.5, 1.0, "Low Demand: (13.5$, 10.0$)", ha='center', va='center', fontsize=8.5)
    ax.text(3.5, 0.6, "High Demand: (42.0$, 45.0$)", ha='center', va='center', fontsize=8.5)

    # Cell (1, 1): Both Discount (Price War)
    rect11 = plt.Rectangle((6.0, 0.4), 3.0, 1.6, facecolor='#fcf3cf', edgecolor='#333333', linewidth=1.5)
    ax.add_patch(rect11)
    ax.text(7.5, 1.5, "Mutual Price War Trap", ha='center', va='center', fontsize=9, color='#b7950b', fontweight='bold')
    ax.text(7.5, 1.0, "Low Demand: (10.5$, 10.5$)", ha='center', va='center', fontsize=8.5)
    ax.text(7.5, 0.6, "High Demand: (36.0$, 36.0$)", ha='center', va='center', fontsize=8.5)

    plt.tight_layout()
    fig.savefig(image_dir / "fig_duopoly_game.png")
    plt.close()
    print("Architecture Diagrams successfully saved.")


# ============================================================
# 7. MAIN EXECUTION CONTROLLER
# ============================================================

def main():
    base_dir = Path(__file__).resolve().parent
    config = Config(
        output_dir=str(base_dir / "results"),
        image_dir=str(base_dir / "images")
    )
    output_dir = Path(config.output_dir)
    image_dir = Path(config.image_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("INTELLIGENT SYSTEM DEVELOPMENT - LABORATORY EXPERIMENT 02")
    print("ENHANCED MULTI-AGENT REINFORCEMENT LEARNING SIMULATION SUITE")
    print(f"Output Directory: {output_dir}")
    print(f"Image Directory : {image_dir}")
    print("=" * 80)

    # Theoretical & Architectural Diagrams
    generate_architecture_diagrams(image_dir)

    # Experiment 1: Baseline
    run_experiment_1_baseline(config, output_dir, image_dir)

    # Experiment 2: Learning Rate
    run_experiment_2_learning_rate(config, output_dir, image_dir)

    # Experiment 3: Exploration Schedule
    run_experiment_3_exploration(config, output_dir, image_dir)

    # Experiment 4: Multi-Seed Statistical Validation
    run_experiment_4_multi_seed(config, output_dir, image_dir)

    # Experiment 5: Markovian Demand Persistence (Question 9 Improvement)
    run_experiment_5_markov_demand_improvement(config, output_dir, image_dir)

    # Experiment 6: Double Q-Learning Maximization Bias Mitigation (Question 10 Improvement)
    run_experiment_6_double_q_learning_improvement(config, output_dir, image_dir)

    # Experiment 7: Multi-Agent Co-Learning Non-stationarity (Question 8 Dynamic Analysis)
    run_experiment_7_multiagent_nonstationarity(config, output_dir, image_dir)

    print("\n" + "=" * 80)
    print("ALL EXPERIMENTS SUCCESSFULLY COMPLETED WITH ZERO ERRORS.")
    print("=" * 80)


if __name__ == "__main__":
    main()
