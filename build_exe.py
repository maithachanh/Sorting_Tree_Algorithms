"""
Script đóng gói ứng dụng Visual AlgoStudio thành file .exe độc lập.
Chạy: python build_exe.py
"""
import sys
import subprocess
import os

def build():
    print("=" * 60)
    print("  BẮT ĐẦU ĐÓNG GÓI ỨNG DỤNG VISUAL ALGOSTUDIO (.EXE)")
    print("=" * 60)

    # 1. Đảm bảo đã cài pyinstaller và pillow
    print("\n[1/3] Đang kiểm tra & cài đặt PyInstaller, Pillow...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller", "pillow"])

    # 2. Sinh icon nếu chưa có
    if not os.path.exists("assets/app_icon.ico"):
        print("\n[2/3] Đang tạo icon ứng dụng...")
        subprocess.check_call([sys.executable, "generate_icon.py"])
    else:
        print("\n[2/3] Icon assets/app_icon.ico đã sẵn sàng.")

    # 3. Tiến hành đóng gói qua PyInstaller
    print("\n[3/3] Đang đóng gói ứng dụng (sẽ mất khoảng 10-30 giây)...")
    spec_file = "Visual_AlgoStudio.spec"
    
    cmd = [sys.executable, "-m", "PyInstaller", "--clean", spec_file]
    subprocess.check_call(cmd)

    exe_path = os.path.join("dist", "Visual_AlgoStudio.exe")
    print("\n" + "=" * 60)
    if os.path.exists(exe_path):
        print("  🎉 THÀNH CÔNG! ĐÃ TẠO FILE EXE:")
        print(f"  👉 {os.path.abspath(exe_path)}")
        print("=" * 60)
        print("\nBạn có thể nhấp đúp trực tiếp vào file Visual_AlgoStudio.exe để chạy!")
    else:
        print("  ❌ Có lỗi xảy ra, vui lòng kiểm tra thông báo phía trên.")
        print("=" * 60)

if __name__ == "__main__":
    build()