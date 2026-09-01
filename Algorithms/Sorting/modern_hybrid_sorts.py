"""
Modern Hybrid Sorting: Tim Sort, Intro Sort, Block Sort.
"""
from Algorithms.step_state import StepState, ActionType
import math

def tim_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = [0]
    swaps = [0]
    min_run = 4

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message=f"Bắt đầu Tim Sort (Chuẩn hóa của Python/Java): Chia các Run nhỏ (size={min_run}) rồi trộn lại.",
        comparisons=comparisons[0],
        swaps=swaps[0]
    )

    # Insertion sort on small runs
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        for i in range(start + 1, end + 1):
            key = arr[i]
            j = i - 1
            while j >= start:
                comparisons[0] += 1
                yield StepState(
                    action_type=ActionType.COMPARE,
                    highlighted_indices=[j, j + 1],
                    current_data=arr,
                    active_line=5,
                    message=f"[Run {start}..{end}] So sánh arr[{j}] = {arr[j]} với key = {key}.",
                    comparisons=comparisons[0],
                    swaps=swaps[0]
                )
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    swaps[0] += 1
                    j -= 1
                else:
                    break
            arr[j + 1] = key
            yield StepState(
                action_type=ActionType.OVERWRITE,
                highlighted_indices=[j + 1],
                current_data=arr,
                active_line=8,
                message=f"[Run {start}..{end}] Chèn key = {key} vào vị trí arr[{j+1}].",
                comparisons=comparisons[0],
                swaps=swaps[0]
            )

    # Merge runs
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min(left + 2 * size - 1, n - 1)

            if mid < right:
                # Merge sublists
                L = arr[left:mid + 1]
                R = arr[mid + 1:right + 1]
                i = 0
                j = 0
                k = left

                while i < len(L) and j < len(R):
                    comparisons[0] += 1
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
                        active_line=14,
                        message=f"Trộn các Run [{left}..{mid}] và [{mid+1}..{right}] vào arr[{k}] = {arr[k]}.",
                        comparisons=comparisons[0],
                        swaps=swaps[0]
                    )
                    k += 1

                while i < len(L):
                    arr[k] = L[i]
                    i += 1
                    swaps[0] += 1
                    k += 1

                while j < len(R):
                    arr[k] = R[j]
                    j += 1
                    swaps[0] += 1
                    k += 1

        size = 2 * size

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Tim Sort hoàn tất! So sánh: {comparisons[0]}, Ghi đè: {swaps[0]}.",
        comparisons=comparisons[0],
        swaps=swaps[0]
    )


def intro_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = [0]
    swaps = [0]
    max_depth = 2 * math.floor(math.log2(n)) if n > 0 else 0

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message=f"Bắt đầu Intro Sort (QuickSort -> HeapSort khi đệ quy quá sâu depth={max_depth} -> InsertionSort khi mảng nhỏ).",
        comparisons=comparisons[0],
        swaps=swaps[0]
    )

    def _heap_sort_subarray(start, end):
        count = end - start + 1
        for i in range(count // 2 - 1, -1, -1):
            _sift_down(start, count, i)
        for i in range(count - 1, 0, -1):
            arr[start], arr[start + i] = arr[start + i], arr[start]
            swaps[0] += 1
            _sift_down(start, i, 0)

    def _sift_down(start, count, root_idx):
        largest = root_idx
        left = 2 * root_idx + 1
        right = 2 * root_idx + 2
        if left < count and arr[start + left] > arr[start + largest]:
            largest = left
        if right < count and arr[start + right] > arr[start + largest]:
            largest = right
        if largest != root_idx:
            arr[start + root_idx], arr[start + largest] = arr[start + largest], arr[start + root_idx]
            swaps[0] += 1
            _sift_down(start, count, largest)

    def _insertion_sort_subarray(start, end):
        for i in range(start + 1, end + 1):
            key = arr[i]
            j = i - 1
            while j >= start and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                swaps[0] += 1
            arr[j + 1] = key

    def _introsort_util(start, end, depth_limit):
        size = end - start + 1
        if size <= 6:
            yield StepState(
                action_type=ActionType.SUBARRAY,
                highlighted_indices=list(range(start, end + 1)),
                current_data=arr,
                active_line=6,
                message=f"Kích thước đoạn nhỏ ({size} <= 6), chuyển sang Insertion Sort.",
                comparisons=comparisons[0],
                swaps=swaps[0]
            )
            _insertion_sort_subarray(start, end)
            return

        if depth_limit == 0:
            yield StepState(
                action_type=ActionType.SUBARRAY,
                highlighted_indices=list(range(start, end + 1)),
                current_data=arr,
                active_line=8,
                message=f"Độ sâu đệ quy chạm giới hạn, chuyển sang Heap Sort để đảm bảo O(N log N).",
                comparisons=comparisons[0],
                swaps=swaps[0]
            )
            _heap_sort_subarray(start, end)
            return

        # QuickSort partition
        pivot = arr[end]
        i = start - 1
        for j in range(start, end):
            comparisons[0] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                swaps[0] += 1
                yield StepState(
                    action_type=ActionType.SWAP,
                    highlighted_indices=[i, j],
                    current_data=arr,
                    active_line=12,
                    message=f"QuickSort partition: Hoán đổi arr[{i}] và arr[{j}].",
                    comparisons=comparisons[0],
                    swaps=swaps[0]
                )
        arr[i + 1], arr[end] = arr[end], arr[i + 1]
        p_idx = i + 1

        yield from _introsort_util(start, p_idx - 1, depth_limit - 1)
        yield from _introsort_util(p_idx + 1, end, depth_limit - 1)

    yield from _introsort_util(0, n - 1, max_depth)

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Intro Sort hoàn tất!",
        comparisons=comparisons[0],
        swaps=swaps[0]
    )


def block_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = [0]
    swaps = [0]
    block_size = max(2, int(math.isqrt(n)))

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message=f"Bắt đầu Block Sort (Chia mảng thành các khối kích thước block = {block_size}).",
        comparisons=comparisons[0],
        swaps=swaps[0]
    )

    # Sort each individual block with insertion sort
    for start in range(0, n, block_size):
        end = min(start + block_size - 1, n - 1)
        for i in range(start + 1, end + 1):
            key = arr[i]
            j = i - 1
            while j >= start and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                swaps[0] += 1
            arr[j + 1] = key
        yield StepState(
            action_type=ActionType.SUBARRAY,
            highlighted_indices=list(range(start, end + 1)),
            current_data=arr,
            active_line=5,
            message=f"Đã sắp xếp khối [{start}..{end}].",
            comparisons=comparisons[0],
            swaps=swaps[0]
        )

    # Merge blocks in pairs
    size = block_size
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min(left + 2 * size - 1, n - 1)
            if mid < right:
                L = arr[left:mid + 1]
                R = arr[mid + 1:right + 1]
                i = 0
                j = 0
                k = left
                while i < len(L) and j < len(R):
                    if L[i] <= R[j]:
                        arr[k] = L[i]
                        i += 1
                    else:
                        arr[k] = R[j]
                        j += 1
                    swaps[0] += 1
                    k += 1
                while i < len(L):
                    arr[k] = L[i]
                    i += 1
                    swaps[0] += 1
                    k += 1
                while j < len(R):
                    arr[k] = R[j]
                    j += 1
                    swaps[0] += 1
                    k += 1
                yield StepState(
                    action_type=ActionType.OVERWRITE,
                    highlighted_indices=list(range(left, right + 1)),
                    current_data=arr,
                    active_line=11,
                    message=f"Trộn các khối liên kề [{left}..{mid}] và [{mid+1}..{right}].",
                    comparisons=comparisons[0],
                    swaps=swaps[0]
                )
        size *= 2

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Block Sort hoàn tất!",
        comparisons=comparisons[0],
        swaps=swaps[0]
    )
