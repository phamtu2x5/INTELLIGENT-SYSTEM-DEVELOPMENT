import os
import time
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import tensorflow as tf
from tensorflow.keras import layers, models

# Top-level class definition for clean pickling
class PyTorchCNN(nn.Module):
    def __init__(self):
        super().__init__()
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
        
    def extract_latent(self, x):
        with torch.no_grad():
            feat = self.features(x)
            latent = self.fc_latent(feat)
        return latent

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    data_path = os.path.join(base_dir, 'data', 'mnist.npz')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Cannot find MNIST data at {data_path}")
        
    print(f"Loading MNIST data from {data_path}...")
    data = np.load(data_path)
    X_train_np = (data['X_train'][:, np.newaxis, :, :] / 255.0).astype(np.float32)
    y_train_np = data['y_train'].astype(np.int64)
    X_test_np = (data['X_test'][:, np.newaxis, :, :] / 255.0).astype(np.float32)
    y_test_np = data['y_test'].astype(np.int64)
    
    print(f"Train samples: {len(X_train_np):,}, Test samples: {len(X_test_np):,}")
    
    # -------------------------------------------------------------
    # 1. Train & Save PyTorch CNN
    # -------------------------------------------------------------
    device = torch.device('mps' if torch.backends.mps.is_available() else ('cuda' if torch.cuda.is_available() else 'cpu'))
    print(f"\n[PyTorch] Using device: {device}")
    
    pt_model = PyTorchCNN().to(device)
    criterion_pt = nn.CrossEntropyLoss()
    optimizer_pt = optim.Adam(pt_model.parameters(), lr=0.001)
    
    train_loader = DataLoader(
        TensorDataset(torch.from_numpy(X_train_np), torch.from_numpy(y_train_np)),
        batch_size=128,
        shuffle=True
    )
    test_loader = DataLoader(
        TensorDataset(torch.from_numpy(X_test_np), torch.from_numpy(y_test_np)),
        batch_size=256,
        shuffle=False
    )
    
    epochs = 5
    print(f"[PyTorch] Training for {epochs} epochs...")
    t0 = time.time()
    for ep in range(epochs):
        pt_model.train()
        total_loss, correct, total = 0.0, 0, 0
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer_pt.zero_grad()
            out = pt_model(xb)
            loss = criterion_pt(out, yb)
            loss.backward()
            optimizer_pt.step()
            
            total_loss += loss.item() * len(yb)
            correct += (out.argmax(1) == yb).sum().item()
            total += len(yb)
        print(f"  Epoch {ep+1}/{epochs}: Loss = {total_loss/total:.4f}, Acc = {correct/total*100:.2f}%")
        
    pt_model.eval()
    test_correct = 0
    with torch.no_grad():
        for xb, yb in test_loader:
            xb, yb = xb.to(device), yb.to(device)
            out = pt_model(xb)
            test_correct += (out.argmax(1) == yb).sum().item()
    test_acc_pt = test_correct / len(y_test_np) * 100
    print(f"[PyTorch] Test Accuracy: {test_acc_pt:.2f}% (Trained in {time.time()-t0:.2f}s)")
    
    pt_pth_path = os.path.join(models_dir, 'mnist_pytorch_cnn.pth')
    pt_full_path = os.path.join(models_dir, 'mnist_pytorch_cnn_full.pt')
    torch.save(pt_model.state_dict(), pt_pth_path)
    torch.save(pt_model, pt_full_path)
    print(f"✓ Saved PyTorch state_dict: {pt_pth_path}")
    print(f"✓ Saved PyTorch full model: {pt_full_path}")
    
    # -------------------------------------------------------------
    # 2. Train & Save Keras CNN
    # -------------------------------------------------------------
    print(f"\n[Keras/TensorFlow] Building and training Keras CNN...")
    X_train_tf = X_train_np.transpose(0, 2, 3, 1)
    X_test_tf = X_test_np.transpose(0, 2, 3, 1)
    
    keras_model = models.Sequential([
        layers.Input(shape=(28, 28, 1)),
        layers.Conv2D(16, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        
        layers.Flatten(),
        layers.Dense(128, activation='relu', name='latent_features'),
        layers.Dropout(0.2),
        layers.Dense(10, activation='softmax')
    ])
    
    keras_model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    t0_tf = time.time()
    keras_model.fit(
        X_train_tf, y_train_np,
        epochs=5,
        batch_size=128,
        verbose=1,
        validation_data=(X_test_tf, y_test_np)
    )
    test_loss_tf, test_acc_tf = keras_model.evaluate(X_test_tf, y_test_np, verbose=0)
    print(f"[Keras] Test Accuracy: {test_acc_tf*100:.2f}% (Trained in {time.time()-t0_tf:.2f}s)")
    
    keras_path = os.path.join(models_dir, 'mnist_keras_cnn.keras')
    keras_model.save(keras_path)
    print(f"✓ Saved Keras model: {keras_path}")
    
    print("\nAll models trained and saved successfully into 'src/Assigment 04/mnist/models/'!")

if __name__ == '__main__':
    main()
