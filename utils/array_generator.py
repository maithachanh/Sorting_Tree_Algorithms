"""
Array generator and validator utility functions.
"""
import random

class ArrayGenerator:
    @staticmethod
    def generate_random(size=15, min_val=5, max_val=100, unique=False):
        """Generates a random list of integers."""
        if unique:
            count = min(size, max_val - min_val + 1)
            return random.sample(range(min_val, max_val + 1), count)
        return [random.randint(min_val, max_val) for _ in range(size)]

    @staticmethod
    def generate_reversed(size=15, min_val=5, max_val=100):
        """Generates a strictly reversed (descending) array."""
        arr = ArrayGenerator.generate_random(size, min_val, max_val, unique=True)
        arr.sort(reverse=True)
        return arr

    @staticmethod
    def generate_nearly_sorted(size=15, min_val=5, max_val=100, swaps=2):
        """Generates a nearly sorted array with a few random swaps."""
        arr = ArrayGenerator.generate_random(size, min_val, max_val, unique=True)
        arr.sort()
        for _ in range(swaps):
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    @staticmethod
    def generate_few_unique(size=15, min_val=10, max_val=50, num_unique=3):
        """Generates an array with few unique duplicate values."""
        unique_values = random.sample(range(min_val, max_val + 1), min(num_unique, max_val - min_val + 1))
        return [random.choice(unique_values) for _ in range(size)]

    @staticmethod
    def parse_user_input(text_str):
        """
        Parses a comma, space, or semicolon separated string into a list of integers.
        Returns (success: bool, result: list or error_message: str)
        """
        if not text_str or not text_str.strip():
            return False, "Chuỗi nhập vào không được để trống!"

        # Normalize delimiters
        cleaned = text_str.replace(',', ' ').replace(';', ' ').replace('|', ' ')
        tokens = cleaned.split()
        
        result = []
        for tok in tokens:
            try:
                val = int(tok)
                if val < 0 or val > 999:
                    return False, f"Giá trị {val} nằm ngoài phạm vi cho phép (0 - 999)."
                result.append(val)
            except ValueError:
                return False, f"'{tok}' không phải là một số nguyên hợp lệ."

        if len(result) < 2:
            return False, "Vui lòng nhập ít nhất 2 phần tử."
        if len(result) > 100:
            return False, "Số lượng phần tử tối đa để mô phỏng tốt nhất là 100."

        return True, result
