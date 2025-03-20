"""Module cung cấp cấu hình cho ứng dụng.

Module này sử dụng thư viện pydantic và python-dotenv để quản lý cấu hình 
từ file YAML và biến môi trường.

Example:
    >>> from src.config import settings
    >>> print(settings.app_name)
    >>> print(settings.models_dir)
"""
import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from dotenv import load_dotenv
from pydantic import BaseSettings, Field, validator

from src.utils.logger import logger

# Load biến môi trường từ file .env
load_dotenv()

# Đường dẫn gốc của dự án
ROOT_DIR = Path(__file__).parent.parent.absolute()


class EnvironmentType(str, Enum):
    """Enum định nghĩa các môi trường."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class Settings(BaseSettings):
    """Class quản lý cấu hình ứng dụng.

    Attributes:
        env: Môi trường (development, production, testing)
        app_name: Tên ứng dụng
        models_dir: Thư mục chứa các mô hình
        faces_dir: Thư mục chứa dữ liệu khuôn mặt
        videos_dir: Thư mục chứa video test
        database_url: URL kết nối cơ sở dữ liệu
        log_level: Mức log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        yolo_model: Tên mô hình YOLO sử dụng
        yolo_confidence: Ngưỡng confidence cho phát hiện người
        face_recognition_tolerance: Ngưỡng tolerance cho nhận diện khuôn mặt
    """

    # Cấu hình cơ bản
    env: EnvironmentType = Field(EnvironmentType.DEVELOPMENT, env="ENV")
    app_name: str = "Retail Monitor"

    # Đường dẫn
    models_dir: Path = Field(ROOT_DIR / "data" / "models", env="MODELS_DIR")
    faces_dir: Path = Field(ROOT_DIR / "data" / "faces", env="FACES_DIR")
    videos_dir: Path = Field(ROOT_DIR / "data" / "videos", env="VIDEOS_DIR")

    # Cơ sở dữ liệu
    database_url: str = Field("sqlite:///./data/app.db", env="DATABASE_URL")

    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")

    # Cấu hình YOLO
    yolo_model: str = "yolov8n.pt"
    yolo_confidence: float = 0.5

    # Cấu hình Face Recognition
    face_recognition_tolerance: float = 0.6

    # Cấu hình MediaPipe
    mediapipe_confidence: float = 0.5

    # Cấu hình stream
    default_camera_id: int = 0
    frame_width: int = 640
    frame_height: int = 480
    fps: int = 30

    @validator("models_dir", "faces_dir", "videos_dir", pre=True)
    def validate_path(cls, value):
        """Xác thực đường dẫn và chuyển thành Path object."""
        if isinstance(value, str):
            path = Path(value)
        else:
            path = value
        
        # Đảm bảo thư mục tồn tại
        path.mkdir(parents=True, exist_ok=True)
        
        return path


def load_yaml_config(env: EnvironmentType) -> Dict[str, Any]:
    """Nạp cấu hình từ file YAML dựa trên môi trường.

    Args:
        env: Môi trường (development, production)

    Returns:
        Dict[str, Any]: Dữ liệu cấu hình từ file YAML
    """
    config_file = ROOT_DIR / "config" / f"{env}.yaml"
    default_config_file = ROOT_DIR / "config" / "default.yaml"

    config_data = {}

    # Đọc cấu hình mặc định
    if default_config_file.exists():
        with open(default_config_file, "r") as f:
            try:
                config_data.update(yaml.safe_load(f) or {})
            except yaml.YAMLError as e:
                logger.error(f"Lỗi khi đọc file cấu hình mặc định: {e}")

    # Đọc cấu hình môi trường cụ thể
    if config_file.exists():
        with open(config_file, "r") as f:
            try:
                env_config = yaml.safe_load(f) or {}
                config_data.update(env_config)
            except yaml.YAMLError as e:
                logger.error(f"Lỗi khi đọc file cấu hình {env}: {e}")

    return config_data


# Xác định môi trường từ biến môi trường
env = os.environ.get("ENV", "development")
env_type = EnvironmentType(env)

# Nạp cấu hình từ file YAML
yaml_config = load_yaml_config(env_type)

# Tạo đối tượng settings
settings = Settings(**yaml_config)

logger.info(f"Đã nạp cấu hình cho môi trường: {settings.env}")
logger.debug(f"Thư mục mô hình: {settings.models_dir}")
logger.debug(f"Thư mục dữ liệu khuôn mặt: {settings.faces_dir}")
logger.debug(f"Thư mục video: {settings.videos_dir}") 