# 🎬 Video Subtitle Tool - Chinese to Vietnamese

Công cụ tự động tạo phụ đề tiếng Việt từ video tiếng Trung sử dụng AI.

## ✨ Tính năng

- 🎵 **Trích xuất audio** từ video tự động
- 🗣️ **Nhận dạng giọng nói** tiếng Trung bằng Whisper AI
- 🌐 **Dịch tự động** từ tiếng Trung sang tiếng Việt
- 📝 **Tạo file phụ đề** định dạng SRT
- 🎨 **Giao diện đẹp** và dễ sử dụng
- ⚙️ **Tùy chỉnh** độ dài phụ đề và model AI

## 🚀 Cài đặt

### Bước 1: Cài đặt Python
Đảm bảo bạn đã cài Python 3.8+ trên máy.

### Bước 2: Cài đặt FFmpeg
**Windows:**
```bash
# Sử dụng chocolatey
choco install ffmpeg

# Hoặc tải từ: https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### Bước 3: Cài đặt thư viện Python
```bash
pip install -r requirements.txt
```

## 📖 Cách sử dụng

### 1. Chạy ứng dụng
```bash
python video_subtitle_tool.py
```

### 2. Các bước thực hiện
1. **Chọn video**: Click "Browse" để chọn file video (.mp4, .avi, .mov, etc.)
2. **Chọn thư mục output**: Chọn nơi lưu file phụ đề
3. **Cài đặt**:
   - **Whisper Model**: `tiny` (nhanh) → `large` (chính xác)
   - **Max subtitle length**: Độ dài tối đa mỗi dòng phụ đề
4. **Bắt đầu**: Click "🚀 Generate Subtitles"

### 3. Kết quả
- File phụ đề được lưu với tên: `[tên_video]_vietnamese.srt`
- Có thể dùng với VLC, Potplayer, hoặc video editor khác

## ⚙️ Cài đặt nâng cao

### Whisper Models
| Model | Tốc độ | Chính xác | Dung lượng |
|-------|--------|-----------|------------|
| tiny  | Rất nhanh | Thấp | ~39 MB |
| base  | Nhanh | Trung bình | ~74 MB |
| small | Trung bình | Tốt | ~244 MB |
| medium| Chậm | Rất tốt | ~769 MB |
| large | Rất chậm | Xuất sắc | ~1550 MB |

### Định dạng video hỗ trợ
- MP4, AVI, MOV, MKV, WMV, FLV, WEBM
- Chất lượng audio tốt sẽ cho kết quả chính xác hơn

## 🐛 Khắc phục sự cố

### Lỗi "FFmpeg not found"
```bash
# Thêm FFmpeg vào PATH environment variable
# Hoặc cài đặt lại FFmpeg
```

### Lỗi dịch thuật
- Kiểm tra kết nối internet
- Thử lại sau vài phút (Google Translate có giới hạn)

### Video không được nhận dạng
- Chuyển đổi sang định dạng MP4
- Đảm bảo file không bị hỏng

## 🤝 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra file `processing_log.txt` để xem chi tiết lỗi
2. Đảm bảo đã cài đặt đầy đủ dependencies
3. Thử với video ngắn hơn (< 10 phút) để test

## 📝 Ghi chú

- **Lần đầu chạy**: Whisper sẽ tải model về máy (có thể mất vài phút)
- **Chất lượng**: Audio càng rõ, phụ đề càng chính xác
- **Tốc độ**: Video 10 phút ≈ 2-5 phút xử lý (tùy model)

---

**Chúc bạn sử dụng vui vẻ! 🎉** 