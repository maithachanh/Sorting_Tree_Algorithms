"""
Dialog shown upon algorithm completion, asking the user how they would like to proceed.
"""
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt

class NextActionDialog(QDialog):
    ACTION_RERUN = "rerun"
    ACTION_CHANGE_ALGO = "change_algo"
    ACTION_CHANGE_DATA = "change_data"

    def __init__(self, algo_name, parent=None):
        super().__init__(parent)
        self.selected_action = None
        self.setWindowTitle("🎉 Mô Phỏng Hoàn Tất")
        self.setFixedSize(480, 290)
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Title / Banner
        lbl_title = QLabel("🎉 Thuật Toán Đã Chạy Xong!")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #10b981;")
        layout.addWidget(lbl_title)

        lbl_desc = QLabel(
            f"Bạn vừa hoàn thành mô phỏng thuật toán <b>{algo_name}</b>.<br>"
            "Bạn có muốn tiếp tục hay thay đổi cấu hình dữ liệu?"
        )
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("color: #e2e8f0; font-size: 13px; line-height: 1.4;")
        layout.addWidget(lbl_desc)

        # Options Container
        btn_box = QVBoxLayout()
        btn_box.setSpacing(10)

        # Option 1: Re-run
        btn_rerun = QPushButton("🔄 Chạy Lại Thuật Toán Này (Re-run)")
        btn_rerun.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                border: 1px solid #334155;
                color: #f8fafc;
                font-weight: 600;
                padding: 10px;
                border-radius: 8px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #334155;
                border-color: #38bdf8;
                color: #38bdf8;
            }
        """)
        btn_rerun.clicked.connect(lambda: self._choose(self.ACTION_RERUN))
        btn_box.addWidget(btn_rerun)

        # Option 2: Keep data, choose another algorithm
        btn_change_algo = QPushButton("📋 Giữ Mảng Hiện Tại & Chọn Giải Thuật Khác")
        btn_change_algo.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                border: 1px solid #334155;
                color: #f8fafc;
                font-weight: 600;
                padding: 10px;
                border-radius: 8px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #334155;
                border-color: #38bdf8;
                color: #38bdf8;
            }
        """)
        btn_change_algo.clicked.connect(lambda: self._choose(self.ACTION_CHANGE_ALGO))
        btn_box.addWidget(btn_change_algo)

        # Option 3: Modify input array
        btn_change_data = QPushButton("✏️ Nhập Mảng Mới Hoặc Đổi Số Lượng Phần Tử")
        btn_change_data.setStyleSheet("""
            QPushButton {
                background-color: #0284c7;
                border: none;
                color: #ffffff;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: #0ea5e9;
            }
        """)
        btn_change_data.clicked.connect(lambda: self._choose(self.ACTION_CHANGE_DATA))
        btn_box.addWidget(btn_change_data)

        layout.addLayout(btn_box)

    def _choose(self, action):
        self.selected_action = action
        self.accept()
