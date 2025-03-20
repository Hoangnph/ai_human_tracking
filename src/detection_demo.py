"""Script demo cho module phát hiện đối tượng.

Demo này sử dụng module detection để phát hiện đối tượng từ camera hoặc file video,
và hiển thị kết quả trực quan.

Cách chạy:
    python src/detection_demo.py --video data/videos/sample.mp4 --classes 0
    python src/detection_demo.py --camera 0 --classes 0 2 67
    python src/detection_demo.py --video data/videos/sample.mp4 --all
"""
import argparse
import sys
import time
from pathlib import Path

# Thêm thư mục gốc của dự án vào sys.path
sys.path.append(str(Path(__file__).parent.parent))

import cv2
import numpy as np

from src.config import settings
from src.detection import ObjectDetector
from src.utils.logger import logger
from src.video import CameraReader, VideoReader, estimate_fps


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Object Detection Demo")
    
    # Định nghĩa nhóm nguồn input
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--video", type=str, help="Đường dẫn tới file video")
    source_group.add_argument("--camera", type=int, help="Camera ID")
    
    # Định nghĩa nhóm các lớp cần phát hiện
    class_group = parser.add_mutually_exclusive_group()
    class_group.add_argument(
        "--classes", nargs="+", type=int, 
        help="Danh sách ID lớp cần phát hiện (mặc định: 0 - người)"
    )
    class_group.add_argument(
        "--all", action="store_true", 
        help="Phát hiện tất cả các lớp"
    )
    
    # Các tùy chọn khác
    parser.add_argument(
        "--conf", type=float, default=None, 
        help="Ngưỡng độ tin cậy (mặc định: từ config)"
    )
    parser.add_argument(
        "--model", type=str, default=None, 
        help="Tên mô hình YOLOv8 (mặc định: từ config)"
    )
    parser.add_argument(
        "--width", type=int, default=640, 
        help="Chiều rộng hiển thị (mặc định: 640)"
    )
    parser.add_argument(
        "--height", type=int, default=480, 
        help="Chiều cao hiển thị (mặc định: 480)"
    )
    parser.add_argument(
        "--no-labels", action="store_true", 
        help="Không hiển thị nhãn"
    )
    
    return parser.parse_args()


def display_info(reader_info, detector):
    """Hiển thị thông tin nguồn video và detector."""
    logger.info("Thông tin video:")
    for key, value in reader_info.items():
        logger.info(f"  {key}: {value}")
    
    logger.info(f"Mô hình: {detector.model_path}")
    logger.info(f"Device: {detector.device}")
    logger.info(f"Confidence threshold: {detector.confidence_threshold}")


def main():
    """Hàm chính của demo."""
    args = parse_args()
    
    # Xác định filter classes
    filter_classes = None
    if not args.all:
        filter_classes = args.classes or [0]  # Mặc định chỉ phát hiện người (class_id=0)
    
    # Khởi tạo ObjectDetector
    detector = ObjectDetector(
        model_name=args.model,
        confidence_threshold=args.conf
    )
    
    # Tải mô hình
    detector.load_model()
    
    # Khởi tạo nguồn video
    if args.video:
        logger.info(f"Đọc từ file video: {args.video}")
        reader = VideoReader(
            args.video,
            resize_width=args.width,
            resize_height=args.height,
            keep_aspect_ratio=True
        )
        source_type = "video"
    else:
        logger.info(f"Đọc từ camera: {args.camera}")
        reader = CameraReader(
            camera_id=args.camera,
            resize_width=args.width,
            resize_height=args.height
        )
        source_type = "camera"
    
    # Chuẩn bị cửa sổ hiển thị
    window_name = "Object Detection Demo"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    try:
        # Mở nguồn video
        if source_type == "video":
            reader.open()
        else:
            reader.start()
        
        # Hiển thị thông tin
        display_info(reader.info, detector)
        
        # Khởi tạo biến đếm
        start_time = time.time()
        frame_count = 0
        detection_count = 0
        
        # Xử lý từng frame
        while True:
            # Đọc frame
            frame = reader.read_frame()
            
            # Kiểm tra frame hợp lệ
            if frame is None:
                logger.info("Hết video hoặc không đọc được frame")
                break
            
            # Phát hiện đối tượng
            detections = detector.detect(frame, filter_classes=filter_classes)
            
            # Vẽ kết quả lên frame
            annotated_frame = detector.draw_results(
                frame, detections, draw_labels=not args.no_labels
            )
            
            # Cập nhật biến đếm
            frame_count += 1
            detection_count += len(detections)
            elapsed_time = time.time() - start_time
            
            # Tính FPS
            fps = estimate_fps(frame_count, elapsed_time)
            
            # Thêm thông tin FPS và số lượng đối tượng
            cv2.putText(
                annotated_frame,
                f"FPS: {fps:.2f} | Objects: {len(detections)}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )
            
            # Hiển thị frame
            cv2.imshow(window_name, annotated_frame)
            
            # Thoát nếu nhấn ESC
            key = cv2.waitKey(1)
            if key == 27:  # ESC
                logger.info("ESC pressed, exiting...")
                break
        
        # Hiển thị thống kê
        logger.info(f"Processed {frame_count} frames in {elapsed_time:.2f} seconds")
        logger.info(f"Average FPS: {fps:.2f}")
        logger.info(f"Total detections: {detection_count}")
        logger.info(f"Average detections per frame: {detection_count/frame_count:.2f}")
        
    except Exception as e:
        logger.error(f"Error in detection demo: {e}")
        
    finally:
        # Đóng nguồn video
        if source_type == "video":
            reader.close()
        else:
            reader.stop()
        
        # Đóng cửa sổ hiển thị
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main() 