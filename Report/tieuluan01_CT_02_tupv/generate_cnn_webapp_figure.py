import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

fig, ax = plt.subplots(figsize=(15, 9), dpi=300)
fig.patch.set_facecolor('#0b0f19')
ax.set_facecolor('#0b0f19')

# Window frame
window = patches.FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                                boxstyle=patches.BoxStyle("Round", pad=0.015, rounding_size=0.02),
                                facecolor='#111827', edgecolor='#1f2937', lw=2)
ax.add_patch(window)

# Top Bar / Badge
ax.text(0.5, 0.94, "[*] MẠNG NƠ-RON TÍCH CHẬP • CNN / RESNET-18 / MOBILENETV2 • TRIỂN KHAI THỰC TIỄN",
        fontsize=10.5, fontweight='bold', color='#38bdf8', ha='center',
        bbox=dict(boxstyle="round,pad=0.4", fc="#0c4a6e", ec="#0284c7", lw=1.2))

# Header Title
ax.text(0.5, 0.89, "Hệ Thống Phân Loại Ảnh Thị Giác Máy Tính Đa Miền (Vision AI Dashboard)",
        fontsize=19, fontweight='bold', color='#f8fafc', ha='center')
ax.text(0.5, 0.855, "Ứng dụng mô hình học sâu CNN trên tập dữ liệu ảnh viễn thám EuroSAT và chữ số ngoại cảnh SVHN",
        fontsize=11.5, fontstyle='italic', color='#94a3b8', ha='center')

# Tabs
tab1 = patches.FancyBboxPatch((0.25, 0.79), 0.24, 0.045, boxstyle="round,pad=0.008,rounding_size=0.01",
                              facecolor='#2563eb', edgecolor='none')
tab2 = patches.FancyBboxPatch((0.51, 0.79), 0.24, 0.045, boxstyle="round,pad=0.008,rounding_size=0.01",
                              facecolor='#1e293b', edgecolor='#334155')
ax.add_patch(tab1)
ax.add_patch(tab2)
ax.text(0.37, 0.812, "[1] Phân Hệ: Phân Loại Viễn Thám EuroSAT", fontsize=11, fontweight='bold', color='#ffffff', ha='center')
ax.text(0.63, 0.812, "[2] Phân Hệ: Nhận Diện Chữ Số SVHN", fontsize=11, fontweight='bold', color='#94a3b8', ha='center')

# Panel 1: Upload & Image Viewer (Left)
p1 = patches.FancyBboxPatch((0.05, 0.16), 0.28, 0.60, boxstyle="round,pad=0.01,rounding_size=0.015",
                            facecolor='#0f172a', edgecolor='#1e293b', lw=1.5)
ax.add_patch(p1)
ax.text(0.08, 0.725, "HÌNH ẢNH ĐẦU VÀO (INPUT)", fontsize=11.5, fontweight='bold', color='#38bdf8')

# Simulated Image Box
img_box = patches.FancyBboxPatch((0.08, 0.38), 0.22, 0.31, boxstyle="round,pad=0.005",
                                facecolor='#064e3b', edgecolor='#10b981', lw=1.8)
ax.add_patch(img_box)

# Draw simulated satellite texture inside
np.random.seed(42)
for _ in range(35):
    cx = 0.09 + np.random.rand() * 0.20
    cy = 0.40 + np.random.rand() * 0.27
    r = 0.01 + np.random.rand() * 0.02
    circle = patches.Circle((cx, cy), r, facecolor='#047857', alpha=0.6)
    ax.add_patch(circle)

# Rivers / paths
ax.plot([0.09, 0.15, 0.22, 0.29], [0.42, 0.50, 0.58, 0.66], color='#0284c7', lw=3, alpha=0.7)
ax.text(0.19, 0.52, "Ảnh Vệ Tinh (EuroSAT)", fontsize=10.5, fontweight='bold', color='#ffffff', ha='center',
        bbox=dict(boxstyle="round,pad=0.3", fc="#000000", ec="none", alpha=0.6))

# Metadata info
ax.text(0.08, 0.33, "Kích thước: 64 x 64 pixels (RGB)", fontsize=9.5, color='#cbd5e1')
ax.text(0.08, 0.29, "Chuẩn hóa: mean=[0.485, 0.456, 0.406]", fontsize=9, color='#94a3b8')
ax.text(0.08, 0.25, "Định dạng tải lên: PNG / TIFF đa phổ", fontsize=9, color='#94a3b8')
ax.text(0.08, 0.20, "Trạng thái: Tải ảnh thành công [OK]", fontsize=9.5, fontweight='bold', color='#10b981')

# Panel 2: Model Architecture & Feature Representation (Middle)
p2 = patches.FancyBboxPatch((0.35, 0.16), 0.30, 0.60, boxstyle="round,pad=0.01,rounding_size=0.015",
                            facecolor='#0f172a', edgecolor='#1e293b', lw=1.5)
ax.add_patch(p2)
ax.text(0.38, 0.725, "MÔ HÌNH SUY LUẬN & ĐẶC TRƯNG", fontsize=11.5, fontweight='bold', color='#38bdf8')

# Selector Box
sel_box = patches.FancyBboxPatch((0.38, 0.64), 0.24, 0.05, boxstyle="round,pad=0.005",
                                facecolor='#1e293b', edgecolor='#3b82f6')
ax.add_patch(sel_box)
ax.text(0.40, 0.665, "Mô hình: ResNet-18 (ONNX) ▼", fontsize=10, color='#f8fafc')

# Feature Activation Map bars
ax.text(0.38, 0.59, "Trực quan hóa Bản đồ Kích hoạt (CAM):", fontsize=9.5, fontweight='bold', color='#cbd5e1')

classes = ['Forest', 'Pasture', 'Residential', 'River', 'Highway']
scores = [0.984, 0.011, 0.003, 0.001, 0.001]
bar_y = [0.52, 0.45, 0.38, 0.31, 0.24]

for c, s, y in zip(classes, scores, bar_y):
    ax.text(0.38, y + 0.02, f"{c}: {s*100:.1f}%", fontsize=9, color='#e2e8f0')
    # background bar
    bg_bar = patches.FancyBboxPatch((0.38, y - 0.015), 0.24, 0.02, boxstyle="round,pad=0.002",
                                   facecolor='#1e293b', edgecolor='none')
    ax.add_patch(bg_bar)
    # filled bar
    fill_bar = patches.FancyBboxPatch((0.38, y - 0.015), 0.24 * s, 0.02, boxstyle="round,pad=0.002",
                                     facecolor='#10b981' if s > 0.5 else '#3b82f6', edgecolor='none')
    ax.add_patch(fill_bar)

ax.text(0.38, 0.185, "Độ phân giải đặc trưng cuối: 512-dim GAP", fontsize=9, color='#64748b')

# Panel 3: Inference Results & Runtime (Right)
p3 = patches.FancyBboxPatch((0.67, 0.16), 0.28, 0.60, boxstyle="round,pad=0.01,rounding_size=0.015",
                            facecolor='#0f172a', edgecolor='#1e293b', lw=1.5)
ax.add_patch(p3)
ax.text(0.70, 0.725, "KẾT QUẢ SUY LUẬN (OUTPUT)", fontsize=11.5, fontweight='bold', color='#38bdf8')

# Result highlight card
res_card = patches.FancyBboxPatch((0.69, 0.46), 0.24, 0.23, boxstyle="round,pad=0.008",
                                  facecolor='#1e293b', edgecolor='#334155')
ax.add_patch(res_card)
ax.text(0.71, 0.64, "PHÂN LỚP DỰ BÁO", fontsize=9.5, fontweight='bold', color='#94a3b8')
ax.text(0.71, 0.575, "Forest", fontsize=24, fontweight='bold', color='#10b981')
ax.text(0.71, 0.525, "(Rừng Tự Nhiên)", fontsize=12, fontweight='bold', color='#a7f3d0')
ax.text(0.71, 0.48, "Độ tin cậy (Confidence): 98.40%", fontsize=10, fontweight='bold', color='#38bdf8')

# Inference stats box
stats_box = patches.FancyBboxPatch((0.69, 0.31), 0.24, 0.12, boxstyle="round,pad=0.006",
                                   facecolor='#18181b', edgecolor='#38bdf8')
ax.add_patch(stats_box)
ax.text(0.71, 0.395, "THÔNG SỐ THỰC THI (RUNTIME)", fontsize=9, fontweight='bold', color='#38bdf8')
ax.text(0.71, 0.36, "Runtime Engine: ONNX Runtime C++", fontsize=8.5, color='#e2e8f0')
ax.text(0.71, 0.33, "Độ trễ (Latency): 14.5 ms (CPU)", fontsize=8.5, color='#e2e8f0')

# Disclaimer / Ecological Note
note_box = patches.FancyBboxPatch((0.69, 0.18), 0.24, 0.10, boxstyle="round,pad=0.006",
                                  facecolor='#18181b', edgecolor='#64748b')
ax.add_patch(note_box)
ax.text(0.71, 0.245, "Ứng dụng thực tế:", fontsize=8.5, fontweight='bold', color='#94a3b8')
ax.text(0.71, 0.20, "Giám sát biến động diện tích rừng,\nquy hoạch sử dụng đất và quản lý đô thị.",
        fontsize=8, color='#cbd5e1', linespacing=1.2)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
plt.tight_layout()

out_path = 'Report/tieuluan01_CT_02_tupv/images/fig509_webapp_cnn_vision_ui.png'
fig.savefig(out_path, bbox_inches='tight')
plt.close(fig)
print(f"✓ Đã lưu {out_path}")
