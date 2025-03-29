from copy import deepcopy
from Node import Node

class Board:
    
    def __init__(self):
        self.header = self.get_default_header()
        self.board = self.get_default_board()
        self.counter = 0
        self.board_width = 7
        self.board_height = 6
        self.y_coords = {col: self.board_height - 1 for col in range(7)}
        self.invalid_move = False
        self.last_move_column = None

    def to_tuple(self):
        return tuple(tuple(row) for row in self.board)
    
    def get_default_header(self):
        return [1, 2, 3, 4, 5, 6, 7]
    
    def get_default_board(self):
        return [list(".......") for _ in range(6)]

    def print_board(self):
        print("\n" + " ".join(map(str, self.header)))
        for row in self.board:
            print(" ".join(row))
        print()

    def is_empty(self, x, y) -> bool:
        # Simply check if the current position is empty
        return self.board[y][x] == "."
    
    def is_board_full(self) -> bool:
        return self.counter == 42
    
    def is_legal_move(self, x) -> bool:
        if self.is_board_full():
            return False
        if not 0 <= x < self.board_width:
            return False  # OUT OF BOUNDS
        if self.y_coords[x] < 0:
            return False  # COLUMN IS FULL
        return self.is_empty(x, self.y_coords[x])

    def make_move(self, x, current_player):
        y = self.y_coords[x]
        self.board[y][x] = current_player  # makes the move
        self.counter += 1  # increase the counter
        self.y_coords[x] -= 1
        self.last_move_column = x

    # WIN CONDITION CHECK
    def is_won(self, x, y, current_player) -> bool:
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                     (1, 1), (-1, -1), (1, -1), (-1, 1)]
        counts = {d: 0 for d in directions}

        for dx, dy in counts:
            x_curr, y_curr = x, y
            while (0 <= x_curr + dx < self.board_width and 
                   0 <= y_curr + dy < self.board_height):
                if self.board[y_curr + dy][x_curr + dx] == current_player:
                    counts[(dx, dy)] += 1
                    x_curr += dx
                    y_curr += dy
                else:
                    break

        return ((counts[(0, 1)] + counts[(0, -1)] + 1) >= 4 or
                (counts[(1, 0)] + counts[(-1, 0)] + 1) >= 4 or
                (counts[(1, 1)] + counts[(-1, -1)] + 1) >= 4 or
                (counts[(1, -1)] + counts[(-1, 1)] + 1) >= 4)

    def get_possible_moves(self, current_player):
        possible_moves = []
        for i in range(self.board_width):
            if self.is_legal_move(i):
                new_board = deepcopy(self)
                new_board.make_move(i, current_player)
                possible_moves.append(new_board)
        return possible_moves

    # def test(self):  # Prototype to simulate moves
    #     stack = []
    #     initial = Node(self)
    #     stack.append(initial)
    #     visited = set()
        
    #     while stack:
    #         current_node = stack.pop() 
    #         current_board = current_node.board

    #         if current_board.is_won():
    #             print("Game finished")
    #             break

    #         for possible_board in current_board.get_possible_moves("X"):  # Iterate all possible moves for the board
    #             board_state = possible_board.to_tuple()  # Convert board to tuple for visited tracking
    #             if board_state not in visited:
    #                 board_copy = deepcopy(possible_board)
    #                 new_node = Node(board_copy, current_node)  # Create new node
    #                 current_node.add_child(new_node)  # Add new node to current node's children
    #                 stack.append(new_node)  # Add new node to stack
    #                 visited.add(board_state)  # Add tuple to visited