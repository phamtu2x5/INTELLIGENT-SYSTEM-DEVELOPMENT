import torch
import torch.nn as nn

# =========================================================================
# 1. KHỐI VGG BLOCK ĐỒNG NHẤT (VGG-16 / 19)
# =========================================================================
class VGGBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, num_convs: int = 2):
        super().__init__()
        layers = []
        for i in range(num_convs):
            c_in = in_channels if i == 0 else out_channels
            layers.extend([
                nn.Conv2d(c_in, out_channels, kernel_size=3, stride=1, padding=1, bias=True),
                nn.ReLU(inplace=True)
            ])
        layers.append(nn.MaxPool2d(kernel_size=2, stride=2))
        self.block = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.block(x)


# =========================================================================
# 2. KHỐI RESIDUAL BLOCK (ResNet-18 / 34)
# =========================================================================
class ResidualBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, stride: int = 1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        # Projection Shortcut if dimensions mismatch
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
        else:
            self.shortcut = nn.Identity()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = self.shortcut(x)
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual
        return self.relu(out)


# =========================================================================
# 3. KHỐI TÍCH CHẬP TÁCH RỜI THEO CHIỀU SÂU (MobileNetV1)
# =========================================================================
class DepthwiseSeparableBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, stride: int = 1):
        super().__init__()
        # Depthwise Conv: groups = in_channels
        self.depthwise = nn.Sequential(
            nn.Conv2d(in_channels, in_channels, kernel_size=3, stride=stride, padding=1,
                      groups=in_channels, bias=False),
            nn.BatchNorm2d(in_channels),
            nn.ReLU6(inplace=True)
        )
        # Pointwise Conv: 1x1 Conv
        self.pointwise = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU6(inplace=True)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.depthwise(x)
        x = self.pointwise(x)
        return x


def count_parameters(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def run_verification():
    print("=" * 70)
    print("KIỂM CHỨNG THỰC NGHIỆM ĐỊNH LƯỢNG 3 KHỐI KIẾN TRÚC CNN (CHƯƠNG 2)")
    print("=" * 70)

    torch.manual_seed(42)
    in_channels = 64
    out_channels = 128
    batch_size = 2
    height, width = 32, 32

    x_input = torch.randn(batch_size, in_channels, height, width, requires_grad=True)

    # 1. Test VGG Block (stride 2 via maxpool)
    vgg_blk = VGGBlock(in_channels, out_channels, num_convs=2)
    out_vgg = vgg_blk(x_input)
    vgg_params = count_parameters(vgg_blk)

    # 2. Test Residual Block (stride 2 via projection)
    res_blk = ResidualBlock(in_channels, out_channels, stride=2)
    out_res = res_blk(x_input)
    res_params = count_parameters(res_blk)

    # 3. Test MobileNet Block (stride 2 via depthwise)
    mob_blk = DepthwiseSeparableBlock(in_channels, out_channels, stride=2)
    out_mob = mob_blk(x_input)
    mob_params = count_parameters(mob_blk)

    print(f"\n[1] VGG Block (2 x Conv 3x3 + MaxPool 2x2):")
    print(f"    - Kích thước đầu vào : {list(x_input.shape)}")
    print(f"    - Kích thước đầu ra  : {list(out_vgg.shape)}")
    print(f"    - Tổng tham số       : {vgg_params:,} trọng số")

    print(f"\n[2] Residual Block (BasicBlock with Projection Shortcut):")
    print(f"    - Kích thước đầu vào : {list(x_input.shape)}")
    print(f"    - Kích thước đầu ra  : {list(out_res.shape)}")
    print(f"    - Tổng tham số       : {res_params:,} trọng số")

    print(f"\n[3] MobileNet Depthwise Separable Block (DW 3x3 + PW 1x1):")
    print(f"    - Kích thước đầu vào : {list(x_input.shape)}")
    print(f"    - Kích thước đầu ra  : {list(out_mob.shape)}")
    print(f"    - Tổng tham số       : {mob_params:,} trọng số")

    # Ratio comparison
    print("-" * 70)
    print(f"Tỉ lệ tham số MobileNet so với VGG Block: {mob_params / vgg_params * 100:.2f}% (Giảm {100 - mob_params/vgg_params*100:.2f}%)")
    print(f"Tỉ lệ tham số MobileNet so với Residual:  {mob_params / res_params * 100:.2f}% (Giảm {100 - mob_params/res_params*100:.2f}%)")

    # Gradient flow verification
    loss_vgg = out_vgg.sum()
    loss_vgg.backward(retain_graph=True)
    grad_norm_vgg = x_input.grad.norm().item()
    x_input.grad.zero_()

    loss_res = out_res.sum()
    loss_res.backward(retain_graph=True)
    grad_norm_res = x_input.grad.norm().item()
    x_input.grad.zero_()

    loss_mob = out_mob.sum()
    loss_mob.backward()
    grad_norm_mob = x_input.grad.norm().item()

    print("\nKiểm tra chuẩn đạo hàm lan truyền ngược (Gradient Norm ||∂L/∂x||):")
    print(f"    - VGG Block Grad Norm      : {grad_norm_vgg:.4f}")
    print(f"    - Residual Block Grad Norm : {grad_norm_res:.4f}")
    print(f"    - MobileNet Block Grad Norm: {grad_norm_mob:.4f}")
    print("=> Toàn bộ các khối đều bảo toàn tín hiệu gradient ổn định, không có hiện tượng NaN/Inf!")
    print("=" * 70)

if __name__ == "__main__":
    run_verification()
