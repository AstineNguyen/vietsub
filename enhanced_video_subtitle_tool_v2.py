#!/usr/bin/env python3
"""
Enhanced Video Subtitle Tool V2 - Improved UI and Functionality
Công cụ tạo phụ đề video nâng cao với giao diện được cải thiện
"""

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

def check_dependencies_available():
    """Check if all dependencies are available"""
    try:
        import whisper
        import moviepy.editor as mp
        from deep_translator import GoogleTranslator
        import pysrt
        import pytesseract
        return True
    except ImportError:
        return False

# Try to import dependencies at startup
try:
    import whisper
    import moviepy.editor as mp
    from deep_translator import GoogleTranslator
    import pysrt
    import pytesseract
except ImportError:
    pass

class EnhancedVideoSubtitleToolV2:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Enhanced Video Subtitle Tool V2")
        
        # Get screen dimensions and set appropriate window size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size to 80% of screen, but max 1200x700
        window_width = min(int(screen_width * 0.8), 1200)
        window_height = min(int(screen_height * 0.8), 700)
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='#1e1e1e')
        self.root.resizable(True, True)
        
        # Processing control variables
        self.is_processing = False
        self.should_stop = False
        self.processing_thread = None
        
        # Settings file for session memory
        self.settings_file = Path.cwd() / "subtitle_tool_settings.json"
        
        # Variables
        self.video_path = tk.StringVar()
        self.output_folder = tk.StringVar(value=str(Path.cwd()))
        self.progress_var = tk.DoubleVar()
        self.status_text = tk.StringVar(value="Ready to process video...")
        
        # Model settings
        self.model_var = tk.StringVar(value="base")
        self.max_length_var = tk.StringVar(value="80")
        
        # OCR Settings
        self.enable_ocr = tk.BooleanVar(value=True)
        self.ocr_interval = tk.StringVar(value="2.0")
        self.overlay_video = tk.BooleanVar(value=False)
        
        # Export options - removed auto-selection, use saved preferences
        self.export_srt = tk.BooleanVar(value=False)
        self.export_transcript = tk.BooleanVar(value=False)
        self.export_ocr_only = tk.BooleanVar(value=False)
        
        # Output settings
        self.output_filename = tk.StringVar(value="")
        self.auto_output_folder = tk.BooleanVar(value=True)
        
        # Colors
        self.bg_color = '#1e1e1e'
        self.card_color = '#2d2d2d'
        self.accent_color = '#0078d4'
        self.text_color = '#ffffff'
        self.success_color = '#28a745'
        self.warning_color = '#ffc107'
        self.danger_color = '#dc3545'
        
        # Configure Tesseract path (Windows)
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        except:
            pass
        
        # Load saved settings
        self.load_settings()
        
        # Setup UI
        self.setup_ui()
        
        # Check dependencies on startup
        if not check_dependencies_available():
            self.show_install_dependencies()
        
        # Save settings when closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Load model settings
                self.model_var.set(settings.get('model', 'base'))
                self.max_length_var.set(settings.get('max_length', '80'))
                
                # Load OCR settings
                self.enable_ocr.set(settings.get('enable_ocr', True))
                self.ocr_interval.set(settings.get('ocr_interval', '2.0'))
                self.overlay_video.set(settings.get('overlay_video', False))
                
                # Load export options
                self.export_srt.set(settings.get('export_srt', True))
                self.export_transcript.set(settings.get('export_transcript', True))
                self.export_ocr_only.set(settings.get('export_ocr_only', False))
                
                # Load output settings
                self.auto_output_folder.set(settings.get('auto_output_folder', True))
                self.output_folder.set(settings.get('output_folder', str(Path.cwd())))
                
                print("✅ Settings loaded from previous session")
        except Exception as e:
            print(f"⚠️ Could not load settings: {e}")
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            settings = {
                'model': self.model_var.get(),
                'max_length': self.max_length_var.get(),
                'enable_ocr': self.enable_ocr.get(),
                'ocr_interval': self.ocr_interval.get(),
                'overlay_video': self.overlay_video.get(),
                'export_srt': self.export_srt.get(),
                'export_transcript': self.export_transcript.get(),
                'export_ocr_only': self.export_ocr_only.get(),
                'auto_output_folder': self.auto_output_folder.get(),
                'output_folder': self.output_folder.get()
            }
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Could not save settings: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        # Stop processing if running
        if self.is_processing:
            if messagebox.askyesno("Confirm Exit", "Processing is in progress. Do you want to stop and exit?"):
                self.stop_processing()
                # Wait a moment for cleanup
                self.root.after(500, self.root.destroy)
            return
        
        # Save settings and exit
        self.save_settings()
        self.root.destroy()

    def setup_ui(self):
        """Setup the main UI with simple centered layout"""
        # Create main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill="both", expand=True)
        
        # Create canvas and scrollbar
        main_canvas = tk.Canvas(main_container, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=main_canvas.yview)
        
        # Create scrollable frame
        self.scrollable_frame = tk.Frame(main_canvas, bg=self.bg_color)
        
        # Center content using padx
        canvas_window = main_canvas.create_window(0, 0, anchor="nw", window=self.scrollable_frame)
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Configure canvas sizing and centering
        def configure_canvas(event=None):
            # Update scroll region
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
            
            # Center the content
            canvas_width = main_canvas.winfo_width()
            content_width = min(800, canvas_width - 100)  # Max width with margins
            x_offset = max(0, (canvas_width - content_width) // 2)
            
            main_canvas.coords(canvas_window, x_offset, 0)
            main_canvas.itemconfig(canvas_window, width=content_width)
        
        self.scrollable_frame.bind("<Configure>", configure_canvas)
        main_canvas.bind("<Configure>", configure_canvas)
        
        # Pack canvas and scrollbar
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def bind_mousewheel(event):
            main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
        def unbind_mousewheel(event):
            main_canvas.unbind_all("<MouseWheel>")
            
        main_canvas.bind("<Enter>", bind_mousewheel)
        main_canvas.bind("<Leave>", unbind_mousewheel)
        
        # Create sections
        self.create_header()
        self.create_file_selection()
        self.create_settings_tabs()
        self.create_progress_section()
        self.create_log_section()
        self.create_action_buttons()
    
    def create_header(self):
        """Create header section"""
        header_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        title_label = tk.Label(
            header_frame,
            text="🎬 Enhanced Video Subtitle Tool V2",
            font=('Segoe UI', 18, 'bold'),
            bg=self.bg_color,
            fg='#ffffff'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Chinese Audio + OCR → Vietnamese Subtitles with Video Output",
            font=('Segoe UI', 10),
            bg=self.bg_color,
            fg='#888888'
        )
        subtitle_label.pack()
    
    def create_file_selection(self):
        """Create file selection section"""
        file_frame = tk.Frame(self.scrollable_frame, bg=self.card_color, relief='raised', bd=1)
        file_frame.pack(fill='x', padx=20, pady=10)
        
        # Title
        tk.Label(
            file_frame,
            text="📁 File Selection",
            font=('Segoe UI', 12, 'bold'),
            bg=self.card_color,
            fg=self.text_color
        ).pack(anchor='w', padx=15, pady=(15, 10))
        
        # Video file selection
        video_row = tk.Frame(file_frame, bg=self.card_color)
        video_row.pack(fill='x', padx=15, pady=5)
        
        tk.Label(video_row, text="Video File:", bg=self.card_color, fg=self.text_color, width=12, anchor='w').pack(side='left')
        
        video_entry_frame = tk.Frame(video_row, bg=self.card_color)
        video_entry_frame.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        self.video_entry = tk.Entry(
            video_entry_frame,
            textvariable=self.video_path,
            bg='#404040',
            fg='white',
            insertbackground='white',
            relief='flat',
            bd=5
        )
        self.video_entry.pack(side='left', fill='x', expand=True)
        
        self.browse_video_btn = tk.Button(
            video_entry_frame,
            text="Browse",
            command=self.browse_video,
            bg=self.accent_color,
            fg='white',
            relief='flat',
            padx=20,
            cursor='hand2'
        )
        self.browse_video_btn.pack(side='right', padx=(10, 0))
        
        # Output folder selection
        output_row = tk.Frame(file_frame, bg=self.card_color)
        output_row.pack(fill='x', padx=15, pady=(5, 15))
        
        tk.Label(output_row, text="Output Folder:", bg=self.card_color, fg=self.text_color, width=12, anchor='w').pack(side='left')
        
        output_entry_frame = tk.Frame(output_row, bg=self.card_color)
        output_entry_frame.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        self.output_entry = tk.Entry(
            output_entry_frame,
            textvariable=self.output_folder,
            bg='#404040',
            fg='white',
            insertbackground='white',
            relief='flat',
            bd=5
        )
        self.output_entry.pack(side='left', fill='x', expand=True)
        
        self.browse_output_btn = tk.Button(
            output_entry_frame,
            text="Browse",
            command=self.browse_output,
            bg=self.accent_color,
            fg='white',
            relief='flat',
            padx=20,
            cursor='hand2'
        )
        self.browse_output_btn.pack(side='right', padx=(10, 0))
    
    def create_settings_tabs(self):
        """Create tabbed settings section"""
        settings_frame = tk.Frame(self.scrollable_frame, bg=self.card_color, relief='raised', bd=1)
        settings_frame.pack(fill='x', padx=20, pady=10)
        
        # Title
        tk.Label(
            settings_frame,
            text="⚙️ Settings",
            font=('Segoe UI', 12, 'bold'),
            bg=self.card_color,
            fg=self.text_color
        ).pack(anchor='w', padx=15, pady=(15, 10))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(settings_frame)
        notebook.pack(fill='x', padx=15, pady=(0, 15))
        
        # Configure notebook style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.card_color)
        style.configure('TNotebook.Tab', background='#404040', foreground='white', padding=[12, 8])
        
        # AI Model Tab
        model_tab = tk.Frame(notebook, bg=self.card_color)
        notebook.add(model_tab, text="🤖 AI Model")
        
        model_row = tk.Frame(model_tab, bg=self.card_color)
        model_row.pack(fill='x', padx=10, pady=10)
        
        tk.Label(model_row, text="Whisper Model:", bg=self.card_color, fg=self.text_color).pack(side='left')
        
        model_combo = ttk.Combobox(
            model_row,
            textvariable=self.model_var,
            values=["tiny", "base", "small", "medium", "large"],
            state="readonly",
            width=15
        )
        model_combo.pack(side='left', padx=(10, 0))
        
        tk.Label(model_row, text="Max Line Length:", bg=self.card_color, fg=self.text_color).pack(side='left', padx=(20, 0))
        
        length_spin = tk.Spinbox(
            model_row,
            textvariable=self.max_length_var,
            from_=40,
            to=120,
            width=8,
            bg='#404040',
            fg='white',
            insertbackground='white'
        )
        length_spin.pack(side='left', padx=(10, 0))
        
        # OCR Tab
        ocr_tab = tk.Frame(notebook, bg=self.card_color)
        notebook.add(ocr_tab, text="👁️ OCR Settings")
        
        ocr_content = tk.Frame(ocr_tab, bg=self.card_color)
        ocr_content.pack(fill='x', padx=10, pady=10)
        
        ocr_enable = tk.Checkbutton(
            ocr_content,
            text="Enable OCR (Read text from video)",
            variable=self.enable_ocr,
            bg=self.card_color,
            fg=self.text_color,
            selectcolor='#404040',
            activebackground=self.card_color,
            activeforeground=self.text_color
        )
        ocr_enable.pack(anchor='w')
        
        interval_row = tk.Frame(ocr_content, bg=self.card_color)
        interval_row.pack(fill='x', pady=(10, 0))
        
        tk.Label(interval_row, text="OCR Interval (seconds):", bg=self.card_color, fg=self.text_color).pack(side='left')
        
        interval_spin = tk.Spinbox(
            interval_row,
            textvariable=self.ocr_interval,
            from_=0.5,
            to=10.0,
            increment=0.5,
            width=8,
            bg='#404040',
            fg='white',
            insertbackground='white'
        )
        interval_spin.pack(side='left', padx=(10, 0))
        
        # Export Tab
        export_tab = tk.Frame(notebook, bg=self.card_color)
        notebook.add(export_tab, text="📤 Export Options")
        
        export_content = tk.Frame(export_tab, bg=self.card_color)
        export_content.pack(fill='x', padx=10, pady=10)
        
        export_checks = [
            (self.export_srt, "Export SRT file (subtitle file)"),
            (self.export_transcript, "Export transcript (combined audio + OCR)"),
            (self.export_ocr_only, "Export OCR-only text"),
        ]
        
        for var, text in export_checks:
            check = tk.Checkbutton(
                export_content,
                text=text,
                variable=var,
                bg=self.card_color,
                fg=self.text_color,
                selectcolor='#404040',
                activebackground=self.card_color,
                activeforeground=self.text_color
            )
            check.pack(anchor='w', pady=2)
        
        # Video Overlay (now enabled with OpenCV)
        overlay_check = tk.Checkbutton(
            export_content,
            text="Create video with burnt-in subtitles (uses OpenCV)",
            variable=self.overlay_video,
            bg=self.card_color,
            fg=self.text_color,
            selectcolor='#404040',
            activebackground=self.card_color,
            activeforeground=self.text_color
        )
        overlay_check.pack(anchor='w', pady=2)
        
        # Info label
        info_label = tk.Label(
            export_content,
            text="💡 Video overlay now uses OpenCV - no ImageMagick needed!",
            bg=self.card_color,
            fg=self.success_color,
            font=('Segoe UI', 8)
        )
        info_label.pack(anchor='w', pady=(5, 0))
        
        # Output Settings Tab
        output_tab = tk.Frame(notebook, bg=self.card_color)
        notebook.add(output_tab, text="📁 Output Settings")
        
        output_content = tk.Frame(output_tab, bg=self.card_color)
        output_content.pack(fill='x', padx=10, pady=10)
        
        # Custom filename
        filename_frame = tk.Frame(output_content, bg=self.card_color)
        filename_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            filename_frame,
            text="Custom Output Filename:",
            bg=self.card_color,
            fg=self.text_color,
            font=('Segoe UI', 10, 'bold')
        ).pack(anchor='w')
        
        filename_row = tk.Frame(filename_frame, bg=self.card_color)
        filename_row.pack(fill='x', pady=(5, 0))
        
        self.filename_entry = tk.Entry(
            filename_row,
            textvariable=self.output_filename,
            bg='#404040',
            fg='white',
            insertbackground='white',
            relief='flat',
            bd=5,
            font=('Segoe UI', 10)
        )
        self.filename_entry.pack(side='left', fill='x', expand=True)
        
        tk.Label(
            filename_row,
            text="(Leave empty for auto-name)",
            bg=self.card_color,
            fg='#888888',
            font=('Segoe UI', 8)
        ).pack(side='right', padx=(10, 0))
        
        # Auto output folder option
        auto_folder_check = tk.Checkbutton(
            output_content,
            text="Use video's folder as output folder (recommended)",
            variable=self.auto_output_folder,
            bg=self.card_color,
            fg=self.text_color,
            selectcolor='#404040',
            activebackground=self.card_color,
            activeforeground=self.text_color,
            font=('Segoe UI', 10)
        )
        auto_folder_check.pack(anchor='w', pady=(10, 5))
        
        # Output folder preview
        self.output_preview_label = tk.Label(
            output_content,
            text="Output folder: (Select video first)",
            bg=self.card_color,
            fg='#888888',
            font=('Segoe UI', 9),
            wraplength=400,
            justify='left'
        )
        self.output_preview_label.pack(anchor='w', pady=(0, 10))
        
        # Manual output folder selection (when auto is disabled)
        manual_folder_frame = tk.Frame(output_content, bg=self.card_color)
        manual_folder_frame.pack(fill='x', pady=(0, 10))
        
        self.manual_folder_btn = tk.Button(
            manual_folder_frame,
            text="📁 Choose Custom Output Folder",
            command=self.choose_custom_output,
            bg=self.accent_color,
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            state='disabled'  # Disabled by default when auto is on
        )
        self.manual_folder_btn.pack(side='left')
        
        # Bind auto folder checkbox to enable/disable manual selection
        def toggle_manual_folder():
            if self.auto_output_folder.get():
                self.manual_folder_btn.config(state='disabled')
                self.update_output_preview()
            else:
                self.manual_folder_btn.config(state='normal')
        
        self.auto_output_folder.trace('w', lambda *args: toggle_manual_folder())
        
        # Bind video path to update preview
        self.video_path.trace('w', lambda *args: self.update_output_preview())
    
    def update_output_preview(self):
        """Update output folder preview"""
        try:
            if self.auto_output_folder.get() and self.video_path.get():
                video_folder = str(Path(self.video_path.get()).parent)
                self.output_folder.set(video_folder)
                self.output_preview_label.config(
                    text=f"Output folder: {video_folder}",
                    fg=self.success_color
                )
            elif not self.auto_output_folder.get():
                current_folder = self.output_folder.get()
                self.output_preview_label.config(
                    text=f"Output folder: {current_folder}",
                    fg=self.text_color
                )
            else:
                self.output_preview_label.config(
                    text="Output folder: (Select video first)",
                    fg='#888888'
                )
        except Exception:
            self.output_preview_label.config(
                text="Output folder: (Select video first)",
                fg='#888888'
            )
    
    def choose_custom_output(self):
        """Choose custom output folder"""
        folder_path = filedialog.askdirectory(title="Select Custom Output Folder")
        if folder_path:
            self.output_folder.set(folder_path)
            self.output_preview_label.config(
                text=f"Output folder: {folder_path}",
                fg=self.text_color
            )
    
    def create_progress_section(self):
        """Create progress section"""
        progress_frame = tk.Frame(self.scrollable_frame, bg=self.card_color, relief='raised', bd=1)
        progress_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            progress_frame,
            text="📊 Progress",
            font=('Segoe UI', 12, 'bold'),
            bg=self.card_color,
            fg=self.text_color
        ).pack(anchor='w', padx=15, pady=(15, 10))
        
        # Status label
        self.status_label = tk.Label(
            progress_frame,
            textvariable=self.status_text,
            bg=self.card_color,
            fg=self.text_color,
            font=('Segoe UI', 10)
        )
        self.status_label.pack(anchor='w', padx=15, pady=(0, 10))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=300,
            mode='determinate'
        )
        self.progress_bar.pack(fill='x', padx=15, pady=(0, 15))
    
    def create_log_section(self):
        """Create log section"""
        log_frame = tk.Frame(self.scrollable_frame, bg=self.card_color, relief='raised', bd=1)
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(
            log_frame,
            text="📝 Processing Log",
            font=('Segoe UI', 12, 'bold'),
            bg=self.card_color,
            fg=self.text_color
        ).pack(anchor='w', padx=15, pady=(15, 10))
        
        # Log text area with fixed height
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,  # Fixed height
            bg='#1a1a1a',
            fg='#00ff00',
            insertbackground='white',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        self.log_text.pack(fill='both', expand=True, padx=15, pady=(0, 15))
    
    def create_action_buttons(self):
        """Create action buttons"""
        button_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color)
        button_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        # Process button
        self.process_btn = tk.Button(
            button_frame,
            text="🚀 Generate Enhanced Subtitles",
            command=self.start_processing,
            bg=self.success_color,
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            padx=30,
            pady=15,
            cursor='hand2'
        )
        self.process_btn.pack(side='left', padx=(0, 10))
        
        # Stop button
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹️ Stop Processing",
            command=self.stop_processing,
            bg=self.danger_color,
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            padx=30,
            pady=15,
            cursor='hand2',
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=(0, 10))
        
        # Clear log button
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear Log",
            command=self.clear_log,
            bg='#6c757d',
            fg='white',
            relief='flat',
            padx=20,
            pady=15,
            cursor='hand2'
        )
        clear_btn.pack(side='left')
    
    def browse_video(self):
        """Browse for video file"""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.video_path.set(file_path)
            
            # Only auto-fill filename if it's completely empty (not just from previous session)
            if not self.output_filename.get().strip():
                video_name = Path(file_path).stem
                self.output_filename.set(f"{video_name}_vietnamese")
            
            # Update output preview
            self.update_output_preview()
    
    def browse_output(self):
        """Browse for output folder"""
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            self.output_folder.set(folder_path)
    
    def clear_log(self):
        """Clear the log text"""
        self.log_text.delete(1.0, tk.END)
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
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
        
        # Check if any export option is selected
        if not any([self.export_srt.get(), self.export_transcript.get(), 
                   self.export_ocr_only.get(), self.overlay_video.get()]):
            messagebox.showerror("Error", "Please select at least one export option!")
            return
        
        if not check_dependencies_available():
            self.show_install_dependencies()
            return
        
        # Set processing state
        self.is_processing = True
        self.should_stop = False
        
        # Update UI
        self.process_btn.config(state='disabled', text="Processing...")
        self.stop_btn.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        
        # Save settings before processing
        self.save_settings()
        
        # Start processing in thread
        self.processing_thread = threading.Thread(target=self.process_video)
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def stop_processing(self):
        """Stop the current processing"""
        if self.is_processing:
            self.should_stop = True
            self.log_message("🛑 Stopping processing... Please wait for cleanup...")
            self.update_status("Stopping processing...", None)
            
            # Update UI immediately
            self.stop_btn.config(state='disabled', text="Stopping...")
            
            # The processing thread will handle cleanup and reset UI
    
    def process_video(self):
        """Process the video file with stop functionality"""
        audio_file = None
        try:
            video_file = self.video_path.get()
            output_dir = Path(self.output_folder.get())
            
            # Use custom filename if provided, otherwise use video filename
            if self.output_filename.get().strip():
                video_name = self.output_filename.get().strip()
                self.log_message(f"📝 Using custom filename: {video_name}")
            else:
                video_name = Path(video_file).stem
                self.log_message(f"📝 Using auto filename: {video_name}")
            
            self.log_message("🎬 Starting enhanced video processing...")
            
            # Step 1: Extract audio
            if self.should_stop:
                return
            self.update_status("Extracting audio from video...", 10)
            audio_file = output_dir / f"{video_name}_audio.wav"
            self.extract_audio(video_file, str(audio_file))
            
            # Step 2: Transcribe audio
            if self.should_stop:
                return
            self.update_status("Transcribing Chinese audio...", 25)
            model = whisper.load_model(self.model_var.get())
            result = model.transcribe(str(audio_file), language="zh")
            
            # Step 3: OCR processing (if enabled)
            if self.should_stop:
                return
            ocr_results = []
            if self.enable_ocr.get():
                self.update_status("Processing OCR from video frames...", 45)
                ocr_results = self.extract_ocr_from_video(video_file)
                if self.should_stop:
                    return
            
            # Step 4: Translate content
            if self.should_stop:
                return
            self.update_status("Translating to Vietnamese...", 65)
            translator = GoogleTranslator(source='zh-CN', target='vi')
            
            # Process audio subtitles
            audio_subtitles = self.create_subtitles_from_audio(result, translator)
            if self.should_stop:
                return
            
            # Process OCR subtitles
            ocr_subtitles = []
            if ocr_results:
                ocr_subtitles = self.create_subtitles_from_ocr(ocr_results, translator)
                if self.should_stop:
                    return
            
            # Step 5: Export files
            if self.should_stop:
                return
            self.update_status("Saving output files...", 85)
            
            if self.export_srt.get():
                if self.should_stop:
                    return
                # Save combined SRT
                combined_subtitles = self.merge_subtitles(audio_subtitles, ocr_subtitles)
                srt_file = output_dir / f"{video_name}_enhanced_vietnamese.srt"
                self.save_subtitles(combined_subtitles, str(srt_file))
                self.log_message(f"✅ SRT file saved: {srt_file}")
            
            if self.export_transcript.get():
                if self.should_stop:
                    return
                # Save transcript
                transcript_file = output_dir / f"{video_name}_transcript.txt"
                self.save_transcript(audio_subtitles, ocr_subtitles, str(transcript_file))
                self.log_message(f"✅ Transcript saved: {transcript_file}")
            
            if self.export_ocr_only.get() and ocr_results:
                if self.should_stop:
                    return
                # Save OCR only
                ocr_file = output_dir / f"{video_name}_ocr_only.txt"
                self.save_ocr_text(ocr_subtitles, str(ocr_file))
                self.log_message(f"✅ OCR text saved: {ocr_file}")
            
            # Create video with burnt-in subtitles if requested
            if self.overlay_video.get():
                if self.should_stop:
                    return
                self.update_status("Creating video with burnt-in subtitles...", 90)
                combined_subtitles = self.merge_subtitles(audio_subtitles, ocr_subtitles)
                output_video = output_dir / f"{video_name}_with_subtitles.mp4"
                self.create_video_with_subtitles(video_file, combined_subtitles, str(output_video))
                if self.should_stop:
                    return
                self.log_message(f"✅ Video with subtitles saved: {output_video}")
            
            if not self.should_stop:
                self.update_status("✅ Processing complete!", 100)
                self.log_message("🎉 Enhanced subtitle generation completed successfully!")
            
        except Exception as e:
            if not self.should_stop:
                self.log_message(f"❌ Error: {e}")
                self.update_status("❌ Processing failed", 0)
        finally:
            # Clean up
            if audio_file and audio_file.exists():
                try:
                    audio_file.unlink()
                    if not self.should_stop:
                        self.log_message("🗑️ Temporary audio file cleaned up")
                except:
                    pass
            
            # Handle stop case
            if self.should_stop:
                self.log_message("🛑 Processing stopped by user")
                self.update_status("❌ Processing stopped", 0)
            
            # Reset processing state and UI
            self.is_processing = False
            self.should_stop = False
            self.process_btn.config(state='normal', text="🚀 Generate Enhanced Subtitles")
            self.stop_btn.config(state='disabled', text="⏹️ Stop Processing")
    
    def extract_audio(self, video_file, audio_file):
        """Extract audio from video"""
        self.log_message("🎵 Extracting audio...")
        video = mp.VideoFileClip(video_file)
        audio = video.audio
        audio.write_audiofile(audio_file, verbose=False, logger=None)
        video.close()
        audio.close()
        self.log_message("✅ Audio extracted successfully")
    
    def extract_ocr_from_video(self, video_file):
        """Extract text from video frames using OCR"""
        self.log_message("👁️ Starting OCR processing...")
        ocr_results = []
        interval = float(self.ocr_interval.get())
        
        try:
            cap = cv2.VideoCapture(video_file)
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps
            
            frame_interval = int(fps * interval)
            frame_count = 0
            processed_frames = 0
            
            while True:
                if self.should_stop:
                    break
                    
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    if self.should_stop:
                        break
                        
                    timestamp = frame_count / fps
                    
                    # Convert frame to PIL Image
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(frame_rgb)
                    
                    # Extract text using OCR
                    try:
                        text = pytesseract.image_to_string(pil_image, lang='chi_sim')
                        text = text.strip()
                        
                        if text and len(text) > 2:  # Only keep meaningful text
                            ocr_results.append({
                                'timestamp': timestamp,
                                'text': text
                            })
                            self.log_message(f"OCR at {timestamp:.1f}s: {text[:50]}...")
                    
                    except Exception as e:
                        self.log_message(f"⚠️ OCR error at {timestamp:.1f}s: {e}")
                    
                    processed_frames += 1
                    # Update progress
                    progress = 45 + (processed_frames * 20 / (duration / interval))
                    self.update_status(f"OCR processing... {processed_frames} frames", min(progress, 64))
                
                frame_count += 1
            
            cap.release()
            
            if not self.should_stop:
                self.log_message(f"✅ OCR completed. Found {len(ocr_results)} text segments")
            else:
                self.log_message(f"🛑 OCR stopped. Processed {len(ocr_results)} text segments")
            
        except Exception as e:
            self.log_message(f"❌ OCR processing failed: {e}")
        
        return ocr_results
    
    def create_subtitles_from_audio(self, transcription_result, translator):
        """Create subtitles from audio transcription"""
        subtitles = []
        max_length = int(self.max_length_var.get())
        
        for i, segment in enumerate(transcription_result['segments']):
            if self.should_stop:
                break
                
            chinese_text = segment['text'].strip()
            if not chinese_text:
                continue
            
            self.log_message(f"Translating audio segment {i+1}/{len(transcription_result['segments'])}")
            
            try:
                vietnamese_text = translator.translate(chinese_text)
                
                # Break long lines
                if len(vietnamese_text) > max_length:
                    vietnamese_text = self.break_long_lines(vietnamese_text, max_length)
                
                subtitle = {
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': vietnamese_text,
                    'source': 'audio'
                }
                subtitles.append(subtitle)
                
                self.log_message(f"Audio CN: {chinese_text}")
                self.log_message(f"Audio VI: {vietnamese_text}")
                
            except Exception as e:
                self.log_message(f"⚠️ Translation error for audio segment {i+1}: {e}")
                subtitles.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': chinese_text,
                    'source': 'audio'
                })
        
        return subtitles
    
    def create_subtitles_from_ocr(self, ocr_results, translator):
        """Create subtitles from OCR results"""
        subtitles = []
        
        for i, ocr_item in enumerate(ocr_results):
            if self.should_stop:
                break
                
            chinese_text = ocr_item['text']
            timestamp = ocr_item['timestamp']
            
            try:
                vietnamese_text = translator.translate(chinese_text)
                
                subtitles.append({
                    'start': timestamp,
                    'end': timestamp + 2.0,  # Default 2 second duration
                    'text': vietnamese_text,
                    'source': 'ocr'
                })
                
                self.log_message(f"OCR CN: {chinese_text}")
                self.log_message(f"OCR VI: {vietnamese_text}")
                
            except Exception as e:
                self.log_message(f"⚠️ Translation error for OCR {i+1}: {e}")
        
        return subtitles
    
    def merge_subtitles(self, audio_subs, ocr_subs):
        """Merge audio and OCR subtitles"""
        # Simple merge - you could implement more sophisticated logic
        all_subs = audio_subs + ocr_subs
        # Sort by start time
        all_subs.sort(key=lambda x: x['start'])
        return all_subs
    
    def break_long_lines(self, text, max_length):
        """Break long lines into multiple lines"""
        if len(text) <= max_length:
            return text
        
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
        subs = pysrt.SubRipFile()
        
        for i, subtitle in enumerate(subtitles):
            start_time = pysrt.SubRipTime(seconds=subtitle['start'])
            end_time = pysrt.SubRipTime(seconds=subtitle['end'])
            
            sub = pysrt.SubRipItem(
                index=i+1,
                start=start_time,
                end=end_time,
                text=subtitle['text']
            )
            subs.append(sub)
        
        subs.save(output_file, encoding='utf-8')
    
    def save_transcript(self, audio_subs, ocr_subs, output_file):
        """Save combined transcript"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== ENHANCED VIDEO TRANSCRIPT ===\n\n")
            
            if audio_subs:
                f.write("--- AUDIO TRANSCRIPTION ---\n")
                for sub in audio_subs:
                    f.write(f"[{sub['start']:.1f}s - {sub['end']:.1f}s] {sub['text']}\n")
                f.write("\n")
            
            if ocr_subs:
                f.write("--- OCR TEXT ---\n")
                for sub in ocr_subs:
                    f.write(f"[{sub['start']:.1f}s] {sub['text']}\n")
    
    def save_ocr_text(self, ocr_subs, output_file):
        """Save OCR-only text"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== OCR EXTRACTED TEXT ===\n\n")
            for sub in ocr_subs:
                f.write(f"[{sub['start']:.1f}s] {sub['text']}\n")
    
    def create_video_with_subtitles(self, video_file, subtitles, output_file):
        """Create video with burnt-in subtitles using OpenCV"""
        try:
            self.log_message("🎬 Creating video with burnt-in subtitles...")
            
            # Open input video
            cap = cv2.VideoCapture(video_file)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Setup video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
            
            frame_count = 0
            
            while True:
                if self.should_stop:
                    break
                    
                ret, frame = cap.read()
                if not ret:
                    break
                
                current_time = frame_count / fps
                
                # Find active subtitles at current time
                active_subtitles = []
                for sub in subtitles:
                    if sub['start'] <= current_time <= sub['end']:
                        active_subtitles.append(sub['text'])
                
                # Add subtitles to frame
                if active_subtitles:
                    frame = self.add_subtitles_to_frame(frame, active_subtitles, width, height)
                
                # Write frame
                out.write(frame)
                frame_count += 1
                
                # Update progress occasionally
                if frame_count % int(fps * 2) == 0:  # Every 2 seconds
                    progress = 90 + (frame_count / total_frames) * 9
                    self.update_status(f"Processing video frame {frame_count}/{total_frames}", progress)
            
            # Release resources
            cap.release()
            out.release()
            
            # Use moviepy to add audio back
            self.log_message("🔊 Adding audio to video...")
            video_clip = mp.VideoFileClip(output_file)
            audio_clip = mp.VideoFileClip(video_file).audio
            final_clip = video_clip.set_audio(audio_clip)
            
            # Save final video with audio
            temp_output = output_file.replace('.mp4', '_temp.mp4')
            final_clip.write_videofile(temp_output, verbose=False, logger=None)
            
            # Replace original with final
            import shutil
            shutil.move(temp_output, output_file)
            
            # Cleanup
            video_clip.close()
            audio_clip.close()
            final_clip.close()
            
            self.log_message("✅ Video with subtitles created successfully!")
            
        except Exception as e:
            self.log_message(f"❌ Video creation failed: {e}")
            raise e
    
    def add_subtitles_to_frame(self, frame, subtitles, width, height):
        """Add subtitle text to a video frame with auto word wrap"""
        try:
            # Convert frame to PIL Image for better text rendering
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            draw = ImageDraw.Draw(pil_image)
            
            # Font settings - smaller font size
            font_size = max(14, int(height * 0.025))  # Reduced from 0.04 to 0.025 for smaller text
            try:
                # Try to use a nice font
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                try:
                    # Try other common fonts
                    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
                except:
                    # Fallback to default font
                    font = ImageFont.load_default()
            
            # Calculate usable width (with margins)
            margin_x = int(width * 0.05)  # 5% margin on each side
            margin_y = 30
            usable_width = width - (2 * margin_x)
            
            # Process all subtitles with word wrap
            all_lines = []
            for subtitle in subtitles:
                wrapped_lines = self.wrap_text(subtitle, font, usable_width, draw)
                all_lines.extend(wrapped_lines)
            
            # Position settings
            line_height = font_size + 8
            total_text_height = len(all_lines) * line_height
            y_start = height - margin_y - total_text_height
            
            # Ensure subtitles don't go off-screen at top
            if y_start < margin_y:
                y_start = margin_y
            
            # Draw each line
            for i, line in enumerate(all_lines):
                y_pos = y_start + (i * line_height)
                
                # Get text size for centering
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x_pos = (width - text_width) // 2
                
                # Ensure text doesn't go off-screen horizontally
                if x_pos < margin_x:
                    x_pos = margin_x
                elif x_pos + text_width > width - margin_x:
                    x_pos = width - margin_x - text_width
                
                # Draw text outline (black) - thinner outline
                outline_width = 1
                for dx in range(-outline_width, outline_width + 1):
                    for dy in range(-outline_width, outline_width + 1):
                        if dx != 0 or dy != 0:
                            draw.text((x_pos + dx, y_pos + dy), line, font=font, fill=(0, 0, 0))
                
                # Draw main text (white)
                draw.text((x_pos, y_pos), line, font=font, fill=(255, 255, 255))
            
            # Convert back to OpenCV format
            frame_with_subs = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            return frame_with_subs
            
        except Exception as e:
            self.log_message(f"⚠️ Subtitle overlay error: {e}")
            return frame
    
    def wrap_text(self, text, font, max_width, draw):
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            # Test current line + new word
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            test_width = bbox[2] - bbox[0]
            
            if test_width <= max_width:
                # Word fits, add it to current line
                current_line.append(word)
            else:
                # Word doesn't fit
                if current_line:
                    # Save current line and start new one
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Single word is too long, force it anyway
                    lines.append(word)
                    current_line = []
        
        # Add remaining words
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def show_install_dependencies(self):
        """Show dialog to install dependencies"""
        msg = """Some required packages are missing. Would you like to install them?

Required packages:
• openai-whisper (for speech recognition)
• moviepy (for video processing)
• deep-translator (for translation)
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
            "deep-translator",
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
    app = EnhancedVideoSubtitleToolV2(root)
    root.mainloop()

if __name__ == "__main__":
    main() 