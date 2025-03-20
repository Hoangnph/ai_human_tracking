"""Module cung cấp thiết lập logging cho toàn bộ ứng dụng.

Module này sử dụng thư viện loguru để cung cấp logging đồng nhất và linh hoạt,
với khả năng ghi log ra console và file.

Example:
    >>> from src.utils.logger import logger
    >>> logger.info("Đã khởi tạo ứng dụng")
    >>> logger.error("Lỗi kết nối camera")
"""
import os
import sys
from datetime import datetime
from typing import Dict, Optional, Union

from loguru import logger as loguru_logger

# Xóa handler mặc định của loguru
loguru_logger.remove()

# Format các message log
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# Thư mục logs
LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../logs"))
os.makedirs(LOGS_DIR, exist_ok=True)

# Tên file log dựa theo ngày
log_filename = os.path.join(LOGS_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log")


def setup_logger(
    level: Union[str, int] = "INFO",
    rotation: str = "1 day",
    retention: str = "1 month",
    log_to_console: bool = True,
    log_to_file: bool = True,
    diagnose: bool = True,
) -> None:
    """Thiết lập cấu hình logger.

    Args:
        level: Mức log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        rotation: Cấu hình rotation log file ("100 MB", "1 day",...)
        retention: Thời gian giữ log file ("1 week", "1 month",...)
        log_to_console: Có ghi log ra console không
        log_to_file: Có ghi log ra file không
        diagnose: Có bật diagnose mode không (lưu thêm traceback đầy đủ)
    """
    # Thêm handler console nếu cần
    if log_to_console:
        loguru_logger.add(
            sys.stderr,
            format=LOG_FORMAT,
            level=level,
            diagnose=diagnose,
            backtrace=diagnose,
        )

    # Thêm handler file nếu cần
    if log_to_file:
        loguru_logger.add(
            log_filename,
            format=LOG_FORMAT,
            level=level,
            rotation=rotation,
            retention=retention,
            compression="zip",
            diagnose=diagnose,
            backtrace=diagnose,
        )


# Thiết lập logger với cấu hình mặc định
# Đọc level từ biến môi trường hoặc sử dụng mặc định
log_level = os.environ.get("LOG_LEVEL", "INFO")
setup_logger(level=log_level)

# Export logger để sử dụng trong các module khác
logger = loguru_logger 