
from Board import *
from MinMax import *

class Game:
    def __init__(self, board: GameBoard) -> None:
        self.board = board

    
    def play_game(self, starting_player: Player, enemy: Player, depth, algorithm_name = "minmax"):
        current_player1: Player = starting_player
        current_player2: Player = enemy
        while(not self.board.is_no_more_possible_moves()):
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
                print(move)
            else:
                print(f'No more moves for player_{current_player1.player_number}')
                break

            current_player1 = enemy if current_player1 == starting_player else starting_player
            current_player2 = starting_player if current_player1 == starting_player else enemy
        
        print("Game over")

    def find_best_move_for_player(self, current_player: Player, enemy: Player, depth, algorithm_name):
        best_score = float('-inf')
        best_move = None
        possible_moves = self.board.get_possible_moves(current_player.player_number)

        for move in possible_moves:
            self.board.make_move(move)
            if(algorithm_name == 'alfabeta'):
                score = minmax_alfabeta(
                    self.board,
                    depth,
                    current_player,
                    current_player,
                    enemy,
                    float('-inf'),
                    float('inf')
                )
            else:
                score = minmax(
                    self.board,
                    depth,
                    current_player,
                    current_player,
                    enemy
                )

            self.board.undo_move(move)

            if(score > best_score):
                best_score = score
                best_move = move
        
        return best_move
