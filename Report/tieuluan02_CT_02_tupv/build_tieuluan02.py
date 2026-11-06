# -*- coding: utf-8 -*-
"""
Script: build_tieuluan02.py
Mục đích: Biên dịch tài liệu LaTeX báo cáo Tiểu luận 02 thành PDF bằng XeLaTeX
Tác giả: Phạm Văn Tư - B23DCCN879
"""

import os
import subprocess

def compile_pdf():
    rep_dir = os.path.dirname(os.path.abspath(__file__))
    base_name = "tieuluan02_CT_02_tupv"
    tex_path = os.path.join(rep_dir, f"{base_name}.tex")
    
    if not os.path.exists(tex_path):
        print(f"Lỗi: Không tìm thấy file {tex_path}")
        return False
        
    print(f"--- Bắt đầu biên dịch XeLaTeX (Pass 1) cho {base_name}.tex ---")
    cmd = ["xelatex", "-interaction=nonstopmode", f"{base_name}.tex"]
    res1 = subprocess.run(cmd, cwd=rep_dir, capture_output=True, text=True)
    if res1.returncode != 0:
        print("Lỗi biên dịch Pass 1:")
        print(res1.stdout[-2500:])
        return False
        
    print("--- Bắt đầu biên dịch XeLaTeX (Pass 2 cập nhật Mục lục & Hình) ---")
    res2 = subprocess.run(cmd, cwd=rep_dir, capture_output=True, text=True)
    if res2.returncode != 0:
        print("Lỗi biên dịch Pass 2:")
        print(res2.stdout[-2500:])
        return False

    print("\n--- Dọn dẹp các tệp phụ trợ (.aux, .log, .toc, .lof, .lot, .out) ---")
    aux_extensions = [".aux", ".log", ".out", ".toc", ".lof", ".lot", ".fls", ".fdb_latexmk", ".synctex.gz"]
    for ext in aux_extensions:
        aux_file = os.path.join(rep_dir, f"{base_name}{ext}")
        if os.path.exists(aux_file):
            os.remove(aux_file)
            print(f"  Đã xóa: {os.path.basename(aux_file)}")
            
    pdf_path = os.path.join(rep_dir, f"{base_name}.pdf")
    if os.path.exists(pdf_path):
        size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
        print(f"✓ Xuất bản thành công báo cáo PDF: {pdf_path} ({size_mb:.2f} MB)")
        return True
    return False

if __name__ == '__main__':
    compile_pdf()
