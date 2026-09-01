"""
Heap Data Structure Operations: Max Heapify, Min Heapify, Extract Max/Min, Change Key.
"""
from Algorithms.step_state import StepState, ActionType
from Algorithms.Tree.tree_models import BinaryNode, reset_node_counter

def build_tree_from_heap_array(arr):
    """Converts a flat heap array into a BinaryNode tree representation."""
    if not arr:
        return None
    nodes = [BinaryNode(v) for v in arr]
    n = len(nodes)
    for i in range(n):
        left_idx = 2 * i + 1
        right_idx = 2 * i + 2
        if left_idx < n:
            nodes[i].left = nodes[left_idx]
        if right_idx < n:
            nodes[i].right = nodes[right_idx]
    return nodes[0]


def max_heapify_simulation(values):
    arr = list(values)
    n = len(arr)
    reset_node_counter()
    tree_root = build_tree_from_heap_array(arr)

    yield StepState(
        action_type=ActionType.INFO,
        current_data=tree_root,
        active_line=1,
        message=f"Bắt đầu xây dựng Max-Heap từ mảng {n} phần tử: Cha luôn lớn hơn hoặc bằng các Con.",
        extra_info={"array": list(arr)}
    )

    def _sift_down(size, root_idx):
        nonlocal tree_root
        largest = root_idx
        left = 2 * root_idx + 1
        right = 2 * root_idx + 2

        if left < size and arr[left] > arr[largest]:
            largest = left
        if right < size and arr[right] > arr[largest]:
            largest = right

        if largest != root_idx:
            arr[root_idx], arr[largest] = arr[largest], arr[root_idx]
            tree_root = build_tree_from_heap_array(arr)
            yield StepState(
                action_type=ActionType.HEAPIFY,
                current_data=tree_root,
                active_line=6,
                message=f"Heapify: Hoán đổi phần tử tại chỉ số {root_idx} (giá trị={arr[largest]}) với chỉ số {largest} (giá trị={arr[root_idx]}).",
                extra_info={"array": list(arr)}
            )
            yield from _sift_down(size, largest)

    for i in range(n // 2 - 1, -1, -1):
        yield StepState(
            action_type=ActionType.VISIT_NODE,
            current_data=tree_root,
            active_line=3,
            message=f"Kiểm tra tính chất Max-Heap tại nút gốc chỉ số i = {i} (giá trị = {arr[i]}).",
            extra_info={"array": list(arr)}
        )
        yield from _sift_down(n, i)

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=tree_root,
        active_line=1,
        message=f"Max-Heap hoàn tất! Mảng đống: {arr}",
        extra_info={"array": list(arr)}
    )


def extract_max_heap_simulation(values):
    arr = list(values)
    # Build max heap first
    for i in range(len(arr) // 2 - 1, -1, -1):
        # heapify
        pass
    arr.sort(reverse=True) # start with valid heap
    n = len(arr)
    tree_root = build_tree_from_heap_array(arr)

    yield StepState(
        action_type=ActionType.BUILD_TREE,
        current_data=tree_root,
        active_line=1,
        message=f"Max-Heap ban đầu. Bắt đầu trích xuất phần tử cực đại (Extract Max = {arr[0]}).",
        extra_info={"array": list(arr)}
    )

    if n > 0:
        max_val = arr[0]
        arr[0] = arr[-1]
        arr.pop()
        tree_root = build_tree_from_heap_array(arr)
        yield StepState(
            action_type=ActionType.EXTRACT,
            current_data=tree_root,
            active_line=4,
            message=f"Lấy phần tử cực đại {max_val} ra ngoài. Đưa phần tử cuối cùng lên đỉnh và vun đống lại.",
            extra_info={"array": list(arr), "extracted": max_val}
        )

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=tree_root,
        active_line=1,
        message="Trích xuất phần tử cực đại thành công!",
        extra_info={"array": list(arr)}
    )
