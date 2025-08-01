# 🎬 Video Subtitle Tool - Chinese to Vietnamese

**Công cụ tự động tạo phụ đề tiếng Việt từ video tiếng Trung sử dụng AI**

![Python](https://img.shields.io/badge/python-3.8+-blue.svg) ![Whisper](https://img.shields.io/badge/Whisper-AI-green.svg) ![Status](https://img.shields.io/badge/status-ready-brightgreen.svg)

---

## 🚀 Quick Start

### 1. Kiểm tra hệ thống
```bash
python check_system.py
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy tool
```bash
# Cách 1: Chạy trực tiếp
python video_subtitle_tool.py

# Cách 2: Double-click (Windows)
run_subtitle_tool.bat
```

---

## ✨ Tính năng chính

- 🎵 **Trích xuất audio** tự động từ video
- 🗣️ **Nhận dạng giọng nói** tiếng Trung bằng Whisper AI
- 🌐 **Dịch tự động** sang tiếng Việt
- 📝 **Tạo phụ đề .srt** với timing chính xác
- 🎨 **Giao diện modern** với dark theme
- 📊 **Real-time progress** và logging
- ⚙️ **Tùy chỉnh model AI** và format

---

## 📋 Yêu cầu hệ thống

### Bắt buộc:
- **Python 3.8+**
- **FFmpeg** (để xử lý video/audio)
- **Internet connection** (để tải models và dịch thuật)

### Thư viện Python:
- `openai-whisper` - Speech-to-text AI
- `moviepy` - Video processing  
- `googletrans` - Translation service
- `pysrt` - Subtitle file handling
- `torch` & `torchaudio` - AI model backend

---

## 📖 Hướng dẫn sử dụng

### Chuẩn bị video:
- **Format**: MP4, AVI, MOV, MKV (khuyến nghị MP4)
- **Audio quality**: Rõ ràng, ít noise
- **Duration**: Test với video < 10 phút lần đầu

### Quy trình xử lý:
1. **Select video** → Browse file video
2. **Choose output** → Thư mục lưu phụ đề
3. **Configure settings**:
   - **Model**: `tiny` (fast) → `large` (accurate)
   - **Max length**: Độ dài dòng phụ đề (default: 80)
4. **Start processing** → Click "🚀 Generate Subtitles"
5. **Get result** → File `.srt` trong output folder

---

## ⚙️ Cấu hình nâng cao

### Whisper Models:
| Model | Speed | Accuracy | Size | Use Case |
|-------|--------|----------|------|----------|
| `tiny` | ⚡⚡⚡ | ⭐⭐ | ~39MB | Quick test |
| `base` | ⚡⚡ | ⭐⭐⭐ | ~74MB | **Recommended** |
| `small` | ⚡ | ⭐⭐⭐⭐ | ~244MB | Good quality |
| `medium` | 🐌 | ⭐⭐⭐⭐⭐ | ~769MB | High accuracy |
| `large` | 🐌🐌 | ⭐⭐⭐⭐⭐ | ~1550MB | Best quality |

### Performance Tips:
- **Video < 15 min**: Tối ưu cho xử lý nhanh
- **Good audio**: Clean audio = Better accuracy
- **Stable internet**: Cần thiết cho translation
- **RAM**: ≥8GB cho model `medium`/`large`

---

## 🛠️ Khắc phục sự cố

### "Python not found"
```bash
# Cài Python từ python.org (nhớ tick "Add to PATH")
python --version
```

### "FFmpeg not found"  
```bash
# Windows (Chocolatey)
choco install ffmpeg

# Windows (Manual)
# Download từ: https://ffmpeg.org/download.html
# Add to System PATH

# Test
ffmpeg -version
```

### "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### Tool runs slow
- Use smaller model (`tiny`, `base`)
- Shorter videos (<15min)
- Check internet speed
- Close other heavy applications

### Poor subtitle quality
- Use larger model (`small`, `medium`)
- Ensure clear audio
- Check if video is actually Chinese
- Try different audio enhancement

---

## 📁 Project Structure

```
VideoSubtitleTool/
├── video_subtitle_tool.py    # Main application
├── check_system.py           # System requirements checker
├── requirements.txt          # Python dependencies
├── run_subtitle_tool.bat     # Windows batch launcher
├── README.md                 # This file
├── README_SUBTITLE_TOOL.md   # Detailed documentation
└── QUICK_START.md           # Setup guide
```

---

## 🤝 Hỗ trợ

### Debugging:
1. **System check**: `python check_system.py`
2. **Check logs**: Xem processing log trong UI
3. **Test connectivity**: `ping google.com`
4. **Verify packages**: `pip list | findstr whisper`

### Common Issues:
- **Long processing**: Normal for first run (downloading models)
- **Translation errors**: Check internet, try again later
- **Poor accuracy**: Use larger model, better audio quality
- **Memory errors**: Use smaller model or shorter video

---

## 📝 Notes

- **First run**: Whisper downloads models (~100MB-1.5GB)
- **Processing time**: ~20-40% of video duration
- **Output format**: Standard SRT compatible with all players
- **Languages**: Currently Chinese → Vietnamese only

---

## 🎉 Ready to go!

```bash
# Quick test workflow:
cd VideoSubtitleTool
python check_system.py          # ✅ Verify setup
python video_subtitle_tool.py   # 🚀 Launch tool
# Select test video < 10min, use 'base' model
```

**Happy subtitling! 🎬✨**

---

*Created with ❤️ for seamless video subtitle generation* 