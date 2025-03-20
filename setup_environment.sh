#!/bin/bash
# Script thiết lập môi trường phát triển cho dự án giám sát thông minh
# Sử dụng Conda để tạo môi trường ảo và cài đặt các dependency

echo "Bắt đầu thiết lập môi trường phát triển..."

# Kiểm tra Conda đã được cài đặt hay chưa
if ! command -v conda &> /dev/null; then
    echo "Conda không được tìm thấy. Vui lòng cài đặt Conda trước khi chạy script này."
    exit 1
fi

# Tạo môi trường Conda
echo "Tạo môi trường Conda 'retail-monitor' với Python 3.9..."
conda create -n retail-monitor python=3.9 pip=23.0.1 -y

# Kích hoạt môi trường
echo "Kích hoạt môi trường..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate retail-monitor

# Cập nhật pip
echo "Cập nhật pip..."
pip install --upgrade pip

# Cài đặt các thư viện cốt lõi từng phần để dễ theo dõi lỗi
echo "Cài đặt thư viện YOLOv8..."
pip install ultralytics==8.0.20

echo "Cài đặt thư viện xử lý ảnh và số liệu..."
pip install opencv-python==4.7.0.72 numpy==1.24.3 Pillow==9.5.0

echo "Cài đặt thư viện face recognition..."
pip install face-recognition==1.3.0 dlib==19.24.0

echo "Cài đặt MediaPipe (phiên bản có sẵn)..."
pip install mediapipe==0.10.5

echo "Cài đặt các thư viện web và API..."
pip install fastapi==0.95.1 uvicorn==0.22.0 pydantic==1.10.7 python-multipart==0.0.6

echo "Cài đặt các thư viện cơ sở dữ liệu..."
pip install sqlalchemy==2.0.12 aiosqlite==0.19.0 

echo "Cài đặt thư viện giao diện và tiện ích..."
pip install streamlit==1.22.0 plotly==5.14.1 loguru==0.7.0 python-dotenv==1.0.0 pytest==7.3.1

# Cài đặt các dependencies tùy chọn (có thể không cần thiết cho MVP)
echo "Cài đặt các dependencies tùy chọn..."
pip install psycopg2-binary==2.9.6

# Lưu danh sách các package đã cài đặt
echo "Tạo file requirements.txt..."
pip freeze > requirements.txt

# Tạo file pyproject.toml
echo "Tạo file pyproject.toml..."
cat > pyproject.toml << EOF
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "retail-monitor"
version = "0.1.0"
description = "Hệ thống giám sát thông minh sử dụng YOLO, face-recognition và MediaPipe"
readme = "README.md"
authors = [
    {name = "AI_HUMAN_TRACKING Team"}
]
requires-python = ">=3.9"

[tool.black]
line-length = 88
target-version = ["py39"]

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true

[tool.pytest.ini_options]
minversion = "6.0"
testpaths = ["tests"]
EOF

echo "Thiết lập môi trường hoàn tất!"
echo "Để sử dụng môi trường này, chạy: conda activate retail-monitor" 