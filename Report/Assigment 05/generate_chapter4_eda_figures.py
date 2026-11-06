# -*- coding: utf-8 -*-
"""
Script: generate_chapter4_eda_figures.py
Generates 10 individual, publication-quality, 300 DPI figures for Chapter 4 EDA & Data Preprocessing:
- Fig 4.1: Diabetes cleaning funnel & class imbalance
- Fig 4.2: Diabetes clinical biomarkers KDE (HbA1c & Glucose)
- Fig 4.3: Diabetes Pearson correlation matrix
- Fig 4.4: SVHN 10-digit optical sample grid
- Fig 4.5: SVHN class distribution (Train vs Test)
- Fig 4.6: SVHN RGB channel intensity distributions
- Fig 4.7: EuroSAT 10-class satellite remote sensing sample grid
- Fig 4.8: EuroSAT land use / land cover class distribution
- Fig 4.9: EuroSAT RGB spectral reflection density distributions
- Fig 4.10: Multi-domain input tensor and spatial dimensionality matrix
"""

import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import torchvision.datasets as dsets
from PIL import Image

# Styling parameters
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.9
plt.rcParams['grid.color'] = '#dddddd'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

output_dirs = [
    "Report/Assigment 05/images",
    "src/Assigment 05/reports/figures"
]
for d in output_dirs:
    os.makedirs(d, exist_ok=True)

def save_and_copy(fig, filename):
    p1 = os.path.join("Report/Assigment 05/images", filename)
    p2 = os.path.join("src/Assigment 05/reports/figures", filename)
    fig.savefig(p1, dpi=300, bbox_inches='tight')
    shutil.copy(p1, p2)
    plt.close(fig)
    print(f"Saved: {filename}")

# =========================================================================
# 1. DIABETES PREDICTION DATASET (100K SAMPLES)
# =========================================================================
print("Processing Diabetes dataset...")
df_raw = pd.read_csv("src/Assigment 02/diabetes/data/diabetes_prediction_dataset.csv")
n_raw = len(df_raw)
df_dedup = df_raw.drop_duplicates().copy()
n_dups = n_raw - len(df_dedup)
df_clean = df_dedup[df_dedup['gender'] != 'Other'].copy()
n_other = len(df_dedup) - len(df_clean)
n_final = len(df_clean)

df_clean['gender_code'] = (df_clean['gender'] == 'Male').astype(int)
smoking_map = {'never': 0, 'No Info': 0, 'former': 1, 'not current': 1, 'current': 2, 'ever': 2}
df_clean['smoking_code'] = df_clean['smoking_history'].map(smoking_map).fillna(0).astype(int)

# Fig 4.1: Cleaning Funnel
fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=300)
stages = ['1. Hồ sơ thô ban đầu', '2. Loại bỏ trùng lặp', '3. Chuẩn hóa giới tính', '4. Tập sạch sẵn sàng']
counts = [n_raw, len(df_dedup), n_final, n_final]
colors_a = ['#34495e', '#e67e22', '#c0392b', '#27ae60']
bars = ax.barh(np.arange(len(stages)), counts, color=colors_a, height=0.48, edgecolor='#222222', lw=0.9)
ax.set_yticks(np.arange(len(stages)))
ax.set_yticklabels(stages, fontsize=10, fontweight='bold')
ax.invert_yaxis()
ax.set_xlabel('Số lượng bản ghi hồ sơ bệnh nhân', fontsize=10.5, fontweight='bold')
ax.set_xlim(0, 126000)
ax.set_title('Quy Trình Kiểm Toán & Làm Sạch Dữ Liệu Diabetes (100,000 Bản Ghi Gốc)', fontsize=11.5, fontweight='bold', pad=12)

labels = [
    f'{n_raw:,} hồ sơ',
    f'-{n_dups:,} bản ghi trùng ({len(df_dedup):,} còn lại)',
    f'-{n_other} nhãn ngoại lai ({n_final:,} còn lại)',
    f'{n_final:,} mẫu sạch (87,664 bình thường vs 8,464 ĐTĐ - 10.4:1)'
]
for bar, txt in zip(bars, labels):
    w = bar.get_width()
    ax.text(w + 1500, bar.get_y() + bar.get_height()/2, txt, va='center', ha='left', fontsize=8.8, fontweight='bold', color='#2c3e50')
ax.grid(True, axis='x', linestyle=':', alpha=0.6)
save_and_copy(fig, "fig401_diabetes_cleaning_funnel.png")

# Fig 4.2: Biomarkers KDE
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.5), dpi=300)
sns.kdeplot(df_clean[df_clean.diabetes==0]['HbA1c_level'], ax=ax1, label='Không ĐTĐ (Âm tính)', color='#2980b9', lw=2.2, fill=True, alpha=0.18)
sns.kdeplot(df_clean[df_clean.diabetes==1]['HbA1c_level'], ax=ax1, label='Mắc ĐTĐ (Dương tính)', color='#e74c3c', lw=2.2, fill=True, alpha=0.22)
ax1.axvline(6.5, color='#c0392b', linestyle='--', lw=1.8, label='Ngưỡng chẩn đoán ADA (6.5%)')
ax1.set_title('Phân Bố Mật Độ Xác Suất HbA1c Level', fontsize=10.5, fontweight='bold', pad=10)
ax1.set_xlabel('Chỉ số HbA1c (%)', fontsize=9.5, fontweight='bold')
ax1.set_ylabel('Mật độ xác suất (KDE)', fontsize=9.5, fontweight='bold')
ax1.legend(fontsize=8.5, loc='upper left')
ax1.grid(True, linestyle=':', alpha=0.6)

sns.kdeplot(df_clean[df_clean.diabetes==0]['blood_glucose_level'], ax=ax2, label='Không ĐTĐ (Âm tính)', color='#2980b9', lw=2.2, fill=True, alpha=0.18)
sns.kdeplot(df_clean[df_clean.diabetes==1]['blood_glucose_level'], ax=ax2, label='Mắc ĐTĐ (Dương tính)', color='#e74c3c', lw=2.2, fill=True, alpha=0.22)
ax2.axvline(126.0, color='#e67e22', linestyle='--', lw=1.8, label='Ngưỡng đường huyết đói ĐTĐ (126 mg/dL)')
ax2.set_title('Phân Bố Mật Độ Đường Huyết Tức Thời (Blood Glucose)', fontsize=10.5, fontweight='bold', pad=10)
ax2.set_xlabel('Nồng độ Glucose (mg/dL)', fontsize=9.5, fontweight='bold')
ax2.set_ylabel('Mật độ xác suất (KDE)', fontsize=9.5, fontweight='bold')
ax2.legend(fontsize=8.5, loc='upper right')
ax2.grid(True, linestyle=':', alpha=0.6)
save_and_copy(fig, "fig402_diabetes_biomarker_kde.png")

# Fig 4.3: Pearson Correlation Matrix
fig, ax = plt.subplots(figsize=(7.5, 6.0), dpi=300)
feat_names = ['Gender', 'Age', 'Hyperten.', 'HeartDis.', 'Smoking', 'BMI', 'HbA1c', 'Glucose', 'Diabetes']
corr = df_clean[['gender_code', 'age', 'hypertension', 'heart_disease', 'smoking_code', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'diabetes']].corr()
corr.columns = feat_names
corr.index = feat_names
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, cmap='Blues', annot=True, fmt='.2f', annot_kws={'size': 8.5, 'weight': 'bold'},
            cbar_kws={'shrink': 0.8, 'aspect': 20, 'pad': 0.04}, ax=ax, square=True, linewidths=0.6, linecolor='#ffffff')
ax.set_title('Ma Trận Hệ Số Tương Quan Tuyến Tính Pearson (Tập Sạch 96,128 Mẫu)', fontsize=11, fontweight='bold', pad=12)
ax.tick_params(axis='both', which='major', labelsize=9)
save_and_copy(fig, "fig403_diabetes_correlation_matrix.png")


# =========================================================================
# 2. SVHN DATASET
# =========================================================================
print("Processing SVHN dataset...")
svhn_train = dsets.SVHN(root='src/Assigment 05/data', split='train', download=False)
svhn_test = dsets.SVHN(root='src/Assigment 05/data', split='test', download=False)
train_labels = svhn_train.labels
test_labels = svhn_test.labels

# Fig 4.4: SVHN Sample Grid (10 classes x 5 samples)
fig, axes = plt.subplots(10, 5, figsize=(8.0, 14.0), dpi=300)
digit_samples = {d: [] for d in range(10)}
for idx in range(len(svhn_train)):
    lbl = int(train_labels[idx])
    if len(digit_samples[lbl]) < 5:
        img = np.transpose(svhn_train.data[idx], (1, 2, 0))
        digit_samples[lbl].append(img)
    if all(len(v) == 5 for v in digit_samples.values()):
        break

for d in range(10):
    for col in range(5):
        ax = axes[d, col]
        ax.imshow(digit_samples[d][col])
        ax.set_xticks([])
        ax.set_yticks([])
        if col == 0:
            ax.set_ylabel(f"Chữ số {d}", fontsize=9.5, fontweight='bold', rotation=0, labelpad=28, va='center')
        if d == 0:
            ax.set_title(f"Mẫu {col+1}", fontsize=9.5, fontweight='bold', pad=6)

plt.suptitle("Lưới Ảnh Quang Học Mẫu 10 Phân Lớp Chữ Số SVHN (32×32 RGB)\n(Nhiễu nền ngoại cảnh, số lân cận xâm lấn, góc nghiêng 3D)", fontsize=11.5, fontweight='bold', y=0.995)
plt.tight_layout()
save_and_copy(fig, "fig404_svhn_sample_grid.png")

# Fig 4.5: SVHN Class Distribution
fig, ax = plt.subplots(figsize=(9.0, 4.5), dpi=300)
train_counts = np.bincount(train_labels, minlength=10)
test_counts = np.bincount(test_labels, minlength=10)
x_digits = np.arange(10)
width = 0.38
b1 = ax.bar(x_digits - width/2, train_counts, width, label=f'Tập Huấn luyện ({len(train_labels):,} ảnh)', color='#2980b9', edgecolor='#222222', lw=0.8)
b2 = ax.bar(x_digits + width/2, test_counts, width, label=f'Tập Kiểm tra ({len(test_labels):,} ảnh)', color='#27ae60', edgecolor='#222222', lw=0.8)
ax.set_xticks(x_digits)
ax.set_xticklabels([f"Số {d}" for d in range(10)], fontsize=9.5, fontweight='bold')
ax.set_ylabel("Số lượng ảnh mẫu", fontsize=10, fontweight='bold')
ax.set_title("Phân Bố Tần Suất 10 Lớp Chữ Số Ngoại Cảnh SVHN (Train vs Test)", fontsize=11.5, fontweight='bold', pad=12)
ax.legend(fontsize=9, loc='upper right')
ax.grid(True, axis='y', linestyle=':', alpha=0.6)
for bar in b1:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 150, f'{h:,}', ha='center', va='bottom', fontsize=7.2, rotation=45, color='#1f3a93', fontweight='bold')
save_and_copy(fig, "fig405_svhn_class_distribution.png")

# Fig 4.6: SVHN RGB Histograms
fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=300)
np.random.seed(42)
sub_idx = np.random.choice(len(svhn_train), 3000, replace=False)
r_vals = svhn_train.data[sub_idx, 0, :, :].flatten() / 255.0
g_vals = svhn_train.data[sub_idx, 1, :, :].flatten() / 255.0
b_vals = svhn_train.data[sub_idx, 2, :, :].flatten() / 255.0

# Subsample 50,000 points for fast KDE
sub_p = np.random.choice(len(r_vals), 50000, replace=False)
sns.kdeplot(r_vals[sub_p], ax=ax, color='#e74c3c', label=f'Kênh Red (μ={r_vals.mean():.3f}, σ={r_vals.std():.3f})', lw=2.0)
sns.kdeplot(g_vals[sub_p], ax=ax, color='#27ae60', label=f'Kênh Green (μ={g_vals.mean():.3f}, σ={g_vals.std():.3f})', lw=2.0)
sns.kdeplot(b_vals[sub_p], ax=ax, color='#2980b9', label=f'Kênh Blue (μ={b_vals.mean():.3f}, σ={b_vals.std():.3f})', lw=2.0)
ax.set_xlim(0, 1)
ax.set_xlabel("Cường độ sáng chuẩn hóa [0, 1]", fontsize=10, fontweight='bold')
ax.set_ylabel("Mật độ xác suất", fontsize=10, fontweight='bold')
ax.set_title("Phân Phối Cường Độ Quang Học 3 Kênh Màu RGB Của Tập SVHN", fontsize=11.5, fontweight='bold', pad=12)
ax.legend(fontsize=9.5, loc='upper right')
ax.grid(True, linestyle=':', alpha=0.6)
save_and_copy(fig, "fig406_svhn_rgb_channel_histograms.png")


# =========================================================================
# 3. EUROSAT SATELLITE DATASET (27,000 SAMPLES)
# =========================================================================
print("Processing EuroSAT satellite dataset...")
eurosat_ds = dsets.EuroSAT(root='src/Assigment 05/data', download=False)
euro_classes = eurosat_ds.classes
euro_vn_names = {
    'AnnualCrop': 'Cây hàng năm',
    'Forest': 'Rừng tự nhiên',
    'HerbaceousVegetation': 'Thảm thực vật thảo',
    'Highway': 'Đường cao tốc',
    'Industrial': 'Khu công nghiệp',
    'Pasture': 'Đồng cỏ chăn thả',
    'PermanentCrop': 'Cây lâu năm',
    'Residential': 'Khu dân cư',
    'River': 'Sông ngòi',
    'SeaLake': 'Biển & hồ nước'
}

# Fig 4.7: EuroSAT Sample Grid (10 classes x 5 samples)
fig, axes = plt.subplots(10, 5, figsize=(8.0, 14.0), dpi=300)
euro_samples = {c: [] for c in range(10)}
for img, lbl in eurosat_ds:
    if len(euro_samples[lbl]) < 5:
        euro_samples[lbl].append(np.array(img))
    if all(len(v) == 5 for v in euro_samples.values()):
        break

for c in range(10):
    c_name = euro_classes[c]
    vn_name = euro_vn_names[c_name]
    for col in range(5):
        ax = axes[c, col]
        ax.imshow(euro_samples[c][col])
        ax.set_xticks([])
        ax.set_yticks([])
        if col == 0:
            ax.set_ylabel(f"{c_name}\n({vn_name})", fontsize=8.2, fontweight='bold', rotation=0, labelpad=48, va='center')
        if c == 0:
            ax.set_title(f"Mẫu {col+1}", fontsize=9.5, fontweight='bold', pad=6)

plt.suptitle("Lưới Ảnh Mẫu Viễn Thám Vệ Tinh Sentinel-2 EuroSAT (64×64 RGB)\n(10 phân lớp che phủ và sử dụng đất LULC, góc nhìn phương thẳng đứng)", fontsize=11.5, fontweight='bold', y=0.995)
plt.tight_layout()
save_and_copy(fig, "fig407_eurosat_sample_grid.png")

# Fig 4.8: EuroSAT Class Distribution
fig, ax = plt.subplots(figsize=(9.5, 4.5), dpi=300)
euro_targets = [s[1] for s in eurosat_ds.samples]
euro_counts = np.bincount(euro_targets, minlength=10)
x_euro = np.arange(10)
bar_colors = ['#27ae60', '#1e824c', '#2ecc71', '#d35400', '#7f8c8d', '#f39c12', '#16a085', '#9b59b6', '#2980b9', '#3498db']
bars_e = ax.bar(x_euro, euro_counts, color=bar_colors, edgecolor='#222222', lw=0.9, width=0.6)
ax.set_xticks(x_euro)
ax.set_xticklabels([f"{euro_classes[i]}\n({euro_vn_names[euro_classes[i]]})" for i in range(10)], fontsize=8.0, fontweight='bold', rotation=25, ha='right')
ax.set_ylabel("Số lượng ảnh viễn thám", fontsize=10, fontweight='bold')
ax.set_ylim(0, 3500)
ax.set_title("Phân Bố Số Lượng 10 Phân Lớp Đất Bề Mặt Tập Ảnh Vệ Tinh EuroSAT (Tổng 27,000 Mẫu)", fontsize=11.5, fontweight='bold', pad=12)
ax.grid(True, axis='y', linestyle=':', alpha=0.6)
for bar in bars_e:
    h = bar.get_height()
    pct = h / 27000 * 100
    ax.text(bar.get_x() + bar.get_width()/2, h + 60, f'{h:,}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=7.8, fontweight='bold', color='#2c3e50')
save_and_copy(fig, "fig408_eurosat_class_distribution.png")

# Fig 4.9: EuroSAT RGB Spectral Histograms
fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=300)
np.random.seed(42)
sub_euro_idx = np.random.choice(len(eurosat_ds), 2000, replace=False)
e_r, e_g, e_b = [], [], []
for i in sub_euro_idx:
    arr = np.array(eurosat_ds[i][0], dtype=np.float32) / 255.0
    e_r.append(arr[:, :, 0].flatten())
    e_g.append(arr[:, :, 1].flatten())
    e_b.append(arr[:, :, 2].flatten())

e_r = np.concatenate(e_r)
e_g = np.concatenate(e_g)
e_b = np.concatenate(e_b)

r_m, r_s = e_r.mean(), e_r.std()
g_m, g_s = e_g.mean(), e_g.std()
b_m, b_s = e_b.mean(), e_b.std()

sub_pts = np.random.choice(len(e_r), 50000, replace=False)
sns.kdeplot(e_r[sub_pts], ax=ax, color='#e74c3c', label=f'Kênh Red (μ={r_m:.3f}, σ={r_s:.3f})', lw=2.0)
sns.kdeplot(e_g[sub_pts], ax=ax, color='#27ae60', label=f'Kênh Green (μ={g_m:.3f}, σ={g_s:.3f})', lw=2.0)
sns.kdeplot(e_b[sub_pts], ax=ax, color='#2980b9', label=f'Kênh Blue (μ={b_m:.3f}, σ={b_s:.3f})', lw=2.0)
ax.set_xlim(0, 1)
ax.set_xlabel("Hệ số phản xạ phổ quang học chuẩn hóa [0, 1]", fontsize=10, fontweight='bold')
ax.set_ylabel("Mật độ xác suất phản xạ phổ", fontsize=10, fontweight='bold')
ax.set_title("Đặc Tính Phổ Phản Xạ Quang Học 3 Kênh Màu RGB Của Ảnh Vệ Tinh EuroSAT", fontsize=11.5, fontweight='bold', pad=12)
ax.legend(fontsize=9.5, loc='upper right')
ax.grid(True, linestyle=':', alpha=0.6)
save_and_copy(fig, "fig409_eurosat_rgb_spectral_histograms.png")


# =========================================================================
# 4. MULTI-DOMAIN TENSOR & COMPARISON MATRIX
# =========================================================================
print("Generating Fig 4.10: Multi-domain Tensor Matrix...")
fig, ax = plt.subplots(figsize=(10.0, 5.2), dpi=300)
domains = ['Dữ liệu Bảng Y Sinh\n(Diabetes 100k)', 'Ảnh Quang Học Ngoại Cảnh\n(SVHN 99k)', 'Ảnh Viễn Thám Vệ Tinh\n(EuroSAT 27k)']
rect_colors = ['#ebf5fb', '#fef9e7', '#eafaf1']
border_colors = ['#2980b9', '#f39c12', '#27ae60']
box_texts = [
    "Dạng biểu diễn: Chuỗi đặc trưng 1 chiều\nTensor đầu vào: (Batch, 1, 8)\nChiều không gian: L = 8 đặc trưng\nKênh tín hiệu: C_in = 1\n\nMô hình thiết kế: 1D-CNN\n(Conv1D trích xuất tương tác phi tuyến\ngiữa các cặp chỉ số sinh hóa lâm sàng)",
    "Dạng biểu diễn: Lưới điểm ảnh 2 chiều\nTensor đầu vào: (Batch, 3, 32, 32)\nChiều không gian: 32 × 32 pixels\nKênh màu quang học: 3 kênh RGB\n\nMô hình thiết kế: 2D-CNN\n(Baseline CNN, VGG-11, ResNet-18;\nQuy tắc: CẤM lật ngang ký tự)",
    "Dạng biểu diễn: Lưới viễn thám đa phổ\nTensor đầu vào: (Batch, 3, 64, 64)\nChiều không gian: 64 × 64 pixels\nKênh phản xạ phổ: 3 kênh RGB\n\nMô hình thiết kế: 2D-CNN & Transfer\n(ResNet-18, MobileNetV2;\nQuy tắc: Đối xứng quay tự do 2D)"
]

ax.set_xlim(-0.5, 2.5)
ax.set_ylim(-0.2, 1.2)
ax.axis('off')

for i in range(3):
    ax.text(i, 1.05, domains[i], ha='center', va='center', fontsize=11, fontweight='bold', color=border_colors[i],
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor=border_colors[i], lw=2))
    ax.text(i, 0.45, box_texts[i], ha='center', va='center', fontsize=9.2, color='#2c3e50',
            bbox=dict(boxstyle='square,pad=0.8', facecolor=rect_colors[i], edgecolor=border_colors[i], lw=1.5))

plt.title("So Sánh Hình Thái Không Gian Biểu Diễn & Định Dạng Tensor Giữa 3 Bộ Dữ Liệu Đa Miền", fontsize=12, fontweight='bold', pad=25)
plt.tight_layout()
save_and_copy(fig, "fig410_multidomain_tensor_matrix.png")

print("All 10 individual figures generated and copied successfully!")
