# Kế hoạch Thực hiện Dự án

## Phương án MVP (3 ngày)

### Ngày 1: Thiết lập và Phát hiện Người
- **Sáng**:
  - Thiết lập môi trường phát triển và cài đặt thư viện
  - Tạo cấu trúc dự án cơ bản
  - Thử nghiệm YOLO với mô hình pretrained cho phát hiện người

- **Chiều**:
  - Phát triển module xử lý video (đọc từ camera hoặc file)
  - Tích hợp YOLO để phát hiện người trong video
  - Thêm bounding box hiển thị vị trí người

### Ngày 2: Nhận diện Khuôn mặt
- **Sáng**:
  - Cài đặt và thử nghiệm thư viện face_recognition
  - Tạo cơ sở dữ liệu khuôn mặt đơn giản (nhân viên mẫu)
  - Tích hợp nhận diện khuôn mặt vào pipeline

- **Chiều**:
  - Phát triển logic phân loại người (nhân viên/khách hàng)
  - Cải thiện hiệu suất xử lý
  - Thêm thông tin hiển thị lên video output

### Ngày 3: Phân tích Hành vi Cơ bản và Tích hợp
- **Sáng**:
  - Tích hợp MediaPipe để phát hiện pose
  - Phát triển các quy tắc đơn giản để nhận diện hành vi cơ bản (đứng, đi, cầm đồ vật)

- **Chiều**:
  - Tích hợp các thành phần lại với nhau
  - Phát triển giao diện đơn giản để hiển thị kết quả
  - Triển khai thử nghiệm và ghi nhận kết quả

### Kết quả MVP dự kiến:
- Ứng dụng Python có khả năng:
  - Phát hiện người trong video
  - Nhận diện và phân biệt nhân viên (đã có trong database)
  - Xác định một số hành vi cơ bản
  - Hiển thị thông tin overlay trên video

## Phương án Nâng cấp Hệ thống

### Giai đoạn 1 (Tuần 1-2): Cải thiện Độ chính xác
- Tối ưu hóa các tham số mô hình
- Bổ sung xử lý theo dõi đối tượng (object tracking)
- Cải thiện nhận diện khuôn mặt trong điều kiện ánh sáng khác nhau
- Mở rộng bộ dữ liệu khuôn mặt
- Thêm các quy tắc phức tạp hơn để phân tích hành vi

### Giai đoạn 2 (Tuần 3-4): Phát triển Backend
- Thiết kế và triển khai cơ sở dữ liệu
- Phát triển API cho việc quản lý dữ liệu
- Triển khai hệ thống xác thực và phân quyền
- Phát triển tính năng lưu trữ sự kiện và hoạt động

### Giai đoạn 3 (Tuần 5-6): Phát triển Frontend và Báo cáo
- Thiết kế và phát triển giao diện người dùng web
- Phát triển dashboard hiển thị thông tin theo thời gian thực
- Xây dựng các báo cáo thống kê
- Triển khai tính năng cảnh báo

### Giai đoạn 4 (Tuần 7-8): Mở rộng và Tối ưu hóa
- Triển khai xử lý phân tán (nếu cần)
- Thêm tính năng học máy nâng cao để phát hiện hành vi phức tạp
- Tối ưu hóa hiệu suất cho việc xử lý nhiều luồng video
- Phát triển chức năng tự động cập nhật model 