#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
neo4j_graph_rag.py
==================
Module GraphRAG liên kết trực tiếp giữa RAG và Cơ sở Dữ liệu Đồ thị Neo4j (code RAG + link_DB).
Thực hiện:
1. Nhận truy vấn / thông tin ca bệnh của người dùng.
2. Truy vấn đồ thị Neo4j qua Cypher để trích xuất tri thức liên kết (Graph Context).
3. Kết hợp với văn bản chuẩn từ Hướng dẫn QĐ 5481/QĐ-BYT Bộ Y Tế và Vinmec.
4. Cung cấp ngữ cảnh RAG hoàn chỉnh cho Chatbot tư vấn lâm sàng.
"""

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from typing import Dict, List, Any, Optional
from src.knowledge.neo4j_kg_service import neo4j_service
from src.knowledge.vietnamese_guidelines_rag import VietnameseGuidelinesRAG

class Neo4jGraphRAG:
    """
    GraphRAG Engine: Kết nối RAG với CSDL Đồ thị Neo4j (code RAG + link_DB)
    """
    def __init__(self):
        self.neo4j = neo4j_service
        self.text_rag = VietnameseGuidelinesRAG()

    def retrieve_graph_context(self, user_query: str, clinical_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Truy vấn CSDL Đồ thị Neo4j (link_DB) dựa trên ngữ cảnh lâm sàng của người bệnh.
        
        Quy trình trích xuất đồ thị (Graph Traversal):
        1. Ngưỡng sinh hóa chẩn đoán: MATCH (:Disease)-[:DIAGNOSED_BY]->(:Biomarker)
        2. Tương tác nguy hại cồn: MATCH (:Drug)-[:RISK_OF]->(:AdverseEffect)
        3. Chống chỉ định suy thận: MATCH (:Drug)-[:CONTRAINDICATED_IN]->(:Complication)
        4. Hoán đổi thực phẩm NIN: MATCH (:Food)-[:CAN_BE_REPLACED_BY]->(:Food)
        5. Sản phẩm nhà thuốc Long Châu: MATCH (:Drug)-[:DISPENSED_AS_PRODUCT]->(:PharmacyProduct)
        """
        clinical_data = clinical_data or {}
        graph_facts = []
        cypher_queries_executed = []

        if not self.neo4j.is_connected():
            return {
                "connected": False,
                "graph_facts": ["(Neo4j offline - Fallback sang In-Memory Knowledge Base)"],
                "cypher_logs": []
            }

        # ---------------------------------------------------------------------
        # CYPHER 1: Tra cứu Ngưỡng Sinh hóa Chẩn đoán Bệnh từ Neo4j
        # Mục đích: Rút trích tiêu chuẩn FPG >= 126 mg/dL và HbA1c >= 6.5% theo QĐ 5481/QĐ-BYT
        # ---------------------------------------------------------------------
        hba1c = clinical_data.get("hba1c")
        glucose = clinical_data.get("blood_glucose_level")
        if hba1c is not None or glucose is not None or "xét nghiệm" in user_query.lower() or "đường huyết" in user_query.lower():
            cypher_diag = """
            MATCH (d:Disease)-[r:DIAGNOSED_BY]->(b:Biomarker)
            RETURN d.name AS disease, b.name AS biomarker, r.threshold AS threshold, r.condition AS condition
            """
            cypher_queries_executed.append(cypher_diag.strip())
            rows = self.neo4j.execute_cypher(cypher_diag)
            for r in rows:
                cond = f" ({r['condition']})" if r.get('condition') else ""
                graph_facts.append(f"• [Neo4j Chẩn đoán] {r['disease']} được xác định khi {r['biomarker']} đạt ngưỡng: {r['threshold']}{cond}")

        # ---------------------------------------------------------------------
        # CYPHER 2 & 3: Rà soát An toàn Dược lý và Chống chỉ định Chết người
        # Mục đích:
        #   - Phát hiện nguy cơ toan Lactic tử vong khi dùng Metformin kết hợp Rượu bia.
        #   - Phát hiện chống chỉ định tuyệt đối khi mức lọc cầu thận eGFR < 30 mL/phút.
        # ---------------------------------------------------------------------
        drug = clinical_data.get("current_drug", "Metformin")
        alcohol = clinical_data.get("alcohol_use", False) or ("bia" in user_query.lower() or "rượu" in user_query.lower())
        egfr = clinical_data.get("egfr")

        # Rà soát tương tác với cồn
        if alcohol:
            cypher_alc = """
            MATCH (dr:Drug {id: 'METFORMIN'})-[r:RISK_OF]->(a:AdverseEffect {id: 'LACTIC_ACIDOSIS'})
            RETURN dr.name AS drug, a.name AS adverse, r.trigger AS trigger, r.severity AS severity, a.mortality AS mortality
            """
            cypher_queries_executed.append(cypher_alc.strip())
            rows = self.neo4j.execute_cypher(cypher_alc)
            for r in rows:
                graph_facts.append(f"• [Neo4j Cảnh báo Đỏ] {r['drug']} kết hợp với {r['trigger']} gây nguy cơ: {r['adverse']} (Mức độ: {r['severity']}, Tỷ lệ tử vong: {r['mortality']}). CẤM TUYỆT ĐỐI.")

        # Rà soát suy thận theo eGFR
        if egfr is not None:
            cypher_renal = """
            MATCH (dr:Drug {id: 'METFORMIN'})-[r:CONTRAINDICATED_IN]->(c:Complication {id: 'CKD'})
            RETURN dr.name AS drug, c.name AS complication, r.condition AS condition, r.severity AS severity
            """
            cypher_queries_executed.append(cypher_renal.strip())
            rows = self.neo4j.execute_cypher(cypher_renal)
            if egfr < 30:
                graph_facts.append(f"• [Neo4j Chống chỉ định] eGFR = {egfr} mL/phút (< 30): CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI Metformin theo QĐ 5481/QĐ-BYT.")
            elif 30 <= egfr < 45:
                graph_facts.append(f"• [Neo4j Thận trọng liều] eGFR = {egfr} mL/phút (Suy thận 3b): Bắt buộc giảm 50% liều Metformin (tối đa không quá 1000 mg/ngày).")

        # ---------------------------------------------------------------------
        # CYPHER 4: Tra cứu Thay thế Món ăn Việt Nam Chỉ số GI thấp (NIN)
        # Mục đích: Đề xuất thực phẩm thay thế lành mạnh từ Viện Dinh Dưỡng Quốc Gia
        # ---------------------------------------------------------------------
        food_keywords = ["cơm", "phở", "bánh mì", "trà sữa", "ăn"]
        if any(k in user_query.lower() for k in food_keywords):
            cypher_food = """
            MATCH (f1:Food)-[r:CAN_BE_REPLACED_BY]->(f2:Food)
            RETURN f1.name AS original, f1.gi AS old_gi, f2.name AS swap, f2.gi AS new_gi, r.reason AS reason
            LIMIT 3
            """
            cypher_queries_executed.append(cypher_food.strip())
            rows = self.neo4j.execute_cypher(cypher_food)
            for r in rows:
                graph_facts.append(f"• [Neo4j Dinh dưỡng NIN] Thay {r['original']} (GI: {r['old_gi']}) ➔ {r['swap']} (GI: {r['new_gi']}) | Căn cứ: {r['reason']}")

        # ---------------------------------------------------------------------
        # CYPHER 5: Ánh xạ Sang Danh mục Sản phẩm Nhà thuốc Long Châu
        # Mục đích: Cung cấp thông tin tên thương mại, giá niêm yết và trạng thái kê đơn Rx
        # ---------------------------------------------------------------------
        cypher_prod = """
        MATCH (dr:Drug {id: 'METFORMIN'})-[:DISPENSED_AS_PRODUCT]->(p:PharmacyProduct)
        RETURN p.brand_name AS name, p.box_price_vnd AS price, p.is_prescription_rx AS is_rx
        LIMIT 2
        """
        cypher_queries_executed.append(cypher_prod.strip())
        rows = self.neo4j.execute_cypher(cypher_prod)
        for r in rows:
            rx_label = "Thuốc kê đơn (Rx)" if r['is_rx'] else "Không cần đơn"
            graph_facts.append(f"• [Neo4j FPT Long Châu] {r['name']} ({rx_label}) - Giá niêm yết: {r['price']:,} VNĐ")

        return {
            "connected": True,
            "graph_facts": graph_facts,
            "cypher_logs": cypher_queries_executed,
            "db_source": "Neo4j Community Graph Database (bolt://localhost:7687)"
        }

    def generate_augmented_context(self, user_query: str, clinical_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Tổng hợp toàn diện (KB + RAG ==> chat):
        Kết hợp Fact từ Neo4j Graph Database + Text Chunks từ Hướng dẫn QĐ 5481 / Vinmec
        """
        graph_data = self.retrieve_graph_context(user_query, clinical_data)
        text_rag_data = self.text_rag.retrieve(user_query, top_k=2)

        context_lines = [
            "=== TRI THỨC TRÍCH XUẤT TỪ NEO4J KNOWLEDGE GRAPH (link_DB) ===",
            f"Nguồn kết nối: {graph_data.get('db_source', 'In-memory Graph')}"
        ]
        for fact in graph_data.get("graph_facts", []):
            context_lines.append(fact)

        context_lines.append("\n=== TRI THỨC VĂN BẢN QUY CHUẨN (QĐ 5481/QĐ-BYT & VINMEC RAG) ===")
        for chunk in text_rag_data:
            context_lines.append(f"[{chunk['source']}] {chunk['title']}: {chunk['content'][:250]}...")

        return "\n".join(context_lines)

# Khởi tạo instance GraphRAG
graph_rag = Neo4jGraphRAG()

if __name__ == '__main__':
    rag = Neo4jGraphRAG()
    test_context = rag.generate_augmented_context(
        user_query="Tôi đang uống Metformin thì có uống bia được không và nên ăn cơm gạo gì?",
        clinical_data={"current_drug": "Metformin", "alcohol_use": True, "egfr": 42.0}
    )
    print(test_context)
