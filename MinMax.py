
from Board import *
from Player import Player

def minmax(board: GameBoard, depth: int, current_player: Player, starting_player: Player, enemy: Player) -> float:
    # print("Board on start processing algorithm")
    # board.display_board()
    if(depth == 0 or board.is_no_more_possible_moves()):
        return board.get_score(starting_player)

    if(board.check_player_win(starting_player.player_number)):
        return float('inf')
    
    if(board.check_player_win(enemy.player_number)):
        return float('-inf')
    
    if(current_player == starting_player):
        max_score = float('-inf')
        possible_moves = board.get_possible_moves(current_player.player_number)
        for move in possible_moves:
            board.make_move(move)
            score = minmax(
                board,
                depth - 1,
                enemy,
                starting_player,
                enemy
            )
            # print(f'Score for starting player: {starting_player.player_number} || score: {score}')
            board.undo_move(move)
            max_score = max(max_score, score)
       
        return max_score

    else:
        min_score = float('inf')
        possible_moves = board.get_possible_moves(current_player.player_number)
        for move in possible_moves:
            board.make_move(move)
            score = minmax(
                board,
                depth - 1,
                starting_player,
                starting_player,
                enemy
            )
            # print(f'Score for enemy player: {enemy.player_number} || score: {score}')
            board.undo_move(move)
            min_score = min(min_score, score)
        
        return min_score
