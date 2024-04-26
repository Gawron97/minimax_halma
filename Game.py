
import time
from Board import *
from MinMax import *

class Game:
    def __init__(self, board: GameBoard) -> None:
        self.board = board

    
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