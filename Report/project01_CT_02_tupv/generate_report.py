#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_report.py
==================
Tự động tạo tệp mã nguồn LaTeX project01_CT_02_tupv.tex
Báo cáo Dự án Hệ thống Thông minh: Hệ Multi-Agent DiaAgent-MAS.
Tuyệt đối tuân thủ quy tắc:
- KHÔNG sử dụng từ "tác tử", sử dụng "Agent", "Multi-Agent"
- Định dạng chuẩn PTIT, Times New Roman, XeLaTeX
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from sections.intro import get_intro
from sections.theory import get_theory
from sections.architecture import get_architecture
from sections.experiments import get_experiments
from sections.conclusion import get_conclusion
from sections.references import get_references

def get_preamble():
    return r"""\documentclass[12pt,a4paper]{article}

% =========================================================================
% GÓI THƯ VIỆN & CẤU HÌNH CƠ BẢN (XELATEX COMPATIBLE)
% =========================================================================
\usepackage{fontspec}
\setmainfont{Times New Roman}

\usepackage[top=2.2cm, bottom=2.2cm, left=2.5cm, right=2.0cm]{geometry}
\usepackage{amsmath, amsfonts, amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{float}
\usepackage{xcolor}
\usepackage{colortbl}
\usepackage{tikz}
\usetikzlibrary{calc, shapes.geometric, arrows.meta, positioning}
\usepackage{hyperref}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{enumitem}
\usepackage{listings}
\usepackage{setspace}
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\usepackage{microtype}

% Dãn dòng chuẩn học thuật PTIT
\setstretch{1.2}

% Định nghĩa màu sắc thương hiệu báo cáo
\definecolor{ptitblue}{RGB}{0, 51, 153}
\definecolor{darkblue}{RGB}{10, 40, 100}
\definecolor{lightgray}{RGB}{245, 247, 250}
\definecolor{codebg}{RGB}{248, 250, 252}
\definecolor{warnbg}{RGB}{254, 243, 199}
\definecolor{warnframe}{RGB}{217, 119, 6}

% Cấu hình Tiếng Việt cho Caption
\renewcommand{\figurename}{Hình}
\renewcommand{\tablename}{Bảng}
\captionsetup[figure]{name=Hình, labelfont={bf,color=blue!70!black}, font=small, skip=4pt}
\captionsetup[table]{name=Bảng, labelfont={bf,color=blue!70!black}, font=small, skip=4pt}

% Cấu hình Hyperref
\hypersetup{
    colorlinks=true,
    linkcolor=blue!80!black,
    citecolor=green!60!black,
    urlcolor=blue!70!black,
    pdftitle={Báo cáo Dự án 01: Hệ Multi-Agent Thông Minh Quản Lý Bệnh Đái Tháo Đường (DiaAgent-MAS)},
    pdfauthor={Phạm Văn Tư - B23DCCN879}
}

% Định dạng tiêu đề mục
\titleformat{\section}
  {\normalfont\Large\bfseries\color{blue!70!black}}
  {\thesection}{1em}{}
\titlespacing*{\section}{0pt}{10pt}{5pt}

\titleformat{\subsection}
  {\normalfont\large\bfseries\color{black!85}}
  {\thesubsection}{1em}{}
\titlespacing*{\subsection}{0pt}{7pt}{3pt}

\titleformat{\subsubsection}
  {\normalfont\normalsize\bfseries\color{black!75}}
  {\thesubsubsection}{1em}{}
\titlespacing*{\subsubsection}{0pt}{5pt}{2pt}

% Danh sách gọn gàng
\setlist[itemize]{leftmargin=1.5em, itemsep=2pt, topsep=2pt, parsep=0pt}
\setlist[enumerate]{leftmargin=1.5em, itemsep=2pt, topsep=2pt, parsep=0pt}

% Cấu hình listings cho mã Python
\lstdefinestyle{pythonstyle}{
    language=Python,
    backgroundcolor=\color{codebg},
    basicstyle=\ttfamily\footnotesize,
    keywordstyle=\color{blue!80!black}\bfseries,
    commentstyle=\color{gray}\itshape,
    stringstyle=\color{green!50!black},
    numbers=left,
    numberstyle=\tiny\color{gray},
    stepnumber=1,
    numbersep=8pt,
    frame=single,
    framerule=0.6pt,
    rulecolor=\color{gray!30},
    breaklines=true,
    breakatwhitespace=true,
    tabsize=4,
    showstringspaces=false
}

% Header & Footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\itshape Học viện Công nghệ Bưu chính Viễn thông}
\fancyhead[R]{\small\itshape Project 01: DiaAgent-MAS}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\setlength{\headheight}{14pt}

\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
"""

def get_cover_and_toc():
    return r"""
\begin{document}

% -------------------------------------------------------------------------
% TRANG BÌA CHUẨN HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG
% -------------------------------------------------------------------------
\begin{titlepage}
\begin{tikzpicture}[remember picture, overlay]
    \node[anchor=center] at (current page.center) {
        \includegraphics[width=\dimexpr\paperwidth-2.0cm\relax, height=\dimexpr\paperheight-2.0cm\relax]{images/ptit_cover_border.jpeg}
    };
\end{tikzpicture}

\begin{center}
    \vspace*{-0.2cm}
    {\fontsize{14.5pt}{19pt}\selectfont \textbf{HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG}}\\[0.3cm]
    {\fontsize{14.5pt}{19pt}\selectfont \textbf{KHOA CÔNG NGHỆ THÔNG TIN 1}}\\[0.3cm]
    {\fontsize{14.5pt}{19pt}\selectfont \textbf{HỌC PHẦN PHÁT TRIỂN CÁC HỆ THỐNG THÔNG MINH}}\\[1.0cm]
    
    % Logo PTIT
    \includegraphics[width=4.3cm]{images/ptit_logo.png}\\[1.0cm]
    
    {\fontsize{17pt}{22pt}\selectfont \textbf{BÁO CÁO DỰ ÁN HỆ THỐNG THÔNG MINH}}\\[0.3cm]
    {\fontsize{15pt}{20pt}\selectfont \textbf{(PROJECT 01)}}\\[0.5cm]
    {\fontsize{14pt}{19pt}\selectfont \textbf{NGHIÊN CỨU VÀ TRIỂN KHAI HỆ MULTI-AGENT THÔNG MINH}}\\[0.2cm]
    {\fontsize{13pt}{18pt}\selectfont \textbf{HỖ TRỢ SÀNG LỌC, CHẨN ĐOÁN VÀ QUẢN TRỊ BỆNH ĐÁI THÁO ĐƯỜNG}}\\[0.2cm]
    {\fontsize{13pt}{18pt}\selectfont \textbf{(DIAAGENT-MAS)}}\\[1.1cm]
\end{center}

\begin{flushleft}
    \hspace{2.8cm}
    \begin{tabular}{ll}
        \textbf{Lớp:} & D23CTPM01 \\[0.3cm]
        \textbf{Họ và tên sinh viên:} & Phạm Văn Tư \\[0.3cm]
        \textbf{Mã sinh viên:} & B23DCCN879 \\[0.3cm]
        \textbf{Giảng viên hướng dẫn:} & PGS.TS Trần Đình Quế \\[0.3cm]
        \textbf{Học kỳ:} & Học kỳ 1 năm học 2026 – 2027
    \end{tabular}
\end{flushleft}

\vfill
\begin{center}
    {\fontsize{12pt}{15pt}\selectfont \textbf{Hà Nội, 2026}}\\[0.4cm]
\end{center}
\end{titlepage}

\clearpage
\pagenumbering{roman}
\tableofcontents
\clearpage
\listoffigures
\listoftables
\clearpage

\pagenumbering{arabic}
"""

def generate_tex_file():
    tex_path = os.path.join(BASE_DIR, "project01_CT_02_tupv.tex")
    
    parts = [
        get_preamble(),
        get_cover_and_toc(),
        get_intro(),
        get_theory(),
        get_architecture(),
        get_experiments(),
        get_conclusion(),
        get_references()
    ]
    
    full_text = "\n".join(parts)
    
    # STRICT AUDIT: tuyệt đối không được có từ "tác tử"
    if "tác tử" in full_text.lower():
        raise ValueError("LỖI NGHIÊM TRỌNG: Phát hiện từ cấm 'tác tử' trong nội dung báo cáo!")
        
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(full_text)
        
    line_count = len(full_text.splitlines())
    print(f"✓ Đã tạo thành công tệp LaTeX: {tex_path}")
    print(f"  Tổng số dòng: {line_count}")
    print("  Kiểm tra từ cấm 'tác tử': ĐẠT (0 lần xuất hiện).")
    return tex_path

if __name__ == "__main__":
    generate_tex_file()
