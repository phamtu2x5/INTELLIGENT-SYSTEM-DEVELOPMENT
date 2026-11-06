# build_tieuluan01.py
import os
import sys
import subprocess
import shutil

# Ensure current dir is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from sections.preamble import get_preamble
from sections.cover_and_toc import get_cover_and_toc
from sections.chapter1_history import get_chapter1
from sections.chapter2_ml import get_chapter2
from sections.chapter3_cnn import get_chapter3
from sections.chapter4_rnn import get_chapter4
from sections.references import get_references

def generate_tex():
    tex_path = os.path.join(BASE_DIR, 'tieuluan01_CT_02_tupv.tex')
    
    parts = [
        get_preamble(),
        get_cover_and_toc(),
        get_chapter1(),
        get_chapter2(),
        get_chapter3(),
        get_chapter4(),
        get_references()
    ]
    
    full_content = "\n".join(parts)
    
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
        
    print(f"✓ Đã ghép và xuất bản file LaTeX: {tex_path}")
    print(f"  Tổng số dòng: {len(full_content.splitlines())}")
    return tex_path

def compile_pdf(tex_path):
    base_name = os.path.splitext(os.path.basename(tex_path))[0]
    
    print("\n--- Bắt đầu biên dịch XeLaTeX (Pass 1) ---")
    cmd = ["xelatex", "-interaction=nonstopmode", f"{base_name}.tex"]
    res1 = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
    if res1.returncode != 0:
        print("Lỗi biên dịch Pass 1:")
        print(res1.stdout[-2500:])
        return False
    print("✓ Hoàn thành Pass 1")
    
    print("\n--- Bắt đầu biên dịch XeLaTeX (Pass 2 cập nhật Mục lục, Danh mục hình, Bảng, Mã nguồn) ---")
    res2 = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
    if res2.returncode != 0:
        print("Lỗi biên dịch Pass 2:")
        print(res2.stdout[-2500:])
        return False
    print("✓ Hoàn thành Pass 2")

    print("\n--- Dọn dẹp các tệp phụ trợ (.aux, .log, .toc, .lof, .lot, .out, .lol) ---")
    aux_extensions = [".aux", ".log", ".out", ".toc", ".lof", ".lot", ".lol", ".fls", ".fdb_latexmk", ".synctex.gz"]
    for ext in aux_extensions:
        aux_file = os.path.join(BASE_DIR, f"{base_name}{ext}")
        if os.path.exists(aux_file):
            os.remove(aux_file)
            print(f"  Đã xóa: {os.path.basename(aux_file)}")
            
    pdf_path = os.path.join(BASE_DIR, f"{base_name}.pdf")
    print(f"\n✓ Xuất bản thành công báo cáo PDF: {pdf_path}")
    
    return True

if __name__ == '__main__':
    tex_file = generate_tex()
    compile_pdf(tex_file)
