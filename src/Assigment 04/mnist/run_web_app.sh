#!/bin/bash
# Script khởi chạy Web App Nhận diện chữ số viết tay MNIST
cd "$(dirname "$0")/web_app" || exit
python3 app.py --port 5050
