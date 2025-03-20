"""Tests for detection module.

Module này kiểm tra các chức năng của module detection:
- ObjectDetector
- Detection utils

Để chạy test:
    pytest tests/test_detection.py -v
"""
import os
from pathlib import Path

import cv2
import numpy as np
import pytest

from src.constants import PERSON_CLASS_ID
from src.detection.utils import (
    convert_to_absolute_coords,
    convert_to_relative_coords,
    draw_detections,
    filter_detections,
)
from src.exceptions import ModelLoadError

# Định nghĩa dữ liệu test
TEST_DETECTIONS = [
    ([100.0, 200.0, 300.0, 400.0], 0.9, 0),  # Person với confidence cao
    ([150.0, 250.0, 350.0, 450.0], 0.7, 2),  # Car với confidence trung bình
    ([200.0, 300.0, 400.0, 500.0], 0.4, 0),  # Person với confidence thấp
]


# Kiểm tra các hàm tiện ích
def test_filter_detections_by_confidence():
    """Test lọc kết quả theo độ tin cậy."""
    filtered = filter_detections(TEST_DETECTIONS, conf_threshold=0.6)
    assert len(filtered) == 2
    assert filtered[0][1] == 0.9  # Person với confidence 0.9
    assert filtered[1][1] == 0.7  # Car với confidence 0.7


def test_filter_detections_by_class():
    """Test lọc kết quả theo lớp."""
    filtered = filter_detections(TEST_DETECTIONS, class_ids=[0])
    assert len(filtered) == 2
    assert filtered[0][2] == 0  # Person với confidence 0.9
    assert filtered[1][2] == 0  # Person với confidence 0.4


def test_filter_detections_by_both():
    """Test lọc kết quả theo cả lớp và độ tin cậy."""
    filtered = filter_detections(TEST_DETECTIONS, class_ids=[0], conf_threshold=0.6)
    assert len(filtered) == 1
    assert filtered[0][1] == 0.9  # Person với confidence 0.9
    assert filtered[0][2] == 0  # Class ID 0 (person)


def test_convert_coords():
    """Test chuyển đổi tọa độ tương đối và tuyệt đối."""
    # Tọa độ tuyệt đối
    bbox = [100.0, 200.0, 300.0, 400.0]
    
    # Kích thước ảnh
    width, height = 1000, 800
    
    # Chuyển sang tọa độ tương đối
    rel_bbox = convert_to_relative_coords(bbox, width, height)
    assert rel_bbox == [0.1, 0.25, 0.3, 0.5]
    
    # Chuyển lại sang tọa độ tuyệt đối
    abs_bbox = convert_to_absolute_coords(rel_bbox, width, height)
    assert abs_bbox == bbox


def test_draw_detections():
    """Test vẽ các kết quả phát hiện lên frame."""
    # Tạo frame test
    frame = np.zeros((600, 800, 3), dtype=np.uint8)
    
    # Vẽ kết quả lên frame
    result = draw_detections(frame, TEST_DETECTIONS)
    
    # Kiểm tra kết quả trả về có đúng kích thước không
    assert result.shape == frame.shape
    
    # Kiểm tra frame gốc không bị thay đổi
    assert not np.array_equal(frame, result)


# Kiểm tra ObjectDetector - chỉ khi có mô hình
@pytest.mark.skipif(
    not os.path.exists("data/models/yolov8n.pt") and not os.environ.get("RUN_MODEL_TESTS"),
    reason="YOLOv8 model not available or model tests disabled"
)
class TestObjectDetector:
    """Test ObjectDetector class."""
    
    def test_load_model(self):
        """Test tải mô hình."""
        from src.detection import ObjectDetector
        
        # Sử dụng mô hình nhỏ nhất cho tests
        detector = ObjectDetector(model_name="yolov8n.pt")
        assert detector.load_model() is True
        assert detector.is_loaded is True
        assert len(detector.class_names) > 0
    
    def test_detect_empty_frame(self):
        """Test phát hiện với frame rỗng."""
        from src.detection import ObjectDetector
        
        detector = ObjectDetector(model_name="yolov8n.pt")
        detector.load_model()
        
        # Test với frame None
        results = detector.detect(None)
        assert results == []
        
        # Test với frame rỗng
        empty_frame = np.array([])
        results = detector.detect(empty_frame)
        assert results == []
    
    def test_detect_persons(self):
        """Test phát hiện người trong frame đơn giản."""
        from src.detection import ObjectDetector
        
        # Tạo frame test đơn giản
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Vẽ hình người đơn giản (Có thể không được phát hiện do quá đơn giản)
        cv2.rectangle(frame, (100, 100), (300, 400), (255, 255, 255), -1)
        
        detector = ObjectDetector(model_name="yolov8n.pt")
        detector.load_model()
        
        # Test phát hiện với ngưỡng rất thấp để tăng khả năng phát hiện
        results = detector.detect(frame, conf_threshold=0.01)
        
        # Do đây là frame nhân tạo, chúng ta không thể đảm bảo model sẽ phát hiện,
        # nên chỉ kiểm tra rằng hàm không gây ra lỗi
        assert isinstance(results, list)


# Kiểm tra chức năng phát hiện với hình ảnh thực
@pytest.mark.skipif(
    not os.path.exists("data/models/yolov8n.pt") or not os.path.exists("data/videos/sample.mp4"),
    reason="Model or sample video not available"
)
def test_with_real_image():
    """Test phát hiện đối tượng với hình ảnh thực từ video mẫu."""
    from src.detection import ObjectDetector
    from src.video import VideoReader
    
    # Đọc frame từ video mẫu
    reader = VideoReader("data/videos/sample.mp4")
    reader.open()
    frame = reader.read_frame()
    reader.close()
    
    # Đảm bảo frame hợp lệ
    assert frame is not None
    
    # Thực hiện phát hiện
    detector = ObjectDetector(model_name="yolov8n.pt")
    detector.load_model()
    
    # Phát hiện tất cả đối tượng
    all_detections = detector.detect(frame)
    
    # Phát hiện chỉ người
    person_detections = detector.detect_persons(frame)
    
    # Kiểm tra kết quả - Có thể có hoặc không các đối tượng
    # Chủ yếu đảm bảo không có lỗi xảy ra
    assert isinstance(all_detections, list)
    assert isinstance(person_detections, list)
    
    # Đảm bảo chỉ có người trong kết quả person_detections
    for _, _, cls_id in person_detections:
        assert cls_id == PERSON_CLASS_ID 