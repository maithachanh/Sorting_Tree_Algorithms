"""
Custom styled modal dialogs for querying target elements (insert, delete, search, LCA).
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSpinBox, QComboBox, QFrame
)
from PyQt5.QtCore import Qt

class ValuePromptDialog(QDialog):
    def __init__(self, title, message, default_val=25, available_choices=None, is_two_values=False, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(440, 240)
        self.result_value = default_val
        self.is_two_values = is_two_values
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)

        # Title
        lbl_title = QLabel(f"🎯 {title}")
        lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #38bdf8;")
        layout.addWidget(lbl_title)

        # Prompt Message
        lbl_msg = QLabel(message)
        lbl_msg.setWordWrap(True)
        lbl_msg.setStyleSheet("color: #f8fafc; font-size: 13px;")
        layout.addWidget(lbl_msg)

        # Input widget: ComboBox if choices available, else SpinBox / LineEdit
        if available_choices and len(available_choices) > 0 and not is_two_values:
            self.combo = QComboBox()
            self.combo.setEditable(True)
            for c in available_choices:
                self.combo.addItem(str(c))
            if str(default_val) in [str(c) for c in available_choices]:
                self.combo.setCurrentText(str(default_val))
            layout.addWidget(self.combo)
            self.input_widget = self.combo
        elif is_two_values:
            self.txt_input = QLineEdit()
            self.txt_input.setPlaceholderText("Ví dụ: 20, 80")
            self.txt_input.setText("20, 80")
            layout.addWidget(self.txt_input)
            self.input_widget = self.txt_input
        else:
            self.spin = QSpinBox()
            self.spin.setRange(0, 999)
            self.spin.setValue(int(default_val) if isinstance(default_val, (int, float)) else 25)
            layout.addWidget(self.spin)
            self.input_widget = self.spin

        layout.addStretch()

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        btn_cancel = QPushButton("Hủy Bỏ")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        btn_ok = QPushButton("Xác Nhận & Mô Phỏng ➔")
        btn_ok.setObjectName("btn_primary")
        btn_ok.setStyleSheet("""
            QPushButton {
                background-color: #0284c7;
                color: #ffffff;
                font-weight: bold;
                padding: 8px 18px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #0ea5e9;
            }
        """)
        btn_ok.clicked.connect(self._on_confirm)
        btn_layout.addWidget(btn_ok)

        layout.addLayout(btn_layout)

    def _on_confirm(self):
        if hasattr(self, 'combo'):
            try:
                self.result_value = int(self.combo.currentText().strip())
            except ValueError:
                self.result_value = 25
        elif hasattr(self, 'spin'):
            self.result_value = self.spin.value()
        elif hasattr(self, 'txt_input'):
            raw = self.txt_input.text().replace(',', ' ').split()
            try:
                if len(raw) >= 2:
                    self.result_value = (int(raw[0]), int(raw[1]))
                elif len(raw) == 1:
                    self.result_value = (int(raw[0]), int(raw[0]))
                else:
                    self.result_value = (20, 80)
            except ValueError:
                self.result_value = (20, 80)

        self.accept()
