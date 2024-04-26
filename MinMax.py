
from Board import *
from Player import Player

def minmax(board: GameBoard, depth: int, current_player: Player, starting_player: Player, enemy: Player) -> float:
    # print("Board on start processing algorithm")
    # board.display_board()
    if(depth == 0 or board.is_no_more_possible_moves()):
        return (board.get_score(starting_player), None)

    if(board.check_player_win(starting_player.player_number)):
        return (float('inf'), None)
    
    if(board.check_player_win(enemy.player_number)):
        return (float('-inf'), None)
    
    if(current_player == starting_player):
        max_score = float('-inf')
        best_move = None
        possible_moves = board.get_possible_moves(current_player.player_number)
        for move in possible_moves:
            board.make_move(move)
            score, previuos_best_move = minmax(
                board,
                depth - 1,
                enemy,
                starting_player,
                enemy
            )
            # print(f'Score for starting player: {starting_player.player_number} || score: {score}')
            board.undo_move(move)
            if(score > max_score):
                max_score = score
                best_move = move
       
        return (max_score, best_move)

    else:
        min_score = float('inf')
        min_move = None
        possible_moves = board.get_possible_moves(current_player.player_number)
        for move in possible_moves:
            board.make_move(move)
            score, previous_best_move = minmax(
                board,
                depth - 1,
                starting_player,
                starting_player,
                enemy
            )
            # print(f'Score for enemy player: {enemy.player_number} || score: {score}')
            board.undo_move(move)
            if(score < min_score):
                min_score = score
                min_move = move
        
        return (min_score, min_move)


def minmax_alfabeta(board: GameBoard, depth: int, current_player: Player, starting_player: Player, enemy: Player, alpha: float, beta: float) -> float:
    # print("Board on start processing algorithm")
    # board.display_board()
    if(depth == 0 or board.is_no_more_possible_moves()):
        return (board.get_score(starting_player), None)

    if(board.check_player_win(starting_player.player_number)):
        return (float('inf'), None)
    
    if(board.check_player_win(enemy.player_number)):
        return (float('-inf'), None)
    
    if(current_player == starting_player):
        max_score = float('-inf')
        best_move = None
        possible_moves = board.get_possible_moves(current_player.player_number)
        for move in possible_moves:
            board.make_move(move)
            score, previous_best_move = minmax_alfabeta(
                board,
                depth - 1,
                enemy,
                starting_player,
                enemy,
                alpha,
                beta,
            )
            # print(f'Score for starting player: {starting_player.player_number} || score: {score}')
            board.undo_move(move)
            if(score > max_score):
                max_score = score
                best_move = move
            alpha = max(alpha, score)
            if(beta <= alpha):
                break
       
        return (max_score, best_move)

    else:
        min_score = float('inf')
        min_move = None
        possible_moves = board.get_possible_moves(current_player.player_number)
        for move in possible_moves:
            board.make_move(move)
            score, previuos_min_move = minmax_alfabeta(
                board,
                depth - 1,
                starting_player,
                starting_player,
                enemy,
                alpha,
                beta,
            )
            # print(f'Score for enemy player: {enemy.player_number} || score: {score}')
            board.undo_move(move)
            if(score < min_score):
                min_score = score
                min_move = move
            beta = min(beta, score)
            if(beta <= alpha):
                break
        
        return (min_score, min_move)