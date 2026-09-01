"""
Self-Balancing Tree Algorithms: Tree Rotations, AVL Tree (Build, Insert, Delete), Red-Black Tree, Splay Tree.
"""
from Algorithms.step_state import StepState, ActionType
from Algorithms.Tree.tree_models import BinaryNode, reset_node_counter

def get_height(node):
    if not node:
        return 0
    return node.height

def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)

def build_avl_from_list(values):
    """Utility to build an AVL tree silently without yielding steps."""
    reset_node_counter()
    root = None

    def _rotate_right(y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(get_height(y.left), get_height(y.right))
        x.height = 1 + max(get_height(x.left), get_height(x.right))
        return x

    def _rotate_left(x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(get_height(x.left), get_height(x.right))
        y.height = 1 + max(get_height(y.left), get_height(y.right))
        return y

    def _insert(node, val):
        if not node:
            return BinaryNode(val)
        if val < node.val:
            node.left = _insert(node.left, val)
        elif val > node.val:
            node.right = _insert(node.right, val)
        else:
            return node

        node.height = 1 + max(get_height(node.left), get_height(node.right))
        balance = get_balance(node)

        # 4 cases
        if balance > 1 and val < node.left.val:
            return _rotate_right(node)
        if balance < -1 and val > node.right.val:
            return _rotate_left(node)
        if balance > 1 and val > node.left.val:
            node.left = _rotate_left(node.left)
            return _rotate_right(node)
        if balance < -1 and val < node.right.val:
            node.right = _rotate_right(node.right)
            return _rotate_left(node)
        return node

    for v in values:
        root = _insert(root, v)
    return root


def avl_insert(values, val_to_insert=None):
    """
    Simulates inserting a single element into an existing AVL Tree and rebalancing step-by-step.
    """
    if not values:
        values = [50, 30, 70, 20, 40]

    if val_to_insert is None:
        val_to_insert = 15

    base_values = [v for v in values if v != val_to_insert]
    if not base_values:
        base_values = [50, 30, 70, 20, 40]

    root = build_avl_from_list(base_values)

    yield StepState(
        action_type=ActionType.BUILD_TREE,
        current_data=root,
        active_line=1,
        message=f"Cây AVL ban đầu (đã cân bằng). Bắt đầu chèn phần tử mới val = {val_to_insert}."
    )

    def _rotate_right(y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(get_height(y.left), get_height(y.right))
        x.height = 1 + max(get_height(x.left), get_height(x.right))
        return x

    def _rotate_left(x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(get_height(x.left), get_height(x.right))
        y.height = 1 + max(get_height(y.left), get_height(y.right))
        return y

    def _insert_step(node, val):
        nonlocal root
        if not node:
            new_n = BinaryNode(val)
            yield StepState(
                action_type=ActionType.INSERT_NODE,
                highlighted_indices=[new_n.id],
                current_data=root,
                active_line=3,
                message=f"Tạo nút mới có giá trị {val} tại vị trí lá."
            )
            return new_n

        yield StepState(
            action_type=ActionType.VISIT_NODE,
            highlighted_indices=[node.id],
            current_data=root,
            active_line=4,
            message=f"So sánh giá trị cần chèn ({val}) với nút hiện tại ({node.val})."
        )

        if val < node.val:
            node.left = yield from _insert_step(node.left, val)
        elif val > node.val:
            node.right = yield from _insert_step(node.right, val)
        else:
            yield StepState(
                action_type=ActionType.INFO,
                highlighted_indices=[node.id],
                current_data=root,
                active_line=7,
                message=f"Giá trị {val} đã tồn tại trong cây AVL (không chèn trùng)."
            )
            return node

        # Update height
        node.height = 1 + max(get_height(node.left), get_height(node.right))
        balance = get_balance(node)

        yield StepState(
            action_type=ActionType.INFO,
            highlighted_indices=[node.id],
            current_data=root,
            active_line=9,
            message=f"Kiểm tra độ cao h={node.height} và hệ số cân bằng BF={balance} tại nút {node.val}."
        )

        # Case 1: Left Left (LL)
        if balance > 1 and val < node.left.val:
            yield StepState(
                action_type=ActionType.ROTATE,
                highlighted_indices=[node.id, node.left.id],
                current_data=root,
                active_line=11,
                message=f"Mất cân bằng Left-Left tại nút {node.val} (BF={balance}) -> Thực hiện Phép Xoay Phải (Right Rotation)."
            )
            rotated = _rotate_right(node)
            return rotated

        # Case 2: Right Right (RR)
        if balance < -1 and val > node.right.val:
            yield StepState(
                action_type=ActionType.ROTATE,
                highlighted_indices=[node.id, node.right.id],
                current_data=root,
                active_line=13,
                message=f"Mất cân bằng Right-Right tại nút {node.val} (BF={balance}) -> Thực hiện Phép Xoay Trái (Left Rotation)."
            )
            rotated = _rotate_left(node)
            return rotated

        # Case 3: Left Right (LR)
        if balance > 1 and val > node.left.val:
            yield StepState(
                action_type=ActionType.ROTATE,
                highlighted_indices=[node.id, node.left.id],
                current_data=root,
                active_line=15,
                message=f"Mất cân bằng Left-Right tại nút {node.val} -> Xoay Trái con trái trước, sau đó Xoay Phải nút {node.val}."
            )
            node.left = _rotate_left(node.left)
            return _rotate_right(node)

        # Case 4: Right Left (RL)
        if balance < -1 and val < node.right.val:
            yield StepState(
                action_type=ActionType.ROTATE,
                highlighted_indices=[node.id, node.right.id],
                current_data=root,
                active_line=17,
                message=f"Mất cân bằng Right-Left tại nút {node.val} -> Xoay Phải con phải trước, sau đó Xoay Trái nút {node.val}."
            )
            node.right = _rotate_right(node.right)
            return _rotate_left(node)

        return node

    root = yield from _insert_step(root, val_to_insert)

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message=f"Chèn nút {val_to_insert} vào Cây AVL và tự động cân bằng hoàn tất!"
    )


def avl_delete(values, val_to_delete=None):
    """
    Simulates deleting an element from an existing AVL Tree and rebalancing step-by-step.
    """
    if not values:
        values = [50, 30, 70, 20, 40, 60, 80]

    root = build_avl_from_list(values)
    if not root:
        return

    if val_to_delete is None:
        val_to_delete = values[0] if values else root.val

    yield StepState(
        action_type=ActionType.BUILD_TREE,
        current_data=root,
        active_line=1,
        message=f"Cây AVL ban đầu gồm các nút: {values}. Bắt đầu tìm và xóa phần tử key = {val_to_delete}."
    )

    def _min_value_node(node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _rotate_right(y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(get_height(y.left), get_height(y.right))
        x.height = 1 + max(get_height(x.left), get_height(x.right))
        return x

    def _rotate_left(x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(get_height(x.left), get_height(x.right))
        y.height = 1 + max(get_height(y.left), get_height(y.right))
        return y

    def _delete_step(node, key):
        nonlocal root
        if not node:
            yield StepState(
                action_type=ActionType.INFO,
                current_data=root,
                active_line=2,
                message=f"Không tìm thấy phần tử {key} trong cây AVL để xóa."
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
            node.left = yield from _delete_step(node.left, key)
        elif key > node.val:
            node.right = yield from _delete_step(node.right, key)
        else:
            # Found node
            yield StepState(
                action_type=ActionType.DELETE_NODE,
                highlighted_indices=[node.id],
                current_data=root,
                active_line=5,
                message=f"Đã tìm thấy nút {node.val} cần xóa! Tiến hành loại bỏ khỏi cây."
            )
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            succ = _min_value_node(node.right)
            yield StepState(
                action_type=ActionType.MARK,
                highlighted_indices=[node.id, succ.id],
                current_data=root,
                active_line=8,
                message=f"Nút {node.val} có 2 con -> Lấy phần tử kế cận In-order Successor = {succ.val} thay thế."
            )
            node.val = succ.val
            node.right = yield from _delete_step(node.right, succ.val)

        if node is None:
            return None

        # Recompute height & balance factor
        node.height = 1 + max(get_height(node.left), get_height(node.right))
        balance = get_balance(node)

        yield StepState(
            action_type=ActionType.INFO,
            highlighted_indices=[node.id],
            current_data=root,
            active_line=11,
            message=f"Cập nhật sau xóa: Nút {node.val} có độ cao h={node.height}, hệ số cân bằng BF={balance}."
        )

        # Balance Cases
        if balance > 1 and get_balance(node.left) >= 0:
            yield StepState(
                action_type=ActionType.ROTATE,
                highlighted_indices=[node.id, node.left.id],
                current_data=root,
                active_line=13,
                message=f"Mất cân bằng LL sau khi xóa tại nút {node.val} -> Thực hiện Xoay Phải."
            )
            return _rotate_right(node)

        if balance > 1 and get_balance(node.left) < 0:
            yield StepState(
                action_type=ActionType.ROTATE,
                highlighted_indices=[node.id, node.left.id],
                current_data=root,
                active_line=15,
                message=f"Mất cân bằng LR sau khi xóa tại nút {node.val} -> Xoay Trái con trái rồi Xoay Phải nút {node.val}."
            )
            node.left = _rotate_left(node.left)
            return _rotate_right(node)

        if balance < -1 and get_balance(node.right) <= 0:
            yield StepState(
                action_type=ActionType.ROTATE,
                highlighted_indices=[node.id, node.right.id],
                current_data=root,
                active_line=17,
                message=f"Mất cân bằng RR sau khi xóa tại nút {node.val} -> Thực hiện Xoay Trái."
            )
            return _rotate_left(node)

        if balance < -1 and get_balance(node.right) > 0:
            yield StepState(
                action_type=ActionType.ROTATE,
                highlighted_indices=[node.id, node.right.id],
                current_data=root,
                active_line=19,
                message=f"Mất cân bằng RL sau khi xóa tại nút {node.val} -> Xoay Phải con phải rồi Xoay Trái nút {node.val}."
            )
            node.right = _rotate_right(node.right)
            return _rotate_left(node)

        return node

    root = yield from _delete_step(root, val_to_delete)

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message=f"Xóa phần tử {val_to_delete} khỏi cây AVL và cân bằng lại hoàn tất!"
    )


def avl_tree_simulation(values):
    """Builds complete AVL tree from array step-by-step."""
    reset_node_counter()
    root = None

    yield StepState(
        action_type=ActionType.INFO,
        current_data=None,
        active_line=1,
        message=f"Bắt đầu xây dựng Cây tự cân bằng AVL từ danh sách {len(values)} phần tử: {values}."
    )

    def _rotate_right(y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(get_height(y.left), get_height(y.right))
        x.height = 1 + max(get_height(x.left), get_height(x.right))
        return x

    def _rotate_left(x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(get_height(x.left), get_height(x.right))
        y.height = 1 + max(get_height(y.left), get_height(y.right))
        return y

    def _insert(node, val):
        if not node:
            return BinaryNode(val)

        if val < node.val:
            node.left = yield from _insert(node.left, val)
        elif val > node.val:
            node.right = yield from _insert(node.right, val)
        else:
            return node

        node.height = 1 + max(get_height(node.left), get_height(node.right))
        balance = get_balance(node)

        # Case LL
        if balance > 1 and val < node.left.val:
            yield StepState(
                action_type=ActionType.ROTATE,
                highlighted_indices=[node.id, node.left.id],
                current_data=root,
                active_line=12,
                message=f"Mất cân bằng LL tại nút {node.val} (BF={balance}) -> Xoay Phải."
            )
            return _rotate_right(node)

        # Case RR
        if balance < -1 and val > node.right.val:
            yield StepState(
                action_type=ActionType.ROTATE,
                highlighted_indices=[node.id, node.right.id],
                current_data=root,
                active_line=15,
                message=f"Mất cân bằng RR tại nút {node.val} (BF={balance}) -> Xoay Trái."
            )
            return _rotate_left(node)

        # Case LR
        if balance > 1 and val > node.left.val:
            yield StepState(
                action_type=ActionType.ROTATE,
                highlighted_indices=[node.id, node.left.id],
                current_data=root,
                active_line=18,
                message=f"Mất cân bằng LR tại nút {node.val} -> Xoay Trái con trái rồi Xoay Phải nút {node.val}."
            )
            node.left = _rotate_left(node.left)
            return _rotate_right(node)

        # Case RL
        if balance < -1 and val < node.right.val:
            yield StepState(
                action_type=ActionType.ROTATE,
                highlighted_indices=[node.id, node.right.id],
                current_data=root,
                active_line=21,
                message=f"Mất cân bằng RL tại nút {node.val} -> Xoay Phải con phải rồi Xoay Trái nút {node.val}."
            )
            node.right = _rotate_right(node.right)
            return _rotate_left(node)

        return node

    for v in values:
        root = yield from _insert(root, v)
        yield StepState(
            action_type=ActionType.UPDATE_TREE,
            current_data=root,
            active_line=23,
            message=f"Đã chèn {v} và duy trì cây AVL cân bằng."
        )

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message="Xây dựng Cây AVL hoàn tất!"
    )


def red_black_tree_simulation(values):
    reset_node_counter()
    root = None

    yield StepState(
        action_type=ActionType.INFO,
        current_data=None,
        active_line=1,
        message="Bắt đầu mô phỏng Cây Đỏ - Đen (Red-Black Tree: Nút mới luôn màu Đỏ, Gốc luôn Đen)."
    )

    def _insert(node, val):
        if not node:
            new_n = BinaryNode(val, color='RED')
            return new_n
        if val < node.val:
            node.left = _insert(node.left, val)
        else:
            node.right = _insert(node.right, val)

        if node.left and node.left.color == 'RED' and node.left.left and node.left.left.color == 'RED':
            node.left.color = 'BLACK'
            node.color = 'RED'
        if node.right and node.right.color == 'RED' and node.left and node.left.color == 'RED':
            node.left.color = 'BLACK'
            node.right.color = 'BLACK'
            node.color = 'RED'
        return node

    for v in values:
        root = _insert(root, v)
        if root:
            root.color = 'BLACK'
        yield StepState(
            action_type=ActionType.INSERT_NODE,
            highlighted_indices=[root.id] if root else [],
            current_data=root,
            active_line=6,
            message=f"Chèn {v} vào Red-Black Tree, đổi màu Recolor / Xoay để giữ tính chất cân bằng màu."
        )

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message="Cây Đỏ - Đen đã được tạo và duy trì cân bằng hoàn hảo!"
    )


def splay_tree_simulation(values, target=None):
    reset_node_counter()
    if not values:
        return
    if target is None:
        target = values[-1]

    root = None
    def bst_ins(node, val):
        if not node:
            return BinaryNode(val)
        if val < node.val:
            node.left = bst_ins(node.left, val)
        else:
            node.right = bst_ins(node.right, val)
        return node

    for v in values:
        root = bst_ins(root, v)

    yield StepState(
        action_type=ActionType.BUILD_TREE,
        current_data=root,
        active_line=1,
        message=f"Bắt đầu Splay Tree: Thao tác Splay đưa nút vừa truy cập ({target}) lên đỉnh gốc (Root)."
    )

    def _rotate_right(y):
        x = y.left
        y.left = x.right
        x.right = y
        return x

    def _rotate_left(x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(node, key):
        if node is None or node.val == key:
            return node

        if key < node.val:
            if node.left is None:
                return node
            if key < node.left.val:
                node.left.left = _splay(node.left.left, key)
                node = _rotate_right(node)
            elif key > node.left.val:
                node.left.right = _splay(node.left.right, key)
                if node.left.right is not None:
                    node.left = _rotate_left(node.left)

            return _rotate_right(node) if node.left is not None else node
        else:
            if node.right is None:
                return node
            if key < node.right.val:
                node.right.left = _splay(node.right.left, key)
                if node.right.left is not None:
                    node.right = _rotate_right(node.right)
            elif key > node.right.val:
                node.right.right = _splay(node.right.right, key)
                node = _rotate_left(node)

            return _rotate_left(node) if node.right is not None else node

    root = _splay(root, target)
    yield StepState(
        action_type=ActionType.ROTATE,
        highlighted_indices=[root.id] if root else [],
        current_data=root,
        active_line=10,
        message=f"Hoàn thành Splay: Nút {target} hiện đã trở thành nút gốc Root của cây!"
    )

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message="Mô phỏng Splay Tree hoàn tất!"
    )
