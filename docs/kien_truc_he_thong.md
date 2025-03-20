# Kiến trúc Hệ thống

## Tổng quan
Hệ thống được thiết kế theo kiến trúc module, cho phép dễ dàng thay thế hoặc nâng cấp từng thành phần. Pipeline chính bao gồm các bước: thu thập video, phát hiện người, nhận diện khuôn mặt, phân tích hành vi, và xử lý/hiển thị kết quả.

## Các thành phần chính

### 1. Module Thu thập Video
- **Chức năng**: Lấy video từ camera, file, hoặc stream
- **Công nghệ**: OpenCV, FFMPEG
- **Đầu ra**: Frame video theo thời gian thực

### 2. Module Phát hiện Người
- **Chức năng**: Phát hiện và định vị người trong frame
- **Công nghệ**: YOLOv8
- **Đầu ra**: Bounding boxes của người, confidence scores

### 3. Module Theo dõi Đối tượng
- **Chức năng**: Theo dõi người qua các frame để duy trì ID
- **Công nghệ**: ByteTrack, DeepSORT
- **Đầu ra**: Object IDs, trajectories

### 4. Module Nhận diện Khuôn mặt
- **Chức năng**: Phát hiện, trích xuất đặc trưng và nhận diện khuôn mặt
- **Công nghệ**: face_recognition, DeepFace
- **Đầu ra**: Danh tính người, confidence scores

### 5. Module Phân tích Hành vi
- **Chức năng**: Phát hiện pose và phân tích hành vi
- **Công nghệ**: MediaPipe Pose, Hands
- **Đầu ra**: Pose landmarks, phân loại hành vi

### 6. Module Xử lý Dữ liệu
- **Chức năng**: Lưu trữ và quản lý dữ liệu thu thập
- **Công nghệ**: SQLite/PostgreSQL, MongoDB
- **Đầu ra**: Dữ liệu có cấu trúc cho phân tích

### 7. Module Hiển thị và Báo cáo
- **Chức năng**: Hiển thị kết quả và tạo báo cáo
- **Công nghệ**: Flask/FastAPI, Plotly/Dash
- **Đầu ra**: UI hiển thị video được xử lý và dashboard

## Luồng dữ liệu
1. Video frames được thu thập từ nguồn
2. Frames được xử lý bởi YOLO để phát hiện người
3. Người được phát hiện được theo dõi qua các frame
4. Khuôn mặt được trích xuất và nhận diện
5. Pose được phát hiện và hành vi được phân tích
6. Kết quả được lưu trữ trong cơ sở dữ liệu
7. Dữ liệu được hiển thị trên giao diện người dùng

## Yêu cầu Triển khai
- Môi trường Python 3.8+
- Cài đặt GPU (tùy chọn nhưng khuyến nghị)
- Các thư viện chính: PyTorch, OpenCV, TensorFlow (cho MediaPipe), face_recognition
- Cơ sở dữ liệu: SQLite (MVP), PostgreSQL (production)
- Web framework: FastAPI

## Kiến trúc Phần mềm
Hệ thống được tổ chức theo cấu trúc: 