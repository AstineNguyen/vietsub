# 🚀 Quick Start Guide - Video Subtitle Tool

## ⚡ Cài đặt nhanh trên Windows

### Bước 1: Cài đặt Python
1. **Tải Python**: Vào https://python.org/downloads
2. **Chọn phiên bản**: Python 3.8+ (khuyến nghị 3.11)
3. **Quan trọng**: ✅ Tick vào "Add Python to PATH" khi cài đặt
4. **Kiểm tra**: Mở Command Prompt và gõ:
   ```cmd
   python --version
   ```

### Bước 2: Cài đặt FFmpeg
**Cách 1 - Chocolatey (Khuyến nghị):**
```cmd
# Cài đặt Chocolatey trước (nếu chưa có)
# Mở PowerShell as Administrator và chạy:
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Sau đó cài FFmpeg:
choco install ffmpeg
```

**Cách 2 - Manual:**
1. Tải FFmpeg từ: https://ffmpeg.org/download.html#build-windows
2. Giải nén vào thư mục (ví dụ: `C:\ffmpeg`)
3. Thêm `C:\ffmpeg\bin` vào System PATH

### Bước 3: Cài đặt Python packages
```cmd
# Trong thư mục tool
pip install -r requirements.txt
```

### Bước 4: Kiểm tra cài đặt
```cmd
python check_system.py
```

### Bước 5: Chạy tool
```cmd
# Cách 1: Chạy trực tiếp
python video_subtitle_tool.py

# Cách 2: Double-click file batch
run_subtitle_tool.bat
```

---

## 🎯 Sử dụng nhanh

### 1. Chuẩn bị video
- **Định dạng**: MP4, AVI, MOV (khuyến nghị MP4)
- **Audio**: Rõ ràng, ít nhiễu
- **Thời lượng**: Khuyến nghị < 30 phút lần đầu test

### 2. Các bước xử lý
1. **Mở tool** → `python video_subtitle_tool.py`
2. **Chọn video** → Click "Browse" 
3. **Chọn output folder** → Nơi lưu file .srt
4. **Cài đặt model**:
   - `tiny`: Nhanh nhất, chất lượng thấp
   - `base`: Cân bằng (khuyến nghị)
   - `small`: Chậm hơn, chất lượng tốt
5. **Bắt đầu** → Click "🚀 Generate Subtitles"

### 3. Kết quả
- File phụ đề: `[tên_video]_vietnamese.srt`
- Có thể dùng với: VLC, PotPlayer, Subtitle Edit, etc.

---

## 🛠️ Khắc phục sự cố thường gặp

### "Python was not found"
```cmd
# Kiểm tra Python đã được cài chưa
python --version

# Nếu lỗi: cài lại Python và nhớ tick "Add to PATH"
```

### "FFmpeg not found"
```cmd
# Kiểm tra FFmpeg
ffmpeg -version

# Nếu lỗi: cài lại FFmpeg hoặc thêm vào PATH
```

### "ModuleNotFoundError"
```cmd
# Cài lại packages
pip install -r requirements.txt --upgrade
```

### Tool chạy chậm
- Dùng model `tiny` hoặc `base`
- Đảm bảo có kết nối internet ổn định
- Video ngắn hơn (<15 phút)

### Phụ đề không chính xác
- Dùng model lớn hơn (`small`, `medium`)
- Đảm bảo audio rõ ràng
- Kiểm tra ngôn ngữ video có đúng tiếng Trung không

---

## 📞 Hỗ trợ

### Files log quan trọng:
- System check: `python check_system.py`
- Processing log: Xem trong tool UI

### Các lệnh debug:
```cmd
# Kiểm tra Python packages
pip list | findstr "whisper moviepy googletrans pysrt"

# Kiểm tra FFmpeg
ffmpeg -version

# Test internet connection
ping google.com
```

---

## 🎉 Ready to go!

Sau khi hoàn thành setup:
1. Chạy: `python check_system.py` ✅
2. Chạy: `python video_subtitle_tool.py` ✅  
3. Tạo phụ đề đầu tiên! 🎬

**Happy subtitling! 🚀** 