"""Tiện ích cho module phát hiện đối tượng.

Module này cung cấp các hàm tiện ích để xử lý kết quả phát hiện đối tượng,
như lọc kết quả, vẽ bounding boxes, và chuyển đổi tọa độ.

Example:
    >>> from src.detection.utils import filter_detections, draw_detections
    >>> filtered_results = filter_detections(results, class_ids=[0], conf_threshold=0.5)
    >>> annotated_frame = draw_detections(frame, filtered_results)
"""
from typing import Dict, List, Optional, Tuple, Union

import cv2
import numpy as np

from src.constants import COLORS, PERSON_CLASS_ID
from src.utils.logger import logger

# Các tên lớp của COCO dataset (80 lớp)
COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote",
    "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book",
    "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
]

# Định nghĩa loại Detection Result
# (box [x1, y1, x2, y2], confidence, class_id)
DetectionResult = Tuple[List[float], float, int]


def filter_detections(
    detections: List[DetectionResult],
    class_ids: Optional[List[int]] = None,
    conf_threshold: Optional[float] = None,
) -> List[DetectionResult]:
    """Lọc kết quả phát hiện theo lớp và độ tin cậy.

    Args:
        detections: Danh sách các kết quả phát hiện (bbox, conf, class_id)
        class_ids: Danh sách ID lớp cần giữ lại, None để giữ tất cả
        conf_threshold: Ngưỡng độ tin cậy tối thiểu, None để không lọc theo confidence

    Returns:
        Danh sách các kết quả phát hiện đã lọc
    """
    if not detections:
        return []

    filtered = []
    for bbox, conf, cls_id in detections:
        # Lọc theo độ tin cậy nếu được chỉ định
        if conf_threshold is not None and conf < conf_threshold:
            continue
        
        # Lọc theo lớp
        if class_ids is not None and cls_id not in class_ids:
            continue
            
        filtered.append((bbox, conf, cls_id))
    
    return filtered


def draw_detections(
    frame: np.ndarray,
    detections: List[DetectionResult],
    draw_labels: bool = True,
    label_format: str = "{cls} {conf:.2f}",
    color_map: Optional[Dict[int, Tuple[int, int, int]]] = None,
    thickness: int = 2,
) -> np.ndarray:
    """Vẽ các kết quả phát hiện lên frame.

    Args:
        frame: Frame cần vẽ
        detections: Danh sách các kết quả phát hiện (bbox, conf, class_id)
        draw_labels: Có vẽ nhãn hay không
        label_format: Định dạng nhãn
        color_map: Bản đồ màu sắc cho từng lớp, None để sử dụng màu mặc định
        thickness: Độ dày của đường viền

    Returns:
        Frame đã vẽ các kết quả phát hiện
    """
    if not detections:
        return frame

    # Copy frame để không thay đổi dữ liệu gốc
    output = frame.copy()
    
    for bbox, conf, cls_id in detections:
        # Lấy màu sắc cho lớp
        if color_map and cls_id in color_map:
            color = color_map[cls_id]
        else:
            # Sử dụng màu cố định cho mỗi lớp
            color_idx = cls_id % len(COLORS.values())
            color = list(COLORS.values())[color_idx]
        
        # Chuyển đổi bbox sang int
        x1, y1, x2, y2 = [int(c) for c in bbox]
        
        # Vẽ bounding box
        cv2.rectangle(output, (x1, y1), (x2, y2), color, thickness)
        
        # Vẽ nhãn nếu được yêu cầu
        if draw_labels:
            # Lấy tên lớp
            cls_name = COCO_CLASSES[cls_id] if cls_id < len(COCO_CLASSES) else f"class_{cls_id}"
            
            # Tạo nhãn
            label = label_format.format(cls=cls_name, conf=conf)
            
            # Lấy kích thước văn bản
            (label_width, label_height), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
            )
            
            # Vẽ nền cho nhãn
            cv2.rectangle(
                output,
                (x1, y1 - label_height - 5),
                (x1 + label_width + 5, y1),
                color,
                -1,  # -1 để fill
            )
            
            # Vẽ văn bản
            cv2.putText(
                output,
                label,
                (x1 + 3, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),  # Màu trắng cho văn bản
                2,
            )
    
    return output


def convert_to_relative_coords(
    bbox: List[float], image_width: int, image_height: int
) -> List[float]:
    """Chuyển đổi tọa độ tuyệt đối sang tương đối (0-1).

    Args:
        bbox: Bounding box dạng [x1, y1, x2, y2]
        image_width: Chiều rộng của hình ảnh
        image_height: Chiều cao của hình ảnh

    Returns:
        Bounding box dạng [x1, y1, x2, y2] với tọa độ tương đối
    """
    x1, y1, x2, y2 = bbox
    return [
        x1 / image_width,
        y1 / image_height,
        x2 / image_width,
        y2 / image_height,
    ]


def convert_to_absolute_coords(
    bbox: List[float], image_width: int, image_height: int
) -> List[float]:
    """Chuyển đổi tọa độ tương đối (0-1) sang tuyệt đối.

    Args:
        bbox: Bounding box dạng [x1, y1, x2, y2] với tọa độ tương đối
        image_width: Chiều rộng của hình ảnh
        image_height: Chiều cao của hình ảnh

    Returns:
        Bounding box dạng [x1, y1, x2, y2] với tọa độ tuyệt đối
    """
    x1, y1, x2, y2 = bbox
    return [
        x1 * image_width,
        y1 * image_height,
        x2 * image_width,
        y2 * image_height,
    ]
