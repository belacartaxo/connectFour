import Connect4 as C4
import numpy as np
import csv
import os

def run_simulation(simulation_limit):
    """
    Executes a single simulation of a Connect Four match using two AI agents (MCTS).

    Returns:
    - boardStates: A list of 1D arrays representing the state of the board at each move
    - playerTurns: A list indicating which player ("X" or "O") made each move
    - optimalMoves: A list of the moves chosen by the agents at each step
    """
    boardStates, playerTurns, optimalMoves = C4.ai_vs_ai_simulation_generator(simulation_limit, simulation_limit)
    return boardStates, playerTurns, optimalMoves

def generate_db_csv(folder="datasets", filename="connect4_dataset.csv", iterations=150, append=True, simulation_limit=10000):
    """
    Generates a dataset by simulating multiple Connect Four games and logging the results
    into a CSV file inside a specific folder.

    Parameters:
    - folder: Folder to store the CSV file (e.g., "datasets" or "data")
    - filename: Name of the CSV file
    - iterations: Number of games to simulate
    - append: Whether to append to the existing file or overwrite it
    """
    os.makedirs(folder, exist_ok=True)  # Create folder if it doesn't exist
    filepath = os.path.join(folder, filename)
    
    file_exists = os.path.isfile(filepath)
    mode = 'a' if append else 'w'

    with open(filepath, mode, newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header if file is new or being overwritten
        if not file_exists or not append:
            header = [f"cell_{i+1}" for i in range(42)] + ["player_turn", "chosen_move"]
            writer.writerow(header)

        for i in range(iterations):
            print(f"Initiating simulation {i + 1}:")
            boardStates, playerTurns, optimalMoves = run_simulation(simulation_limit)

            for state, player, move in zip(boardStates, playerTurns, optimalMoves):
                row = list(state) + [player, move]
                writer.writerow(row)

            print(f"Simulation {i + 1} completed!")
            print(f"Progress: { round(((i + 1)/iterations) * 100, 2)}%")
            print("")

# Generate and save in "datasets/connect4_dataset.csv"
generate_db_csv(folder="datasets", filename="connect4_dataset.csv", iterations=500, append=True, simulation_limit=5000)
