"""Module định nghĩa các exception tùy chỉnh cho ứng dụng.

Module này cung cấp các exception tùy chỉnh để xử lý lỗi trong các module khác
một cách nhất quán và có ý nghĩa.

Example:
    >>> from src.exceptions import VideoError, ModelLoadError
    >>> try:
    ...     # Some code that might fail
    ...     pass
    ... except VideoError as e:
    ...     print(f"Lỗi video: {e}")
"""
from typing import Any, Dict, Optional


class RetailMonitorError(Exception):
    """Exception cơ sở cho tất cả các exception trong ứng dụng."""

    def __init__(self, message: str = "Retail Monitor error occurred"):
        self.message = message
        super().__init__(self.message)


class ConfigError(RetailMonitorError):
    """Exception khi có lỗi liên quan đến cấu hình."""

    def __init__(self, message: str = "Configuration error"):
        super().__init__(message)


class VideoError(RetailMonitorError):
    """Exception khi có lỗi liên quan đến video."""

    def __init__(self, message: str = "Video processing error", source: Optional[str] = None):
        self.source = source
        msg = f"{message}" if source is None else f"{message} (source: {source})"
        super().__init__(msg)


class ModelLoadError(RetailMonitorError):
    """Exception khi không thể tải mô hình."""

    def __init__(self, model_name: str, message: str = "Failed to load model"):
        self.model_name = model_name
        super().__init__(f"{message}: {model_name}")


class DetectionError(RetailMonitorError):
    """Exception khi có lỗi trong quá trình phát hiện đối tượng."""

    def __init__(self, message: str = "Object detection error"):
        super().__init__(message)


class TrackingError(RetailMonitorError):
    """Exception khi có lỗi trong quá trình theo dõi đối tượng."""

    def __init__(self, message: str = "Object tracking error"):
        super().__init__(message)


class FaceRecognitionError(RetailMonitorError):
    """Exception khi có lỗi trong quá trình nhận diện khuôn mặt."""

    def __init__(self, message: str = "Face recognition error"):
        super().__init__(message)


class BehaviorAnalysisError(RetailMonitorError):
    """Exception khi có lỗi trong quá trình phân tích hành vi."""

    def __init__(self, message: str = "Behavior analysis error"):
        super().__init__(message)


class DatabaseError(RetailMonitorError):
    """Exception khi có lỗi liên quan đến cơ sở dữ liệu."""

    def __init__(self, message: str = "Database error"):
        super().__init__(message)


class APIError(RetailMonitorError):
    """Exception khi có lỗi trong API."""

    def __init__(
        self, 
        message: str = "API error", 
        status_code: int = 500, 
        details: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.details = details
        super().__init__(message) 