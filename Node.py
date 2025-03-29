import math

class Node:
    def __init__(self, board, parent=None, children=None):
        self.board = board
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def add_child(self, child_node): 
        self.children.append(child_node)
        child_node.parent = self

    def ucb1(self, c=1.4):  
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + c * math.sqrt(math.log(self.parent.visits) / self.visits)