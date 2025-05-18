import math

class Node:
    def __init__(self, board, parent=None):
        """
        Initializes a node representing a game state in the MCTS tree.

        Parameters:
        - board: The game board associated with this node.
        - parent: The parent node in the tree (None if this is the root).
        """
        self.board = board
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def is_fully_expanded(self) -> bool:
        """
        Returns True if all possible moves from this state have been expanded into children.
        """
        return len(self.children) == len(self.board.get_possible_moves("X"))  # or "O" if alternating

    def best_child(self):
        """
        Returns the child node with the highest UCT (Upper Confidence Bound for Trees) value.
        Used to select the most promising node during the selection phase of MCTS.
        """
        return max(self.children, key=lambda child: child.get_uct_value())

    def add_child(self, child):
        """
        Adds a new child node to this node.
        """
        self.children.append(child)

    def get_uct_value(self, c=1.4) -> float:
        """
        Calculates the UCT value for this node, balancing exploration and exploitation.
        """
        exploitation = self.wins / (self.visits + 1e-6)
        exploration = c * math.sqrt(math.log(self.parent.visits + 1) / (self.visits + 1e-6))
        return exploitation + exploration
