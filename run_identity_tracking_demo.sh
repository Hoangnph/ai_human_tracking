#!/bin/bash

# Script để chạy demo theo dõi danh tính (Identity Tracking Demo)
# Script này hiển thị cách duy trì danh tính của người qua thời gian

# Thiết lập đường dẫn cơ bản
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"
PYTHON_ENV_DIR="$PROJECT_ROOT/venv"

# Kiểm tra và kích hoạt môi trường Python
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "🔄 Môi trường ảo Python chưa được kích hoạt."
    
    # Kiểm tra xem môi trường venv tồn tại không
    if [ -d "$PYTHON_ENV_DIR" ] && [ -f "$PYTHON_ENV_DIR/bin/activate" ]; then
        echo "🔄 Tự động kích hoạt môi trường ảo từ: $PYTHON_ENV_DIR"
        source "$PYTHON_ENV_DIR/bin/activate"
    else
        echo "⚠️ Không tìm thấy môi trường ảo tại $PYTHON_ENV_DIR"
        echo "⚠️ Tiếp tục chạy mà không có môi trường ảo. Có thể gặp vấn đề với dependencies."
    fi
fi

# Kiểm tra database khuôn mặt đã sửa
if [ -f "data/faces/database_fixed.pkl" ]; then
    # Sao lưu database hiện tại nếu cần
    if [ -f "data/faces/database.pkl" ]; then
        echo "🔄 Sao lưu database cũ tại data/faces/database.bak.pkl"
        cp data/faces/database.pkl data/faces/database.bak.pkl
    fi
    
    # Sử dụng database đã sửa
    echo "🔄 Sử dụng database đã sửa tại data/faces/database_fixed.pkl"
    cp data/faces/database_fixed.pkl data/faces/database.pkl
else
    echo "⚠️ Cảnh báo: Không tìm thấy database đã sửa."
    echo "⚠️ Sử dụng database hiện tại (nếu có). Có thể gặp vấn đề với nhận diện khuôn mặt."
fi

# Kiểm tra xem thư mục data/videos có tồn tại không
if [ ! -d "data/videos" ]; then
    echo "❌ Lỗi: Thư mục data/videos không tồn tại."
    echo "Vui lòng tạo thư mục data/videos và thêm các video mẫu."
    exit 1
fi

# Xử lý tham số --full=true
FULL_VIDEO=false
for arg in "$@"; do
  if [[ "$arg" == "--full=true" ]]; then
    FULL_VIDEO=true
    break
  fi
done

# Đặt biến video mặc định
DEFAULT_VIDEO="data/videos/sample.mp4"
VIDEO=${1:-$DEFAULT_VIDEO}
# Nếu tham số đầu tiên bắt đầu bằng "--", sử dụng video mặc định
if [[ "$VIDEO" == --* ]]; then
    VIDEO=$DEFAULT_VIDEO
fi

# Kiểm tra tồn tại video
if [ ! -f "$VIDEO" ]; then
    echo "❌ Lỗi: Video không tồn tại: $VIDEO"
    echo "Vui lòng kiểm tra lại đường dẫn video."
    exit 1
fi

# Thông báo bắt đầu
echo "🎬 Chạy Demo Theo Dõi Danh Tính"
echo "Video: $VIDEO"
if [ "$FULL_VIDEO" = true ]; then
    echo "Chế độ: Xem toàn bộ video (không giới hạn số frame)"
else
    echo "Chế độ: Giới hạn 100 frame (mặc định)"
fi
echo "Lưu ý: Bấm phím ESC để thoát."
echo "Bắt đầu demo..."

# Tham số max_frames tùy theo chế độ full video
MAX_FRAMES_PARAM=""
if [ "$FULL_VIDEO" = false ]; then
    MAX_FRAMES_PARAM="--max-frames 100"
fi

# Chạy script với các tham số
python -m src.demos.identity_tracking_demo \
    --video "$VIDEO" \
    --detection-model yolov8n \
    --conf 0.35 \
    --face-model lbp \
    --face-detector haarcascade \
    --tolerance 0.18 \
    --detection-interval 3 \
    --face-detection-interval 2 \
    --resize-factor 0.6 \
    $MAX_FRAMES_PARAM \
    --debug

# Kiểm tra kết quả
if [ $? -eq 0 ]; then
    echo "✅ Demo hoàn tất thành công."
else
    echo "❌ Demo bị lỗi. Vui lòng kiểm tra log."
    exit 1
fi 