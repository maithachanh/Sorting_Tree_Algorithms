"""
Entry point of the Algorithm Visualizer Desktop Application.
"""
import sys
import os
import ctypes

def get_base_dir():
    """Lấy đường dẫn gốc chuẩn xác khi chạy mã nguồn hoặc chạy file .exe độc lập"""
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
sys.path.insert(0, BASE_DIR)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui.main_window import MainWindow
from config import APP_TITLE

# Import stylesheet an toàn
try:
    from utils.theme import THEME_STYLESHEET
except ImportError:
    try:
        from utils.theme import DARK_THEME_QSS as THEME_STYLESHEET
    except ImportError:
        THEME_STYLESHEET = ""

def main():
    # 1. Đặt App ID để Windows Taskbar hiển thị đúng Icon riêng của App
    try:
        myappid = 'visualalgostudio.desktop.app.v2'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    # 2. Khởi tạo ứng dụng Qt
    app = QApplication(sys.argv)
    if THEME_STYLESHEET:
        app.setStyleSheet(THEME_STYLESHEET)

    # 3. Gán Icon ứng dụng cho Taskbar và Window Title
    icon_path = os.path.join(BASE_DIR, "assets", "app_icon.ico")
    if not os.path.exists(icon_path):
        icon_path = os.path.join(BASE_DIR, "assets", "app_icon.png")
        
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)

    # 4. Khởi chạy cửa sổ chính
    window = MainWindow()
    window.setWindowTitle(APP_TITLE)
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()