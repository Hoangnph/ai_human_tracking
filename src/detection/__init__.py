"""Module phát hiện đối tượng sử dụng YOLOv8.

Module này cung cấp các lớp và hàm để phát hiện đối tượng trong hình ảnh/video,
với trọng tâm vào phát hiện người.

Examples:
    >>> from src.detection import ObjectDetector
    >>> detector = ObjectDetector()
    >>> results = detector.detect(frame)
    >>> for bbox, conf, cls_id in results:
    ...     # Process detection results
"""
from src.detection.object_detector import ObjectDetector
from src.detection.utils import (
    filter_detections,
    draw_detections,
    convert_to_relative_coords,
    convert_to_absolute_coords,
)

__all__ = [
    "ObjectDetector",
    "filter_detections",
    "draw_detections",
    "convert_to_relative_coords",
    "convert_to_absolute_coords",
]
