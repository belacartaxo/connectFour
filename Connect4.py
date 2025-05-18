import random
import time
import numpy as np
from copy import deepcopy
from Board import Board
from MCTS import MCTS
from Node import Node

def human_play(game, current_player):
    """
    Handles human player's input. Allows hint request or direct column input.
    Ensures only valid numeric input in the range 1–7.
    """
    while True:
        print("Make a move by choosing your coordinates to play.")
        print("Enter column (1-7) or type 'hint' for a suggestion:")
        user_input = input()

        if user_input.lower() == 'hint':
            best_move = get_hint(game, current_player)
            print("Best move according to the AI: ", best_move)
            continue  # Ask again after showing the hint

        if not user_input.isdigit():
            print("Invalid input. Please enter a number between 1 and 7.")
            continue

        move = int(user_input) - 1
        if 0 <= move < 7:
            return move
        else:
            print("Column out of range. Try again.")


def get_hint(game, current_player):
    """
    Uses MCTS to provide a hint for the current player.
    """
    root = Node(game, None)
    mcts = MCTS(root, current_player)
    best_node = mcts.best_move()
    return best_node.board.last_move_column + 1


def human_vs_human():
    """
    Human vs. Human game loop.
    """
    game = Board()
    player = "X"
    game_over = False

    while not game.is_board_full() and not game_over:
        player = "O" if player == "X" else "X"
        game.print_board()
        print(f"It is now {player}'s turn!")

        valid_move = False
        while not valid_move:
            col = human_play(game, player)
            if not game.is_legal_move(col):
                print("\nWarning: Invalid move. Try again!")
            else:
                game.make_move(col, player)
                valid_move = True

        game_over = game.is_won(col, player)

    game.print_board()
    print("It's a tie!" if game.is_tie() else f"Player {player} has won!\n")


def ai_vs_human():
    """
    AI vs. Human game loop.
    """
    game = Board()
    ai = "O"
    human = "X"
    human_turn = False
    game_over = False

    while not game.is_board_full() and not game_over:
        current_player = human if human_turn else ai
        game.print_board()
        print(f"It is now {current_player}'s turn!")

        if human_turn:
            valid_move = False
            while not valid_move:
                move = human_play(game, current_player)
                if not game.is_legal_move(move):
                    print("\nWarning: Invalid move. Try again!")
                else:
                    game.make_move(move, current_player)
                    valid_move = True
        else:
            root = Node(game, None)
            mcts = MCTS(root, ai)
            start = time.time()
            best_node = mcts.best_move()
            move = best_node.board.last_move_column
            game.make_move(move, ai)
            end = time.time()
            print(f"AI chose column: {move + 1}\nTime taken: {end - start:.2f}s")
        game_over = game.is_won(move, current_player)
        human_turn = not human_turn

    game.print_board()
    print("It's a tie!" if game.is_tie() else f"Player {current_player} has won!\n")


def ai_vs_ai(x_simulation_limit=10000, o_simulation_limit=10000):
    """
    AI vs. AI game loop.
    """
    game = Board()
    players = ["X", "O"]
    current_index = 0
    game_over = False

    while not game.is_board_full() and not game_over:
        current_player = players[current_index]
        game.print_board()
        print(f"It is now {current_player}'s turn!")

        root = Node(game, None)
        mcts = MCTS(root, current_player)
        start = time.time()
        best_node = mcts.best_move()
        move = best_node.board.last_move_column
        game.make_move(move, current_player)
        print(move)
        end = time.time()

        print(f"{current_player} chose column: {move + 1}\nTime taken: {end - start:.2f}s")
        game_over = game.is_won(move, current_player)
        current_index = 1 - current_index

    game.print_board()
    print("It's a tie!" if game.is_tie() else f"Player {current_player} has won!\n")

def run():
    """
    Entry point to choose game mode. Validates input.
    """
    print("Choose a game mode:")
    print("1. Human vs Human")
    print("2. AI vs Human")
    print("3. AI vs AI")

    while True:
        user_input = input("Enter the game mode number (1-3): ")
        if user_input.isdigit():
            game_mode = int(user_input)
            if game_mode in [1, 2, 3]:
                break
        print("Invalid game mode. Please enter 1, 2 or 3.")

    if game_mode == 1:
        human_vs_human()
    elif game_mode == 2:
        ai_vs_human()
    elif game_mode == 3:
        ai_vs_ai()

