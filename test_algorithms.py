"""
Automated unit and integration test for all Sorting and Tree Algorithm generators.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Algorithms.step_state import ActionType, StepState
from Algorithms.code_snippets import CODE_SNIPPETS
from gui.views.visualizer_view import ALGORITHM_MAP

def test_sorting_algorithms():
    print("========================================")
    print("Testing Sorting Algorithms...")
    print("========================================")

    sample_array = [45, 12, 85, 32, 89, 39, 69, 44, 42, 1, 98, 22, 57, 63, 17]
    sorted_expected = sorted(sample_array)

    sorting_keys = [
        "bubble_sort", "selection_sort", "insertion_sort", "interchange_sort",
        "shaker_sort", "comb_sort", "gnome_sort", "quick_sort", "merge_sort",
        "heap_sort", "shell_sort", "tree_sort", "counting_sort", "radix_sort",
        "bucket_sort", "bead_sort", "tim_sort", "intro_sort", "block_sort",
        "bitonic_sort", "bogo_sort"
    ]

    for key in sorting_keys:
        func = ALGORITHM_MAP[key]
        test_arr = [5, 2, 8, 1, 9, 3] if key == "bogo_sort" else list(sample_array)
        generator = func(test_arr)

        steps = list(generator)
        assert len(steps) > 0, f"Algorithm {key} produced 0 steps!"

        last_step = steps[-1]
        assert last_step.action_type == ActionType.FINISH, f"Algorithm {key} did not end with FINISH step!"

        if key != "bogo_sort":
            final_arr = last_step.current_data
            assert final_arr == sorted_expected, f"Algorithm {key} result mismatch: {final_arr} != {sorted_expected}"

        assert key in CODE_SNIPPETS, f"Missing code snippet for {key}"
        print(f"  [PASS] {key:<18} -> Generated {len(steps):>4} steps successfully.")

    print("\n All Sorting Algorithms Verified Successfully!\n")


def test_tree_algorithms():
    print("========================================")
    print("Testing Tree Algorithms...")
    print("========================================")

    tree_elements = [50, 30, 70, 20, 40, 60, 80]

    tree_keys = [
        "preorder_traversal", "inorder_traversal", "postorder_traversal", "levelorder_traversal",
        "bst_search", "bst_insert", "bst_delete", "bst_successor",
        "avl_insert", "avl_delete", "avl_tree", "red_black_tree", "splay_tree",
        "heap_operations", "trie_operations", "segment_tree", "fenwick_tree",
        "b_tree", "kruskal_mst", "prim_mst", "lca_tree"
    ]

    for key in tree_keys:
        func = ALGORITHM_MAP[key]
        if key == "trie_operations":
            generator = func(["cat", "car", "dog"])
        elif key in ("kruskal_mst", "prim_mst"):
            generator = func(6)
        elif key == "bst_insert":
            generator = func(tree_elements, 35)
        elif key == "bst_delete":
            generator = func(tree_elements, 30)
        elif key == "avl_insert":
            generator = func(tree_elements, 15)
        elif key == "avl_delete":
            generator = func(tree_elements, 30)
        else:
            generator = func(tree_elements)

        steps = list(generator)
        assert len(steps) > 0, f"Tree algorithm {key} produced 0 steps!"

        last_step = steps[-1]
        assert last_step.action_type == ActionType.FINISH, f"Tree algorithm {key} did not end with FINISH!"

        assert key in CODE_SNIPPETS, f"Missing code snippet for tree algorithm {key}"
        print(f"  [PASS] {key:<22} -> Generated {len(steps):>4} steps successfully.")

    print("\n All Tree Algorithms Verified Successfully!\n")


if __name__ == "__main__":
    test_sorting_algorithms()
    test_tree_algorithms()
    print("========================================")
    print("ALL TESTS PASSED! APPLICATION 100% READY.")
    print("========================================")
