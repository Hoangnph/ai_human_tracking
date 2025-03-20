# Yêu cầu Dự án: Hệ thống Giám sát Thông minh

## Mục tiêu
Xây dựng hệ thống giám sát thông minh cho cửa hàng bán lẻ, có khả năng:
- Phát hiện người trong video giám sát
- Nhận diện danh tính (phân biệt nhân viên và khách hàng)
- Phân tích hành vi của người để tìm ra insights có giá trị

## Yêu cầu Chức năng
1. **Phát hiện Người**
   - Sử dụng YOLO để phát hiện người trong khung hình
   - Theo dõi người qua các khung hình (object tracking)
   - Xử lý nhiều người trong cùng một khung hình

2. **Nhận diện Danh tính**
   - Sử dụng face-recognition để nhận diện khuôn mặt
   - Phân loại người thành các nhóm: nhân viên đã biết, khách hàng đã biết, người lạ
   - Lưu trữ dữ liệu khuôn mặt cho nhận diện trong tương lai

3. **Phân tích Hành vi**
   - Sử dụng MediaPipe để nhận diện các hành động/cử chỉ
   - Phát hiện các hành vi đặc biệt (ví dụ: lấy sản phẩm, tương tác với nhân viên)
   - Tổng hợp và phân tích thời gian lưu trú của khách hàng

4. **Báo cáo và Thống kê**
   - Thống kê số lượng khách hàng theo thời gian
   - Thời gian lưu trú trung bình của khách hàng
   - Các khu vực được quan tâm nhiều nhất trong cửa hàng
   - Báo cáo hiệu suất nhân viên (thời gian tương tác với khách)

## Yêu cầu Phi Chức năng
1. **Hiệu suất**
   - Xử lý video real-time hoặc gần real-time (độ trễ < 3 giây)
   - Khả năng xử lý đồng thời ít nhất 4 luồng video

2. **Độ chính xác**
   - Phát hiện người: > 95% 
   - Nhận diện khuôn mặt: > 90% với góc nhìn thích hợp
   - Phân tích hành vi: > 85% cho các hành vi đã định nghĩa

3. **Khả năng mở rộng**
   - Kiến trúc mô-đun cho phép dễ dàng thêm các thuật toán mới
   - Lưu trữ dữ liệu phân tích cho mục đích học máy trong tương lai

4. **Quyền riêng tư và An ninh**
   - Tuân thủ quy định về bảo vệ dữ liệu cá nhân
   - Lưu trữ an toàn cho dữ liệu nhận diện khuôn mặt
   - Cơ chế xóa dữ liệu theo yêu cầu 