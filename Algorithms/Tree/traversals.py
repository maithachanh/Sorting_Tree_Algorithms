"""
Tree Traversal Algorithms: Pre-order (NLR), In-order (LNR), Post-order (LRN), Level-order (BFS).
"""
from collections import deque
from Algorithms.step_state import StepState, ActionType
from Algorithms.Tree.tree_models import BinaryNode, reset_node_counter

def build_bst_from_list(values):
    """Builds a binary search tree from a list of numbers."""
    reset_node_counter()
    if not values:
        return None

    def insert(root, val):
        if not root:
            return BinaryNode(val)
        if val < root.val:
            root.left = insert(root.left, val)
        else:
            root.right = insert(root.right, val)
        return root

    root = None
    for v in values:
        root = insert(root, v)
    return root


def preorder_traversal(values):
    root = build_bst_from_list(values)
    traversed_order = []

    yield StepState(
        action_type=ActionType.BUILD_TREE,
        current_data=root,
        active_line=1,
        message="Bắt đầu duyệt tiền thứ tự Pre-order (Node -> Left -> Right).",
        extra_info={"traversed": list(traversed_order)}
    )

    def _preorder(node):
        if not node:
            return
        # Visit Node
        traversed_order.append(node.val)
        yield StepState(
            action_type=ActionType.VISIT_NODE,
            highlighted_indices=[node.id],
            current_data=root,
            active_line=3,
            message=f"Thăm nút hiện tại: {node.val} (N). Kết quả hiện tại: {traversed_order}",
            extra_info={"traversed": list(traversed_order)}
        )

        # Visit Left
        if node.left:
            yield StepState(
                action_type=ActionType.HIGHLIGHT_EDGE,
                highlighted_indices=[node.id, node.left.id],
                current_data=root,
                active_line=4,
                message=f"Đi xuống nhánh con trái của nút {node.val} (L).",
                extra_info={"traversed": list(traversed_order)}
            )
            yield from _preorder(node.left)

        # Visit Right
        if node.right:
            yield StepState(
                action_type=ActionType.HIGHLIGHT_EDGE,
                highlighted_indices=[node.id, node.right.id],
                current_data=root,
                active_line=5,
                message=f"Đi sang nhánh con phải của nút {node.val} (R).",
                extra_info={"traversed": list(traversed_order)}
            )
            yield from _preorder(node.right)

    if root:
        yield from _preorder(root)

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message=f"Hoàn thành duyệt Pre-order! Thứ tự duyệt: {traversed_order}",
        extra_info={"traversed": list(traversed_order)}
    )


def inorder_traversal(values):
    root = build_bst_from_list(values)
    traversed_order = []

    yield StepState(
        action_type=ActionType.BUILD_TREE,
        current_data=root,
        active_line=1,
        message="Bắt đầu duyệt trung thứ tự In-order (Left -> Node -> Right).",
        extra_info={"traversed": list(traversed_order)}
    )

    def _inorder(node):
        if not node:
            return

        # Visit Left
        if node.left:
            yield StepState(
                action_type=ActionType.HIGHLIGHT_EDGE,
                highlighted_indices=[node.id, node.left.id],
                current_data=root,
                active_line=3,
                message=f"Đi sâu xuống nhánh con trái của nút {node.val} (L).",
                extra_info={"traversed": list(traversed_order)}
            )
            yield from _inorder(node.left)

        # Visit Node
        traversed_order.append(node.val)
        yield StepState(
            action_type=ActionType.VISIT_NODE,
            highlighted_indices=[node.id],
            current_data=root,
            active_line=4,
            message=f"Thăm nút hiện tại: {node.val} (N). Kết quả hiện tại: {traversed_order}",
            extra_info={"traversed": list(traversed_order)}
        )

        # Visit Right
        if node.right:
            yield StepState(
                action_type=ActionType.HIGHLIGHT_EDGE,
                highlighted_indices=[node.id, node.right.id],
                current_data=root,
                active_line=5,
                message=f"Đi sang nhánh con phải của nút {node.val} (R).",
                extra_info={"traversed": list(traversed_order)}
            )
            yield from _inorder(node.right)

    if root:
        yield from _inorder(root)

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message=f"Hoàn thành duyệt In-order (Dãy tăng dần trên BST): {traversed_order}",
        extra_info={"traversed": list(traversed_order)}
    )


def postorder_traversal(values):
    root = build_bst_from_list(values)
    traversed_order = []

    yield StepState(
        action_type=ActionType.BUILD_TREE,
        current_data=root,
        active_line=1,
        message="Bắt đầu duyệt hậu thứ tự Post-order (Left -> Right -> Node).",
        extra_info={"traversed": list(traversed_order)}
    )

    def _postorder(node):
        if not node:
            return

        # Visit Left
        if node.left:
            yield from _postorder(node.left)

        # Visit Right
        if node.right:
            yield from _postorder(node.right)

        # Visit Node
        traversed_order.append(node.val)
        yield StepState(
            action_type=ActionType.VISIT_NODE,
            highlighted_indices=[node.id],
            current_data=root,
            active_line=5,
            message=f"Thăm nút hiện tại: {node.val} (N). Kết quả hiện tại: {traversed_order}",
            extra_info={"traversed": list(traversed_order)}
        )

    if root:
        yield from _postorder(root)

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message=f"Hoàn thành duyệt Post-order! Thứ tự duyệt: {traversed_order}",
        extra_info={"traversed": list(traversed_order)}
    )


def levelorder_traversal(values):
    root = build_bst_from_list(values)
    traversed_order = []

    yield StepState(
        action_type=ActionType.BUILD_TREE,
        current_data=root,
        active_line=1,
        message="Bắt đầu duyệt theo tầng Level-order (BFS) bằng Hàng đợi (Queue).",
        extra_info={"traversed": list(traversed_order)}
    )

    if not root:
        return

    queue = deque([root])

    while queue:
        node = queue.popleft()
        traversed_order.append(node.val)

        yield StepState(
            action_type=ActionType.VISIT_NODE,
            highlighted_indices=[node.id],
            current_data=root,
            active_line=5,
            message=f"Lấy nút {node.val} ra khỏi hàng đợi và thăm. Đã duyệt: {traversed_order}",
            extra_info={"traversed": list(traversed_order)}
        )

        if node.left:
            queue.append(node.left)
            yield StepState(
                action_type=ActionType.HIGHLIGHT_EDGE,
                highlighted_indices=[node.id, node.left.id],
                current_data=root,
                active_line=7,
                message=f"Đưa con trái {node.left.val} vào hàng đợi.",
                extra_info={"traversed": list(traversed_order)}
            )

        if node.right:
            queue.append(node.right)
            yield StepState(
                action_type=ActionType.HIGHLIGHT_EDGE,
                highlighted_indices=[node.id, node.right.id],
                current_data=root,
                active_line=9,
                message=f"Đưa con phải {node.right.val} vào hàng đợi.",
                extra_info={"traversed": list(traversed_order)}
            )

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message=f"Hoàn thành duyệt BFS Level-order! Thứ tự duyệt: {traversed_order}",
        extra_info={"traversed": list(traversed_order)}
    )
