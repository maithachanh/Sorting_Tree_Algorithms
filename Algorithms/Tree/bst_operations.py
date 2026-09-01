"""
Binary Search Tree (BST) Operations: Search, Insert (Interactive Single Element), Delete (Interactive Single Element), Successor / Predecessor.
"""
from Algorithms.step_state import StepState, ActionType
from Algorithms.Tree.tree_models import BinaryNode, reset_node_counter
from Algorithms.Tree.traversals import build_bst_from_list

def bst_search(values, target=None):
    root = build_bst_from_list(values)
    if not root:
        return
    if target is None:
        target = values[len(values) // 2] if values else 40

    yield StepState(
        action_type=ActionType.BUILD_TREE,
        current_data=root,
        active_line=1,
        message=f"Bắt đầu tìm kiếm giá trị target = {target} trên Cây nhị phân tìm kiếm (BST)."
    )

    curr = root
    found = False
    while curr:
        yield StepState(
            action_type=ActionType.VISIT_NODE,
            highlighted_indices=[curr.id],
            current_data=root,
            active_line=3,
            message=f"Đang so sánh target ({target}) với nút hiện tại ({curr.val})."
        )

        if curr.val == target:
            found = True
            yield StepState(
                action_type=ActionType.MARK,
                highlighted_indices=[curr.id],
                current_data=root,
                active_line=4,
                message=f"Đã tìm thấy nút có giá trị {target} trong cây BST!"
            )
            break
        elif target < curr.val:
            yield StepState(
                action_type=ActionType.HIGHLIGHT_EDGE,
                highlighted_indices=[curr.id, curr.left.id] if curr.left else [curr.id],
                current_data=root,
                active_line=6,
                message=f"Do {target} < {curr.val}, rẽ sang nhánh con trái."
            )
            curr = curr.left
        else:
            yield StepState(
                action_type=ActionType.HIGHLIGHT_EDGE,
                highlighted_indices=[curr.id, curr.right.id] if curr.right else [curr.id],
                current_data=root,
                active_line=8,
                message=f"Do {target} > {curr.val}, rẽ sang nhánh con phải."
            )
            curr = curr.right

    if not found:
        yield StepState(
            action_type=ActionType.INFO,
            current_data=root,
            active_line=9,
            message=f"Không tìm thấy giá trị {target} trong cây BST!"
        )

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message="Kết thúc thuật toán tìm kiếm BST."
    )


def bst_insert(values, val_to_insert=None):
    """
    Simulates inserting a specific value into an existing BST.
    If val_to_insert is None, picks a default value or inserts the last element into the rest.
    """
    if not values:
        values = [50, 30, 70, 20, 40]

    if val_to_insert is None:
        # Default value to insert
        val_to_insert = 35

    # Build initial tree excluding val_to_insert if present to ensure clean demonstration
    base_values = [v for v in values if v != val_to_insert]
    if not base_values:
        base_values = [50, 30, 70, 20, 40]

    root = build_bst_from_list(base_values)

    yield StepState(
        action_type=ActionType.BUILD_TREE,
        current_data=root,
        active_line=1,
        message=f"Cây BST ban đầu gồm các nút: {base_values}. Bắt đầu chèn phần tử mới val = {val_to_insert}."
    )

    new_node = BinaryNode(val_to_insert)
    if root is None:
        root = new_node
        yield StepState(
            action_type=ActionType.INSERT_NODE,
            highlighted_indices=[root.id],
            current_data=root,
            active_line=3,
            message=f"Cây đang rỗng: Gán nút {val_to_insert} làm gốc Root."
        )
    else:
        curr = root
        parent = None
        while curr:
            parent = curr
            yield StepState(
                action_type=ActionType.VISIT_NODE,
                highlighted_indices=[curr.id],
                current_data=root,
                active_line=4,
                message=f"So sánh giá trị cần chèn ({val_to_insert}) với nút hiện tại ({curr.val})."
            )

            if val_to_insert < curr.val:
                if curr.left is None:
                    curr.left = new_node
                    yield StepState(
                        action_type=ActionType.INSERT_NODE,
                        highlighted_indices=[curr.id, new_node.id],
                        current_data=root,
                        active_line=7,
                        message=f"Tìm thấy vị trí lá trống: Chèn nút {val_to_insert} làm con trái của nút {curr.val}."
                    )
                    break
                else:
                    yield StepState(
                        action_type=ActionType.HIGHLIGHT_EDGE,
                        highlighted_indices=[curr.id, curr.left.id],
                        current_data=root,
                        active_line=5,
                        message=f"Do {val_to_insert} < {curr.val}, tiếp tục đi xuống nhánh con trái."
                    )
                    curr = curr.left
            elif val_to_insert > curr.val:
                if curr.right is None:
                    curr.right = new_node
                    yield StepState(
                        action_type=ActionType.INSERT_NODE,
                        highlighted_indices=[curr.id, new_node.id],
                        current_data=root,
                        active_line=10,
                        message=f"Tìm thấy vị trí lá trống: Chèn nút {val_to_insert} làm con phải của nút {curr.val}."
                    )
                    break
                else:
                    yield StepState(
                        action_type=ActionType.HIGHLIGHT_EDGE,
                        highlighted_indices=[curr.id, curr.right.id],
                        current_data=root,
                        active_line=8,
                        message=f"Do {val_to_insert} > {curr.val}, tiếp tục đi xuống nhánh con phải."
                    )
                    curr = curr.right
            else:
                yield StepState(
                    action_type=ActionType.INFO,
                    highlighted_indices=[curr.id],
                    current_data=root,
                    active_line=11,
                    message=f"Giá trị {val_to_insert} đã tồn tại trong cây BST (không chèn trùng lặp)."
                )
                break

    yield StepState(
        action_type=ActionType.FINISH,
        highlighted_indices=[new_node.id] if new_node else [],
        current_data=root,
        active_line=1,
        message=f"Hoàn thành thao tác chèn phần tử {val_to_insert} vào cây BST!"
    )


def bst_delete(values, val_to_delete=None):
    root = build_bst_from_list(values)
    if not root:
        return

    if val_to_delete is None:
        # Default delete root or first value
        val_to_delete = values[0] if values else root.val

    yield StepState(
        action_type=ActionType.BUILD_TREE,
        current_data=root,
        active_line=1,
        message=f"Cây BST ban đầu gồm các nút: {values}. Bắt đầu tìm và xóa nút có giá trị key = {val_to_delete}."
    )

    def _min_value_node(node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _delete_node(node, key):
        if node is None:
            yield StepState(
                action_type=ActionType.INFO,
                current_data=root,
                active_line=2,
                message=f"Không tìm thấy nút có giá trị {key} trong cây!"
            )
            return None

        yield StepState(
            action_type=ActionType.VISIT_NODE,
            highlighted_indices=[node.id],
            current_data=root,
            active_line=3,
            message=f"Duyệt đến nút {node.val}, so sánh với giá trị cần xóa ({key})."
        )

        if key < node.val:
            node.left = yield from _delete_node(node.left, key)
        elif key > node.val:
            node.right = yield from _delete_node(node.right, key)
        else:
            # Found node to delete
            yield StepState(
                action_type=ActionType.DELETE_NODE,
                highlighted_indices=[node.id],
                current_data=root,
                active_line=6,
                message=f"Đã tìm thấy nút {node.val} cần xóa! Đang phân tích trường hợp con của nút..."
            )

            # Case 1 & 2: 0 con (nút lá) hoặc 1 con
            if node.left is None:
                replacement = node.right
                msg = f"Nút {node.val} là nút lá hoặc chỉ có con phải. Thay thế bằng con phải." if node.right else f"Nút {node.val} là nút lá. Xóa trực tiếp."
                yield StepState(
                    action_type=ActionType.DELETE_NODE,
                    highlighted_indices=[node.id],
                    current_data=root,
                    active_line=7,
                    message=msg
                )
                return replacement
            elif node.right is None:
                replacement = node.left
                yield StepState(
                    action_type=ActionType.DELETE_NODE,
                    highlighted_indices=[node.id],
                    current_data=root,
                    active_line=9,
                    message=f"Nút {node.val} chỉ có 1 con trái. Thay thế nút bằng con trái."
                )
                return replacement

            # Case 3: 2 con
            succ = _min_value_node(node.right)
            yield StepState(
                action_type=ActionType.MARK,
                highlighted_indices=[node.id, succ.id],
                current_data=root,
                active_line=11,
                message=f"Nút {node.val} có đủ 2 con! Tìm phần tử nhỏ nhất bên nhánh phải (In-order Successor = {succ.val}) để thay thế."
            )
            node.val = succ.val
            yield StepState(
                action_type=ActionType.UPDATE_TREE,
                highlighted_indices=[node.id],
                current_data=root,
                active_line=12,
                message=f"Gán giá trị {succ.val} vào nút hiện tại. Tiếp tục đệ quy xóa nút {succ.val} ở nhánh phải."
            )
            node.right = yield from _delete_node(node.right, succ.val)

        return node

    root = yield from _delete_node(root, val_to_delete)

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message=f"Đã hoàn tất thao tác xóa nút {val_to_delete} khỏi cây BST!"
    )


def bst_successor_predecessor(values, target=None):
    root = build_bst_from_list(values)
    if not root:
        return
    if target is None:
        target = values[0] if values else root.val

    yield StepState(
        action_type=ActionType.BUILD_TREE,
        current_data=root,
        active_line=1,
        message=f"Tìm nút kế cận trước (Predecessor) và sau (Successor) của giá trị target = {target}."
    )

    inorder_nodes = []
    def inorder(node):
        if node:
            inorder(node.left)
            inorder_nodes.append(node)
            inorder(node.right)

    inorder(root)
    idx = -1
    for i, n in enumerate(inorder_nodes):
        if n.val == target:
            idx = i
            break

    pred = inorder_nodes[idx - 1].val if idx > 0 else "Không có (Nhỏ nhất)"
    succ = inorder_nodes[idx + 1].val if (0 <= idx < len(inorder_nodes) - 1) else "Không có (Lớn nhất)"

    highlight_ids = [inorder_nodes[idx].id] if idx != -1 else []
    if idx > 0:
        highlight_ids.append(inorder_nodes[idx - 1].id)
    if 0 <= idx < len(inorder_nodes) - 1:
        highlight_ids.append(inorder_nodes[idx + 1].id)

    yield StepState(
        action_type=ActionType.VISIT_NODE,
        highlighted_indices=highlight_ids,
        current_data=root,
        active_line=5,
        message=f"Nút [{target}]: Predecessor (Đứng trước trong In-order) = {pred}, Successor (Đứng sau trong In-order) = {succ}."
    )

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message="Kết thúc thao tác tìm Successor & Predecessor."
    )
