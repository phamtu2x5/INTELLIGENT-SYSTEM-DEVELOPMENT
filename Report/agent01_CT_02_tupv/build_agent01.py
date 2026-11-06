import subprocess
import os
import sys

def build_pdf():
    tex_path = "Report/agent01_CT_02_tupv/agent01_CT_02_tupv.tex"
    work_dir = "Report/agent01_CT_02_tupv"
    
    print(f"--- Bắt đầu biên dịch XeLaTeX cho Agent 01 ---")
    cmd = ["xelatex", "-interaction=nonstopmode", "agent01_CT_02_tupv.tex"]
    
    # Pass 1
    res1 = subprocess.run(cmd, cwd=work_dir, capture_output=True, text=True)
    if res1.returncode != 0:
        print("LỖI Pass 1:")
        print(res1.stdout[-1500:])
        return False
    print("✓ Pass 1 hoàn tất.")

    # Pass 2
    res2 = subprocess.run(cmd, cwd=work_dir, capture_output=True, text=True)
    if res2.returncode != 0:
        print("LỖI Pass 2:")
        print(res2.stdout[-1500:])
        return False
    print("✓ Pass 2 hoàn tất.")

    # Check page count
    pdf_path = "Report/agent01_CT_02_tupv/agent01_CT_02_tupv.pdf"
    info = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True)
    for line in info.stdout.splitlines():
        if "Pages:" in line or "File size:" in line:
            print(f"  {line}")

    # Clean aux
    for ext in [".aux", ".log", ".out"]:
        f_clean = os.path.join(work_dir, f"agent01_CT_02_tupv{ext}")
        if os.path.exists(f_clean):
            os.remove(f_clean)
            
    print(f"✓ Xuất bản thành công: {pdf_path}")
    return True

if __name__ == "__main__":
    build_pdf()
