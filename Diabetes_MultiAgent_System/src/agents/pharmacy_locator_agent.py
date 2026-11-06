#!/usr/bin/env python3
"""
pharmacy_locator_agent.py
=========================
Agent Định vị & Báo giá Dược phẩm FPT Long Châu (Pharmacy Locator & Pricing Agent).
Chuẩn hóa logic thương mại y tế:
- Khi người bệnh CHƯA CÓ chẩn đoán xác định (giai đoạn sàng lọc):
  -> TUYỆT ĐỐI KHÔNG gợi ý thuốc điều trị kê đơn (Rx) như Metformin/Januvia.
  -> Chỉ gợi ý thiết bị y tế theo dõi cá nhân (Máy đo Accu-Chek, Que thử).
- Khi người bệnh ĐÃ CÓ chẩn đoán xác định:
  -> Ánh xạ chính xác hoạt chất sang sản phẩm thương mại tại Long Châu,
  -> Dự toán chi phí dùng thuốc theo tháng (VNĐ) và cảnh báo bắt buộc có đơn bác sĩ.
"""

from typing import Dict, Any, List, Optional
import sys
import os

from src.core.state_schema import DiabetesMASState, PharmacyItem
from src.knowledge.neo4j_kg_service import neo4j_service

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
pharmacy_dir = os.path.join(base_dir, "data", "pharmacy")
if pharmacy_dir not in sys.path:
    sys.path.insert(0, pharmacy_dir)

from crawl_longchau_diabetes import LongChauDiabetesCrawler


class PharmacyLocatorAgent:
    """
    Agent quản lý danh mục sản phẩm Long Châu tương thích với tình trạng bệnh án.
    """

    def __init__(self):
        self.crawler = LongChauDiabetesCrawler()

    def run(self, state: DiabetesMASState) -> DiabetesMASState:
        rx = state.clinical_prescription
        matched_items: List[PharmacyItem] = []
        total_monthly_cost = 0

        # =====================================================================
        # TRƯỜNG HỢP 1: GIAI ĐOẠN SÀNG LỌC / CHƯA KẾT LUẬN BỆNH (KHÔNG KÊ THUỐC RX)
        # =====================================================================
        if rx.assessment_type == "SCREENING_RECOMMENDATION" or not rx.has_confirmed_diabetes or not rx.primary_drug:
            # Chỉ gợi ý máy đo đường huyết và que thử để theo dõi
            device_prods = self.crawler.search_local("Accu-Chek", limit=2)
            for p in device_prods:
                item = PharmacyItem(
                    product_id=p["id"],
                    brand_name=p["brand_name"],
                    active_ingredient=p.get("active_ingredient", "Thiết bị y tế theo dõi"),
                    drug_class="Thiết bị y tế theo dõi tại nhà",
                    unit_price_vnd=p.get("unit_price_vnd", 0),
                    box_price_vnd=p.get("box_price_vnd", 0),
                    is_prescription_rx=False,
                    indication="Theo dõi chỉ số đường huyết cá nhân tại nhà (Không cần đơn bác sĩ)",
                    longchau_url=p.get("longchau_url", ""),
                    monthly_cost_vnd=0
                )
                matched_items.append(item)

            state.pharmacy_items = matched_items
            state.total_monthly_pharmacy_cost_vnd = 0
            state.agent_execution_logs.append({
                "agent": "PharmacyLocatorAgent",
                "status": "DEVICE_ONLY_SUCCESS",
                "message": f"Chưa có chẩn đoán xác định -> Khóa danh mục thuốc điều trị Rx; chỉ hiển thị máy đo & que thử"
            })
            return state

        # =====================================================================
        # TRƯỜNG HỢP 2: ĐÃ CÓ CHẨN ĐOÁN XÁC ĐỊNH -> ÁNH XẠ THUỐC ĐIỀU TRỊ
        # =====================================================================
        primary_name = rx.primary_drug or "Metformin"
        prods_primary = []

        # ---------------------------------------------------------------------
        # TRUY XUẤT NEO4J GRAPH-RAG: Ánh xạ hoạt chất sang biệt dược FPT Long Châu
        # Mục đích:
        #   - Gửi truy vấn Cypher tới CSDL Neo4j:
        #       MATCH (dr:Drug)-[:DISPENSED_AS_PRODUCT]->(p:PharmacyProduct)
        #       WHERE toLower(dr.name) CONTAINS toLower($name)...
        #   - Khai thác quan hệ [:DISPENSED_AS_PRODUCT] liên kết giữa hoạt chất y khoa
        #     chuẩn và 30 sản phẩm thực tế của chuỗi nhà thuốc FPT Long Châu.
        #   - Trích xuất: Tên thương mại (brand_name), giá niêm yết (box_price_vnd),
        #     tình trạng kê đơn (is_prescription_rx) và đường link mua hàng trực tuyến.
        # ---------------------------------------------------------------------
        if neo4j_service.is_connected():
            cypher_prod = """
            MATCH (dr:Drug)-[:DISPENSED_AS_PRODUCT]->(p:PharmacyProduct)
            WHERE toLower(dr.name) CONTAINS toLower($name) 
               OR toLower(dr.id) CONTAINS toLower($name)
               OR toLower(p.brand_name) CONTAINS toLower($name)
            RETURN p.id AS id, p.brand_name AS brand_name, p.active_ingredient AS active_ingredient,
                   p.box_price_vnd AS box_price_vnd, p.unit_price_vnd AS unit_price_vnd,
                   p.is_prescription_rx AS is_prescription_rx, p.longchau_url AS longchau_url,
                   p.drug_class AS drug_class, p.indication AS indication
            LIMIT 2
            """
            prods_primary = neo4j_service.execute_cypher(cypher_prod, {"name": primary_name.split()[0]})

        if not prods_primary:
            prods_primary = self.crawler.search_local(primary_name, limit=2)
        if not prods_primary:
            if "metformin" in primary_name.lower():
                prods_primary = self.crawler.search_local("Glucophage", limit=2)
            elif "sitagliptin" in primary_name.lower() or "dpp" in primary_name.lower():
                prods_primary = self.crawler.search_local("Januvia", limit=1)

        for p in prods_primary[:1]:
            daily_dose = 2.0 if "metformin" in p.get("active_ingredient", "").lower() else 1.0
            cost_info = self.crawler.estimate_monthly_cost(p["id"], daily_dose_units=daily_dose)
            item = PharmacyItem(
                product_id=p["id"],
                brand_name=p["brand_name"],
                active_ingredient=p["active_ingredient"],
                drug_class=p.get("drug_class", "Thuốc điều trị đái tháo đường"),
                unit_price_vnd=p.get("unit_price_vnd", 0),
                box_price_vnd=p.get("box_price_vnd", 0),
                is_prescription_rx=p.get("is_prescription_rx", True),
                indication=p.get("indication", ""),
                longchau_url=p.get("longchau_url", ""),
                monthly_cost_vnd=cost_info.get("monthly_cost_vnd", 0)
            )
            matched_items.append(item)
            total_monthly_cost += item.monthly_cost_vnd

        # Thuốc phối hợp nếu có
        if rx.add_on_drug:
            prods_addon = self.crawler.search_local(rx.add_on_drug, limit=1)
            for p in prods_addon:
                cost_info = self.crawler.estimate_monthly_cost(p["id"], daily_dose_units=1.0)
                item = PharmacyItem(
                    product_id=p["id"],
                    brand_name=p["brand_name"],
                    active_ingredient=p["active_ingredient"],
                    drug_class=p.get("drug_class", "Thuốc phối hợp hạ đường huyết"),
                    unit_price_vnd=p.get("unit_price_vnd", 0),
                    box_price_vnd=p.get("box_price_vnd", 0),
                    is_prescription_rx=p.get("is_prescription_rx", True),
                    indication=p.get("indication", ""),
                    longchau_url=p.get("longchau_url", ""),
                    monthly_cost_vnd=cost_info.get("monthly_cost_vnd", 0)
                )
                matched_items.append(item)
                total_monthly_cost += item.monthly_cost_vnd

        # Kèm thêm que thử theo dõi
        meter_prods = self.crawler.search_local("Accu-Chek Instant", limit=1)
        for p in meter_prods:
            item = PharmacyItem(
                product_id=p["id"],
                brand_name=p["brand_name"],
                active_ingredient=p["active_ingredient"],
                drug_class="Vật tư y tế theo dõi",
                unit_price_vnd=p.get("unit_price_vnd", 0),
                box_price_vnd=p.get("box_price_vnd", 0),
                is_prescription_rx=False,
                indication="Que thử theo dõi đường huyết tại nhà",
                longchau_url=p.get("longchau_url", ""),
                monthly_cost_vnd=0
            )
            matched_items.append(item)

        state.pharmacy_items = matched_items
        state.total_monthly_pharmacy_cost_vnd = total_monthly_cost
        state.agent_execution_logs.append({
            "agent": "PharmacyLocatorAgent",
            "status": "PRESCRIPTION_SUCCESS",
            "message": f"Ánh xạ {len(matched_items)} sản phẩm Long Châu | Ước tính thuốc: {total_monthly_cost:,} VNĐ/tháng"
        })

        return state
