"""
StepState class to encapsulate snapshot of visualization at each discrete step.
"""
from enum import Enum, auto
import copy

class ActionType(Enum):
    COMPARE = "COMPARE"
    SWAP = "SWAP"
    OVERWRITE = "OVERWRITE"
    PIVOT = "PIVOT"
    SORTED = "SORTED"
    SUBARRAY = "SUBARRAY"
    MARK = "MARK"
    
    # Tree specific
    BUILD_TREE = "BUILD_TREE"
    VISIT_NODE = "VISIT_NODE"
    HIGHLIGHT_EDGE = "HIGHLIGHT_EDGE"
    INSERT_NODE = "INSERT_NODE"
    DELETE_NODE = "DELETE_NODE"
    ROTATE = "ROTATE"
    RECOLOR = "RECOLOR"
    HEAPIFY = "HEAPIFY"
    EXTRACT = "EXTRACT"
    MST_EDGE = "MST_EDGE"
    UPDATE_TREE = "UPDATE_TREE"
    
    # General
    INFO = "INFO"
    FINISH = "FINISH"

class StepState:
    def __init__(
        self,
        action_type=ActionType.INFO,
        highlighted_indices=None,
        current_data=None,
        active_line=1,
        message="",
        comparisons=0,
        swaps=0,
        extra_info=None
    ):
        self.action_type = action_type
        # Can be list of indices [i, j] or dict {i: 'compare', j: 'swap', k: 'pivot'}
        self.highlighted_indices = highlighted_indices if highlighted_indices is not None else []
        # Copy data to prevent mutation across steps
        self.current_data = copy.deepcopy(current_data) if current_data is not None else None
        self.active_line = active_line
        self.message = message
        self.comparisons = comparisons
        self.swaps = swaps
        self.extra_info = extra_info or {}

    def __repr__(self):
        return f"<StepState action={self.action_type} line={self.active_line} msg='{self.message}'>"
