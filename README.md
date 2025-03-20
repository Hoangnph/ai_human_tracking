# Retail Monitor

Hệ thống giám sát thông minh sử dụng YOLOv8, face-recognition và MediaPipe để phát hiện người, nhận diện danh tính và phân tích hành vi trong môi trường bán lẻ.

## Thiết lập

1. Clone repository:
```bash
git clone <repo-url>
cd retail-monitor
```

2. Thiết lập môi trường:
```bash
chmod +x setup_environment.sh
./setup_environment.sh
```

3. Kích hoạt môi trường:
```bash
conda activate retail-monitor
```

## Sử dụng

Chạy ứng dụng:
```bash
python src/main.py
```

## Cấu trúc dự án

```
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
```

## License

[MIT License](LICENSE)
