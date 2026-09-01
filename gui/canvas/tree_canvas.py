"""
Tree Canvas Widget — renders 2D hierarchical tree structures with QPainter.
Supports: BinaryNode (BST/AVL/RB/Splay), SegmentTreeNode, TrieNode, BTreeNode, and Fenwick BIT arrays.
"""
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import (QPainter, QColor, QFont, QPen,
                          QRadialGradient, QBrush, QLinearGradient)
from PyQt5.QtCore import Qt, QPointF, QRectF
from Algorithms.step_state import ActionType
from Algorithms.Tree.tree_models import BinaryNode, BTreeNode, TrieNode, SegmentTreeNode
from utils.tree_layout import TreeLayoutCalculator


class TreeCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.root_node = None
        self.highlighted_ids = []
        self.action_type = ActionType.INFO
        self.extra_info = {}
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: #0b1120; border-radius: 10px;")

    def update_state(self, step_state):
        if not step_state:
            return
        self.root_node = step_state.current_data
        self.highlighted_ids = list(step_state.highlighted_indices)
        self.action_type = step_state.action_type
        self.extra_info = step_state.extra_info or {}
        self.update()

    def set_tree(self, root):
        self.root_node = root
        self.highlighted_ids = []
        self.action_type = ActionType.INFO
        self.extra_info = {}
        self.update()

    # ──────────────────────────────────────────────
    # Paint Dispatcher
    # ──────────────────────────────────────────────
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        try:
            painter.fillRect(self.rect(), QColor("#0b1120"))

            # Fenwick BIT array (no tree root — special display)
            if self.root_node is None and "bit_array" in self.extra_info:
                self._draw_fenwick(painter)
                return

            if not self.root_node:
                self._draw_empty(painter)
                return

            w = self.width()
            h = self.height()
            radius = max(18.0, min(24.0, w / 40))

            if isinstance(self.root_node, TrieNode):
                positions = TreeLayoutCalculator.compute_trie_layout(self.root_node, w, h)
                self._draw_trie(painter, self.root_node, positions, radius)

            elif isinstance(self.root_node, SegmentTreeNode):
                positions = TreeLayoutCalculator.compute_binary_tree_layout(self.root_node, w, h, radius)
                self._draw_segment_tree(painter, self.root_node, positions, radius)

            elif isinstance(self.root_node, BTreeNode):
                positions = TreeLayoutCalculator.compute_b_tree_layout(self.root_node, w, h)
                self._draw_b_tree(painter, self.root_node, positions)

            elif isinstance(self.root_node, BinaryNode):
                positions = TreeLayoutCalculator.compute_binary_tree_layout(self.root_node, w, h, radius)
                self._draw_binary_tree(painter, self.root_node, positions, radius)

            else:
                self._draw_empty(painter)

        finally:
            painter.end()

    # ──────────────────────────────────────────────
    # Helper: Empty state
    # ──────────────────────────────────────────────
    def _draw_empty(self, painter):
        painter.setPen(QColor("#64748b"))
        painter.setFont(QFont("Segoe UI", 13))
        painter.drawText(self.rect(), Qt.AlignCenter,
                         "Cây đang rỗng hoặc chưa được khởi tạo.")

    # ──────────────────────────────────────────────
    # Binary Tree (BST / AVL / Red-Black / Splay)
    # ──────────────────────────────────────────────
    def _draw_binary_tree(self, painter, root, positions, radius):
        """Draws edges first, then nodes with gradient fill and optional labels."""

        is_avl = isinstance(root, BinaryNode) and hasattr(root, 'height') and root.height > 1

        def draw_edges(node):
            if not node:
                return
            n_id = node.id if hasattr(node, 'id') else id(node)
            if n_id not in positions:
                return
            x1, y1 = positions[n_id]

            for child in (node.left, node.right):
                if child:
                    c_id = child.id if hasattr(child, 'id') else id(child)
                    if c_id in positions:
                        x2, y2 = positions[c_id]
                        active = (n_id in self.highlighted_ids and c_id in self.highlighted_ids)
                        if active and self.action_type == ActionType.ROTATE:
                            pen = QPen(QColor("#fb923c"), 3.0)
                        elif active:
                            pen = QPen(QColor("#fbbf24"), 2.8)
                        else:
                            pen = QPen(QColor("#334155"), 1.8)
                        painter.setPen(pen)
                        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
                    if child is node.left:
                        draw_edges(node.left)
                    else:
                        draw_edges(node.right)

        draw_edges(root)

        def draw_nodes(node):
            if not node:
                return
            n_id = node.id if hasattr(node, 'id') else id(node)
            if n_id not in positions:
                return
            x, y = positions[n_id]
            is_highlighted = (n_id in self.highlighted_ids)

            # --- Determine fill color ---
            node_color = getattr(node, 'color', None)   # Safe: None if not present
            if node_color == 'RED':
                col_center = QColor("#f87171")
                col_edge   = QColor("#ef4444")
            elif node_color == 'BLACK':
                col_center = QColor("#334155")
                col_edge   = QColor("#0f172a")
            elif is_highlighted:
                if self.action_type == ActionType.ROTATE:
                    col_center, col_edge = QColor("#fb923c"), QColor("#ea580c")  # Orange
                elif self.action_type in (ActionType.VISIT_NODE, ActionType.COMPARE, ActionType.HIGHLIGHT_EDGE):
                    col_center, col_edge = QColor("#fbbf24"), QColor("#d97706")  # Amber
                elif self.action_type in (ActionType.INSERT_NODE, ActionType.MARK, ActionType.FINISH):
                    col_center, col_edge = QColor("#34d399"), QColor("#059669")  # Emerald
                elif self.action_type == ActionType.DELETE_NODE:
                    col_center, col_edge = QColor("#f87171"), QColor("#dc2626")  # Red
                else:
                    col_center, col_edge = QColor("#38bdf8"), QColor("#0284c7")
            else:
                col_center, col_edge = QColor("#1d4ed8"), QColor("#1e3a5f")

            # --- Glow ring for highlighted node ---
            if is_highlighted:
                glow_color = col_center
                glow_color.setAlpha(70)
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(glow_color))
                painter.drawEllipse(QPointF(x, y), radius * 1.55, radius * 1.55)

            # --- Radial gradient sphere ---
            grad = QRadialGradient(x - radius / 3, y - radius / 3, radius * 1.3)
            grad.setColorAt(0.0, col_center)
            grad.setColorAt(1.0, col_edge)

            border_color = QColor("#ffffff") if is_highlighted else QColor("#475569")
            border_width = 2.5 if is_highlighted else 1.2
            painter.setPen(QPen(border_color, border_width))
            painter.setBrush(QBrush(grad))
            painter.drawEllipse(QPointF(x, y), radius, radius)

            # --- Node value label ---
            painter.setPen(QColor("#ffffff"))
            painter.setFont(QFont("Segoe UI", max(8, int(radius * 0.6)), QFont.Bold))
            rect = QRectF(x - radius, y - radius, radius * 2, radius * 2)
            painter.drawText(rect, Qt.AlignCenter, str(node.val))

            # --- AVL Balance Factor label ---
            node_height = getattr(node, 'height', None)
            if node_height is not None and isinstance(node_height, int):
                bf = (getattr(node.left, 'height', 0) if node.left else 0) - \
                     (getattr(node.right, 'height', 0) if node.right else 0)
                bf_text = f"BF={bf:+d}"
                bf_color = QColor("#f87171") if abs(bf) > 1 else (
                    QColor("#fbbf24") if abs(bf) == 1 else QColor("#34d399"))
                painter.setPen(bf_color)
                painter.setFont(QFont("Segoe UI", max(7, int(radius * 0.42))))
                painter.drawText(QRectF(x + radius * 0.6, y - radius * 1.6, 50, 14),
                                 Qt.AlignLeft, bf_text)

            # --- Recurse ---
            draw_nodes(node.left)
            draw_nodes(node.right)

        draw_nodes(root)

    # ──────────────────────────────────────────────
    # Segment Tree
    # ──────────────────────────────────────────────
    def _draw_segment_tree(self, painter, root, positions, radius):
        """Draws segment tree edges then nodes with [L..R]=sum labels."""
        def draw_edges(node):
            if not node:
                return
            n_id = node.id if hasattr(node, 'id') else id(node)
            if n_id not in positions:
                return
            x1, y1 = positions[n_id]
            for child in (node.left, node.right):
                if child:
                    c_id = child.id if hasattr(child, 'id') else id(child)
                    if c_id in positions:
                        x2, y2 = positions[c_id]
                        active = n_id in self.highlighted_ids and c_id in self.highlighted_ids
                        painter.setPen(QPen(QColor("#0891b2" if active else "#334155"),
                                           2.5 if active else 1.5))
                        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
                    draw_edges(child)

        draw_edges(root)

        def draw_nodes(node):
            if not node:
                return
            n_id = node.id if hasattr(node, 'id') else id(node)
            if n_id not in positions:
                return
            x, y = positions[n_id]
            is_highlighted = n_id in self.highlighted_ids

            # Node is a rectangle for segment tree
            col_top = QColor("#0891b2") if is_highlighted else QColor("#0c4a6e")
            col_bot = QColor("#0e7490") if is_highlighted else QColor("#083344")

            rect_w = radius * 2.4
            rect_h = radius * 1.6
            rect = QRectF(x - rect_w / 2, y - rect_h / 2, rect_w, rect_h)

            grad = QLinearGradient(x, y - rect_h / 2, x, y + rect_h / 2)
            grad.setColorAt(0.0, col_top)
            grad.setColorAt(1.0, col_bot)

            border_col = QColor("#38bdf8") if is_highlighted else QColor("#0369a1")
            painter.setPen(QPen(border_col, 2.0 if is_highlighted else 1.2))
            painter.setBrush(QBrush(grad))
            painter.drawRoundedRect(rect, 5, 5)

            # Label: [L..R]\nSum
            seg_label = f"[{node.start}..{node.end}]"
            val_label = f"Σ={node.val}"
            painter.setPen(QColor("#e0f2fe"))
            painter.setFont(QFont("Consolas", max(7, int(radius * 0.45)), QFont.Bold))
            painter.drawText(QRectF(x - rect_w / 2, y - rect_h / 2, rect_w, rect_h / 2 + 2),
                             Qt.AlignCenter, seg_label)
            painter.setPen(QColor("#fbbf24") if is_highlighted else QColor("#7dd3fc"))
            painter.setFont(QFont("Segoe UI", max(7, int(radius * 0.5)), QFont.Bold))
            painter.drawText(QRectF(x - rect_w / 2, y, rect_w, rect_h / 2),
                             Qt.AlignCenter, val_label)

            draw_nodes(node.left)
            draw_nodes(node.right)

        draw_nodes(root)

    # ──────────────────────────────────────────────
    # B-Tree
    # ──────────────────────────────────────────────
    def _draw_b_tree(self, painter, root, positions):
        """Draws B-Tree with key boxes and children connections."""

        def draw_edges(node):
            if not node:
                return
            n_id = node.id if hasattr(node, 'id') else id(node)
            if n_id not in positions:
                return
            x1, y1 = positions[n_id]
            for child in getattr(node, 'children', []):
                c_id = child.id if hasattr(child, 'id') else id(child)
                if c_id in positions:
                    x2, y2 = positions[c_id]
                    painter.setPen(QPen(QColor("#334155"), 1.8))
                    painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
                draw_edges(child)

        def draw_nodes(node):
            if not node:
                return
            n_id = node.id if hasattr(node, 'id') else id(node)
            if n_id not in positions:
                return
            x, y = positions[n_id]
            keys = node.keys if node.keys else []
            is_highlighted = n_id in self.highlighted_ids

            key_w = 36
            key_h = 32
            total_w = max(key_w * len(keys), key_w) + 12
            rect_x = x - total_w / 2

            # Outer rounded box
            outer_rect = QRectF(rect_x - 4, y - key_h / 2 - 4, total_w + 8, key_h + 8)
            painter.setPen(QPen(QColor("#38bdf8" if is_highlighted else "#475569"), 1.8))
            painter.setBrush(QBrush(QColor("#1e3a5f" if is_highlighted else "#1e293b")))
            painter.drawRoundedRect(outer_rect, 6, 6)

            # Individual key cells
            for i, key in enumerate(keys):
                kx = rect_x + i * key_w
                key_rect = QRectF(kx, y - key_h / 2, key_w, key_h)
                painter.setPen(QPen(QColor("#64748b"), 0.8))
                painter.setBrush(QBrush(QColor("#0c4a6e" if is_highlighted else "#1e3a5f")))
                painter.drawRoundedRect(key_rect, 3, 3)
                painter.setPen(QColor("#f8fafc"))
                painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
                painter.drawText(key_rect, Qt.AlignCenter, str(key))

            if not keys:
                painter.setPen(QColor("#475569"))
                painter.setFont(QFont("Segoe UI", 9))
                painter.drawText(outer_rect, Qt.AlignCenter, "(rỗng)")

            for child in getattr(node, 'children', []):
                draw_nodes(child)

        draw_edges(root)
        draw_nodes(root)

    # ──────────────────────────────────────────────
    # Trie
    # ──────────────────────────────────────────────
    def _draw_trie(self, painter, root, positions, radius):
        """Draws Trie prefix tree with character labels on edges."""
        def draw_edges(node):
            if not node:
                return
            n_id = node.id if hasattr(node, 'id') else id(node)
            if n_id not in positions:
                return
            x1, y1 = positions[n_id]
            for ch, child in getattr(node, 'children', {}).items():
                c_id = child.id if hasattr(child, 'id') else id(child)
                if c_id in positions:
                    x2, y2 = positions[c_id]
                    is_active = c_id in self.highlighted_ids
                    painter.setPen(QPen(QColor("#38bdf8" if is_active else "#334155"), 2.0 if is_active else 1.5))
                    painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
                    # Edge character label
                    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                    painter.setPen(QColor("#fbbf24"))
                    painter.setFont(QFont("Consolas", 9, QFont.Bold))
                    painter.drawText(QRectF(mx - 10, my - 14, 20, 16), Qt.AlignCenter, ch)
                draw_edges(child)

        def draw_nodes(node):
            if not node:
                return
            n_id = node.id if hasattr(node, 'id') else id(node)
            if n_id not in positions:
                return
            x, y = positions[n_id]
            is_end  = getattr(node, 'is_end_of_word', False)
            is_high = n_id in self.highlighted_ids
            r = radius * 0.85

            if is_high:
                painter.setPen(Qt.NoPen)
                glow = QColor("#fbbf24")
                glow.setAlpha(60)
                painter.setBrush(QBrush(glow))
                painter.drawEllipse(QPointF(x, y), r * 1.5, r * 1.5)

            col = QColor("#10b981") if is_end else (QColor("#f59e0b") if is_high else QColor("#1d4ed8"))
            painter.setPen(QPen(QColor("#ffffff" if is_high else "#475569"), 1.8))
            painter.setBrush(QBrush(col))
            painter.drawEllipse(QPointF(x, y), r, r)

            painter.setPen(QColor("#ffffff"))
            painter.setFont(QFont("Consolas", max(9, int(r * 0.7)), QFont.Bold))
            char_str = node.char if node.char else "•"
            painter.drawText(QRectF(x - r, y - r, r * 2, r * 2), Qt.AlignCenter, char_str)

            if is_end:
                painter.setPen(QPen(QColor("#10b981"), 2.5))
                painter.setBrush(Qt.NoBrush)
                painter.drawEllipse(QPointF(x, y), r + 4, r + 4)

            for child in getattr(node, 'children', {}).values():
                draw_nodes(child)

        draw_edges(root)
        draw_nodes(root)

    # ──────────────────────────────────────────────
    # Fenwick / BIT Bar Chart
    # ──────────────────────────────────────────────
    def _draw_fenwick(self, painter):
        """Draws Fenwick BIT array as a bar chart with binary index annotations."""
        bit = self.extra_info.get("bit_array", [])
        original = self.extra_info.get("original", [])

        w = self.width()
        h = self.height()
        n = max(len(bit), 1)

        # Title
        painter.setPen(QColor("#38bdf8"))
        painter.setFont(QFont("Segoe UI", 13, QFont.Bold))
        painter.drawText(QRectF(0, 8, w, 30), Qt.AlignCenter,
                         "Cây Fenwick (Binary Indexed Tree — BIT Array)")

        if not bit:
            painter.setPen(QColor("#64748b"))
            painter.drawText(self.rect(), Qt.AlignCenter, "Đang khởi tạo BIT...")
            return

        pad_x = 50
        pad_top = 55
        pad_bot = 60
        usable_w = max(10, w - 2 * pad_x)
        usable_h = max(10, h - pad_top - pad_bot)

        max_val = max(bit) if max(bit) > 0 else 1
        bar_gap = max(4, int(usable_w / (n * 6)))
        bar_w   = max(20.0, (usable_w - bar_gap * (n - 1)) / n)

        for i, val in enumerate(bit):
            bar_h = max(8.0, (val / max_val) * usable_h * 0.85)
            x = pad_x + i * (bar_w + bar_gap)
            y = h - pad_bot - bar_h

            # Gradient bar
            col_top = QColor("#0ea5e9")
            col_bot = QColor("#0c4a6e")
            grad = QLinearGradient(x, y, x, y + bar_h)
            grad.setColorAt(0.0, col_top)
            grad.setColorAt(1.0, col_bot)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(grad))
            painter.drawRoundedRect(QRectF(x, y, bar_w, bar_h), 4, 4)

            # Value label above bar
            painter.setPen(QColor("#e0f2fe"))
            painter.setFont(QFont("Segoe UI", max(7, int(bar_w * 0.38)), QFont.Bold))
            painter.drawText(QRectF(x, y - 20, bar_w, 18), Qt.AlignCenter, str(val))

            # Index below bar
            painter.setPen(QColor("#38bdf8"))
            painter.setFont(QFont("Consolas", max(7, int(bar_w * 0.32))))
            painter.drawText(QRectF(x, h - pad_bot + 4, bar_w, 18),
                             Qt.AlignCenter, f"[{i+1}]")

            # Binary representation
            painter.setPen(QColor("#64748b"))
            painter.setFont(QFont("Consolas", max(6, int(bar_w * 0.28))))
            painter.drawText(QRectF(x, h - pad_bot + 22, bar_w, 16),
                             Qt.AlignCenter, f"{(i+1):04b}")

        # Original array label
        if original:
            painter.setPen(QColor("#94a3b8"))
            painter.setFont(QFont("Segoe UI", 10))
            painter.drawText(QRectF(pad_x, h - 18, w - pad_x * 2, 16),
                             Qt.AlignCenter,
                             f"Mảng gốc: {original}")
