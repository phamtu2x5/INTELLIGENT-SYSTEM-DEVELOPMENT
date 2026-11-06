import os
import torch
import torch.nn as nn
import numpy as np
torch.set_num_threads(1)

class PyTorchRNN(nn.Module):
    def __init__(self, cell_type, input_dim=8, hidden_dim=64, output_dim=1, num_layers=1, bidirectional=False):
        super().__init__()
        self.cell_type = cell_type
        self.bidirectional = bidirectional
        num_directions = 2 if bidirectional else 1
        
        if cell_type == 'rnn':
            self.rnn = nn.RNN(input_dim, hidden_dim, num_layers=num_layers, batch_first=True)
        elif cell_type == 'lstm':
            self.rnn = nn.LSTM(input_dim, hidden_dim, num_layers=num_layers, batch_first=True, bidirectional=bidirectional)
        elif cell_type == 'gru':
            self.rnn = nn.GRU(input_dim, hidden_dim, num_layers=num_layers, batch_first=True, bidirectional=bidirectional)
            
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim * num_directions, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim)
        )
        
    def forward(self, x):
        out, _ = self.rnn(x)
        last_hidden = out[:, -1, :]
        return self.fc(last_hidden)

_loaded_models = {}

def get_stock_model(model_name='lstm'):
    key = f"stock_{model_name}"
    if key in _loaded_models:
        return _loaded_models[key]
        
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_dir, '..', 'models')
    
    bi = (model_name == 'bilstm')
    c_type = 'lstm' if 'lstm' in model_name else ('gru' if 'gru' in model_name else 'rnn')
    model = PyTorchRNN(cell_type=c_type, input_dim=8, hidden_dim=64, output_dim=1, bidirectional=bi)
    
    ckpt_path = os.path.join(model_dir, f"pytorch_amzn_{model_name}.pth")
    if os.path.exists(ckpt_path):
        model.load_state_dict(torch.load(ckpt_path, weights_only=True, map_location='cpu'))
    model.eval()
    _loaded_models[key] = model
    return model

def get_customer_model(model_name='lstm'):
    key = f"cust_{model_name}"
    if key in _loaded_models:
        return _loaded_models[key]
        
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_dir, '..', 'models')
    
    bi = (model_name == 'bilstm')
    c_type = 'lstm' if 'lstm' in model_name else ('gru' if 'gru' in model_name else 'rnn')
    model = PyTorchRNN(cell_type=c_type, input_dim=8, hidden_dim=64, output_dim=2, bidirectional=bi)
    
    ckpt_path = os.path.join(model_dir, f"pytorch_cust_{model_name}.pth")
    if os.path.exists(ckpt_path):
        model.load_state_dict(torch.load(ckpt_path, weights_only=True, map_location='cpu'))
    model.eval()
    _loaded_models[key] = model
    return model
