#!/bin/bash
# Script thiết lập cấu trúc thư mục dự án
# Tạo các thư mục cần thiết theo kiến trúc đã đề xuất

echo "Bắt đầu thiết lập cấu trúc dự án..."

# Tạo các thư mục chính
mkdir -p config
mkdir -p data/faces/{employees,known_customers}
mkdir -p data/models/yolo
mkdir -p data/videos
mkdir -p docs
mkdir -p logs
mkdir -p src/{video,detection,tracking,face_recognition,behavior,database,api,ui,utils}
mkdir -p tests

# Tạo các file __init__.py cho mỗi package
find src -type d -exec touch {}/__init__.py \;

# Tạo các file chính
touch src/main.py
touch src/config.py
touch src/constants.py
touch src/exceptions.py

# Tạo các file module
# Video module
touch src/video/camera.py
touch src/video/video_reader.py
touch src/video/video_writer.py
touch src/video/utils.py

# Detection module
touch src/detection/yolo_detector.py
touch src/detection/utils.py

# Tracking module
touch src/tracking/byte_tracker.py
touch src/tracking/object_tracker.py

# Face recognition module
touch src/face_recognition/face_detector.py
touch src/face_recognition/face_encoder.py
touch src/face_recognition/face_matcher.py
touch src/face_recognition/face_database.py

# Behavior module
touch src/behavior/pose_detector.py
touch src/behavior/hand_detector.py
touch src/behavior/action_classifier.py
touch src/behavior/behavior_rules.py

# Database module
touch src/database/models.py
touch src/database/crud.py
touch src/database/database.py

# API module
touch src/api/schemas.py
touch src/api/dependencies.py
mkdir -p src/api/routes
touch src/api/routes/__init__.py
touch src/api/routes/base.py

# UI module
touch src/ui/dashboard.py
touch src/ui/video_display.py

# Utils module
touch src/utils/logger.py
touch src/utils/profiler.py
touch src/utils/visualization.py

# Tạo các file cấu hình
touch config/default.yaml
touch config/development.yaml
touch config/production.yaml

# Tạo file .env.example
cat > .env.example << EOF
# Environment configuration
ENV=development

# Database
DATABASE_URL=sqlite:///./data/app.db

# Paths
MODELS_DIR=./data/models
FACES_DIR=./data/faces
VIDEOS_DIR=./data/videos

# Logging
LOG_LEVEL=INFO
EOF

# Tạo file .gitignore
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
.conda/
.python-version

# IDE
.idea/
.vscode/
*.swp
*.swo
.DS_Store

# Project specific
logs/*.log
data/videos/*
!data/videos/.gitkeep
data/faces/*
!data/faces/.gitkeep
!data/faces/employees/.gitkeep
!data/faces/known_customers/.gitkeep

# Keep empty directories
!/**/.gitkeep
EOF

# Tạo các .gitkeep để giữ cấu trúc thư mục trống
find data -type d -empty -exec touch {}/.gitkeep \;
find logs -type d -empty -exec touch {}/.gitkeep \;

# Tạo README.md cơ bản
cat > README.md << EOF
# Retail Monitor

Hệ thống giám sát thông minh sử dụng YOLOv8, face-recognition và MediaPipe để phát hiện người, nhận diện danh tính và phân tích hành vi trong môi trường bán lẻ.

## Thiết lập

1. Clone repository:
\`\`\`bash
git clone <repo-url>
cd retail-monitor
\`\`\`

2. Thiết lập môi trường:
\`\`\`bash
chmod +x setup_environment.sh
./setup_environment.sh
\`\`\`

3. Kích hoạt môi trường:
\`\`\`bash
conda activate retail-monitor
\`\`\`

## Sử dụng

Chạy ứng dụng:
\`\`\`bash
python src/main.py
\`\`\`

## Cấu trúc dự án

\`\`\`
retail-monitor/
├── config/                     # Configuration files
├── data/                       # Data files
│   ├── faces/                  # Face database
│   ├── models/                 # Pre-trained models
│   └── videos/                 # Test videos
├── docs/                       # Documentation
├── logs/                       # Log files
├── src/                        # Source code
│   ├── main.py                 # Entry point
│   ├── video/                  # Video module
│   ├── detection/              # Detection module
│   ├── face_recognition/       # Face recognition module
│   ├── behavior/               # Behavior analysis module
│   ├── database/               # Database module
│   ├── api/                    # API module
│   ├── ui/                     # UI module
│   └── utils/                  # Utilities
└── tests/                      # Test code
\`\`\`

## License

[MIT License](LICENSE)
EOF

# Cập nhật quyền chạy
chmod +x setup_environment.sh

echo "Thiết lập cấu trúc dự án hoàn tất!" 