"""
Algorithm Selection View: Rich categorized cards for all 21+ Sorting and Tree algorithms.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFrame, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from core.session_manager import SessionManager

# Metadata for Sorting Algorithms
SORTING_ALGORITHMS = [
    # 1. Simple Comparison
    {"key": "bubble_sort", "name_vi": "Sắp xếp Nổi bọt", "name_en": "Bubble Sort", "group": "Cơ bản", "time": "O(N²)", "space": "O(1)", "desc": "So sánh 2 phần tử kề nhau và đổi chỗ liên tục để đẩy phần tử lớn nhất về cuối."},
    {"key": "selection_sort", "name_vi": "Sắp xếp Chọn", "name_en": "Selection Sort", "group": "Cơ bản", "time": "O(N²)", "space": "O(1)", "desc": "Tìm phần tử nhỏ nhất trong dãy chưa sắp xếp và đưa về vị trí đầu dãy."},
    {"key": "insertion_sort", "name_vi": "Sắp xếp Chèn", "name_en": "Insertion Sort", "group": "Cơ bản", "time": "O(N²)", "space": "O(1)", "desc": "Lần lượt lấy từng phần tử chèn vào đúng vị trí của dãy đã có thứ tự bên trái."},
    {"key": "interchange_sort", "name_vi": "Đổi chỗ Trực tiếp", "name_en": "Interchange Sort", "group": "Cơ bản", "time": "O(N²)", "space": "O(1)", "desc": "So sánh phần tử i với tất cả phần tử đứng sau j > i, đổi chỗ ngay khi vi phạm thứ tự."},
    {"key": "shaker_sort", "name_vi": "Sắp xếp Shaker (Cocktail)", "name_en": "Shaker / Cocktail Sort", "group": "Biến thể", "time": "O(N²)", "space": "O(1)", "desc": "Nổi bọt hai chiều: lượt đi đẩy số lớn về cuối, lượt về kéo số nhỏ về đầu."},
    {"key": "comb_sort", "name_vi": "Sắp xếp Lược", "name_en": "Comb Sort", "group": "Biến thể", "time": "O(N log N)", "space": "O(1)", "desc": "Cải tiến Bubble Sort bằng cách so sánh các phần tử cách nhau khoảng cách gap thu hẹp dần."},
    {"key": "gnome_sort", "name_vi": "Sắp xếp Chú Lùn", "name_en": "Gnome Sort", "group": "Biến thể", "time": "O(N²)", "space": "O(1)", "desc": "Nếu đúng thứ tự thì tiến 1 bước, nếu sai thứ tự thì đổi chỗ và lùi 1 bước."},

    # 2. Advanced Comparison
    {"key": "quick_sort", "name_vi": "Sắp xếp Nhanh", "name_en": "Quick Sort", "group": "Chia để trị", "time": "O(N log N)", "space": "O(log N)", "desc": "Chọn phần tử chốt (Pivot), phân đoạn mảng thành 2 nửa nhỏ hơn và lớn hơn pivot."},
    {"key": "merge_sort", "name_vi": "Sắp xếp Trộn", "name_en": "Merge Sort", "group": "Chia để trị", "time": "O(N log N)", "space": "O(N)", "desc": "Chia đôi mảng đệ quy cho đến khi còn 1 phần tử rồi trộn có thứ tự từng cặp."},
    {"key": "heap_sort", "name_vi": "Sắp xếp Đống", "name_en": "Heap Sort", "group": "Cấu trúc cây", "time": "O(N log N)", "space": "O(1)", "desc": "Xây dựng Max-Heap, liên tục lấy phần tử gốc lớn nhất đưa về cuối mảng và vun đống."},
    {"key": "tree_sort", "name_vi": "Sắp xếp Cây", "name_en": "Tree Sort", "group": "Cấu trúc cây", "time": "O(N log N)", "space": "O(N)", "desc": "Chèn các phần tử vào Cây nhị phân tìm kiếm (BST), sau đó duyệt In-order để trích xuất."},
    {"key": "shell_sort", "name_vi": "Sắp xếp Shell", "name_en": "Shell Sort", "group": "Nâng cao", "time": "O(N^(3/2))", "space": "O(1)", "desc": "Sắp xếp chèn trên các dãy con cách nhau khoảng cách gap giảm dần về 1."},

    # 3. Distribution & Non-comparison
    {"key": "counting_sort", "name_vi": "Sắp xếp Đếm", "name_en": "Counting Sort", "group": "Phân phối", "time": "O(N + K)", "space": "O(K)", "desc": "Đếm tần suất xuất hiện của từng giá trị rồi tính vị trí chính xác trong mảng kết quả."},
    {"key": "radix_sort", "name_vi": "Sắp xếp Theo Chữ Số", "name_en": "Radix Sort (LSD)", "group": "Phân phối", "time": "O(d*(N+K))", "space": "O(N+K)", "desc": "Sắp xếp ổn định lần lượt theo từng chữ số từ hàng đơn vị đến hàng cao nhất."},
    {"key": "bucket_sort", "name_vi": "Sắp xếp Theo Xô", "name_en": "Bucket Sort", "group": "Phân phối", "time": "O(N + K)", "space": "O(N)", "desc": "Phân phối các phần tử vào các xô con đồng đều, sắp xếp từng xô rồi ghép lại."},
    {"key": "bead_sort", "name_vi": "Sắp xếp Trọng Lực Hạt", "name_en": "Bead / Gravity Sort", "group": "Vật lý / Hạt", "time": "O(N)", "space": "O(N²)", "desc": "Mô phỏng các hạt bàn tính rơi tự do theo trọng lực để sắp xếp mảng số nguyên dương."},

    # 4. Modern Hybrids & Networks
    {"key": "tim_sort", "name_vi": "Tim Sort", "name_en": "TimSort (Python/Java)", "group": "Lai hiện đại", "time": "O(N log N)", "space": "O(N)", "desc": "Thuật toán sắp xếp chuẩn của Python & Java: Chia mảng thành các Run rồi trộn thông minh."},
    {"key": "intro_sort", "name_vi": "Intro Sort", "name_en": "Introspective Sort", "group": "Lai hiện đại", "time": "O(N log N)", "space": "O(log N)", "desc": "Bắt đầu với QuickSort, chuyển sang HeapSort nếu đệ quy sâu, dùng InsertionSort khi mảng nhỏ."},
    {"key": "block_sort", "name_vi": "Sắp xếp Khối", "name_en": "Block Merge Sort", "group": "Lai hiện đại", "time": "O(N log N)", "space": "O(1)", "desc": "Chia mảng thành các khối √N, sắp xếp từng khối rồi trộn tối ưu bộ nhớ O(1)."},
    {"key": "bitonic_sort", "name_vi": "Sắp xếp Mạng Bitonic", "name_en": "Bitonic Sort", "group": "Mạng sắp xếp", "time": "O(log² N)", "space": "O(N log² N)", "desc": "Mô hình mạng sắp xếp song song dựa trên dãy bitonic (nửa tăng, nửa giảm)."},
    {"key": "bogo_sort", "name_vi": "Bogo Sort (Stupid Sort)", "name_en": "Bogo Sort", "group": "Ngẫu nhiên", "time": "O((N+1)!)", "space": "O(1)", "desc": "Xáo trộn ngẫu nhiên liên tục cho đến khi mảng may mắn tự sắp xếp."}
]

# Metadata for Tree Algorithms
TREE_ALGORITHMS = [
    # 1. Traversals
    {"key": "preorder_traversal", "name_vi": "Duyệt Tiền thứ tự (NLR)", "name_en": "Pre-order Traversal (DFS)", "group": "Duyệt cây", "time": "O(N)", "space": "O(H)", "desc": "Thăm nút gốc trước (N), sau đó duyệt nhánh con trái (L), rồi đến nhánh con phải (R)."},
    {"key": "inorder_traversal", "name_vi": "Duyệt Trung thứ tự (LNR)", "name_en": "In-order Traversal (DFS)", "group": "Duyệt cây", "time": "O(N)", "space": "O(H)", "desc": "Duyệt nhánh trái (L), thăm nút gốc (N), duyệt nhánh phải (R) -> Tạo dãy số tăng dần trên BST."},
    {"key": "postorder_traversal", "name_vi": "Duyệt Hậu thứ tự (LRN)", "name_en": "Post-order Traversal (DFS)", "group": "Duyệt cây", "time": "O(N)", "space": "O(H)", "desc": "Duyệt nhánh trái (L), duyệt nhánh phải (R), rồi mới thăm nút gốc (N)."},
    {"key": "levelorder_traversal", "name_vi": "Duyệt Theo Tầng (BFS)", "name_en": "Level-order Traversal (BFS)", "group": "Duyệt cây", "time": "O(N)", "space": "O(W)", "desc": "Duyệt cây theo từng tầng từ trên xuống dưới, từ trái sang phải bằng hàng đợi Queue."},

    # 2. BST Operations
    {"key": "bst_search", "name_vi": "Tìm kiếm trên BST", "name_en": "BST Search", "group": "Thao tác BST", "time": "O(log N)", "space": "O(1)", "desc": "Hỏi giá trị cần tìm, rẽ trái nếu nhỏ hơn, rẽ phải nếu lớn hơn để tìm kiếm nút trên BST."},
    {"key": "bst_insert", "name_vi": "Chèn nút vào cây BST", "name_en": "BST Insertion", "group": "Thao tác BST", "time": "O(log N)", "space": "O(1)", "desc": "Hỏi giá trị muốn thêm, mô phỏng duyệt tìm vị trí thích hợp và chèn nút mới vào cây BST."},
    {"key": "bst_delete", "name_vi": "Xóa nút khỏi cây BST", "name_en": "BST Deletion", "group": "Thao tác BST", "time": "O(log N)", "space": "O(1)", "desc": "Hỏi giá trị muốn xóa, mô phỏng xóa 3 trường hợp: lá, 1 con, hoặc 2 con (dùng Successor)."},
    {"key": "bst_successor", "name_vi": "Tìm Nút Kế Cận (Pre/Succ)", "name_en": "Predecessor & Successor", "group": "Thao tác BST", "time": "O(log N)", "space": "O(1)", "desc": "Tìm phần tử đứng ngay trước và ngay sau theo thứ tự In-order của một giá trị."},

    # 3. AVL Tree Operations (Interactive Insert & Delete)
    {"key": "avl_insert", "name_vi": "Chèn nút vào Cây AVL", "name_en": "AVL Tree Insertion", "group": "Cây AVL", "time": "O(log N)", "space": "O(log N)", "desc": "Hỏi giá trị muốn chèn, thêm vào cây AVL và mô phỏng các phép xoay LL, RR, LR, RL để tự cân bằng."},
    {"key": "avl_delete", "name_vi": "Xóa nút khỏi Cây AVL", "name_en": "AVL Tree Deletion", "group": "Cây AVL", "time": "O(log N)", "space": "O(log N)", "desc": "Hỏi giá trị muốn xóa, loại bỏ nút khỏi cây AVL và thực hiện xoay cân bằng lại từng bước."},
    {"key": "avl_tree", "name_vi": "Xây dựng Cây AVL", "name_en": "AVL Tree Build", "group": "Cây AVL", "time": "O(N log N)", "space": "O(N)", "desc": "Xây dựng cây AVL hoàn chỉnh từ toàn bộ mảng dữ liệu ban đầu, duy trì |BF| <= 1."},

    # 4. Other Self Balancing Trees
    {"key": "red_black_tree", "name_vi": "Cây Đỏ - Đen (Red-Black)", "name_en": "Red-Black Tree", "group": "Tự cân bằng", "time": "O(log N)", "space": "O(N)", "desc": "Cây tự cân bằng theo màu sắc (Đỏ/Đen) đảm bảo đường đi từ gốc đến lá không lệch quá 2 lần."},
    {"key": "splay_tree", "name_vi": "Cây Splay", "name_en": "Splay Tree", "group": "Tự cân bằng", "time": "O(log N)", "space": "O(N)", "desc": "Thao tác Splay tự động đẩy các nút vừa được truy cập lên gốc qua các phép xoay Zig-Zag."},

    # 5. Heap Operations
    {"key": "heap_operations", "name_vi": "Giải thuật Đống (Heapify)", "name_en": "Max/Min Heap Operations", "group": "Cấu trúc Heap", "time": "O(log N)", "space": "O(1)", "desc": "Vun đống Max-Heap, trích xuất phần tử cực đại (Extract Max) và cập nhật khóa."},

    # 6. Advanced Trees
    {"key": "b_tree", "name_vi": "Cây B (B-Tree)", "name_en": "B-Tree / B+ Tree", "group": "Đa đường nâng cao", "time": "O(log N)", "space": "O(N)", "desc": "Cây tìm kiếm đa phân tự cân bằng, tối ưu cho cấu trúc chỉ mục cơ sở dữ liệu và ổ đĩa."},
    {"key": "trie_operations", "name_vi": "Cây Tiền Tố (Trie)", "name_en": "Trie (Prefix Tree)", "group": "Đa đường nâng cao", "time": "O(L)", "space": "O(Alphabet*N)", "desc": "Cây tìm kiếm chuỗi ký tự theo tiền tố, hỗ trợ tự động hoàn thành từ điển siêu tốc."},
    {"key": "segment_tree", "name_vi": "Cây Phân Đoạn (Segment Tree)", "name_en": "Segment Tree", "group": "Đa đường nâng cao", "time": "O(log N)", "space": "O(N)", "desc": "Quản lý và truy vấn tổng/min/max theo khoảng [L..R] và cập nhật điểm trong O(log N)."},
    {"key": "fenwick_tree", "name_vi": "Cây Fenwick (BIT)", "name_en": "Binary Indexed Tree", "group": "Đa đường nâng cao", "time": "O(log N)", "space": "O(N)", "desc": "Cấu trúc cây chỉ số nhị phân tính tổng tiền tố và cập nhật mảng cực kỳ tinh gọn."},

    # 7. Graph Trees
    {"key": "kruskal_mst", "name_vi": "Cây Khung Tối Tiểu Kruskal", "name_en": "Kruskal's MST Algorithm", "group": "Cây trên đồ thị", "time": "O(E log E)", "space": "O(V)", "desc": "Tìm cây khung có tổng trọng số nhỏ nhất bằng cách sắp xếp cạnh và dùng Disjoint Set (DSU)."},
    {"key": "prim_mst", "name_vi": "Cây Khung Tối Tiểu Prim", "name_en": "Prim's MST Algorithm", "group": "Cây trên đồ thị", "time": "O(E + V log V)", "space": "O(V)", "desc": "Phát triển cây khung tối tiểu từ một đỉnh nguồn bằng cách tham lam chọn cạnh nhẹ nhất nối vết cắt."},
    {"key": "lca_tree", "name_vi": "Tổ Tiên Chung Gần Nhất (LCA)", "name_en": "Lowest Common Ancestor", "group": "Cây trên đồ thị", "time": "O(H)", "space": "O(1)", "desc": "Tìm nút tổ tiên chung nằm sâu nhất của hai nút con bất kỳ trên cây."}
]

class AlgorithmSelectView(QWidget):
    algorithm_selected = pyqtSignal(str, str, str, dict) # (category, algo_key, algo_name, meta)
    back_to_input_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = SessionManager.instance()
        self.current_category = "sorting"
        self.cards = []

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(15)

        # Header with Back button and Title
        header_row = QHBoxLayout()
        self.btn_back = QPushButton("⬅ Quay Lại Nhập Dữ Liệu")
        self.btn_back.clicked.connect(self.back_to_input_requested.emit)
        header_row.addWidget(self.btn_back)

        header_row.addStretch()

        title_lbl = QLabel("🎯 Bước 2: Lựa Chọn Giải Thuật Mô Phỏng")
        title_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #38bdf8;")
        header_row.addWidget(title_lbl)

        header_row.addStretch()
        main_layout.addLayout(header_row)

        # Category Switcher Buttons
        cat_row = QHBoxLayout()
        cat_row.setSpacing(15)

        self.btn_cat_sorting = QPushButton("📊 THUẬT TOÁN SẮP XẾP (21 Giải Thuật)")
        self.btn_cat_sorting.setCheckable(True)
        self.btn_cat_sorting.setChecked(True)
        self.btn_cat_sorting.setStyleSheet("""
            QPushButton {
                background-color: #0284c7;
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
            }
        """)
        self.btn_cat_sorting.clicked.connect(lambda: self._switch_category("sorting"))
        cat_row.addWidget(self.btn_cat_sorting)

        self.btn_cat_tree = QPushButton("🌲 THUẬT TOÁN & CẤU TRÚC CÂY (20 Giải Thuật)")
        self.btn_cat_tree.setCheckable(True)
        self.btn_cat_tree.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #94a3b8;
                font-size: 14px;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
                border: 1px solid #334155;
            }
        """)
        self.btn_cat_tree.clicked.connect(lambda: self._switch_category("tree"))
        cat_row.addWidget(self.btn_cat_tree)

        main_layout.addLayout(cat_row)

        # Search / Filter Bar
        search_row = QHBoxLayout()
        lbl_search = QLabel("🔍 Tìm kiếm nhanh:")
        lbl_search.setStyleSheet("color: #94a3b8; font-weight: 500;")
        search_row.addWidget(lbl_search)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Nhập tên giải thuật (ví dụ: Quick, AVL, BST, Merge, DFS, Radix, MST...)...")
        self.txt_search.textChanged.connect(self._filter_cards)
        search_row.addWidget(self.txt_search)

        main_layout.addLayout(search_row)

        # Scroll Area with Card Grid
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        self.cards_container = QWidget()
        self.grid_layout = QGridLayout(self.cards_container)
        self.grid_layout.setSpacing(14)
        self.grid_layout.setContentsMargins(5, 5, 5, 5)

        self.scroll_area.setWidget(self.cards_container)
        main_layout.addWidget(self.scroll_area)

        self._populate_cards("sorting")

    def _switch_category(self, cat):
        self.current_category = cat
        if cat == "sorting":
            self.btn_cat_sorting.setStyleSheet("background-color: #0284c7; color: #ffffff; font-size: 14px; font-weight: bold; padding: 12px; border-radius: 8px;")
            self.btn_cat_tree.setStyleSheet("background-color: #1e293b; color: #94a3b8; font-size: 14px; font-weight: bold; padding: 12px; border-radius: 8px; border: 1px solid #334155;")
        else:
            self.btn_cat_tree.setStyleSheet("background-color: #059669; color: #ffffff; font-size: 14px; font-weight: bold; padding: 12px; border-radius: 8px;")
            self.btn_cat_sorting.setStyleSheet("background-color: #1e293b; color: #94a3b8; font-size: 14px; font-weight: bold; padding: 12px; border-radius: 8px; border: 1px solid #334155;")

        self.txt_search.clear()
        self._populate_cards(cat)

    def _populate_cards(self, cat):
        # Clear existing cards
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.cards.clear()
        algo_list = SORTING_ALGORITHMS if cat == "sorting" else TREE_ALGORITHMS

        cols = 3
        for idx, algo in enumerate(algo_list):
            card = self._create_algo_card(cat, algo)
            row = idx // cols
            col = idx % cols
            self.grid_layout.addWidget(card, row, col)
            self.cards.append((card, algo))

    def _create_algo_card(self, cat, algo):
        card = QFrame()
        card.setObjectName("algo_card")
        card.setStyleSheet("""
            QFrame#algo_card {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 12px;
            }
            QFrame#algo_card:hover {
                background-color: #243248;
                border: 1px solid #38bdf8;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        # Header with Group Badge
        top_row = QHBoxLayout()
        lbl_group = QLabel(algo["group"])
        lbl_group.setStyleSheet("background-color: #334155; color: #38bdf8; font-size: 10px; font-weight: bold; padding: 2px 6px; border-radius: 4px;")
        top_row.addWidget(lbl_group)
        top_row.addStretch()

        lbl_time = QLabel(f"⏱ {algo['time']}")
        lbl_time.setStyleSheet("color: #f59e0b; font-size: 11px; font-weight: 600;")
        top_row.addWidget(lbl_time)
        layout.addLayout(top_row)

        # Name VI
        lbl_name_vi = QLabel(algo["name_vi"])
        lbl_name_vi.setStyleSheet("font-size: 15px; font-weight: bold; color: #f8fafc;")
        layout.addWidget(lbl_name_vi)

        # Name EN
        lbl_name_en = QLabel(algo["name_en"])
        lbl_name_en.setStyleSheet("font-size: 12px; color: #94a3b8; font-style: italic;")
        layout.addWidget(lbl_name_en)

        # Description
        lbl_desc = QLabel(algo["desc"])
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("font-size: 12px; color: #cbd5e1; margin-top: 4px;")
        layout.addWidget(lbl_desc)

        layout.addStretch()

        # Start button on card
        btn_start = QPushButton("▶ Khởi Chạy Mô Phỏng")
        btn_start.setStyleSheet("""
            QPushButton {
                background-color: #0284c7;
                color: #ffffff;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0ea5e9;
            }
        """)
        btn_start.clicked.connect(lambda _, a=algo: self._on_card_selected(cat, a))
        layout.addWidget(btn_start)

        return card

    def _on_card_selected(self, cat, algo):
        self.session.set_algorithm(cat, algo["key"], algo["name_vi"], algo)
        self.algorithm_selected.emit(cat, algo["key"], algo["name_vi"], algo)

    def _filter_cards(self, query):
        query = query.strip().lower()
        for card, algo in self.cards:
            match = (
                query in algo["name_vi"].lower()
                or query in algo["name_en"].lower()
                or query in algo["group"].lower()
                or query in algo["desc"].lower()
            )
            card.setVisible(match)
