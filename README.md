# 🎬 Enhanced Video Subtitle Tool V2

**Công cụ tự động tạo phụ đề tiếng Việt từ video tiếng Trung sử dụng AI với giao diện hiện đại**

![Python](https://img.shields.io/badge/python-3.8+-blue.svg) ![Whisper](https://img.shields.io/badge/Whisper-AI-green.svg) ![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-red.svg) ![Status](https://img.shields.io/badge/status-ready-brightgreen.svg)

---

## 🚀 Quick Start

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy tool
```bash
# Cách 1: Double-click (Windows) - Khuyên dùng
run_enhanced_tool_v2.bat

# Cách 2: Chạy trực tiếp
python enhanced_video_subtitle_tool_v2.py
```

---

## ✨ Tính năng chính

### 🎯 **Core Features**
- 🎵 **Trích xuất audio** tự động từ video
- 🗣️ **Nhận dạng giọng nói** tiếng Trung bằng Whisper AI
- 👁️ **OCR Text Detection** từ video frames
- 🌐 **Dịch tự động** sang tiếng Việt (Google Translate)
- 📝 **Xuất nhiều định dạng**: SRT, Transcript, OCR-only
- 🎬 **Video với phụ đề burnt-in** (sử dụng OpenCV)

### 🎨 **UI/UX Enhancements**
- 🖤 **Dark theme** hiện đại và đẹp mắt
- 📊 **Real-time progress** với log chi tiết
- ⚙️ **Tabbed settings** dễ sử dụng
- 🛑 **Stop/Cancel** processing bất cứ lúc nào
- 💾 **Session memory** - ghi nhớ cài đặt
- 📁 **Smart output management**

### 🔧 **Advanced Settings**
- 🤖 **5 Whisper models** (tiny → large)
- 👁️ **OCR interval** tùy chỉnh
- 📏 **Max line length** cho phụ đề
- 📤 **Flexible export options**
- 🎯 **Custom output filename**

---

## 📋 Yêu cầu hệ thống

### Bắt buộc:
- **Python 3.8+**
- **FFmpeg** (để xử lý video/audio)
- **Internet connection** (để tải models và dịch thuật)

### Tùy chọn (cho OCR):
- **Tesseract OCR** (Windows: tự động detect ở `C:\Program Files\Tesseract-OCR\`)

---

## 🎯 Supported Formats

### Video Input:
- `.mp4`, `.avi`, `.mov`, `.mkv`, `.wmv`, `.flv`

### Output Files:
- **SRT**: File phụ đề chuẩn
- **Transcript**: Kết hợp audio + OCR text
- **OCR-only**: Chỉ text từ video
- **Video**: MP4 với phụ đề burnt-in

---

## 💡 Cách sử dụng

### 1. **Khởi động**
- Chạy `run_enhanced_tool_v2.bat` hoặc `python enhanced_video_subtitle_tool_v2.py`
- Cài đặt từ lần trước sẽ được tự động khôi phục

### 2. **Chọn video**
- Click "Browse" để chọn file video
- Output folder sẽ tự động được set theo video (có thể thay đổi)

### 3. **Cấu hình**
- **AI Model**: Chọn Whisper model (base khuyên dùng)
- **OCR Settings**: Bật/tắt OCR và set interval
- **Export Options**: **Bắt buộc chọn ít nhất 1 option**
- **Output Settings**: Custom filename và folder

### 4. **Xử lý**
- Click "🚀 Generate Enhanced Subtitles"
- Theo dõi progress và log
- Có thể dừng bất cứ lúc nào với "⏹️ Stop Processing"

### 5. **Kết quả**
- Files được lưu trong output folder
- Cài đặt tự động được lưu cho lần sau

---

## 🛠️ Troubleshooting

### Lỗi thường gặp:

**1. "Some required packages are missing"**
```bash
pip install -r requirements.txt
```

**2. "FFmpeg not found"**
- Windows: Tải FFmpeg và thêm vào PATH
- Hoặc cài qua: `pip install ffmpeg-python`

**3. "OCR not working"**
- Cài Tesseract OCR cho Windows
- Hoặc tắt OCR trong settings

**4. "Translation failed"**
- Kiểm tra internet connection
- Google Translate có thể bị rate limit

---

## 📁 Project Structure

```
VideoSubtitleTool/
├── enhanced_video_subtitle_tool_v2.py  # 🎯 Main application
├── run_enhanced_tool_v2.bat           # 🚀 Windows launcher
├── requirements.txt                   # 📦 Dependencies
├── README.md                         # 📖 This file
├── FEATURES_UPDATE.md                # 📝 New features docs
└── subtitle_tool_settings.json      # ⚙️ User settings (auto-created)
```

---

## 🔄 Updates & Features

Xem file `FEATURES_UPDATE.md` để biết chi tiết về:
- 🛑 Stop/Cancel functionality
- 💾 Session memory system
- ❌ Export options changes
- 🔧 UI/UX improvements

---

## ⚡ Performance Tips

1. **Model Selection**:
   - `tiny`: Nhanh nhất, độ chính xác thấp
   - `base`: **Khuyên dùng** - cân bằng tốt
   - `small/medium`: Chậm hơn, chính xác hơn
   - `large`: Chậm nhất, chính xác nhất

2. **OCR Settings**:
   - Interval 2.0s: Cân bằng tốt
   - Interval thấp: Nhiều text hơn, chậm hơn
   - Tắt OCR: Nhanh hơn nếu video không có text

3. **Export Options**:
   - Chỉ chọn những format cần thiết
   - Video overlay mất thời gian lâu nhất

---

## 📞 Support

- 🐛 **Bug reports**: Tạo issue với log chi tiết
- 💡 **Feature requests**: Mô tả rõ tính năng mong muốn
- ❓ **Questions**: Kiểm tra README và docs trước

---

## 📄 License

MIT License - Free to use and modify

---

**Made with ❤️ using Python, Whisper AI, OpenCV, and modern UI principles** 