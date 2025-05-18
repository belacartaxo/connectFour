import random
from copy import deepcopy
from Node import Node

class MCTS:
    def __init__(self, initial_state, current_player, simulation_limit=10000):
        """
        Initializes the MCTS agent.

        Parameters:
        - initial_state: The root node containing the current game state.
        - current_player: The player for whom the move is being calculated.
        - simulation_limit: Maximum number of simulations to run (default: 10000).
        """
        self.root = initial_state
        self.simulation_limit = simulation_limit
        self.current_player = current_player

    def selection(self):
        """
        Selects the most promising node by traversing the tree
        using the UCT value until a leaf is reached.
        """
        node = self.root
        while node.children:
            node = node.best_child()
        return node

    def expansion(self, node):
        """
        Expands the given node by generating all possible child states.
        """
        current_player = self.current_player
        for board in node.board.get_possible_moves(current_player):
            new_node = Node(board, parent=node)
            node.add_child(new_node)

    def simulation(self, node):
        """
        Simulates a random playout from the current node until
        the game ends with a win or a tie.
        """
        sim_board = deepcopy(node.board)
        player = "O" if self.current_player == "X" else "X"

        while not sim_board.is_board_full():
            legal_moves = [i for i in range(sim_board.board_width) if sim_board.is_legal_move(i)]
            move = random.choice(legal_moves)
            sim_board.make_move(move, player)

            if sim_board.is_won(move, player):
                return player

            player = "O" if player == "X" else "X"

        return "."

    def backpropagation(self, node, result):
        """
        Updates the statistics of the nodes on the path from the
        simulation result back to the root.
        """
        while node is not None:
            node.visits += 1
            if result == self.current_player:
                node.wins += 1
            elif result == ".":
                node.wins += 0.5
            node = node.parent

    def check_for_win(self, leaf) -> Node:
        """
        Checks if there is an immediate winning move for the current player.
        If found, returns a new node representing that winning move.
        """
        possible_moves = [i for i in range(leaf.board.board_width) if leaf.board.is_legal_move(i)]

        for i in possible_moves:
            simulated_board = deepcopy(leaf.board)
            simulated_board.make_move(i, self.current_player)
            if simulated_board.is_won(i, self.current_player):
                return Node(simulated_board, parent=leaf)

        return None

    def best_move(self):
        """
        Runs the full MCTS process and returns the best child of the root node.
        """
        leaf = self.selection()
        if not leaf.children:
            self.expansion(leaf)

        winning_node = self.check_for_win(leaf)
        if winning_node:
            return winning_node

        for child in leaf.children:
            result = self.simulation(child)
            self.backpropagation(child, result)

        children = leaf.children

        for _ in range(7, self.simulation_limit + 1):
            selected_leaf = random.choice(children)
            result = self.simulation(selected_leaf)
            self.backpropagation(selected_leaf, result)

        return self.root.best_child()
