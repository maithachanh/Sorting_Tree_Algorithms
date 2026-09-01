"""
Sorting Networks: Bitonic Sort with Power-of-2 Padding for Arbitrary Lengths.
"""
from Algorithms.step_state import StepState, ActionType
import math

def bitonic_sort(arr_input):
    orig_n = len(arr_input)
    if orig_n <= 1:
        return

    # Pad to nearest power of 2
    next_pow2 = 1 << (orig_n - 1).bit_length()
    pad_count = next_pow2 - orig_n
    arr = list(arr_input) + [float('inf')] * pad_count

    comparisons = [0]
    swaps = [0]

    yield StepState(
        action_type=ActionType.INFO,
        highlighted_indices=[],
        current_data=arr[:orig_n],
        active_line=1,
        message=f"Bắt đầu Bitonic Sort (Mạng sắp xếp song song, đệm lên kích thước lũy thừa 2 = {next_pow2}).",
        comparisons=comparisons[0],
        swaps=swaps[0]
    )

    def _comp_and_swap(i, j, dire):
        if i >= next_pow2 or j >= next_pow2:
            return

        comparisons[0] += 1
        swapped = False
        if (dire == 1 and arr[i] > arr[j]) or (dire == 0 and arr[i] < arr[j]):
            arr[i], arr[j] = arr[j], arr[i]
            swaps[0] += 1
            swapped = True

        # Only yield visible steps within original array range
        if i < orig_n or j < orig_n:
            high_idx = [idx for idx in [i, j] if idx < orig_n]
            if swapped:
                yield StepState(
                    action_type=ActionType.SWAP,
                    highlighted_indices=high_idx,
                    current_data=arr[:orig_n],
                    active_line=4,
                    message=f"Bitonic Compare & Swap: Đổi chỗ tại chỉ số {i} và {j}.",
                    comparisons=comparisons[0],
                    swaps=swaps[0]
                )
            else:
                yield StepState(
                    action_type=ActionType.COMPARE,
                    highlighted_indices=high_idx,
                    current_data=arr[:orig_n],
                    active_line=6,
                    message=f"Bitonic Compare: Đã đúng chiều thứ tự mong muốn ({'Tăng' if dire==1 else 'Giảm'}).",
                    comparisons=comparisons[0],
                    swaps=swaps[0]
                )

    def _bitonic_merge(low, cnt, dire):
        if cnt > 1:
            k = cnt // 2
            for i in range(low, low + k):
                yield from _comp_and_swap(i, i + k, dire)
            yield from _bitonic_merge(low, k, dire)
            yield from _bitonic_merge(low + k, k, dire)

    def _bitonic_sort_rec(low, cnt, dire):
        if cnt > 1:
            k = cnt // 2
            # Sắp xếp nửa đầu tăng dần
            yield from _bitonic_sort_rec(low, k, 1)
            # Sắp xếp nửa sau giảm dần
            yield from _bitonic_sort_rec(low + k, k, 0)
            # Trộn bitonic
            yield from _bitonic_merge(low, cnt, dire)

    yield from _bitonic_sort_rec(0, next_pow2, 1)

    # Trim padding back to original size
    final_arr = [int(x) if isinstance(x, (int, float)) and x != float('inf') else x for x in arr[:orig_n]]

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=list(range(orig_n)),
        current_data=final_arr,
        active_line=1,
        message=f"Bitonic Sort hoàn tất! So sánh: {comparisons[0]}, Hoán đổi: {swaps[0]}.",
        comparisons=comparisons[0],
        swaps=swaps[0]
    )
