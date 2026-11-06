import os
import time
import argparse
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
import torch

from model import get_stock_model, get_customer_model

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STOCK_DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'stock_market', 'amazon_stock_price.csv')
CUST_DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'customer_behavior', 'customer_sequential_behavior.csv')

# Load and cache datasets
print("Đang nạp dữ liệu vào bộ nhớ Web App...")
df_stock = pd.read_csv(STOCK_DATA_PATH)
df_cust = pd.read_csv(CUST_DATA_PATH)
print("Dữ liệu đã sẵn sàng.")

# Scaler constants for Amazon Close price
CLOSE_MIN = float(df_stock['Close'].min())
CLOSE_MAX = float(df_stock['Close'].max())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stock/history', methods=['GET'])
def get_stock_history():
    # Trả về 100 phiên giao dịch gần nhất
    recent = df_stock.tail(100).copy()
    result = {
        'dates': recent['Date'].tolist(),
        'close': [round(x, 2) for x in recent['Close'].tolist()],
        'open': [round(x, 2) for x in recent['Open'].tolist()],
        'high': [round(x, 2) for x in recent['High'].tolist()],
        'low': [round(x, 2) for x in recent['Low'].tolist()],
        'volume': recent['Volume'].tolist(),
        'ma20': [round(x, 2) for x in recent['MA20'].tolist()],
        'rsi': [round(x, 1) for x in recent['RSI_14'].tolist()]
    }
    return jsonify(result)

@app.route('/api/stock/predict', methods=['POST'])
def predict_stock():
    t_start = time.perf_counter()
    req = request.get_json(silent=True) or {}
    model_name = req.get('model', 'lstm').lower()
    
    # Lấy 30 phiên cuối cùng làm cửa sổ trượt đầu vào
    lookback = 30
    feature_cols = ['Close', 'Open', 'High', 'Low', 'Volume', 'Return', 'MA20', 'RSI_14']
    recent_features = df_stock[feature_cols].tail(lookback).values.copy()
    
    # Chuẩn hoá min-max theo phạm vi dữ liệu
    min_vals = df_stock[feature_cols].min().values
    max_vals = df_stock[feature_cols].max().values
    norm_features = (recent_features - min_vals) / (max_vals - min_vals + 1e-8)
    
    tensor_in = torch.from_numpy(norm_features[np.newaxis, :, :]).float()
    
    model = get_stock_model(model_name)
    with torch.no_grad():
        norm_pred = model(tensor_in).item()
        
    pred_price = round(norm_pred * (CLOSE_MAX - CLOSE_MIN) + CLOSE_MIN, 2)
    last_actual_price = round(float(df_stock['Close'].iloc[-1]), 2)
    diff = round(pred_price - last_actual_price, 2)
    pct_change = round((diff / last_actual_price) * 100.0, 2)
    direction = 'TĂNG' if diff >= 0 else 'GIẢM'
    
    latency = round((time.perf_counter() - t_start) * 1000.0, 2)
    
    return jsonify({
        'success': True,
        'model': model_name.upper(),
        'last_actual_price': last_actual_price,
        'predicted_price': pred_price,
        'difference': diff,
        'percent_change': pct_change,
        'direction': direction,
        'latency_ms': latency
    })

@app.route('/api/customer/predict', methods=['POST'])
def predict_customer():
    t_start = time.perf_counter()
    req = request.get_json(silent=True) or {}
    model_name = req.get('model', 'lstm').lower()
    preset = req.get('preset', 'churn')
    
    # Chọn mẫu khách hàng theo kịch bản
    if preset == 'loyal':
        c_id = df_cust[df_cust['ChurnNextPeriod'] == 0]['CustomerID'].iloc[0]
    elif preset == 'churn':
        c_id = df_cust[df_cust['ChurnNextPeriod'] == 1]['CustomerID'].iloc[0]
    else:
        c_id = int(req.get('customer_id', 1))
        
    sub = df_cust[df_cust['CustomerID'] == c_id].sort_values('Month')
    feat_cols = ['Sessions', 'PageViews', 'CartAdds', 'Purchases', 'AvgDurationMin', 'Complaints', 'SpentUSD', 'DiscountRatio']
    raw_vals = sub[feat_cols].values
    
    # Chuẩn hoá standard
    mean_vals = df_cust[feat_cols].mean().values
    std_vals = df_cust[feat_cols].std().values
    norm_vals = (raw_vals - mean_vals) / (std_vals + 1e-8)
    
    tensor_in = torch.from_numpy(norm_vals[np.newaxis, :, :]).float()
    
    model = get_customer_model(model_name)
    with torch.no_grad():
        logits = model(tensor_in)
        probs = torch.softmax(logits, dim=1)[0].numpy()
        
    churn_prob = round(float(probs[1]) * 100.0, 1)
    stay_prob = round(float(probs[0]) * 100.0, 1)
    
    if churn_prob >= 65.0:
        risk_level = 'CAO'
        risk_color = '#ef4444'
        action = 'Cần gửi voucher kích cầu và liên hệ trực tiếp hỗ trợ giải quyết khiếu nại ngay.'
    elif churn_prob >= 35.0:
        risk_level = 'TRUNG BÌNH'
        risk_color = '#f59e0b'
        action = 'Gửi email cá nhân hóa và nhắc nhở các sản phẩm còn lưu trong giỏ hàng.'
    else:
        risk_level = 'THẤP'
        risk_color = '#10b981'
        action = 'Khách hàng có mức độ tương tác tốt, duy trì chương trình chăm sóc khách hàng thân thiết.'
        
    latency = round((time.perf_counter() - t_start) * 1000.0, 2)
    
    return jsonify({
        'success': True,
        'customer_id': int(c_id),
        'churn_probability': churn_prob,
        'stay_probability': stay_prob,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'recommendation': action,
        'months': sub['Month'].tolist(),
        'sessions': sub['Sessions'].tolist(),
        'spent': sub['SpentUSD'].tolist(),
        'complaints': sub['Complaints'].tolist(),
        'latency_ms': latency
    })

def main():
    parser = argparse.ArgumentParser(description="RNN Time Series & Sequence Web App")
    parser.add_argument('--port', type=int, default=8080, help="Port (mặc định: 8080)")
    parser.add_argument('--host', type=str, default='127.0.0.1', help="Host (mặc định: 127.0.0.1)")
    args = parser.parse_args()

    print("\n" + "=" * 65)
    print(f"🚀 Assignment 06 RNN Web App đang khởi chạy!")
    print(f"👉 Mở trình duyệt tại: http://{args.host}:{args.port}")
    print("=" * 65 + "\n")

    app.run(host=args.host, port=args.port, debug=False)

if __name__ == '__main__':
    main()
