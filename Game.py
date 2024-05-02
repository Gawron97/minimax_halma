
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
    

    def play_game_exp(self, starting_player: Player, enemy: Player, depth, algorithm_name = "minmax"):
        current_node = self.root
        current_player1: Player = starting_player
        current_player2: Player = enemy
        round = 0

        while(True):
            round += 1
            start_time = time.time()

            if(current_node.board.check_player_win(starting_player.player_number)):
                print(f'Player_{starting_player.player_number} win')
                return 
            if(current_node.board.check_player_win(enemy.player_number)):
                print(f'Player_{enemy.player_number} win')
                return
            
            if(round == 20 or round == 40 or round == 60):
                current_player1.update_actual_strategy()
                current_player2.update_actual_strategy()
                print(f'player_{current_player1.player_number} strategy: {current_player1.actual_strategy}')
                print(f'player_{current_player2.player_number} strategy: {current_player2.actual_strategy}')
            
            current_node = self.find_best_move_for_player_exp(current_player1, current_player2, depth, algorithm_name, current_node)
            del current_node.parent

            if(current_node.move):
                current_node.board.display_board()
                print(f'player_{current_player1.player_number} {current_node.move}')
            else:
                print(f'No more moves for player_{current_player1.player_number}')
                break
            
            current_player1.playing_time += (time.time() - start_time)
            current_player1, current_player2 = current_player2, current_player1

        print("Game over")


    def find_best_move_for_player_exp(self, current_player: Player, enemy: Player, depth, algorithm_name, current_node: Node) -> Node:
        if(algorithm_name == 'alfabeta'):
            (max_score, best_node) = minmax_alfabeta_exp(depth, current_player, current_player, enemy, float('-inf'), float('inf'), current_node)
        else:
            (max_score, best_node) = minmax_exp(depth, current_player, current_player, enemy, current_node)

        return best_node