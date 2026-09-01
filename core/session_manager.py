"""
Session Manager holding the current state of data and active algorithm across views.
"""
from config import DEFAULT_ARRAY, DEFAULT_TREE_ELEMENTS

class SessionManager:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = SessionManager()
        return cls._instance

    def __init__(self):
        self.sorting_array = list(DEFAULT_ARRAY)
        self.tree_elements = list(DEFAULT_TREE_ELEMENTS)
        self.current_category = "sorting"  # "sorting" or "tree"
        self.current_algorithm_key = "bubble_sort"
        self.current_algorithm_name = "Bubble Sort"
        self.algorithm_meta = {}

    def set_sorting_array(self, arr):
        self.sorting_array = list(arr)

    def set_tree_elements(self, elements):
        self.tree_elements = list(elements)

    def set_algorithm(self, category, key, name, meta=None):
        self.current_category = category
        self.current_algorithm_key = key
        self.current_algorithm_name = name
        self.algorithm_meta = meta or {}
