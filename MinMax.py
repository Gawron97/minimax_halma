
from Board import *

def minmax(board: GameBoard, depth, player, starting_player, enemy):
    if(depth == 0 or board.is_no_more_possible_moves()):
        pass

    if(board.check_player_win(starting_player)):
        return float('inf')
    
    if(board.check_player_win(enemy)):
        return float('-inf')
