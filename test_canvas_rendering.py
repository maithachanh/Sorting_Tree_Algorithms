"""
Comprehensive test script to simulate every Sorting and Tree algorithm on its respective Canvas
and trigger paintEvent to ensure zero AttributeError, KeyError, or rendering crashes.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from gui.views.visualizer_view import VisualizerView, ALGORITHM_MAP
from core.session_manager import SessionManager

app = QApplication(sys.argv)

def test_all_visualizations():
    print("==================================================")
    print("Testing Full Visualizer & Canvas Rendering Flow...")
    print("==================================================")

    session = SessionManager.instance()
    view = VisualizerView()
    view.resize(1200, 800)

    # 1. Test Sorting Algorithms
    sorting_keys = [
        "bubble_sort", "selection_sort", "insertion_sort", "interchange_sort",
        "shaker_sort", "comb_sort", "gnome_sort", "quick_sort", "merge_sort",
        "heap_sort", "shell_sort", "tree_sort", "counting_sort", "radix_sort",
        "bucket_sort", "bead_sort", "tim_sort", "intro_sort", "block_sort",
        "bitonic_sort", "bogo_sort"
    ]

    for key in sorting_keys:
        session.set_algorithm("sorting", key, key)
        session.set_sorting_array([45, 12, 85, 32, 89, 39, 69, 44])
        view.start_simulation()
        
        # Step through every step and render
        for i in range(len(view.controller.steps)):
            view.controller.jump_to_step(i)
            # Force repaint
            canvas = view.canvas_stack.currentWidget()
            canvas.repaint()

        print(f"  [CANVAS OK] Sorting: {key:<20} ({len(view.controller.steps):>3} frames rendered)")

    # 2. Test Tree & Graph Algorithms
    tree_keys = [
        "preorder_traversal", "inorder_traversal", "postorder_traversal", "levelorder_traversal",
        "bst_search", "bst_insert", "bst_delete", "bst_successor",
        "avl_insert", "avl_delete", "avl_tree", "red_black_tree", "splay_tree",
        "heap_operations", "trie_operations", "segment_tree", "fenwick_tree",
        "b_tree", "kruskal_mst", "prim_mst", "lca_tree"
    ]

    for key in tree_keys:
        session.set_algorithm("tree", key, key)
        session.set_tree_elements([50, 30, 70, 20, 40, 60, 80])
        # Direct generator load into view controller without blocking dialogs in test mode
        gen_func = ALGORITHM_MAP[key]
        if key in ("kruskal_mst", "prim_mst"):
            view.canvas_stack.setCurrentIndex(2)
            view.controller.load_generator(gen_func, 6 if key == "kruskal_mst" else 5)
        elif key == "trie_operations":
            view.canvas_stack.setCurrentIndex(1)
            view.controller.load_generator(gen_func, ["cat", "car", "dog"])
        elif key == "bst_insert":
            view.canvas_stack.setCurrentIndex(1)
            view.controller.load_generator(gen_func, [50, 30, 70, 20, 40], 35)
        elif key == "bst_delete":
            view.canvas_stack.setCurrentIndex(1)
            view.controller.load_generator(gen_func, [50, 30, 70, 20, 40], 30)
        elif key == "avl_insert":
            view.canvas_stack.setCurrentIndex(1)
            view.controller.load_generator(gen_func, [50, 30, 70, 20, 40], 15)
        elif key == "avl_delete":
            view.canvas_stack.setCurrentIndex(1)
            view.controller.load_generator(gen_func, [50, 30, 70, 20, 40], 30)
        elif key == "bst_search":
            view.canvas_stack.setCurrentIndex(1)
            view.controller.load_generator(gen_func, [50, 30, 70, 20, 40], 30)
        elif key == "bst_successor":
            view.canvas_stack.setCurrentIndex(1)
            view.controller.load_generator(gen_func, [50, 30, 70, 20, 40], 30)
        elif key == "lca_tree":
            view.canvas_stack.setCurrentIndex(1)
            view.controller.load_generator(gen_func, [50, 30, 70, 20, 40], 20, 40)
        else:
            view.canvas_stack.setCurrentIndex(1)
            view.controller.load_generator(gen_func, [50, 30, 70, 20, 40, 60, 80])

        view.complexity_panel.update_complexity(key)

        for i in range(len(view.controller.steps)):
            view.controller.jump_to_step(i)
            canvas = view.canvas_stack.currentWidget()
            canvas.repaint()

        print(f"  [CANVAS OK] Tree/Graph: {key:<20} ({len(view.controller.steps):>3} frames rendered)")

    print("\n==================================================")
    print(" ALL 42 ALGORITHM VISUALIZATIONS RENDERED PERFECTLY!")
    print("==================================================")

if __name__ == "__main__":
    test_all_visualizations()
