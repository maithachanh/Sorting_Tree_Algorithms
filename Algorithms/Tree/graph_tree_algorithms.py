"""
Graph Tree Algorithms: MST (Kruskal, Prim) and Lowest Common Ancestor (LCA).
Fixed: Prim now passes 'edges' and 'visited' in extra_info every step.
"""
from Algorithms.step_state import StepState, ActionType
from Algorithms.Tree.tree_models import BinaryNode, reset_node_counter
from Algorithms.Tree.traversals import build_bst_from_list


def kruskal_mst_simulation(nodes_count=6):
    """Kruskal's MST — sorts all edges and greedily adds non-cycle edges using DSU."""
    edges = [
        (0, 1, 4), (0, 2, 4), (1, 2, 2),
        (2, 3, 3), (2, 5, 2), (2, 4, 4),
        (3, 4, 3), (5, 4, 3)
    ]
    # De-duplicate and sort by weight
    edge_set = sorted(
        list(set((min(u, v), max(u, v), w) for u, v, w in edges)),
        key=lambda x: x[2]
    )

    parent = list(range(nodes_count))

    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj
            return True
        return False

    mst_edges = []
    total_weight = 0

    yield StepState(
        action_type=ActionType.INFO,
        current_data=None,
        active_line=1,
        message=(f"Bắt đầu thuật toán Kruskal tìm Cây khung tối tiểu (MST) "
                 f"với {nodes_count} đỉnh. Sắp xếp {len(edge_set)} cạnh tăng dần theo trọng số."),
        extra_info={"edges": edge_set, "mst": [], "visited": list(range(nodes_count))}
    )

    for u, v, w in edge_set:
        yield StepState(
            action_type=ActionType.COMPARE,
            current_data=None,
            active_line=4,
            message=f"Xét cạnh ({u} — {v}) có trọng số w = {w}. Kiểm tra có tạo chu trình không?",
            extra_info={"edges": edge_set, "mst": list(mst_edges),
                        "current_edge": (u, v, w),
                        "visited": list(range(nodes_count))}
        )

        if union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            yield StepState(
                action_type=ActionType.MST_EDGE,
                current_data=None,
                active_line=6,
                message=(f"✅ Không tạo chu trình → Thêm cạnh ({u} — {v}, w={w}) vào MST. "
                         f"Tổng trọng số hiện tại: {total_weight}."),
                extra_info={"edges": edge_set, "mst": list(mst_edges),
                            "current_edge": (u, v, w),
                            "visited": list(range(nodes_count))}
            )
        else:
            yield StepState(
                action_type=ActionType.INFO,
                current_data=None,
                active_line=8,
                message=f"❌ Cạnh ({u} — {v}) tạo chu trình khép kín → Bỏ qua cạnh này.",
                extra_info={"edges": edge_set, "mst": list(mst_edges),
                            "visited": list(range(nodes_count))}
            )

        if len(mst_edges) == nodes_count - 1:
            break

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=None,
        active_line=1,
        message=f"🎉 Kruskal MST hoàn tất! MST gồm {len(mst_edges)} cạnh. Tổng trọng số tối thiểu: {total_weight}.",
        extra_info={"edges": edge_set, "mst": list(mst_edges),
                    "visited": list(range(nodes_count))}
    )


def prim_mst_simulation(nodes_count=5):
    """Prim's MST — grows MST greedily by always picking the minimum crossing edge."""
    # Adjacency list: node -> [(neighbor, weight)]
    adj = {
        0: [(1, 2), (3, 6)],
        1: [(0, 2), (2, 3), (3, 8), (4, 5)],
        2: [(1, 3), (4, 7)],
        3: [(0, 6), (1, 8), (4, 9)],
        4: [(1, 5), (2, 7), (3, 9)]
    }

    # Build displayable edge list (undirected, de-duplicated)
    display_edges = sorted(
        list(set((min(u, v), max(u, v), w)
                 for u, neighbors in adj.items()
                 for v, w in neighbors)),
        key=lambda x: x[2]
    )

    visited = {0}
    mst_edges = []
    total_weight = 0

    yield StepState(
        action_type=ActionType.INFO,
        current_data=None,
        active_line=1,
        message="Bắt đầu thuật toán Prim: Khởi tạo từ đỉnh nguồn 0, dần mở rộng cây khung sang đỉnh chưa thăm gần nhất.",
        extra_info={"edges": display_edges, "mst": [],
                    "visited": list(visited)}
    )

    while len(visited) < nodes_count:
        min_edge = None
        min_w = float('inf')

        # Scan all crossing edges
        for u in visited:
            for v, w in adj.get(u, []):
                if v not in visited and w < min_w:
                    min_w = w
                    min_edge = (u, v, w)

        if min_edge is None:
            break

        u, v, w = min_edge
        # Show current candidate before adding
        yield StepState(
            action_type=ActionType.COMPARE,
            current_data=None,
            active_line=4,
            message=(f"Vết cắt: Đỉnh đã thăm = {sorted(visited)}. "
                     f"Cạnh nhẹ nhất qua vết cắt: ({u} — {v}, w={w})."),
            extra_info={"edges": display_edges, "mst": list(mst_edges),
                        "current_edge": (u, v, w),
                        "visited": list(visited)}
        )

        visited.add(v)
        mst_edges.append((u, v, w))
        total_weight += w

        yield StepState(
            action_type=ActionType.MST_EDGE,
            current_data=None,
            active_line=6,
            message=(f"✅ Chọn cạnh ({u} — {v}, w={w}) → Thêm đỉnh {v} vào cây. "
                     f"Tổng trọng số hiện tại: {total_weight}."),
            extra_info={"edges": display_edges, "mst": list(mst_edges),
                        "current_edge": (u, v, w),
                        "visited": list(visited)}
        )

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=None,
        active_line=1,
        message=f"🎉 Prim MST hoàn tất! Cây khung tối tiểu gồm {len(mst_edges)} cạnh. Tổng trọng số: {total_weight}.",
        extra_info={"edges": display_edges, "mst": list(mst_edges),
                    "visited": list(visited)}
    )


def lca_simulation(values, n1=None, n2=None):
    """Lowest Common Ancestor (LCA) on a BST — traversal path visualization."""
    root = build_bst_from_list(values)
    if not root:
        return

    if n1 is None or n2 is None:
        if len(values) >= 2:
            n1, n2 = values[0], values[-1]
        else:
            n1, n2 = 20, 80

    yield StepState(
        action_type=ActionType.BUILD_TREE,
        current_data=root,
        active_line=1,
        message=f"Tìm Tổ tiên chung gần nhất (LCA) của 2 nút [{n1}] và [{n2}] trên cây BST."
    )

    curr = root
    while curr:
        yield StepState(
            action_type=ActionType.VISIT_NODE,
            highlighted_indices=[curr.id],
            current_data=root,
            active_line=4,
            message=f"Đang kiểm tra tại nút {curr.val}: n1={n1}, n2={n2}."
        )

        if n1 < curr.val and n2 < curr.val:
            yield StepState(
                action_type=ActionType.HIGHLIGHT_EDGE,
                highlighted_indices=[curr.id, curr.left.id] if curr.left else [curr.id],
                current_data=root,
                active_line=5,
                message=f"Cả {n1} và {n2} đều < {curr.val} → Đi sang nhánh con Trái."
            )
            curr = curr.left
        elif n1 > curr.val and n2 > curr.val:
            yield StepState(
                action_type=ActionType.HIGHLIGHT_EDGE,
                highlighted_indices=[curr.id, curr.right.id] if curr.right else [curr.id],
                current_data=root,
                active_line=6,
                message=f"Cả {n1} và {n2} đều > {curr.val} → Đi sang nhánh con Phải."
            )
            curr = curr.right
        else:
            yield StepState(
                action_type=ActionType.MARK,
                highlighted_indices=[curr.id],
                current_data=root,
                active_line=7,
                message=(f"🎯 Tổ tiên chung gần nhất (LCA) của [{n1}] và [{n2}] "
                         f"chính là nút {curr.val}! "
                         f"(Một nút nằm bên trái, một nút nằm bên phải → Đây là điểm phân nhánh.)")
            )
            break

    yield StepState(
        action_type=ActionType.FINISH,
        current_data=root,
        active_line=1,
        message="Hoàn thành thuật toán LCA!"
    )
