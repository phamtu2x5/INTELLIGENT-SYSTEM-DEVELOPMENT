import os
import numpy as np
import torch
import torch.nn as nn
import tensorflow as tf

class PyTorchCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
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

def test_inference():
    models_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(models_dir, '..', 'data', 'mnist.npz')
    
    data = np.load(data_path)
    X_test = data['X_test'][:5]
    y_test = data['y_test'][:5]
    
    print("=" * 60)
    print("  KIỂM TRA LOAD MÔ HÌNH VÀ SUY LUẬN TRÊN 5 ẢNH TEST")
    print("=" * 60)
    print(f"Nhãn thực tế (Ground Truth)       : {y_test.tolist()}\n")
    
    # 1. PyTorch Model (via state_dict)
    pt_path = os.path.join(models_dir, 'mnist_pytorch_cnn.pth')
    if os.path.exists(pt_path):
        model_pt = PyTorchCNN()
        model_pt.load_state_dict(torch.load(pt_path, weights_only=True, map_location='cpu'))
        model_pt.eval()
        x_pt = torch.from_numpy((X_test[:, np.newaxis, :, :] / 255.0).astype(np.float32))
        with torch.no_grad():
            preds_pt = model_pt(x_pt).argmax(dim=1).numpy()
        print(f"PyTorch CNN dự đoán (Accuracy: 99.09%): {preds_pt.tolist()} -> Khớp 100%: {np.array_equal(preds_pt, y_test)}")
        
    # 2. Keras Model
    keras_path = os.path.join(models_dir, 'mnist_keras_cnn.keras')
    if os.path.exists(keras_path):
        model_keras = tf.keras.models.load_model(keras_path)
        x_keras = (X_test[:, :, :, np.newaxis] / 255.0).astype(np.float32)
        preds_keras = model_keras.predict(x_keras, verbose=0).argmax(axis=1)
        print(f"Keras CNN dự đoán   (Accuracy: 99.00%): {preds_keras.tolist()} -> Khớp 100%: {np.array_equal(preds_keras, y_test)}")
    print("=" * 60)

if __name__ == '__main__':
    test_inference()
