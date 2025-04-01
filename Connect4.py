from copy import deepcopy
from Board import Board
from MCTS import MCTS
from Node import Node

class Connect4Game:
    def __init__(self):
        self.board = Board()
        self.current_player = "X"

    def human_play(self):
        print("Make a move by choosing your coordinates to play.")
        return int(input("Enter column (1-7): ")) - 1
    
    def ai_play(self, mcts):
        print("AI is thinking...")
        mcts.update_root(deepcopy(self.board), self.current_player)  # update root
        best_move = mcts.best_move()  # Gets best move using MCTS
        x = best_move.board.last_move_column  # Gets last move column
        print(f"AI {self.current_player} chooses column {x + 1}")
        return x
    
    def start_game(self):
        print("Choose a game mode:")
        print("1. Human vs Human")
        print("2. AI vs Human")
        print("3. AI vs AI")
        game_mode = int(input("Enter the game mode number: "))

        if game_mode not in [1, 2, 3]:
            print("Invalid game mode selected!")
            return

        
        is_game_over = False
        self.current_player = "X"

        if game_mode in [2, 3]:
            initial_node = Node(deepcopy(self.board))
            mcts = MCTS(initial_node, self.current_player, 12000)

        while not self.board.is_board_full() and not is_game_over:
            self.board.print_board()
            print(f"It is now {self.current_player}'s turn!")

            if game_mode == 1:     
                x = self.human_play()
            elif game_mode == 2:  
                x = self.human_play() if self.current_player == "X" else self.ai_play(mcts)
            elif game_mode == 3:  
                x = self.ai_play(mcts)

            if not self.board.is_legal_move(x):
                print("\nWarning: Invalid Move. Try again!")
            else:
                self.board.make_move(x, self.current_player)
                is_game_over = self.board.is_won(x, self.board.y_coords[x] + 1, self.current_player)
                if not is_game_over:
                    self.current_player = "O" if self.current_player == "X" else "X"
        
        self.board.print_board()
        if is_game_over:
            print(f"Player {self.current_player} has won!\n")
        elif self.board.is_board_full():
            print("It's a tie!")

if __name__ == "__main__":
    game = Connect4Game()
    game.start_game()