#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_project01.py
==================
Biên dịch báo cáo Project 01 (DiaAgent-MAS) sang định dạng PDF chuẩn bằng XeLaTeX.
Tự động dọn dẹp toàn bộ tệp nhật ký (.log) và tệp trung gian (.aux, .toc, .out, ...)
tuân thủ tuyệt đối yêu cầu của người dùng.
"""

import os
import sys
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from generate_report import generate_tex_file

def build_pdf():
    print("==================================================================")
    print(" BẮT ĐẦU QUY TRÌNH XUẤT BẢN BÁO CÁO PROJECT 01 (DIAAGENT-MAS)")
    print("==================================================================")
    
    # Bước 1: Khởi tạo/Cập nhật mã nguồn LaTeX
    tex_path = generate_tex_file()
    base_name = "project01_CT_02_tupv"
    
    # Bước 2: Pass 1 XeLaTeX
    print("\n--- [Bước 1/3] Biên dịch XeLaTeX Pass 1 ---")
    cmd = ["xelatex", "-interaction=nonstopmode", f"{base_name}.tex"]
    res1 = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
    if res1.returncode != 0:
        print("✗ LỖI BIÊN DỊCH PASS 1:")
        print(res1.stdout[-2500:])
        return False
    print("✓ Pass 1 hoàn tất thành công.")
    
    # Bước 3: Pass 2 XeLaTeX (Cập nhật Mục lục, Danh mục hình ảnh, Bảng biểu)
    print("\n--- [Bước 2/3] Biên dịch XeLaTeX Pass 2 (Hoàn thiện Tham chiếu & Mục lục) ---")
    res2 = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
    if res2.returncode != 0:
        print("✗ LỖI BIÊN DỊCH PASS 2:")
        print(res2.stdout[-2500:])
        return False
    print("✓ Pass 2 hoàn tất thành công.")
    
    # Bước 4: Dọn dẹp triệt để toàn bộ log và tệp trung gian
    print("\n--- [Bước 3/3] Dọn dẹp triệt để tệp nhật ký (.log) và tệp phụ trợ ---")
    aux_extensions = [
        ".aux", ".log", ".out", ".toc", ".lof", ".lot", 
        ".lol", ".fls", ".fdb_latexmk", ".synctex.gz"
    ]
    cleaned_count = 0
    for ext in aux_extensions:
        aux_file = os.path.join(BASE_DIR, f"{base_name}{ext}")
        if os.path.exists(aux_file):
            try:
                os.remove(aux_file)
                print(f"  ✓ Đã xóa: {os.path.basename(aux_file)}")
                cleaned_count += 1
            except Exception as e:
                print(f"  ! Không thể xóa {aux_file}: {e}")
                
    pdf_path = os.path.join(BASE_DIR, f"{base_name}.pdf")
    if os.path.exists(pdf_path):
        size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
        print("==================================================================")
        print(f"✓ XUẤT BẢN THÀNH CÔNG: {pdf_path}")
        print(f"  Dung lượng tệp PDF: {size_mb:.2f} MB")
        
        # Kiểm tra thông tin trang qua pdfinfo
        try:
            info = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True)
            for line in info.stdout.splitlines():
                if "Pages:" in line or "Page size:" in line:
                    print(f"  {line}")
        except Exception:
            pass
        print("==================================================================")
        return True
    else:
        print("✗ Không tìm thấy tệp PDF xuất bản!")
        return False

if __name__ == "__main__":
    success = build_pdf()
    sys.exit(0 if success else 1)
