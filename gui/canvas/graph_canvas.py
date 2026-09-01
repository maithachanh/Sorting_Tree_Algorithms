"""
Graph Canvas Widget for MST (Kruskal, Prim) and Graph Tree Algorithms.
Renders all edges, MST edges (green), current candidate edge (amber), and visited nodes.
"""
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QRadialGradient
from PyQt5.QtCore import Qt, QPointF, QRectF
import math

# Default graph layout for Kruskal / Prim (6 nodes)
KRUSKAL_EDGES = [
    (0, 1, 4), (0, 2, 4), (1, 2, 2), (2, 3, 3),
    (2, 5, 2), (2, 4, 4), (3, 4, 3), (5, 4, 3)
]

# Prim uses 5 nodes — deduplicate edge set for display
PRIM_EDGES = [
    (0, 1, 2), (0, 3, 6), (1, 2, 3), (1, 3, 8),
    (1, 4, 5), (2, 4, 7), (3, 4, 9)
]


class GraphCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.edges       = []      # All edges (u, v, w)
        self.mst_edges   = []      # Accepted MST edges
        self.current_edge = None   # Currently evaluated edge
        self.visited_nodes = set() # Visited nodes (Prim)
        self.message     = ""
        self.num_nodes   = 6
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: #0b1120; border-radius: 10px;")

    def update_state(self, step_state):
        if not step_state:
            return
        extra = step_state.extra_info or {}
        self.edges        = extra.get("edges", [])
        self.mst_edges    = extra.get("mst", [])
        self.current_edge = extra.get("current_edge", None)
        self.visited_nodes= set(extra.get("visited", []))
        self.message      = step_state.message

        # Auto-detect num_nodes from edges
        all_nodes = set()
        for e in self.edges:
            all_nodes.add(e[0]); all_nodes.add(e[1])
        if all_nodes:
            self.num_nodes = max(all_nodes) + 1

        # Fallback defaults when edges are missing
        if not self.edges:
            if "kruskal" in self.message.lower() or len(self.mst_edges) > 0 and self.num_nodes >= 6:
                self.edges = KRUSKAL_EDGES
                self.num_nodes = 6
            else:
                self.edges = PRIM_EDGES
                self.num_nodes = 5

        self.update()

    # ──────────────────────────────────────────
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        try:
            painter.fillRect(self.rect(), QColor("#0b1120"))
            self._draw_graph(painter)
        finally:
            painter.end()

    def _get_node_positions(self):
        w = self.width()
        h = self.height()
        cx, cy = w / 2, h / 2
        r_layout = min(w, h) * 0.33
        n = self.num_nodes
        positions = {}
        for i in range(n):
            angle = 2 * math.pi * i / n - math.pi / 2
            positions[i] = (cx + r_layout * math.cos(angle),
                            cy + r_layout * math.sin(angle))
        return positions

    def _is_mst_edge(self, u, v):
        return any(
            min(u, v) == min(mu, mv) and max(u, v) == max(mu, mv)
            for mu, mv, _ in self.mst_edges
        )

    def _is_current_edge(self, u, v):
        if not self.current_edge:
            return False
        cu, cv = self.current_edge[0], self.current_edge[1]
        return min(u, v) == min(cu, cv) and max(u, v) == max(cu, cv)

    def _draw_graph(self, painter):
        node_pos = self._get_node_positions()
        node_r   = 22.0

        # 1. Draw edges
        seen = set()
        for u, v, weight in self.edges:
            key = (min(u, v), max(u, v))
            if key in seen:
                continue
            seen.add(key)
            if u not in node_pos or v not in node_pos:
                continue
            x1, y1 = node_pos[u]
            x2, y2 = node_pos[v]

            in_mst   = self._is_mst_edge(u, v)
            is_curr  = self._is_current_edge(u, v)

            if in_mst:
                pen = QPen(QColor("#10b981"), 3.8)  # Emerald green — MST
            elif is_curr:
                pen = QPen(QColor("#f59e0b"), 3.2)  # Amber — current candidate
            else:
                pen = QPen(QColor("#1e3a5f"), 2.0)  # Dark blue — default

            painter.setPen(pen)
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

            # Weight label
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            offset_x = (y2 - y1) * 0.07
            offset_y = (x1 - x2) * 0.07
            w_rect = QRectF(mx + offset_x - 12, my + offset_y - 10, 24, 18)
            weight_col = QColor("#fbbf24") if in_mst else (
                QColor("#f59e0b") if is_curr else QColor("#64748b"))
            painter.setPen(weight_col)
            painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
            painter.drawText(w_rect, Qt.AlignCenter, str(weight))

        # 2. Draw nodes
        for i, (nx, ny) in node_pos.items():
            is_visited = i in self.visited_nodes
            in_mst_node = any(i == u or i == v for u, v, _ in self.mst_edges)

            if in_mst_node:
                col_c, col_e = QColor("#10b981"), QColor("#064e3b")
            elif is_visited:
                col_c, col_e = QColor("#38bdf8"), QColor("#0c4a6e")
            else:
                col_c, col_e = QColor("#1d4ed8"), QColor("#1e3a5f")

            # Glow for MST nodes
            if in_mst_node:
                glow = QColor("#10b981")
                glow.setAlpha(50)
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(glow))
                painter.drawEllipse(QPointF(nx, ny), node_r * 1.5, node_r * 1.5)

            grad = QRadialGradient(nx - node_r / 3, ny - node_r / 3, node_r * 1.2)
            grad.setColorAt(0.0, col_c)
            grad.setColorAt(1.0, col_e)

            border = QColor("#10b981") if in_mst_node else QColor("#38bdf8")
            painter.setPen(QPen(border, 2.2))
            painter.setBrush(QBrush(grad))
            painter.drawEllipse(QPointF(nx, ny), node_r, node_r)

            painter.setPen(QColor("#ffffff"))
            painter.setFont(QFont("Segoe UI", 11, QFont.Bold))
            painter.drawText(
                QRectF(nx - node_r, ny - node_r, node_r * 2, node_r * 2),
                Qt.AlignCenter, str(i))

        # 3. Legend
        self._draw_legend(painter)

    def _draw_legend(self, painter):
        """Draws a compact legend in the top-left corner."""
        items = [
            (QColor("#334155"), "Cạnh thường"),
            (QColor("#f59e0b"), "Đang xét"),
            (QColor("#10b981"), "Cạnh MST"),
        ]
        x, y = 12, 12
        painter.setFont(QFont("Segoe UI", 9))
        for col, label in items:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(col))
            painter.drawRoundedRect(QRectF(x, y, 16, 8), 2, 2)
            painter.setPen(QColor("#94a3b8"))
            painter.drawText(QRectF(x + 20, y - 2, 90, 14), Qt.AlignVCenter, label)
            y += 18
