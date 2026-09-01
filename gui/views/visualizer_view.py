"""
Visualizer View: Split-screen visual animation synchronized with line-by-line code highlighting.
Now includes: Complexity Info Panel, interactive prompts for BST/AVL insert/delete/search/LCA.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSplitter, QStackedWidget, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal

from core.animation_controller import AnimationController
from core.session_manager import SessionManager
from Algorithms.code_snippets import CODE_SNIPPETS

# Widgets & Canvas
from gui.widgets.code_highlighter import CodeViewerWidget
from gui.widgets.control_bar import PlaybackControlBar
from gui.widgets.log_panel import LogPanel
from gui.canvas.sorting_canvas import SortingCanvas
from gui.canvas.tree_canvas import TreeCanvas
from gui.canvas.graph_canvas import GraphCanvas
from gui.views.next_action_dialog import NextActionDialog
from gui.widgets.custom_dialogs import ValuePromptDialog

# Sorting algorithms
from Algorithms.Sorting.simple_sorts     import bubble_sort, selection_sort, insertion_sort, interchange_sort
from Algorithms.Sorting.advanced_sorts   import quick_sort, merge_sort, heap_sort, shell_sort, tree_sort
from Algorithms.Sorting.variant_sorts    import shaker_sort, comb_sort, gnome_sort
from Algorithms.Sorting.distribution_sorts import counting_sort, radix_sort, bucket_sort, bead_sort
from Algorithms.Sorting.modern_hybrid_sorts import tim_sort, intro_sort, block_sort
from Algorithms.Sorting.network_sorts   import bitonic_sort
from Algorithms.Sorting.esoteric_sorts  import bogo_sort

# Tree algorithms
from Algorithms.Tree.traversals         import preorder_traversal, inorder_traversal, postorder_traversal, levelorder_traversal
from Algorithms.Tree.bst_operations     import bst_search, bst_insert, bst_delete, bst_successor_predecessor
from Algorithms.Tree.self_balancing     import avl_tree_simulation, avl_insert, avl_delete, red_black_tree_simulation, splay_tree_simulation
from Algorithms.Tree.heap_algorithms    import max_heapify_simulation
from Algorithms.Tree.advanced_trees     import trie_simulation, segment_tree_simulation, fenwick_tree_simulation, b_tree_simulation
from Algorithms.Tree.graph_tree_algorithms import kruskal_mst_simulation, prim_mst_simulation, lca_simulation

# ─── Algorithm Map ───────────────────────────────────────────────────────────
ALGORITHM_MAP = {
    # Sorting
    "bubble_sort": bubble_sort,     "selection_sort": selection_sort,
    "insertion_sort": insertion_sort, "interchange_sort": interchange_sort,
    "shaker_sort": shaker_sort,     "comb_sort": comb_sort,
    "gnome_sort": gnome_sort,       "quick_sort": quick_sort,
    "merge_sort": merge_sort,       "heap_sort": heap_sort,
    "shell_sort": shell_sort,       "tree_sort": tree_sort,
    "counting_sort": counting_sort, "radix_sort": radix_sort,
    "bucket_sort": bucket_sort,     "bead_sort": bead_sort,
    "tim_sort": tim_sort,           "intro_sort": intro_sort,
    "block_sort": block_sort,       "bitonic_sort": bitonic_sort,
    "bogo_sort": bogo_sort,
    # Tree
    "preorder_traversal":   preorder_traversal,
    "inorder_traversal":    inorder_traversal,
    "postorder_traversal":  postorder_traversal,
    "levelorder_traversal": levelorder_traversal,
    "bst_search":    bst_search,
    "bst_insert":    bst_insert,
    "bst_delete":    bst_delete,
    "bst_successor": bst_successor_predecessor,
    "avl_insert":    avl_insert,
    "avl_delete":    avl_delete,
    "avl_tree":      avl_tree_simulation,
    "red_black_tree":   red_black_tree_simulation,
    "splay_tree":       splay_tree_simulation,
    "heap_operations":  max_heapify_simulation,
    "trie_operations":  trie_simulation,
    "segment_tree":     segment_tree_simulation,
    "fenwick_tree":     fenwick_tree_simulation,
    "b_tree":           b_tree_simulation,
    "kruskal_mst":  kruskal_mst_simulation,
    "prim_mst":     prim_mst_simulation,
    "lca_tree":     lca_simulation,
}

# ─── Complexity metadata ──────────────────────────────────────────────────────
COMPLEXITY_INFO = {
    "bubble_sort":          ("O(N²)", "O(N²)", "O(1)"),
    "selection_sort":       ("O(N²)", "O(N²)", "O(1)"),
    "insertion_sort":       ("O(N)", "O(N²)", "O(1)"),
    "interchange_sort":     ("O(N²)", "O(N²)", "O(1)"),
    "shaker_sort":          ("O(N)", "O(N²)", "O(1)"),
    "comb_sort":            ("O(N log N)", "O(N²)", "O(1)"),
    "gnome_sort":           ("O(N)", "O(N²)", "O(1)"),
    "quick_sort":           ("O(N log N)", "O(N²)", "O(log N)"),
    "merge_sort":           ("O(N log N)", "O(N log N)", "O(N)"),
    "heap_sort":            ("O(N log N)", "O(N log N)", "O(1)"),
    "shell_sort":           ("O(N log N)", "O(N^(3/2))", "O(1)"),
    "tree_sort":            ("O(N log N)", "O(N²)", "O(N)"),
    "counting_sort":        ("O(N+K)", "O(N+K)", "O(K)"),
    "radix_sort":           ("O(d·(N+K))", "O(d·(N+K))", "O(N+K)"),
    "bucket_sort":          ("O(N+K)", "O(N²)", "O(N)"),
    "bead_sort":            ("O(N·max)", "O(N·max)", "O(N²)"),
    "tim_sort":             ("O(N)", "O(N log N)", "O(N)"),
    "intro_sort":           ("O(N log N)", "O(N log N)", "O(log N)"),
    "block_sort":           ("O(N log N)", "O(N log N)", "O(1)"),
    "bitonic_sort":         ("O(log² N)", "O(log² N)", "O(N·log² N)"),
    "bogo_sort":            ("O(N)", "O(∞)", "O(1)"),
    # Tree
    "preorder_traversal":   ("O(N)", "O(N)", "O(H)"),
    "inorder_traversal":    ("O(N)", "O(N)", "O(H)"),
    "postorder_traversal":  ("O(N)", "O(N)", "O(H)"),
    "levelorder_traversal": ("O(N)", "O(N)", "O(W)"),
    "bst_search":           ("O(log N)", "O(N)", "O(1)"),
    "bst_insert":           ("O(log N)", "O(N)", "O(1)"),
    "bst_delete":           ("O(log N)", "O(N)", "O(1)"),
    "bst_successor":        ("O(N)", "O(N)", "O(N)"),
    "avl_insert":           ("O(log N)", "O(log N)", "O(log N)"),
    "avl_delete":           ("O(log N)", "O(log N)", "O(log N)"),
    "avl_tree":             ("O(N log N)", "O(N log N)", "O(N)"),
    "red_black_tree":       ("O(log N)", "O(log N)", "O(N)"),
    "splay_tree":           ("O(log N) amortized", "O(N)", "O(N)"),
    "heap_operations":      ("O(log N)", "O(log N)", "O(1)"),
    "trie_operations":      ("O(L)", "O(L)", "O(Σ·N)"),
    "segment_tree":         ("O(N)", "O(log N)", "O(N)"),
    "fenwick_tree":         ("O(N log N)", "O(log N)", "O(N)"),
    "b_tree":               ("O(log N)", "O(log N)", "O(N)"),
    "kruskal_mst":          ("O(E log E)", "O(E log E)", "O(V)"),
    "prim_mst":             ("O(E + V log V)", "O(E + V log V)", "O(V)"),
    "lca_tree":             ("O(H)", "O(H)", "O(1)"),
}


class ComplexityPanel(QFrame):
    """Small info panel showing Best/Worst/Space complexity."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("complexity_panel")
        self.setStyleSheet("""
            QFrame#complexity_panel {
                background-color: #0f172a;
                border: 1px solid #1e3a5f;
                border-radius: 8px;
            }
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(16)

        # Build metrics inline to guarantee attribute availability before addWidget
        self._val_best, w_best   = self._make_metric("⚡ Tốt nhất",   "#34d399")
        self._val_worst, w_worst = self._make_metric("🔴 Tệ nhất",    "#f87171")
        self._val_space, w_space = self._make_metric("💾 Không gian", "#a78bfa")

        layout.addWidget(w_best)

        sep = QLabel("|"); sep.setStyleSheet("color: #334155;")
        layout.addWidget(sep)

        layout.addWidget(w_worst)

        sep2 = QLabel("|"); sep2.setStyleSheet("color: #334155;")
        layout.addWidget(sep2)

        layout.addWidget(w_space)
        layout.addStretch()

    @staticmethod
    def _make_metric(label, color):
        """Returns (value_label, container_widget) for a single metric."""
        w = QWidget()
        vl = QVBoxLayout(w)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(1)

        lbl_title = QLabel(label)
        lbl_title.setStyleSheet("color: #64748b; font-size: 9px;")
        vl.addWidget(lbl_title)

        lbl_val = QLabel("—")
        lbl_val.setStyleSheet(
            f"color: {color}; font-size: 12px; font-weight: bold; font-family: Consolas;")
        vl.addWidget(lbl_val)
        return lbl_val, w

    def update_complexity(self, algo_key):
        info = COMPLEXITY_INFO.get(algo_key, ("—", "—", "—"))
        self._val_best.setText(info[0])
        self._val_worst.setText(info[1])
        self._val_space.setText(info[2])


# ─── Main Visualizer View ────────────────────────────────────────────────────

class VisualizerView(QWidget):
    back_to_algo_select = pyqtSignal()
    request_change_data = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.session    = SessionManager.instance()
        self.controller = AnimationController(self)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(8)

        # ── Top nav bar ───────────────────────────────────────────────────────
        top_bar = QHBoxLayout()
        self.btn_back = QPushButton("⬅ Chọn Giải Thuật Khác")
        self.btn_back.clicked.connect(self._on_back_clicked)
        top_bar.addWidget(self.btn_back)

        self.lbl_category_badge = QLabel("SORTING")
        self.lbl_category_badge.setStyleSheet("""
            background-color: #0284c7; color: #ffffff;
            font-weight: bold; font-size: 11px;
            padding: 3px 10px; border-radius: 5px;
        """)
        top_bar.addWidget(self.lbl_category_badge)

        self.lbl_title = QLabel("Mô Phỏng Thuật Toán")
        self.lbl_title.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #38bdf8; margin-left: 6px;")
        top_bar.addWidget(self.lbl_title)

        top_bar.addStretch()

        btn_new_data = QPushButton("✏️ Đổi Dữ Liệu Mảng")
        btn_new_data.clicked.connect(self.request_change_data.emit)
        top_bar.addWidget(btn_new_data)

        main_layout.addLayout(top_bar)

        # ── Complexity info strip ─────────────────────────────────────────────
        self.complexity_panel = ComplexityPanel()
        main_layout.addWidget(self.complexity_panel)

        # ── Main split view: Canvas (left) | Code + Log (right) ──────────────
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setStyleSheet("""
            QSplitter::handle { background-color: #1e3a5f; width: 4px; border-radius: 2px; }
        """)

        # Left canvas stack
        self.canvas_stack = QStackedWidget()
        self.canvas_stack.setStyleSheet(
            "background-color: #0b1120; border: 1px solid #1e3a5f; border-radius: 10px;")

        self.sorting_canvas = SortingCanvas()
        self.tree_canvas    = TreeCanvas()
        self.graph_canvas   = GraphCanvas()

        self.canvas_stack.addWidget(self.sorting_canvas)  # 0
        self.canvas_stack.addWidget(self.tree_canvas)     # 1
        self.canvas_stack.addWidget(self.graph_canvas)    # 2
        self.splitter.addWidget(self.canvas_stack)

        # Right panel: Code viewer + Log
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: transparent;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(8)

        self.code_viewer = CodeViewerWidget()
        right_layout.addWidget(self.code_viewer, stretch=3)

        self.log_panel = LogPanel()
        right_layout.addWidget(self.log_panel, stretch=1)

        self.splitter.addWidget(right_panel)
        self.splitter.setSizes([760, 500])
        main_layout.addWidget(self.splitter, stretch=1)

        # ── Playback control bar ──────────────────────────────────────────────
        self.controls = PlaybackControlBar()
        main_layout.addWidget(self.controls)

        # ── Wire signals ──────────────────────────────────────────────────────
        self.controller.step_updated.connect(self._on_step_updated)
        self.controller.play_state_changed.connect(self.controls.set_playing_state)
        self.controller.animation_finished.connect(self._on_animation_finished)

        self.controls.play_clicked.connect(self.controller.play)
        self.controls.pause_clicked.connect(self.controller.pause)
        self.controls.step_forward_clicked.connect(self.controller.step_forward)
        self.controls.step_backward_clicked.connect(self.controller.step_backward)
        self.controls.reset_clicked.connect(self.controller.reset)
        self.controls.step_slider_moved.connect(self.controller.jump_to_step)
        self.controls.speed_changed.connect(self.controller.set_speed)

    # ─────────────────────────────────────────────────────────────────────────
    def start_simulation(self):
        """Initializes and starts visualization for current session."""
        self.controller.pause()
        cat  = self.session.current_category
        key  = self.session.current_algorithm_key
        name = self.session.current_algorithm_name

        self.lbl_title.setText(f"  {name}")

        # Complexity panel
        self.complexity_panel.update_complexity(key)

        # Category badge & canvas selection
        if cat == "sorting":
            self._set_badge("SORTING", "#0284c7")
            self.canvas_stack.setCurrentIndex(0)
            data_input = list(self.session.sorting_array)
            extra_args = []
        else:
            self._set_badge("TREE / GRAPH", "#059669")
            if key in ("kruskal_mst", "prim_mst"):
                self.canvas_stack.setCurrentIndex(2)  # Graph canvas
            else:
                self.canvas_stack.setCurrentIndex(1)  # Tree canvas
            data_input = list(self.session.tree_elements)
            extra_args = self._prompt_interactive_args(key, data_input)

        # Code snippet
        snippet = CODE_SNIPPETS.get(key, "# Code snippet đang được cập nhật...")
        self.code_viewer.set_code(snippet)

        # Load generator
        gen_func = ALGORITHM_MAP.get(key, bubble_sort)
        if key in ("kruskal_mst", "prim_mst"):
            self.controller.load_generator(gen_func, 6 if key == "kruskal_mst" else 5)
        elif key == "trie_operations":
            self.controller.load_generator(gen_func, ["cat", "car", "cart", "dog", "dot"])
        else:
            self.controller.load_generator(gen_func, data_input, *extra_args)

    def _set_badge(self, text, color):
        self.lbl_category_badge.setText(text)
        self.lbl_category_badge.setStyleSheet(
            f"background-color: {color}; color: #ffffff; "
            f"font-weight: bold; font-size: 11px; padding: 3px 10px; border-radius: 5px;")

    # ─────────────────────────────────────────────────────────────────────────
    def _prompt_interactive_args(self, key, data_input):
        """Show a dialog prompting the user for a target value."""
        if key == "bst_insert":
            dlg = ValuePromptDialog(
                title="Chèn Phần Tử Vào Cây BST",
                message="Nhập giá trị phần tử mà bạn muốn THÊM vào cây nhị phân tìm kiếm BST:",
                default_val=35,
                parent=self
            )
            return [dlg.result_value] if dlg.exec_() else [35]

        elif key == "bst_delete":
            default_val = data_input[0] if data_input else 50
            dlg = ValuePromptDialog(
                title="Xóa Phần Tử Khỏi Cây BST",
                message="Chọn hoặc nhập giá trị phần tử mà bạn muốn XÓA khỏi cây BST:",
                default_val=default_val,
                available_choices=sorted(data_input),
                parent=self
            )
            return [dlg.result_value] if dlg.exec_() else [default_val]

        elif key == "avl_insert":
            dlg = ValuePromptDialog(
                title="Chèn Phần Tử Vào Cây AVL",
                message="Nhập giá trị phần tử mà bạn muốn THÊM vào Cây tự cân bằng AVL:",
                default_val=15,
                parent=self
            )
            return [dlg.result_value] if dlg.exec_() else [15]

        elif key == "avl_delete":
            default_val = data_input[0] if data_input else 50
            dlg = ValuePromptDialog(
                title="Xóa Phần Tử Khỏi Cây AVL",
                message="Chọn hoặc nhập giá trị phần tử mà bạn muốn XÓA khỏi Cây AVL:",
                default_val=default_val,
                available_choices=sorted(data_input),
                parent=self
            )
            return [dlg.result_value] if dlg.exec_() else [default_val]

        elif key == "bst_search":
            mid = data_input[len(data_input) // 2] if data_input else 40
            dlg = ValuePromptDialog(
                title="Tìm Kiếm Trên BST",
                message="Nhập giá trị phần tử mà bạn muốn TÌM KIẾM trên cây BST:",
                default_val=mid,
                available_choices=sorted(data_input),
                parent=self
            )
            return [dlg.result_value] if dlg.exec_() else [mid]

        elif key == "bst_successor":
            default_val = data_input[0] if data_input else 50
            dlg = ValuePromptDialog(
                title="Tìm Nút Kế Cận (Predecessor & Successor)",
                message="Chọn nút bạn muốn tìm phần tử đứng trước và sau theo In-order:",
                default_val=default_val,
                available_choices=sorted(data_input),
                parent=self
            )
            return [dlg.result_value] if dlg.exec_() else [default_val]

        elif key == "lca_tree":
            dlg = ValuePromptDialog(
                title="Tìm Tổ Tiên Chung Gần Nhất (LCA)",
                message="Nhập 2 giá trị nút cách nhau dấu phẩy (ví dụ: 20, 80) để tìm LCA:",
                is_two_values=True,
                parent=self
            )
            if dlg.exec_():
                v1, v2 = dlg.result_value
                return [v1, v2]
            return [20, 80]

        return []

    # ─────────────────────────────────────────────────────────────────────────
    def _on_step_updated(self, step_state, current_idx, total_steps):
        # 1. Canvas
        self.canvas_stack.currentWidget().update_state(step_state)
        # 2. Code highlighting
        self.code_viewer.highlight_line(step_state.active_line)
        # 3. Log + traversal order
        self.log_panel.update_log(step_state)
        # 4. Slider / counter
        self.controls.update_step(current_idx, total_steps)

    def _on_animation_finished(self):
        dialog = NextActionDialog(self.session.current_algorithm_name, self)
        if dialog.exec_():
            action = dialog.selected_action
            if action == NextActionDialog.ACTION_RERUN:
                self.controller.reset()
                self.controller.play()
            elif action == NextActionDialog.ACTION_CHANGE_ALGO:
                self.back_to_algo_select.emit()
            elif action == NextActionDialog.ACTION_CHANGE_DATA:
                self.request_change_data.emit()

    def _on_back_clicked(self):
        self.controller.pause()
        self.back_to_algo_select.emit()
