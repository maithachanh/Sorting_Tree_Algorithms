"""
Input Configuration View: Create custom array/tree data with presets, size sliders, and live preview.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSpinBox, QSlider, QFrame, QGroupBox, QButtonGroup, QRadioButton
)
from PyQt5.QtCore import Qt, pyqtSignal
from utils.array_generator import ArrayGenerator
from core.session_manager import SessionManager
from config import DEFAULT_ARRAY_SIZE, MIN_ARRAY_SIZE, MAX_ARRAY_SIZE

class InputView(QWidget):
    continue_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = SessionManager.instance()
        self.current_array = list(self.session.sorting_array)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)

        # Title / Header
        title_box = QVBoxLayout()
        title_lbl = QLabel("🛠️ Bước 1: Khởi Tạo & Cấu Hình Dữ Liệu")
        title_lbl.setStyleSheet("font-size: 22px; font-weight: bold; color: #38bdf8;")
        sub_lbl = QLabel("Tùy chỉnh số lượng phần tử, nhập giá trị thủ công hoặc tạo mảng ngẫu nhiên theo các mẫu có sẵn.")
        sub_lbl.setStyleSheet("color: #94a3b8; font-size: 14px;")
        title_box.addWidget(title_lbl)
        title_box.addWidget(sub_lbl)
        main_layout.addLayout(title_box)

        # Container Card
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(18)

        # 1. Size control
        size_layout = QHBoxLayout()
        lbl_size = QLabel("📊 Số lượng phần tử (N):")
        lbl_size.setStyleSheet("font-size: 14px; font-weight: 600; color: #f8fafc;")
        size_layout.addWidget(lbl_size)

        self.spin_size = QSpinBox()
        self.spin_size.setRange(MIN_ARRAY_SIZE, MAX_ARRAY_SIZE)
        self.spin_size.setValue(len(self.current_array))
        self.spin_size.setFixedWidth(80)
        self.spin_size.valueChanged.connect(self._on_size_changed)
        size_layout.addWidget(self.spin_size)

        self.slider_size = QSlider(Qt.Horizontal)
        self.slider_size.setRange(MIN_ARRAY_SIZE, MAX_ARRAY_SIZE)
        self.slider_size.setValue(len(self.current_array))
        self.slider_size.valueChanged.connect(self.spin_size.setValue)
        size_layout.addWidget(self.slider_size)

        card_layout.addLayout(size_layout)

        # 2. Preset Generator Buttons
        preset_box = QGroupBox("Mẫu Sinh Dữ Liệu Nhanh")
        preset_layout = QHBoxLayout(preset_box)
        preset_layout.setSpacing(10)

        btn_random = QPushButton("🎲 Ngẫu Nhiên")
        btn_random.clicked.connect(self._gen_random)
        preset_layout.addWidget(btn_random)

        btn_reversed = QPushButton("📉 Nghịch Đảo")
        btn_reversed.clicked.connect(self._gen_reversed)
        preset_layout.addWidget(btn_reversed)

        btn_nearly = QPushButton("📈 Gần Như Đã Sắp")
        btn_nearly.clicked.connect(self._gen_nearly_sorted)
        preset_layout.addWidget(btn_nearly)

        btn_duplicates = QPushButton("🔁 Nhiều Trùng Lặp")
        btn_duplicates.clicked.connect(self._gen_few_unique)
        preset_layout.addWidget(btn_duplicates)

        card_layout.addWidget(preset_box)

        # 3. Custom Value Text Input
        input_box = QGroupBox("Nhập Thủ Công Giá Trị (Cách nhau bởi dấu phẩy hoặc khoảng trắng)")
        input_layout = QVBoxLayout(input_box)

        self.txt_input = QLineEdit()
        self.txt_input.setPlaceholderText("Ví dụ: 45, 12, 85, 32, 89, 39, 69, 44...")
        self.txt_input.setText(", ".join(map(str, self.current_array)))
        self.txt_input.textChanged.connect(self._on_text_changed)
        input_layout.addWidget(self.txt_input)

        self.lbl_status = QLabel("✓ Dữ liệu mảng hợp lệ (15 phần tử)")
        self.lbl_status.setStyleSheet("color: #10b981; font-size: 12px; font-weight: 500;")
        input_layout.addWidget(self.lbl_status)

        card_layout.addWidget(input_box)

        # 4. Live Mini Visual Preview
        preview_box = QGroupBox("Xem Trước Trực Quan Dữ Liệu")
        prev_layout = QVBoxLayout(preview_box)
        self.lbl_preview_bars = QLabel()
        self.lbl_preview_bars.setMinimumHeight(45)
        self.lbl_preview_bars.setStyleSheet("background-color: #0b1120; border-radius: 6px; padding: 5px;")
        prev_layout.addWidget(self.lbl_preview_bars)
        card_layout.addWidget(preview_box)

        main_layout.addWidget(card)

        # Bottom Continue Action Button
        bot_layout = QHBoxLayout()
        bot_layout.addStretch()

        self.btn_continue = QPushButton("Tiếp Tục Chọn Giải Thuật ➔")
        self.btn_continue.setObjectName("btn_primary")
        self.btn_continue.setStyleSheet("""
            QPushButton {
                background-color: #0284c7;
                color: #ffffff;
                font-size: 15px;
                font-weight: bold;
                padding: 12px 28px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0ea5e9;
            }
        """)
        self.btn_continue.clicked.connect(self._on_continue)
        bot_layout.addWidget(self.btn_continue)

        main_layout.addLayout(bot_layout)
        self._update_preview()

    def _on_size_changed(self, size):
        self.slider_size.blockSignals(True)
        self.slider_size.setValue(size)
        self.slider_size.blockSignals(False)
        self.current_array = ArrayGenerator.generate_random(size=size, min_val=5, max_val=100)
        self.txt_input.blockSignals(True)
        self.txt_input.setText(", ".join(map(str, self.current_array)))
        self.txt_input.blockSignals(False)
        self.session.set_sorting_array(self.current_array)
        self.session.set_tree_elements(self.current_array)
        self.lbl_status.setText(f"✓ Dữ liệu mảng hợp lệ ({len(self.current_array)} phần tử)")
        self.lbl_status.setStyleSheet("color: #10b981; font-size: 12px;")
        self.btn_continue.setEnabled(True)
        self._update_preview()

    def _gen_random(self):
        size = self.spin_size.value()
        self.current_array = ArrayGenerator.generate_random(size=size, min_val=5, max_val=100)
        self._apply_new_array()

    def _gen_reversed(self):
        size = self.spin_size.value()
        self.current_array = ArrayGenerator.generate_reversed(size=size, min_val=5, max_val=100)
        self._apply_new_array()

    def _gen_nearly_sorted(self):
        size = self.spin_size.value()
        self.current_array = ArrayGenerator.generate_nearly_sorted(size=size, min_val=5, max_val=100)
        self._apply_new_array()

    def _gen_few_unique(self):
        size = self.spin_size.value()
        self.current_array = ArrayGenerator.generate_few_unique(size=size, min_val=10, max_val=60)
        self._apply_new_array()

    def _apply_new_array(self):
        self.txt_input.blockSignals(True)
        self.txt_input.setText(", ".join(map(str, self.current_array)))
        self.txt_input.blockSignals(False)
        self.session.set_sorting_array(self.current_array)
        self.session.set_tree_elements(self.current_array)
        self.lbl_status.setText(f"✓ Dữ liệu mảng hợp lệ ({len(self.current_array)} phần tử)")
        self.lbl_status.setStyleSheet("color: #10b981; font-size: 12px;")
        self.btn_continue.setEnabled(True)
        self._update_preview()

    def _on_text_changed(self, text):
        success, result = ArrayGenerator.parse_user_input(text)
        if success:
            self.current_array = result
            self.spin_size.blockSignals(True)
            self.slider_size.blockSignals(True)
            self.spin_size.setValue(len(result))
            self.slider_size.setValue(len(result))
            self.spin_size.blockSignals(False)
            self.slider_size.blockSignals(False)

            self.session.set_sorting_array(self.current_array)
            self.session.set_tree_elements(self.current_array)
            self.lbl_status.setText(f"✓ Dữ liệu mảng hợp lệ ({len(self.current_array)} phần tử)")
            self.lbl_status.setStyleSheet("color: #10b981; font-size: 12px;")
            self.btn_continue.setEnabled(True)
            self._update_preview()
        else:
            self.lbl_status.setText(f"✗ {result}")
            self.lbl_status.setStyleSheet("color: #ef4444; font-size: 12px;")
            self.btn_continue.setEnabled(False)

    def _update_preview(self):
        if not self.current_array:
            self.lbl_preview_bars.setText("")
            return
        # Text based preview
        items_str = "  ".join(f"[{x}]" for x in self.current_array)
        self.lbl_preview_bars.setText(f"<span style='color: #38bdf8; font-family: Consolas; font-weight: bold;'>{items_str}</span>")

    def _on_continue(self):
        self.session.set_sorting_array(self.current_array)
        self.session.set_tree_elements(self.current_array)
        self.continue_requested.emit()
