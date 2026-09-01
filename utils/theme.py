"""
Modern Theme, Colors and QSS Stylesheet for the Visualizer Application.
"""

# Color Palette (Hex)
COLOR_BG_DARK = "#0f172a"          # Very dark slate
COLOR_BG_CARD = "#1e293b"          # Dark slate container
COLOR_BG_CARD_HOVER = "#334155"    # Card hover
COLOR_BG_LIGHTER = "#334155"       # Sub container
COLOR_ACCENT = "#38bdf8"           # Cyan accent
COLOR_ACCENT_HOVER = "#0ea5e9"
COLOR_TEXT_PRIMARY = "#f8fafc"     # Crisp White
COLOR_TEXT_MUTED = "#94a3b8"       # Gray text
COLOR_BORDER = "#475569"           # Border color

# Sorting Animation Colors
SORT_COLOR_DEFAULT = "#38bdf8"     # Sky Blue
SORT_COLOR_COMPARE = "#f59e0b"     # Amber / Yellow
SORT_COLOR_SWAP = "#ef4444"        # Red
SORT_COLOR_PIVOT = "#c084fc"       # Purple
SORT_COLOR_SORTED = "#10b981"      # Emerald Green
SORT_COLOR_SUBARRAY = "#06b6d4"    # Cyan
SORT_COLOR_AUX = "#64748b"         # Slate (for temporary buckets/arrays)

# Tree Animation Colors
TREE_NODE_DEFAULT = "#38bdf8"      # Blue
TREE_NODE_VISIT = "#f59e0b"        # Yellow
TREE_NODE_FOUND = "#10b981"        # Green
TREE_NODE_DELETE = "#ef4444"       # Red
TREE_NODE_PIVOT = "#c084fc"        # Purple
TREE_NODE_BALANCING = "#fb923c"    # Orange
TREE_EDGE_DEFAULT = "#64748b"      # Muted Gray
TREE_EDGE_ACTIVE = "#f59e0b"       # Active Yellow
TREE_EDGE_MST = "#10b981"          # MST Green

# Red-Black Tree Specific
RB_RED = "#ef4444"
RB_BLACK = "#1e293b"

# Main Modern Dark QSS
DARK_STYLESHEET = """
QMainWindow {
    background-color: #0f172a;
}

QWidget {
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    color: #f8fafc;
    background-color: transparent;
}

/* ScrollBars */
QScrollBar:vertical {
    border: none;
    background: #0f172a;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #334155;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #475569;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: #0f172a;
    height: 10px;
    margin: 0px;
}
QScrollBar::handle:horizontal {
    background: #334155;
    min-width: 20px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal:hover {
    background: #475569;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Push Buttons */
QPushButton {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #334155;
    border-color: #38bdf8;
    color: #38bdf8;
}
QPushButton:pressed {
    background-color: #0ea5e9;
    color: #0f172a;
    border-color: #0ea5e9;
}
QPushButton:disabled {
    background-color: #1e293b;
    color: #64748b;
    border-color: #1e293b;
}

/* Primary Action Button */
QPushButton#btn_primary {
    background-color: #0284c7;
    color: #ffffff;
    border: none;
}
QPushButton#btn_primary:hover {
    background-color: #0ea5e9;
}
QPushButton#btn_primary:pressed {
    background-color: #38bdf8;
    color: #0f172a;
}

/* Danger / Stop Button */
QPushButton#btn_danger {
    background-color: #991b1b;
    color: #ffffff;
    border: none;
}
QPushButton#btn_danger:hover {
    background-color: #dc2626;
}

/* Success Button */
QPushButton#btn_success {
    background-color: #065f46;
    color: #ffffff;
    border: none;
}
QPushButton#btn_success:hover {
    background-color: #059669;
}

/* LineEdit & SpinBox */
QLineEdit, QSpinBox, QComboBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 6px 12px;
    color: #f8fafc;
    font-size: 13px;
    selection-background-color: #0284c7;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid #38bdf8;
    background-color: #1e293b;
}

/* Slider */
QSlider::groove:horizontal {
    height: 6px;
    background: #334155;
    border-radius: 3px;
}
QSlider::sub-page:horizontal {
    background: #38bdf8;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #f8fafc;
    border: 2px solid #38bdf8;
    width: 16px;
    margin-top: -5px;
    margin-bottom: -5px;
    border-radius: 8px;
}
QSlider::handle:horizontal:hover {
    background: #38bdf8;
}

/* Tooltips */
QToolTip {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #38bdf8;
    padding: 6px;
    border-radius: 4px;
    font-size: 12px;
}

/* GroupBox / Panels */
QGroupBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    margin-top: 18px;
    padding: 15px;
    font-weight: bold;
    font-size: 14px;
    color: #38bdf8;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 10px;
    left: 15px;
}
"""
