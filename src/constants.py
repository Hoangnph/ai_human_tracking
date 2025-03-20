"""Module chứa các hằng số sử dụng trong ứng dụng.

Module này định nghĩa các hằng số, enum, và giá trị cố định được sử dụng
xuyên suốt trong ứng dụng.

Example:
    >>> from src.constants import PERSON_CLASS_ID, COLORS, IdentityType
    >>> print(PERSON_CLASS_ID)  # 0
    >>> print(COLORS["red"])  # (255, 0, 0)
"""
from enum import Enum, auto
from typing import Dict, List, Tuple

# YOLOv8 class IDs
PERSON_CLASS_ID = 0

# Ngưỡng tin cậy mặc định cho phát hiện người
DEFAULT_CONFIDENCE_THRESHOLD = 0.5

# Ngưỡng IoU (Intersection over Union) cho NMS
DEFAULT_IOU_THRESHOLD = 0.45

# Ngưỡng tin cậy cho nhận diện khuôn mặt
DEFAULT_FACE_RECOGNITION_TOLERANCE = 0.6

# Cấu hình khung video
DEFAULT_FRAME_WIDTH = 640
DEFAULT_FRAME_HEIGHT = 480
DEFAULT_FPS = 30

# Thời gian chờ tối đa (ms) cho việc đọc frame từ camera
CAMERA_READ_TIMEOUT_MS = 5000

# Màu sắc sử dụng cho visualization (BGR format cho OpenCV)
COLORS: Dict[str, Tuple[int, int, int]] = {
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "yellow": (0, 255, 255),
    "magenta": (255, 0, 255),
    "cyan": (255, 255, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
}

# Các loại font cho visualization
FONT = {
    "face": 0,  # FONT_HERSHEY_SIMPLEX
    "scale": 0.8,
    "thickness": 2,
}


class IdentityType(str, Enum):
    """Enum định nghĩa các loại danh tính."""

    EMPLOYEE = "employee"
    KNOWN_CUSTOMER = "known_customer"
    UNKNOWN = "unknown"


class BehaviorType(str, Enum):
    """Enum định nghĩa các loại hành vi được phát hiện."""

    STANDING = "standing"
    WALKING = "walking"
    SITTING = "sitting"
    PRODUCT_INTERACTION = "product_interaction"
    EMPLOYEE_INTERACTION = "employee_interaction"
    UNKNOWN = "unknown"


# Mapping màu sắc cho các loại danh tính và hành vi
IDENTITY_COLORS = {
    IdentityType.EMPLOYEE: COLORS["blue"],
    IdentityType.KNOWN_CUSTOMER: COLORS["green"],
    IdentityType.UNKNOWN: COLORS["red"],
}

BEHAVIOR_COLORS = {
    BehaviorType.STANDING: COLORS["white"],
    BehaviorType.WALKING: COLORS["cyan"],
    BehaviorType.SITTING: COLORS["yellow"],
    BehaviorType.PRODUCT_INTERACTION: COLORS["magenta"],
    BehaviorType.EMPLOYEE_INTERACTION: COLORS["green"],
    BehaviorType.UNKNOWN: COLORS["white"],
}

# Cấu hình MediaPipe Pose
MEDIAPIPE_POSE_LANDMARKS = [
    "nose",
    "left_eye_inner",
    "left_eye",
    "left_eye_outer",
    "right_eye_inner",
    "right_eye",
    "right_eye_outer",
    "left_ear",
    "right_ear",
    "mouth_left",
    "mouth_right",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_pinky",
    "right_pinky",
    "left_index",
    "right_index",
    "left_thumb",
    "right_thumb",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
    "left_heel",
    "right_heel",
    "left_foot_index",
    "right_foot_index",
] 