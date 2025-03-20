"""Test đơn giản cho VideoReader với video mẫu.

File này chứa các test đơn giản để kiểm tra chức năng của VideoReader
với video mẫu đã tạo. Tests này có thể chạy riêng không cần pytest.

Cách chạy:
    python tests/test_video_simple.py
"""
import os
import sys
from pathlib import Path

# Thêm thư mục gốc vào sys.path
sys.path.append(str(Path(__file__).parent.parent))

import cv2
import numpy as np

from src.utils.logger import logger
from src.video import VideoReader


def test_video_reader_basic():
    """Kiểm tra các chức năng cơ bản của VideoReader."""
    # Đường dẫn đến video mẫu
    video_path = "data/videos/sample.mp4"
    
    if not os.path.exists(video_path):
        logger.error(f"Không tìm thấy file video: {video_path}")
        return False
    
    logger.info(f"Bắt đầu kiểm tra VideoReader với file: {video_path}")
    
    # Tạo đối tượng VideoReader
    reader = VideoReader(
        video_path=video_path,
        resize_width=320,
        resize_height=240,
        keep_aspect_ratio=True
    )
    
    try:
        # Mở video
        reader.open()
        logger.info("Đã mở file video thành công")
        
        # Kiểm tra thông tin video
        logger.info("Thông tin video:")
        for key, value in reader.info.items():
            logger.info(f"  {key}: {value}")
        
        # Đọc và hiển thị 10 frame đầu tiên
        frame_count = 0
        for _ in range(10):
            frame = reader.read_frame()
            if frame is not None:
                frame_count += 1
                # Kiểm tra kích thước frame
                height, width = frame.shape[:2]
                logger.info(f"Frame {frame_count}: shape={width}x{height}")
            else:
                logger.warning("Không thể đọc frame")
                break
        
        # Kiểm tra seek
        logger.info("Kiểm tra chức năng seek...")
        
        # Seek đến vị trí 50%
        mid_frame = reader.info["total_frames"] // 2
        reader.set_frame(mid_frame)
        frame = reader.read_frame()
        if frame is not None:
            logger.info(f"Đã seek đến vị trí giữa, frame={reader.get_current_frame_number()}")
        else:
            logger.error("Không thể đọc frame sau khi seek")
        
        # Seek đến frame cụ thể
        target_frame = 100
        reader.set_frame(target_frame)
        frame = reader.read_frame()
        if frame is not None:
            logger.info(f"Đã seek đến frame {target_frame}, current_frame={reader.get_current_frame_number()}")
        else:
            logger.error(f"Không thể đọc frame sau khi seek đến frame {target_frame}")
        
        # Kiểm tra vị trí theo mili giây
        position_ms = reader.get_position_ms()
        logger.info(f"Vị trí hiện tại: {position_ms:.2f} ms")
        
        logger.info("Kiểm tra VideoReader thành công")
        return True
        
    except Exception as e:
        logger.error(f"Lỗi khi kiểm tra VideoReader: {e}")
        return False
    
    finally:
        # Đóng video
        reader.close()
        logger.info("Đã đóng file video")


if __name__ == "__main__":
    # Cấu hình logger cho console
    # logger.remove()
    # logger.add(sys.stdout, level="INFO")
    
    # Chạy test
    result = test_video_reader_basic()
    
    # Hiển thị kết quả
    if result:
        logger.success("✅ Tất cả các kiểm tra cho VideoReader đã pass")
    else:
        logger.error("❌ Có lỗi trong quá trình kiểm tra VideoReader") 