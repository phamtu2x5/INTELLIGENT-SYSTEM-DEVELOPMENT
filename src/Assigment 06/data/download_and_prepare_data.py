import os
import numpy as np
import pandas as pd
import yfinance as yf

def prepare_datasets():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    stock_dir = os.path.join(base_dir, 'stock_market')
    cust_dir = os.path.join(base_dir, 'customer_behavior')
    os.makedirs(stock_dir, exist_ok=True)
    os.makedirs(cust_dir, exist_ok=True)

    print("=" * 65)
    print("1. TẢI VÀ CHUẨN BỊ DỮ LIỆU CỔ PHIẾU AMAZON (AMZN) 1997 - 2024")
    print("=" * 65)
    amzn_raw = yf.download('AMZN', start='1997-05-15', end='2024-12-31', progress=False)
    
    # Flatten MultiIndex columns nếu có
    if isinstance(amzn_raw.columns, pd.MultiIndex):
        amzn_raw.columns = [col[0] for col in amzn_raw.columns]
        
    df_amzn = amzn_raw.reset_index()
    df_amzn['Date'] = pd.to_datetime(df_amzn['Date'])
    df_amzn = df_amzn.sort_values('Date').reset_index(drop=True)
    
    # Thêm các chỉ báo kỹ thuật tài chính cơ bản
    df_amzn['Return'] = df_amzn['Close'].pct_change()
    df_amzn['MA20'] = df_amzn['Close'].rolling(window=20).mean()
    df_amzn['MA50'] = df_amzn['Close'].rolling(window=50).mean()
    df_amzn['Volatility_20'] = df_amzn['Return'].rolling(window=20).std()
    
    # Tính RSI 14 ngày
    delta = df_amzn['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-8)
    df_amzn['RSI_14'] = 100 - (100 / (1 + rs))
    
    df_amzn = df_amzn.dropna().reset_index(drop=True)
    amzn_file = os.path.join(stock_dir, 'amazon_stock_price.csv')
    df_amzn.to_csv(amzn_file, index=False)
    print(f"✓ Đã lưu dữ liệu cổ phiếu Amazon ({len(df_amzn):,} phiên giao dịch): {amzn_file}")
    print(df_amzn[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Return', 'RSI_14']].head(3))

    print("\n" + "=" * 65)
    print("2. TẢI VÀ CHUẨN BỊ DỮ LIỆU GIÁ VÀNG & BẠC (GOLD & SILVER)")
    print("=" * 65)
    gs_raw = yf.download(['GC=F', 'SI=F'], start='2000-08-30', end='2024-12-31', progress=False)
    df_gold = gs_raw['Close']['GC=F'].reset_index().rename(columns={'GC=F': 'Gold_Close'})
    df_silver = gs_raw['Close']['SI=F'].reset_index().rename(columns={'SI=F': 'Silver_Close'})
    df_metals = pd.merge(df_gold, df_silver, on='Date', how='inner').dropna().sort_values('Date').reset_index(drop=True)
    metals_file = os.path.join(stock_dir, 'gold_silver_prices.csv')
    df_metals.to_csv(metals_file, index=False)
    print(f"✓ Đã lưu dữ liệu kim loại quý ({len(df_metals):,} ngày): {metals_file}")

    print("\n" + "=" * 65)
    print("3. TỔNG HỢP BỘ DỮ LIỆU CHUỖI HÀNH VI KHÁCH HÀNG (CUSTOMER BEHAVIOR)")
    print("=" * 65)
    # Tạo dữ liệu chuỗi hành vi khách hàng qua 12 tháng liên tục
    np.random.seed(42)
    n_customers = 5000
    n_months = 12
    records = []
    
    for cust_id in range(1, n_customers + 1):
        # 3 nhóm khách hàng thực tế:
        # Group 0: Khách hàng trung thành (70%) - xu hướng ổn định/tăng trưởng
        # Group 1: Khách hàng suy giảm tương tác và rời bỏ (20%) - decay qua các tháng
        # Group 2: Khách hàng thất thường / nhạy cảm giá (10%)
        p_group = np.random.choice([0, 1, 2], p=[0.70, 0.20, 0.10])
        
        base_sessions = np.random.randint(5, 30)
        base_spend = np.random.uniform(20.0, 300.0)
        
        churn_label = 0
        if p_group == 1:
            churn_label = 1
            
        for month in range(1, n_months + 1):
            if p_group == 0:
                # Ổn định hoặc tăng nhẹ
                trend = 1.0 + 0.02 * month + np.random.normal(0, 0.1)
                complaints = np.random.poisson(0.1)
            elif p_group == 1:
                # Suy giảm hoạt động mạnh dần về các tháng cuối
                trend = max(0.1, 1.0 - 0.08 * month + np.random.normal(0, 0.15))
                complaints = np.random.poisson(0.5 + 0.1 * month)
            else:
                # Biến động ngẫu nhiên
                trend = 0.5 + 0.8 * np.random.rand()
                complaints = np.random.poisson(0.3)
                
            sessions = max(1, int(round(base_sessions * trend)))
            page_views = sessions * np.random.randint(3, 12)
            cart_adds = max(0, int(round(page_views * np.random.uniform(0.1, 0.35))))
            purchases = max(0, int(round(cart_adds * np.random.uniform(0.2, 0.8))))
            avg_duration = max(1.0, np.random.normal(12.0, 3.0) * trend)
            spent = round(max(0.0, purchases * (base_spend / max(1, base_sessions // 2)) * np.random.uniform(0.8, 1.2)), 2)
            discount_ratio = round(float(np.clip(np.random.beta(2, 5), 0.0, 1.0)), 3)
            
            records.append({
                'CustomerID': cust_id,
                'Month': month,
                'Sessions': sessions,
                'PageViews': page_views,
                'CartAdds': cart_adds,
                'Purchases': purchases,
                'AvgDurationMin': round(avg_duration, 1),
                'Complaints': complaints,
                'SpentUSD': spent,
                'DiscountRatio': discount_ratio,
                'ChurnNextPeriod': churn_label
            })
            
    df_cust = pd.DataFrame(records)
    cust_file = os.path.join(cust_dir, 'customer_sequential_behavior.csv')
    df_cust.to_csv(cust_file, index=False)
    print(f"✓ Đã tạo dữ liệu chuỗi hành vi ({len(df_cust):,} bản ghi cho {n_customers:,} khách hàng): {cust_file}")
    print(df_cust.head(3))
    print("\nHoàn tất tải và chuẩn bị toàn bộ dữ liệu!")

if __name__ == '__main__':
    prepare_datasets()
