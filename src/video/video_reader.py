"""Module cung cấp class để đọc video từ file.

Class VideoReader cho phép đọc và xử lý video từ file với các chức năng:
- Đọc frame theo frame
- Thông tin về video (FPS, kích thước, tổng số frame)
- Tùy chọn tiền xử lý frame

Example:
    >>> from src.video.video_reader import VideoReader
    >>> reader = VideoReader("path/to/video.mp4")
    >>> reader.open()
    >>> while True:
    ...     frame = reader.read_frame()
    ...     if frame is None:
    ...         break
    ...     # Process frame
    >>> reader.close()
"""
import os
from pathlib import Path
from typing import Dict, Optional, Tuple, Union

import cv2
import numpy as np

from src.config import settings
from src.exceptions import VideoError
from src.utils.logger import logger
from src.video.utils import check_frame_valid, resize_frame


class VideoReader:
    """Class đọc và xử lý video từ file.

    Attributes:
        video_path: Đường dẫn tới file video
        resize_width: Chiều rộng resize (None = không resize)
        resize_height: Chiều cao resize (None = không resize)
        keep_aspect_ratio: Giữ tỷ lệ khung hình khi resize
        convert_to_rgb: Chuyển đổi từ BGR (OpenCV) sang RGB
        preprocessing: Có tiền xử lý frame hay không
        cap: Đối tượng VideoCapture của OpenCV
        is_opened: Trạng thái mở của video
        info: Thông tin về video (fps, width, height, total_frames)
    """

    def __init__(
        self,
        video_path: Union[str, Path],
        resize_width: Optional[int] = None,
        resize_height: Optional[int] = None,
        keep_aspect_ratio: bool = True,
        convert_to_rgb: bool = False,
        preprocessing: bool = True,
    ):
        """Khởi tạo VideoReader.

        Args:
            video_path: Đường dẫn tới file video
            resize_width: Chiều rộng resize (None = không resize)
            resize_height: Chiều cao resize (None = không resize)
            keep_aspect_ratio: Giữ tỷ lệ khung hình khi resize
            convert_to_rgb: Chuyển đổi từ BGR (OpenCV) sang RGB
            preprocessing: Có tiền xử lý frame hay không
        """
        self.video_path = Path(video_path)
        self.resize_width = resize_width
        self.resize_height = resize_height
        self.keep_aspect_ratio = keep_aspect_ratio
        self.convert_to_rgb = convert_to_rgb
        self.preprocessing = preprocessing
        self.cap = None
        self.is_opened = False
        self.info = {}

    def open(self) -> bool:
        """Mở file video.

        Returns:
            True nếu mở thành công, False nếu thất bại

        Raises:
            VideoError: Nếu file không tồn tại hoặc không thể mở
        """
        if not os.path.exists(self.video_path):
            raise VideoError(f"File video không tồn tại: {self.video_path}", str(self.video_path))

        try:
            self.cap = cv2.VideoCapture(str(self.video_path))
            self.is_opened = self.cap.isOpened()

            if not self.is_opened:
                raise VideoError(f"Không thể mở file video: {self.video_path}", str(self.video_path))

            # Lấy thông tin video
            self._get_video_info()
            logger.info(f"Đã mở file video: {self.video_path}")
            logger.debug(f"Thông tin video: {self.info}")
            return True
        except Exception as e:
            logger.error(f"Lỗi khi mở file video {self.video_path}: {e}")
            self.is_opened = False
            raise VideoError(f"Lỗi khi mở file video: {e}", str(self.video_path))

    def _get_video_info(self) -> None:
        """Lấy thông tin video từ file.
        
        Populates self.info with video properties.
        """
        if not self.is_opened or self.cap is None:
            return
        
        # Lấy thông tin cơ bản
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        codec = int(self.cap.get(cv2.CAP_PROP_FOURCC))
        
        # Decode codec thành chuỗi
        codec_str = ''.join([chr((codec >> 8 * i) & 0xFF) for i in range(4)])
        
        self.info = {
            "width": width,
            "height": height,
            "fps": fps,
            "total_frames": total_frames,
            "codec": codec_str,
            "duration": total_frames / fps if fps > 0 else 0,  # Thời lượng tính bằng giây
        }

    def read_frame(self) -> Optional[np.ndarray]:
        """Đọc frame tiếp theo từ video.

        Returns:
            Frame tiếp theo hoặc None nếu hết video
        """
        if not self.is_opened or self.cap is None:
            return None

        ret, frame = self.cap.read()
        if not ret or frame is None:
            return None

        # Xử lý frame nếu cần
        if self.preprocessing:
            # Resize nếu có kích thước mục tiêu
            if self.resize_width is not None and self.resize_height is not None:
                frame = resize_frame(
                    frame, 
                    self.resize_width, 
                    self.resize_height,
                    self.keep_aspect_ratio
                )
            
            # Chuyển sang RGB nếu cần
            if self.convert_to_rgb:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return frame

    def set_position(self, position_ms: int) -> bool:
        """Đặt vị trí đọc của video.

        Args:
            position_ms: Vị trí tính bằng mili giây

        Returns:
            True nếu đặt thành công, False nếu thất bại
        """
        if not self.is_opened or self.cap is None:
            return False
        return self.cap.set(cv2.CAP_PROP_POS_MSEC, position_ms)

    def set_frame(self, frame_number: int) -> bool:
        """Đặt frame hiện tại của video.

        Args:
            frame_number: Số thứ tự frame cần đặt

        Returns:
            True nếu đặt thành công, False nếu thất bại
        """
        if not self.is_opened or self.cap is None:
            return False
        return self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    def get_position_ms(self) -> float:
        """Lấy vị trí hiện tại của video tính bằng mili giây.

        Returns:
            Vị trí hiện tại tính bằng mili giây
        """
        if not self.is_opened or self.cap is None:
            return 0.0
        return self.cap.get(cv2.CAP_PROP_POS_MSEC)

    def get_current_frame_number(self) -> int:
        """Lấy số thứ tự frame hiện tại.

        Returns:
            Số thứ tự frame hiện tại
        """
        if not self.is_opened or self.cap is None:
            return 0
        return int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

    def close(self) -> None:
        """Đóng video."""
        if self.cap is not None:
            self.cap.release()
            self.is_opened = False
            logger.info(f"Đã đóng file video: {self.video_path}")

    def __enter__(self):
        """Context manager enter."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def __del__(self):
        """Destructor."""
        self.close()
