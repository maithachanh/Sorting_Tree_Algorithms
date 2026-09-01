"""
Tree Layout Utility to compute (x, y) coordinates for rendering trees smoothly on Canvas.
Supports Binary Trees, AVL, Red-Black, Splay, Trie, B-Tree, Segment Tree.
"""

class TreeLayoutCalculator:
    """
    Computes visual 2D positions for tree structures to prevent overlaps.
    """

    @staticmethod
    def compute_binary_tree_layout(root, width=800, height=500, node_radius=22):
        """
        Computes (x, y) coordinates for a standard binary tree using an in-order x-coordinate layout
        combined with level-based y-coordinates.
        """
        if not root:
            return {}

        positions = {}
        # Step 1: Assign in-order rank to get x positions
        order = []

        def in_order_traverse(node, depth=0):
            if not node:
                return
            in_order_traverse(node.left, depth + 1)
            order.append((node, depth))
            in_order_traverse(node.right, depth + 1)

        in_order_traverse(root, 0)

        n = len(order)
        if n == 0:
            return positions

        # Find maximum depth
        max_depth = max(depth for _, depth in order) if order else 0
        y_step = min(70, max(45, (height - 100) / (max_depth + 1))) if max_depth > 0 else 60
        x_margin = max(40, node_radius * 2)
        usable_width = max(width - 2 * x_margin, 200)

        for rank, (node, depth) in enumerate(order):
            if n == 1:
                x = width / 2
            else:
                x = x_margin + (rank / (n - 1)) * usable_width
            y = 50 + depth * y_step
            positions[node.id if hasattr(node, 'id') else id(node)] = (x, y)

        return positions

    @staticmethod
    def compute_b_tree_layout(root, width=800, height=500):
        """
        Computes 2D bounding boxes and center positions for B-Tree / B+ Tree nodes.
        """
        if not root:
            return {}

        positions = {}
        levels = {}

        def get_levels(node, depth=0):
            if not node:
                return
            if depth not in levels:
                levels[depth] = []
            levels[depth].append(node)
            for child in getattr(node, 'children', []):
                get_levels(child, depth + 1)

        get_levels(root, 0)
        y_step = 80

        for depth, nodes in levels.items():
            count = len(nodes)
            spacing = width / (count + 1)
            y = 50 + depth * y_step
            for i, node in enumerate(nodes):
                x = spacing * (i + 1)
                positions[node.id if hasattr(node, 'id') else id(node)] = (x, y)

        return positions

    @staticmethod
    def compute_trie_layout(root, width=800, height=500):
        """
        Computes 2D positions for Trie structures with branch spreading.
        """
        if not root:
            return {}

        positions = {}

        def layout_trie(node, x_min, x_max, depth=0):
            if not node:
                return
            x = (x_min + x_max) / 2
            y = 50 + depth * 60
            node_id = node.id if hasattr(node, 'id') else id(node)
            positions[node_id] = (x, y)

            children = list(getattr(node, 'children', {}).values())
            if not children:
                return

            c_count = len(children)
            c_width = (x_max - x_min) / c_count
            for i, child in enumerate(children):
                c_min = x_min + i * c_width
                c_max = c_min + c_width
                layout_trie(child, c_min, c_max, depth + 1)

        layout_trie(root, 40, width - 40, 0)
        return positions
