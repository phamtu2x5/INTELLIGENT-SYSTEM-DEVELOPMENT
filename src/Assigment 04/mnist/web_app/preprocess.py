import io
import base64
import numpy as np
from PIL import Image
import cv2
from scipy.ndimage import center_of_mass
import torch

def preprocess_canvas_image(base64_data):
    """
    Tiền xử lý ảnh vẽ từ Canvas HTML5 để đưa về chuẩn MNIST (28x28 grayscale, 
    chữ trắng nền đen, bảo toàn tỉ lệ khung hình 20x20 và căn giữa theo trọng tâm).
    """
    if not base64_data:
        return None, None, "Dữ liệu ảnh rỗng."

    if ',' in base64_data:
        base64_data = base64_data.split(',')[1]

    try:
        img_bytes = base64.b64decode(base64_data)
        pil_img = Image.open(io.BytesIO(img_bytes)).convert('RGBA')
    except Exception as e:
        return None, None, f"Lỗi giải mã ảnh base64: {str(e)}"

    # Tạo nền đen và dán ảnh vẽ lên (xử lý cả kênh alpha)
    bg = Image.new('RGBA', pil_img.size, (0, 0, 0, 255))
    bg.paste(pil_img, mask=pil_img.split()[3])  # dùng alpha channel làm mask
    gray_img = bg.convert('L')
    img_np = np.array(gray_img, dtype=np.uint8)

    # Nếu người dùng vẽ màu đen trên nền trắng thì đảo ngược lại (MNIST chuẩn là chữ trắng nền đen)
    corners = [img_np[0, 0], img_np[0, -1], img_np[-1, 0], img_np[-1, -1]]
    if np.mean(corners) > 128:
        img_np = 255 - img_np

    # Kiểm tra xem bảng vẽ có nét vẽ hay không
    non_zero_mask = img_np > 30
    if np.sum(non_zero_mask) < 25:
        return None, None, "Bảng vẽ đang trống, vui lòng vẽ một chữ số."

    # Tìm hộp bao (bounding box) quanh chữ số
    coords = cv2.findNonZero(non_zero_mask.astype(np.uint8))
    x, y, w, h = cv2.boundingRect(coords)
    digit_crop = img_np[y:y+h, x:x+w]

    # Co giãn chữ số để vừa trong khung 20x20 mà vẫn giữ nguyên tỉ lệ khung hình (aspect ratio)
    if w > h:
        new_w = 20
        new_h = max(1, int(round(h * 20.0 / w)))
    else:
        new_h = 20
        new_w = max(1, int(round(w * 20.0 / h)))

    digit_resized = cv2.resize(digit_crop, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Đặt vào khung 28x28 tạm thời
    img_28 = np.zeros((28, 28), dtype=np.float32)
    pad_y = (28 - new_h) // 2
    pad_x = (28 - new_w) // 2
    img_28[pad_y:pad_y+new_h, pad_x:pad_x+new_w] = digit_resized

    # Căn chỉnh vị trí chữ số theo trọng tâm (Center of Mass) về vị trí (13.5, 13.5) chuẩn MNIST
    cy, cx = center_of_mass(img_28)
    if not (np.isnan(cy) or np.isnan(cx)):
        shift_y = int(round(13.5 - cy))
        shift_x = int(round(13.5 - cx))
        M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
        img_28 = cv2.warpAffine(img_28, M, (28, 28))

    # Chuẩn hoá pixel về đoạn [0.0, 1.0]
    img_norm = np.clip(img_28 / 255.0, 0.0, 1.0).astype(np.float32)

    # Chuyển thành PyTorch Tensor: shape (1, 1, 28, 28)
    tensor = torch.from_numpy(img_norm[np.newaxis, np.newaxis, :, :]).float()

    # Tạo ảnh xem trước 28x28 (phóng to 112x112 nearest-neighbor để hiển thị rõ nét trên web)
    preview_np = (img_norm * 255).astype(np.uint8)
    preview_scaled = cv2.resize(preview_np, (112, 112), interpolation=cv2.INTER_NEAREST)
    preview_pil = Image.fromarray(preview_scaled)
    buffer = io.BytesIO()
    preview_pil.save(buffer, format='PNG')
    preview_base64 = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode('utf-8')

    return tensor, preview_base64, None
