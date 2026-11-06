import subprocess
import os
import sys
from pathlib import Path

def clean_temp_files(work_dir: Path, base_name: str):
    """Xóa bỏ sạch sẽ toàn bộ các file log và file phụ trợ sinh ra sau khi biên dịch."""
    extensions = [".log", ".aux", ".out", ".toc", ".synctex.gz", ".fls", ".fdb_latexmk"]
    cleaned = []
    for ext in extensions:
        f = work_dir / f"{base_name}{ext}"
        if f.exists():
            f.unlink()
            cleaned.append(f.name)
    if cleaned:
        print(f"✓ Đã tự động dọn dẹp các file log và phụ trợ: {', '.join(cleaned)}")

def build_pdf():
    work_dir = Path(__file__).resolve().parent
    base_name = "agent02_CT_02_tupv"
    tex_file = f"{base_name}.tex"
    pdf_file = f"{base_name}.pdf"
    
    print(f"--- Bắt đầu biên dịch XeLaTeX cho Agent 02 ({tex_file}) ---")
    cmd = ["xelatex", "-interaction=nonstopmode", tex_file]
    
    # Pass 1
    res1 = subprocess.run(cmd, cwd=str(work_dir), capture_output=True, text=True)
    if res1.returncode != 0:
        print("LỖI Pass 1:")
        print(res1.stdout[-1500:])
        clean_temp_files(work_dir, base_name)
        return False
    print("✓ Pass 1 hoàn tất.")

    # Pass 2 (resolve references, TOC, citations)
    res2 = subprocess.run(cmd, cwd=str(work_dir), capture_output=True, text=True)
    if res2.returncode != 0:
        print("LỖI Pass 2:")
        print(res2.stdout[-1500:])
        clean_temp_files(work_dir, base_name)
        return False
    print("✓ Pass 2 hoàn tất.")

    # Tự động xóa file log và file trung gian
    clean_temp_files(work_dir, base_name)

    # Page count analysis
    pdf_path = work_dir / pdf_file
    if pdf_path.exists():
        import pypdf
        reader = pypdf.PdfReader(str(pdf_path))
        print(f"\n==========================================")
        print(f"THỐNG KÊ XUẤT BẢN FILE PDF THÀNH CÔNG:")
        print(f"  Tên file : {pdf_file}")
        print(f"  Đường dẫn: {pdf_path}")
        print(f"  Số trang : {len(reader.pages)} trang")
        print(f"  Dung lượng: {pdf_path.stat().st_size / 1024 / 1024:.2f} MB")
        print(f"==========================================")
        for i, page in enumerate(reader.pages):
            lines = [l.strip() for l in page.extract_text().splitlines() if l.strip()]
            first = lines[0] if lines else "EMPTY"
            last = lines[-1] if lines else "EMPTY"
            print(f"  Trang {i+1:2d} ({len(lines):2d} dòng): {first[:35]} ... {last[:35]}")
    else:
        print("Không tìm thấy file PDF đầu ra.")
        return False

    return True

if __name__ == "__main__":
    build_pdf()
