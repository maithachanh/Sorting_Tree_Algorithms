"""
Esoteric Sorting: Bogo Sort (Stupid Sort).
"""
from Algorithms.step_state import StepState, ActionType
import random

def bogo_sort(arr_input):
    arr = list(arr_input)
    n = len(arr)
    comparisons = 0
    swaps = 0
    max_tries = 100

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr,
        active_line=1,
        message="Bắt đầu Bogo Sort (Xáo trộn ngẫu nhiên liên tục cho đến khi may mắn mảng tự tăng dần).",
        comparisons=comparisons,
        swaps=swaps
    )

    def is_sorted():
        nonlocal comparisons
        for i in range(n - 1):
            comparisons += 1
            if arr[i] > arr[i + 1]:
                return False
        return True

    tries = 0
    while not is_sorted() and tries < max_tries:
        tries += 1
        random.shuffle(arr)
        swaps += 1
        yield StepState(
            action_type=ActionType.SWAP,
            highlighted_indices=list(range(n)),
            current_data=arr,
            active_line=5,
            message=f"Lần thử #{tries}: Xáo trộn toàn bộ mảng ngẫu nhiên!",
            comparisons=comparisons,
            swaps=swaps
        )

    if is_sorted():
        msg = f"Thần kỳ! Bogo Sort đã thành công sau {tries} lần thử!"
    else:
        msg = f"Dừng Bogo Sort sau {max_tries} lần thử để tránh lặp vô tận (Độ phức tạp O((N+1)!))."

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(n)),
        current_data=arr,
        active_line=1,
        message=msg,
        comparisons=comparisons,
        swaps=swaps
    )
