# Tài liệu Kiến trúc Giải pháp (Solution Architecture)

## 1. Tổng quan giải pháp

### 1.1 Mục tiêu
Xây dựng hệ thống giám sát thông minh cho cửa hàng bán lẻ, tích hợp các công nghệ computer vision tiên tiến để phát hiện người, nhận diện danh tính và phân tích hành vi, từ đó cung cấp insights cho việc quản lý cửa hàng.

### 1.2 Lưu ý về YOLOv11
Hiện tại (tính đến năm 2023), phiên bản YOLO mới nhất được phát hành chính thức là YOLOv8 từ Ultralytics. Chưa có phiên bản YOLOv11 chính thức. Giải pháp này sẽ sử dụng YOLOv8 - phiên bản mới và ổn định nhất hiện nay.

### 1.3 Kiến trúc tổng thể
Hệ thống được thiết kế theo kiến trúc module, với luồng xử lý tuần tự:

```
Video Input → Phát hiện người (YOLO) → Theo dõi đối tượng → Nhận diện khuôn mặt → Phân tích hành vi → Lưu trữ và phân tích → Hiển thị/Báo cáo
```

## 2. Môi trường Phát triển và Triển khai

### 2.1 Môi trường ảo Python
Sử dụng Conda làm môi trường ảo chính:

```
name: retail-monitor
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - pip=22.3
```

Lý do sử dụng Python 3.9:
- Tương thích tốt với tất cả thư viện cần thiết
- Ổn định và được hỗ trợ rộng rãi
- Cân bằng giữa các tính năng mới và khả năng tương thích ngược

### 2.2 Các thư viện chính và phiên bản

```
# Core Libraries
ultralytics==8.0.20  # YOLOv8
opencv-python==4.7.0.72
numpy==1.24.3
Pillow==9.5.0

# Face Recognition
face-recognition==1.3.0
dlib==19.24.0

# Pose Estimation
mediapipe==0.10.0

# Object Tracking
ByteTrack==0.3.2  # hoặc DeepSORT

# Backend/API
fastapi==0.95.1
uvicorn==0.22.0
pydantic==1.10.7
python-multipart==0.0.6

# Database
sqlalchemy==2.0.12
psycopg2-binary==2.9.6 # For PostgreSQL
aiosqlite==0.19.0  # For SQLite with async support

# Visualization & UI
streamlit==1.22.0  # For MVP
plotly==5.14.1

# Utilities
loguru==0.7.0  # Enhanced logging
python-dotenv==1.0.0  # Environment variables
pytest==7.3.1  # Testing
```

### 2.3 Yêu cầu phần cứng
- **CPU**: Intel i7 thế hệ 10+ hoặc AMD Ryzen 7 3700X+
- **RAM**: 16GB+
- **GPU**: NVIDIA RTX 2060+ (6GB+ VRAM) 
- **Lưu trữ**: SSD 256GB+ cho hệ thống, HDD/SSD 1TB+ cho lưu trữ video

## 3. Kiến trúc Phần mềm

### 3.1 Cấu trúc dự án

```
retail-monitor/
├── .github/                     # CI/CD configurations
├── config/                      # Configuration files
│   ├── default.yaml             # Default configuration
│   ├── development.yaml         # Development environment settings
│   └── production.yaml          # Production environment settings
├── data/                        # Data files
│   ├── faces/                   # Face database
│   │   ├── employees/           # Employee face encodings
│   │   └── known_customers/     # Known customer face encodings
│   ├── models/                  # Pre-trained models
│   │   ├── yolo/                # YOLO models
│   │   └── behavior/            # Behavior classification models
│   └── videos/                  # Test videos
├── docs/                        # Documentation
├── logs/                        # Log files
├── src/                         # Source code
│   ├── __init__.py
│   ├── main.py                  # Application entry point
│   ├── config.py                # Configuration loader
│   ├── constants.py             # Application constants
│   ├── exceptions.py            # Custom exception classes
│   ├── video/                   # Video processing module
│   │   ├── __init__.py
│   │   ├── camera.py            # Camera interface
│   │   ├── video_reader.py      # Video file reader
│   │   └── video_writer.py      # Video writer for saving results
│   ├── detection/               # Object detection module
│   │   ├── __init__.py
│   │   ├── yolo_detector.py     # YOLO implementation
│   │   └── utils.py             # Detection utilities
│   ├── tracking/                # Object tracking module
│   │   ├── __init__.py
│   │   ├── byte_tracker.py      # ByteTrack implementation
│   │   └── object_tracker.py    # Tracking interface
│   ├── face_recognition/        # Face recognition module
│   │   ├── __init__.py
│   │   ├── face_detector.py     # Face detection
│   │   ├── face_encoder.py      # Face encoding
│   │   ├── face_matcher.py      # Face matching
│   │   └── face_database.py     # Face database management
│   ├── behavior/                # Behavior analysis module
│   │   ├── __init__.py
│   │   ├── pose_detector.py     # MediaPipe pose implementation
│   │   ├── hand_detector.py     # MediaPipe hands implementation
│   │   ├── action_classifier.py # Action classification
│   │   └── behavior_rules.py    # Rule-based behavior analysis
│   ├── database/                # Database module
│   │   ├── __init__.py
│   │   ├── models.py            # Database models
│   │   ├── crud.py              # CRUD operations
│   │   └── database.py          # Database connection
│   ├── api/                     # API module
│   │   ├── __init__.py
│   │   ├── routes/              # API routes
│   │   ├── schemas.py           # API schemas
│   │   └── dependencies.py      # API dependencies
│   ├── ui/                      # User interface module
│   │   ├── __init__.py
│   │   ├── dashboard.py         # Dashboard UI
│   │   └── video_display.py     # Video display UI
│   └── utils/                   # Utilities
│       ├── __init__.py
│       ├── logger.py            # Logging utility
│       ├── profiler.py          # Performance profiling
│       └── visualization.py     # Visualization utilities
├── tests/                       # Test code
│   ├── __init__.py
│   ├── conftest.py              # Test configuration
│   ├── test_detection.py
│   ├── test_tracking.py
│   ├── test_face_recognition.py
│   └── test_behavior.py
├── .gitignore
├── .env.example                 # Example environment variables
├── pyproject.toml               # Project metadata and dependencies
├── setup.py                     # Installation script
└── README.md                    # Project documentation
```

### 3.2 Mô tả module

#### 3.2.1 Module Video
- **Chức năng**: Xử lý đầu vào video từ nhiều nguồn (camera, file, streaming)
- **Đầu vào**: URL camera, đường dẫn file video, hoặc stream URL
- **Luồng xử lý**: 
  1. Khởi tạo kết nối với nguồn video
  2. Đọc từng frame theo thời gian thực
  3. Tiền xử lý frame (resize, normalize)
- **Đầu ra**: Frame video đã tiền xử lý

#### 3.2.2 Module Phát hiện
- **Chức năng**: Phát hiện người trong mỗi frame video
- **Đầu vào**: Frame video từ module Video
- **Luồng xử lý**:
  1. Áp dụng YOLOv8 để phát hiện người
  2. Lọc các detection với confidence thấp
  3. Chuẩn hóa bounding box
- **Đầu ra**: Danh sách vị trí (bounding boxes) của tất cả người trong frame

#### 3.2.3 Module Theo dõi
- **Chức năng**: Theo dõi người qua các frame liên tiếp
- **Đầu vào**: Frame video và bounding boxes từ module Phát hiện
- **Luồng xử lý**:
  1. Áp dụng ByteTrack để liên kết người qua các frame
  2. Duy trì ID và quỹ đạo cho mỗi người
  3. Xử lý occlusion và re-identification
- **Đầu ra**: Danh sách người với unique ID và thông tin quỹ đạo

#### 3.2.4 Module Nhận diện Khuôn mặt
- **Chức năng**: Nhận diện khuôn mặt và xác định danh tính
- **Đầu vào**: Frame video và bounding boxes của người từ module Theo dõi
- **Luồng xử lý**:
  1. Phát hiện khuôn mặt trong mỗi bounding box
  2. Trích xuất đặc trưng khuôn mặt (encoding)
  3. So sánh với database khuôn mặt đã biết
  4. Phân loại thành nhân viên, khách hàng quen, hoặc người lạ
- **Đầu ra**: Danh tính của các cá nhân và độ tin cậy

#### 3.2.5 Module Phân tích Hành vi
- **Chức năng**: Phân tích hành vi dựa trên pose và cử chỉ
- **Đầu vào**: Frame video, bounding boxes, và IDs từ các module trước
- **Luồng xử lý**:
  1. Áp dụng MediaPipe để phát hiện pose và keypoints
  2. Phân tích chuyển động dựa trên thay đổi của keypoints
  3. Áp dụng rule-based hoặc ML-based để phân loại hành vi
- **Đầu ra**: Phân loại hành vi và trạng thái (đứng, đi bộ, tương tác với sản phẩm...)

#### 3.2.6 Module Cơ sở dữ liệu
- **Chức năng**: Lưu trữ và quản lý dữ liệu
- **Đầu vào**: Kết quả từ các module xử lý
- **Luồng xử lý**:
  1. Chuẩn hóa dữ liệu theo schema
  2. Lưu trữ vào cơ sở dữ liệu quan hệ hoặc NoSQL
  3. Cung cấp API truy vấn
- **Đầu ra**: Dữ liệu có cấu trúc, sẵn sàng cho phân tích

#### 3.2.7 Module API
- **Chức năng**: Cung cấp REST API cho frontend và các hệ thống khác
- **Đầu vào**: Yêu cầu HTTP
- **Luồng xử lý**:
  1. Xác thực và phân quyền
  2. Xử lý yêu cầu
  3. Truy vấn dữ liệu
- **Đầu ra**: JSON response

#### 3.2.8 Module UI
- **Chức năng**: Cung cấp giao diện người dùng trực quan
- **Đầu vào**: Dữ liệu từ API
- **Luồng xử lý**:
  1. Hiển thị video với overlay thông tin
  2. Trực quan hóa dữ liệu và thống kê
  3. Tương tác người dùng
- **Đầu ra**: Dashboard và UI tương tác

## 4. Tiêu chuẩn Lập trình

### 4.1 Tiêu chuẩn Code Python

#### 4.1.1 Style Guide
- Tuân thủ PEP 8 cho định dạng code
- Tuân thủ PEP 257 cho docstrings
- Sử dụng Black và isort để tự động định dạng code
- Tối đa độ dài dòng: 88 ký tự (theo tiêu chuẩn Black)

#### 4.1.2 Nguyên tắc chung
- Ưu tiên sử dụng hàm thuần túy (pure functions)
- Đặt tên biến và hàm mô tả rõ mục đích, sử dụng các auxiliary verbs (is_, has_, get_, etc.)
- Sử dụng type hints cho tất cả các hàm và phương thức
- Tránh các magic numbers, sử dụng constants có tên có ý nghĩa
- Áp dụng nguyên tắc DRY (Don't Repeat Yourself)
- Tuân thủ nguyên tắc SOLID
- Ưu tiên sử dụng list comprehensions và generator expressions hơn là vòng lặp truyền thống

#### 4.1.3 Xử lý lỗi
- Sử dụng exception hierarchy riêng cho ứng dụng
- Catch các exception cụ thể, không catch tất cả exception
- Ghi log exception đầy đủ với traceback
- Sử dụng pattern try-except-else-finally khi phù hợp
- Ưu tiên fail fast, xử lý lỗi sớm trong hàm

#### 4.1.4 Hiệu suất
- Sử dụng asyncio cho các tác vụ I/O-bound
- Sử dụng multiprocessing cho các tác vụ CPU-bound
- Tối ưu hóa code trong các điểm nóng (bottlenecks)
- Sử dụng cProfile hoặc công cụ tương tự để phân tích hiệu suất

### 4.2 Documentation

#### 4.2.1 Doc String
Sử dụng định dạng Google Style cho tất cả docstrings:

```python
def function_name(param1: type, param2: type) -> return_type:
    """One-line summary of function.

    Detailed description of function, providing more context and
    explanation of the algorithm if necessary.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ExceptionType: Description of when this exception is raised.
    """
```

#### 4.2.2 Module Documentation
Mỗi module phải có docstring mô tả mục đích, các hàm/class chính, và cách sử dụng:

```python
"""Module for YOLO-based human detection.

This module provides functions and classes to detect humans in images
and videos using YOLOv8 object detection model.

Example:
    >>> from src.detection import yolo_detector
    >>> detector = yolo_detector.YOLODetector()
    >>> results = detector.detect(image)
"""
```

#### 4.2.3 README
Mỗi thư mục chính phải có README.md mô tả:
- Mục đích của module
- Các thành phần chính
- Cách sử dụng
- Ví dụ code
- Yêu cầu phụ thuộc

#### 4.2.4 API Documentation
Sử dụng OpenAPI Specification (thông qua FastAPI) cho API documentation.

## 5. Thiết kế Interface

### 5.1 Interface giữa các Module

#### 5.1.1 Video Input → Detection
```python
def process_frame(frame: np.ndarray) -> np.ndarray:
    """Process a single video frame.
    
    Args:
        frame: The input video frame in BGR format.
        
    Returns:
        The processed frame ready for detection.
    """
```

#### 5.1.2 Detection → Tracking
```python
def detect_persons(frame: np.ndarray) -> List[Detection]:
    """Detect persons in a frame.
    
    Args:
        frame: The input video frame.
        
    Returns:
        A list of Detection objects containing bounding boxes, 
        confidence scores, and class IDs.
    """
```

#### 5.1.3 Tracking → Face Recognition
```python
def track_objects(
    frame: np.ndarray, 
    detections: List[Detection]
) -> List[TrackedObject]:
    """Track objects across multiple frames.
    
    Args:
        frame: The current video frame.
        detections: The list of detections from the current frame.
        
    Returns:
        A list of tracked objects with unique IDs and trajectory information.
    """
```

#### 5.1.4 Face Recognition → Behavior Analysis
```python
def recognize_faces(
    frame: np.ndarray, 
    tracked_objects: List[TrackedObject]
) -> List[IdentifiedPerson]:
    """Recognize faces in tracked objects.
    
    Args:
        frame: The current video frame.
        tracked_objects: List of tracked objects.
        
    Returns:
        A list of identified persons with identity information.
    """
```

#### 5.1.5 Behavior Analysis → Data Storage
```python
def analyze_behavior(
    frame: np.ndarray,
    identified_persons: List[IdentifiedPerson]
) -> List[PersonBehavior]:
    """Analyze the behavior of identified persons.
    
    Args:
        frame: The current video frame.
        identified_persons: List of identified persons.
        
    Returns:
        A list of person behaviors with behavior classification.
    """
```

### 5.2 Data Structures

#### 5.2.1 Detection
```python
@dataclass
class Detection:
    bbox: Tuple[float, float, float, float]  # (x1, y1, x2, y2) in normalized coords
    confidence: float
    class_id: int
```

#### 5.2.2 TrackedObject
```python
@dataclass
class TrackedObject:
    track_id: int
    bbox: Tuple[float, float, float, float]
    confidence: float
    class_id: int
    trajectory: List[Tuple[float, float]]  # List of center points (x, y)
```

#### 5.2.3 IdentifiedPerson
```python
@dataclass
class IdentifiedPerson:
    track_id: int
    bbox: Tuple[float, float, float, float]
    face_bbox: Optional[Tuple[float, float, float, float]]
    identity: Optional[str]  # None if unknown
    identity_type: Literal["employee", "known_customer", "unknown"]
    confidence: float
```

#### 5.2.4 PersonBehavior
```python
@dataclass
class PersonBehavior:
    track_id: int
    identity: Optional[str]
    identity_type: Literal["employee", "known_customer", "unknown"]
    bbox: Tuple[float, float, float, float]
    pose_landmarks: Optional[List[Tuple[float, float, float]]]
    behavior: str  # e.g., "walking", "standing", "product_interaction"
    behavior_confidence: float
    timestamp: datetime
```

## 6. Workflow Triển khai

### 6.1 MVP (3 ngày)
Tập trung vào việc xây dựng pipeline cơ bản:
1. Thiết lập môi trường và cài đặt thư viện
2. Tích hợp YOLOv8 cho phát hiện người
3. Tích hợp face_recognition cho nhận diện cơ bản
4. Tích hợp MediaPipe cho phân tích pose đơn giản
5. Phát triển UI đơn giản với Streamlit

### 6.2 Phase 1: Cải thiện Độ chính xác (2 tuần)
1. Tối ưu hóa tham số mô hình
2. Tích hợp object tracking (ByteTrack)
3. Cải thiện nhận diện khuôn mặt
4. Mở rộng phân tích hành vi

### 6.3 Phase 2: Phát triển Backend (2 tuần)
1. Thiết kế schema database
2. Triển khai FastAPI
3. Phát triển hệ thống lưu trữ và truy xuất dữ liệu
4. Triển khai hệ thống xác thực và phân quyền

### 6.4 Phase 3: Frontend và Analytics (2 tuần)
1. Phát triển dashboard với Plotly Dash
2. Phát triển báo cáo và thống kê
3. Tích hợp trực quan hóa dữ liệu

### 6.5 Phase 4: Tối ưu hóa và Mở rộng (2 tuần)
1. Tối ưu hiệu suất hệ thống
2. Triển khai xử lý phân tán (nếu cần)
3. Phát triển các tính năng nâng cao

## 7. Đảm bảo Chất lượng

### 7.1 Kiểm thử
- Unit tests cho tất cả các module
- Integration tests giữa các module
- End-to-end tests cho quy trình đầy đủ
- Performance tests cho các điểm nóng

### 7.2 Linting và Kiểm tra Tĩnh
- Sử dụng flake8, mypy, và black
- Pre-commit hooks để đảm bảo chất lượng code
- CI/CD pipeline với GitHub Actions

### 7.3 Monitoring và Logging
- Structured logging với loguru
- Telemetry với OpenTelemetry
- Performance monitoring với Prometheus (tùy chọn)
- Trực quan hóa log với Grafana (tùy chọn)

## 8. Kết luận

Tài liệu này cung cấp kiến trúc giải pháp chi tiết cho hệ thống giám sát thông minh sử dụng YOLOv8, face-recognition, và MediaPipe. Kiến trúc module hóa cho phép dễ dàng phát triển, kiểm thử, và mở rộng hệ thống theo thời gian. Workflow triển khai được chia thành các giai đoạn rõ ràng, bắt đầu từ MVP và dần dần mở rộng các tính năng và hiệu suất.

Khi triển khai dự án này, cần chú ý đến:
- Hiệu suất xử lý thời gian thực
- Độ chính xác của các mô hình
- Khả năng mở rộng quy mô
- Quyền riêng tư và bảo mật dữ liệu

Tuân thủ các tiêu chuẩn lập trình và guidelines được đề xuất sẽ giúp đảm bảo code base dễ bảo trì và mở rộng trong tương lai.