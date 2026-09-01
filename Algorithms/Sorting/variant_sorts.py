"""
Variant Sorting Algorithms: Shaker (Cocktail) Sort, Comb Sort, Gnome Sort.
"""
from Algorithms.step_state import StepState, ActionType

def shaker_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0
    start = 0
    end = n - 1
    swapped = True

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message="Bắt đầu Shaker Sort (Cocktail Sort - Nổi bọt 2 chiều trái sang phải và phải sang trái).",
        comparisons=comparisons,
        swaps=swaps
    )

    while swapped:
        swapped = False

        # Forward pass (Trái sang phải)
        for i in range(start, end):
            comparisons += 1
            yield StepState(
                action_type=ActionType.COMPARE,
                highlighted_indices=[i, i + 1],
                current_data=arr,
                active_line=5,
                message=f"Lượt đi (Phải): So sánh arr[{i}] = {arr[i]} và arr[{i+1}] = {arr[i+1]}.",
                comparisons=comparisons,
                swaps=swaps
            )

            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swaps += 1
                swapped = True
                yield StepState(
                    action_type=ActionType.SWAP,
                    highlighted_indices=[i, i + 1],
                    current_data=arr,
                    active_line=6,
                    message=f"Hoán đổi arr[{i}] và arr[{i+1}].",
                    comparisons=comparisons,
                    swaps=swaps
                )

        if not swapped:
            break

        swapped = False
        end -= 1

        # Backward pass (Phải sang trái)
        for i in range(end - 1, start - 1, -1):
            comparisons += 1
            yield StepState(
                action_type=ActionType.COMPARE,
                highlighted_indices=[i, i + 1],
                current_data=arr,
                active_line=9,
                message=f"Lượt về (Trái): So sánh arr[{i}] = {arr[i]} và arr[{i+1}] = {arr[i+1]}.",
                comparisons=comparisons,
                swaps=swaps
            )

            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swaps += 1
                swapped = True
                yield StepState(
                    action_type=ActionType.SWAP,
                    highlighted_indices=[i, i + 1],
                    current_data=arr,
                    active_line=10,
                    message=f"Hoán đổi arr[{i}] và arr[{i+1}].",
                    comparisons=comparisons,
                    swaps=swaps
                )

        start += 1

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Shaker Sort hoàn tất! So sánh: {comparisons}, Hoán đổi: {swaps}.",
        comparisons=comparisons,
        swaps=swaps
    )


def comb_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0
    gap = n
    shrink = 1.3
    sorted_flag = False

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message="Bắt đầu Comb Sort (Cải tiến Bubble Sort bằng cách thu hẹp khoảng cách gap theo tỉ lệ 1.3).",
        comparisons=comparisons,
        swaps=swaps
    )

    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True

        yield StepState(
            action_type=ActionType.SUBARRAY,
            highlighted_indices=[],
            current_data=arr,
            active_line=4,
            message=f"Thu hẹp khoảng cách so sánh gap = {gap}.",
            comparisons=comparisons,
            swaps=swaps
        )

        for i in range(0, n - gap):
            comparisons += 1
            yield StepState(
                action_type=ActionType.COMPARE,
                highlighted_indices=[i, i + gap],
                current_data=arr,
                active_line=6,
                message=f"So sánh arr[{i}] = {arr[i]} và arr[{i+gap}] = {arr[i+gap]}.",
                comparisons=comparisons,
                swaps=swaps
            )

            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swaps += 1
                sorted_flag = False
                yield StepState(
                    action_type=ActionType.SWAP,
                    highlighted_indices=[i, i + gap],
                    current_data=arr,
                    active_line=7,
                    message=f"Hoán đổi arr[{i}] và arr[{i+gap}].",
                    comparisons=comparisons,
                    swaps=swaps
                )

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Comb Sort hoàn tất! So sánh: {comparisons}, Hoán đổi: {swaps}.",
        comparisons=comparisons,
        swaps=swaps
    )


def gnome_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0
    idx = 0

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[0],
        current_data=arr,
        active_line=1,
        message="Bắt đầu Gnome Sort: Nếu đúng thứ tự tiến lên 1 bước, nếu sai thứ tự đổi chỗ và lùi lại 1 bước.",
        comparisons=comparisons,
        swaps=swaps
    )

    while idx < n:
        if idx == 0:
            idx += 1

        comparisons += 1
        yield StepState(
            action_type=ActionType.COMPARE,
            highlighted_indices=[idx - 1, idx],
            current_data=arr,
            active_line=5,
            message=f"So sánh arr[{idx-1}] = {arr[idx-1]} và arr[{idx}] = {arr[idx]}.",
            comparisons=comparisons,
            swaps=swaps
        )

        if arr[idx] >= arr[idx - 1]:
            idx += 1
            yield StepState(
                action_type=ActionType.SUBARRAY,
                highlighted_indices=[idx - 1] if idx <= n else [],
                current_data=arr,
                active_line=6,
                message=f"Đúng thứ tự, chú lùn (Gnome) tiến lên chỉ số {idx}.",
                comparisons=comparisons,
                swaps=swaps
            )
        else:
            arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]
            swaps += 1
            yield StepState(
                action_type=ActionType.SWAP,
                highlighted_indices=[idx - 1, idx],
                current_data=arr,
                active_line=8,
                message=f"Sai thứ tự! Đổi chỗ arr[{idx-1}] và arr[{idx}], lùi lại chỉ số {idx-1}.",
                comparisons=comparisons,
                swaps=swaps
            )
            idx -= 1

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Gnome Sort hoàn tất! So sánh: {comparisons}, Hoán đổi: {swaps}.",
        comparisons=comparisons,
        swaps=swaps
    )
