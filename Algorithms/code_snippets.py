"""
Dictionary of Code Snippets for all Sorting and Tree Algorithms.
The line numbers match the active_line emitted by their generators.
"""

CODE_SNIPPETS = {
    # ------------------ SORTING ALGORITHMS ------------------
    "bubble_sort": """def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]""",

    "selection_sort": """def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]""",

    "insertion_sort": """def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key""",

    "interchange_sort": """def interchange_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]""",

    "shaker_sort": """def shaker_sort(arr):
    start = 0; end = len(arr) - 1
    while start < end:
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
        start += 1""",

    "quick_sort": """def quick_sort(arr, low, high):
    if low < high:
        # Lomuto Partition
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        p = i + 1
        quick_sort(arr, low, p - 1)
        quick_sort(arr, p + 1, high)""",

    "merge_sort": """def merge_sort(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        # Merge operation
        L = arr[left:mid+1]; R = arr[mid+1:right+1]
        i = j = 0; k = left
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                arr[k] = L[i]; i += 1
            else:
                arr[k] = R[j]; j += 1
            k += 1
        while i < len(L): arr[k] = L[i]; i += 1; k += 1
        while j < len(R): arr[k] = R[j]; j += 1; k += 1""",

    "heap_sort": """def heap_sort(arr):
    n = len(arr)
    # Build Max Heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

def heapify(arr, n, i):
    largest = i; l = 2*i + 1; r = 2*i + 2
    if l < n and arr[l] > arr[largest]: largest = l
    if r < n and arr[r] > arr[largest]: largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)""",

    "shell_sort": """def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2""",

    "tree_sort": """def tree_sort(arr):
    root = None
    for x in arr:
        root = insert_bst(root, x)
    idx = 0
    def inorder(node):
        nonlocal idx
        if node:
            inorder(node.left)
            arr[idx] = node.val; idx += 1
            inorder(node.right)
    inorder(root)""",

    "counting_sort": """def counting_sort(arr):
    max_val = max(arr); min_val = min(arr)
    count = [0] * (max_val - min_val + 1)
    for x in arr:
        count[x - min_val] += 1
    idx = 0
    for val, freq in enumerate(count):
        for _ in range(freq):
            arr[idx] = val + min_val
            idx += 1""",

    "radix_sort": """def radix_sort(arr):
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        count_sort_by_digit(arr, exp)
        exp *= 10

def count_sort_by_digit(arr, exp):
    n = len(arr); output = [0] * n; count = [0] * 10
    for i in range(n): count[(arr[i] // exp) % 10] += 1
    for i in range(1, 10): count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        idx = (arr[i] // exp) % 10
        output[count[idx] - 1] = arr[i]; count[idx] -= 1
    for i in range(n): arr[i] = output[i]""",

    "bucket_sort": """def bucket_sort(arr):
    buckets = [[] for _ in range(len(arr))]
    for x in arr:
        b_idx = int(x / max_val * (len(arr) - 1))
        buckets[b_idx].append(x)
    idx = 0
    for b in buckets:
        b.sort()
        for x in b:
            arr[idx] = x; idx += 1""",

    "tim_sort": """def tim_sort(arr):
    min_run = 32; n = len(arr)
    for i in range(0, n, min_run):
        insertion_sort(arr, i, min(i + min_run - 1, n - 1))
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                merge(arr, left, mid, right)
        size = 2 * size""",

    "intro_sort": """def intro_sort(arr):
    max_depth = 2 * math.floor(math.log2(len(arr)))
    def _intro(start, end, depth_limit):
        if end - start <= 16:
            insertion_sort(arr, start, end)
        elif depth_limit == 0:
            heap_sort_range(arr, start, end)
        else:
            p = partition(arr, start, end)
            _intro(start, p - 1, depth_limit - 1)
            _intro(p + 1, end, depth_limit - 1)
    _intro(0, len(arr) - 1, max_depth)""",

    "block_sort": """def block_sort(arr):
    block_size = int(math.sqrt(len(arr)))
    for start in range(0, len(arr), block_size):
        insertion_sort(arr, start, min(start + block_size, len(arr)))
    # Merge sorted blocks in pairs
    merge_blocks(arr, block_size)""",

    "bitonic_sort": """def bitonic_sort(arr, low, cnt, dire):
    if cnt > 1:
        k = cnt // 2
        bitonic_sort(arr, low, k, 1)      # Tăng dần
        bitonic_sort(arr, low + k, k, 0)  # Giảm dần
        bitonic_merge(arr, low, cnt, dire)

def bitonic_merge(arr, low, cnt, dire):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            comp_and_swap(arr, i, i + k, dire)
        bitonic_merge(arr, low, k, dire)
        bitonic_merge(arr, low + k, k, dire)""",

    "comb_sort": """def comb_sort(arr):
    gap = len(arr); shrink = 1.3; sorted_flag = False
    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1: gap = 1; sorted_flag = True
        for i in range(0, len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted_flag = False""",

    "gnome_sort": """def gnome_sort(arr):
    idx = 0; n = len(arr)
    while idx < n:
        if idx == 0 or arr[idx] >= arr[idx - 1]:
            idx += 1
        else:
            arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]
            idx -= 1""",

    "bead_sort": """def bead_sort(arr):
    max_val = max(arr); n = len(arr)
    grid = [[False] * max_val for _ in range(n)]
    for i, x in enumerate(arr):
        for j in range(x): grid[i][j] = True
    for j in range(max_val):
        count = sum(grid[i][j] for i in range(n))
        for i in range(n - count): grid[i][j] = False
        for i in range(n - count, n): grid[i][j] = True
    for i in range(n): arr[i] = sum(grid[i])""",

    "bogo_sort": """def bogo_sort(arr):
    while not is_sorted(arr):
        random.shuffle(arr)

def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))""",

    # ------------------ TREE ALGORITHMS ------------------
    "preorder_traversal": """def preorder_traversal(root):
    if root:
        print(root.val)       # 1. Thăm Node
        preorder(root.left)   # 2. Duyệt nhánh con Trái
        preorder(root.right)  # 3. Duyệt nhánh con Phải""",

    "inorder_traversal": """def inorder_traversal(root):
    if root:
        inorder(root.left)    # 1. Duyệt nhánh con Trái
        print(root.val)       # 2. Thăm Node
        inorder(root.right)   # 3. Duyệt nhánh con Phải""",

    "postorder_traversal": """def postorder_traversal(root):
    if root:
        postorder(root.left)   # 1. Duyệt nhánh con Trái
        postorder(root.right)  # 2. Duyệt nhánh con Phải
        print(root.val)        # 3. Thăm Node""",

    "levelorder_traversal": """def levelorder_traversal(root):
    if not root: return
    queue = [root]
    while queue:
        node = queue.pop(0)
        print(node.val)
        if node.left: queue.append(node.left)
        if node.right: queue.append(node.right)""",

    "bst_search": """def bst_search(root, target):
    curr = root
    while curr:
        if curr.val == target:
            return curr  # Tìm thấy nút
        elif target < curr.val:
            curr = curr.left
        else:
            curr = curr.right
    return None  # Không tìm thấy""",

    "bst_insert": """def bst_insert(root, val):
    if not root:
        return Node(val)
    curr = root
    while curr:
        if val < curr.val:
            if not curr.left:
                curr.left = Node(val); break
            curr = curr.left
        elif val > curr.val:
            if not curr.right:
                curr.right = Node(val); break
            curr = curr.right
        else: break
    return root""",

    "bst_delete": """def bst_delete(root, key):
    if not root: return None
    if key < root.val:
        root.left = bst_delete(root.left, key)
    elif key > root.val:
        root.right = bst_delete(root.right, key)
    else:
        # Trường hợp 0 hoặc 1 con
        if not root.left: return root.right
        elif not root.right: return root.left
        # Trường hợp 2 con: Tìm Inorder Successor
        temp = min_value_node(root.right)
        root.val = temp.val
        root.right = bst_delete(root.right, temp.val)
    return root""",

    "bst_successor": """def find_successor_predecessor(root, target):
    inorder_list = get_inorder(root)
    idx = inorder_list.index(target)
    pred = inorder_list[idx - 1] if idx > 0 else None
    succ = inorder_list[idx + 1] if idx < len(inorder_list) - 1 else None
    return pred, succ""",

    "avl_tree": """def avl_build(values):
    root = None
    for val in values:
        root = avl_insert(root, val)
    return root""",

    "avl_insert": """def avl_insert(node, val):
    if not node: return AVLNode(val)
    if val < node.val: node.left = avl_insert(node.left, val)
    elif val > node.val: node.right = avl_insert(node.right, val)
    else: return node
    
    node.height = 1 + max(h(node.left), h(node.right))
    balance = get_balance(node)
    
    # 4 Trường hợp mất cân bằng và xoay cây:
    if balance > 1 and val < node.left.val: return rotate_right(node)   # LL
    if balance < -1 and val > node.right.val: return rotate_left(node)   # RR
    if balance > 1 and val > node.left.val:                             # LR
        node.left = rotate_left(node.left); return rotate_right(node)
    if balance < -1 and val < node.right.val:                           # RL
        node.right = rotate_right(node.right); return rotate_left(node)
    return node""",

    "avl_delete": """def avl_delete(node, key):
    if not node: return None
    if key < node.val: node.left = avl_delete(node.left, key)
    elif key > node.val: node.right = avl_delete(node.right, key)
    else:
        if not node.left: return node.right
        elif not node.right: return node.left
        temp = min_value_node(node.right)
        node.val = temp.val
        node.right = avl_delete(node.right, temp.val)
    
    node.height = 1 + max(h(node.left), h(node.right))
    balance = get_balance(node)
    
    # Cân bằng lại sau khi xóa
    if balance > 1 and get_balance(node.left) >= 0: return rotate_right(node)  # LL
    if balance > 1 and get_balance(node.left) < 0:                             # LR
        node.left = rotate_left(node.left); return rotate_right(node)
    if balance < -1 and get_balance(node.right) <= 0: return rotate_left(node) # RR
    if balance < -1 and get_balance(node.right) > 0:                           # RL
        node.right = rotate_right(node.right); return rotate_left(node)
    return node""",

    "red_black_tree": """def rb_insert_fixup(root, z):
    while z.parent and z.parent.color == 'RED':
        if z.parent == z.parent.parent.left:
            y = z.parent.parent.right # Bác của z
            if y and y.color == 'RED': # Case 1: Đổi màu
                z.parent.color = 'BLACK'; y.color = 'BLACK'
                z.parent.parent.color = 'RED'; z = z.parent.parent
            else:
                if z == z.parent.right: # Case 2: Xoay Trái
                    z = z.parent; rotate_left(z)
                # Case 3: Xoay Phải & Đổi màu
                z.parent.color = 'BLACK'; z.parent.parent.color = 'RED'
                rotate_right(z.parent.parent)
    root.color = 'BLACK'""",

    "splay_tree": """def splay(root, key):
    if not root or root.val == key: return root
    # Đẩy nút key lên vị trí gốc thông qua các phép Zig-Zig, Zig-Zag
    if key < root.val:
        if not root.left: return root
        if key < root.left.val:
            root.left.left = splay(root.left.left, key)
            root = rotate_right(root)
        elif key > root.left.val:
            root.left.right = splay(root.left.right, key)
            if root.left.right: root.left = rotate_left(root.left)
        return rotate_right(root) if root.left else root
    else:
        # Nhánh phải tương tự
        return rotate_left(root) if root.right else root""",

    "heap_operations": """def max_heapify(arr, n, i):
    largest = i; l = 2 * i + 1; r = 2 * i + 2
    if l < n and arr[l] > arr[largest]: largest = l
    if r < n and arr[r] > arr[largest]: largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        max_heapify(arr, n, largest)

def extract_max(arr):
    max_val = arr[0]
    arr[0] = arr[-1]; arr.pop()
    max_heapify(arr, len(arr), 0)
    return max_val""",

    "trie_operations": """class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode(ch)
            curr = curr.children[ch]
        curr.is_end_of_word = True""",

    "segment_tree": """def build_segment_tree(arr, l, r):
    if l == r:
        return SegmentNode(l, r, arr[l])
    mid = (l + r) // 2
    left = build_segment_tree(arr, l, mid)
    right = build_segment_tree(arr, mid + 1, r)
    return SegmentNode(l, r, left.val + right.val, left, right)""",

    "fenwick_tree": """def bit_update(bit, n, idx, val):
    i = idx + 1
    while i <= n:
        bit[i] += val
        i += i & (-i)

def bit_query(bit, idx):
    s = 0; i = idx + 1
    while i > 0:
        s += bit[i]
        i -= i & (-i)
    return s""",

    "b_tree": """def btree_insert(root, key):
    if len(root.keys) == 2 * t - 1:
        s = BTreeNode(leaf=False)
        s.children.append(root)
        split_child(s, 0, root)
        insert_non_full(s, key)
        return s
    else:
        insert_non_full(root, key)
        return root""",

    "kruskal_mst": """def kruskal_mst(edges, num_nodes):
    edges.sort(key=lambda e: e.weight)
    mst = []
    dsu = DSU(num_nodes)
    for u, v, w in edges:
        if dsu.union(u, v):
            mst.append((u, v, w))
            if len(mst) == num_nodes - 1:
                break
    return mst""",

    "prim_mst": """def prim_mst(graph, num_nodes):
    visited = {0}; mst = []
    while len(visited) < num_nodes:
        # Chọn cạnh nhẹ nhất nối vết cắt
        min_edge = find_min_crossing_edge(visited, graph)
        u, v, w = min_edge
        visited.add(v)
        mst.append(min_edge)
    return mst""",

    "lca_tree": """def lowest_common_ancestor(root, n1, n2):
    curr = root
    while curr:
        if n1 < curr.val and n2 < curr.val:
            curr = curr.left
        elif n1 > curr.val and n2 > curr.val:
            curr = curr.right
        else:
            return curr # Đỉnh phân nhánh chính là LCA
    return None"""
}
