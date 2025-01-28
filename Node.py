from copy import deepcopy
from Board import GameBoard

class Node:
    def __init__(self, board, parent = None, move = None) -> None:
        self.board: GameBoard = board
        self.parent: Node = parent
        self.move = move
        self.children: list[Node] = []
        self.best_child: Node = None
        self.min_child: Node = None
        self.score = None
        self.move_explored = False

    def expand_moves(self, player_number):
        if(not self.move_explored):
            possible_moves = self.board.get_possible_moves(player_number)
            for move in possible_moves:
                new_board = deepcopy(self.board)
                new_board.make_move(move)
                child_node = Node(new_board, self, move)
                self.children.append(child_node)
            self.move_explored = True

    def delete_node(self):
        # Recursively delete all children
        for child in self.children:
            child.delete_node()
        # Remove references to children and other attributes
        self.children.clear()
        self.best_child = None
        self.min_child = None
        self.parent = None
        del self.board
        # Now delete the current node
        del self