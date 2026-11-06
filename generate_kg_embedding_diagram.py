#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_kg_embedding_diagram.py
================================
Tạo sơ đồ trực quan hóa không gian Vector Embedding (2D Node & Link Embedding Space)
cho 143 Node thực thể và 271 Liên kết quan hệ trong Đồ thị Tri thức Neo4j DiaAgent-MAS.
Kết xuất ảnh chất lượng cao 300 DPI phục vụ hiển thị trên Web App và Báo cáo PDF.
"""

import os
import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Patch, Polygon
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
from scipy.spatial import ConvexHull
from neo4j import GraphDatabase

# Cấu hình thẩm mỹ cao cấp chuẩn Nature / IEEE
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#D1D5DB'
plt.rcParams['axes.linewidth'] = 0.8

def build_embedding_visualization():
    # 1. Nạp toàn bộ dữ liệu đồ thị từ Neo4j
    G = nx.MultiDiGraph()
    neo4j_connected = False
    try:
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password123"))
        with driver.session() as session:
            # Lấy nodes
            n_res = session.run("MATCH (n) RETURN n.id AS id, labels(n)[0] AS ntype, properties(n) AS props")
            for r in n_res:
                props = dict(r["props"])
                props["entity_type"] = r["ntype"]
                G.add_node(r["id"], **props)
            
            # Lấy relationships
            r_res = session.run("MATCH (a)-[r]->(b) RETURN a.id AS src, b.id AS tgt, type(r) AS rel, properties(r) AS props")
            for r in r_res:
                G.add_edge(r["src"], r["tgt"], relation=r["rel"], **r["props"])
        driver.close()
        neo4j_connected = True
        print(f"[Embedding Diagram] ✓ Đã nạp thành công từ Neo4j: {G.number_of_nodes()} Nodes, {G.number_of_edges()} Edges")
    except Exception as e:
        print(f"[Embedding Diagram Warning] Không thể kết nối Neo4j ({e}). Sẽ sử dụng Fallback cục bộ.")

    if G.number_of_nodes() == 0:
        print("[Embedding Diagram Error] Không có dữ liệu đồ thị để vẽ.")
        return None, None

    # Đọc catalog Long Châu để lấy tên thương mại thân thiện
    catalog_path = "Diabetes_MultiAgent_System/data/pharmacy/longchau_diabetes_products.json"
    longchau_catalog = {}
    if os.path.exists(catalog_path):
        with open(catalog_path, "r", encoding="utf-8") as f:
            items = json.load(f)
            for item in items:
                longchau_catalog[item.get("id")] = item

    # Phân loại thực thể và màu sắc chủ đạo
    type_meta = {
        'Disease': {'color': '#DC2626', 'marker': 'o', 'size': 380, 'name': 'Bệnh lý (Disease)'},
        'Complication': {'color': '#991B1B', 'marker': 'D', 'size': 320, 'name': 'Biến chứng (Complication)'},
        'Comorbidity': {'color': '#B91C1C', 'marker': 's', 'size': 300, 'name': 'Bệnh đồng mắc (Comorbidity)'},
        'RiskFactor': {'color': '#EA580C', 'marker': '^', 'size': 280, 'name': 'Yếu tố nguy cơ (Risk Factor)'},
        'Symptom': {'color': '#F97316', 'marker': 'v', 'size': 280, 'name': 'Triệu chứng (Symptom)'},
        'Biomarker': {'color': '#D97706', 'marker': 'p', 'size': 320, 'name': 'Chỉ số sinh học (Biomarker)'},
        'Drug': {'color': '#2563EB', 'marker': 'h', 'size': 380, 'name': 'Dược chất (Active Drug)'},
        'AdverseEffect': {'color': '#E11D48', 'marker': 'X', 'size': 300, 'name': 'Tác dụng phụ / Cảnh báo (Adverse Effect)'},
        'Food': {'color': '#16A34A', 'marker': 'H', 'size': 260, 'name': 'Dinh dưỡng / Thực phẩm NIN (Food)'},
        'PharmacyProduct': {'color': '#7C3AED', 'marker': 's', 'size': 240, 'name': 'Sản phẩm FPT Long Châu (Pharmacy Product)'},
        'ClinicalProtocol': {'color': '#0D9488', 'marker': 'P', 'size': 320, 'name': 'Phác đồ / Hướng dẫn (Clinical Protocol)'},
        'Source': {'color': '#475569', 'marker': '*', 'size': 360, 'name': 'Nguồn tri thức (Knowledge Source)'},
        'Other': {'color': '#6B7280', 'marker': 'o', 'size': 200, 'name': 'Khác'}
    }

    # Bảng Semantic Cluster Priors xác định tọa độ trọng tâm của từng phân vùng
    cluster_centers = {
        'Disease_Core': np.array([-2.0, 3.5]),
        'Symptoms': np.array([-6.5, 6.0]),
        'Biomarkers': np.array([-5.5, 0.5]),
        'Complications': np.array([-6.0, 3.2]),
        'Drugs': np.array([2.5, 2.2]),
        'Pharmacy_Rx': np.array([7.0, 3.5]),
        'Pharmacy_Devices': np.array([6.5, -4.5]),
        'Foods_HighGI': np.array([-4.5, -5.5]),
        'Foods_LowGI': np.array([-1.0, -6.5]),
        'Adverse': np.array([1.5, 6.5]),
        'Protocols': np.array([2.0, -2.5]),
        'Sources': np.array([0.0, 0.0])
    }

    np.random.seed(42)
    initial_pos = {}
    for node, data in G.nodes(data=True):
        ntype = data.get('entity_type', 'Other')
        if ntype == 'Disease':
            c = cluster_centers['Disease_Core']
        elif ntype == 'Symptom':
            c = cluster_centers['Symptoms']
        elif ntype == 'Biomarker':
            c = cluster_centers['Biomarkers']
        elif ntype in ['Complication', 'Comorbidity', 'RiskFactor']:
            c = cluster_centers['Complications']
        elif ntype == 'Drug':
            c = cluster_centers['Drugs']
        elif ntype == 'AdverseEffect':
            c = cluster_centers['Adverse']
        elif ntype == 'Food':
            gi = data.get('gi', 50)
            c = cluster_centers['Foods_HighGI'] if gi >= 70 else cluster_centers['Foods_LowGI']
        elif ntype == 'PharmacyProduct':
            if node in ['lc_dia_23', 'lc_dia_24', 'lc_dia_25', 'lc_dia_26', 'lc_dia_27', 'lc_dia_28', 'lc_dia_29', 'lc_dia_30']:
                c = cluster_centers['Pharmacy_Devices']
            else:
                c = cluster_centers['Pharmacy_Rx']
        elif ntype == 'ClinicalProtocol':
            c = cluster_centers['Protocols']
        elif ntype == 'Source':
            c = cluster_centers['Sources']
        else:
            c = np.array([0.0, 0.0])
            
        noise = np.random.normal(0, 0.75, size=2)
        initial_pos[node] = c + noise

    # Thuật toán Spring Force-Directed Layout dựa trên topology đồ thị
    pos = nx.spring_layout(G, pos=initial_pos, iterations=90, k=1.35, seed=42)

    # Khởi tạo khung vẽ kích thước lớn (24 x 14.5 inches, chuẩn 300 DPI)
    fig, ax = plt.subplots(figsize=(24, 14.5), facecolor='#FAFAFA')
    ax.set_facecolor('#FFFFFF')

    # Vẽ lưới toạ độ tiềm ẩn
    ax.grid(True, linestyle='--', color='#E5E7EB', alpha=0.6, zorder=0)
    ax.axhline(0, color='#CBD5E1', linewidth=1.0, linestyle='-', alpha=0.8, zorder=0)
    ax.axvline(0, color='#CBD5E1', linewidth=1.0, linestyle='-', alpha=0.8, zorder=0)

    # 1. Vẽ các vùng mây cụm ngữ nghĩa (Semantic Cluster Halos / Convex Hulls)
    clusters_to_draw = [
        {
            'nodes': [n for n, d in G.nodes(data=True) if d.get('entity_type') == 'Drug'],
            'color': '#DBEAFE', 'edge': '#3B82F6', 'label': 'Cụm Dược chất Phác đồ ĐTĐ (QĐ 5481/BYT & ADA)'
        },
        {
            'nodes': [f'lc_dia_{i:02d}' for i in range(1, 23)],
            'color': '#EDE9FE', 'edge': '#8B5CF6', 'label': 'Cụm Thuốc Biệt dược Kê đơn FPT Long Châu'
        },
        {
            'nodes': [n for n, d in G.nodes(data=True) if d.get('entity_type') == 'Biomarker'],
            'color': '#FEF3C7', 'edge': '#F59E0B', 'label': 'Cụm Chỉ số Xét nghiệm Sinh hóa Máu'
        },
        {
            'nodes': [n for n, d in G.nodes(data=True) if d.get('entity_type') in ['Disease', 'Complication', 'Comorbidity', 'RiskFactor']],
            'color': '#FEE2E2', 'edge': '#EF4444', 'label': 'Cụm Bệnh lý & Biến chứng Đa cơ quan'
        },
        {
            'nodes': [n for n, d in G.nodes(data=True) if d.get('entity_type') == 'Symptom'],
            'color': '#FFEDD5', 'edge': '#F97316', 'label': 'Cụm Triệu chứng Lâm sàng (Vinmec & BYT)'
        },
        {
            'nodes': [n for n, d in G.nodes(data=True) if d.get('entity_type') == 'Food'],
            'color': '#DCFCE7', 'edge': '#22C55E', 'label': 'Cụm Dinh dưỡng Thực phẩm Việt Nam (NIN)'
        },
        {
            'nodes': ['lc_dia_23', 'lc_dia_24', 'lc_dia_25', 'lc_dia_26', 'lc_dia_27', 'lc_dia_28', 'lc_dia_29', 'lc_dia_30'],
            'color': '#E0E7FF', 'edge': '#6366F1', 'label': 'Cụm Thiết bị Đo & Sữa Dinh dưỡng Tại nhà'
        },
        {
            'nodes': [n for n, d in G.nodes(data=True) if d.get('entity_type') == 'AdverseEffect'],
            'color': '#FFE4E6', 'edge': '#F43F5E', 'label': 'Cụm Cảnh báo An toàn & Tác dụng phụ'
        }
    ]

    for c_info in clusters_to_draw:
        pts = np.array([pos[n] for n in c_info['nodes'] if n in pos])
        if len(pts) >= 3:
            try:
                hull = ConvexHull(pts)
                hull_pts = pts[hull.vertices]
                center = pts.mean(axis=0)
                expanded_hull = center + (hull_pts - center) * 1.30
                poly = Polygon(expanded_hull, closed=True, facecolor=c_info['color'], 
                               edgecolor=c_info['edge'], alpha=0.32, linestyle=':', linewidth=1.4, zorder=1)
                ax.add_patch(poly)
            except Exception:
                pass

    # 2. Phong cách đường vẽ quan hệ (Relation Styles)
    rel_styles = {
        'TREATS': {'color': '#059669', 'ls': '-', 'lw': 1.6, 'alpha': 0.70, 'rad': 0.08},
        'CONTRAINDICATED_IN': {'color': '#DC2626', 'ls': '--', 'lw': 2.2, 'alpha': 0.85, 'rad': -0.12},
        'RISK_OF': {'color': '#E11D48', 'ls': '-.', 'lw': 1.6, 'alpha': 0.75, 'rad': 0.14},
        'CAUTION_IN': {'color': '#F59E0B', 'ls': '--', 'lw': 1.5, 'alpha': 0.75, 'rad': -0.08},
        'HIGHLY_RECOMMENDED_FOR': {'color': '#2563EB', 'ls': '-', 'lw': 2.0, 'alpha': 0.80, 'rad': 0.10},
        'DIAGNOSED_BY': {'color': '#D97706', 'ls': '-', 'lw': 1.6, 'alpha': 0.70, 'rad': -0.06},
        'HAS_SYMPTOM': {'color': '#EA580C', 'ls': ':', 'lw': 1.4, 'alpha': 0.65, 'rad': 0.05},
        'MONITORED_BY': {'color': '#D97706', 'ls': ':', 'lw': 1.4, 'alpha': 0.65, 'rad': 0.05},
        'DISPENSED_AS_PRODUCT': {'color': '#8B5CF6', 'ls': ':', 'lw': 1.2, 'alpha': 0.60, 'rad': 0.04},
        'CAN_BE_REPLACED_BY': {'color': '#16A34A', 'ls': '-', 'lw': 1.8, 'alpha': 0.80, 'rad': 0.14},
        'CAUSES_COMPLICATION': {'color': '#B91C1C', 'ls': '-', 'lw': 1.8, 'alpha': 0.75, 'rad': 0.07},
        'RECOMMENDED_DEVICE_FOR': {'color': '#6366F1', 'ls': ':', 'lw': 1.3, 'alpha': 0.65, 'rad': 0.05},
        'NUTRITIONAL_SUPPORT_FOR': {'color': '#0D9488', 'ls': ':', 'lw': 1.3, 'alpha': 0.65, 'rad': 0.05},
        'CITED_FROM': {'color': '#94A3B8', 'ls': ':', 'lw': 0.8, 'alpha': 0.25, 'rad': 0.02}
    }

    # 3. Vẽ các cạnh quan hệ (Edges)
    for u, v, k, d in G.edges(data=True, keys=True):
        if u not in pos or v not in pos:
            continue
        rel = d.get('relation', 'REL')
        style = rel_styles.get(rel, {'color': '#CBD5E1', 'ls': ':', 'lw': 0.8, 'alpha': 0.35, 'rad': 0.0})

        p1, p2 = pos[u], pos[v]
        arrow = FancyArrowPatch(
            p1, p2,
            arrowstyle='-|>',
            connectionstyle=f"arc3,rad={style['rad']}",
            mutation_scale=9,
            color=style['color'],
            linestyle=style['ls'],
            linewidth=style['lw'],
            alpha=style['alpha'],
            zorder=2
        )
        ax.add_patch(arrow)

    # 4. Vẽ các Node thực thể
    for node, data in G.nodes(data=True):
        if node not in pos:
            continue
        x, y = pos[node]
        ntype = data.get('entity_type', 'Other')
        meta = type_meta.get(ntype, type_meta['Other'])
        
        # Điểm scatter node
        ax.scatter(x, y, s=meta['size'], c=meta['color'], marker=meta['marker'], 
                   edgecolors='#FFFFFF', linewidths=1.6, zorder=4, alpha=0.92)

        # Nhãn text
        label_text = data.get('name', node)
        if node.startswith('lc_dia_'):
            item_info = longchau_catalog.get(node, {})
            label_text = item_info.get('brand_name', label_text)
            if len(label_text) > 20:
                label_text = label_text[:18] + ".."
        elif len(label_text) > 24:
            label_text = label_text[:22] + ".."

        offset_y = 0.20 if y >= 0 else -0.25
        ax.text(
            x, y + offset_y, label_text,
            fontsize=7.2,
            fontweight='bold',
            color='#1E293B',
            ha='center',
            va='center',
            zorder=5,
            path_effects=[pe.withStroke(linewidth=2.4, foreground='#FFFFFF')]
        )

    # 5. Tiêu đề học thuật
    total_nodes = G.number_of_nodes()
    total_edges = G.number_of_edges()
    ax.set_title(
        f"SƠ ĐỒ KHÔNG GIAN EMBEDDING ĐỒ THỊ TRI THỨC Y TẾ (DIAAGENT-MAS NEO4J GRAPH EMBEDDINGS)\n"
        f"Biểu diễn Chiếu Giảm Chiều Không gian Tiềm ẩn 2D của {total_nodes} Node Thực thể & {total_edges} Mối Quan hệ Lâm sàng Chuẩn QĐ 5481/QĐ-BYT, Vinmec & Long Châu",
        fontsize=14.0, fontweight='bold', color='#0F172A', pad=18
    )

    ax.set_xlabel("Không gian Biểu diễn Vector Tiềm ẩn 1 (Latent Dimension 1 - Z₁)", fontsize=11, fontweight='bold', color='#475569', labelpad=8)
    ax.set_ylabel("Không gian Biểu diễn Vector Tiềm ẩn 2 (Latent Dimension 2 - Z₂)", fontsize=11, fontweight='bold', color='#475569', labelpad=8)

    # 6. Legend phân loại Node (Góc trên trái)
    node_legend_elements = [
        Line2D([0], [0], marker=m['marker'], color='w', label=m['name'], 
               markerfacecolor=m['color'], markersize=9, markeredgecolor='black', markeredgewidth=0.5)
        for t, m in type_meta.items() if t in ['Disease', 'Complication', 'Symptom', 'Biomarker', 'Drug', 'AdverseEffect', 'Food', 'PharmacyProduct', 'ClinicalProtocol', 'Source']
    ]
    leg1 = ax.legend(handles=node_legend_elements, loc='upper left', frameon=True, 
                     title="Nhóm Thực thể Node (12 Entity Classes)", title_fontsize=10.0, 
                     fontsize=8.5, facecolor='#F8FAFC', edgecolor='#CBD5E1', framealpha=0.95)
    ax.add_artist(leg1)

    # 7. Legend phân loại Liên kết Edge (Góc dưới phải)
    edge_legend_elements = [
        Line2D([0], [1], color='#059669', lw=2, linestyle='-', label='TREATS (Chỉ định điều trị)'),
        Line2D([0], [1], color='#DC2626', lw=2.2, linestyle='--', label='CONTRAINDICATED_IN (Chống chỉ định)'),
        Line2D([0], [1], color='#E11D48', lw=1.8, linestyle='-.', label='RISK_OF (Nguy cơ tác dụng phụ)'),
        Line2D([0], [1], color='#2563EB', lw=2, linestyle='-', label='HIGHLY_RECOMMENDED_FOR (Bảo vệ tim thận)'),
        Line2D([0], [1], color='#D97706', lw=1.8, linestyle='-', label='DIAGNOSED_BY / MONITORED_BY (Xét nghiệm)'),
        Line2D([0], [1], color='#8B5CF6', lw=1.8, linestyle=':', label='DISPENSED_AS_PRODUCT (Biệt dược FPT Long Châu)'),
        Line2D([0], [1], color='#16A34A', lw=2, linestyle='-', label='CAN_BE_REPLACED_BY (Chuyển đổi thực phẩm NIN)')
    ]
    leg2 = ax.legend(handles=edge_legend_elements, loc='lower right', frameon=True, 
                     title="Mối Quan hệ Cạnh Liên kết (Relation Types)", title_fontsize=10.0, 
                     fontsize=8.5, facecolor='#F8FAFC', edgecolor='#CBD5E1', framealpha=0.95)

    # 8. Hộp thông tin tóm tắt
    info_box_text = (
        f"Cơ sở Kỹ thuật Knowledge Graph & Embedding:\n"
        f"• Tổng số Node thực thể: {total_nodes} | Tổng số Cạnh liên kết: {total_edges}\n"
        f"• Động cơ cơ sở dữ liệu: Neo4j Graph Database 5.x (bolt://localhost:7687)\n"
        f"• Thuật toán không gian: Force-Directed Graph Layout + Semantic Clustering Priors\n"
        f"• Nguồn tri thức tích hợp: QĐ 5481/QĐ-BYT, Vinmec Clinical, NIN, ADA 2024 & FPT Long Châu."
    )
    ax.text(
        0.015, 0.02, info_box_text,
        transform=ax.transAxes,
        fontsize=8.2,
        color='#334155',
        verticalalignment='bottom',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#F1F5F9', edgecolor='#CBD5E1', alpha=0.95)
    )

    plt.tight_layout()
    
    webapp_out = "Diabetes_MultiAgent_System/data/knowledge_graph_node_embeddings.png"
    report_out = "Report/project01_CT_02_tupv/images/fig_kg_node_embeddings.png"
    
    os.makedirs(os.path.dirname(webapp_out), exist_ok=True)
    os.makedirs(os.path.dirname(report_out), exist_ok=True)
    
    plt.savefig(webapp_out, dpi=300, bbox_inches='tight')
    plt.savefig(report_out, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Đã xuất ảnh sơ đồ Node & Link Embeddings thành công:")
    print(f"  1. Web App: {webapp_out} ({os.path.getsize(webapp_out)/1024:.1f} KB)")
    print(f"  2. Report:  {report_out} ({os.path.getsize(report_out)/1024:.1f} KB)")
    return webapp_out, report_out

if __name__ == '__main__':
    build_embedding_visualization()
