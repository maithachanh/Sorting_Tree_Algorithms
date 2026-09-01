"""
Log and Step Explanation Panel.
Displays human-readable algorithm decisions, statistics, and traversal order.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QFrame, QScrollArea)
from PyQt5.QtCore import Qt
from Algorithms.step_state import ActionType

ACTION_MAP = {
    ActionType.COMPARE:        ("SO SÁNH",      "#f59e0b", "#0f172a"),
    ActionType.SWAP:           ("HOÁN ĐỔI",     "#ef4444", "#ffffff"),
    ActionType.OVERWRITE:      ("GHI ĐÈ",       "#ec4899", "#ffffff"),
    ActionType.PIVOT:          ("CHỐT PIVOT",   "#a855f7", "#ffffff"),
    ActionType.SORTED:         ("ĐÃ SẮP XẾP",  "#10b981", "#ffffff"),
    ActionType.SUBARRAY:       ("ĐOẠN CON",     "#06b6d4", "#0f172a"),
    ActionType.MARK:           ("ĐÁNH DẤU",     "#34d399", "#0f172a"),
    ActionType.VISIT_NODE:     ("THĂM NÚT",     "#f59e0b", "#0f172a"),
    ActionType.HIGHLIGHT_EDGE: ("DUYỆT NHÁNH",  "#38bdf8", "#0f172a"),
    ActionType.INSERT_NODE:    ("CHÈN NÚT",     "#10b981", "#ffffff"),
    ActionType.DELETE_NODE:    ("XÓA NÚT",      "#ef4444", "#ffffff"),
    ActionType.ROTATE:         ("XOAY CÂY",     "#f97316", "#ffffff"),
    ActionType.RECOLOR:        ("ĐỔI MÀU",      "#8b5cf6", "#ffffff"),
    ActionType.HEAPIFY:        ("VUN ĐỐNG",     "#8b5cf6", "#ffffff"),
    ActionType.EXTRACT:        ("TRÍCH XUẤT",   "#e11d48", "#ffffff"),
    ActionType.MST_EDGE:       ("CẠNH MST",     "#10b981", "#ffffff"),
    ActionType.BUILD_TREE:     ("XÂY CÂY",      "#06b6d4", "#0f172a"),
    ActionType.UPDATE_TREE:    ("CẬP NHẬT",     "#0ea5e9", "#0f172a"),
    ActionType.FINISH:         ("✅ HOÀN TẤT",  "#10b981", "#ffffff"),
    ActionType.INFO:           ("THÔNG TIN",    "#38bdf8", "#0f172a"),
}


class LogPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # ── Stats row ──────────────────────────────────────
        stats_row = QHBoxLayout()
        stats_row.setSpacing(10)

        self.badge_action = QLabel("SẴN SÀNG")
        self.badge_action.setStyleSheet("""
            background-color: #38bdf8;
            color: #0f172a;
            font-weight: bold;
            font-size: 11px;
            padding: 4px 10px;
            border-radius: 5px;
        """)
        stats_row.addWidget(self.badge_action)

        self.stats_compare = QLabel("So sánh: 0")
        self.stats_compare.setStyleSheet("color: #f59e0b; font-weight: 600; font-size: 12px;")
        stats_row.addWidget(self.stats_compare)

        self.stats_swaps = QLabel("Hoán đổi: 0")
        self.stats_swaps.setStyleSheet("color: #ef4444; font-weight: 600; font-size: 12px;")
        stats_row.addWidget(self.stats_swaps)

        stats_row.addStretch()

        # Traversal order badge (hidden by default)
        self.traversal_badge = QLabel("")
        self.traversal_badge.setWordWrap(False)
        self.traversal_badge.setStyleSheet("""
            color: #34d399;
            font-size: 11px;
            font-weight: 600;
        """)
        self.traversal_badge.setVisible(False)
        stats_row.addWidget(self.traversal_badge)

        layout.addLayout(stats_row)

        # ── Message Box ────────────────────────────────────
        self.msg_box = QFrame()
        self.msg_box.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
            }
        """)
        box_layout = QVBoxLayout(self.msg_box)
        box_layout.setContentsMargins(12, 8, 12, 8)
        box_layout.setSpacing(4)

        self.lbl_message = QLabel("Sẵn sàng bắt đầu mô phỏng thuật toán.")
        self.lbl_message.setWordWrap(True)
        self.lbl_message.setStyleSheet(
            "color: #f8fafc; font-size: 13px; line-height: 1.5; background: transparent;")
        box_layout.addWidget(self.lbl_message)

        # Extra traversal sequence display
        self.lbl_traversal = QLabel("")
        self.lbl_traversal.setWordWrap(True)
        self.lbl_traversal.setVisible(False)
        self.lbl_traversal.setStyleSheet(
            "color: #34d399; font-size: 12px; font-family: Consolas; background: transparent;")
        box_layout.addWidget(self.lbl_traversal)

        # Extra BF / rotation info display
        self.lbl_extra = QLabel("")
        self.lbl_extra.setVisible(False)
        self.lbl_extra.setStyleSheet(
            "color: #fbbf24; font-size: 11px; background: transparent;")
        box_layout.addWidget(self.lbl_extra)

        layout.addWidget(self.msg_box)

    def update_log(self, step_state):
        if not step_state:
            return

        # ── Action badge ──────────────────────────────────
        badge_text, bg_color, fg_color = ACTION_MAP.get(
            step_state.action_type, ("THÔNG BÁO", "#38bdf8", "#0f172a"))
        self.badge_action.setText(badge_text)
        self.badge_action.setStyleSheet(f"""
            background-color: {bg_color};
            color: {fg_color};
            font-weight: bold;
            font-size: 11px;
            padding: 4px 10px;
            border-radius: 5px;
        """)

        # ── Message ───────────────────────────────────────
        self.lbl_message.setText(step_state.message)

        # ── Counters ──────────────────────────────────────
        self.stats_compare.setText(f"So sánh: {step_state.comparisons}")
        self.stats_swaps.setText(f"Hoán đổi: {step_state.swaps}")

        extra = step_state.extra_info or {}

        # ── Traversal order sequence ──────────────────────
        traversed = extra.get("traversed")
        if traversed is not None and len(traversed) > 0:
            seq_text = " → ".join(str(v) for v in traversed)
            self.lbl_traversal.setText(f"Thứ tự duyệt: {seq_text}")
            self.lbl_traversal.setVisible(True)
            self.traversal_badge.setText(f"📋 {len(traversed)} nút đã duyệt")
            self.traversal_badge.setVisible(True)
        else:
            self.lbl_traversal.setVisible(False)
            self.traversal_badge.setVisible(False)

        # ── BIT array display ─────────────────────────────
        bit_arr = extra.get("bit_array")
        if bit_arr is not None:
            self.lbl_extra.setText(f"BIT[]: {bit_arr}")
            self.lbl_extra.setVisible(True)
        else:
            self.lbl_extra.setVisible(False)

        # Change msg_box border color based on action type
        color_border = bg_color if bg_color != "#38bdf8" else "#334155"
        self.msg_box.setStyleSheet(f"""
            QFrame {{
                background-color: #1e293b;
                border: 1px solid {color_border};
                border-radius: 8px;
            }}
        """)
