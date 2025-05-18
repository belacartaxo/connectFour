class NodeDT:
    def __init__(self, feature=None, split_criteria=None, left=None, right=None, value=None):
        """
        Initializes a node for a Decision Tree.

        Parameters:
        - feature: The feature used to split the data at this node (e.g., "number of rooms").
        - split_criteria: The threshold value for splitting (e.g., <= 5 goes left, > 5 goes right).
        - left: The left child node (corresponds to data satisfying the split condition).
        - right: The right child node (corresponds to data not satisfying the split condition).
        - value: The predicted value or class if this node is a leaf.
        """
        self.feature = feature
        self.split_criteria = split_criteria
        self.left = left
        self.right = right
        self.value = value
        self.children = {}  # For potential extension to multi-branch trees (e.g., categorical splits)

    def is_leaf(self) -> bool:
        """
        Returns True if the node is a leaf (i.e., it holds a prediction value and has no children).
        """
        return self.value is not None
