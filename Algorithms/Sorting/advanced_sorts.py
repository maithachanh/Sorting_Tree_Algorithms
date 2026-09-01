"""
Advanced Sorting Algorithms: Quick Sort, Merge Sort, Heap Sort, Shell Sort, Tree Sort.
"""
from Algorithms.step_state import StepState, ActionType

def quick_sort(arr_input):
    arr = list(arr_input)
    comparisons = [0]
    swaps = [0]

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message="Bắt đầu Quick Sort (Chia để trị bằng phần tử chốt Pivot).",
        comparisons=comparisons[0],
        swaps=swaps[0]
    )

    def _quick_sort_step(low, high):
        if low < high:
            yield StepState(
                action_type=ActionType.SUBARRAY,
                highlighted_indices=list(range(low, high + 1)),
                current_data=arr,
                active_line=3,
                message=f"Xét đoạn con từ chỉ số {low} đến {high}.",
                comparisons=comparisons[0],
                swaps=swaps[0]
            )

            # Lomuto partition
            pivot = arr[high]
            i = low - 1
            yield StepState(
                action_type=ActionType.PIVOT,
                highlighted_indices=[high],
                current_data=arr,
                active_line=6,
                message=f"Chọn phần tử chốt pivot = arr[{high}] = {pivot}.",
                comparisons=comparisons[0],
                swaps=swaps[0]
            )

            for j in range(low, high):
                comparisons[0] += 1
                yield StepState(
                    action_type=ActionType.COMPARE,
                    highlighted_indices=[j, high],
                    current_data=arr,
                    active_line=8,
                    message=f"So sánh arr[{j}] = {arr[j]} với pivot {pivot}.",
                    comparisons=comparisons[0],
                    swaps=swaps[0]
                )

                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    swaps[0] += 1
                    yield StepState(
                        action_type=ActionType.SWAP,
                        highlighted_indices=[i, j],
                        current_data=arr,
                        active_line=10,
                        message=f"Hoán đổi arr[{i}] và arr[{j}] để gom các phần tử <= {pivot} về bên trái.",
                        comparisons=comparisons[0],
                        swaps=swaps[0]
                    )

            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            swaps[0] += 1
            p_idx = i + 1
            yield StepState(
                action_type=ActionType.SORTED,
                highlighted_indices=[p_idx],
                current_data=arr,
                active_line=11,
                message=f"Đặt pivot về vị trí chính xác tại chỉ số {p_idx}.",
                comparisons=comparisons[0],
                swaps=swaps[0]
            )

            yield from _quick_sort_step(low, p_idx - 1)
            yield from _quick_sort_step(p_idx + 1, high)

    yield from _quick_sort_step(0, len(arr) - 1)

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(len(arr))),
        current_data=arr,
        active_line=1,
        message=f"Quick Sort hoàn tất! So sánh: {comparisons[0]}, Hoán đổi: {swaps[0]}.",
        comparisons=comparisons[0],
        swaps=swaps[0]
    )


def merge_sort(arr_input):
    arr = list(arr_input)
    comparisons = [0]
    swaps = [0]

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message="Bắt đầu Merge Sort (Chia đôi mảng và Trộn có thứ tự).",
        comparisons=comparisons[0],
        swaps=swaps[0]
    )

    def _merge_sort_step(left, right):
        if left < right:
            mid = (left + right) // 2
            yield StepState(
                action_type=ActionType.SUBARRAY,
                highlighted_indices=list(range(left, right + 1)),
                current_data=arr,
                active_line=3,
                message=f"Chia đoạn [{left}..{right}] thành [{left}..{mid}] và [{mid+1}..{right}].",
                comparisons=comparisons[0],
                swaps=swaps[0]
            )

            yield from _merge_sort_step(left, mid)
            yield from _merge_sort_step(mid + 1, right)

            # Merge in-place / auxiliary
            yield StepState(
                action_type=ActionType.INFO,
                highlighted_indices=list(range(left, right + 1)),
                current_data=arr,
                active_line=7,
                message=f"Bắt đầu trộn 2 nửa đã sắp: [{left}..{mid}] và [{mid+1}..{right}].",
                comparisons=comparisons[0],
                swaps=swaps[0]
            )

            L = arr[left:mid + 1]
            R = arr[mid + 1:right + 1]
            i = 0
            j = 0
            k = left

            while i < len(L) and j < len(R):
                comparisons[0] += 1
                yield StepState(
                    action_type=ActionType.COMPARE,
                    highlighted_indices=[k],
                    current_data=arr,
                    active_line=9,
                    message=f"So sánh phần tử {L[i]} từ nửa trái và {R[j]} từ nửa phải.",
                    comparisons=comparisons[0],
                    swaps=swaps[0]
                )

                if L[i] <= R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                swaps[0] += 1
                yield StepState(
                    action_type=ActionType.OVERWRITE,
                    highlighted_indices=[k],
                    current_data=arr,
                    active_line=11,
                    message=f"Ghi giá trị {arr[k]} vào vị trí kết quả arr[{k}].",
                    comparisons=comparisons[0],
                    swaps=swaps[0]
                )
                k += 1

            while i < len(L):
                arr[k] = L[i]
                i += 1
                swaps[0] += 1
                yield StepState(
                    action_type=ActionType.OVERWRITE,
                    highlighted_indices=[k],
                    current_data=arr,
                    active_line=13,
                    message=f"Lấy nốt phần tử còn lại {arr[k]} từ nửa trái vào arr[{k}].",
                    comparisons=comparisons[0],
                    swaps=swaps[0]
                )
                k += 1

            while j < len(R):
                arr[k] = R[j]
                j += 1
                swaps[0] += 1
                yield StepState(
                    action_type=ActionType.OVERWRITE,
                    highlighted_indices=[k],
                    current_data=arr,
                    active_line=15,
                    message=f"Lấy nốt phần tử còn lại {arr[k]} từ nửa phải vào arr[{k}].",
                    comparisons=comparisons[0],
                    swaps=swaps[0]
                )
                k += 1

    yield from _merge_sort_step(0, len(arr) - 1)

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(len(arr))),
        current_data=arr,
        active_line=1,
        message=f"Merge Sort hoàn tất! So sánh: {comparisons[0]}, Ghi đè: {swaps[0]}.",
        comparisons=comparisons[0],
        swaps=swaps[0]
    )


def heap_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message="Bắt đầu Heap Sort: Bước 1 - Xây dựng Max-Heap từ mảng ban đầu.",
        comparisons=comparisons,
        swaps=swaps
    )

    def _heapify(size, root_idx):
        nonlocal comparisons, swaps
        largest = root_idx
        left = 2 * root_idx + 1
        right = 2 * root_idx + 2

        if left < size:
            comparisons += 1
            if arr[left] > arr[largest]:
                largest = left

        if right < size:
            comparisons += 1
            if arr[right] > arr[largest]:
                largest = right

        if largest != root_idx:
            arr[root_idx], arr[largest] = arr[largest], arr[root_idx]
            swaps += 1
            yield StepState(
                action_type=ActionType.SWAP,
                highlighted_indices=[root_idx, largest],
                current_data=arr,
                active_line=7,
                message=f"Vun đống (Heapify): Đổi chỗ arr[{root_idx}] với con lớn hơn arr[{largest}].",
                comparisons=comparisons,
                swaps=swaps
            )
            yield from _heapify(size, largest)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        yield from _heapify(n, i)

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[0],
        current_data=arr,
        active_line=10,
        message="Đã tạo xong Max Heap. Bước 2: Lần lượt đưa gốc (max) về cuối mảng và vun đống lại.",
        comparisons=comparisons,
        swaps=swaps
    )

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        swaps += 1
        yield StepState(
            action_type=ActionType.SWAP,
            highlighted_indices=[0, i],
            current_data=arr,
            active_line=12,
            message=f"Đưa phần tử lớn nhất arr[0] = {arr[i]} về vị trí cố định arr[{i}].",
            comparisons=comparisons,
            swaps=swaps
        )
        yield from _heapify(i, 0)

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Heap Sort hoàn tất! So sánh: {comparisons}, Hoán đổi: {swaps}.",
        comparisons=comparisons,
        swaps=swaps
    )


def shell_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0
    gap = n // 2

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message=f"Bắt đầu Shell Sort với khoảng cách khởi tạo gap = {gap}.",
        comparisons=comparisons,
        swaps=swaps
    )

    while gap > 0:
        yield StepState(
            action_type=ActionType.SUBARRAY,
            highlighted_indices=[],
            current_data=arr,
            active_line=4,
            message=f"Đang sắp xếp chèn cho các phần tử cách nhau gap = {gap}.",
            comparisons=comparisons,
            swaps=swaps
        )

        for i in range(gap, n):
            temp = arr[i]
            j = i
            yield StepState(
                action_type=ActionType.PIVOT,
                highlighted_indices=[i],
                current_data=arr,
                active_line=6,
                message=f"Lấy phần tử arr[{i}] = {temp} để chèn vào dãy cách khoảng {gap}.",
                comparisons=comparisons,
                swaps=swaps
            )

            while j >= gap:
                comparisons += 1
                yield StepState(
                    action_type=ActionType.COMPARE,
                    highlighted_indices=[j - gap, j],
                    current_data=arr,
                    active_line=8,
                    message=f"So sánh arr[{j - gap}] = {arr[j - gap]} với temp = {temp}.",
                    comparisons=comparisons,
                    swaps=swaps
                )

                if arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    swaps += 1
                    yield StepState(
                        action_type=ActionType.OVERWRITE,
                        highlighted_indices=[j],
                        current_data=arr,
                        active_line=9,
                        message=f"Dịch chuyển arr[{j - gap}] sang vị trí arr[{j}].",
                        comparisons=comparisons,
                        swaps=swaps
                    )
                    j -= gap
                else:
                    break

            arr[j] = temp
            yield StepState(
                action_type=ActionType.SORTED,
                highlighted_indices=[j],
                current_data=arr,
                active_line=11,
                message=f"Đặt temp = {temp} vào vị trí arr[{j}].",
                comparisons=comparisons,
                swaps=swaps
            )

        gap //= 2

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Shell Sort hoàn tất! So sánh: {comparisons}, Ghi đè: {swaps}.",
        comparisons=comparisons,
        swaps=swaps
    )


def tree_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message="Bắt đầu Tree Sort: Chèn các phần tử vào Cây nhị phân tìm kiếm (BST), sau đó duyệt In-order.",
        comparisons=comparisons,
        swaps=swaps
    )

    class Node:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None

    root = None

    def insert(node, key):
        nonlocal comparisons
        if node is None:
            return Node(key)
        comparisons += 1
        if key < node.val:
            node.left = insert(node.left, key)
        else:
            node.right = insert(node.right, key)
        return node

    for idx, x in enumerate(arr):
        root = insert(root, x)
        yield StepState(
            action_type=ActionType.PIVOT,
            highlighted_indices=[idx],
            current_data=arr,
            active_line=6,
            message=f"Chèn arr[{idx}] = {x} vào Cây nhị phân tìm kiếm.",
            comparisons=comparisons,
            swaps=swaps
        )

    # In-order traversal to overwrite array
    out_idx = 0
    def inorder(node):
        nonlocal out_idx, swaps
        if node:
            yield from inorder(node.left)
            arr[out_idx] = node.val
            swaps += 1
            yield StepState(
                action_type=ActionType.OVERWRITE,
                highlighted_indices=[out_idx],
                current_data=arr,
                active_line=10,
                message=f"Duyệt In-order (LNR): Trích xuất giá trị {node.val} đưa vào arr[{out_idx}].",
                comparisons=comparisons,
                swaps=swaps
            )
            out_idx += 1
            yield from inorder(node.right)

    yield from inorder(root)

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Tree Sort hoàn tất! So sánh: {comparisons}, Trích xuất: {swaps}.",
        comparisons=comparisons,
        swaps=swaps
    )
