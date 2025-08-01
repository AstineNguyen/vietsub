# 🚀 Enhanced Video Subtitle Tool - User Guide

## 🎯 Tính năng nâng cao

Tool này được nâng cấp để đáp ứng yêu cầu của bạn:

### ✨ **Tính năng chính:**
1. **🎤 Nhận dạng âm thanh**: Whisper AI cho giọng nói tiếng Trung
2. **👀 OCR chữ trong video**: Tesseract OCR cho text tiếng Trung xuất hiện trong video  
3. **🌐 Dịch tự động**: Google Translate sang tiếng Việt
4. **📄 Nhiều định dạng xuất**: SRT, transcript, OCR riêng, phân tích tổng hợp
5. **🎨 Video overlay**: Ghép phụ đề đã dịch thẳng vào video
6. **⏱️ Timestamps chính xác**: Theo dõi thời gian cho từng dòng

---

## 🚀 Cách chạy

### **Cách 1: Chạy trực tiếp**
```bash
python enhanced_video_subtitle_tool.py
```

### **Cách 2: Sử dụng batch script**
```bash
run_enhanced_tool.bat
```

---

## 🎮 Hướng dẫn sử dụng

### **1. File Selection**
- **Video file**: Chọn video có âm thanh tiếng Trung và/hoặc chữ Trung Quốc
- **Output folder**: Thư mục lưu tất cả file kết quả

### **2. Processing Options**
- **☑️ Enable OCR**: Bật để detect chữ Trung Quốc trong video
- **OCR interval**: Khoảng cách giữa các frame scan (mặc định: 2.0 giây)
- **☑️ Video overlay**: Tạo video mới với phụ đề được ghép sẵn

### **3. Export Options**
Chọn định dạng file muốn xuất:

#### **📝 SRT Subtitle File**
- File `.srt` tiêu chuẩn cho video player
- Chứa phụ đề tiếng Việt với timing chính xác
- Tương thích với VLC, PotPlayer, v.v.

#### **🎤 Audio Transcript**  
- File `.txt` chứa transcript âm thanh
- Format:
```
[10.50s - 15.20s]
Chinese: 你好，欢迎观看这个视频
Vietnamese: Xin chào, chào mừng xem video này
--------------------------------------------------
```

#### **👀 OCR Text Only**
- File `.txt` chứa chỉ text được detect từ video
- Format:
```
[25.40s]
Chinese: 中文字幕
Vietnamese: Phụ đề tiếng Trung
----------------------------------------
```

### **4. Settings**
- **Whisper Model**: Chọn độ chính xác vs tốc độ
  - `tiny`: Nhanh nhất, chất lượng thấp
  - `base`: **Khuyến nghị** - cân bằng
  - `small`: Chậm hơn, chất lượng tốt
  - `medium/large`: Chậm, chất lượng cao nhất
- **Max subtitle length**: Độ dài tối đa mỗi dòng phụ đề

---

## 📁 File Output

Sau khi xử lý, bạn sẽ có các file:

```
📁 Output Folder/
├── 📄 [video_name]_vietnamese.srt              # Phụ đề SRT
├── 📄 [video_name]_audio_transcript.txt        # Transcript âm thanh
├── 📄 [video_name]_ocr_text.txt               # Text từ OCR  
├── 📄 [video_name]_complete_analysis.txt       # Phân tích tổng hợp
└── 🎬 [video_name]_with_subtitles.mp4         # Video có phụ đề (nếu chọn)
```

### **Complete Analysis Format:**
```
=== Complete Video Analysis ===
Generated: 2025-01-27 15:30:45

[10.50s] AUDIO
Chinese: 你好，欢迎观看这个视频
Vietnamese: Xin chào, chào mừng xem video này  
Duration: 4.70s
============================================================

[25.40s] TEXT
Chinese: 中文字幕
Vietnamese: Phụ đề tiếng Trung
============================================================
```

---

## ⚙️ Tùy chỉnh nâng cao

### **OCR Settings:**
- **Interval**: 1.0-5.0 giây (1.0 = chính xác hơn, 5.0 = nhanh hơn)
- **Languages**: Hỗ trợ cả Simplified + Traditional Chinese
- **Quality**: Tự động xử lý contrast và brightness

### **Video Overlay:**
- **Font**: Arial Bold, 24px
- **Position**: Bottom center
- **Style**: White text, black outline
- **Format**: MP4 H.264

---

## 🎯 Use Cases

### **1. Video giáo dục tiếng Trung**
```
✅ OCR: ON (để detect slide text)
✅ Audio: ON (để transcript lời giảng)
✅ Export: SRT + Complete Analysis
✅ Overlay: ON (video học có sẵn phụ đề)
```

### **2. Phim/Drama có hardcode subtitle**
```
✅ OCR: ON (detect phụ đề gốc)
✅ Audio: ON (detect đối thoại)
✅ Export: All formats
❌ Overlay: OFF (đã có sẵn phụ đề)
```

### **3. Presentation/Conference**
```
✅ OCR: ON (slide content)
✅ Audio: ON (speech)
✅ Export: Transcript + OCR separate
✅ Overlay: ON (tạo video có phụ đề)
```

---

## 🛠️ Troubleshooting

### **"Tesseract not found"**
```bash
# Tesseract đã được cài tự động, nhưng nếu lỗi:
winget install UB-Mannheim.TesseractOCR
```

### **"No text detected"**
- Kiểm tra video có chứa chữ Trung Quốc không
- Giảm OCR interval xuống 1.0s
- Đảm bảo chữ rõ ràng, không bị mờ

### **OCR không chính xác**
- Sử dụng video có độ phân giải cao
- Đảm bảo chữ có contrast tốt với background
- Tăng chất lượng video nguồn

### **Tool chạy chậm**
```
Audio processing: Dùng model "tiny" hoặc "base"
OCR processing: Tăng interval lên 3.0-5.0s
Video overlay: Tắt nếu không cần thiết
```

---

## 📊 Performance Tips

### **Video tối ưu:**
- **Resolution**: 720p-1080p
- **Format**: MP4 H.264
- **Duration**: <30 phút lần đầu test
- **Audio**: Clear, minimal background noise

### **OCR tối ưu:**
- **Text size**: ≥16px trong video
- **Contrast**: Chữ trắng/đen trên nền tương phản
- **Font**: Sans-serif fonts work better
- **Position**: Không bị che khuất

---

## 🎉 Ready to Use!

```bash
# Quick workflow:
1. Chạy: run_enhanced_tool.bat
2. Chọn video tiếng Trung có chữ
3. Enable OCR + chọn export options
4. Click "🚀 Generate Enhanced Subtitles"
5. Đợi kết quả trong output folder
```

**Enjoy your enhanced video subtitles! 🎬✨** 