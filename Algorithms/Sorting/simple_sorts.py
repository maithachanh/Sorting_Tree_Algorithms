"""
Simple Comparison Sorting Algorithms: Bubble, Selection, Insertion, Interchange.
"""
from Algorithms.step_state import StepState, ActionType

def bubble_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=2,
        message=f"Bắt đầu thuật toán Bubble Sort với mảng có {n} phần tử.",
        comparisons=comparisons,
        swaps=swaps
    )

    for i in range(n - 1):
        yield StepState(
            action_type=ActionType.SUBARRAY,
            highlighted_indices=[n - i - 1],
            current_data=arr,
            active_line=3,
            message=f"Vòng lặp ngoài i = {i}: Đang duyệt tìm phần tử lớn nhất để đưa về vị trí {n - i - 1}.",
            comparisons=comparisons,
            swaps=swaps
        )
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            yield StepState(
                action_type=ActionType.COMPARE,
                highlighted_indices=[j, j + 1],
                current_data=arr,
                active_line=5,
                message=f"So sánh arr[{j}] = {arr[j]} với arr[{j+1}] = {arr[j+1]}.",
                comparisons=comparisons,
                swaps=swaps
            )

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
                yield StepState(
                    action_type=ActionType.SWAP,
                    highlighted_indices=[j, j + 1],
                    current_data=arr,
                    active_line=6,
                    message=f"Do {arr[j+1]} > {arr[j]}, tiến hành hoán đổi arr[{j}] và arr[{j+1}].",
                    comparisons=comparisons,
                    swaps=swaps
                )

        if not swapped:
            break

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Sắp xếp hoàn tất! Tổng cộng {comparisons} phép so sánh và {swaps} lần hoán đổi.",
        comparisons=comparisons,
        swaps=swaps
    )


def selection_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=2,
        message=f"Bắt đầu Selection Sort: Tìm phần tử nhỏ nhất đặt vào đầu mỗi dãy con.",
        comparisons=comparisons,
        swaps=swaps
    )

    for i in range(n - 1):
        min_idx = i
        yield StepState(
            action_type=ActionType.PIVOT,
            highlighted_indices=[min_idx],
            current_data=arr,
            active_line=4,
            message=f"Vòng lặp i = {i}: Tạm coi arr[{min_idx}] = {arr[min_idx]} là giá trị nhỏ nhất.",
            comparisons=comparisons,
            swaps=swaps
        )

        for j in range(i + 1, n):
            comparisons += 1
            yield StepState(
                action_type=ActionType.COMPARE,
                highlighted_indices=[j, min_idx],
                current_data=arr,
                active_line=6,
                message=f"So sánh phần tử đang xét arr[{j}] = {arr[j]} với min hiện tại arr[{min_idx}] = {arr[min_idx]}.",
                comparisons=comparisons,
                swaps=swaps
            )

            if arr[j] < arr[min_idx]:
                min_idx = j
                yield StepState(
                    action_type=ActionType.PIVOT,
                    highlighted_indices=[min_idx],
                    current_data=arr,
                    active_line=7,
                    message=f"Cập nhật vị trí nhỏ nhất mới min_idx = {min_idx} (giá trị = {arr[min_idx]}).",
                    comparisons=comparisons,
                    swaps=swaps
                )

        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
            yield StepState(
                action_type=ActionType.SWAP,
                highlighted_indices=[i, min_idx],
                current_data=arr,
                active_line=9,
                message=f"Hoán đổi phần tử nhỏ nhất arr[{min_idx}] về đúng vị trí arr[{i}].",
                comparisons=comparisons,
                swaps=swaps
            )

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Sắp xếp hoàn tất! Tổng cộng {comparisons} phép so sánh và {swaps} lần hoán đổi.",
        comparisons=comparisons,
        swaps=swaps
    )


def insertion_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[0],
        current_data=arr,
        active_line=2,
        message=f"Bắt đầu Insertion Sort: Coi phần tử arr[0] = {arr[0]} đã ở đúng vị trí.",
        comparisons=comparisons,
        swaps=swaps
    )

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        yield StepState(
            action_type=ActionType.PIVOT,
            highlighted_indices=[i],
            current_data=arr,
            active_line=4,
            message=f"Lấy phần tử khóa key = arr[{i}] = {key} để chèn vào dãy đã sắp xếp bên trái.",
            comparisons=comparisons,
            swaps=swaps
        )

        while j >= 0:
            comparisons += 1
            yield StepState(
                action_type=ActionType.COMPARE,
                highlighted_indices=[j, j + 1],
                current_data=arr,
                active_line=6,
                message=f"So sánh arr[{j}] = {arr[j]} với key = {key}.",
                comparisons=comparisons,
                swaps=swaps
            )

            if arr[j] > key:
                arr[j + 1] = arr[j]
                swaps += 1
                yield StepState(
                    action_type=ActionType.OVERWRITE,
                    highlighted_indices=[j + 1],
                    current_data=arr,
                    active_line=7,
                    message=f"Do {arr[j]} > {key}, dời arr[{j}] sang phải vị trí {j+1}.",
                    comparisons=comparisons,
                    swaps=swaps
                )
                j -= 1
            else:
                break

        arr[j + 1] = key
        yield StepState(
            action_type=ActionType.SORTED,
            highlighted_indices=[j + 1],
            current_data=arr,
            active_line=9,
            message=f"Chèn key = {key} vào vị trí thích hợp arr[{j+1}].",
            comparisons=comparisons,
            swaps=swaps
        )

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Sắp xếp hoàn tất! Tổng cộng {comparisons} phép so sánh và {swaps} lần dịch chuyển.",
        comparisons=comparisons,
        swaps=swaps
    )


def interchange_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=2,
        message=f"Bắt đầu Interchange Sort (Sắp xếp đổi chỗ trực tiếp).",
        comparisons=comparisons,
        swaps=swaps
    )

    for i in range(n - 1):
        for j in range(i + 1, n):
            comparisons += 1
            yield StepState(
                action_type=ActionType.COMPARE,
                highlighted_indices=[i, j],
                current_data=arr,
                active_line=5,
                message=f"So sánh arr[{i}] = {arr[i]} với arr[{j}] = {arr[j]}.",
                comparisons=comparisons,
                swaps=swaps
            )

            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
                swaps += 1
                yield StepState(
                    action_type=ActionType.SWAP,
                    highlighted_indices=[i, j],
                    current_data=arr,
                    active_line=6,
                    message=f"Do arr[{i}] > arr[{j}], đổi chỗ ngay lập tức ({arr[j]} <-> {arr[i]}).",
                    comparisons=comparisons,
                    swaps=swaps
                )

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=f"Sắp xếp hoàn tất! Tổng cộng {comparisons} phép so sánh và {swaps} lần hoán đổi.",
        comparisons=comparisons,
        swaps=swaps
    )
