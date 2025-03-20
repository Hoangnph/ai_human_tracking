"""Entry point chính của ứng dụng Retail Monitor.

Module này là điểm khởi đầu của ứng dụng, thực hiện việc nạp cấu hình,
khởi tạo các thành phần và điều phối luồng xử lý.

Example:
    Để chạy ứng dụng:

    ```bash
    python src/main.py
    ```
"""
import argparse
import sys
from pathlib import Path

from src.config import settings
from src.utils.logger import logger


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Retail Monitor - Hệ thống giám sát thông minh")
    parser.add_argument(
        "--env",
        type=str,
        choices=["development", "production", "testing"],
        default="development",
        help="Môi trường chạy (mặc định: development)",
    )
    parser.add_argument(
        "--video",
        type=str,
        default=None,
        help="Đường dẫn tới file video để xử lý (nếu không cung cấp, sẽ sử dụng camera)",
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        help="Camera ID để sử dụng (mặc định: 0)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["all", "detection", "face", "behavior"],
        default="all",
        help="Chế độ xử lý (mặc định: all)",
    )
    return parser.parse_args()


def check_environment():
    """Kiểm tra môi trường và hiển thị thông tin cấu hình."""
    logger.info(f"Starting {settings.app_name} in {settings.env} mode")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Using YOLO model: {settings.yolo_model}")
    logger.info(f"Models directory: {settings.models_dir}")
    logger.info(f"Faces directory: {settings.faces_dir}")
    logger.info(f"Videos directory: {settings.videos_dir}")
    
    # Kiểm tra thư mục dữ liệu
    for dir_path in [settings.models_dir, settings.faces_dir, settings.videos_dir]:
        if not dir_path.exists():
            logger.warning(f"Directory not found: {dir_path}")
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {dir_path}")


def main():
    """Hàm main của ứng dụng."""
    args = parse_args()
    
    # Kiểm tra môi trường
    check_environment()
    
    # Thông báo về tính năng sẽ được triển khai
    logger.info("Retail Monitor environment setup completed")
    logger.info("Ready to implement video processing and object detection modules")
    
    if args.video:
        video_path = Path(args.video)
        if not video_path.exists():
            logger.error(f"Video file not found: {video_path}")
            return
        logger.info(f"Video mode: Will process file {video_path} when implemented")
    else:
        logger.info(f"Camera mode: Will use camera ID {args.camera} when implemented")
    
    logger.info(f"Processing mode: {args.mode}")
    
    # Các module sẽ được triển khai ở các nhiệm vụ tiếp theo
    logger.info("Modules to be implemented:")
    logger.info("- Video processing")
    logger.info("- YOLO-based human detection")
    logger.info("- Object tracking")
    logger.info("- Face recognition")
    logger.info("- Behavior analysis")


if __name__ == "__main__":
    main() 