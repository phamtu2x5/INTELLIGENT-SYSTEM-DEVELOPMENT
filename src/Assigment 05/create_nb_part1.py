import json

cells = []

def add_md(text):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")]
    })

def add_code(text):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.strip().split("\n")]
    })

# 1. Header
add_md("""# HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG
## BÀI TẬP LỚN ASSIGNMENT 05: PHÁT TRIỂN HỆ THỐNG THÔNG MINH
### CHUYÊN ĐỀ: MẠNG NƠ-RON TÍCH CHẬP (CNN) — TỪ NỀN TẢNG TOÁN HỌC ĐẾN KIẾN TRÚC PHÁT TRIỂN
**Sinh viên thực hiện:** Phạm Văn Tư — Mã SV: B23DCCN879 — Lớp: D23CTPM01  
**Giảng viên hướng dẫn:** PGS.TS Trần Đình Quế

---
### PHẦN 1: CƠ SỞ LÝ THUYẾT & HIỆN THỰC HÓA CÁC HÀM TOÁN HỌC TRONG MẠNG NƠ-RON TÍCH CHẬP (CNN)""")

# 2. Section 1
add_md("""### 1. Nạp Thư viện Chuẩn & Cấu hình Môi trường Thực nghiệm
Trong bài toán này, toàn bộ các hàm toán học cốt lõi được xây dựng tường minh bằng thư viện số học NumPy và kiểm chứng bằng PyTorch. Hệ thống tuân thủ nguyên tắc tự chứa (Self-Contained), không sử dụng các file script phụ trợ bên ngoài.""")

add_code("""import os
import time
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F

# Cấu hình hạt giống ngẫu nhiên để đảm bảo tính tái lập (Reproducibility)
np.random.seed(42)
torch.manual_seed(42)

print(f"PyTorch Version: {torch.__version__}")
device = torch.device("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"))
print(f"Thiết bị tính toán sử dụng: {device}")""")

# 3. Section 2
add_md("""### 2. Định nghĩa Toán học của Hàm Tích chập 2D Đa Kênh (Multi-Channel Convolution Function)
Xét tensor đầu vào $X \\in \\mathbb{R}^{H_{\\text{in}} \\times W_{\\text{in}} \\times C_{\\text{in}}}$ và bộ lọc gồm $M$ kernels $W \\in \\mathbb{R}^{K_H \\times K_W \\times C_{\\text{in}} \\times M}$, vector độ chệch $b \\in \\mathbb{R}^M$.

Tại mỗi vị trí không gian $(i, j)$ và kênh đầu ra thứ $m \\in \\{1, \\dots, M\\}$, giá trị của bản đồ đặc trưng được tính theo tích vô hướng từng phần tử (Frobenius Inner Product) cộng dồn trên toàn bộ $C_{\\text{in}}$ kênh:
$$Z(i, j, m) = \\sum_{c=1}^{C_{\\text{in}}} \\sum_{p=0}^{K_H-1} \\sum_{q=0}^{K_W-1} X(s \\cdot i + p - P, s \\cdot j + q - P, c) \\cdot W(p, q, c, m) + b(m)$$

Kích thước không gian của bản đồ đặc trưng đầu ra được xác định bởi công thức giải tích:
$$H_{\\text{out}} = \\left\\lfloor \\frac{H_{\\text{in}} + 2P - d(K_H - 1) - 1}{s} \\right\\rfloor + 1, \\quad W_{\\text{out}} = \\left\\lfloor \\frac{W_{\\text{in}} + 2P - d(K_W - 1) - 1}{s} \\right\\rfloor + 1$$""")

add_code("""def conv2d_forward_explicit(X, W, b, stride=1, padding=0):
    \"\"\"
    Cài đặt hàm tích chập 2D đa kênh thuần toán học (Explicit Loops).
    Tham số:
      X: Tensor đầu vào shape (H_in, W_in, C_in)
      W: Ma trận trọng số shape (K_h, K_w, C_in, C_out)
      b: Vector bias shape (C_out,)
      stride: Bước trượt s
      padding: Số lượng hàng/cột số 0 đệm viền P
    Trả về:
      Z: Tensor đặc trưng đầu ra shape (H_out, W_out, C_out)
    \"\"\"
    H_in, W_in, C_in = X.shape
    K_h, K_w, C_in_w, C_out = W.shape
    assert C_in == C_in_w, "Số kênh đầu vào phải khớp với số kênh của bộ lọc!"
    
    # 1. Áp dụng đệm viền Zero-Padding
    if padding > 0:
        X_padded = np.pad(X, ((padding, padding), (padding, padding), (0, 0)), mode="constant", constant_values=0)
    else:
        X_padded = X
        
    # 2. Tính kích thước không gian đầu ra
    H_out = int(np.floor((H_in + 2 * padding - K_h) / stride)) + 1
    W_out = int(np.floor((W_in + 2 * padding - K_w) / stride)) + 1
    
    Z = np.zeros((H_out, W_out, C_out), dtype=np.float32)
    
    # 3. Quét cửa sổ trượt
    for m in range(C_out):
        for i in range(H_out):
            for j in range(W_out):
                h_start = i * stride
                h_end = h_start + K_h
                w_start = j * stride
                w_end = w_start + K_w
                
                # Cửa sổ tiếp nhận cục bộ X_slice shape (K_h, K_w, C_in)
                X_slice = X_padded[h_start:h_end, w_start:w_end, :]
                
                # Tích vô hướng từng phần tử trên 3 chiều không gian và kênh + bias
                Z[i, j, m] = np.sum(X_slice * W[:, :, :, m]) + b[m]
                
    return Z

# Kiểm chứng tính đúng đắn với tensor ngẫu nhiên
x_sample = np.random.randn(8, 8, 3).astype(np.float32)
w_sample = np.random.randn(3, 3, 3, 4).astype(np.float32)
b_sample = np.zeros(4, dtype=np.float32)

z_custom = conv2d_forward_explicit(x_sample, w_sample, b_sample, stride=1, padding=1)
print(f"Tensor đầu vào: {x_sample.shape}")
print(f"Bộ lọc Kernel: {w_sample.shape}")
print(f"Bản đồ đặc trưng đầu ra: {z_custom.shape} (Bảo toàn kích thước không gian H_out = H_in nhờ Same Padding)")""")

# 4. Section 3
add_md("""### 3. Hàm Kích hoạt Phi tuyến (Nonlinear Activation Function)
Bản chất toán học của hàm ReLU:
$$\\text{ReLU}(z) = \\max(0, z), \\quad \\frac{d}{dz}\\text{ReLU}(z) = \\begin{cases} 1 & \\text{nếu } z > 0 \\\\ 0 & \\text{nếu } z \\le 0 \\end{cases}$$

Ưu điểm quyết định:
1. Triệt tiêu hiện tượng bão hòa đạo hàm (Vanishing Gradient): Khi $z > 0$, đạo hàm luôn bằng 1 giúp gradient truyền ngược nguyên vẹn qua hàng chục tầng sâu.
2. Tạo tính thưa thớt (Sparsity): Khóa các nơ-ron không hoạt động ($z \\le 0$), giúp mạng học biểu diễn tách biệt rõ ràng.""")

add_code("""def relu_forward(Z):
    \"\"\"Hàm kích hoạt phi tuyến ReLU: A = max(0, Z)\"\"\"
    return np.maximum(0, Z)

a_custom = relu_forward(z_custom)
print(f"Tỷ lệ nơ-ron bị kích hoạt (Active Neurons): {np.mean(a_custom > 0) * 100:.2f}%")
print(f"Số lượng giá trị âm bị triệt tiêu về 0: {np.sum(a_custom == 0)} / {a_custom.size}")""")

# 5. Section 4
add_md("""### 4. Hàm Gom cụm Không gian: Max Pooling vs Global Average Pooling (GAP)
1. **Max Pooling $2 \\times 2$ (Stride 2):**
$$P(i, j, c) = \\max_{p, q \\in [0, 1]} A(2i + p, 2j + q, c)$$
Thu nhỏ kích thước không gian 4 lần ($H/2 \\times W/2$), trích xuất đặc trưng có độ kích hoạt mạnh nhất trong vùng lân cận.

2. **Global Average Pooling (GAP):**
$$v(c) = \\frac{1}{H \\cdot W} \\sum_{i=1}^H \\sum_{j=1}^W A(i, j, c)$$
Thu gọn toàn bộ không gian 2D về 1 giá trị vô hướng duy nhất trên mỗi kênh, loại bỏ hoàn toàn các tầng liên kết đầy đủ (Dense) cồng kềnh với hàng triệu tham số.""")

add_code("""def maxpool2d_forward(A, pool_size=2, stride=2):
    \"\"\"Hàm gom cụm cực đại Max Pooling 2D\"\"\"
    H, W, C = A.shape
    H_out = (H - pool_size) // stride + 1
    W_out = (W - pool_size) // stride + 1
    P = np.zeros((H_out, W_out, C), dtype=np.float32)
    
    for c in range(C):
        for i in range(H_out):
            for j in range(W_out):
                h_start = i * stride
                h_end = h_start + pool_size
                w_start = j * stride
                w_end = w_start + pool_size
                P[i, j, c] = np.max(A[h_start:h_end, w_start:w_end, c])
    return P

def global_average_pooling(A):
    \"\"\"Hàm gom cụm trung bình toàn cục Global Average Pooling (GAP)\"\"\"
    return np.mean(A, axis=(0, 1))

p_custom = maxpool2d_forward(a_custom, pool_size=2, stride=2)
v_gap = global_average_pooling(a_custom)

print(f"Kích thước sau Max Pooling: {p_custom.shape} (Giảm 75% số điểm ảnh)")
print(f"Kích thước sau GAP: {v_gap.shape} (Vector đặc trưng 1D đại diện cho {v_gap.shape[0]} kênh)")""")

# 6. Section 5
add_md("""### 5. Biểu diễn Kiến trúc CNN Dưới Dạng Hàm Hợp (Composite Function)
Toàn bộ mạng nơ-ron tích chập từ ảnh đầu vào đến vector xác suất dự đoán được biểu diễn toán học như một hàm hợp gồm $L$ phép biến đổi ánh xạ liên tiếp:
$$\\hat{y} = f(X; \\theta) = (f_L \\circ f_{L-1} \\circ \\dots \\circ f_3 \\circ f_2 \\circ f_1)(X)$$

Trong đó chuỗi biến đổi hình thái tensor qua từng tầng được định nghĩa tường minh:
1. $f_1: \\mathbb{R}^{32 \\times 32 \\times 3} \\to \\mathbb{R}^{32 \\times 32 \\times 32}$ — Biến đổi tích chập $Z^{[1]} = \\text{Conv2D}(X)$
2. $f_2: \\mathbb{R}^{32 \\times 32 \\times 32} \\to \\mathbb{R}^{32 \\times 32 \\times 32}$ — Kích hoạt phi tuyến $A^{[1]} = \\text{ReLU}(Z^{[1]})$
3. $f_3: \\mathbb{R}^{32 \\times 32 \\times 32} \\to \\mathbb{R}^{16 \\times 16 \\times 32}$ — Gom cụm không gian $P^{[1]} = \\text{MaxPool}(A^{[1]})$
4. $f_4: \\mathbb{R}^{16 \\times 16 \\times 32} \\to \\mathbb{R}^{16 \\times 16 \\times 64}$ — Tích chập tầng sâu $Z^{[2]} = \\text{Conv2D}(P^{[1]})$
5. $f_5: \\mathbb{R}^{16 \\times 16 \\times 64} \\to \\mathbb{R}^{16 \\times 16 \\times 64}$ — Kích hoạt $A^{[2]} = \\text{ReLU}(Z^{[2]})$
6. $f_6: \\mathbb{R}^{16 \\times 16 \\times 64} \\to \\mathbb{R}^{8 \\times 8 \\times 64}$ — Gom cụm không gian $P^{[2]} = \\text{MaxPool}(A^{[2]})$
7. $f_7: \\mathbb{R}^{8 \\times 8 \\times 64} \\to \\mathbb{R}^{64}$ — Nén không gian toàn cục $v = \\text{GAP}(P^{[2]})$
8. $f_8: \\mathbb{R}^{64} \\to \\mathbb{R}^{10}$ — Chiếu tuyến tính sang không gian nhãn $z_c = W_c v + b_c$
9. $f_9: \\mathbb{R}^{10} \\to [0, 1]^{10}$ — Chuẩn hóa xác suất Softmax $\\hat{y} = \\text{Softmax}(z_c)$""")

add_code("""class ExplicitCompositeCNN(nn.Module):
    \"\"\"
    Mô hình Mạng nơ-ron Tích chập thể hiện tường minh 100% bản chất Hàm Hợp.
    Mỗi hàm thành phần f_i là một toán tử toán học độc lập.
    \"\"\"
    def __init__(self, num_classes=10):
        super().__init__()
        # f_1: Conv2D 3 -> 32
        self.f1_conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1)
        # f_2: ReLU
        self.f2_relu1 = nn.ReLU()
        # f_3: MaxPool 2x2
        self.f3_pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # f_4: Conv2D 32 -> 64
        self.f4_conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        # f_5: ReLU
        self.f5_relu2 = nn.ReLU()
        # f_6: MaxPool 2x2
        self.f6_pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # f_7: Global Average Pooling (GAP)
        self.f7_gap = nn.AdaptiveAvgPool2d((1, 1))
        
        # f_8: Affine Transformation (Linear Layer)
        self.f8_linear = nn.Linear(in_features=64, out_features=num_classes)
        
        # f_9: Softmax
        self.f9_softmax = nn.Softmax(dim=-1)

    def forward(self, x, verbose=False):
        \"\"\"Lan truyền tiến biểu thị phép hợp hàm: f = f_9 o f_8 o ... o f_1\"\"\"
        if verbose: print(f"[Tầng 0] Đầu vào x: {tuple(x.shape)}")
        
        x = self.f1_conv1(x)
        if verbose: print(f"[f_1: Conv2D]     z1: {tuple(x.shape)}")
        
        x = self.f2_relu1(x)
        if verbose: print(f"[f_2: ReLU]       a1: {tuple(x.shape)}")
        
        x = self.f3_pool1(x)
        if verbose: print(f"[f_3: MaxPool]    p1: {tuple(x.shape)}")
        
        x = self.f4_conv2(x)
        if verbose: print(f"[f_4: Conv2D]     z2: {tuple(x.shape)}")
        
        x = self.f5_relu2(x)
        if verbose: print(f"[f_5: ReLU]       a2: {tuple(x.shape)}")
        
        x = self.f6_pool2(x)
        if verbose: print(f"[f_6: MaxPool]    p2: {tuple(x.shape)}")
        
        x = self.f7_gap(x)
        if verbose: print(f"[f_7: GAP]        v_gap: {tuple(x.shape)}")
        
        # Làm phẳng tensor (B, 64, 1, 1) -> (B, 64)
        v = torch.flatten(x, 1)
        
        z_c = self.f8_linear(v)
        if verbose: print(f"[f_8: Affine]     logits: {tuple(z_c.shape)}")
        
        y_hat = self.f9_softmax(z_c)
        if verbose: print(f"[f_9: Softmax]    y_hat: {tuple(y_hat.shape)}")
        
        return y_hat

# Kiểm tra dòng chảy kích hoạt và tensor shape flow
model_composite = ExplicitCompositeCNN(num_classes=10)
dummy_batch = torch.randn(2, 3, 32, 32)
print("--- THEO DÕI DÒNG CHẢY HÀM HỢP (TENSOR SHAPE FLOW) ---")
output_probs = model_composite(dummy_batch, verbose=True)""")

# 7. Section 6
add_md("""### 6. Thống kê Chi phí Tính toán & Số lượng Tham số của Mạng
Đếm chi tiết số lượng tham số học được trong từng hàm:
* $\\text{Conv}_1$: $(3 \\times 3 \\times 3 + 1) \\times 32 = 28 \\times 32 = 896$ tham số.
* $\\text{Conv}_2$: $(3 \\times 3 \\times 32 + 1) \\times 64 = 289 \\times 64 = 18,496$ tham số.
* $\\text{GAP}$: $0$ tham số (phép toán thống kê không tham số).
* $\\text{Linear Head}$: $(64 + 1) \\times 10 = 650$ tham số.
* **Tổng cộng:** $896 + 18,496 + 650 = 20,042$ tham số.""")

add_code("""def count_parameters(model):
    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Tổng số tham số học được của mạng: {total_params:,}")
    print("-" * 65)
    print(f"{'Tên tầng / Hàm':<25} | {'Shape trọng số':<20} | {'Số tham số':<12}")
    print("-" * 65)
    for name, param in model.named_parameters():
        print(f"{name:<25} | {str(tuple(param.shape)):<20} | {param.numel():<12,}")
    print("-" * 65)
    return total_params

count_parameters(model_composite)""")

# 8. Section 7
add_md("""### 7. Trực quan hóa Bản đồ Đặc trưng Cục bộ (Feature Maps Visualization)
Để kiểm chứng trực quan cơ chế hoạt động của hàm hợp, ta kích hoạt mạng với một ảnh giả lập và trích xuất các bản đồ đặc trưng tại các tầng trung gian.""")

add_code("""synthetic_img = np.zeros((32, 32, 3), dtype=np.float32)
synthetic_img[8:24, 8:24, :] = 1.0
synthetic_img[12:20, 12:20, 0] = 0.5
tensor_img = torch.tensor(synthetic_img).permute(2, 0, 1).unsqueeze(0)

with torch.no_grad():
    feat_stage1 = model_composite.f2_relu1(model_composite.f1_conv1(tensor_img))
    feat_stage2 = model_composite.f5_relu2(model_composite.f4_conv2(model_composite.f3_pool1(feat_stage1)))

fig, axes = plt.subplots(2, 8, figsize=(16, 5.8), dpi=200)
fig.suptitle("Trực quan hóa Bản đồ Đặc trưng Trung gian Trích xuất từ Hàm Hợp CNN", fontsize=13, fontweight="bold", y=0.98, color="#0F172A")
for idx in range(8):
    axes[0, idx].imshow(feat_stage1[0, idx].cpu().numpy(), cmap="viridis")
    axes[0, idx].axis("off")
    axes[0, idx].set_title(f"Tầng 1 - Kênh {idx+1}", fontsize=9.5, fontweight="bold", pad=8, color="#1E293B")
    
    axes[1, idx].imshow(feat_stage2[0, idx].cpu().numpy(), cmap="plasma")
    axes[1, idx].axis("off")
    axes[1, idx].set_title(f"Tầng 2 - Kênh {idx+1}", fontsize=9.5, fontweight="bold", pad=8, color="#1E293B")

plt.subplots_adjust(top=0.88, bottom=0.06, left=0.04, right=0.96, hspace=0.45, wspace=0.18)
plt.savefig("../reports/figures/fig04_intermediate_feature_maps.png", dpi=300, bbox_inches="tight")
plt.show()""")

# 9. Conclusion
add_md("""### 8. Kết luận Phần 1
1. Mạng nơ-ron tích chập (CNN) được biểu diễn chặt chẽ về mặt toán học thông qua **hàm hợp đa tầng** $f = (f_L \\circ \\dots \\circ f_1)$.
2. Mỗi hàm thành phần giải quyết một nhiệm vụ toán học xác định:
   * $f_{\\text{conv}}$: Trích xuất đặc trưng không gian cục bộ qua chia sẻ trọng số và liên kết cục bộ.
   * $\\phi$: Kích hoạt phi tuyến ReLU triệt tiêu bão hòa đạo hàm.
   * $f_{\\text{pool}}$ & $f_{\\text{GAP}}$: Giảm chiều không gian, triệt tiêu số lượng tham số trước tầng phân loại.
3. Toàn bộ mã nguồn trên được tổ chức tự chứa, sẵn sàng để làm nền tảng mở rộng sang Phần 2 (Các kiến trúc phát triển VGG, ResNet, MobileNet).""")

nb = {
    "cells": cells,
    "metadata": {
        "language_info": {
            "name": "python",
            "version": "3.12.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

nb_path = "src/Assigment 05/notebooks/01_cnn_mathematical_functions_and_composite_model.ipynb"
with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=2)

print("Notebook Part 1 generated successfully at:", nb_path)
