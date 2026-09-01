"""
Distribution / Non-Comparison Sorting: Counting Sort, Radix Sort, Bucket Sort, Bead Sort.
"""
from Algorithms.step_state import StepState, ActionType

def counting_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0

    if not arr:
        return

    max_val = max(arr)
    min_val = min(arr)
    k = max_val - min_val + 1

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message=f"Bắt đầu Counting Sort: Dải giá trị từ {min_val} đến {max_val} (kích thước bảng đếm = {k}).",
        comparisons=comparisons,
        swaps=swaps
    )

    count = [0] * k
    for i, x in enumerate(arr):
        count[x - min_val] += 1
        yield StepState(
            action_type=ActionType.MARK,
            highlighted_indices=[i],
            current_data=arr,
            active_line=4,
            message=f"Đếm tần suất: Tăng số lượng của phần tử {x} lên {count[x - min_val]}.",
            comparisons=comparisons,
            swaps=swaps
        )

    out_idx = 0
    for val_offset, freq in enumerate(count):
        val = val_offset + min_val
        for _ in range(freq):
            arr[out_idx] = val
            swaps += 1
            yield StepState(
                action_type=ActionType.OVERWRITE,
                highlighted_indices=[out_idx],
                current_data=arr,
                active_line=8,
                message=f"Đặt lại giá trị {val} vào vị trí arr[{out_idx}].",
                comparisons=comparisons,
                swaps=swaps
            )
            out_idx += 1

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Counting Sort hoàn tất! Thời gian O(N + K) với {swaps} lần ghi.",
        comparisons=comparisons,
        swaps=swaps
    )


def radix_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0

    if not arr:
        return

    max_val = max(arr)
    exp = 1

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message=f"Bắt đầu Radix Sort (LSD): Sắp xếp lần lượt theo từng chữ số từ hàng đơn vị.",
        comparisons=comparisons,
        swaps=swaps
    )

    while max_val // exp > 0:
        digit_name = "hàng đơn vị" if exp == 1 else ("hàng chục" if exp == 10 else f"hàng {exp}")
        yield StepState(
            action_type=ActionType.INFO,
            highlighted_indices=[],
            current_data=arr,
            active_line=3,
            message=f"Đang gom nhóm và sắp xếp theo {digit_name} (exp = {exp}).",
            comparisons=comparisons,
            swaps=swaps
        )

        output = [0] * n
        count = [0] * 10

        for i in range(n):
            digit = (arr[i] // exp) % 10
            count[digit] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            digit = (arr[i] // exp) % 10
            pos = count[digit] - 1
            output[pos] = arr[i]
            count[digit] -= 1

        for i in range(n):
            arr[i] = output[i]
            swaps += 1
            yield StepState(
                action_type=ActionType.OVERWRITE,
                highlighted_indices=[i],
                current_data=arr,
                active_line=8,
                message=f"Cập nhật arr[{i}] = {arr[i]} sau khi ổn định chữ số {digit_name}.",
                comparisons=comparisons,
                swaps=swaps
            )

        exp *= 10

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Radix Sort hoàn tất! Độ phức tạp O(d * (n + k)).",
        comparisons=comparisons,
        swaps=swaps
    )


def bucket_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0

    if n <= 1:
        return

    max_val = max(arr)
    min_val = min(arr)
    bucket_count = max(3, min(n, 10))

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message=f"Bắt đầu Bucket Sort: Phân phối phần tử vào {bucket_count} xô (Buckets).",
        comparisons=comparisons,
        swaps=swaps
    )

    buckets = [[] for _ in range(bucket_count)]
    range_span = (max_val - min_val + 1) / bucket_count

    for i, x in enumerate(arr):
        b_idx = min(int((x - min_val) / range_span), bucket_count - 1)
        buckets[b_idx].append(x)
        yield StepState(
            action_type=ActionType.MARK,
            highlighted_indices=[i],
            current_data=arr,
            active_line=5,
            message=f"Phần tử arr[{i}] = {x} được xếp vào Xô số #{b_idx + 1}.",
            comparisons=comparisons,
            swaps=swaps
        )

    # Sort each bucket and place back
    out_idx = 0
    for b_idx, b in enumerate(buckets):
        b.sort()
        for val in b:
            arr[out_idx] = val
            swaps += 1
            yield StepState(
                action_type=ActionType.OVERWRITE,
                highlighted_indices=[out_idx],
                current_data=arr,
                active_line=9,
                message=f"Đổ các phần tử từ Xô #{b_idx + 1} về mảng: arr[{out_idx}] = {val}.",
                comparisons=comparisons,
                swaps=swaps
            )
            out_idx += 1

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Bucket Sort hoàn tất!",
        comparisons=comparisons,
        swaps=swaps
    )


def bead_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0

    if any(x < 0 for x in arr):
        # Bead sort only for non-negative
        return

    max_val = max(arr) if arr else 0

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message=f"Bắt đầu Bead Sort (Gravity Sort - Sắp xếp trọng lực hạt bàn tính).",
        comparisons=comparisons,
        swaps=swaps
    )

    # Grid of beads
    grid = [[False] * max_val for _ in range(n)]
    for i, x in enumerate(arr):
        for j in range(x):
            grid[i][j] = True

    # Drop beads
    for j in range(max_val):
        count = sum(grid[i][j] for i in range(n))
        for i in range(n - count):
            grid[i][j] = False
        for i in range(n - count, n):
            grid[i][j] = True

    # Read result
    for i in range(n):
        new_val = sum(grid[i])
        arr[i] = new_val
        swaps += 1
        yield StepState(
            action_type=ActionType.OVERWRITE,
            highlighted_indices=[i],
            current_data=arr,
            active_line=7,
            message=f"Hạt rơi xuống: Hàng {i} có {new_val} hạt -> arr[{i}] = {new_val}.",
            comparisons=comparisons,
            swaps=swaps
        )

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Bead Sort (Gravity Sort) hoàn tất!",
        comparisons=comparisons,
        swaps=swaps
    )
