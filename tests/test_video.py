"""Tests for video module.

Module này kiểm tra các chức năng của module video:
- VideoReader
- CameraReader
- Video utils

Để chạy test:
    pytest tests/test_video.py -v
"""
import os
from pathlib import Path

import cv2
import numpy as np
import pytest

from src.exceptions import VideoError
from src.video import CameraReader, VideoReader
from src.video.utils import (
    add_text_to_frame,
    check_frame_valid,
    convert_color,
    normalize_frame,
    resize_frame,
)


# Kiểm tra utils
def test_resize_frame():
    """Test resize_frame function."""
    # Tạo frame test đơn giản
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    frame[100:200, 100:200] = 255  # Vẽ hình vuông màu trắng
    
    # Test resize không giữ tỷ lệ
    resized = resize_frame(frame, 320, 240, keep_aspect_ratio=False)
    assert resized.shape == (240, 320, 3)
    
    # Test resize giữ tỷ lệ
    resized = resize_frame(frame, 320, 240, keep_aspect_ratio=True)
    assert resized.shape == (240, 320, 3)


def test_normalize_frame():
    """Test normalize_frame function."""
    frame = np.full((10, 10, 3), 255, dtype=np.uint8)
    normalized = normalize_frame(frame)
    assert normalized.dtype == np.float32
    assert np.allclose(normalized, 1.0)


def test_check_frame_valid():
    """Test check_frame_valid function."""
    valid_frame = np.zeros((10, 10, 3), dtype=np.uint8)
    assert check_frame_valid(valid_frame) is True
    
    # None frame
    assert check_frame_valid(None) is False
    
    # Empty frame
    empty_frame = np.array([])
    assert check_frame_valid(empty_frame) is False


def test_convert_color():
    """Test convert_color function."""
    # Tạo frame BGR với màu đỏ (0, 0, 255)
    frame = np.zeros((10, 10, 3), dtype=np.uint8)
    frame[:, :, 2] = 255  # BGR: đỏ là kênh thứ 3 (index 2)
    
    # Chuyển sang RGB
    rgb_frame = convert_color(frame, cv2.COLOR_BGR2RGB)
    
    # Kiểm tra: Trong RGB, đỏ là kênh thứ 1 (index 0)
    assert rgb_frame[0, 0, 0] == 255
    assert rgb_frame[0, 0, 1] == 0
    assert rgb_frame[0, 0, 2] == 0


def test_add_text_to_frame():
    """Test add_text_to_frame function."""
    frame = np.zeros((100, 300, 3), dtype=np.uint8)
    text = "Test text"
    position = (10, 50)
    
    result = add_text_to_frame(frame, text, position)
    
    # Kiểm tra kết quả trả về có đúng kích thước không
    assert result.shape == frame.shape
    
    # Kiểm tra frame gốc không bị thay đổi
    assert np.all(frame == 0)


# Kiểm tra VideoReader - các test này cần file video mẫu
@pytest.mark.skipif(not os.path.exists("data/videos/sample.mp4"), 
                    reason="Sample video file not available")
class TestVideoReader:
    """Test VideoReader class."""
    
    def test_open_valid_file(self):
        """Test opening a valid video file."""
        reader = VideoReader("data/videos/sample.mp4")
        assert reader.open() is True
        assert reader.is_opened is True
        assert "width" in reader.info
        assert "height" in reader.info
        assert "fps" in reader.info
        reader.close()
    
    def test_open_invalid_file(self):
        """Test opening an invalid video file."""
        reader = VideoReader("nonexistent_file.mp4")
        with pytest.raises(VideoError):
            reader.open()
    
    def test_read_frame(self):
        """Test reading frames from a video file."""
        with VideoReader("data/videos/sample.mp4") as reader:
            frame = reader.read_frame()
            assert frame is not None
            assert isinstance(frame, np.ndarray)
            assert frame.shape[2] == 3  # Should be a color image


# Kiểm tra CameraReader - các test này cần camera
@pytest.mark.skipif(not cv2.VideoCapture(0).isOpened(), 
                    reason="No camera available")
class TestCameraReader:
    """Test CameraReader class."""
    
    def test_start_camera(self):
        """Test starting a camera."""
        camera = CameraReader(camera_id=0)
        try:
            assert camera.start() is True
            assert camera.is_running is True
            assert "width" in camera.info
            assert "height" in camera.info
            assert "fps" in camera.info
        finally:
            camera.stop()
    
    def test_read_frame(self):
        """Test reading frames from a camera."""
        with CameraReader(camera_id=0) as camera:
            frame = camera.read_frame()
            assert frame is not None
            assert isinstance(frame, np.ndarray)
            assert frame.shape[2] == 3  # Should be a color image
    
    def test_camera_properties(self):
        """Test getting and setting camera properties."""
        with CameraReader(camera_id=0) as camera:
            # Lấy FPS hiện tại
            current_fps = camera.get_camera_property(cv2.CAP_PROP_FPS)
            
            # Thử đặt FPS mới (có thể không được hỗ trợ trên tất cả camera)
            new_fps = 30.0
            camera.set_camera_property(cv2.CAP_PROP_FPS, new_fps)
            
            # Kiểm tra FPS mới (lưu ý: một số camera có thể không hỗ trợ thay đổi FPS)
            # Vì vậy, chúng ta chỉ kiểm tra rằng hàm hoạt động mà không gây ra lỗi
            fps_after = camera.get_camera_property(cv2.CAP_PROP_FPS)
            assert isinstance(fps_after, float) 