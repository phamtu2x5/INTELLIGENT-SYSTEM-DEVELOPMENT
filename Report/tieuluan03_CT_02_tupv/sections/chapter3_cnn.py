# sections/chapter3_cnn.py

def get_chapter3():
    return r"""
% =========================================================================
% CHƯƠNG 3: MẠNG NƠ-RON TÍCH CHẬP (CONVOLUTIONAL NEURAL NETWORKS)
% =========================================================================
\chapter{Mạng Nơ-ron Tích Chập (CNN)}

\section{Cơ Sở Lý Thuyết Mạng Nơ-ron Tích Chập \& Biểu Diễn Không Gian}

Mạng nơ-ron đa tầng truyền thống (MLP) gặp phải hai hạn chế chí mạng khi xử lý dữ liệu hình ảnh 2 chiều:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Bùng nổ tham số tính toán:} Nếu duỗi phẳng (flatten) một ảnh màu kích thước khiêm tốn $224 \times 224 \times 3$ thành vector $150,528$ chiều, một tầng ẩn đầu tiên chỉ với $1,024$ nơ-ron sẽ đòi hỏi hơn $154$ triệu tham số trọng số, dẫn đến hiện tượng quá khớp (overfitting) trầm trọng và bất khả thi về bộ nhớ phần cứng.
    \item \textbf{Phá hủy cấu trúc topo không gian:} Việc chuyển đổi ma trận 2D thành vector 1D làm mất hoàn toàn mối tương quan không gian lân cận (spatial locality) giữa các điểm ảnh kề cận.
\end{enumerate}

Mạng nơ-ron Tích chập (Convolutional Neural Networks -- CNN) giải quyết triệt để vấn đề này bằng cách tận dụng tính bất biến tịnh tiến (translation invariance) và tính cục bộ thông qua ba nguyên lý kiến trúc: Vùng tiếp nhận cục bộ (Local Receptive Fields), Chia sẻ trọng số (Weight Sharing) và Lấy mẫu giảm dần (Spatial Pooling).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{images/fig00_image_matrix_and_tensor_representation.png}
    \caption{Biểu diễn ảnh số từ Ma trận Pixel rời rạc đến Tensor 3D/4D trong không gian tính toán học sâu.}
    \label{fig:cnn_image_tensor}
\end{figure}

\subsection{Toán Học Phép Toán Tích Chập 2 Chiều (2D Convolution)}
Trong học sâu, phép toán tích chập thực chất là phép toán tương quan chéo (cross-correlation). Cho một tensor đầu vào $\mathbf{X} \in \mathbb{R}^{C_{\text{in}} \times H \times W}$ và một tập hợp gồm $C_{\text{out}}$ bộ lọc (filters/kernels) $\mathbf{K} \in \mathbb{R}^{C_{\text{out}} \times C_{\text{in}} \times k_h \times k_w}$, giá trị tại vị trí $(i, j)$ của bản đồ đặc trưng đầu ra (feature map) thuộc kênh thứ $c$ được xác định bởi:
\begin{equation}
\mathbf{Y}_{c, i, j} = \sum_{m=1}^{C_{\text{in}}} \sum_{u=0}^{k_h - 1} \sum_{v=0}^{k_w - 1} \mathbf{X}_{m, \, i \cdot s + u, \, j \cdot s + v} \cdot \mathbf{K}_{c, m, u, v} + b_c
\end{equation}
trong đó $s$ là bước trượt (stride), và $b_c$ là bias của bộ lọc thứ $c$. Kích thước không gian của bản đồ đặc trưng đầu ra phụ thuộc vào kích thước đầu vào $(H, W)$, kích thước bộ lọc $(k_h, k_w)$, đệm số không (padding $p$) và bước trượt $s$:
\begin{equation}
H_{\text{out}} = \left\lfloor \frac{H - k_h + 2p}{s} \right\rfloor + 1, \qquad W_{\text{out}} = \left\lfloor \frac{W - k_w + 2p}{s} \right\rfloor + 1
\end{equation}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.95\textwidth]{images/fig06_numerical_convolution_step_by_step.png}
    \caption{Minh họa số học chi tiết từng bước trượt của phép toán tích chập 2D trên ma trận điểm ảnh.}
    \label{fig:cnn_conv_numeric}
\end{figure}

\subsection{Vùng Cảm Nhận (Receptive Field) và Phép Gộp (Pooling)}
Vùng cảm nhận (Receptive Field -- RF) là kích thước vùng không gian trên ảnh đầu vào mà một nơ-ron ở tầng sâu có thể “quan sát” được. Khi xếp chồng liên tiếp các tầng tích chập nhỏ $k \times k$ với bước trượt $s=1$, vùng cảm nhận hiệu dụng $RF_l$ tại tầng $l$ tăng tuyến tính:
\begin{equation}
RF_l = RF_{l-1} + (k_l - 1) \cdot \prod_{i=1}^{l-1} s_i
\end{equation}
Nguyên lý này là nền tảng của kiến trúc VGG: thay vì dùng một bộ lọc lớn $5 \times 5$ (đòi hỏi $25$ trọng số), việc xếp chồng 2 tầng $3 \times 3$ liên tiếp cho cùng một vùng cảm nhận $5 \times 5$ nhưng chỉ tiêu tốn $2 \times (3 \times 3) = 18$ trọng số (giảm $28\%$ tham số) và tăng gấp đôi số hàm phi tuyến ReLU.

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{images/fig07_receptive_field_stacking.png}
    \caption{Cơ chế tích lũy vùng cảm nhận (Receptive Field) khi xếp chồng các bộ lọc tích chập nhỏ.}
    \label{fig:cnn_rf}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{images/fig03_pooling_and_gap_comparison.png}
    \caption{So sánh cơ chế hoạt động của Max Pooling, Average Pooling và Global Average Pooling (GAP).}
    \label{fig:cnn_pooling}
\end{figure}

Phép gộp (Spatial Pooling) thực hiện lấy mẫu giảm kích thước không gian nhằm tăng tính bất biến trước các biến đổi co dãn, dịch chuyển nhỏ, đồng thời mở rộng nhanh vùng cảm nhận cho các tầng tiếp theo:
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Max Pooling:} Chọn giá trị cực đại trong vùng cửa sổ, giữ lại các đặc trưng biên và vân bề mặt có cường độ kích hoạt mạnh nhất.
    \item \textbf{Global Average Pooling (GAP) (Lin et al., 2013):} Tính trung bình cộng toàn bộ không gian của mỗi bản đồ đặc trưng, biến tensor $\mathbb{R}^{C \times H \times W}$ trực tiếp thành vector $\mathbb{R}^C$. GAP loại bỏ hoàn toàn các tầng kết nối đầy đủ (Dense layers) cồng kềnh, giảm hàng chục triệu tham số và chống quá khớp triệt để.
\end{itemize}

\subsection{Tiến Hóa Kiến Trúc: VGG, ResNet và MobileNet}

\begin{figure}[H]
    \centering
    \includegraphics[width=\textwidth]{images/fig201_cnn_evolution_blocks.png}
    \caption{Sơ đồ tiến hóa kiến trúc CNN: Từ khối tích chập phẳng đến khối Residual (ResNet) và Tích chập tách biệt chiều sâu (MobileNet).}
    \label{fig:cnn_blocks_evolution}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.90\textwidth]{images/fig202_vgg_block_and_receptive_field.png}
    \caption{Kiến trúc khối VGG Block và cơ chế tương đương vùng cảm nhận của các bộ lọc $3 \times 3$.}
    \label{fig:cnn_vgg_block}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.90\textwidth]{images/fig203_resnet_residual_block_and_gradient.png}
    \caption{Kiến trúc khối phần dư Residual Block (ResNet) và cơ chế “đường cao tốc” dòng gradient.}
    \label{fig:cnn_resnet_block}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.90\textwidth]{images/fig204_mobilenet_depthwise_separable.png}
    \caption{Kiến trúc Depthwise Separable Convolution trong MobileNet: Tách biệt hoàn toàn không gian và kênh màu.}
    \label{fig:cnn_mobilenet_block}
\end{figure}

\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Khối Residual (ResNet - He et al., 2015):} Giải quyết hiện tượng thoái hóa mạng sâu bằng kết nối tắt: $\mathbf{y} = \mathcal{F}(\mathbf{x}) + \mathbf{x}$. Đạo hàm theo quy tắc dây chuyền:
    \begin{equation}
    \frac{\partial \mathcal{E}}{\partial \mathbf{x}} = \frac{\partial \mathcal{E}}{\partial \mathbf{y}} \left( \frac{\partial \mathcal{F}}{\partial \mathbf{x}} + \mathbf{I} \right)
    \end{equation}
    Thành phần ma trận đơn vị $\mathbf{I}$ đảm bảo gradient luôn có một “đường cao tốc” truyền thẳng về các tầng đầu tiên mà không bao giờ bị triệt tiêu về 0, ngay cả khi các trọng số của $\mathcal{F}$ tiến về 0.
    \item \textbf{Depthwise Separable Convolution (MobileNet - Howard et al., 2017):} Phân rã phép tích chập chuẩn:
    \begin{enumerate}
        \item \textit{Depthwise Conv:} Áp dụng 1 bộ lọc $k \times k$ cho mỗi kênh đầu vào độc lập: Chi phí $C_{\text{in}} \cdot H \cdot W \cdot k^2$.
        \item \textit{Pointwise Conv:} Áp dụng $C_{\text{out}}$ bộ lọc $1 \times 1 \times C_{\text{in}}$ để kết hợp tuyến tính các kênh: Chi phí $C_{\text{in}} \cdot C_{\text{out}} \cdot H \cdot W$.
    \end{enumerate}
    Tỷ lệ chi phí tính toán so với tích chập tiêu chuẩn là:
    \begin{equation}
    \frac{\text{Chi phí MobileNet}}{\text{Chi phí Standard Conv}} = \frac{C_{\text{in}} \cdot H \cdot W \cdot k^2 + C_{\text{in}} \cdot C_{\text{out}} \cdot H \cdot W}{C_{\text{in}} \cdot C_{\text{out}} \cdot H \cdot W \cdot k^2} = \frac{1}{C_{\text{out}}} + \frac{1}{k^2}
    \end{equation}
    Với bộ lọc $3 \times 3$ ($k=3$), chi phí tính toán FLOPs giảm khoảng $\frac{1}{9} \approx 88.9\%$, cho phép các mô hình thị giác chạy thời gian thực trên vi xử lý điện thoại thông minh.
\end{itemize}

\section{Khảo Sát Thực Nghiệm và Tiền Xử Lý 3 Bộ Dữ Liệu Đa Miền}

\subsection{Tập Dữ Liệu 1: Nhận Dạng Chữ Số Nhà SVHN (Street View House Numbers)}
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Nguồn gốc dữ liệu:} Tập dữ liệu ảnh số Stanford SVHN thu thập từ ảnh chụp đời thực Google Street View (\url{http://ufldl.stanford.edu/housenumbers/}).
    \item \textbf{Quy mô và kích thước:} Gồm $73,257$ ảnh huấn luyện và $26,032$ ảnh kiểm thử (tổng cộng $99,289$ ảnh), kích thước chuẩn $32 \times 32 \times 3$ điểm ảnh màu RGB, thuộc 10 lớp chữ số từ $0$ đến $9$.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.90\textwidth]{images/fig404_svhn_sample_grid.png}
    \caption{Lưới mẫu ảnh thực tế từ tập dữ liệu SVHN thể hiện tính đa dạng về ánh sáng, phông nền và biến dạng.}
    \label{fig:svhn_grid}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig405_svhn_class_distribution.png}
    \caption{Phân bố số lượng mẫu theo 10 phân lớp chữ số trong tập dữ liệu SVHN.}
    \label{fig:svhn_dist}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig406_svhn_rgb_channel_histograms.png}
    \caption{Lược đồ phân bố cường độ điểm ảnh trên 3 kênh màu Red, Green, Blue của tập dữ liệu SVHN.}
    \label{fig:svhn_hist}
\end{figure}

\noindent \textbf{Nhận xét EDA:} Khác với ảnh viết tay đen trắng lý tưởng như MNIST, ảnh SVHN chứa nhiễu nền thực tế rất mạnh (gạch, tường, viền kim loại), nhiều ký tự bị nghiêng hoặc che khuất một phần. Quy trình tiền xử lý đòi hỏi chuẩn hóa Z-score độc lập trên từng kênh màu: $\mu = [0.4377, 0.4438, 0.4728]$, $\sigma = [0.1980, 0.2010, 0.1970]$ kết hợp tăng cường dữ liệu bằng phép dịch chuyển ngẫu nhiên (Random Crop) và biến đổi màu (Color Jitter).

\subsection{Tập Dữ Liệu 2: Phân Loại Ảnh Vệ Tinh Viễn Thám EuroSAT (Land Cover)}
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Nguồn gốc dữ liệu:} Bộ dữ liệu viễn thám EuroSAT thu nhận từ vệ tinh Sentinel-2 của Cơ quan Vũ trụ Châu Âu (ESA) (\url{https://github.com/phelber/eurosat}).
    \item \textbf{Quy mô và kích thước:} Gồm $27,000$ ảnh quang phổ độ phân giải $64 \times 64 \times 3$ điểm ảnh, phân chia hoàn hảo vào 10 lớp mục tiêu sử dụng đất: Rừng rậm (Forest), Sông hồ (River), Đồng ruộng hoa màu (Annual Crop), Khu dân cư (Residential), Khu công nghiệp (Industrial), Đồng cỏ (Pasture), v.v.
\end{itemize}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.90\textwidth]{images/fig407_eurosat_sample_grid.png}
    \caption{Lưới mẫu ảnh viễn thám vệ tinh EuroSAT thuộc 10 phân lớp sử dụng đất khác nhau.}
    \label{fig:eurosat_grid}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig408_eurosat_class_distribution.png}
    \caption{Phân bố số lượng mẫu hoàn toàn cân bằng giữa 10 phân lớp trong tập dữ liệu EuroSAT.}
    \label{fig:eurosat_dist}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig409_eurosat_rgb_spectral_histograms.png}
    \caption{Lược đồ phản xạ quang phổ kênh màu RGB thể hiện đặc trưng sinh thái của ảnh vệ tinh EuroSAT.}
    \label{fig:eurosat_hist}
\end{figure}

\noindent \textbf{Nhận xét EDA:} EuroSAT có phân bố lớp cân bằng tuyệt đối ($2,000$ đến $3,000$ ảnh/lớp). Đặc trưng của ảnh vệ tinh là tính bất biến phương hướng (ảnh chụp từ trên đỉnh đầu nhìn xuống không có khái niệm trên/dưới), do đó các kỹ thuật tăng cường dữ liệu xoay $90^\circ, 180^\circ, 270^\circ$ và lật gương hai chiều (Horizontal/Vertical Flip) đem lại hiệu quả cải thiện năng lực tổng quát hóa vượt bậc.

\subsection{Tập Dữ Liệu 3: Chuỗi Đặc Trưng Y Sinh 1D CNN (Diabetes Sequence)}
Ngoài dữ liệu ảnh 2D, chúng tôi khảo sát ứng dụng của \textbf{1D CNN} trên tập dữ liệu lâm sàng y tế (100,000 mẫu tiểu đường). Bằng cách sắp xếp các chỉ số sinh hóa theo thứ tự tương quan sinh học thành tensor 1D $[B, 1, 8]$, bộ lọc tích chập 1D kích thước hạt nhân $1 \times 3$ có khả năng tự động trích xuất các tổ hợp đặc trưng cục bộ (ví dụ: tương tác giữa BMI, Glucose và HbA1c) mà không làm tăng số lượng tham số như mạng MLP truyền thống.

\section{Hiện Thực Hóa Mã Nguồn Trên 3 Nền Tảng (Scratch, Keras, PyTorch)}

\subsection{Hiện Thực Hóa Tích Chập 2D Scratch Bằng NumPy}
Đoạn mã~\ref{lst:conv2d_scratch} hiện thực hóa phép toán tích chập 2D đa kênh và Max Pooling từ nguyên lý toán học thuần túy.

\begin{lstlisting}[language=Python, caption={Hiện thực hóa phép toán Tích chập 2D và Max Pooling từ Scratch bằng NumPy}, label={lst:conv2d_scratch}]
import numpy as np

def conv2d_forward_scratch(X, W, b, stride=1, padding=0):
    # X: Tensor dau vao [N, C_in, H, W]
    # W: Trong so bo loc [C_out, C_in, k_h, k_w]
    # b: Vector bias [C_out]
    N, C_in, H, W = X.shape
    C_out, _, k_h, k_w = W.shape
    
    # Dem so khong (Zero-padding)
    if padding > 0:
        X_pad = np.pad(X, ((0,0), (0,0), (padding, padding), (padding, padding)), mode='constant')
    else:
        X_pad = X
        
    H_pad, W_pad = X_pad.shape[2], X_pad.shape[3]
    H_out = (H_pad - k_h) // stride + 1
    W_out = (W_pad - k_w) // stride + 1
    out = np.zeros((N, C_out, H_out, W_out))
    
    for i in range(H_out):
        for j in range(W_out):
            h_start = i * stride
            h_end = h_start + k_h
            w_start = j * stride
            w_end = w_start + k_w
            
            # Trich xuat vung cua so
            slice_X = X_pad[:, :, h_start:h_end, w_start:w_end] # [N, C_in, k_h, k_w]
            
            for c in range(C_out):
                # Nhan chap vo huong va cong bias
                out[:, c, i, j] = np.sum(slice_X * W[c, :, :, :], axis=(1, 2, 3)) + b[c]
                
    return out

def maxpool2d_forward_scratch(X, pool_size=2, stride=2):
    N, C, H, W = X.shape
    H_out = (H - pool_size) // stride + 1
    W_out = (W - pool_size) // stride + 1
    out = np.zeros((N, C, H_out, W_out))
    
    for i in range(H_out):
        for j in range(W_out):
            h_start, h_end = i * stride, i * stride + pool_size
            w_start, w_end = j * stride, j * stride + pool_size
            slice_X = X[:, :, h_start:h_end, w_start:w_end]
            out[:, :, i, j] = np.max(slice_X, axis=(2, 3))
    return out
\end{lstlisting}

\subsection{Hiện Thực Hóa Mạng Custom CNN và Khối Tích Chập Kiểu VGG Bằng Keras / TensorFlow}
Đoạn mã~\ref{lst:cnn_keras} xây dựng mạng CNN với Keras kết hợp khối tích chập lặp theo phong cách VGG Block và Global Average Pooling thay vì Flatten.

\begin{lstlisting}[language=Python, caption={Hiện thực hóa mạng Custom CNN và khối tích chập kiểu VGG bằng Keras}, label={lst:cnn_keras}]
import tensorflow as tf
from tensorflow.keras import layers, models

def build_vgg_block(x, filters, num_convs):
    # Khoi VGG dac trung: cac tang Conv2D 3x3 xep chong kem MaxPooling
    for _ in range(num_convs):
        x = layers.Conv2D(filters, (3, 3), padding='same', activation='relu')(x)
        x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2), strides=(2, 2))(x)
    return x

def build_keras_custom_cnn(input_shape=(32, 32, 3), num_classes=10):
    inputs = layers.Input(shape=input_shape)
    
    # Khoi tich chap 1 (2 tang Conv 3x3 kieu VGG)
    x = build_vgg_block(inputs, filters=32, num_convs=2)
    x = layers.Dropout(0.2)(x)
    
    # Khoi tich chap 2 (2 tang Conv 3x3 kieu VGG)
    x = build_vgg_block(x, filters=64, num_convs=2)
    x = layers.Dropout(0.3)(x)
    
    # GAP thay the hoan toan Dense cong kenh chong qua khop
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.4)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = models.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model
\end{lstlisting}

\subsection{Hiện Thực Hóa Khối Nơ-ron Kiểu MobileNetV2 Bằng PyTorch}
Đoạn mã~\ref{lst:mobilenet_pytorch} hiện thực hóa khối nơ-ron cốt lõi \texttt{InvertedResidualBlock} theo nguyên lý thiết kế của MobileNetV2, kết hợp phép tích chập tách biệt chiều sâu (Depthwise Separable Convolution) và kết nối tắt phần dư tuyến tính (Linear Bottleneck).

\begin{lstlisting}[language=Python, caption={Hiện thực hóa khối Inverted Residual kiểu MobileNetV2 trong PyTorch}, label={lst:mobilenet_pytorch}]
import torch
import torch.nn as nn

class InvertedResidualBlock(nn.Module):
    # Khoi Inverted Residual: 1x1 Expansion -> 3x3 Depthwise -> 1x1 Linear Projection
    def __init__(self, in_c, out_c, stride=1, expand_ratio=6):
        super(InvertedResidualBlock, self).__init__()
        self.use_residual = (stride == 1 and in_c == out_c)
        hidden_dim = int(in_c * expand_ratio)
        layers_list = []
        
        # 1. Pointwise Expansion (1x1 Conv) mo rong kenh
        if expand_ratio != 1:
            layers_list.extend([
                nn.Conv2d(in_c, hidden_dim, kernel_size=1, bias=False),
                nn.BatchNorm2d(hidden_dim),
                nn.ReLU6(inplace=True)
            ])
            
        # 2. Depthwise Convolution (3x3 Conv voi groups=hidden_dim)
        layers_list.extend([
            nn.Conv2d(hidden_dim, hidden_dim, kernel_size=3, stride=stride, padding=1, 
                      groups=hidden_dim, bias=False),
            nn.BatchNorm2d(hidden_dim),
            nn.ReLU6(inplace=True)
        ])
        
        # 3. Pointwise Linear Projection (1x1 Conv - khong dung kich hoat phi tuyen)
        layers_list.extend([
            nn.Conv2d(hidden_dim, out_c, kernel_size=1, bias=False),
            nn.BatchNorm2d(out_c)
        ])
        self.conv = nn.Sequential(*layers_list)
        
    def forward(self, x):
        if self.use_residual:
            return x + self.conv(x) # Ket noi tat shortcut cong truc tiep
        return self.conv(x)
\end{lstlisting}

\subsection{Hiện Thực Hóa Kiến Trúc Mạng Kiểu ResNet-18 Bằng PyTorch}
Đoạn mã~\ref{lst:resnet_pytorch} hiện thực hóa mạng tích chập theo phong cách ResNet-18 với khối \texttt{ResidualBlock} tự định nghĩa từ đầu trong PyTorch.

\begin{lstlisting}[language=Python, caption={Hiện thực hóa kiến trúc kiểu ResNet-18 với khối Residual Block trong PyTorch}, label={lst:resnet_pytorch}]
import torch
import torch.nn as nn

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        # Ket noi tat (Shortcut) neu kich thuoc khong gian hoac so kenh thay doi
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
            
    def forward(self, x):
        residual = self.shortcut(x)
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual # Duong cao toc cong truc tiep
        return self.relu(out)

class ResNet18(nn.Module):
    def __init__(self, num_classes=10):
        super(ResNet18, self).__init__()
        self.in_channels = 64
        self.stem = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)
        )
        self.layer1 = self._make_layer(64, 2, stride=1)
        self.layer2 = self._make_layer(128, 2, stride=2)
        self.layer3 = self._make_layer(256, 2, stride=2)
        self.layer4 = self._make_layer(512, 2, stride=2)
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)
        
    def _make_layer(self, out_channels, num_blocks, stride):
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for s in strides:
            layers.append(ResidualBlock(self.in_channels, out_channels, s))
            self.in_channels = out_channels
        return nn.Sequential(*layers)
        
    def forward(self, x):
        x = self.stem(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avg_pool(x)
        x = torch.flatten(x, 1)
        return self.fc(x)
\end{lstlisting}

\section{Đánh Giá và Đối Chuẩn Các Biến Thể Kiến Trúc CNN Trên Các Tập Dữ Liệu}

\noindent \textbf{Phương pháp luận thực nghiệm và cấu hình kiến trúc:}
Nhằm phục vụ mục đích nghiên cứu học thuật và đánh giá khách quan đặc tính hội tụ của từng trường phái thiết kế mạng, toàn bộ các mô hình trong thực nghiệm này được \textbf{hiện thực hóa theo phong cách kiến trúc đặc trưng} (khối Residual kiểu ResNet, khối Inverted Residual kiểu MobileNet, và khối xếp chồng tuần tự kiểu VGG). Các mô hình được cấu hình thích ứng với độ phân giải ảnh thực tế ($32 \times 32$ trên SVHN và $64 \times 64$ trên EuroSAT, với 10 lớp đầu ra) và được \textbf{huấn luyện hoàn toàn từ đầu (Train from Scratch với trọng số ngẫu nhiên)}.

Báo cáo chủ ý không sử dụng toàn bộ mô hình nền tảng lớn được tiền huấn luyện sẵn (Pretrained Foundation Models trên 1.2 triệu ảnh ImageNet kích thước $224 \times 224$) để tránh việc mô hình được hưởng lợi từ tri thức học trước, qua đó phản ánh trung thực năng lực trích xuất đặc trưng thuần túy của từng cấu trúc hình học mạng trên dữ liệu mục tiêu. Bốn biến thể kiến trúc đối chuẩn bao gồm:
\begin{enumerate}[leftmargin=1.2cm]
    \item \textbf{Custom CNN (Baseline):} Kiến trúc 4 tầng tích chập phẳng kết hợp Global Average Pooling ($0.35$ triệu tham số).
    \item \textbf{Kiến trúc kiểu VGG-11 (VGG-style):} Cấu trúc mạng tuần tự sâu gồm các khối Conv $3 \times 3$ lặp lại ($9.36$ triệu tham số).
    \item \textbf{Kiến trúc kiểu MobileNetV2 (MobileNet-style):} Cấu trúc nơ-ron di động siêu nhẹ tối ưu hóa bằng Inverted Residual và Depthwise Separable Conv ($2.24$ triệu tham số).
    \item \textbf{Kiến trúc kiểu ResNet-18 (ResNet-style):} Cấu trúc nơ-ron phần dư sâu 18 tầng với các khối Residual Block chống triệt tiêu gradient ($11.18$ triệu tham số).
\end{enumerate}

\begin{table}[H]
\centering
\small
\caption{Bảng đối chuẩn đa chiều giữa các biến thể kiến trúc CNN (huấn luyện từ đầu -- Train from Scratch) trên tập dữ liệu SVHN và EuroSAT}
\label{tab:cnn_benchmark_master}
\begin{tabularx}{\textwidth}{l l >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X >{\centering\arraybackslash}X}
\toprule
\textbf{Tập Dữ Liệu} & \textbf{Biến Thể Kiến Trúc} & \textbf{Acc (\%)} & \textbf{Tham Số (M)} & \textbf{FLOPs (G)} & \textbf{Độ Trễ (ms)} & \textbf{FPS} \\
\midrule
\multirow{4}{*}{\textbf{SVHN}} 
& Custom CNN (Baseline) & 91.45 & 0.35 & 0.08 & 4.2 & 238 \\
& Kiểu VGG-11 (VGG-style) & 93.80 & 9.36 & 0.15 & 9.4 & 106 \\
& Kiểu MobileNetV2 (MobileNet-style) & 94.20 & 2.24 & 0.31 & 6.8 & 147 \\
& \textbf{Kiểu ResNet-18 (ResNet-style)} & \textbf{95.82} & \textbf{11.18} & \textbf{1.12} & \textbf{14.5} & \textbf{69} \\
\midrule
\multirow{4}{*}{\textbf{EuroSAT}} 
& Custom CNN (Baseline) & 92.10 & 0.35 & 0.32 & 5.1 & 196 \\
& Kiểu VGG-11 (VGG-style) & 94.75 & 9.36 & 0.61 & 12.8 & 78 \\
& Kiểu MobileNetV2 (MobileNet-style) & 96.85 & 2.24 & 0.65 & 8.5 & 118 \\
& \textbf{Kiểu ResNet-18 (ResNet-style)} & \textbf{98.40} & \textbf{11.18} & \textbf{2.25} & \textbf{18.2} & \textbf{55} \\
\midrule
\textbf{Diabetes 1D} 
& \textbf{1D CNN (Conv1D)} & \textbf{95.25} & \textbf{0.04} & \textbf{0.005} & \textbf{0.8} & \textbf{1,250} \\
\bottomrule
\end{tabularx}
\end{table}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig503_svhn_learning_curves_comparison.png}
    \caption{Đường cong hàm mất mát và độ chính xác trong quá trình huấn luyện từ đầu (from-scratch) so sánh 4 biến thể kiến trúc trên tập dữ liệu SVHN.}
    \label{fig:svhn_curves}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig504_svhn_resnet18_confusion_matrix.png}
    \caption{Ma trận nhầm lẫn của biến thể kiến trúc kiểu ResNet-18 huấn luyện trên tập kiểm thử SVHN.}
    \label{fig:svhn_cfm}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig505_eurosat_learning_curves_comparison.png}
    \caption{Đường cong học tập so sánh tốc độ hội tụ từ đầu của 4 biến thể kiến trúc trên tập dữ liệu viễn thám EuroSAT.}
    \label{fig:eurosat_curves}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig506_eurosat_resnet18_confusion_matrix.png}
    \caption{Ma trận nhầm lẫn của biến thể kiến trúc kiểu ResNet-18 trên tập kiểm thử EuroSAT (Độ chính xác ấn tượng 98.40\%).}
    \label{fig:eurosat_cfm}
\end{figure}

\begin{figure}[H]
    \centering
    \includegraphics[width=0.88\textwidth]{images/fig508_latency_and_fps_benchmark.png}
    \caption{Đối chuẩn tốc độ suy luận thực tế (Latency tính bằng mili-giây và Thông lượng FPS) của 4 biến thể kiến trúc trên phần cứng.}
    \label{fig:cnn_latency}
\end{figure}

\noindent \textbf{Phân tích đánh đổi thiết kế (Trade-off Analysis):}
\begin{itemize}[leftmargin=1.2cm]
    \item \textbf{Hiệu năng tuyệt đối của biến thể kiểu ResNet-18:} Trên cả hai miền dữ liệu, kiến trúc kiểu ResNet-18 xác lập đỉnh cao về độ chính xác: đạt $95.82\%$ trên SVHN và $98.40\%$ trên EuroSAT. Cơ chế Residual Block cho phép trích xuất các đặc trưng ngữ nghĩa phân cấp cực kỳ trừu tượng mà không gặp hiện tượng bão hòa gradient.
    \item \textbf{Ưu thế triển khai thực tế của biến thể kiểu MobileNetV2:} Kết quả đối chuẩn tại Hình~\ref{fig:cnn_latency} và Bảng~\ref{tab:cnn_benchmark_master} chứng minh kiến trúc kiểu MobileNetV2 là lựa chọn tối ưu cho bài toán triển khai thực tế. Mô hình chỉ thua kém kiểu ResNet-18 khoảng $1.5\%$ độ chính xác nhưng giảm tới $80\%$ số lượng tham số ($2.24$M so với $11.18$M), giảm $71\%$ số phép tính FLOPs và tăng gần gấp đôi thông lượng xử lý FPS ($118$ FPS so với $55$ FPS trên EuroSAT, và $147$ FPS so với $69$ FPS trên SVHN). Đây là lựa chọn lý tưởng cho các thiết bị biên và hệ thống giám sát nhúng.
    \item \textbf{Giới hạn tính toán của biến thể kiểu VGG-11:} Kiến trúc kiểu VGG-11 đạt độ chính xác khá tốt ($93.80\%$ trên SVHN và $94.75\%$ trên EuroSAT), tuy nhiên do cấu trúc tích chập tuần tự truyền thống không có cơ chế tách kênh hoặc skip connection nên số lượng tham số lên tới $9.36$M và thông lượng FPS bị hạn chế (chỉ $78$ FPS trên EuroSAT). So với kiểu MobileNetV2, kiểu VGG-11 tốn hơn gấp 4 lần tham số nhưng lại cho độ chính xác thấp hơn, qua đó chứng minh bước tiến vượt bậc của các khối tích chập hiện đại.
    \item \textbf{Mô hình nền tảng Custom CNN:} Với số tham số tối thiểu ($0.35$M) và tốc độ xử lý nhanh nhất ($196$--$238$ FPS), Custom CNN đáp ứng tốt các bài toán phân loại đơn giản hoặc đóng vai trò baseline kiểm chứng ban đầu.
\end{itemize}

\section{Đóng Gói Triển Khai Hệ Thống Web App Thị Giác Máy Tính}

Các mô hình kiến trúc kiểu ResNet-18 và kiểu MobileNetV2 sau khi hoàn tất huấn luyện được xuất khẩu (export) sang định dạng trung gian mở \textbf{ONNX (Open Neural Network Exchange)} và tối ưu hóa thời gian thực thi bằng \textbf{ONNX Runtime Execution Provider}. Hệ thống được đóng gói hoàn chỉnh thành một Web Dashboard tương tác trực quan (Hình~\ref{fig:cnn_webapp_ui}).

\begin{figure}[H]
    \centering
    \includegraphics[width=0.92\textwidth]{images/fig509_webapp_cnn_vision_ui.png}
    \caption{Giao diện Web App tương tác Hệ thống Phân loại Thị giác Máy tính Đa miền (Vision AI Dashboard): Tải ảnh, trực quan hóa bản đồ kích hoạt CAM và trả về xác suất nhận diện thời gian thực.}
    \label{fig:cnn_webapp_ui}
\end{figure}

Giao diện ứng dụng cung cấp hai phân hệ độc lập: (1) Phân hệ phân loại ảnh viễn thám vệ tinh EuroSAT (xác định mục đích sử dụng đất với độ chính xác lên tới $98.40\%$, hỗ trợ giám sát tài nguyên rừng và quy hoạch đô thị), và (2) Phân hệ nhận diện biển số nhà ngoại cảnh SVHN. Nhờ tối ưu hóa bằng runtime C++, hệ thống đạt độ trễ suy luận chỉ $14.5$ ms trên CPU thông thường và dưới $3.2$ ms trên bộ tăng tốc phần cứng, đáp ứng trọn vẹn tiêu chuẩn vận hành sản phẩm công nghiệp.

\newpage
"""
