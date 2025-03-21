# Tham số chính của Hệ thống Nhận diện Danh tính (Identity Tracking)

Tài liệu này mô tả các tham số quan trọng của hệ thống nhận diện danh tính và hướng dẫn cách điều chỉnh chúng để đạt hiệu quả tối ưu trong các điều kiện khác nhau.

## Tham số điều khiển quy trình phát hiện

### 1. Tần suất phát hiện đối tượng (detection_interval)
- **Mô tả**: Xác định cứ bao nhiêu frames thì hệ thống sẽ thực hiện phát hiện đối tượng (người) một lần
- **File cấu hình**: `run_identity_tracking_demo.sh`
- **Giá trị mặc định**: 3
- **Hướng dẫn điều chỉnh**:
  - Giảm xuống (1-2) nếu cần theo dõi chính xác đối tượng di chuyển nhanh
  - Tăng lên (5-10) để cải thiện hiệu suất trên hệ thống yếu
  - Giá trị tối ưu thường là 3-5 cho hầu hết trường hợp

### 2. Tần suất phát hiện khuôn mặt (face_detection_interval)
- **Mô tả**: Xác định cứ bao nhiêu frames thì hệ thống sẽ thực hiện phát hiện khuôn mặt một lần cho mỗi đối tượng đã được theo dõi
- **File cấu hình**: `run_identity_tracking_demo.sh`
- **Giá trị mặc định**: 2
- **Hướng dẫn điều chỉnh**:
  - Giảm xuống (1) để tăng tần suất phát hiện khuôn mặt, hữu ích khi khuôn mặt thường xuyên thay đổi góc độ
  - Tăng lên (3-5) để tối ưu hiệu suất nếu khuôn mặt ít thay đổi góc độ
  - Nên giữ giá trị này nhỏ hơn detection_interval

## Tham số cho độ chính xác phát hiện

### 1. Ngưỡng tin cậy phát hiện đối tượng (conf)
- **Mô tả**: Ngưỡng tối thiểu cho điểm tin cậy khi phát hiện người bằng YOLO
- **File cấu hình**: `run_identity_tracking_demo.sh`
- **Giá trị mặc định**: 0.35
- **Hướng dẫn điều chỉnh**:
  - Giảm xuống (0.25-0.3) nếu không phát hiện được người trong điều kiện ánh sáng yếu
  - Tăng lên (0.4-0.5) nếu có quá nhiều phát hiện sai
  - Giá trị 0.35-0.4 thường phù hợp cho hầu hết trường hợp

### 2. Ngưỡng tương đồng nhận diện khuôn mặt (tolerance)
- **Mô tả**: Ngưỡng tối đa cho khoảng cách giữa hai khuôn mặt để coi là cùng một người (giá trị thấp hơn = nghiêm ngặt hơn)
- **File cấu hình**: `run_identity_tracking_demo.sh`
- **Giá trị đã điều chỉnh**: 0.18 (giá trị ban đầu là 0.45)
- **Hướng dẫn điều chỉnh**:
  - Giá trị càng thấp càng nghiêm ngặt khi nhận diện (ít false positive)
  - Giá trị càng cao càng dễ dãi khi nhận diện (ít false negative)
  - Thường nên bắt đầu từ 0.18-0.25 và điều chỉnh dựa trên kết quả thực tế
  - **Quan trọng**: Điểm tương đồng thường thay đổi theo điều kiện ánh sáng, góc khuôn mặt, và mô hình face encoding được sử dụng

## Tham số mô hình

### 1. Mô hình phát hiện đối tượng (detection-model)
- **Mô tả**: Mô hình YOLO sử dụng để phát hiện người
- **File cấu hình**: `run_identity_tracking_demo.sh`
- **Giá trị mặc định**: yolov8n
- **Các lựa chọn**:
  - yolov8n: Nhẹ, nhanh, độ chính xác thấp hơn
  - yolov8s: Cân bằng giữa tốc độ và độ chính xác
  - yolov8m: Chính xác hơn, chậm hơn
  - yolov8l/yolov8x: Chính xác nhất, chậm nhất

### 2. Mô hình phát hiện khuôn mặt (face-detector)
- **Mô tả**: Thuật toán sử dụng để phát hiện khuôn mặt
- **File cấu hình**: `run_identity_tracking_demo.sh`
- **Giá trị mặc định**: haarcascade
- **Các lựa chọn**:
  - haarcascade: Nhanh, độ chính xác vừa phải, yêu cầu khuôn mặt nhìn thẳng
  - hog: Chậm hơn nhưng phát hiện được khuôn mặt ở nhiều góc độ khác nhau

### 3. Mô hình mã hóa khuôn mặt (face-model)
- **Mô tả**: Thuật toán sử dụng để trích xuất đặc trưng khuôn mặt
- **File cấu hình**: `run_identity_tracking_demo.sh`
- **Giá trị mặc định**: lbp
- **Các lựa chọn**:
  - lbp: Local Binary Patterns Histograms, nhanh nhưng ít chính xác
  - eigen: Eigenfaces, cân bằng giữa tốc độ và độ chính xác
  - fisher: Fisherfaces, chính xác hơn nhưng chậm hơn

## Các tham số khác

### 1. Hệ số resize (resize-factor)
- **Mô tả**: Hệ số thu nhỏ kích thước frame để tăng tốc xử lý
- **File cấu hình**: `run_identity_tracking_demo.sh`
- **Giá trị mặc định**: 0.6
- **Hướng dẫn điều chỉnh**:
  - Giảm xuống (0.4-0.5) để tăng tốc độ xử lý trên hệ thống yếu
  - Tăng lên (0.7-0.8) để cải thiện độ chính xác nếu khuôn mặt nhỏ

### 2. Số frame tối đa (max-frames)
- **Mô tả**: Số frame tối đa sẽ xử lý trước khi kết thúc (0 = không giới hạn)
- **File cấu hình**: `run_identity_tracking_demo.sh`
- **Giá trị mặc định**: Không đặt (xử lý toàn bộ video)
- **Hướng dẫn điều chỉnh**:
  - Đặt một giá trị cụ thể (100-1000) cho mục đích kiểm thử
  - Để trống hoặc 0 cho xử lý đầy đủ video

## Lời khuyên khi điều chỉnh

1. **Tuần tự từng bước**: Chỉ thay đổi một tham số một lần và kiểm tra kết quả
2. **Dựa vào log**: Kiểm tra log để hiểu được điểm tương đồng thực tế đạt được
3. **Video test**: Sử dụng video test cố định để so sánh hiệu quả của các cài đặt khác nhau
4. **Cân bằng**: Tìm sự cân bằng giữa tốc độ xử lý và độ chính xác phù hợp với nhu cầu
5. **Môi trường**: Cài đặt cần được điều chỉnh cho từng môi trường cụ thể (ánh sáng, góc camera...) 