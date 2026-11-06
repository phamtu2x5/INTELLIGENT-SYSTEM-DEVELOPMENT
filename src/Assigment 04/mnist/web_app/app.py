import os
import time
import argparse
from flask import Flask, render_template, request, jsonify
import torch
import numpy as np

from model import get_model
from preprocess import preprocess_canvas_image

app = Flask(__name__)

# Khởi tạo và nạp mô hình vào bộ nhớ khi máy chủ khởi động
print("Đang nạp mô hình PyTorch CNN (MNIST)...")
cnn_model = get_model()
print("Mô hình đã sẵn sàng phục vụ suy luận.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    t_start = time.perf_counter()
    data = request.get_json(force=True)
    if not data or 'image' not in data:
        return jsonify({'success': False, 'error': 'Dữ liệu yêu cầu không hợp lệ.'}), 400

    image_b64 = data.get('image')
    tensor, preview_b64, err = preprocess_canvas_image(image_b64)
    if err:
        return jsonify({'success': False, 'error': err}), 200

    # Chạy mô hình PyTorch suy luận
    with torch.no_grad():
        logits = cnn_model(tensor)
        probabilities = torch.softmax(logits, dim=1)[0].cpu().numpy().tolist()

    predicted_digit = int(np.argmax(probabilities))
    confidence = float(probabilities[predicted_digit])
    latency_ms = (time.perf_counter() - t_start) * 1000.0

    return jsonify({
        'success': True,
        'digit': predicted_digit,
        'confidence': confidence,
        'probabilities': [round(p, 4) for p in probabilities],
        'preprocessed_image': preview_b64,
        'latency_ms': round(latency_ms, 2)
    })

def main():
    parser = argparse.ArgumentParser(description="MNIST Handwritten Digit Recognition Web App")
    parser.add_argument('--port', type=int, default=5050, help="Cổng chạy server (mặc định: 5050)")
    parser.add_argument('--host', type=str, default='127.0.0.1', help="Host IP (mặc định: 127.0.0.1)")
    args = parser.parse_args()

    print("\n" + "=" * 65)
    print(f"🚀 MNIST Handwritten Digit Web App đang khởi chạy!")
    print(f"👉 Mở trình duyệt tại địa chỉ: http://{args.host}:{args.port}")
    print("=" * 65 + "\n")

    app.run(host=args.host, port=args.port, debug=False)

if __name__ == '__main__':
    main()
