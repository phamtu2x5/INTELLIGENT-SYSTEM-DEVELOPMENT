# -*- coding: utf-8 -*-
"""
Script: generate_chapter6_figures.py
Tạo các biểu đồ trực quan chuẩn xuất bản học thuật (300 DPI) cho Chương 6: Hệ Đa Tác Tử (Multi-Agent Systems - MAS)
Tác giả: Phạm Văn Tư - B23DCCN879
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cấu hình chung cho Matplotlib
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

# =============================================================================
# HÌNH 6.1: PHÂN LOẠI CÁC CẤU TRÚC LIÊN KẾT ĐA TÁC TỬ (MAS TOPOLOGIES)
# =============================================================================
def generate_fig601():
    fig, axes = plt.subplots(2, 2, figsize=(14, 11), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    
    # Tiêu đề chính
    fig.suptitle("CÁC KIẾN TRÚC VÀ CẤU TRÚC MẠNG LƯỚI PHỐI HỢP ĐA TÁC TỬ (MAS TOPOLOGIES)",
                 fontsize=15, fontweight='bold', color='#1A365D', y=0.98)
    
    # 1. TOPOLOGY A: CENTRALIZED SUPERVISOR
    ax = axes[0, 0]
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title("A. Mô hình Tập trung (Centralized Supervisor / Router)", 
                 fontsize=12, fontweight='bold', color='#0F172A', pad=12)
    
    # Supervisor ở giữa
    sup = FancyBboxPatch((3.5, 4.0), 3.0, 2.0, boxstyle="round,pad=0.2",
                         fc='#1E40AF', ec='#1E3A8A', lw=2)
    ax.add_patch(sup)
    ax.text(5.0, 5.0, "SUPERVISOR\nAGENT\n(Nhạc trưởng)", ha='center', va='center',
            color='white', fontweight='bold', fontsize=10)
    
    # Các Worker Agents xung quanh
    workers = [
        (1.0, 7.5, "Diagnostic Agent", "#059669"),
        (7.0, 7.5, "Pharmacist Agent", "#D97706"),
        (1.0, 0.8, "Dietitian Agent", "#7C3AED"),
        (7.0, 0.8, "Regulatory Agent", "#DC2626")
    ]
    for wx, wy, label, col in workers:
        w_box = FancyBboxPatch((wx, wy), 2.0, 1.4, boxstyle="round,pad=0.15",
                               fc=col, ec='#1F2937', lw=1.2)
        ax.add_patch(w_box)
        ax.text(wx+1.0, wy+0.7, label, ha='center', va='center',
                color='white', fontweight='bold', fontsize=8.5)
        # Mũi tên 2 chiều với Supervisor
        ax.annotate('', xy=(5.0, 5.0), xytext=(wx+1.0, wy+0.7),
                    arrowprops=dict(arrowstyle='<->', color='#475569', lw=1.5, ls='--'))
    ax.text(5.0, 0.2, "Ưu điểm: Kiểm soát luồng chặt chẽ | Nhược điểm: Điểm nghẽn trung tâm",
            ha='center', fontsize=8.5, fontstyle='italic', color='#475569')

    # 2. TOPOLOGY B: HIERARCHICAL TREE
    ax = axes[0, 1]
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title("B. Mô hình Phân cấp Hình cây (Hierarchical Tree)", 
                 fontsize=12, fontweight='bold', color='#0F172A', pad=12)
    
    # Tầng 1: Chief Executive
    t1 = FancyBboxPatch((3.5, 7.8), 3.0, 1.5, boxstyle="round,pad=0.2",
                        fc='#991B1B', ec='#7F1D1D', lw=1.8)
    ax.add_patch(t1)
    ax.text(5.0, 8.55, "Chief Medical Officer\n(Bác sĩ Trưởng)", ha='center', va='center',
            color='white', fontweight='bold', fontsize=9.5)
    
    # Tầng 2: Team Leads
    leads = [(1.2, 4.5, "Clinical Lead", "#2563EB"), (6.0, 4.5, "Lifestyle Lead", "#0D9488")]
    for lx, ly, label, col in leads:
        l_box = FancyBboxPatch((lx, ly), 2.8, 1.4, boxstyle="round,pad=0.15",
                               fc=col, ec='#1E293B', lw=1.2)
        ax.add_patch(l_box)
        ax.text(lx+1.4, ly+0.7, label, ha='center', va='center',
                color='white', fontweight='bold', fontsize=9)
        ax.annotate('', xy=(lx+1.4, ly+1.4), xytext=(5.0, 7.8),
                    arrowprops=dict(arrowstyle='->', color='#334155', lw=1.5))
        
    # Tầng 3: Specialists
    specs = [
        (0.3, 1.2, "Diagnostic DL", "#3B82F6", 2.6),
        (3.0, 1.2, "Pharmacist KG", "#3B82F6", 2.6),
        (5.7, 1.2, "Dietitian", "#14B8A6", 7.4),
        (8.0, 1.2, "Regulatory", "#14B8A6", 7.4)
    ]
    for sx, sy, label, col, parent_x in specs:
        s_box = FancyBboxPatch((sx, sy), 1.8, 1.3, boxstyle="round,pad=0.1",
                               fc=col, ec='#334155', lw=1.0)
        ax.add_patch(s_box)
        ax.text(sx+0.9, sy+0.65, label, ha='center', va='center',
                color='white', fontweight='bold', fontsize=8)
        ax.annotate('', xy=(sx+0.9, sy+1.3), xytext=(parent_x, 4.5),
                    arrowprops=dict(arrowstyle='->', color='#64748B', lw=1.2))
    ax.text(5.0, 0.2, "Ưu điểm: Phân quyền rõ ràng | Nhược điểm: Độ trễ trao đổi phân tầng",
            ha='center', fontsize=8.5, fontstyle='italic', color='#475569')

    # 3. TOPOLOGY C: SEQUENTIAL PIPELINE
    ax = axes[1, 0]
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title("C. Mô hình Dây chuyền Tuần tự (Sequential Pipeline)", 
                 fontsize=12, fontweight='bold', color='#0F172A', pad=12)
    
    stages = [
        (1.0, 7.0, "1. Triage Agent", "Tiếp nhận & Lọc triệu chứng", "#1E3A8A"),
        (1.0, 5.0, "2. Diagnostic Agent", "Mô hình Học sâu phân loại rủi ro", "#065F46"),
        (1.0, 3.0, "3. Pharmacist Agent", "Tra cứu tương tác thuốc trên KG", "#92400E"),
        (1.0, 1.0, "4. Formulator Agent", "Tổng hợp phác đồ điều trị cuối", "#5B21B6")
    ]
    for sx, sy, title, desc, col in stages:
        p_box = FancyBboxPatch((sx, sy), 8.0, 1.4, boxstyle="round,pad=0.15",
                               fc=col, ec='#1E293B', lw=1.2)
        ax.add_patch(p_box)
        ax.text(sx+0.4, sy+0.85, title, fontweight='bold', color='white', fontsize=9.5)
        ax.text(sx+0.4, sy+0.35, desc, color='#E2E8F0', fontsize=8)
        if sy > 1.0:
            ax.annotate('', xy=(sx+4.0, sy-0.6), xytext=(sx+4.0, sy),
                        arrowprops=dict(arrowstyle='->', color='#DC2626', lw=2.2))
    ax.text(5.0, 0.2, "Ưu điểm: Đơn giản, dễ kiểm thử | Nhược điểm: Kém linh hoạt khi rẽ nhánh",
            ha='center', fontsize=8.5, fontstyle='italic', color='#475569')

    # 4. TOPOLOGY D: MULTI-AGENT DEBATE & CONSENSUS
    ax = axes[1, 1]
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title("D. Mô hình Tranh luận & Phản biện Ngang hàng (Multi-Agent Debate)", 
                 fontsize=12, fontweight='bold', color='#0F172A', pad=12)
    
    # 3 tác tử tranh luận tạo thành tam giác
    agents_tri = [
        (5.0, 7.2, "Agent A (Macro Analyst)", "Đề xuất: Tích cực gom CP", "#1D4ED8"),
        (1.5, 2.5, "Agent B (Risk Officer)", "Phản biện: Cảnh báo lạm phát", "#B91C1C"),
        (8.5, 2.5, "Agent C (Quant Forecaster)", "Dữ liệu: BiLSTM dự báo tăng", "#047857")
    ]
    coords = []
    for ax_pos, ay_pos, title, sub, col in agents_tri:
        abox = FancyBboxPatch((ax_pos-1.8, ay_pos-0.9), 3.6, 1.8, boxstyle="round,pad=0.15",
                              fc=col, ec='#1E293B', lw=1.2)
        ax.add_patch(abox)
        ax.text(ax_pos, ay_pos+0.25, title, ha='center', va='center',
                color='white', fontweight='bold', fontsize=8.5)
        ax.text(ax_pos, ay_pos-0.35, sub, ha='center', va='center',
                color='#FEF08A', fontsize=7.5)
        coords.append((ax_pos, ay_pos))
        
    # Mũi tên phản biện 2 chiều giữa các tác tử
    ax.annotate('', xy=coords[1], xytext=coords[0],
                arrowprops=dict(arrowstyle='<->', color='#EA580C', lw=1.8, ls='-'))
    ax.annotate('', xy=coords[2], xytext=coords[0],
                arrowprops=dict(arrowstyle='<->', color='#EA580C', lw=1.8, ls='-'))
    ax.annotate('', xy=coords[2], xytext=coords[1],
                arrowprops=dict(arrowstyle='<->', color='#EA580C', lw=1.8, ls='-'))
    
    # Hộp đồng thuận ở giữa
    c_box = FancyBboxPatch((3.5, 3.8), 3.0, 1.4, boxstyle="round,pad=0.1",
                           fc='#F1F5F9', ec='#0F172A', lw=1.5, ls='--')
    ax.add_patch(c_box)
    ax.text(5.0, 4.7, "CONSENSUS ENGINE", ha='center', va='center',
            fontweight='bold', fontsize=8, color='#0F172A')
    ax.text(5.0, 4.15, "Bầu chọn Đa số / Trọng số", ha='center', va='center',
            fontsize=7.5, color='#475569')
    
    ax.text(5.0, 0.2, "Ưu điểm: Triệt tiêu ảo giác qua phản biện chéo | Nhược điểm: Chi phí token cao",
            ha='center', fontsize=8.5, fontstyle='italic', color='#475569')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    out_path = os.path.join(OUTPUT_DIR, "fig601_mas_architecture_taxonomy.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"✓ Đã tạo thành công: {out_path}")

# =============================================================================
# HÌNH 6.2: GIAO THỨC TRUYỀN THÔNG & CẤU TRÚC THÔNG ĐIỆP ĐA TÁC TỬ
# =============================================================================
def generate_fig602():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    fig.suptitle("GIAO THỨC TRUYỀN THÔNG & CẤU TRÚC THÔNG ĐIỆP TRONG HỆ ĐA TÁC TỬ (A2A PROTOCOLS)",
                 fontsize=14, fontweight='bold', color='#1E3A8A', y=0.98)
    
    # PANEL 1: FIPA-ACL & LÝ THUYẾT HÀNH ĐỘNG LỜI NÓI
    ax1.set_facecolor('#F8FAFC')
    ax1.axis('off')
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_title("A. Cấu Trúc Thông Điệp Chuẩn FIPA-ACL (Cổ Điển)",
                  fontsize=11.5, fontweight='bold', color='#0F172A', pad=10)
    
    # Hộp FIPA Envelope
    env = FancyBboxPatch((0.5, 0.5), 9.0, 8.8, boxstyle="round,pad=0.2",
                         fc='#EFF6FF', ec='#3B82F6', lw=1.8)
    ax1.add_patch(env)
    
    fields = [
        ("PERFORMATIVE", "INFORM / REQUEST / PROPOSE / REFUSE / CFP", "#1E40AF"),
        ("SENDER", "agent://healthcare.hospital/pharmacist_kg_01", "#047857"),
        ("RECEIVER", "agent://healthcare.hospital/clinical_supervisor", "#B45309"),
        ("ONTOLOGY", "urn:ptit:ontology:diabetes_vietnam_v2", "#6D28D9"),
        ("LANGUAGE", "JSON-LD / Turtle RDF / FIPA-SL", "#475569"),
        ("REPLY-WITH", "msg_req_879_check_interaction_01", "#0F172A"),
        ("IN-REPLY-TO", "msg_call_5481_cmo_inquiry", "#0F172A"),
        ("CONTENT", "Triple: (Metformin, CHONG_CHI_DINH, Ruou_Bia)\nWarning: Lactic Acidosis risk critical", "#BE123C")
    ]
    y_pos = 8.3
    for k, v, col in fields:
        ax1.text(0.9, y_pos, f"{k}:", fontweight='bold', fontsize=9, color=col)
        ax1.text(3.5, y_pos, v, fontsize=8.5, color='#1E293B', family='monospace')
        y_pos -= 0.95
        
    # PANEL 2: MODERN STRUCTURED JSON A2A PROTOCOL
    ax2.set_facecolor('#0F172A')
    ax2.axis('off')
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.set_title("B. Giao Thức Hiện Đại: Structured JSON / Tool Calling",
                  fontsize=11.5, fontweight='bold', color='#0F172A', pad=10)
    
    json_box = FancyBboxPatch((0.5, 0.5), 9.0, 8.8, boxstyle="round,pad=0.2",
                              fc='#1E293B', ec='#64748B', lw=1.8)
    ax2.add_patch(json_box)
    
    json_text = """{
  "protocol_version": "A2A-v2.0-PTIT",
  "message_id": "msg_953137b4_step3",
  "source_agent": {
    "role": "pharmacist_kg_agent",
    "capability": ["knowledge_graph", "drug_interaction"]
  },
  "target_agent": "cmo_supervisor",
  "performative": "PROPOSE_CONTRAINDICATION",
  "timestamp": "2026-10-23T08:50:00Z",
  "payload": {
    "patient_id": "VN_PATIENT_2026_879",
    "detected_conflicts": [
      {
        "drug_a": "Metformin",
        "substance_b": "Ruou_Bia",
        "severity": "CRITICAL_FATAL",
        "evidence": "Quyet dinh 5481/QD-BYT"
      }
    ],
    "recommendation": "Tam ngung dung Metformin truoc lien hoan"
  },
  "verification_hash": "sha256:7f8a91bc..."
}"""
    ax2.text(0.9, 8.8, json_text, fontsize=8.0, color='#38BDF8', family='monospace', va='top')
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    out_path = os.path.join(OUTPUT_DIR, "fig602_mas_communication_protocols.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"✓ Đã tạo thành công: {out_path}")

# =============================================================================
# HÌNH 6.3: ĐỐI CHUẨN KIẾN TRÚC LANGGRAPH VS AUTOGEN VS CREWAI
# =============================================================================
def generate_fig603():
    fig, axes = plt.subplots(1, 3, figsize=(15, 6.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    fig.suptitle("ĐỐI CHUẨN KIẾN TRÚC 3 FRAMEWORK ĐA TÁC TỬ HÀNG ĐẦU HIỆN NAY",
                 fontsize=14, fontweight='bold', color='#1E3A8A', y=0.98)
    
    # 1. LANGGRAPH
    ax1 = axes[0]
    ax1.set_facecolor('#F8FAFC')
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title("1. LangGraph (LangChain)", fontsize=11.5, fontweight='bold', color='#1E40AF')
    
    b1 = FancyBboxPatch((0.5, 0.5), 9.0, 8.8, boxstyle="round,pad=0.2",
                        fc='#EFF6FF', ec='#2563EB', lw=1.5)
    ax1.add_patch(b1)
    
    # Diagram StateGraph
    nodes = [(5.0, 7.8, "START / State"), (2.0, 5.0, "Triage Node"), 
             (8.0, 5.0, "Pharmacist Node"), (5.0, 2.2, "Supervisor Node")]
    for nx_pos, ny_pos, lbl in nodes:
        c = FancyBboxPatch((nx_pos-1.4, ny_pos-0.6), 2.8, 1.2, boxstyle="round,pad=0.1",
                           fc='#1D4ED8', ec='#1E3A8A')
        ax1.add_patch(c)
        ax1.text(nx_pos, ny_pos, lbl, ha='center', va='center', color='white', fontweight='bold', fontsize=7.5)
    
    # Edges
    ax1.annotate('', xy=(2.0, 5.6), xytext=(5.0, 7.2), arrowprops=dict(arrowstyle='->', color='#2563EB', lw=1.5))
    ax1.annotate('', xy=(8.0, 5.6), xytext=(5.0, 7.2), arrowprops=dict(arrowstyle='->', color='#2563EB', lw=1.5))
    ax1.annotate('', xy=(5.0, 3.4), xytext=(2.0, 4.4), arrowprops=dict(arrowstyle='->', color='#2563EB', lw=1.5))
    ax1.annotate('', xy=(5.0, 3.4), xytext=(8.0, 4.4), arrowprops=dict(arrowstyle='->', color='#2563EB', lw=1.5))
    ax1.annotate('', xy=(5.0, 7.2), xytext=(5.0, 3.4), 
                 arrowprops=dict(arrowstyle='->', color='#DC2626', lw=1.5, ls='--', connectionstyle="arc3,rad=-0.5"))
    ax1.text(6.8, 4.0, "Conditional\nEdge (Loop)", color='#DC2626', fontsize=7, fontweight='bold')
    
    ax1.text(5.0, 0.9, "• Cyclic Directed Graph (StateGraph)\n• Kiểm soát trạng thái chính xác tuyệt đối\n• Hỗ trợ Human-in-the-loop tự nhiên",
             ha='center', fontsize=8, color='#1E293B')

    # 2. MICROSOFT AUTOGEN
    ax2 = axes[1]
    ax2.set_facecolor('#F8FAFC')
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title("2. Microsoft AutoGen", fontsize=11.5, fontweight='bold', color='#047857')
    
    b2 = FancyBboxPatch((0.5, 0.5), 9.0, 8.8, boxstyle="round,pad=0.2",
                        fc='#ECFDF5', ec='#059669', lw=1.5)
    ax2.add_patch(b2)
    
    # GroupChat Manager
    mgr = FancyBboxPatch((2.5, 6.8), 5.0, 1.4, boxstyle="round,pad=0.1",
                         fc='#047857', ec='#064E3B')
    ax2.add_patch(mgr)
    ax2.text(5.0, 7.5, "GroupChatManager", ha='center', va='center', color='white', fontweight='bold', fontsize=8.5)
    
    # Conversable Agents
    ag_list = [(2.0, 4.0, "UserProxy\n(Code Exec)"), (5.0, 2.0, "Medical\nAssistant"), (8.0, 4.0, "Critic\nAgent")]
    for ax_pos, ay_pos, lbl in ag_list:
        ab = FancyBboxPatch((ax_pos-1.2, ay_pos-0.6), 2.4, 1.2, boxstyle="round,pad=0.1",
                            fc='#059669', ec='#047857')
        ax2.add_patch(ab)
        ax2.text(ax_pos, ay_pos, lbl, ha='center', va='center', color='white', fontweight='bold', fontsize=7.5)
        ax2.annotate('', xy=(ax_pos, ay_pos+0.6), xytext=(5.0, 6.8),
                    arrowprops=dict(arrowstyle='<->', color='#047857', lw=1.4))
        
    ax2.text(5.0, 0.9, "• ConversableAgent + GroupChat\n• Tự động chọn người phát ngôn (Speaker Selection)\n• Khả năng tự viết & chạy code Python an toàn",
             ha='center', fontsize=8, color='#1E293B')

    # 3. CREWAI
    ax3 = axes[2]
    ax3.set_facecolor('#F8FAFC')
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.axis('off')
    ax3.set_title("3. CrewAI (Role-Playing)", fontsize=11.5, fontweight='bold', color='#B45309')
    
    b3 = FancyBboxPatch((0.5, 0.5), 9.0, 8.8, boxstyle="round,pad=0.2",
                        fc='#FFFBEB', ec='#D97706', lw=1.5)
    ax3.add_patch(b3)
    
    # Role-playing cards
    roles = [
        (1.0, 6.8, "Role: Clinical Lead", "Goal: Phác đồ chuẩn Bộ Y Tế", "#B45309"),
        (1.0, 4.8, "Role: Senior Pharmacist", "Goal: Bắt lỗi tương tác thuốc", "#D97706"),
        (1.0, 2.8, "Role: Clinical Dietitian", "Goal: Thực đơn đái tháo đường", "#F59E0B")
    ]
    for rx, ry, r_title, r_goal, r_col in roles:
        rb = FancyBboxPatch((rx, ry), 8.0, 1.4, boxstyle="round,pad=0.1",
                            fc=r_col, ec='#78350F')
        ax3.add_patch(rb)
        ax3.text(rx+0.4, ry+0.85, r_title, fontweight='bold', color='white', fontsize=8.5)
        ax3.text(rx+0.4, ry+0.35, r_goal, color='#FEF3C7', fontsize=7.5)
        
    ax3.text(5.0, 0.9, "• Role + Goal + Backstory + Tasks\n• Triển khai theo phong cách công ty nhân sự\n• Quy trình Sequential & Hierarchical mượt mà",
             ha='center', fontsize=8, color='#1E293B')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    out_path = os.path.join(OUTPUT_DIR, "fig603_langgraph_vs_autogen_crewai.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"✓ Đã tạo thành công: {out_path}")

# =============================================================================
# HÌNH 6.4: QUY TRÌNH HỘI CHẨN Y TẾ LÂM SÀNG ĐA CHUYÊN KHOA
# =============================================================================
def generate_fig604():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title("QUY TRÌNH HỘI CHẨN LÂM SÀNG ĐA TÁC TỬ (MULTI-SPECIALTY CLINICAL MAS PIPELINE)",
                 fontsize=14, fontweight='bold', color='#1E3A8A', pad=15)
    
    # 1. BỆNH NHÂN ĐẦU VÀO
    p_box = FancyBboxPatch((0.5, 4.0), 2.2, 3.0, boxstyle="round,pad=0.15",
                           fc='#334155', ec='#0F172A', lw=1.5)
    ax.add_patch(p_box)
    ax.text(1.6, 6.4, "BỆNH NHÂN\n(ĐẦU VÀO)", ha='center', color='white', fontweight='bold', fontsize=9)
    ax.text(1.6, 5.1, "• HbA1c: 7.8%\n• Glucose: 145\n• eGFR: 42 mL\n• Đang dùng: Metformin\n• Hỏi: Rượu bia + Gà", 
            ha='center', color='#94A3B8', fontsize=7)
    
    # 2. TRIAGE AGENT
    tr_box = FancyBboxPatch((3.5, 4.5), 2.2, 2.0, boxstyle="round,pad=0.15",
                            fc='#0284C7', ec='#0369A1', lw=1.5)
    ax.add_patch(tr_box)
    ax.text(4.6, 5.7, "1. TRIAGE\nAGENT", ha='center', color='white', fontweight='bold', fontsize=9)
    ax.text(4.6, 4.9, "Sơ lọc lâm sàng &\nTrích xuất đặc trưng", ha='center', color='#E0F2FE', fontsize=7.5)
    ax.annotate('', xy=(3.5, 5.5), xytext=(2.7, 5.5), arrowprops=dict(arrowstyle='->', color='#0284C7', lw=2))

    # 3. BA TÁC TỬ CHUYÊN KHOA SONG SONG
    spec_agents = [
        (6.8, 7.2, "2. DIAGNOSTIC\nDL AGENT", "Chẩn đoán MLP/CNN:\nTiểu đường Type 2 (99%)", "#059669"),
        (6.8, 4.5, "3. PHARMACIST\nKG AGENT", "Đồ thị Tri thức Dược thư:\nCHỐNG CHỈ ĐỊNH RƯỢU BIA\nCảnh báo giảm liều do eGFR", "#D97706"),
        (6.8, 1.8, "4. DIETITIAN\nAGENT", "Cẩm nang Dinh dưỡng:\nĂn ức gà luộc bỏ da\nKiêng gà chiên dầu mỡ", "#7C3AED")
    ]
    for sx, sy, title, desc, col in spec_agents:
        sb = FancyBboxPatch((sx, sy), 2.6, 1.8, boxstyle="round,pad=0.15",
                            fc=col, ec='#1F2937', lw=1.4)
        ax.add_patch(sb)
        ax.text(sx+1.3, sy+1.3, title, ha='center', va='center', color='white', fontweight='bold', fontsize=8.5)
        ax.text(sx+1.3, sy+0.6, desc, ha='center', va='center', color='#FEF08A', fontsize=7)
        # Nối từ Triage sang 3 Specialist
        ax.annotate('', xy=(sx, sy+0.9), xytext=(5.7, 5.5),
                    arrowprops=dict(arrowstyle='->', color='#64748B', lw=1.5))
        
    # 4. REGULATORY AGENT
    reg_box = FancyBboxPatch((10.3, 7.2), 2.4, 1.8, boxstyle="round,pad=0.15",
                            fc='#DC2626', ec='#991B1B', lw=1.4)
    ax.add_patch(reg_box)
    ax.text(11.5, 8.4, "5. REGULATORY\nRAG AGENT", ha='center', color='white', fontweight='bold', fontsize=8.5)
    ax.text(11.5, 7.7, "Tra cứu Quyết định\n5481/QĐ-BYT Bộ Y Tế", ha='center', color='#FEE2E2', fontsize=7.5)
    
    # 5. CMO SUPERVISOR AGENT
    cmo_box = FancyBboxPatch((10.3, 2.5), 2.4, 3.8, boxstyle="round,pad=0.2",
                            fc='#1E3A8A', ec='#172554', lw=2)
    ax.add_patch(cmo_box)
    ax.text(11.5, 5.5, "6. BÁC SĨ TRƯỞNG\n(CMO SUPERVISOR)", ha='center', color='white', fontweight='bold', fontsize=9.5)
    ax.text(11.5, 4.0, "• Hội chẩn đa chuyên khoa\n• Giải quyết xung đột liều\n• Phê chuẩn phác đồ an toàn\n• Chặn đứng ảo giác y khoa",
            ha='center', color='#93C5FD', fontsize=7.5)
    
    # Nối các chuyên khoa vào CMO Supervisor
    for sx, sy, _, _, _ in spec_agents:
        ax.annotate('', xy=(10.3, 4.4), xytext=(sx+2.6, sy+0.9),
                    arrowprops=dict(arrowstyle='->', color='#1E3A8A', lw=1.6))
    ax.annotate('', xy=(11.5, 6.3), xytext=(11.5, 7.2),
                arrowprops=dict(arrowstyle='->', color='#DC2626', lw=1.6))
    
    # 6. PHÁC ĐỒ ĐIỀU TRỊ CUỐI CÙNG
    out_box = FancyBboxPatch((13.4, 3.0), 1.4, 3.0, boxstyle="round,pad=0.1",
                            fc='#047857', ec='#064E3B', lw=2)
    ax.add_patch(out_box)
    ax.text(14.1, 4.5, "PHÁC ĐỒ\nCUỐI CÙNG\n(AN TOÀN 100%)", ha='center', va='center',
            color='white', fontweight='bold', fontsize=8.5)
    ax.annotate('', xy=(13.4, 4.5), xytext=(12.7, 4.5),
                arrowprops=dict(arrowstyle='->', color='#047857', lw=2.5))
    
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig604_healthcare_multi_agent_flow.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"✓ Đã tạo thành công: {out_path}")

# =============================================================================
# HÌNH 6.5: TRANH LUẬN ĐA TÁC TỬ TÀI CHÍNH (MULTI-AGENT DEBATE)
# =============================================================================
def generate_fig605():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title("CƠ CHẾ TRANH LUẬN ĐA TÁC TỬ (MULTI-AGENT DEBATE) TRONG BÀN GIAO DỊCH TÀI CHÍNH VN30 & VÀNG SJC",
                 fontsize=13.5, fontweight='bold', color='#1E3A8A', pad=15)
    
    # Trục thời gian 3 vòng tranh luận (Round 1, 2, 3)
    ax.axvline(4.3, color='#CBD5E1', ls='--', lw=1.5)
    ax.axvline(8.6, color='#CBD5E1', ls='--', lw=1.5)
    
    ax.text(2.1, 9.4, "VÒNG 1: ĐỀ XUẤT ĐỘC LẬP\n(Independent Pitch)", ha='center', fontweight='bold', color='#1E293B', fontsize=9.5)
    ax.text(6.45, 9.4, "VÒNG 2: PHẢN BIỆN CHÉO\n(Cross-Examination / Rebuttal)", ha='center', fontweight='bold', color='#B91C1C', fontsize=9.5)
    ax.text(10.8, 9.4, "VÒNG 3: ĐỒNG THUẬN QUỸ\n(Consensus & Allocation)", ha='center', fontweight='bold', color='#047857', fontsize=9.5)
    
    # Tác tử A: Macro Analyst
    a1 = FancyBboxPatch((0.4, 6.2), 3.4, 2.4, boxstyle="round,pad=0.1", fc='#1E40AF', ec='#1E3A8A')
    ax.add_patch(a1)
    ax.text(2.1, 8.0, "MACRO ANALYST", ha='center', color='white', fontweight='bold', fontsize=8.5)
    ax.text(2.1, 6.9, "• USD/VND tăng mạnh\n• FPT hưởng lợi tỷ giá\n• Khuyến nghị: Tăng tỷ trọng", color='#DBEAFE', fontsize=7.5, ha='center')
    
    # Tác tử B: Quant BiLSTM
    b1 = FancyBboxPatch((0.4, 3.4), 3.4, 2.4, boxstyle="round,pad=0.1", fc='#047857', ec='#064E3B')
    ax.add_patch(b1)
    ax.text(2.1, 5.2, "QUANT BiLSTM AGENT", ha='center', color='white', fontweight='bold', fontsize=8.5)
    ax.text(2.1, 4.1, "• BiLSTM dự báo FPT +1.8%\n• Vàng SJC biên độ 90-92tr\n• Tín hiệu: Mua lướt sóng", color='#D1FAE5', fontsize=7.5, ha='center')

    # Tác tử C: Risk & Compliance
    c1 = FancyBboxPatch((0.4, 0.6), 3.4, 2.4, boxstyle="round,pad=0.1", fc='#B91C1C', ec='#7F1D1D')
    ax.add_patch(c1)
    ax.text(2.1, 2.4, "RISK & COMPLIANCE", ha='center', color='white', fontweight='bold', fontsize=8.5)
    ax.text(2.1, 1.3, "• Áp lực lạm phát cao\n• Vàng SJC rủi ro can thiệp NHNN\n• Khuyến nghị: Phòng thủ tiền mặt", color='#FEE2E2', fontsize=7.5, ha='center')

    # VÒNG 2: TRANH LUẬN
    deb1 = FancyBboxPatch((4.7, 4.8), 3.5, 3.8, boxstyle="round,pad=0.1", fc='#FEF2F2', ec='#EF4444', lw=1.5)
    ax.add_patch(deb1)
    ax.text(6.45, 8.0, "TRANH LUẬN NẢY LỬA", ha='center', color='#991B1B', fontweight='bold', fontsize=9)
    ax.text(6.45, 6.3, "• Risk Agent: 'BiLSTM bỏ qua rủi ro chính sách đấu thầu vàng của NHNN!'\n• Macro Agent: 'Nhưng dòng tiền xuất khẩu FPT được bảo chứng thực tế!'\n• Quant Agent: 'Độ tin cậy mô hình 94.2% trong ngắn hạn.'", 
            ha='center', color='#1E293B', fontsize=7.5)
    
    ax.annotate('', xy=(4.7, 7.0), xytext=(3.8, 7.4), arrowprops=dict(arrowstyle='->', color='#1E40AF', lw=1.5))
    ax.annotate('', xy=(4.7, 6.5), xytext=(3.8, 4.6), arrowprops=dict(arrowstyle='->', color='#047857', lw=1.5))
    ax.annotate('', xy=(4.7, 5.5), xytext=(3.8, 1.8), arrowprops=dict(arrowstyle='->', color='#B91C1C', lw=1.5))

    # VÒNG 3: QUYẾT ĐỊNH DANH MỤC
    pm_box = FancyBboxPatch((9.2, 2.5), 4.2, 5.0, boxstyle="round,pad=0.2", fc='#0F172A', ec='#0284C7', lw=2)
    ax.add_patch(pm_box)
    ax.text(11.3, 6.8, "PORTFOLIO MANAGER\n(QUYẾT ĐỊNH ĐỒNG THUẬN)", ha='center', color='#38BDF8', fontweight='bold', fontsize=9.5)
    ax.text(11.3, 4.5, "1. CỔ PHIẾU FPT (Tỷ trọng 50%):\n   Đồng thuận tăng mạnh nhờ tỷ giá\n   và tăng trưởng lợi nhuận.\n\n2. VÀNG SJC (Tỷ trọng 20%):\n   Hạ tỷ trọng phòng ngừa NHNN\n   thu hẹp chênh lệch Nghị định 24.\n\n3. TIỀN MẶT / VCB (Tỷ trọng 30%):\n   Đảm bảo thanh khoản phòng thủ.",
            ha='center', color='white', fontsize=8)
    
    ax.annotate('', xy=(9.2, 6.0), xytext=(8.2, 6.5), arrowprops=dict(arrowstyle='->', color='#0284C7', lw=2))

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig605_financial_multi_agent_debate.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"✓ Đã tạo thành công: {out_path}")

# =============================================================================
# HÌNH 6.6: GIAO DIỆN WEB APP DASHBOARD GIÁM SÁT HỆ ĐA TÁC TỬ THỜI GIAN THỰC
# =============================================================================
def generate_fig606():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Header Streamlit Dashboard
    ax.text(0.5, 9.4, "HỆ THỐNG GIÁM SÁT TÁC TỬ ĐA MIỀN THỜI GIAN THỰC (MULTI-AGENT SYSTEM MONITOR - PTIT 2026)",
            color='#38BDF8', fontweight='bold', fontsize=12)
    ax.text(0.5, 8.9, "Học viên: Phạm Văn Tư - B23DCCN879 | Nhóm lớp: CT | GVHD: PGS.TS Trần Đình Quế",
            color='#94A3B8', fontsize=8.5)
    
    # 3 CỘT TRỰC QUAN HÓA STREAMLIT
    # CỘT 1: BẢNG THIẾT LẬP THAM SỐ (LEFT PANEL)
    c1 = FancyBboxPatch((0.5, 0.5), 3.8, 8.0, boxstyle="round,pad=0.15", fc='#1E293B', ec='#334155', lw=1.5)
    ax.add_patch(c1)
    ax.text(2.4, 8.0, "1. CẤU HÌNH ĐẦU VÀO LÂM SÀNG", color='white', fontweight='bold', fontsize=9, ha='center')
    
    params = [
        "Chỉ số HbA1c: 7.8% (Cực cao)",
        "Đường huyết đói: 145 mg/dL",
        "Chỉ số eGFR: 42 mL/min (Suy thận độ 3)",
        "Thuốc đang dùng: Metformin 1000mg",
        "Câu hỏi: Uống rượu bia & ăn gà?"
    ]
    yp = 7.2
    for p in params:
        ax.text(0.8, yp, f"• {p}", color='#E2E8F0', fontsize=8)
        yp -= 0.65
        
    btn = FancyBboxPatch((0.8, 3.0), 3.2, 0.8, boxstyle="round,pad=0.1", fc='#2563EB', ec='#1D4ED8')
    ax.add_patch(btn)
    ax.text(2.4, 3.4, "KÍCH HOẠT HỘI CHẨN MAS", color='white', fontweight='bold', fontsize=8.5, ha='center')

    # CỘT 2: ĐỒ THỊ MẠNG LƯỚI TÁC TỬ (CENTER PANEL - AGENT NETWORK GRAPH)
    c2 = FancyBboxPatch((4.6, 0.5), 5.6, 8.0, boxstyle="round,pad=0.15", fc='#1E293B', ec='#334155', lw=1.5)
    ax.add_patch(c2)
    ax.text(7.4, 8.0, "2. ĐỒ THỊ TƯƠNG TÁC TÁC TỬ (LIVE NETWORK)", color='#38BDF8', fontweight='bold', fontsize=9, ha='center')
    
    # Các Node Tác tử hoạt động
    mas_nodes = [
        (7.4, 5.8, "CMO Supervisor", "#1E40AF"),
        (5.6, 6.8, "Triage Agent", "#0284C7"),
        (9.2, 6.8, "Diagnostic DL", "#059669"),
        (5.6, 3.8, "Pharmacist KG", "#D97706"),
        (9.2, 3.8, "Dietitian Agent", "#7C3AED"),
        (7.4, 2.0, "Regulatory RAG", "#DC2626")
    ]
    for nx_pos, ny_pos, n_lbl, n_col in mas_nodes:
        circle = patches.Circle((nx_pos, ny_pos), 0.65, fc=n_col, ec='#F8FAFC', lw=1.2)
        ax.add_patch(circle)
        ax.text(nx_pos, ny_pos-0.95, n_lbl, ha='center', color='white', fontweight='bold', fontsize=7.5)
        
    # Đường truyền tin động
    for i in range(1, len(mas_nodes)):
        ax.annotate('', xy=(7.4, 5.8), xytext=(mas_nodes[i][0], mas_nodes[i][1]),
                    arrowprops=dict(arrowstyle='<->', color='#38BDF8', lw=1.5, ls='--'))
        
    ax.text(7.4, 1.0, "Trạng thái: 6/6 Tác tử trực tuyến | Tin nhắn đã trao đổi: 18", 
            ha='center', color='#4ADE80', fontsize=8, fontweight='bold')

    # CỘT 3: BIÊN BẢN HỘI CHẨN & ĐỒNG THUẬN (RIGHT PANEL - CONSENSUS TRACE)
    c3 = FancyBboxPatch((10.5, 0.5), 4.0, 8.0, boxstyle="round,pad=0.15", fc='#1E293B', ec='#334155', lw=1.5)
    ax.add_patch(c3)
    ax.text(12.5, 8.0, "3. BIÊN BẢN HỘI CHẨN & PHÁC ĐỒ", color='#4ADE80', fontweight='bold', fontsize=9, ha='center')
    
    trace_lines = [
        "[08:45:01] Triage: Da phan tach 4 chi so.",
        "[08:45:02] Diagnostic: Dai thao duong Type 2.",
        "[08:45:03] Pharmacist KG: PHAT HIEN NGUY CO!",
        "  - Tuyet doi cam con + Metformin.",
        "  - eGFR 42: Giam lieu con 500mg/ngay.",
        "[08:45:04] Dietitian: Duoc an uc ga luoc.",
        "[08:45:05] Regulatory: Trich dan QD 5481/BYT.",
        "[08:45:06] CMO: Phe duyet phac do tong the."
    ]
    yt = 7.3
    for tl in trace_lines:
        col = '#F87171' if 'NGUY CƠ' in tl or 'cấm' in tl else ('#38BDF8' if 'CMO' in tl else '#E2E8F0')
        ax.text(10.8, yt, tl, color=col, fontsize=7.2, family='monospace')
        yt -= 0.52
        
    res_box = FancyBboxPatch((10.8, 0.8), 3.4, 2.2, boxstyle="round,pad=0.1", fc='#047857', ec='#059669')
    ax.add_patch(res_box)
    ax.text(12.5, 2.5, "KẾT LUẬN CUỐI CÙNG:", color='white', fontweight='bold', fontsize=8, ha='center')
    ax.text(12.5, 1.5, "1. TUYỆT ĐỐI KHÔNG UỐNG RƯỢU\n2. GIẢM LIỀU METFORMIN CÒN 500MG\n3. ĐƯỢC ĂN ỨC GÀ NẠC BỎ DA LUỘC",
            color='#FEF08A', fontsize=7.2, ha='center', fontweight='bold')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig606_mas_webapp_dashboard.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"✓ Đã tạo thành công: {out_path}")

if __name__ == '__main__':
    print("--- Bắt đầu khởi tạo các sơ đồ đồ họa chất lượng cao cho Chương 6 (MAS) ---")
    generate_fig601()
    generate_fig602()
    generate_fig603()
    generate_fig604()
    generate_fig605()
    generate_fig606()
    print("✓ Đã hoàn thành toàn bộ 6 biểu đồ cho Chương 6!")
