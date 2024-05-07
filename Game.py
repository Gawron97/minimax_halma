
from copy import deepcopy
import time
from MinMax import *

class Game:
    def __init__(self, board: GameBoard) -> None:
        self.board = board
        self.root: Node = Node(deepcopy(board))

    
    def play_game(self, starting_player: Player, enemy: Player, depth, algorithm_name = "minmax"):
        current_player1: Player = starting_player
        current_player2: Player = enemy
        while(not self.board.is_no_more_possible_moves()):
            start_time = time.time()
            if(self.board.check_player_win(starting_player.player_number)):
                print(f'Player_{starting_player.player_number} win')
                return 
            if(self.board.check_player_win(enemy.player_number)):
                print(f'Player_{enemy.player_number} win')
                return
            
            move = self.find_best_move_for_player(current_player1, current_player2, depth, algorithm_name)
            if(move):
                self.board.make_move(move)
                self.board.display_board()
                print(f'player_{current_player1.player_number} {move}')
            else:
                print(f'No more moves for player_{current_player1.player_number}')
                break
            current_player1.playing_time += (time.time() - start_time)
            current_player1 = enemy if current_player1 == starting_player else starting_player
            current_player2 = starting_player if current_player1 == starting_player else enemy
        
        print("Game over")

    def find_best_move_for_player(self, current_player: Player, enemy: Player, depth, algorithm_name):

        if(algorithm_name == 'alfabeta'):
            (score, best_move) = minmax_alfabeta(
                    self.board,
                    depth,
                    current_player,
                    current_player,
                    enemy,
                    float('-inf'),
                    float('inf')
                )
        else:
            (score, best_move) = minmax(
                    self.board,
                    depth,
                    current_player,
                    current_player,
                    enemy
                )
        return (best_move)
    

    def play_game_exp(self, starting_player: Player, enemy: Player, depth, algorithm_name = "minmax") -> float:
        current_node = self.root
        current_player1: Player = starting_player
        current_player2: Player = enemy
        round = 0
        visited_nodes = 0

        while(True):
            round += 1
            start_time = time.time()

            if(current_node.board.check_player_win(starting_player.player_number)):
                print(f'Player_{starting_player.player_number} win')
                starting_player.isWin = True
                return visited_nodes
            if(current_node.board.check_player_win(enemy.player_number)):
                print(f'Player_{enemy.player_number} win')
                enemy.isWin = True
                return visited_nodes
            
            if(round > 10):
                depth = 2
            else:
                depth = 3
            
            if(round == 20):                
                round = 0

            current_player1.update_strategy()
            current_player2.update_strategy()
            print(f'player_{current_player1.player_number} strategy: {current_player1.actual_strategy} ratio: {current_player1.strategy_ratio} couter: {current_player1.counter}')
            print(f'player_{current_player2.player_number} strategy: {current_player2.actual_strategy} ratio: {current_player2.strategy_ratio} couter: {current_player2.counter}')
            
            current_node, current_visited_node = self.find_best_move_for_player_exp(current_player1, current_player2, depth, algorithm_name, current_node)
            self.delete_useless_nodes(current_node)
            visited_nodes += current_visited_node

            if(current_node.move):
                current_node.board.display_board()
                print(f'player_{current_player1.player_number} {current_node.move}')
                print(f'round: {round}')
                print(f'nodes visited: {current_visited_node}')
                print(f'node from start visited: {visited_nodes}')
            else:
                print(f'No more moves for player_{current_player1.player_number}')
                break
            
            current_player1.playing_time += (time.time() - start_time)
            current_player1, current_player2 = current_player2, current_player1

        print("Game over")
        return visited_nodes


    def find_best_move_for_player_exp(self, current_player: Player, enemy: Player, depth, algorithm_name, current_node: Node) -> Node:
        if(algorithm_name == 'alfabeta'):
            (max_score, best_node, visited_nodes) = minmax_alfabeta_exp(depth, current_player, current_player, enemy, float('-inf'), float('inf'), current_node, 0)
        else:
            (max_score, best_node, visited_nodes) = minmax_exp(depth, current_player, current_player, enemy, current_node, 0)

        return best_node, visited_nodes
    
    def delete_useless_nodes(self, node: Node):
        node.parent.children.remove(node)
        for child in node.parent.children:
            child.delete_node()
        del node.parent