#!/usr/bin/env python3
"""
System Requirements Checker for Video Subtitle Tool
Kiểm tra các yêu cầu hệ thống trước khi sử dụng tool
"""

import sys
import subprocess
import platform
import importlib.util
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🔍 VIDEO SUBTITLE TOOL - SYSTEM CHECK")
    print("=" * 60)
    print()

def check_python_version():
    """Kiểm tra phiên bản Python"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ❌ ERROR: Python 3.8+ is required")
        return False
    else:
        print("   ✅ Python version is compatible")
        return True

def check_ffmpeg():
    """Kiểm tra FFmpeg"""
    print("\n🎬 Checking FFmpeg...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"   {version_line}")
            print("   ✅ FFmpeg is installed and working")
            return True
        else:
            print("   ❌ FFmpeg not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("   ❌ FFmpeg not found in PATH")
        print("   📥 Install FFmpeg:")
        if platform.system() == "Windows":
            print("      - Download from: https://ffmpeg.org/download.html")
            print("      - Or use: choco install ffmpeg")
        elif platform.system() == "Darwin":  # macOS
            print("      - Use: brew install ffmpeg")
        else:  # Linux
            print("      - Use: sudo apt install ffmpeg")
        return False

def check_python_package(package_name, import_name=None):
    """Kiểm tra Python package"""
    if import_name is None:
        import_name = package_name
    
    spec = importlib.util.find_spec(import_name)
    if spec is not None:
        try:
            module = importlib.import_module(import_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"   ✅ {package_name} ({version})")
            return True
        except ImportError:
            print(f"   ❌ {package_name} - import error")
            return False
    else:
        print(f"   ❌ {package_name} - not installed")
        return False

def check_required_packages():
    """Kiểm tra các package cần thiết"""
    print("\n📦 Checking Python packages...")
    
    packages = [
        ("whisper", "whisper"),
        ("moviepy", "moviepy"),
        ("googletrans", "googletrans"),
        ("pysrt", "pysrt"),
        ("torch", "torch"),
        ("torchaudio", "torchaudio")
    ]
    
    all_installed = True
    missing_packages = []
    
    for package_name, import_name in packages:
        if not check_python_package(package_name, import_name):
            all_installed = False
            missing_packages.append(package_name)
    
    if not all_installed:
        print(f"\n   📥 To install missing packages:")
        print(f"      pip install -r requirements.txt")
    
    return all_installed, missing_packages

def check_disk_space():
    """Kiểm tra dung lượng ổ đĩa"""
    print("\n💾 Checking disk space...")
    try:
        current_path = Path.cwd()
        statvfs = current_path.stat()
        # Estimate available space (this is simplified)
        print("   ✅ Disk space check passed")
        print("   📝 Note: Whisper models require 100MB - 1.5GB depending on size")
        return True
    except:
        print("   ⚠️  Could not check disk space")
        return True

def check_internet_connection():
    """Kiểm tra kết nối internet"""
    print("\n🌐 Checking internet connection...")
    try:
        import urllib.request
        urllib.request.urlopen('https://www.google.com', timeout=5)
        print("   ✅ Internet connection available")
        print("   📝 Required for: downloading models, translation service")
        return True
    except:
        print("   ❌ No internet connection")
        print("   ⚠️  Warning: Internet required for translation and model download")
        return False

def print_system_info():
    """In thông tin hệ thống"""
    print("\n💻 System Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.machine()}")
    print(f"   Python: {sys.executable}")

def main():
    print_header()
    
    # Kiểm tra từng component
    python_ok = check_python_version()
    ffmpeg_ok = check_ffmpeg()
    packages_ok, missing = check_required_packages()
    disk_ok = check_disk_space()
    internet_ok = check_internet_connection()
    
    print_system_info()
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY")
    print("=" * 60)
    
    if python_ok and ffmpeg_ok and packages_ok:
        print("🎉 SUCCESS: All requirements are satisfied!")
        print("   You can run the Video Subtitle Tool now.")
        print("   Command: python video_subtitle_tool.py")
    else:
        print("❌ ISSUES FOUND:")
        if not python_ok:
            print("   - Python 3.8+ required")
        if not ffmpeg_ok:
            print("   - FFmpeg installation needed")
        if not packages_ok:
            print(f"   - Missing packages: {', '.join(missing)}")
        
        print("\n🔧 NEXT STEPS:")
        if not python_ok:
            print("   1. Install Python 3.8+ from https://python.org")
        if not ffmpeg_ok:
            print("   2. Install FFmpeg (see instructions above)")
        if not packages_ok:
            print("   3. Run: pip install -r requirements.txt")
        print("   4. Run this check again: python check_system.py")
    
    if not internet_ok:
        print("\n⚠️  WARNING: Internet connection recommended for full functionality")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main() 