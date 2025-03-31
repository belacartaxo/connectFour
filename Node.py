import math

class Node:
    def __init__(self, board, parent=None, children=None):
        self.board = board
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
    
    def is_fully_expanded(self):
        return len(self.children) == len(self.board.getPossibleMoves())

    def best_child(self,):
        return max(self.children, key=lambda child: child.get_uct_value())

    def add_child(self, child):
        self.children.append(child)

    def get_uct_value(self, c=1.4):
        if self.visits == 0 or self.parent is None or self.parent.visits == 0:
            return float('inf')
        exploitation = self.wins / self.visits
        exploration = c * math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploitation + exploration
