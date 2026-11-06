#!/usr/bin/env python3
"""
Generate ultra-crisp, publication-grade architectural and theoretical diagrams for Agent 02:
1. fig_mdp_model.png: Multi-Agent Duopoly MDP Architecture (with zero text overlaps, generous spacing, elegant cards)
2. fig_duopoly_game.png: Duopoly Pricing Game Theory Payoff Matrix (with clean cells, badges, and Pareto/Nash indicators)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# Set font family
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['font.family'] = 'sans-serif'


def generate_perfect_mdp_model(output_path: Path):
    """
    Generate clean, modern, zero-overlap Multi-Agent MDP Architecture.
    Using a 120 x 60 coordinate space for precision layout.
    """
    fig, ax = plt.subplots(figsize=(12, 5.8), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 60)
    ax.axis('off')

    # Main Diagram Title Banner
    ax.text(60, 57.5, "DUOPOLY MULTI-AGENT MDP INTERACTION ARCHITECTURE", 
            fontsize=12, fontweight='bold', color='#0f172a', ha='center', va='top')
    ax.text(60, 54.5, "Simultaneous Decision-Making & Strategic Interaction in a Shared E-Commerce Market", 
            fontsize=9.5, color='#475569', ha='center', va='top', style='italic')

    # -------------------------------------------------------------
    # 1. LEFT CARD: AGENT A (RL-BASED)
    # -------------------------------------------------------------
    ax.add_patch(patches.FancyBboxPatch((3, 6), 28, 44, boxstyle="round,pad=0.8",
                                        facecolor='#f0fdf4', edgecolor='#16a34a', linewidth=2.0))
    # Header bar
    ax.add_patch(patches.FancyBboxPatch((3, 43), 28, 7, boxstyle="round,pad=0.5",
                                        facecolor='#16a34a', edgecolor='#16a34a', linewidth=1.0))
    ax.text(17, 46.5, "AGENT A (RL-BASED)", fontsize=10.5, fontweight='bold', color='#ffffff', ha='center', va='center')

    # Sub-items Agent A
    ax.text(17, 39, "Learning Algorithm", fontsize=9, fontweight='bold', color='#15803d', ha='center')
    ax.text(17, 35.5, "• Tabular Q-Learning\n• Double Q-Learning\n• Softmax Boltzmann", 
            fontsize=8.2, color='#1e293b', ha='center', linespacing=1.3)

    ax.add_patch(patches.Rectangle((5, 23.5), 24, 8, facecolor='#ffffff', edgecolor='#bbf7d0', linewidth=1.2))
    ax.text(17, 29.5, "State Observation", fontsize=8.5, fontweight='bold', color='#166534', ha='center')
    ax.text(17, 26, "s_A(t) = (d_t, c_A) in {0,1}^2", fontsize=8.2, color='#0f172a', ha='center')

    ax.add_patch(patches.Rectangle((5, 12), 24, 9, facecolor='#ffffff', edgecolor='#bbf7d0', linewidth=1.2))
    ax.text(17, 18.5, "Action Decision", fontsize=8.5, fontweight='bold', color='#166534', ha='center')
    ax.text(17, 15, "a_A(t) in {0: Regular, 1: -20%}\n(Simultaneous Action)", fontsize=8.0, color='#0f172a', ha='center', linespacing=1.2)

    # -------------------------------------------------------------
    # 2. CENTER CARD: E-COMMERCE ENVIRONMENT
    # -------------------------------------------------------------
    ax.add_patch(patches.FancyBboxPatch((42, 4), 36, 48, boxstyle="round,pad=0.8",
                                        facecolor='#f8fafc', edgecolor='#0284c7', linewidth=2.2))
    # Header bar
    ax.add_patch(patches.FancyBboxPatch((42, 45), 36, 7, boxstyle="round,pad=0.5",
                                        facecolor='#0284c7', edgecolor='#0284c7', linewidth=1.0))
    ax.text(60, 48.5, "E-COMMERCE ENVIRONMENT", fontsize=11, fontweight='bold', color='#ffffff', ha='center', va='center')

    # Sub-block 1: Demand Dynamics
    ax.add_patch(patches.FancyBboxPatch((44, 34), 32, 9, boxstyle="round,pad=0.4",
                                        facecolor='#e0f2fe', edgecolor='#38bdf8', linewidth=1.2))
    ax.text(60, 40.5, "1. Market Demand Dynamics (d_t)", fontsize=8.8, fontweight='bold', color='#0369a1', ha='center')
    ax.text(60, 36.5, "Low Demand (d=0): N = 10 customers\nHigh Demand (d=1): N = 20 customers\n(i.i.d. Uniform or Markov Persistence rho=0.80)", 
            fontsize=7.8, color='#0f172a', ha='center', linespacing=1.2)

    # Sub-block 2: Conversion & Binomial Sales
    ax.add_patch(patches.FancyBboxPatch((44, 20), 32, 12, boxstyle="round,pad=0.4",
                                        facecolor='#f0fdf4', edgecolor='#4ade80', linewidth=1.2))
    ax.text(60, 29.5, "2. Customer Conversion & Sales", fontsize=8.8, fontweight='bold', color='#15803d', ha='center')
    ax.text(60, 25.0, "p_i(t) = clip(0.30 + 0.25*d + 0.15*a_i - 0.10*a_-i)", fontsize=7.8, fontweight='bold', color='#166534', ha='center')
    ax.text(60, 22.0, "Sales S_i ~ Binomial(N_t, p_i(t))", fontsize=8.0, color='#0f172a', ha='center')

    # Sub-block 3: Economic Profit Engine
    ax.add_patch(patches.FancyBboxPatch((44, 6.5), 32, 11.5, boxstyle="round,pad=0.4",
                                        facecolor='#fffbeb', edgecolor='#fcd34d', linewidth=1.2))
    ax.text(60, 15.5, "3. Reward / Economic Profit Engine", fontsize=8.8, fontweight='bold', color='#b45309', ha='center')
    ax.text(60, 12.0, "r_i(t) = S_i(t) * [P_i(t) - C]", fontsize=8.2, fontweight='bold', color='#92400e', ha='center')
    ax.text(60, 8.8, "Price: P=10$, Cost: C=5$ | Margin: 5$ (No Disc) vs 3$ (Disc)", fontsize=7.6, color='#78350f', ha='center')

    # -------------------------------------------------------------
    # 3. RIGHT CARD: AGENT B (RULE-BASED / OPPONENT)
    # -------------------------------------------------------------
    ax.add_patch(patches.FancyBboxPatch((89, 6), 28, 44, boxstyle="round,pad=0.8",
                                        facecolor='#fff7ed', edgecolor='#ea580c', linewidth=2.0))
    # Header bar
    ax.add_patch(patches.FancyBboxPatch((89, 43), 28, 7, boxstyle="round,pad=0.5",
                                        facecolor='#ea580c', edgecolor='#ea580c', linewidth=1.0))
    ax.text(103, 46.5, "AGENT B (RULE / RL)", fontsize=10.5, fontweight='bold', color='#ffffff', ha='center', va='center')

    # Sub-items Agent B
    ax.text(103, 39, "Decision Policy", fontsize=9, fontweight='bold', color='#c2410c', ha='center')
    ax.text(103, 35.5, "• Rule-Based Expert Logic\n• 3 Fixed Condition Rules\n• Or Co-Learning RL Agent", 
            fontsize=8.2, color='#1e293b', ha='center', linespacing=1.3)

    ax.add_patch(patches.Rectangle((91, 23.5), 24, 8, facecolor='#ffffff', edgecolor='#fed7aa', linewidth=1.2))
    ax.text(103, 29.5, "State Observation", fontsize=8.5, fontweight='bold', color='#9a3412', ha='center')
    ax.text(103, 26, "s_B(t) = (d_t, c_B) in {0,1}^2", fontsize=8.2, color='#0f172a', ha='center')

    ax.add_patch(patches.Rectangle((91, 12), 24, 9, facecolor='#ffffff', edgecolor='#fed7aa', linewidth=1.2))
    ax.text(103, 18.5, "Action Decision", fontsize=8.5, fontweight='bold', color='#9a3412', ha='center')
    ax.text(103, 15, "a_B(t) in {0: Regular, 1: -20%}\n(Simultaneous Action)", fontsize=8.0, color='#0f172a', ha='center', linespacing=1.2)

    # -------------------------------------------------------------
    # 4. EXPLICIT NON-OVERLAPPING INTERACTION ARROWS
    # -------------------------------------------------------------
    # Action A Arrow (Agent A -> Environment, Top)
    ax.annotate("", xy=(42, 38), xytext=(31, 38),
                arrowprops=dict(arrowstyle="->,head_width=0.45,head_length=0.7", color="#16a34a", lw=2.2))
    ax.text(36.5, 40.5, "Action a_A(t)", fontsize=8.5, fontweight='bold', color='#15803d', ha='center', va='bottom',
            bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#16a34a", lw=1.0))

    # Feedback A Arrow (Environment -> Agent A, Bottom)
    ax.annotate("", xy=(31, 16), xytext=(42, 16),
                arrowprops=dict(arrowstyle="->,head_width=0.45,head_length=0.7", color="#0284c7", lw=2.2))
    ax.text(36.5, 12.5, "State s_A, Reward r_A", fontsize=8.2, fontweight='bold', color='#0369a1', ha='center', va='top',
            bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#0284c7", lw=1.0))

    # Action B Arrow (Agent B -> Environment, Top)
    ax.annotate("", xy=(78, 38), xytext=(89, 38),
                arrowprops=dict(arrowstyle="->,head_width=0.45,head_length=0.7", color="#ea580c", lw=2.2))
    ax.text(83.5, 40.5, "Action a_B(t)", fontsize=8.5, fontweight='bold', color='#c2410c', ha='center', va='bottom',
            bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#ea580c", lw=1.0))

    # Feedback B Arrow (Environment -> Agent B, Bottom)
    ax.annotate("", xy=(89, 16), xytext=(78, 16),
                arrowprops=dict(arrowstyle="->,head_width=0.45,head_length=0.7", color="#0284c7", lw=2.2))
    ax.text(83.5, 12.5, "State s_B, Reward r_B", fontsize=8.2, fontweight='bold', color='#0369a1', ha='center', va='top',
            bbox=dict(boxstyle="round,pad=0.2", fc="#ffffff", ec="#0284c7", lw=1.0))

    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close()
    print(f"Generated perfect MDP diagram at: {output_path}")


def generate_perfect_duopoly_game(output_path: Path):
    """
    Generate clean, elegant Game Theory Payoff Matrix for the Duopoly Pricing Game.
    """
    fig, ax = plt.subplots(figsize=(11, 5.0), dpi=300)
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 50)
    ax.axis('off')

    # Title
    ax.text(55, 47.5, "DUOPOLY PRICING GAME: STRATEGIC PAYOFF MATRIX", 
            fontsize=12, fontweight='bold', color='#0f172a', ha='center')
    ax.text(55, 44.5, "Expected Profit ($ per step) under Low Demand (N=10) and High Demand (N=20)", 
            fontsize=9.0, color='#475569', ha='center', style='italic')

    # Column Headers (Competitor B)
    ax.text(45, 39.5, "Competitor B: Regular Price (a_B = 0)", fontsize=9.5, fontweight='bold', color='#c2410c', ha='center')
    ax.text(85, 39.5, "Competitor B: Discount 20% (a_B = 1)", fontsize=9.5, fontweight='bold', color='#c2410c', ha='center')

    # Row Headers (Agent A)
    ax.text(12, 28, "Agent A:\nRegular Price\n(a_A = 0)", fontsize=9.5, fontweight='bold', color='#15803d', ha='center', va='center')
    ax.text(12, 12, "Agent A:\nDiscount 20%\n(a_A = 1)", fontsize=9.5, fontweight='bold', color='#15803d', ha='center', va='center')

    # Cell 00: Both Regular (Pareto Optimal)
    ax.add_patch(patches.FancyBboxPatch((27, 21), 36, 15, boxstyle="round,pad=0.5",
                                        facecolor='#eff6ff', edgecolor='#3b82f6', linewidth=2.0))
    ax.add_patch(patches.Rectangle((28.5, 32.5), 33, 2.8, facecolor='#2563eb', edgecolor='none'))
    ax.text(45, 33.9, "MUTUAL COOPERATION (PARETO OPTIMAL)", fontsize=7.8, fontweight='bold', color='#ffffff', ha='center', va='center')
    ax.text(45, 29.0, "High Margin Preservation (5$ / unit)", fontsize=8.5, fontweight='bold', color='#1e40af', ha='center')
    ax.text(45, 25.5, "Low Demand (N=10) : (15.00 $,  15.00 $)", fontsize=8.2, color='#0f172a', ha='center')
    ax.text(45, 22.5, "High Demand (N=20): (55.00 $,  55.00 $)", fontsize=8.5, fontweight='bold', color='#1e3a8a', ha='center')

    # Cell 01: Agent A Regular, Comp Discount
    ax.add_patch(patches.FancyBboxPatch((67, 21), 36, 15, boxstyle="round,pad=0.5",
                                        facecolor='#fef2f2', edgecolor='#ef4444', linewidth=1.8))
    ax.add_patch(patches.Rectangle((68.5, 32.5), 33, 2.8, facecolor='#dc2626', edgecolor='none'))
    ax.text(85, 33.9, "AGENT A UNDERCUT PENALTY", fontsize=7.8, fontweight='bold', color='#ffffff', ha='center', va='center')
    ax.text(85, 29.0, "Conversion Loss (-10% penalty)", fontsize=8.5, fontweight='bold', color='#991b1b', ha='center')
    ax.text(85, 25.5, "Low Demand (N=10) : (10.00 $,  10.50 $)", fontsize=8.2, color='#0f172a', ha='center')
    ax.text(85, 22.5, "High Demand (N=20): (45.00 $,  36.00 $)", fontsize=8.5, color='#7f1d1d', ha='center')

    # Cell 10: Agent A Discount, Comp Regular
    ax.add_patch(patches.FancyBboxPatch((27, 4.5), 36, 15, boxstyle="round,pad=0.5",
                                        facecolor='#f0fdf4', edgecolor='#22c55e', linewidth=1.8))
    ax.add_patch(patches.Rectangle((28.5, 16.0), 33, 2.8, facecolor='#16a34a', edgecolor='none'))
    ax.text(45, 17.4, "AGENT A AGGRESSIVE STEAL", fontsize=7.8, fontweight='bold', color='#ffffff', ha='center', va='center')
    ax.text(45, 12.5, "Volume Gain (+15%) vs Margin Loss (-40%)", fontsize=8.2, fontweight='bold', color='#166534', ha='center')
    ax.text(45, 9.2, "Low Demand (N=10) : (13.50 $,  10.00 $)", fontsize=8.2, color='#0f172a', ha='center')
    ax.text(45, 6.2, "High Demand (N=20): (42.00 $,  45.00 $)", fontsize=8.5, color='#14532d', ha='center')

    # Cell 11: Both Discount (Price War Trap)
    ax.add_patch(patches.FancyBboxPatch((67, 4.5), 36, 15, boxstyle="round,pad=0.5",
                                        facecolor='#fefce8', edgecolor='#eab308', linewidth=2.0))
    ax.add_patch(patches.Rectangle((68.5, 16.0), 33, 2.8, facecolor='#ca8a04', edgecolor='none'))
    ax.text(85, 17.4, "PRICE WAR TRAP (DEFENSIVE EQUILIBRIUM)", fontsize=7.6, fontweight='bold', color='#ffffff', ha='center', va='center')
    ax.text(85, 12.5, "Mutual Margin Destruction (3$ / unit)", fontsize=8.5, fontweight='bold', color='#854d0e', ha='center')
    ax.text(85, 9.2, "Low Demand (N=10) : (10.50 $,  10.50 $)", fontsize=8.2, color='#0f172a', ha='center')
    ax.text(85, 6.2, "High Demand (N=20): (36.00 $,  36.00 $)", fontsize=8.5, fontweight='bold', color='#713f12', ha='center')

    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close()
    print(f"Generated perfect Duopoly Game diagram at: {output_path}")


if __name__ == "__main__":
    img_dir = Path(__file__).resolve().parent
    generate_perfect_mdp_model(img_dir / "fig_mdp_model.png")
    generate_perfect_duopoly_game(img_dir / "fig_duopoly_game.png")
