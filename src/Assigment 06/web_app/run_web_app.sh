#!/bin/bash
# Script khởi chạy Web App Dự Báo Chuỗi Thời Gian & Hành Vi Khách Hàng (Assignment 06)
cd "$(dirname "$0")" || exit
python3 app.py --port 8080
