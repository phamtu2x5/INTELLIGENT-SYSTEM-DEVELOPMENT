import os
import torch
import torch.nn as nn

class PyTorchCNN(nn.Module):
    def __init__(self):
        super().__init__()
        # Khối trích xuất đặc trưng tích chập (Conv -> BatchNorm -> ReLU -> MaxPool)
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 28x28 -> 14x14
            
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)   # 14x14 -> 7x7
        )
        # Tầng Fully Connected
        self.fc_latent = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, 128),
            nn.ReLU()
        )
        self.dropout = nn.Dropout(0.2)
        self.classifier = nn.Linear(128, 10)
        
    def forward(self, x):
        feat = self.features(x)
        latent = self.fc_latent(feat)
        out = self.classifier(self.dropout(latent))
        return out

_cached_model = None

def get_model(weights_path=None):
    global _cached_model
    if _cached_model is not None:
        return _cached_model

    if weights_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        weights_path = os.path.join(current_dir, '..', 'models', 'mnist_pytorch_cnn.pth')
        
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Không tìm thấy file trọng số tại: {weights_path}")

    model = PyTorchCNN()
    model.load_state_dict(torch.load(weights_path, weights_only=True, map_location='cpu'))
    model.eval()
    _cached_model = model
    return _cached_model
