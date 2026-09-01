"""
Playback Control Bar with Play, Pause, Step Next/Prev, Step Slider and Speed Slider.
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from config import SPEED_DEFAULT, SPEED_MIN, SPEED_MAX

class PlaybackControlBar(QWidget):
    play_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    step_forward_clicked = pyqtSignal()
    step_backward_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()
    step_slider_moved = pyqtSignal(int)
    speed_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(8)

        # Timeline Slider Row
        slider_row = QHBoxLayout()
        slider_row.setSpacing(12)

        self.step_label = QLabel("Bước: 0 / 0")
        self.step_label.setStyleSheet("color: #38bdf8; font-weight: bold; min-width: 100px;")
        slider_row.addWidget(self.step_label)

        self.step_slider = QSlider(Qt.Horizontal)
        self.step_slider.setRange(0, 0)
        self.step_slider.setValue(0)
        self.step_slider.sliderMoved.connect(self._on_step_slider_moved)
        slider_row.addWidget(self.step_slider)

        main_layout.addLayout(slider_row)

        # Buttons and Speed Controls Row
        control_row = QHBoxLayout()
        control_row.setSpacing(10)

        # Reset button
        self.btn_reset = QPushButton("🔄 Đặt Lại")
        self.btn_reset.clicked.connect(self.reset_clicked.emit)
        control_row.addWidget(self.btn_reset)

        # Step Back button
        self.btn_prev = QPushButton("⏮ Lùi Bước")
        self.btn_prev.clicked.connect(self.step_backward_clicked.emit)
        control_row.addWidget(self.btn_prev)

        # Play/Pause toggle button
        self.btn_play = QPushButton("▶ Bắt Đầu")
        self.btn_play.setObjectName("btn_primary")
        self.btn_play.setStyleSheet("min-width: 110px; font-weight: bold;")
        self.btn_play.clicked.connect(self._on_play_toggle)
        control_row.addWidget(self.btn_play)

        # Step Next button
        self.btn_next = QPushButton("Tiếp Bước ⏭")
        self.btn_next.clicked.connect(self.step_forward_clicked.emit)
        control_row.addWidget(self.btn_next)

        control_row.addStretch()

        # Speed Slider
        lbl_speed = QLabel("⏱ Tốc Độ:")
        lbl_speed.setStyleSheet("color: #94a3b8; font-weight: 500;")
        control_row.addWidget(lbl_speed)

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(SPEED_MIN, SPEED_MAX)
        # Invert speed visually: left = slow, right = fast
        self.speed_slider.setValue(SPEED_MAX - SPEED_DEFAULT + SPEED_MIN)
        self.speed_slider.setFixedWidth(140)
        self.speed_slider.valueChanged.connect(self._on_speed_slider_changed)
        control_row.addWidget(self.speed_slider)

        self.speed_val_label = QLabel("Vừa")
        self.speed_val_label.setStyleSheet("color: #38bdf8; min-width: 45px;")
        control_row.addWidget(self.speed_val_label)

        main_layout.addLayout(control_row)

        self.is_playing = False

    def update_step(self, current_idx, total_steps):
        """Updates the slider position and step text."""
        self.step_slider.blockSignals(True)
        self.step_slider.setRange(0, max(0, total_steps - 1))
        self.step_slider.setValue(current_idx)
        self.step_slider.blockSignals(False)

        total_display = max(1, total_steps)
        self.step_label.setText(f"Bước: {current_idx + 1} / {total_display}")

    def set_playing_state(self, is_playing):
        self.is_playing = is_playing
        if is_playing:
            self.btn_play.setText("⏸ Tạm Dừng")
            self.btn_play.setStyleSheet("background-color: #f59e0b; color: #0f172a; min-width: 110px; font-weight: bold;")
        else:
            self.btn_play.setText("▶ Tiếp Tục")
            self.btn_play.setObjectName("btn_primary")
            self.btn_play.setStyleSheet("background-color: #0284c7; color: #ffffff; min-width: 110px; font-weight: bold;")

    def _on_play_toggle(self):
        if self.is_playing:
            self.pause_clicked.emit()
        else:
            self.play_clicked.emit()

    def _on_step_slider_moved(self, val):
        self.step_slider_moved.emit(val)

    def _on_speed_slider_changed(self, slider_val):
        # Invert so right is faster (smaller ms)
        delay_ms = SPEED_MAX - slider_val + SPEED_MIN
        if delay_ms < 100:
            self.speed_val_label.setText("Rất nhanh")
        elif delay_ms < 300:
            self.speed_val_label.setText("Nhanh")
        elif delay_ms < 600:
            self.speed_val_label.setText("Vừa")
        else:
            self.speed_val_label.setText("Chậm")
        self.speed_changed.emit(delay_ms)
