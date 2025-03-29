import random
from copy import deepcopy
from Node import Node

class MCTS:
    def __init__(self, initial_state, current_player, simulation_limit):
        self.root = initial_state
        self.simulation_limit = simulation_limit
        self.current_player = current_player  # O jogador que deve mover a seguir

    def update_root(self, new_board_state, new_current_player):
        """
        Atualiza o nó raiz para o estado atual do jogo e jogador atual
        Args:
            new_board_state: O novo estado do tabuleiro
            new_current_player: O jogador que deve mover a seguir ('X' ou 'O')
        """
        # Procura pelo estado nos filhos da raiz atual
        for child in self.root.children:
            if child.board == new_board_state:
                self.root = child
                self.current_player = new_current_player
                return
        
        # Se não encontrou, cria um novo nó raiz
        self.root = Node(deepcopy(new_board_state))
        self.root.current_player = new_current_player
        self.current_player = new_current_player

    def selection(self):
        current_node = self.root
        while current_node.children:
            current_node = max(current_node.children, key=lambda x: x.ucb1())
        return current_node
    
    def expansion(self, node):
        """Expande o nó com todos os movimentos possíveis para o jogador atual"""
        possible_moves = node.board.get_possible_moves(node.current_player)
        for move in possible_moves:
            child_node = Node(deepcopy(move))
            child_node.current_player = "O" if node.current_player == "X" else "X"
            node.add_child(child_node)

    def simulation(self, node):
        """Simula um jogo aleatório a partir deste nó"""
        sim_board = deepcopy(node.board)
        current_player = node.current_player
        last_move = None
        
        while not sim_board.is_board_full():
            # Verifica se o último movimento venceu
            if last_move and sim_board.is_won(last_move[0], last_move[1], "O" if current_player == "X" else "X"):
                return 1 if ("O" if current_player == "X" else "X") == self.current_player else 0
            
            # Faz um movimento aleatório
            possible_moves = sim_board.get_possible_moves(current_player)
            if not possible_moves:
                break
                
            move = random.choice(possible_moves)
            sim_board.make_move(move.last_move_column, current_player)
            last_move = (move.last_move_column, sim_board.y_coords[move.last_move_column] + 1)
            current_player = "O" if current_player == "X" else "X"
        
        # Verificação final de vitória
        if last_move and sim_board.is_won(last_move[0], last_move[1], "O" if current_player == "X" else "X"):
            return 1 if ("O" if current_player == "X" else "X") == self.current_player else 0
        return 0  # Empate
    
    def backpropagation(self, node, result):
        """Propaga os resultados da simulação pela árvore"""
        current_node = node
        while current_node is not None:
            current_node.visits += 1
            if (current_node.current_player == self.current_player and result == 1) or \
               (current_node.current_player != self.current_player and result == 0):
                current_node.wins += 1
            current_node = current_node.parent

    def best_move(self):
        """Executa o MCTS e retorna o melhor movimento"""
        for _ in range(self.simulation_limit):
            leaf = self.selection()
            self.expansion(leaf)
            result = self.simulation(leaf)
            self.backpropagation(leaf, result)

        # Retorna o movimento do nó mais visitado
        best_child = max(self.root.children, key=lambda x: x.visits)
        return best_child