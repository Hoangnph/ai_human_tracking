"""Module cung cấp lớp ObjectDetector để phát hiện đối tượng sử dụng YOLOv8.

Lớp này tải mô hình YOLOv8 pre-trained và cung cấp các phương thức để phát hiện
đối tượng trong hình ảnh/video. Mặc định tập trung vào phát hiện người nhưng
có thể được sử dụng để phát hiện các đối tượng khác.

Example:
    >>> from src.detection.object_detector import ObjectDetector
    >>> detector = ObjectDetector(model_name="yolov8m.pt")
    >>> results = detector.detect(frame)
    >>> for bbox, conf, cls_id in results:
    ...     # Process detection results
"""
import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any

import cv2
import numpy as np
import torch
from ultralytics import YOLO

from src.config import settings
from src.constants import PERSON_CLASS_ID, DEFAULT_CONFIDENCE_THRESHOLD
from src.detection.utils import DetectionResult, filter_detections
from src.exceptions import ModelLoadError
from src.utils.logger import logger


class ObjectDetector:
    """Lớp phát hiện đối tượng sử dụng YOLOv8.

    Attributes:
        model_path: Đường dẫn tới file mô hình
        confidence_threshold: Ngưỡng độ tin cậy tối thiểu
        iou_threshold: Ngưỡng IoU cho NMS
        device: Thiết bị chạy mô hình (cuda, cpu)
        model: Đối tượng mô hình YOLO
        is_loaded: Trạng thái tải mô hình
        class_names: Danh sách tên lớp
    """

    def __init__(
        self,
        model_name: str = None,
        confidence_threshold: float = None,
        iou_threshold: float = 0.45,
        device: str = None,
    ):
        """Khởi tạo ObjectDetector.

        Args:
            model_name: Tên file mô hình, mặc định lấy từ settings
            confidence_threshold: Ngưỡng độ tin cậy, mặc định lấy từ settings
            iou_threshold: Ngưỡng IoU cho NMS
            device: Thiết bị chạy mô hình, None để tự động phát hiện
        """
        # Lấy các tham số từ settings nếu không được chỉ định
        self.model_name = model_name or settings.yolo_model
        self.confidence_threshold = confidence_threshold or settings.yolo_confidence
        self.iou_threshold = iou_threshold
        
        # Kiểm tra và chuẩn bị đường dẫn mô hình
        models_dir = settings.models_dir
        if not os.path.exists(models_dir):
            os.makedirs(models_dir, exist_ok=True)
        
        # Xác định device
        self.device = device
        if self.device is None:
            self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        
        # Khởi tạo biến
        self.model = None
        self.is_loaded = False
        self.class_names = []
        
        # Xây dựng đường dẫn đến file mô hình
        self.model_path = os.path.join(models_dir, self.model_name)
        
        # YOLO Hub models được chỉ định trực tiếp bằng tên
        if self.model_name in ["yolov8n", "yolov8s", "yolov8m", "yolov8l", "yolov8x"]:
            self.model_path = self.model_name
            
        logger.info(f"Khởi tạo ObjectDetector với mô hình: {self.model_path}")
        logger.info(f"Confidence threshold: {self.confidence_threshold}")
        logger.info(f"Device: {self.device}")

    def load_model(self) -> bool:
        """Tải mô hình YOLOv8.

        Returns:
            True nếu tải thành công, False nếu thất bại

        Raises:
            ModelLoadError: Nếu không thể tải mô hình
        """
        try:
            start_time = time.time()
            
            # Tải mô hình
            self.model = YOLO(self.model_path)
            
            # Chuyển sang device phù hợp
            self.model.to(self.device)
            
            # Lấy danh sách tên lớp
            self.class_names = self.model.names if hasattr(self.model, "names") else []
            
            self.is_loaded = True
            load_time = time.time() - start_time
            
            logger.info(f"Đã tải mô hình {self.model_path} thành công trong {load_time:.2f}s")
            logger.info(f"Mô hình có {len(self.class_names)} lớp")
            
            return True
            
        except Exception as e:
            self.is_loaded = False
            error_msg = f"Không thể tải mô hình {self.model_path}: {e}"
            logger.error(error_msg)
            raise ModelLoadError(str(self.model_path), error_msg)

    def detect(
        self,
        frame: np.ndarray,
        conf_threshold: Optional[float] = None,
        filter_classes: Optional[List[int]] = None,
    ) -> List[DetectionResult]:
        """Phát hiện đối tượng trong frame.

        Args:
            frame: Frame cần phát hiện
            conf_threshold: Ngưỡng độ tin cậy, ghi đè tham số mặc định
            filter_classes: Danh sách ID lớp cần lọc, None để không lọc

        Returns:
            Danh sách các kết quả phát hiện (bbox, conf, class_id)

        Raises:
            ModelLoadError: Nếu mô hình chưa được tải
        """
        if not self.is_loaded:
            self.load_model()

        if frame is None or frame.size == 0:
            logger.warning("Frame rỗng hoặc không hợp lệ")
            return []

        # Sử dụng ngưỡng từ tham số hoặc giá trị mặc định
        threshold = conf_threshold or self.confidence_threshold

        try:
            # Thực hiện dự đoán
            results = self.model.predict(
                source=frame,
                conf=threshold,
                iou=self.iou_threshold,
                verbose=False,
            )

            # Chuyển đổi kết quả từ định dạng YOLO sang định dạng của chúng ta
            detections = self._process_yolo_results(results[0], filter_classes)
            
            return detections
            
        except Exception as e:
            logger.error(f"Lỗi khi phát hiện đối tượng: {e}")
            return []

    def detect_persons(
        self, frame: np.ndarray, conf_threshold: Optional[float] = None
    ) -> List[DetectionResult]:
        """Phát hiện người trong frame.

        Hàm tiện ích để chỉ phát hiện người (class_id=0).

        Args:
            frame: Frame cần phát hiện
            conf_threshold: Ngưỡng độ tin cậy, ghi đè tham số mặc định

        Returns:
            Danh sách các kết quả phát hiện (bbox, conf, class_id)
        """
        return self.detect(frame, conf_threshold, filter_classes=[PERSON_CLASS_ID])

    def _process_yolo_results(
        self, result: Any, filter_classes: Optional[List[int]] = None
    ) -> List[DetectionResult]:
        """Xử lý kết quả từ YOLO để chuyển thành định dạng của chúng ta.

        Args:
            result: Kết quả từ YOLO model
            filter_classes: Danh sách ID lớp cần lọc

        Returns:
            Danh sách các kết quả phát hiện (bbox, conf, class_id)
        """
        detections = []
        
        # Kiểm tra kết quả
        if not hasattr(result, "boxes"):
            return detections
            
        # Lấy các giá trị từ kết quả YOLO
        boxes = result.boxes
        
        # Xử lý từng box
        for box in boxes:
            # Lấy tọa độ box
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            
            # Lấy độ tin cậy
            confidence = float(box.conf[0].cpu().numpy())
            
            # Lấy ID lớp
            class_id = int(box.cls[0].cpu().numpy())
            
            # Lọc theo lớp nếu cần
            if filter_classes and class_id not in filter_classes:
                continue
                
            # Thêm vào danh sách kết quả
            detection = ([x1, y1, x2, y2], confidence, class_id)
            detections.append(detection)
            
        return detections

    def draw_results(
        self,
        frame: np.ndarray,
        detections: List[DetectionResult],
        draw_labels: bool = True,
    ) -> np.ndarray:
        """Vẽ kết quả phát hiện lên frame.

        Hàm tiện ích để vẽ các kết quả phát hiện, sử dụng hàm draw_detections.

        Args:
            frame: Frame cần vẽ
            detections: Danh sách các kết quả phát hiện
            draw_labels: Có vẽ nhãn hay không

        Returns:
            Frame đã vẽ các kết quả phát hiện
        """
        from src.detection.utils import draw_detections
        
        return draw_detections(
            frame,
            detections,
            draw_labels=draw_labels,
            label_format="{cls} {conf:.2f}",
        )

    def __del__(self):
        """Destructor để giải phóng tài nguyên."""
        # Giải phóng model khỏi bộ nhớ
        self.model = None
        torch.cuda.empty_cache() if torch.cuda.is_available() else None 