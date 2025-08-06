# Enhanced Video Subtitle Tool V2 - Tính năng mới

## 🛑 Chức năng Dừng/Hủy Quá trình

### Tính năng mới:
- **Nút Stop**: Thêm nút "⏹️ Stop Processing" để dừng quá trình xử lý bất cứ lúc nào
- **Dừng an toàn**: Quá trình dừng được xử lý an toàn với cleanup tự động
- **Kiểm tra điểm dừng**: Các điểm kiểm tra `should_stop` được thêm vào tất cả các bước xử lý chính:
  - Trích xuất audio
  - Nhận dạng giọng nói (Whisper)
  - Xử lý OCR từng frame
  - Dịch thuật từng đoạn
  - Tạo video với phụ đề

### Cách sử dụng:
1. Bắt đầu xử lý như bình thường với nút "🚀 Generate Enhanced Subtitles"
2. Nếu muốn dừng, click nút "⏹️ Stop Processing" (chỉ hiện khi đang xử lý)
3. Chờ ứng dụng dọn dẹp và reset trạng thái

## 💾 Ghi nhớ Lựa chọn (Session Memory)

### Tính năng mới:
- **Lưu cài đặt tự động**: Tất cả cài đặt được lưu vào file `subtitle_tool_settings.json`
- **Khôi phục khi khởi động**: Cài đặt từ phiên trước được tự động khôi phục
- **Lưu khi đóng**: Cài đặt được lưu khi đóng ứng dụng

### Cài đặt được ghi nhớ:
- **Model Settings**: Whisper model, độ dài dòng tối đa
- **OCR Settings**: Bật/tắt OCR, khoảng thời gian OCR
- **Export Options**: SRT, transcript, OCR-only, video overlay
- **Output Settings**: Tự động chọn thư mục, thư mục output

## ❌ Bỏ Tự động Chọn Export Options

### Thay đổi:
- **Trước**: SRT và Transcript được tự động chọn
- **Bây giờ**: Không có option nào được tự động chọn
- **Yêu cầu**: Phải chọn ít nhất 1 export option trước khi xử lý
- **Ghi nhớ**: Lựa chọn export sẽ được ghi nhớ cho lần sử dụng tiếp theo

### Lợi ích:
- Người dùng có kiểm soát hoàn toàn về output
- Tránh tạo file không cần thiết
- Cài đặt được duy trì giữa các phiên sử dụng

## 🔧 Cải tiến khác

### UI/UX:
- Nút Stop với màu đỏ để dễ nhận biết
- Thông báo lỗi khi chưa chọn export option
- Status message rõ ràng khi dừng quá trình

### Xử lý lỗi:
- Cleanup an toàn khi dừng giữa chừng
- Xử lý exception tốt hơn
- Log message phân biệt giữa hoàn thành và dừng

### Performance:
- Kiểm tra should_stop ở mọi bước quan trọng
- Tránh lãng phí tài nguyên khi người dùng muốn dừng
- Cleanup tự động file tạm

## 📝 Sử dụng

1. **Khởi động**: Ứng dụng tự động load cài đặt từ lần trước
2. **Chọn video**: Browse và chọn file video
3. **Cấu hình**: Điều chỉnh cài đặt theo nhu cầu
4. **Chọn export**: **Bắt buộc** chọn ít nhất 1 loại output
5. **Xử lý**: Click "Generate" để bắt đầu
6. **Dừng** (nếu cần): Click "Stop Processing" để dừng
7. **Đóng**: Cài đặt tự động được lưu khi đóng app

## 🗂️ File cài đặt

File `subtitle_tool_settings.json` sẽ được tạo trong thư mục ứng dụng chứa:
```json
{
  "model": "base",
  "max_length": "80",
  "enable_ocr": true,
  "ocr_interval": "2.0",
  "overlay_video": false,
  "export_srt": true,
  "export_transcript": true,
  "export_ocr_only": false,
  "auto_output_folder": true,
  "output_folder": "..."
}
```

Có thể xóa file này để reset về cài đặt mặc định. 