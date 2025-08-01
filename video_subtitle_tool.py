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

try:
    import whisper
    import moviepy.editor as mp
    from googletrans import Translator
    import pysrt
    DEPENDENCIES_OK = True
except ImportError:
    DEPENDENCIES_OK = False

class VideoSubtitleTool:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Video Subtitle Tool - Chinese to Vietnamese")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e1e')
        
        # Variables
        self.video_path = tk.StringVar()
        self.output_folder = tk.StringVar(value=str(Path.cwd()))
        self.progress_var = tk.DoubleVar()
        self.status_text = tk.StringVar(value="Ready to process video...")
        
        # Colors
        self.bg_color = '#1e1e1e'
        self.card_color = '#2d2d2d'
        self.accent_color = '#0078d4'
        self.text_color = '#ffffff'
        self.success_color = '#28a745'
        self.warning_color = '#ffc107'
        
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
            text="🎬 Video Subtitle Generator",
            font=title_font,
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            self.root,
            text="Convert Chinese audio to Vietnamese subtitles automatically",
            font=("Segoe UI", 12),
            bg=self.bg_color,
            fg='#cccccc'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        # File selection card
        self.create_file_selection_card(main_frame)
        
        # Settings card
        self.create_settings_card(main_frame)
        
        # Process button
        self.create_process_button(main_frame)
        
        # Progress and status
        self.create_progress_section(main_frame)
        
        # Log area
        self.create_log_area(main_frame)
    
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
            text="🚀 Generate Subtitles",
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
            height=8,
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
        """Process the video file"""
        try:
            video_file = self.video_path.get()
            output_dir = Path(self.output_folder.get())
            video_name = Path(video_file).stem
            
            self.log_message("🎬 Starting video processing...")
            
            # Step 1: Extract audio
            self.update_status("Extracting audio from video...", 10)
            audio_file = output_dir / f"{video_name}_audio.wav"
            self.extract_audio(video_file, str(audio_file))
            
            # Step 2: Transcribe audio
            self.update_status("Transcribing Chinese audio...", 30)
            model = whisper.load_model(self.model_var.get())
            result = model.transcribe(str(audio_file), language="zh")
            
            # Step 3: Translate to Vietnamese
            self.update_status("Translating to Vietnamese...", 60)
            translator = Translator()
            subtitles = self.create_subtitles(result, translator)
            
            # Step 4: Save subtitle file
            self.update_status("Saving subtitle file...", 90)
            srt_file = output_dir / f"{video_name}_vietnamese.srt"
            self.save_subtitles(subtitles, str(srt_file))
            
            # Clean up audio file
            if audio_file.exists():
                audio_file.unlink()
            
            self.update_status("✅ Processing completed successfully!", 100)
            self.log_message(f"✅ Subtitles saved to: {srt_file}")
            
            messagebox.showinfo("Success", f"Subtitles generated successfully!\nSaved to: {srt_file}")
            
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
            self.update_status("❌ Processing failed", 0)
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
        
        finally:
            # Re-enable button
            self.process_btn.config(state='normal', text="🚀 Generate Subtitles")
    
    def extract_audio(self, video_file, audio_file):
        """Extract audio from video"""
        self.log_message("🎵 Extracting audio...")
        video = mp.VideoFileClip(video_file)
        audio = video.audio
        audio.write_audiofile(audio_file, verbose=False, logger=None)
        video.close()
        audio.close()
        self.log_message("✅ Audio extracted successfully")
    
    def create_subtitles(self, transcription_result, translator):
        """Create subtitles with translation"""
        subtitles = []
        max_length = int(self.max_length_var.get())
        
        for i, segment in enumerate(transcription_result['segments']):
            chinese_text = segment['text'].strip()
            if not chinese_text:
                continue
            
            self.log_message(f"Translating segment {i+1}/{len(transcription_result['segments'])}")
            
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
                    'text': vietnamese_text
                }
                subtitles.append(subtitle)
                
                self.log_message(f"CN: {chinese_text}")
                self.log_message(f"VI: {vietnamese_text}")
                self.log_message("---")
                
            except Exception as e:
                self.log_message(f"⚠️ Translation error for segment {i+1}: {e}")
                # Use original Chinese text if translation fails
                subtitles.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': chinese_text
                })
        
        return subtitles
    
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
    
    def save_subtitles(self, subtitles, output_file):
        """Save subtitles to SRT file"""
        self.log_message("💾 Saving subtitle file...")
        
        srt_subtitles = pysrt.SubRipFile()
        
        for i, subtitle in enumerate(subtitles):
            start_time = pysrt.SubRipTime(seconds=subtitle['start'])
            end_time = pysrt.SubRipTime(seconds=subtitle['end'])
            
            srt_subtitle = pysrt.SubRipItem(
                index=i+1,
                start=start_time,
                end=end_time,
                text=subtitle['text']
            )
            srt_subtitles.append(srt_subtitle)
        
        srt_subtitles.save(output_file, encoding='utf-8')
        self.log_message("✅ Subtitle file saved successfully")
    
    def show_install_dependencies(self):
        """Show dialog to install dependencies"""
        msg = """Some required packages are missing. Would you like to install them?

Required packages:
• openai-whisper (for speech recognition)
• moviepy (for video processing)
• googletrans (for translation)
• pysrt (for subtitle files)

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
            "pysrt"
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
    app = VideoSubtitleTool(root)
    root.mainloop()

if __name__ == "__main__":
    main() 