"""Tiện ích xử lý frame video.

Module này cung cấp các hàm tiện ích để tiền xử lý và xử lý frame video
trước khi đưa vào các module phát hiện và phân tích.

Example:
    >>> from src.video.utils import resize_frame, normalize_frame
    >>> resized_frame = resize_frame(frame, width=640, height=480)
    >>> normalized_frame = normalize_frame(resized_frame)
"""
from typing import Optional, Tuple, Union

import cv2
import numpy as np

from src.config import settings
from src.exceptions import VideoError
from src.utils.logger import logger


def resize_frame(
    frame: np.ndarray, 
    width: Optional[int] = None, 
    height: Optional[int] = None,
    keep_aspect_ratio: bool = True
) -> np.ndarray:
    """Thay đổi kích thước frame.

    Args:
        frame: Frame cần thay đổi kích thước
        width: Chiều rộng mong muốn, mặc định là settings.frame_width
        height: Chiều cao mong muốn, mặc định là settings.frame_height
        keep_aspect_ratio: Giữ tỷ lệ khung hình gốc

    Returns:
        Frame đã thay đổi kích thước

    Raises:
        VideoError: Nếu frame rỗng hoặc không hợp lệ
    """
    if frame is None or frame.size == 0:
        raise VideoError("Frame rỗng hoặc không hợp lệ")

    # Sử dụng giá trị từ cấu hình nếu không được chỉ định
    if width is None:
        width = settings.frame_width
    if height is None:
        height = settings.frame_height

    # Nếu giữ tỷ lệ khung hình
    if keep_aspect_ratio:
        h, w = frame.shape[:2]
        # Tính toán tỷ lệ thay đổi
        r_w = width / w
        r_h = height / h
        r = min(r_w, r_h)  # Lấy tỷ lệ nhỏ hơn để không vượt quá kích thước
        
        new_w = int(w * r)
        new_h = int(h * r)
        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        # Tạo khung hình đúng kích thước với nền đen
        result = np.zeros((height, width, 3), dtype=np.uint8)
        # Đặt ảnh đã resize vào giữa
        y_offset = (height - new_h) // 2
        x_offset = (width - new_w) // 2
        result[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        return result
    else:
        # Thay đổi kích thước trực tiếp
        return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)


def normalize_frame(frame: np.ndarray) -> np.ndarray:
    """Chuẩn hóa frame để xử lý với mô hình.

    Chuyển đổi frame thành định dạng phù hợp cho các mô hình deep learning:
    - Chuẩn hóa giá trị pixel về [0, 1]
    - Thay đổi kênh màu nếu cần

    Args:
        frame: Frame cần chuẩn hóa

    Returns:
        Frame đã chuẩn hóa
    """
    # Copy frame để không thay đổi dữ liệu gốc
    normalized = frame.copy().astype(np.float32)
    
    # Chuẩn hóa giá trị [0, 255] -> [0, 1]
    normalized /= 255.0
    
    return normalized


def convert_color(frame: np.ndarray, conversion_code: int = cv2.COLOR_BGR2RGB) -> np.ndarray:
    """Chuyển đổi không gian màu của frame.

    OpenCV sử dụng định dạng BGR trong khi hầu hết các thư viện khác sử dụng RGB.

    Args:
        frame: Frame cần chuyển đổi
        conversion_code: Mã chuyển đổi màu (cv2.COLOR_*)

    Returns:
        Frame đã chuyển đổi
    """
    return cv2.cvtColor(frame, conversion_code)


def add_text_to_frame(
    frame: np.ndarray,
    text: str,
    position: Tuple[int, int],
    font_scale: float = 0.7,
    color: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2
) -> np.ndarray:
    """Thêm văn bản vào frame.

    Args:
        frame: Frame cần thêm văn bản
        text: Nội dung văn bản
        position: Vị trí (x, y) để đặt văn bản
        font_scale: Tỷ lệ phông chữ
        color: Màu sắc văn bản (BGR)
        thickness: Độ dày của văn bản

    Returns:
        Frame đã thêm văn bản
    """
    # Copy frame để không thay đổi dữ liệu gốc
    result = frame.copy()
    
    # Thêm nền tối sau văn bản để dễ đọc
    text_size = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
    )[0]
    
    # Tạo hình chữ nhật nền
    cv2.rectangle(
        result, 
        (position[0] - 5, position[1] - text_size[1] - 5),
        (position[0] + text_size[0] + 5, position[1] + 5),
        (0, 0, 0), 
        -1
    )
    
    # Thêm văn bản
    cv2.putText(
        result, 
        text, 
        position, 
        cv2.FONT_HERSHEY_SIMPLEX, 
        font_scale, 
        color, 
        thickness, 
        cv2.LINE_AA
    )
    
    return result


def estimate_fps(frame_count: int, elapsed_time: float) -> float:
    """Ước tính FPS (Frames Per Second).

    Args:
        frame_count: Số lượng frame đã xử lý
        elapsed_time: Thời gian đã trôi qua (giây)

    Returns:
        FPS ước tính
    """
    return frame_count / elapsed_time if elapsed_time > 0 else 0


def check_frame_valid(frame: np.ndarray) -> bool:
    """Kiểm tra frame có hợp lệ không.

    Args:
        frame: Frame cần kiểm tra

    Returns:
        True nếu frame hợp lệ, False nếu không
    """
    return frame is not None and frame.size > 0 and frame.shape[0] > 0 and frame.shape[1] > 0
