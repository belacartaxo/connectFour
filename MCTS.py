import random
from copy import deepcopy
from Node import Node

class MCTS:
    def __init__(self, initial_state, current_player, simulation_limit):
        # Initialize MCTS with the root node (initial game state),
        # the current player, and how many simulations to run per move.
        self.root = initial_state
        self.simulation_limit = simulation_limit
        self.current_player = current_player

    def update_root(self, new_board_state, new_current_player):
        # Update the root node to match the current game state.
        # If the current board exists among the children, we reuse that node.
        self.current_player = new_current_player
        for child in self.root.children:
            if child.board.to_tuple() == new_board_state.to_tuple():
                self.root = child
                self.root.parent = None
                return
        # If not found, create a new root node from scratch
        self.root = Node(new_board_state)

    def selection(self):
        # Traverse the tree starting from the root, choosing the best child
        # using UCT (Upper Confidence Bound) until a leaf node is reached.
        node = self.root
        while node.children:
            node = node.best_child()
        return node

    def expansion(self, node):
        # Expand the selected node by generating all valid child states (next moves)
        # for the player whose turn it is in this node.
        current_player = self.current_player if node.board.counter % 2 == 0 else ("O" if self.current_player == "X" else "X")
        for move in node.board.get_possible_moves(current_player):
            new_node = Node(move, parent=node)
            node.add_child(new_node)

    def simulation(self, node):
        # Simulate a random playout from the given node until the game ends.
        # The simulation follows random moves until there's a winner or a tie.
        sim_board = deepcopy(node.board)
        player = self.current_player if sim_board.counter % 2 == 0 else ("O" if self.current_player == "X" else "X")

        while not sim_board.is_board_full():
            legal_moves = [i for i in range(sim_board.board_width) if sim_board.is_legal_move(i)]
            if not legal_moves:
                break
            move = random.choice(legal_moves)
            sim_board.make_move(move, player)

            if sim_board.is_won(move, sim_board.y_coords[move] + 1, player):
                return player  # Return the winner

            # Switch players
            player = "O" if player == "X" else "X"

        return None  # It's a tie (draw)

    def backpropagation(self, node, result):
        # Propagate the result of the simulation up the tree,
        # updating visit counts and win counts along the way.
        while node is not None:
            node.visits += 1
            if result == self.current_player:
                node.wins += 1  # Win for the AI
            elif result is None:
                node.wins += 0.5  # Tie counts as half-win
            # Move up to the parent node
            node = node.parent

    def best_move(self):
        # Main MCTS loop: run simulations, expand, simulate, backpropagate
        for _ in range(self.simulation_limit):
            leaf = self.selection()
            if not leaf.children:
                self.expansion(leaf)
            # Pick a random child to simulate if expansion created children
            if leaf.children:
                leaf = random.choice(leaf.children)
            result = self.simulation(leaf)
            self.backpropagation(leaf, result)

        # After all simulations, return the child with the highest win rate
        return self.root.best_child()
