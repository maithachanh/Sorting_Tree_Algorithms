"""
Sorting Canvas Widget rendering beautiful dynamic bar charts with QPainter.
Optimized for dense arrays from N=3 up to N=100 elements.
"""
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QLinearGradient, QBrush
from PyQt5.QtCore import Qt, QRectF
from Algorithms.step_state import ActionType

class SortingCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        self.highlighted_indices = []
        self.action_type = ActionType.INFO
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: #0b1120; border-radius: 10px;")

    def update_state(self, step_state):
        """Updates canvas state from a StepState object."""
        if not step_state:
            return
        if isinstance(step_state.current_data, list):
            self.data = list(step_state.current_data)
        self.highlighted_indices = list(step_state.highlighted_indices)
        self.action_type = step_state.action_type
        self.update()

    def set_data(self, data_list):
        self.data = list(data_list)
        self.highlighted_indices = []
        self.action_type = ActionType.INFO
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        try:
            # Draw dark canvas background
            painter.fillRect(self.rect(), QColor("#0b1120"))

            if not self.data:
                painter.setPen(QColor("#64748b"))
                painter.setFont(QFont("Segoe UI", 14))
                painter.drawText(self.rect(), Qt.AlignCenter, "Chưa có dữ liệu mảng để hiển thị.")
                return

            n = len(self.data)
            w = self.width()
            h = self.height()

            # Dynamic padding based on size
            padding_x = 20 if n > 60 else 30
            padding_top = 35 if n > 40 else 40
            padding_bottom = 20 if n > 40 else 35

            usable_w = max(10, w - 2 * padding_x)
            usable_h = max(10, h - padding_top - padding_bottom)

            max_val = max(self.data) if self.data and max(self.data) > 0 else 1

            # Dynamic spacing: tighter for larger N
            if n > 80:
                bar_spacing = 1
            elif n > 50:
                bar_spacing = 2
            elif n > 25:
                bar_spacing = 3
            else:
                bar_spacing = max(3, min(8, int(usable_w / (n * 5))))

            total_spacing = bar_spacing * (n - 1)
            bar_width = max(2.0, (usable_w - total_spacing) / n)

            # Determine font size based on bar width
            show_numbers = (bar_width >= 16)
            show_indices = (bar_width >= 20)

            font_size_val = max(7, min(12, int(bar_width * 0.45)))
            font_val = QFont("Segoe UI", font_size_val, QFont.Bold)
            font_idx = QFont("Segoe UI", max(6, min(10, int(bar_width * 0.35))))

            for i, val in enumerate(self.data):
                bar_h = max(4.0, (val / max_val) * usable_h)
                x = padding_x + i * (bar_width + bar_spacing)
                y = h - padding_bottom - bar_h

                rect = QRectF(x, y, bar_width, bar_h)

                # Determine bar color based on action & highlight
                is_highlighted = (i in self.highlighted_indices)

                if self.action_type == ActionType.FINISH:
                    col_top, col_bot = QColor("#34d399"), QColor("#059669") # Emerald Green
                elif is_highlighted:
                    if self.action_type == ActionType.COMPARE:
                        col_top, col_bot = QColor("#fbbf24"), QColor("#d97706") # Amber
                    elif self.action_type in (ActionType.SWAP, ActionType.OVERWRITE):
                        col_top, col_bot = QColor("#f87171"), QColor("#dc2626") # Red
                    elif self.action_type == ActionType.PIVOT:
                        col_top, col_bot = QColor("#c084fc"), QColor("#7e22ce") # Purple
                    elif self.action_type == ActionType.SORTED:
                        col_top, col_bot = QColor("#34d399"), QColor("#059669") # Green
                    elif self.action_type == ActionType.SUBARRAY:
                        col_top, col_bot = QColor("#22d3ee"), QColor("#0891b2") # Cyan
                    else:
                        col_top, col_bot = QColor("#38bdf8"), QColor("#0284c7")
                else:
                    col_top, col_bot = QColor("#38bdf8"), QColor("#0284c7") # Default Sky Blue

                # Create smooth linear gradient
                gradient = QLinearGradient(x, y, x, y + bar_h)
                gradient.setColorAt(0.0, col_top)
                gradient.setColorAt(1.0, col_bot)

                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(gradient))
                # Draw rounded bar on top
                radius = min(3.0, bar_width / 3) if bar_width >= 4 else 0
                painter.drawRoundedRect(rect, radius, radius)

                # Draw Value on top of bar (if bar wide enough)
                if show_numbers:
                    painter.setPen(QColor("#f8fafc"))
                    painter.setFont(font_val)
                    val_rect = QRectF(x - 5, y - 20, bar_width + 10, 18)
                    painter.drawText(val_rect, Qt.AlignCenter, str(val))

                # Draw Index below the bar
                if show_indices:
                    painter.setPen(QColor("#64748b"))
                    painter.setFont(font_idx)
                    idx_rect = QRectF(x - 5, h - padding_bottom + 4, bar_width + 10, 18)
                    painter.drawText(idx_rect, Qt.AlignCenter, str(i))
        finally:
            painter.end()
