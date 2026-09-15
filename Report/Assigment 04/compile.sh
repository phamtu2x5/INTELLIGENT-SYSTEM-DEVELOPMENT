#!/bin/bash
# Compile LaTeX report with XeLaTeX and clean up all auxiliary/log files
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=== [1/2] Pass 1: Generating aux and references ==="
/Library/TeX/texbin/xelatex -interaction=nonstopmode A04_CT_tupv.879.tex > /dev/null 2>&1 || true

echo "=== [2/2] Pass 2: Finalizing TOC, LOT, LOF, and references ==="
/Library/TeX/texbin/xelatex -interaction=nonstopmode A04_CT_tupv.879.tex > /dev/null 2>&1

echo "=== Cleaning up logs and auxiliary files ==="
rm -f A04_CT_tupv.879.log A04_CT_tupv.879.aux A04_CT_tupv.879.toc A04_CT_tupv.879.lof A04_CT_tupv.879.lot A04_CT_tupv.879.out

echo "=== Compilation finished successfully! Output: A04_CT_tupv.879.pdf ==="
