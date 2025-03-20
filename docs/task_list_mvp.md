# Task List cho Giai đoạn MVP (3 ngày)

Dựa trên tài liệu kiến trúc giải pháp và kế hoạch thực hiện, dưới đây là danh sách nhiệm vụ chi tiết cho giai đoạn MVP:

## Ngày 1: Thiết lập Môi trường và Phát hiện Người

### 1. Thiết lập Môi trường Phát triển
- [x] 1.1. Tạo môi trường ảo Python 3.9 với Conda
  - Ưu tiên: Cao
  - Thời gian: 30 phút
  - Output: Môi trường `retail-monitor` đã cài đặt

- [x] 1.2. Cài đặt các thư viện cốt lõi
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: Tệp requirements.txt với các phiên bản đã xác định

- [x] 1.3. Thiết lập cấu trúc dự án theo tài liệu kiến trúc
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: Cấu trúc thư mục dự án

### 2. Triển khai Module Video
- [x] 2.1. Phát triển class VideoReader để đọc từ file video
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: src/video/video_reader.py

- [x] 2.2. Phát triển class CameraReader để đọc từ camera
  - Ưu tiên: Trung bình
  - Thời gian: 1 giờ
  - Output: src/video/camera.py

- [x] 2.3. Phát triển tiện ích tiền xử lý frame 
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: src/video/utils.py

### 3. Triển khai YOLO cho Phát hiện Người
- [ ] 3.1. Tải và cấu hình pre-trained YOLOv8 model
  - Ưu tiên: Cao
  - Thời gian: 30 phút
  - Output: Mô hình YOLOv8 đã tải trong thư mục data/models/yolo

- [ ] 3.2. Phát triển YOLODetector class
  - Ưu tiên: Cao
  - Thời gian: 2 giờ
  - Output: src/detection/yolo_detector.py

- [ ] 3.3. Phát triển utilities cho việc xử lý kết quả phát hiện
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: src/detection/utils.py

### 4. Tích hợp và Trực quan hóa Kết quả
- [ ] 4.1. Tạo script tích hợp giữa Video và YOLO
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: src/main.py phiên bản cơ bản

- [ ] 4.2. Thêm visualization cho bounding boxes
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: src/utils/visualization.py

- [ ] 4.3. Kiểm tra và ghi nhận hiệu suất với video test
  - Ưu tiên: Trung bình
  - Thời gian: 30 phút
  - Output: Báo cáo hiệu suất cơ bản

## Ngày 2: Nhận diện Khuôn mặt

### 1. Thiết lập Module Face Recognition
- [ ] 1.1. Cài đặt thư viện face-recognition và dlib
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: Thư viện cài đặt thành công

- [ ] 1.2. Phát triển FaceDetector class
  - Ưu tiên: Cao
  - Thời gian: 2 giờ
  - Output: src/face_recognition/face_detector.py

- [ ] 1.3. Phát triển FaceEncoder class
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: src/face_recognition/face_encoder.py

### 2. Quản lý Dữ liệu Khuôn mặt
- [ ] 2.1. Tạo cấu trúc thư mục lưu trữ embedding khuôn mặt
  - Ưu tiên: Cao
  - Thời gian: 30 phút
  - Output: Cấu trúc thư mục data/faces

- [ ] 2.2. Tạo dữ liệu mẫu cho nhân viên
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: Dữ liệu khuôn mặt mẫu trong data/faces/employees

- [ ] 2.3. Phát triển FaceDatabase class
  - Ưu tiên: Cao
  - Thời gian: 2 giờ
  - Output: src/face_recognition/face_database.py

### 3. Tích hợp và Nhận diện
- [ ] 3.1. Phát triển FaceMatcher class
  - Ưu tiên: Cao
  - Thời gian: 2 giờ
  - Output: src/face_recognition/face_matcher.py

- [ ] 3.2. Tích hợp face recognition vào pipeline hiện có
  - Ưu tiên: Cao
  - Thời gian: 2 giờ
  - Output: Cập nhật src/main.py

- [ ] 3.3. Thêm hiển thị danh tính lên video
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: Cập nhật src/utils/visualization.py

### 4. Tối ưu Hiệu suất
- [ ] 4.1. Kiểm tra và tối ưu tốc độ nhận diện
  - Ưu tiên: Trung bình
  - Thời gian: 1 giờ
  - Output: Báo cáo hiệu suất và cải tiến

- [ ] 4.2. Cải thiện độ chính xác bằng cách điều chỉnh threshold
  - Ưu tiên: Trung bình
  - Thời gian: 1 giờ
  - Output: Threshold tối ưu

## Ngày 3: Phân tích Hành vi và Hoàn thiện MVP

### 1. Tích hợp MediaPipe
- [ ] 1.1. Cài đặt và kiểm tra MediaPipe
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: MediaPipe hoạt động đúng

- [ ] 1.2. Phát triển PoseDetector class
  - Ưu tiên: Cao
  - Thời gian: 2 giờ
  - Output: src/behavior/pose_detector.py

- [ ] 1.3. Phát triển HandDetector class (tùy chọn)
  - Ưu tiên: Thấp
  - Thời gian: 1 giờ
  - Output: src/behavior/hand_detector.py

### 2. Phân tích Hành vi Cơ bản
- [ ] 2.1. Phát triển logic phân tích hành vi đơn giản
  - Ưu tiên: Cao
  - Thời gian: 3 giờ
  - Output: src/behavior/behavior_rules.py

- [ ] 2.2. Xác định và phân loại các hành vi cơ bản (đứng, đi bộ, v.v.)
  - Ưu tiên: Cao
  - Thời gian: 2 giờ
  - Output: Danh sách hành vi đã phân loại

- [ ] 2.3. Tích hợp phân tích hành vi vào pipeline
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: Cập nhật src/main.py

### 3. Phát triển UI đơn giản
- [ ] 3.1. Thiết lập Streamlit app cơ bản
  - Ưu tiên: Cao
  - Thời gian: 2 giờ
  - Output: src/ui/dashboard.py

- [ ] 3.2. Hiển thị video với overlay thông tin
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: src/ui/video_display.py

- [ ] 3.3. Thêm trực quan hóa đơn giản cho kết quả phân tích
  - Ưu tiên: Trung bình
  - Thời gian: 1 giờ
  - Output: Các biểu đồ trong dashboard

### 4. Tích hợp và Kiểm thử Cuối cùng
- [ ] 4.1. Tích hợp tất cả các thành phần
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: Hệ thống hoạt động đầy đủ

- [ ] 4.2. Kiểm thử với nhiều điều kiện khác nhau
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: Báo cáo kiểm thử

- [ ] 4.3. Tạo tài liệu hướng dẫn triển khai và sử dụng
  - Ưu tiên: Cao
  - Thời gian: 1 giờ
  - Output: README.md cập nhật

## Kết quả MVP dự kiến:
- Ứng dụng Python hoạt động với khả năng:
  - Phát hiện người trong video sử dụng YOLOv8
  - Nhận diện và phân biệt nhân viên (đã có trong database)
  - Xác định một số hành vi cơ bản (đứng, đi bộ, tương tác với sản phẩm)
  - Hiển thị thông tin trên video và dashboard đơn giản
  - Giao diện Streamlit đơn giản để hiển thị kết quả

## Lưu ý quan trọng:
- Ưu tiên tập trung vào core functionality trước khi cải thiện UI
- Nếu gặp vấn đề với hiệu suất, có thể giảm độ phân giải video hoặc tăng khoảng thời gian giữa các frame xử lý
- Ghi nhận các vấn đề và hạn chế trong quá trình phát triển để cải thiện trong các giai đoạn tiếp theo
- Đảm bảo code có docstring và comment đầy đủ theo tiêu chuẩn đã đề ra 