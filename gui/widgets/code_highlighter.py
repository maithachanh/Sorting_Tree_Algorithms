"""
Code Viewer Widget with Line-by-Line Execution Highlighting.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt5.QtGui import QFont, QTextCursor, QTextCharFormat, QColor, QSyntaxHighlighter
from PyQt5.QtCore import Qt, QRegExp

class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """Simple and elegant Python syntax highlighter."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Keyword format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#38bdf8")) # Cyan
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            r"\bdef\b", r"\bclass\b", r"\breturn\b", r"\bif\b", r"\belif\b",
            r"\belse\b", r"\bwhile\b", r"\bfor\b", r"\bin\b", r"\band\b",
            r"\bor\b", r"\bnot\b", r"\byield\b", r"\bfrom\b", r"\bimport\b",
            r"\bNone\b", r"\bTrue\b", r"\bFalse\b", r"\bbreak\b", r"\bcontinue\b"
        ]
        for kw in keywords:
            self.highlighting_rules.append((QRegExp(kw), keyword_format))

        # Function format
        func_format = QTextCharFormat()
        func_format.setForeground(QColor("#a855f7")) # Purple
        self.highlighting_rules.append((QRegExp(r"\b[A-Za-z0-9_]+(?=\()"), func_format))

        # Numbers format
        num_format = QTextCharFormat()
        num_format.setForeground(QColor("#f59e0b")) # Amber
        self.highlighting_rules.append((QRegExp(r"\b[0-9]+\b"), num_format))

        # Comments format
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#64748b")) # Slate
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegExp(r"#[^\n]*"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)


class CodeViewerWidget(QWidget):
    """
    Displays the algorithm code and highlights the currently executing line.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.raw_lines = []
        self.active_line = 1

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Header Label
        self.header_label = QLabel("💻 Mã Nguồn Thuật Toán (Mô Phỏng Trực Tiếp)")
        self.header_label.setStyleSheet("font-weight: bold; color: #38bdf8; font-size: 13px; padding-bottom: 2px;")
        layout.addWidget(self.header_label)

        # Text Edit
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("Consolas", 11))
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #0b1120;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px;
                color: #e2e8f0;
                line-height: 1.5;
            }
        """)
        layout.addWidget(self.text_edit)

        self.highlighter = PythonSyntaxHighlighter(self.text_edit.document())

    def set_code(self, code_str):
        """Loads new code string into the viewer."""
        self.raw_lines = code_str.strip().split('\n')
        self._render_code(1)

    def highlight_line(self, line_num):
        """Highlights the active line (1-indexed)."""
        self.active_line = line_num
        self._render_code(line_num)

    def _render_code(self, active_line):
        """Renders code with custom line numbers and active line highlighting."""
        html_lines = []
        for idx, line in enumerate(self.raw_lines, start=1):
            is_active = (idx == active_line)
            line_no_str = f"{idx:>2}"
            # Escape HTML characters
            escaped = (
                line.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace(" ", "&nbsp;")
            )

            if is_active:
                # Active line background with bright indicator
                html_lines.append(
                    f"<div style='background-color: rgba(56, 189, 248, 0.25); border-left: 4px solid #38bdf8; padding: 2px 4px; font-weight: bold;'>"
                    f"<span style='color: #38bdf8;'>▶ {line_no_str} | </span>"
                    f"<span style='color: #ffffff;'>{escaped}</span>"
                    f"</div>"
                )
            else:
                html_lines.append(
                    f"<div style='padding: 2px 4px;'>"
                    f"<span style='color: #475569;'>&nbsp;&nbsp;{line_no_str} | </span>"
                    f"<span style='color: #cbd5e1;'>{escaped}</span>"
                    f"</div>"
                )

        full_html = f"<div style='font-family: Consolas, monospace; font-size: 13px; line-height: 1.4;'>{''.join(html_lines)}</div>"
        self.text_edit.setHtml(full_html)

        # Scroll to ensure active line is visible
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        for _ in range(active_line - 1):
            cursor.movePosition(QTextCursor.Down)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()
