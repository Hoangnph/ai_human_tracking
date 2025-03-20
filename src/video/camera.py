"""Module cung cấp class để đọc video từ camera.

Class CameraReader cho phép đọc và xử lý video từ camera với các chức năng:
- Kết nối với camera thông qua ID hoặc URL
- Đọc frame theo frame
- Tùy chọn tiền xử lý frame

Example:
    >>> from src.video.camera import CameraReader
    >>> camera = CameraReader(camera_id=0)
    >>> camera.start()
    >>> while True:
    ...     frame = camera.read_frame()
    ...     if frame is None:
    ...         break
    ...     # Process frame
    >>> camera.stop()
"""
import time
from typing import Dict, Optional, Tuple, Union

import cv2
import numpy as np

from src.config import settings
from src.constants import CAMERA_READ_TIMEOUT_MS
from src.exceptions import VideoError
from src.utils.logger import logger
from src.video.utils import check_frame_valid, resize_frame


class CameraReader:
    """Class đọc và xử lý video từ camera.

    Attributes:
        camera_id: ID của camera hoặc URL stream
        resize_width: Chiều rộng resize (None = không resize)
        resize_height: Chiều cao resize (None = không resize)
        keep_aspect_ratio: Giữ tỷ lệ khung hình khi resize
        convert_to_rgb: Chuyển đổi từ BGR (OpenCV) sang RGB
        preprocessing: Có tiền xử lý frame hay không
        fps: FPS mong muốn (0 = không giới hạn)
        cap: Đối tượng VideoCapture của OpenCV
        is_running: Trạng thái hoạt động của camera
        info: Thông tin về camera (fps, width, height)
        last_frame_time: Thời điểm đọc frame cuối cùng
    """

    def __init__(
        self,
        camera_id: Union[int, str] = 0,
        resize_width: Optional[int] = None,
        resize_height: Optional[int] = None,
        keep_aspect_ratio: bool = True,
        convert_to_rgb: bool = False,
        preprocessing: bool = True,
        fps: int = 0,
    ):
        """Khởi tạo CameraReader.

        Args:
            camera_id: ID của camera (0, 1, ...) hoặc URL stream
            resize_width: Chiều rộng resize (None = không resize)
            resize_height: Chiều cao resize (None = không resize)
            keep_aspect_ratio: Giữ tỷ lệ khung hình khi resize
            convert_to_rgb: Chuyển đổi từ BGR (OpenCV) sang RGB
            preprocessing: Có tiền xử lý frame hay không
            fps: FPS mong muốn (0 = không giới hạn)
        """
        self.camera_id = camera_id
        self.resize_width = resize_width if resize_width is not None else settings.frame_width
        self.resize_height = resize_height if resize_height is not None else settings.frame_height
        self.keep_aspect_ratio = keep_aspect_ratio
        self.convert_to_rgb = convert_to_rgb
        self.preprocessing = preprocessing
        self.fps = fps
        self.cap = None
        self.is_running = False
        self.info = {}
        self.last_frame_time = 0
        self.frame_delay = 1.0 / fps if fps > 0 else 0

    def start(self) -> bool:
        """Bắt đầu đọc từ camera.

        Returns:
            True nếu kết nối thành công, False nếu thất bại

        Raises:
            VideoError: Nếu không thể kết nối với camera
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            
            # Đặt các thuộc tính camera
            if self.resize_width and self.resize_height:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resize_width)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resize_height)
            
            if self.fps > 0:
                self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            # Kiểm tra kết nối
            if not self.cap.isOpened():
                raise VideoError(f"Không thể kết nối với camera ID: {self.camera_id}", str(self.camera_id))
            
            # Đọc frame đầu tiên để kiểm tra
            ret, frame = self.cap.read()
            if not ret or frame is None:
                raise VideoError(f"Không thể đọc frame từ camera ID: {self.camera_id}", str(self.camera_id))
            
            # Lấy thông tin camera
            self._get_camera_info()
            
            self.is_running = True
            logger.info(f"Đã kết nối với camera ID: {self.camera_id}")
            logger.debug(f"Thông tin camera: {self.info}")
            
            self.last_frame_time = time.time()
            return True
        except Exception as e:
            logger.error(f"Lỗi khi kết nối với camera ID {self.camera_id}: {e}")
            if self.cap is not None:
                self.cap.release()
                self.cap = None
            self.is_running = False
            raise VideoError(f"Lỗi khi kết nối với camera: {e}", str(self.camera_id))

    def _get_camera_info(self) -> None:
        """Lấy thông tin camera.
        
        Populates self.info with camera properties.
        """
        if self.cap is None:
            return
        
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        # Nếu thông số không hợp lệ, sử dụng giá trị mặc định từ cấu hình
        if width <= 0:
            width = settings.frame_width
        if height <= 0:
            height = settings.frame_height
        if fps <= 0:
            fps = settings.fps
        
        self.info = {
            "width": width,
            "height": height,
            "fps": fps,
            "camera_id": self.camera_id,
        }

    def read_frame(self) -> Optional[np.ndarray]:
        """Đọc frame tiếp theo từ camera.

        Returns:
            Frame tiếp theo hoặc None nếu không thể đọc

        Raises:
            VideoError: Nếu có lỗi khi đọc frame
        """
        if not self.is_running or self.cap is None:
            return None

        # Thực hiện giới hạn FPS nếu cần
        if self.fps > 0:
            elapsed = time.time() - self.last_frame_time
            if elapsed < self.frame_delay:
                # Nếu chưa đủ thời gian, chờ
                time.sleep(self.frame_delay - elapsed)

        try:
            ret, frame = self.cap.read()
            if not ret or frame is None:
                logger.warning(f"Không thể đọc frame từ camera ID {self.camera_id}")
                return None

            self.last_frame_time = time.time()

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
        except Exception as e:
            logger.error(f"Lỗi khi đọc frame từ camera ID {self.camera_id}: {e}")
            return None

    def get_camera_property(self, property_id: int) -> float:
        """Lấy giá trị thuộc tính của camera.

        Args:
            property_id: ID thuộc tính (cv2.CAP_PROP_*)

        Returns:
            Giá trị thuộc tính hoặc 0 nếu không có sẵn
        """
        if not self.is_running or self.cap is None:
            return 0.0
        return self.cap.get(property_id)

    def set_camera_property(self, property_id: int, value: float) -> bool:
        """Đặt giá trị thuộc tính của camera.

        Args:
            property_id: ID thuộc tính (cv2.CAP_PROP_*)
            value: Giá trị cần đặt

        Returns:
            True nếu đặt thành công, False nếu thất bại
        """
        if not self.is_running or self.cap is None:
            return False
        return self.cap.set(property_id, value)

    def stop(self) -> None:
        """Dừng và giải phóng camera."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            self.is_running = False
            logger.info(f"Đã ngắt kết nối với camera ID: {self.camera_id}")

    def __enter__(self):
        """Context manager enter."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()

    def __del__(self):
        """Destructor."""
        self.stop()
