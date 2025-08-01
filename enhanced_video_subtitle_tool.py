import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, font
import subprocess
import threading
import json
from pathlib import Path
import time
import re
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont

try:
    import whisper
    import moviepy.editor as mp
    from googletrans import Translator
    import pysrt
    import pytesseract
    DEPENDENCIES_OK = True
except ImportError:
    DEPENDENCIES_OK = False

class EnhancedVideoSubtitleTool:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Enhanced Video Subtitle Tool - Chinese OCR + Audio")
        self.root.geometry("1000x800")
        self.root.configure(bg='#1e1e1e')
        
        # Variables
        self.video_path = tk.StringVar()
        self.output_folder = tk.StringVar(value=str(Path.cwd()))
        self.progress_var = tk.DoubleVar()
        self.status_text = tk.StringVar(value="Ready to process video...")
        
        # OCR Settings
        self.enable_ocr = tk.BooleanVar(value=True)
        self.ocr_interval = tk.StringVar(value="2.0")  # seconds
        self.overlay_video = tk.BooleanVar(value=False)
        
        # Export options
        self.export_srt = tk.BooleanVar(value=True)
        self.export_transcript = tk.BooleanVar(value=True)
        self.export_ocr_only = tk.BooleanVar(value=True)
        
        # Colors
        self.bg_color = '#1e1e1e'
        self.card_color = '#2d2d2d'
        self.accent_color = '#0078d4'
        self.text_color = '#ffffff'
        self.success_color = '#28a745'
        self.warning_color = '#ffc107'
        
        # Configure Tesseract path (Windows)
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        except:
            pass
        
        # Setup UI
        self.setup_ui()
        
        # Check dependencies on startup
        if not DEPENDENCIES_OK:
            self.show_install_dependencies()
    
    def setup_ui(self):
        """Setup the main UI"""
        # Title
        title_font = font.Font(family="Segoe UI", size=24, weight="bold")
        title_label = tk.Label(
            self.root, 
            text="🎬 Enhanced Video Subtitle Tool",
            font=title_font,
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            self.root,
            text="Chinese Audio + Text Recognition → Vietnamese Subtitles",
            font=("Segoe UI", 12),
            bg=self.bg_color,
            fg='#cccccc'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Main frame with scrollbar
        main_canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # File selection card
        self.create_file_selection_card(scrollable_frame)
        
        # Processing options card
        self.create_processing_options_card(scrollable_frame)
        
        # Export options card
        self.create_export_options_card(scrollable_frame)
        
        # Settings card
        self.create_settings_card(scrollable_frame)
        
        # Process button
        self.create_process_button(scrollable_frame)
        
        # Progress and status
        self.create_progress_section(scrollable_frame)
        
        # Log area
        self.create_log_area(scrollable_frame)
    
    def create_file_selection_card(self, parent):
        """Create file selection card"""
        card = tk.Frame(parent, bg=self.card_color, relief='raised', bd=1)
        card.pack(fill='x', pady=10)
        
        # Card title
        title = tk.Label(
            card, 
            text="📁 Select Video File",
            font=("Segoe UI", 14, "bold"),
            bg=self.card_color,
            fg=self.text_color
        )
        title.pack(anchor='w', padx=20, pady=(15, 10))
        
        # Video file selection
        video_frame = tk.Frame(card, bg=self.card_color)
        video_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            video_frame,
            text="Video file:",
            font=("Segoe UI", 10),
            bg=self.card_color,
            fg=self.text_color
        ).pack(anchor='w')
        
        video_input_frame = tk.Frame(video_frame, bg=self.card_color)
        video_input_frame.pack(fill='x', pady=5)
        
        video_entry = tk.Entry(
            video_input_frame,
            textvariable=self.video_path,
            font=("Segoe UI", 10),
            bg='#404040',
            fg=self.text_color,
            insertbackground=self.text_color,
            relief='flat',
            bd=5
        )
        video_entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        browse_btn = tk.Button(
            video_input_frame,
            text="Browse",
            command=self.browse_video,
            bg=self.accent_color,
            fg='white',
            font=("Segoe UI", 10),
            relief='flat',
            padx=20,
            cursor='hand2'
        )
        browse_btn.pack(side='right', padx=(10, 0))
        
        # Output folder selection
        output_frame = tk.Frame(card, bg=self.card_color)
        output_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        tk.Label(
            output_frame,
            text="Output folder:",
            font=("Segoe UI", 10),
            bg=self.card_color,
            fg=self.text_color
        ).pack(anchor='w')
        
        output_input_frame = tk.Frame(output_frame, bg=self.card_color)
        output_input_frame.pack(fill='x', pady=5)
        
        output_entry = tk.Entry(
            output_input_frame,
            textvariable=self.output_folder,
            font=("Segoe UI", 10),
            bg='#404040',
            fg=self.text_color,
            insertbackground=self.text_color,
            relief='flat',
            bd=5
        )
        output_entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        output_browse_btn = tk.Button(
            output_input_frame,
            text="Browse",
            command=self.browse_output_folder,
            bg=self.accent_color,
            fg='white',
            font=("Segoe UI", 10),
            relief='flat',
            padx=20,
            cursor='hand2'
        )
        output_browse_btn.pack(side='right', padx=(10, 0))

    def create_processing_options_card(self, parent):
        """Create processing options card"""
        card = tk.Frame(parent, bg=self.card_color, relief='raised', bd=1)
        card.pack(fill='x', pady=10)
        
        title = tk.Label(
            card,
            text="🔧 Processing Options",
            font=("Segoe UI", 14, "bold"),
            bg=self.card_color,
            fg=self.text_color
        )
        title.pack(anchor='w', padx=20, pady=(15, 10))
        
        options_frame = tk.Frame(card, bg=self.card_color)
        options_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Enable OCR checkbox
        ocr_check = tk.Checkbutton(
            options_frame,
            text="🔍 Enable OCR (Detect Chinese text in video)",
            variable=self.enable_ocr,
            bg=self.card_color,
            fg=self.text_color,
            font=("Segoe UI", 11),
            selectcolor=self.card_color,
            activebackground=self.card_color,
            activeforeground=self.text_color
        )
        ocr_check.pack(anchor='w', pady=5)
        
        # OCR interval setting
        ocr_interval_frame = tk.Frame(options_frame, bg=self.card_color)
        ocr_interval_frame.pack(fill='x', pady=5)
        
        tk.Label(
            ocr_interval_frame,
            text="OCR sampling interval (seconds):",
            font=("Segoe UI", 10),
            bg=self.card_color,
            fg=self.text_color
        ).pack(side='left')
        
        interval_entry = tk.Entry(
            ocr_interval_frame,
            textvariable=self.ocr_interval,
            font=("Segoe UI", 10),
            bg='#404040',
            fg=self.text_color,
            width=8,
            relief='flat',
            bd=2
        )
        interval_entry.pack(side='left', padx=(10, 0))
        
        # Video overlay checkbox
        overlay_check = tk.Checkbutton(
            options_frame,
            text="🎨 Create video with translated text overlay",
            variable=self.overlay_video,
            bg=self.card_color,
            fg=self.text_color,
            font=("Segoe UI", 11),
            selectcolor=self.card_color,
            activebackground=self.card_color,
            activeforeground=self.text_color
        )
        overlay_check.pack(anchor='w', pady=5)

    def create_export_options_card(self, parent):
        """Create export options card"""
        card = tk.Frame(parent, bg=self.card_color, relief='raised', bd=1)
        card.pack(fill='x', pady=10)
        
        title = tk.Label(
            card,
            text="📄 Export Options",
            font=("Segoe UI", 14, "bold"),
            bg=self.card_color,
            fg=self.text_color
        )
        title.pack(anchor='w', padx=20, pady=(15, 10))
        
        export_frame = tk.Frame(card, bg=self.card_color)
        export_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # SRT subtitles
        srt_check = tk.Checkbutton(
            export_frame,
            text="📝 Export SRT subtitle file (for video players)",
            variable=self.export_srt,
            bg=self.card_color,
            fg=self.text_color,
            font=("Segoe UI", 11),
            selectcolor=self.card_color,
            activebackground=self.card_color,
            activeforeground=self.text_color
        )
        srt_check.pack(anchor='w', pady=3)
        
        # Audio transcript
        transcript_check = tk.Checkbutton(
            export_frame,
            text="🎤 Export audio transcript (timestamped dialogue)",
            variable=self.export_transcript,
            bg=self.card_color,
            fg=self.text_color,
            font=("Segoe UI", 11),
            selectcolor=self.card_color,
            activebackground=self.card_color,
            activeforeground=self.text_color
        )
        transcript_check.pack(anchor='w', pady=3)
        
        # OCR only
        ocr_only_check = tk.Checkbutton(
            export_frame,
            text="👀 Export OCR text only (detected text from video)",
            variable=self.export_ocr_only,
            bg=self.card_color,
            fg=self.text_color,
            font=("Segoe UI", 11),
            selectcolor=self.card_color,
            activebackground=self.card_color,
            activeforeground=self.text_color
        )
        ocr_only_check.pack(anchor='w', pady=3)

    def create_settings_card(self, parent):
        """Create settings card"""
        card = tk.Frame(parent, bg=self.card_color, relief='raised', bd=1)
        card.pack(fill='x', pady=10)
        
        title = tk.Label(
            card,
            text="⚙️ Settings",
            font=("Segoe UI", 14, "bold"),
            bg=self.card_color,
            fg=self.text_color
        )
        title.pack(anchor='w', padx=20, pady=(15, 10))
        
        settings_frame = tk.Frame(card, bg=self.card_color)
        settings_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        # Whisper model selection
        tk.Label(
            settings_frame,
            text="Whisper Model:",
            font=("Segoe UI", 10),
            bg=self.card_color,
            fg=self.text_color
        ).grid(row=0, column=0, sticky='w', pady=5)
        
        self.model_var = tk.StringVar(value="base")
        model_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.model_var,
            values=["tiny", "base", "small", "medium", "large"],
            state="readonly",
            width=15
        )
        model_combo.grid(row=0, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # Max subtitle length
        tk.Label(
            settings_frame,
            text="Max subtitle length:",
            font=("Segoe UI", 10),
            bg=self.card_color,
            fg=self.text_color
        ).grid(row=1, column=0, sticky='w', pady=5)
        
        self.max_length_var = tk.StringVar(value="80")
        length_entry = tk.Entry(
            settings_frame,
            textvariable=self.max_length_var,
            font=("Segoe UI", 10),
            bg='#404040',
            fg=self.text_color,
            width=10,
            relief='flat',
            bd=2
        )
        length_entry.grid(row=1, column=1, sticky='w', padx=(10, 0), pady=5)
    
    def create_process_button(self, parent):
        """Create process button"""
        button_frame = tk.Frame(parent, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        self.process_btn = tk.Button(
            button_frame,
            text="🚀 Generate Enhanced Subtitles",
            command=self.start_processing,
            bg=self.success_color,
            fg='white',
            font=("Segoe UI", 14, "bold"),
            relief='flat',
            padx=40,
            pady=15,
            cursor='hand2'
        )
        self.process_btn.pack()
    
    def create_progress_section(self, parent):
        """Create progress and status section"""
        progress_frame = tk.Frame(parent, bg=self.bg_color)
        progress_frame.pack(fill='x', pady=10)
        
        # Status label
        status_label = tk.Label(
            progress_frame,
            textvariable=self.status_text,
            font=("Segoe UI", 11),
            bg=self.bg_color,
            fg=self.text_color
        )
        status_label.pack(anchor='w')
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(fill='x', pady=(5, 0))
    
    def create_log_area(self, parent):
        """Create log area"""
        log_frame = tk.Frame(parent, bg=self.card_color, relief='raised', bd=1)
        log_frame.pack(fill='both', expand=True, pady=10)
        
        title = tk.Label(
            log_frame,
            text="📝 Processing Log",
            font=("Segoe UI", 12, "bold"),
            bg=self.card_color,
            fg=self.text_color
        )
        title.pack(anchor='w', padx=15, pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            bg='#1a1a1a',
            fg='#00ff00',
            insertbackground='#00ff00',
            font=("Consolas", 9),
            relief='flat',
            bd=5
        )
        self.log_text.pack(fill='both', expand=True, padx=15, pady=(0, 15))
    
    def browse_video(self):
        """Browse for video file"""
        filetypes = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.video_path.set(filename)
    
    def browse_output_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder.set(folder)
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_line)
        self.log_text.see(tk.END)
        self.root.update()
    
    def update_status(self, status, progress=None):
        """Update status and progress"""
        self.status_text.set(status)
        if progress is not None:
            self.progress_var.set(progress)
        self.root.update()
    
    def start_processing(self):
        """Start processing in a separate thread"""
        if not self.video_path.get():
            messagebox.showerror("Error", "Please select a video file!")
            return
        
        if not DEPENDENCIES_OK:
            self.show_install_dependencies()
            return
        
        # Disable button during processing
        self.process_btn.config(state='disabled', text="Processing...")
        self.log_text.delete(1.0, tk.END)
        
        # Start processing in thread
        thread = threading.Thread(target=self.process_video)
        thread.daemon = True
        thread.start()
    
    def process_video(self):
        """Process the video file with enhanced features"""
        try:
            video_file = self.video_path.get()
            output_dir = Path(self.output_folder.get())
            video_name = Path(video_file).stem
            
            self.log_message("🎬 Starting enhanced video processing...")
            
            # Step 1: Extract audio
            self.update_status("Extracting audio from video...", 5)
            audio_file = output_dir / f"{video_name}_audio.wav"
            self.extract_audio(video_file, str(audio_file))
            
            # Step 2: Process OCR if enabled
            ocr_results = []
            if self.enable_ocr.get():
                self.update_status("Detecting Chinese text in video...", 15)
                ocr_results = self.process_video_ocr(video_file)
            
            # Step 3: Transcribe audio
            self.update_status("Transcribing Chinese audio...", 35)
            model = whisper.load_model(self.model_var.get())
            audio_result = model.transcribe(str(audio_file), language="zh")
            
            # Step 4: Translate content
            self.update_status("Translating to Vietnamese...", 55)
            translator = Translator()
            
            # Process audio subtitles
            audio_subtitles = self.create_subtitles(audio_result, translator, "audio")
            
            # Process OCR subtitles
            ocr_subtitles = []
            if ocr_results:
                ocr_subtitles = self.translate_ocr_results(ocr_results, translator)
            
            # Step 5: Export files
            self.update_status("Exporting files...", 80)
            self.export_results(video_name, output_dir, audio_subtitles, ocr_subtitles, audio_result, ocr_results)
            
            # Step 6: Create overlay video if requested
            if self.overlay_video.get() and (audio_subtitles or ocr_subtitles):
                self.update_status("Creating video with text overlay...", 90)
                self.create_overlay_video(video_file, output_dir, video_name, audio_subtitles, ocr_subtitles)
            
            # Clean up audio file
            if audio_file.exists():
                audio_file.unlink()
            
            self.update_status("✅ Enhanced processing completed successfully!", 100)
            self.log_message(f"✅ All files saved to: {output_dir}")
            
            messagebox.showinfo("Success", f"Enhanced subtitles generated successfully!\nSaved to: {output_dir}")
            
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
            self.update_status("❌ Processing failed", 0)
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
        
        finally:
            # Re-enable button
            self.process_btn.config(state='normal', text="🚀 Generate Enhanced Subtitles")
    
    def extract_audio(self, video_file, audio_file):
        """Extract audio from video"""
        self.log_message("🎵 Extracting audio...")
        video = mp.VideoFileClip(video_file)
        audio = video.audio
        audio.write_audiofile(audio_file, verbose=False, logger=None)
        video.close()
        audio.close()
        self.log_message("✅ Audio extracted successfully")
    
    def process_video_ocr(self, video_file):
        """Process video for OCR text detection"""
        self.log_message("👀 Processing video for text detection...")
        
        cap = cv2.VideoCapture(video_file)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        interval = float(self.ocr_interval.get())
        frame_interval = int(fps * interval)
        
        ocr_results = []
        current_frame = 0
        
        while current_frame < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            ret, frame = cap.read()
            
            if not ret:
                break
            
            timestamp = current_frame / fps
            self.log_message(f"Scanning frame at {timestamp:.1f}s...")
            
            # OCR processing
            try:
                # Configure Tesseract for Chinese
                custom_config = r'--oem 3 --psm 6 -l chi_sim+chi_tra'
                text = pytesseract.image_to_string(frame, config=custom_config)
                
                if text.strip():
                    # Get bounding boxes for text
                    boxes = pytesseract.image_to_boxes(frame, config=custom_config)
                    
                    ocr_results.append({
                        'timestamp': timestamp,
                        'text': text.strip(),
                        'boxes': boxes,
                        'frame_number': current_frame
                    })
                    
                    self.log_message(f"Found text: {text.strip()[:50]}...")
                    
            except Exception as e:
                self.log_message(f"OCR error at {timestamp:.1f}s: {e}")
            
            current_frame += frame_interval
        
        cap.release()
        self.log_message(f"✅ OCR completed. Found {len(ocr_results)} text segments.")
        return ocr_results
    
    def create_subtitles(self, transcription_result, translator, source_type):
        """Create subtitles with translation"""
        subtitles = []
        max_length = int(self.max_length_var.get())
        
        segments = transcription_result['segments']
        self.log_message(f"Processing {len(segments)} {source_type} segments...")
        
        for i, segment in enumerate(segments):
            chinese_text = segment['text'].strip()
            if not chinese_text:
                continue
            
            self.log_message(f"Translating {source_type} segment {i+1}/{len(segments)}")
            
            try:
                # Translate to Vietnamese
                translation = translator.translate(chinese_text, src='zh', dest='vi')
                vietnamese_text = translation.text
                
                # Break long lines
                if len(vietnamese_text) > max_length:
                    vietnamese_text = self.break_long_lines(vietnamese_text, max_length)
                
                subtitle = {
                    'start': segment['start'],
                    'end': segment['end'],
                    'chinese': chinese_text,
                    'vietnamese': vietnamese_text,
                    'source': source_type
                }
                subtitles.append(subtitle)
                
                self.log_message(f"CN: {chinese_text}")
                self.log_message(f"VI: {vietnamese_text}")
                self.log_message("---")
                
            except Exception as e:
                self.log_message(f"⚠️ Translation error for {source_type} segment {i+1}: {e}")
                # Use original Chinese text if translation fails
                subtitles.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'chinese': chinese_text,
                    'vietnamese': chinese_text,
                    'source': source_type
                })
        
        return subtitles
    
    def translate_ocr_results(self, ocr_results, translator):
        """Translate OCR detected text"""
        self.log_message("🔄 Translating detected text...")
        translated_ocr = []
        
        for i, ocr_item in enumerate(ocr_results):
            chinese_text = ocr_item['text']
            timestamp = ocr_item['timestamp']
            
            try:
                translation = translator.translate(chinese_text, src='zh', dest='vi')
                vietnamese_text = translation.text
                
                translated_ocr.append({
                    'timestamp': timestamp,
                    'chinese': chinese_text,
                    'vietnamese': vietnamese_text,
                    'boxes': ocr_item['boxes'],
                    'frame_number': ocr_item['frame_number']
                })
                
                self.log_message(f"OCR {i+1}/{len(ocr_results)}: {chinese_text} → {vietnamese_text}")
                
            except Exception as e:
                self.log_message(f"⚠️ OCR translation error: {e}")
                translated_ocr.append({
                    'timestamp': timestamp,
                    'chinese': chinese_text,
                    'vietnamese': chinese_text,
                    'boxes': ocr_item['boxes'],
                    'frame_number': ocr_item['frame_number']
                })
        
        return translated_ocr
    
    def break_long_lines(self, text, max_length):
        """Break long lines into multiple lines"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    def export_results(self, video_name, output_dir, audio_subtitles, ocr_subtitles, audio_result, ocr_results):
        """Export all requested file formats"""
        
        # Export SRT file (combined)
        if self.export_srt.get():
            self.log_message("💾 Exporting SRT subtitle file...")
            srt_file = output_dir / f"{video_name}_vietnamese.srt"
            self.save_srt_file(audio_subtitles, str(srt_file))
        
        # Export audio transcript
        if self.export_transcript.get():
            self.log_message("📄 Exporting audio transcript...")
            transcript_file = output_dir / f"{video_name}_audio_transcript.txt"
            self.save_transcript(audio_subtitles, str(transcript_file), "Audio Transcript")
        
        # Export OCR only
        if self.export_ocr_only.get() and ocr_subtitles:
            self.log_message("👀 Exporting OCR text file...")
            ocr_file = output_dir / f"{video_name}_ocr_text.txt"
            self.save_ocr_text(ocr_subtitles, str(ocr_file))
        
        # Export combined analysis (detailed)
        combined_file = output_dir / f"{video_name}_complete_analysis.txt"
        self.save_combined_analysis(audio_subtitles, ocr_subtitles, str(combined_file))
    
    def save_srt_file(self, subtitles, output_file):
        """Save subtitles to SRT file"""
        srt_subtitles = pysrt.SubRipFile()
        
        for i, subtitle in enumerate(subtitles):
            start_time = pysrt.SubRipTime(seconds=subtitle['start'])
            end_time = pysrt.SubRipTime(seconds=subtitle['end'])
            
            srt_subtitle = pysrt.SubRipItem(
                index=i+1,
                start=start_time,
                end=end_time,
                text=subtitle['vietnamese']
            )
            srt_subtitles.append(srt_subtitle)
        
        srt_subtitles.save(output_file, encoding='utf-8')
        self.log_message(f"✅ SRT file saved: {output_file}")
    
    def save_transcript(self, subtitles, output_file, title):
        """Save transcript with timestamps"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"=== {title} ===\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for subtitle in subtitles:
                start_time = f"{subtitle['start']:.2f}s"
                end_time = f"{subtitle['end']:.2f}s"
                
                f.write(f"[{start_time} - {end_time}]\n")
                f.write(f"Chinese: {subtitle['chinese']}\n")
                f.write(f"Vietnamese: {subtitle['vietnamese']}\n")
                f.write("-" * 50 + "\n\n")
        
        self.log_message(f"✅ Transcript saved: {output_file}")
    
    def save_ocr_text(self, ocr_results, output_file):
        """Save OCR detected text"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== OCR Detected Text ===\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for ocr_item in ocr_results:
                timestamp = f"{ocr_item['timestamp']:.2f}s"
                
                f.write(f"[{timestamp}]\n")
                f.write(f"Chinese: {ocr_item['chinese']}\n")
                f.write(f"Vietnamese: {ocr_item['vietnamese']}\n")
                f.write("-" * 40 + "\n\n")
        
        self.log_message(f"✅ OCR text saved: {output_file}")
    
    def save_combined_analysis(self, audio_subtitles, ocr_subtitles, output_file):
        """Save complete analysis with all detected content"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== Complete Video Analysis ===\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Combine and sort by timestamp
            all_content = []
            
            for sub in audio_subtitles:
                all_content.append({
                    'timestamp': sub['start'],
                    'type': 'AUDIO',
                    'chinese': sub['chinese'],
                    'vietnamese': sub['vietnamese'],
                    'duration': sub['end'] - sub['start']
                })
            
            for ocr in ocr_subtitles:
                all_content.append({
                    'timestamp': ocr['timestamp'],
                    'type': 'TEXT',
                    'chinese': ocr['chinese'],
                    'vietnamese': ocr['vietnamese'],
                    'duration': 0
                })
            
            # Sort by timestamp
            all_content.sort(key=lambda x: x['timestamp'])
            
            for item in all_content:
                timestamp = f"{item['timestamp']:.2f}s"
                content_type = item['type']
                
                f.write(f"[{timestamp}] {content_type}\n")
                f.write(f"Chinese: {item['chinese']}\n")
                f.write(f"Vietnamese: {item['vietnamese']}\n")
                if item['duration'] > 0:
                    f.write(f"Duration: {item['duration']:.2f}s\n")
                f.write("=" * 60 + "\n\n")
        
        self.log_message(f"✅ Complete analysis saved: {output_file}")
    
    def create_overlay_video(self, video_file, output_dir, video_name, audio_subtitles, ocr_subtitles):
        """Create video with text overlay"""
        self.log_message("🎨 Creating video with text overlay...")
        
        try:
            # Load video
            video = mp.VideoFileClip(video_file)
            
            # Create subtitle clips for audio
            subtitle_clips = []
            for subtitle in audio_subtitles:
                txt_clip = mp.TextClip(
                    subtitle['vietnamese'],
                    fontsize=24,
                    color='white',
                    font='Arial-Bold',
                    stroke_color='black',
                    stroke_width=2
                ).set_position(('center', 'bottom')).set_start(subtitle['start']).set_end(subtitle['end'])
                
                subtitle_clips.append(txt_clip)
            
            # Combine video with subtitles
            final_video = mp.CompositeVideoClip([video] + subtitle_clips)
            
            # Export
            output_video = output_dir / f"{video_name}_with_subtitles.mp4"
            final_video.write_videofile(
                str(output_video),
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # Cleanup
            video.close()
            final_video.close()
            for clip in subtitle_clips:
                clip.close()
            
            self.log_message(f"✅ Overlay video saved: {output_video}")
            
        except Exception as e:
            self.log_message(f"⚠️ Video overlay error: {e}")
    
    def show_install_dependencies(self):
        """Show dialog to install dependencies"""
        msg = """Some required packages are missing. Would you like to install them?

Required packages:
• openai-whisper (for speech recognition)
• moviepy (for video processing)
• googletrans (for translation)
• pysrt (for subtitle files)
• pytesseract (for OCR)
• opencv-python (for video analysis)

Click 'Install' to install automatically."""
        
        result = messagebox.askyesno("Install Dependencies", msg)
        if result:
            self.install_dependencies()
    
    def install_dependencies(self):
        """Install required dependencies"""
        self.log_message("📦 Installing dependencies...")
        self.update_status("Installing required packages...", 0)
        
        packages = [
            "openai-whisper",
            "moviepy", 
            "googletrans==4.0.0rc1",
            "pysrt",
            "pytesseract",
            "opencv-python",
            "Pillow"
        ]
        
        def install():
            try:
                for i, package in enumerate(packages):
                    self.log_message(f"Installing {package}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    progress = ((i + 1) / len(packages)) * 100
                    self.update_status(f"Installing {package}...", progress)
                
                self.log_message("✅ All dependencies installed successfully!")
                self.update_status("Dependencies installed. Please restart the application.", 100)
                messagebox.showinfo("Success", "Dependencies installed successfully!\nPlease restart the application.")
                
            except Exception as e:
                self.log_message(f"❌ Installation failed: {e}")
                messagebox.showerror("Error", f"Installation failed: {e}")
        
        thread = threading.Thread(target=install)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = EnhancedVideoSubtitleTool(root)
    root.mainloop()

if __name__ == "__main__":
    main() 