"""Script demo for testing video module.

Cách chạy:
    python src/video_demo.py --video data/videos/sample.mp4
    
    Hoặc sử dụng camera:
    python src/video_demo.py --camera 0
"""
import argparse
import time
import sys
from pathlib import Path

# Thêm thư mục gốc của dự án vào sys.path
sys.path.append(str(Path(__file__).parent.parent))

import cv2
import numpy as np

from utils.logger import logger
from video import CameraReader, VideoReader, add_text_to_frame, estimate_fps


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Video Module Demo")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--video", type=str, help="Path to video file")
    group.add_argument("--camera", type=int, help="Camera ID")
    parser.add_argument("--width", type=int, default=640, help="Display width")
    parser.add_argument("--height", type=int, default=480, help="Display height")
    return parser.parse_args()


def display_video_info(info):
    """Display video information."""
    logger.info("Video Information:")
    for key, value in info.items():
        logger.info(f"  {key}: {value}")


def main():
    """Main function."""
    args = parse_args()
    
    # Tùy thuộc vào nguồn input, sử dụng VideoReader hoặc CameraReader
    if args.video:
        logger.info(f"Reading from video file: {args.video}")
        reader = VideoReader(
            args.video,
            resize_width=args.width,
            resize_height=args.height,
            keep_aspect_ratio=True
        )
        source_type = "video"
    else:
        logger.info(f"Reading from camera: {args.camera}")
        reader = CameraReader(
            camera_id=args.camera,
            resize_width=args.width,
            resize_height=args.height
        )
        source_type = "camera"
    
    try:
        # Mở nguồn video
        if source_type == "video":
            reader.open()
        else:
            reader.start()
        
        # Hiển thị thông tin
        display_video_info(reader.info)
        
        # Tạo cửa sổ hiển thị
        window_name = "Video Demo"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        
        # Biến đếm thống kê
        start_time = time.time()
        frame_count = 0
        
        # Đọc và hiển thị video
        while True:
            # Đọc frame
            frame = reader.read_frame()
            
            # Kiểm tra frame hợp lệ
            if frame is None:
                logger.info("End of video or failed to read frame")
                break
            
            # Cập nhật bộ đếm
            frame_count += 1
            elapsed_time = time.time() - start_time
            
            # Tính FPS
            fps = estimate_fps(frame_count, elapsed_time)
            
            # Hiển thị thông tin trên frame
            frame = add_text_to_frame(
                frame, 
                f"Source: {source_type} | Frame: {frame_count} | FPS: {fps:.2f}",
                (10, 30),
                color=(0, 255, 0)
            )
            
            # Hiển thị frame
            cv2.imshow(window_name, frame)
            
            # Thoát nếu nhấn ESC
            key = cv2.waitKey(1)
            if key == 27:  # ESC
                logger.info("ESC pressed, exiting...")
                break
        
        # Hiển thị thống kê
        logger.info(f"Processed {frame_count} frames in {elapsed_time:.2f} seconds")
        logger.info(f"Average FPS: {fps:.2f}")
        
    except Exception as e:
        logger.error(f"Error processing video: {e}")
    
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