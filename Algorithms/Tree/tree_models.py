"""
Node and Tree Data Models for Tree Visualizations.
"""
import copy

_node_counter = 0

def get_next_node_id():
    global _node_counter
    _node_counter += 1
    return _node_counter

def reset_node_counter():
    global _node_counter
    _node_counter = 0

class BinaryNode:
    def __init__(self, val, left=None, right=None, color=None, height=1):
        self.id = get_next_node_id()
        self.val = val
        self.left = left
        self.right = right
        self.color = color  # 'RED', 'BLACK', or None for standard
        self.height = height

    def clone(self):
        return copy.deepcopy(self)

    def to_dict(self):
        """Converts to a dictionary representation for fast serialization."""
        return {
            "id": self.id,
            "val": self.val,
            "color": self.color,
            "height": self.height,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }

class BTreeNode:
    def __init__(self, leaf=False):
        self.id = get_next_node_id()
        self.leaf = leaf
        self.keys = []
        self.children = []

class TrieNode:
    def __init__(self, char=""):
        self.id = get_next_node_id()
        self.char = char
        self.children = {}  # char -> TrieNode
        self.is_end_of_word = False

class SegmentTreeNode:
    def __init__(self, start, end, total, left=None, right=None):
        self.id = get_next_node_id()
        self.start = start
        self.end = end
        self.val = total
        self.left = left
        self.right = right
