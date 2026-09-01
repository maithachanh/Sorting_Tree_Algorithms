"""
Advanced and Multiway Tree Structures: Trie, Segment Tree, Fenwick (BIT), B-Tree.
"""
from Algorithms.step_state import StepState, ActionType
from Algorithms.Tree.tree_models import TrieNode, SegmentTreeNode, BTreeNode, reset_node_counter

def trie_simulation(words=None):
    if not words:
        words = ["cat", "car", "cart", "dog", "dot"]

    reset_node_counter()
    root = TrieNode()

    yield StepState(
        action_type=ActionType.INFO,
        current_data=root,
        active_line=1,
        message=f"Bắt đầu xây dựng Cây tiền tố (Trie) với danh sách từ: {words}."
    )

    for word in words:
        curr = root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode(ch)
            curr = curr.children[ch]
            yield StepState(
                action_type=ActionType.INSERT_NODE,
                highlighted_indices=[curr.id],
                current_data=root,
                active_line=4,
                message=f"Chèn ký tự '{ch}' của từ '{word}' vào Trie."
            )
        curr.is_end_of_word = True
        yield StepState(
            action_type=ActionType.MARK,
            highlighted_indices=[curr.id],
            current_data=root,
            active_line=7,
            message=f"Đánh dấu kết thúc từ '{word}' tại nút '{curr.char}'."
        )

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message="Xây dựng Trie hoàn tất!"
    )


def segment_tree_simulation(values):
    arr = list(values)[:8] if len(values) > 8 else list(values)
    n = len(arr)
    reset_node_counter()

    yield StepState(
        action_type=ActionType.INFO,
        current_data=None,
        active_line=1,
        message=f"Bắt đầu xây dựng Cây phân đoạn (Segment Tree) tính tổng khoảng cho mảng: {arr}."
    )

    def _build(l, r):
        if l == r:
            node = SegmentTreeNode(l, r, arr[l])
            return node
        mid = (l + r) // 2
        left_child = _build(l, mid)
        right_child = _build(mid + 1, r)
        node = SegmentTreeNode(l, r, left_child.val + right_child.val, left_child, right_child)
        return node

    root = _build(0, n - 1)

    yield StepState(
        action_type=ActionType.BUILD_TREE,
        highlighted_indices=[root.id],
        current_data=root,
        active_line=6,
        message=f"Đã xây dựng xong Segment Tree. Gốc quản lý đoạn [0..{n-1}] với tổng = {root.val}."
    )

    # Simulate a range query [1..3]
    ql, qr = 1, min(3, n - 1)
    yield StepState(
        action_type=ActionType.VISIT_NODE,
        current_data=root,
        active_line=8,
        message=f"Mô phỏng truy vấn tổng đoạn Range Query [{ql}..{qr}] = {sum(arr[ql:qr+1])} trong O(log N)."
    )

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message="Mô phỏng Segment Tree hoàn tất!"
    )


def fenwick_tree_simulation(values):
    arr = list(values)[:10] if len(values) > 10 else list(values)
    n = len(arr)
    bit = [0] * (n + 1)

    yield StepState(
        action_type=ActionType.INFO,
        current_data=None,
        active_line=1,
        message=f"Bắt đầu xây dựng Cây Fenwick (Binary Indexed Tree - BIT) với {n} phần tử.",
        extra_info={"bit_array": list(bit), "original": list(arr)}
    )

    def _update(idx, val):
        i = idx + 1
        while i <= n:
            bit[i] += val
            i += i & (-i)

    for i, x in enumerate(arr):
        _update(i, x)
        yield StepState(
            action_type=ActionType.UPDATE_TREE,
            current_data=None,
            active_line=5,
            message=f"Cập nhật BIT: Thêm phần tử arr[{i}] = {x}. bit[] = {bit[1:]}",
            extra_info={"bit_array": list(bit[1:]), "original": list(arr)}
        )

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=None,
        active_line=1,
        message=f"Fenwick Tree hoàn tất! Cho phép tính tiền tố Prefix Sum O(log N).",
        extra_info={"bit_array": list(bit[1:]), "original": list(arr)}
    )


def b_tree_simulation(values):
    reset_node_counter()
    root = BTreeNode(leaf=True)

    yield StepState(
        action_type=ActionType.INFO,
        current_data=root,
        active_line=1,
        message="Bắt đầu mô phỏng Cây B (B-Tree bậc 3): Mỗi nút có thể chứa tối đa 2 khóa trước khi tách."
    )

    for v in values:
        if len(root.keys) < 2:
            root.keys.append(v)
            root.keys.sort()
        else:
            # Demonstration of split
            mid_val = root.keys[1]
            new_root = BTreeNode(leaf=False)
            new_root.keys.append(mid_val)
            left_child = BTreeNode(leaf=True)
            left_child.keys.append(root.keys[0])
            right_child = BTreeNode(leaf=True)
            right_child.keys.append(v)
            new_root.children = [left_child, right_child]
            root = new_root

        yield StepState(
            action_type=ActionType.INSERT_NODE,
            highlighted_indices=[root.id],
            current_data=root,
            active_line=5,
            message=f"Chèn khóa {v} vào B-Tree."
        )

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message="Mô phỏng B-Tree hoàn tất!"
    )
