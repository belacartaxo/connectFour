from copy import deepcopy
from Node import Node

class Board:
    def __init__(self):
        """
        Initializes the Connect Four board.
        - 6 rows x 7 columns represented by a list of lists.
        - y_coords stores the next available row index for each column.
        """
        self.counter = 0
        self.board_width = 7
        self.board_height = 6
        self.board = [list(".......") for _ in range(self.board_height)]
        self.y_coords = {col: self.board_height - 1 for col in range(self.board_width)}
        self.last_move_column = None

    def to_tuple(self):
        """
        Returns an immutable representation of the board (useful for hashing).
        """
        return tuple(tuple(row) for row in self.board)

    def get_simulation_board(self):
        """
        Placeholder for compatibility or extensions (e.g., for neural network input).
        """
        return []

    def print_board(self):
        """
        Displays the board to the console.
        """
        print("\n" + " ".join(map(str, [1, 2, 3, 4, 5, 6, 7])))
        for row in self.board:
            print(" ".join(row))
        print()

    def is_empty(self, x, y) -> bool:
        """
        Checks if a given cell is empty.
        """
        return self.board[y][x] == "."

    def is_board_full(self) -> bool:
        """
        Checks if the board is full (42 moves).
        """
        return self.counter == 42

    def is_legal_move(self, x) -> bool:
        """
        Checks if a move is legal:
        - Column must be within bounds.
        - Column must not be full.
        """
        if self.is_board_full():
            return False
        if not 0 <= x < self.board_width:
            return False
        if self.y_coords[x] < 0:
            return False
        return self.is_empty(x, self.y_coords[x])

    def make_move(self, x, current_player):
        """
        Places a piece from the current player in the specified column.
        Updates the board, move counter, and last played column.
        """
        y = self.y_coords[x]
        self.board[y][x] = current_player
        self.counter += 1
        self.y_coords[x] -= 1
        self.last_move_column = x

    def count_in_direction(self, current_player, dx, dy, x, y):
        """
        Counts how many consecutive pieces exist in a given direction from (x, y).
        """
        count = 0
        while (0 <= x + dx < self.board_width and 
               0 <= y + dy < self.board_height and 
               self.board[y + dy][x + dx] == current_player):
            x += dx
            y += dy
            count += 1
        return count

    def is_won(self, x, current_player) -> bool:
        """
        Checks whether the last move in column x resulted in a win.
        """
        directions = [((0, 1), (0, -1)),      # Horizontal
                      ((1, 0), (-1, 0)),      # Vertical
                      ((1, 1), (-1, -1)),     # Main diagonal
                      ((1, -1), (-1, 1))]     # Anti-diagonal

        y = self.y_coords[x] + 1  # Find the row where the last move was placed
        if y is None:
            return False
        for (dy1, dx1), (dy2, dx2) in directions:
            total = (self.count_in_direction(current_player, dx1, dy1, x, y) +
                     self.count_in_direction(current_player, dx2, dy2, x, y) + 1)
            if total >= 4:
                return True
        return False

    def has_winner(self) -> bool:
        """
        Scans the board to detect if there is a winning sequence for any player.
        Used in end-of-game checks (e.g., for tie).
        """
        for y in range(self.board_height):
            for x in range(self.board_width):
                if self.board[y][x] in ["X", "O"]:
                    current_player = self.board[y][x]
                    for (dx1, dy1), (dx2, dy2) in [((0, 1), (0, -1)),
                                                  ((1, 0), (-1, 0)),
                                                  ((1, 1), (-1, -1)),
                                                  ((1, -1), (-1, 1))]:
                        count = 1
                        count += self.count_in_direction(current_player, dx1, dy1, x, y)
                        count += self.count_in_direction(current_player, dx2, dy2, x, y)
                        if count >= 4:
                            return True
        return False

    def is_tie(self) -> bool:
        """
        Returns True if the board is full and there is no winner.
        """
        return self.is_board_full() and not self.has_winner()

    def get_possible_moves(self, current_player):
        """
        Returns a list of possible future board states given the current player's move.
        Useful for MCTS simulation.
        """
        possible_boards = []
        for i in range(self.board_width):
            if self.is_legal_move(i):
                new_board = deepcopy(self)
                new_board.make_move(i, current_player)
                possible_boards.append(new_board)
        return possible_boards
