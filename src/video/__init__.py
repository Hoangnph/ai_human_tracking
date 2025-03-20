"""Module xử lý video từ nhiều nguồn (camera, file).

Module này cung cấp các class và hàm tiện ích để:
- Đọc video từ nhiều nguồn khác nhau
- Xử lý và tiền xử lý frame
- Các tiện ích làm việc với video

Examples:
    Đọc video từ file:
    
    >>> from src.video import VideoReader
    >>> with VideoReader("path/to/video.mp4") as reader:
    ...     for frame in reader:
    ...         # Process frame
    
    Đọc video từ camera:
    
    >>> from src.video import CameraReader
    >>> with CameraReader(camera_id=0) as camera:
    ...     while True:
    ...         frame = camera.read_frame()
    ...         if frame is None:
    ...             break
    ...         # Process frame
"""
from src.video.camera import CameraReader
from src.video.utils import (
    add_text_to_frame,
    check_frame_valid,
    convert_color,
    estimate_fps,
    normalize_frame,
    resize_frame,
)
from src.video.video_reader import VideoReader

__all__ = [
    "VideoReader",
    "CameraReader",
    "resize_frame",
    "normalize_frame",
    "convert_color",
    "add_text_to_frame",
    "estimate_fps",
    "check_frame_valid",
]
