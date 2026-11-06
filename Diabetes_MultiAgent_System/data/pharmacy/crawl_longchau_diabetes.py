#!/usr/bin/env python3
"""
crawl_longchau_diabetes.py
===========================
Công cụ thu thập và chuẩn hóa dữ liệu dược phẩm, thiết bị y tế đái tháo đường
từ hệ thống Nhà thuốc FPT Long Châu (nhathuoclongchau.com.vn).

Dữ liệu đầu ra:
- File JSON: data/pharmacy/longchau_diabetes_products.json
- Tích hợp trực tiếp vào PharmacyLocatorAgent & Knowledge Graph.
"""

import json
import os
import re
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional

LONGCHAU_BASE_URL = "https://nhathuoclongchau.com.vn"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}

# Danh mục các hoạt chất và thương hiệu thuốc đái tháo đường chủ lực theo QĐ 5481/QĐ-BYT
KEY_DIABETES_QUERIES = [
    # Nhóm Biguanide
    {"query": "Glucophage", "drug_class": "Biguanide", "ingredient": "Metformin"},
    {"query": "Metformin", "drug_class": "Biguanide", "ingredient": "Metformin"},
    # Nhóm Sulfonylurea
    {"query": "Diamicron", "drug_class": "Sulfonylurea", "ingredient": "Gliclazide"},
    {"query": "Amaryl", "drug_class": "Sulfonylurea", "ingredient": "Glimepiride"},
    # Nhóm Ức chế SGLT-2
    {"query": "Forxiga", "drug_class": "SGLT2 inhibitor", "ingredient": "Dapagliflozin"},
    {"query": "Jardiance", "drug_class": "SGLT2 inhibitor", "ingredient": "Empagliflozin"},
    # Nhóm Ức chế DPP-4
    {"query": "Januvia", "drug_class": "DPP-4 inhibitor", "ingredient": "Sitagliptin"},
    {"query": "Galvus", "drug_class": "DPP-4 inhibitor", "ingredient": "Vildagliptin"},
    {"query": "Trajenta", "drug_class": "DPP-4 inhibitor", "ingredient": "Linagliptin"},
    # Insulin & Bút tiêm
    {"query": "Lantus Solostar", "drug_class": "Insulin Analogue (Nền)", "ingredient": "Insulin Glargine"},
    {"query": "Novomix", "drug_class": "Insulin Premix", "ingredient": "Insulin Aspart"},
    # Thiết bị và Dinh dưỡng đặc trị
    {"query": "Accu-Chek", "drug_class": "Thiết bị & Que thử", "ingredient": "Máy/Que đo đường huyết"},
    {"query": "Glucerna", "drug_class": "Dinh dưỡng y học", "ingredient": "Sữa dinh dưỡng đặc trị"},
]

DEFAULT_CATALOG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "longchau_diabetes_products.json"
)


class LongChauDiabetesCrawler:
    """
    Crawler thu thập dữ liệu sản phẩm thuốc & thiết bị đái tháo đường từ Long Châu.
    Hỗ trợ chế độ trực tuyến (Online Scraping) và bộ đệm ngoại tuyến (Offline Master Catalog).
    """

    def __init__(self, catalog_path: str = DEFAULT_CATALOG_PATH):
        self.catalog_path = catalog_path
        self.products: List[Dict[str, Any]] = []
        self._load_local_catalog()

    def _load_local_catalog(self):
        """Nạp danh mục offline nếu đã tồn tại."""
        if os.path.exists(self.catalog_path):
            try:
                with open(self.catalog_path, "r", encoding="utf-8") as f:
                    self.products = json.load(f)
                print(f"[LongChauCrawler] Đã nạp {len(self.products)} sản phẩm từ {self.catalog_path}")
            except Exception as e:
                print(f"[LongChauCrawler] Lỗi đọc file catalog cục bộ: {e}")
                self.products = []

    def save_catalog(self, output_path: Optional[str] = None):
        """Lưu danh mục sản phẩm vào file JSON."""
        target_path = output_path or self.catalog_path
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)
        print(f"[LongChauCrawler] Đã lưu thành công {len(self.products)} sản phẩm vào: {target_path}")

    def fetch_product_page(self, product_url: str) -> Optional[Dict[str, Any]]:
        """
        Thu thập thông tin chi tiết của một sản phẩm từ đường dẫn Long Châu.
        """
        try:
            resp = requests.get(product_url, headers=HEADERS, timeout=12)
            if resp.status_code != 200:
                print(f"[Crawl Warning] Mã phản hồi {resp.status_code} cho URL: {product_url}")
                return None

            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.find("h1") or soup.find("title")
            title_text = title.get_text(strip=True) if title else ""

            # Trích xuất dữ liệu giá
            price_box = soup.find("div", class_=lambda c: c and "price" in c.lower())
            price_text = price_box.get_text(strip=True) if price_box else ""

            return {
                "title": title_text,
                "price_raw": price_text,
                "url": product_url,
                "status": "active"
            }
        except Exception as e:
            print(f"[Crawl Error] Lỗi khi tải URL {product_url}: {e}")
            return None

    def search_local(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Tìm kiếm nhanh các loại thuốc/sản phẩm tiểu đường trong catalog theo:
        - Tên thương mại (brand_name)
        - Hoạt chất chính (active_ingredient)
        - Phân nhóm dược lý (drug_class)
        """
        q = query.lower().strip()
        matched = []
        for prod in self.products:
            score = 0
            if q in prod.get("brand_name", "").lower():
                score += 3
            if q in prod.get("active_ingredient", "").lower():
                score += 3
            if q in prod.get("drug_class", "").lower():
                score += 1
            if q in prod.get("indication", "").lower():
                score += 1
            if score > 0:
                matched.append((score, prod))

        matched.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in matched[:limit]]

    def estimate_monthly_cost(self, product_id: str, daily_dose_units: float = 1.0) -> Dict[str, Any]:
        """
        Tính toán chi phí tài chính dự kiến theo tháng (30 ngày) cho bệnh nhân.
        """
        target = next((p for p in self.products if p.get("id") == product_id), None)
        if not target:
            return {"error": f"Không tìm thấy sản phẩm có ID: {product_id}"}

        unit_price = target.get("unit_price_vnd", 0)
        daily_cost = unit_price * daily_dose_units
        monthly_cost = daily_cost * 30

        return {
            "product_id": product_id,
            "brand_name": target.get("brand_name"),
            "unit_price_vnd": unit_price,
            "daily_dose_units": daily_dose_units,
            "daily_cost_vnd": int(daily_cost),
            "monthly_cost_vnd": int(monthly_cost),
            "is_prescription_rx": target.get("is_prescription_rx", True),
            "longchau_url": target.get("longchau_url")
        }


if __name__ == "__main__":
    crawler = LongChauDiabetesCrawler()
    print("\n--- TEST TÌM KIẾM THUỐC LONG CHÂU CHO TIỂU ĐƯỜNG ---")
    
    # 1. Tìm kiếm Metformin
    results_metformin = crawler.search_local("Metformin")
    print(f"\n1. Kết quả tìm kiếm 'Metformin' ({len(results_metformin)} sản phẩm):")
    for p in results_metformin:
        print(f" - [{p['id']}] {p['brand_name']} | Giá viên: {p['unit_price_vnd']:,}đ | Hộp: {p['box_price_vnd']:,}đ | Rx: {p['is_prescription_rx']}")

    # 2. Tìm kiếm nhóm bảo vệ thận / suy tim SGLT-2
    results_sglt2 = crawler.search_local("SGLT2")
    print(f"\n2. Kết quả tìm kiếm 'SGLT2' ({len(results_sglt2)} sản phẩm):")
    for p in results_sglt2:
        print(f" - [{p['id']}] {p['brand_name']} ({p['active_ingredient']}) | Giá hộp: {p['box_price_vnd']:,}đ")

    # 3. Dự toán chi phí điều trị hàng tháng
    cost_calc = crawler.estimate_monthly_cost("lc_dia_01", daily_dose_units=2.0) # Glucophage XR 500mg x 2 viên/ngày
    print(f"\n3. Dự toán chi phí điều trị hàng tháng (Glucophage XR 500mg x 2 viên/ngày):")
    print(f" - Chi phí/ngày: {cost_calc['daily_cost_vnd']:,} VNĐ")
    print(f" - Chi phí/tháng (30 ngày): {cost_calc['monthly_cost_vnd']:,} VNĐ")
    print(f" - Bắt buộc kê đơn (Rx): {'CÓ' if cost_calc['is_prescription_rx'] else 'KHÔNG'}")
    print(f" - Mua tại Long Châu: {cost_calc['longchau_url']}")
