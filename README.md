# 🌟 Visual AlgoStudio (v2.0.0)
### 🚀 Ứng Dụng Desktop Mô Phỏng Trực Quan Sinh Động Thuật Toán Sắp Xếp & Cấu Trúc Dữ Liệu Cây

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green.svg?logo=qt)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-0078D6.svg?logo=windows)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Release-v2.0.0%20(Standalone%20EXE)-brightgreen.svg)

---

## 📖 Giới Thiệu Tổng Quan

**Visual AlgoStudio** là một ứng dụng Desktop đồ họa hiện đại (Dark Theme) được phát triển bằng **Python** và **PyQt5**, nhằm mục đích trực quan hóa các bước thực hiện của **42 giải thuật** kinh điển và nâng cao trong Khoa học Máy tính.

Ứng dụng kết hợp giữa **mô phỏng đồ họa động 60fps**, **đồng bộ dòng code đang chạy theo thời gian thực (Code Highlighter)**, **bảng phân tích độ phức tạp thuật toán (Complexity Panel)** và **hộp thoại tương tác thông minh (Interactive Value Prompts)**, giúp người học, sinh viên và giảng viên tiếp cận thuật toán một cách trực quan, sinh động và dễ hiểu nhất.

---

## ✨ Tính Năng Nổi Bật

- 🎨 **Giao diện Dark Theme Cyberpunk / Navy Blue:** Thiết kế chuyên nghiệp, độ tương phản cao, tối ưu cho mắt khi làm việc lâu.
- ⚡ **Tùy chỉnh số lượng phần tử linh hoạt ($N = 3 \rightarrow 100$):**
  - Thanh trượt Slider & SpinBox tùy biến nhanh.
  - Bộ sinh dữ liệu mẫu có sẵn: *Ngẫu nhiên*, *Nghịch đảo*, *Gần như đã sắp*, *Nhiều phần tử trùng lặp*.
  - Hỗ trợ nhập chuỗi số thủ công linh hoạt với các dấu phân cách `,`, `;`, `khoảng trắng`.
- 🔄 **3 Canvas Đồ Họa Riêng Biệt (QPainter Vector Rendering):**
  - **Sorting Canvas:** Biểu đồ cột Gradient 3D, tự động điều chỉnh độ rộng và ẩn số thông minh khi $N$ lớn.
  - **Tree Canvas:** Vẽ cây 2D phân tầng không chồng chéo, hỗ trợ hiển thị hệ số cân bằng $BF$ trên AVL, vầng sáng xoay cây (Pulse Glow), nhãn đoạn `[L..R]` trên Segment Tree, cây tiền tố Trie, hộp khóa B-Tree và mảng BIT Fenwick.
  - **Graph Canvas:** Đồ thị tròn trực quan cho thuật toán tìm Cây khung tối tiểu (MST - Kruskal & Prim) với phân loại cạnh bằng màu sắc.
- 💻 **Đồng bộ hóa Mã Nguồn (Real-time Code Highlighting):** Trỏ sáng từng dòng lệnh Python tương ứng với bước thuật toán đang thực hiện.
- 🎯 **Tương tác Thêm/Xóa Trực Tiếp (Interactive Prompts):** Khi chọn Chèn/Xóa trên BST hoặc AVL, hệ thống sẽ mở modal hỏi giá trị người dùng muốn thao tác và mô phỏng từng bước rẽ nhánh, cân bằng lại.
- 🎮 **Bảng Điều Khiển Phát Toàn Diện:** Play, Pause, Next Step, Previous Step, Thanh trượt tua nhanh (Step Scrubber), Điều chỉnh tốc độ mô phỏng từ $30\text{ms}$ (siêu tốc) đến $1500\text{ms}$ (chậm chi tiết).
- 📦 **Đóng gói Desktop App độc lập (.EXE):** Chạy trực tiếp trên Windows mà **không cần cài Python hay mở terminal**.

---

## 📚 Danh Mục 42 Giải Thuật Được Hỗ Trợ

### 📊 1. Thuật Toán Sắp Xếp (21 Giải Thuật)
| Phân loại | Tên tiếng Việt | Tên tiếng Anh | Độ phức tạp TB |
| :--- | :--- | :--- | :---: |
| **Cơ bản** | Sắp xếp Nổi bọt | Bubble Sort | $O(N^2)$ |
| | Sắp xếp Chọn | Selection Sort | $O(N^2)$ |
| | Sắp xếp Chèn | Insertion Sort | $O(N^2)$ |
| | Đổi chỗ Trực tiếp | Interchange Sort | $O(N^2)$ |
| **Biến thể** | Sắp xếp Shaker (Cocktail) | Shaker / Cocktail Sort | $O(N^2)$ |
| | Sắp xếp Lược | Comb Sort | $O(N \log N)$ |
| | Sắp xếp Chú lùn | Gnome Sort | $O(N^2)$ |
| **Chia để trị** | Sắp xếp Nhanh | Quick Sort (Lomuto Partition) | $O(N \log N)$ |
| | Sắp xếp Trộn | Merge Sort | $O(N \log N)$ |
| **Cấu trúc dữ liệu**| Sắp xếp Đống | Heap Sort (Max-Heap) | $O(N \log N)$ |
| | Sắp xếp Cây | Tree Sort (BST In-order) | $O(N \log N)$ |
| | Sắp xếp Shell | Shell Sort | $O(N^{3/2})$ |
| **Phân phối / Không so sánh** | Sắp xếp Đếm | Counting Sort | $O(N + K)$ |
| | Sắp xếp Theo Chữ Số | Radix Sort (LSD) | $O(d \cdot (N+K))$ |
| | Sắp xếp Theo Xô | Bucket Sort | $O(N + K)$ |
| | Sắp xếp Trọng Lực Hạt | Bead / Gravity Sort | $O(N)$ |
| **Lai hiện đại & Mạng** | TimSort | TimSort (Python/Java default) | $O(N \log N)$ |
| | IntroSort | Introspective Sort (C++ STL) | $O(N \log N)$ |
| | Sắp xếp Khối | Block Merge Sort | $O(N \log N)$ |
| | Sắp xếp Mạng Bitonic | Bitonic Sort | $O(\log^2 N)$ |
| **Ngẫu nhiên** | Sắp xếp Bogo | Bogo Sort (Stupid Sort) | $O((N+1)!)$ |

---

### 🌲 2. Cấu Trúc Dữ Liệu & Giải Thuật Cây (21 Giải Thuật)
| Phân loại | Tên tiếng Việt | Tên tiếng Anh / Thao tác |
| :--- | :--- | :--- |
| **Duyệt Cây** | Duyệt Tiền thứ tự | Pre-order Traversal (NLR - DFS) |
| | Duyệt Trung thứ tự | In-order Traversal (LNR - DFS) |
| | Duyệt Hậu thứ tự | Post-order Traversal (LRN - DFS) |
| | Duyệt Theo Tầng | Level-order Traversal (BFS) |
| **Thao tác BST** | Tìm kiếm trên BST | BST Search (Interactive Target) |
| | Chèn nút vào BST | BST Insertion (Interactive Value) |
| | Xóa nút khỏi BST | BST Deletion (3 trường hợp: lá, 1 con, 2 con) |
| | Tìm Nút Kế Cận | In-order Predecessor & Successor |
| **Cây AVL** | Xây dựng Cây AVL | AVL Tree Build |
| | Chèn nút vào Cây AVL | AVL Insertion & Auto Rebalance (LL, RR, LR, RL) |
| | Xóa nút khỏi Cây AVL | AVL Deletion & Auto Rebalance |
| **Cây Tự Cân Bằng** | Cây Đỏ - Đen | Red-Black Tree (Đổi màu & Cân bằng) |
| | Cây Splay | Splay Tree (Zig-Zig, Zig-Zag đẩy khóa lên gốc) |
| **Cấu trúc Heap** | Thao tác Đống Cực Đại | Max Heapify & Extract Max |
| **Đa Đường & Nâng Cao** | Cây Tiền Tố | Trie (Prefix Tree) |
| | Cây Phân Đoạn | Segment Tree (Range Sum Query $[L..R]$) |
| | Cây Fenwick | Binary Indexed Tree (BIT) |
| | Cây B | B-Tree bậc 3 (Multi-key Split) |
| **Cây Trên Đồ Thị** | Cây Khung Tối Tiểu Kruskal | Kruskal's MST (DSU Disjoint Set) |
| | Cây Khung Tối Tiểu Prim | Prim's MST (Vết cắt Minimum Cut) |
| | Tổ Tiên Chung Gần Nhất | Lowest Common Ancestor (LCA) |

---

## 📂 Cấu Trúc Thư Mục Dự Án

```plaintext
Sorting_Tree_Algorithm/
├── assets/                          # Icon và tài nguyên đồ họa ứng dụng
│   ├── app_icon.ico                 # Multi-size Windows Icon
│   └── app_icon.png                 # High-res PNG logo
├── Algorithms/                      # Lõi chứa 42 Generator giải thuật
│   ├── step_state.py                # Snapshot trạng thái trực quan (StepState)
│   ├── code_snippets.py             # Mã nguồn tương ứng cho từng giải thuật
│   ├── Sorting/                     # 21 Thuật toán sắp xếp
│   │   ├── simple_sorts.py
│   │   ├── advanced_sorts.py
│   │   ├── variant_sorts.py
│   │   ├── distribution_sorts.py
│   │   ├── modern_hybrid_sorts.py
│   │   ├── network_sorts.py
│   │   └── esoteric_sorts.py
│   └── Tree/                        # 21 Thuật toán và cấu trúc cây
│       ├── tree_models.py           # BinaryNode, AVLNode, TrieNode, SegmentNode, BTreeNode
│       ├── traversals.py            # Pre/In/Post/Level-order
│       ├── bst_operations.py        # BST Search, Insert, Delete, Pre/Succ
│       ├── self_balancing.py        # AVL (Insert, Delete, Build), Red-Black, Splay
│       ├── heap_algorithms.py       # Max Heapify & Extract Max
│       ├── advanced_trees.py        # Trie, Segment Tree, Fenwick, B-Tree
│       └── graph_tree_algorithms.py # Kruskal, Prim, LCA
├── core/                            # Quản lý vòng đời và animation
│   ├── animation_controller.py      # Điều khiển tua, phát, tạm dừng, tốc độ
│   └── session_manager.py           # Quản lý dữ liệu dùng chung giữa các màn hình
├── gui/                             # Giao diện người dùng (PyQt5)
│   ├── canvas/                      # Các khung vẽ đồ họa QPainter
│   │   ├── sorting_canvas.py        # Vẽ biểu đồ cột sắp xếp
│   │   ├── tree_canvas.py           # Vẽ cây 2D đa năng
│   │   └── graph_canvas.py          # Vẽ đồ thị MST Kruskal/Prim
│   ├── views/                       # Các màn hình chính
│   │   ├── input_view.py            # Màn hình 1: Nhập và sinh mảng
│   │   ├── algorithm_select_view.py # Màn hình 2: Chọn giải thuật
│   │   ├── visualizer_view.py       # Màn hình 3: Khung mô phỏng trực quan
│   │   └── next_action_dialog.py    # Modal thông báo hoàn thành
│   ├── widgets/                     # Các widget phụ trợ
│   │   ├── code_highlighter.py      # Bộ hiển thị và tô sáng mã code
│   │   ├── control_bar.py           # Thanh nút bấm Play/Pause/Slider
│   │   ├── custom_dialogs.py        # Modal hỏi giá trị chèn/xóa/tìm kiếm
│   │   └── log_panel.py             # Bảng giải thích chi tiết từng bước
│   └── main_window.py               # Cửa sổ chính điều hướng QStackedWidget
├── utils/                           # Tiện ích bổ trợ
│   ├── array_generator.py           # Sinh mảng ngẫu nhiên và parser chuỗi
│   ├── tree_layout.py               # Thuật toán tính tọa độ (x, y) cho cây 2D
│   └── theme.py                     # QSS Stylesheet Dark Theme
├── config.py                        # Cấu hình toàn cục (Kích thước, tốc độ, giới hạn N)
├── generate_icon.py                 # Script tự động tạo Icon ứng dụng
├── main.py                          # File khởi chạy chính
├── test_algorithms.py               # Unit Test kiểm tra toàn bộ 42 giải thuật
├── test_canvas_rendering.py         # Kiểm thử tự động render QPainter
├── Visual_AlgoStudio.spec           # File cấu hình đóng gói PyInstaller
└── requirements.txt                 # Danh sách thư viện phụ thuộc

## 📂 Cấu Trúc Thư Mục Dự Án

### 1. Yêu cầu hệ thống
- Hệ điều hành: Windows 10 / 11 (hoặc macOS, Linux).
- Python: Phiên bản 3.10 trở lên.

### 2. Cài đặt môi trường & thư viện
- Mở Terminal / PowerShell tại thư mục dự án và chạy:
powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

### 3. Khởi chạy ứng dụng từ mã nguồn
- Chạy trực tiếp file main.py:
powershell
python main.py

### 4. Chạy kiểm thử tự động (Unit Test & Render Test)
- Kiểm thử logic toàn bộ 42 giải thuật:
powershell
python test_algorithms.py

- Kiểm thử hiển thị đồ họa trên Canvas:
powershell
python test_canvas_rendering.py

## 📦 Đóng Gói Thành File Cài Đặt / Chạy Trực Tiếp (.EXE)
Để tạo ra một file .exe độc lập duy nhất có thể copy sang bất kỳ máy tính nào chạy ngay mà không cần cài Python:

### 1.Cài đặt công cụ đóng gói:

powershell
python -m pip install pyinstaller pillow

### 2.Sinh bộ Icon độ phân giải cao:

powershell
python generate_icon.py

### 3.Tiến hành đóng gói bằng PyInstaller:

powershell
python -m PyInstaller --clean Visual_AlgoStudio.spec

### 4.Nhận kết quả:
File thực thi độc lập sẽ được tạo tại: dist/Visual_AlgoStudio.exe.

Bạn có thể chuyển file này ra Desktop hoặc gửi cho người khác, chỉ cần nhấp đúp là ứng dụng sẽ mở ngay lập tức!