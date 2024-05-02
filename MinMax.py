
from Board import *
from Player import Player
from Node import Node

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
    
def minmax_exp(depth: int, current_player: Player, starting_player: Player, enemy: Player, node: Node) -> float:
    if(depth == 0):
        return (node.board.get_score(starting_player), None)
    
    if(node.board.check_player_win(starting_player.player_number)):
        return (float('inf'), None)
    
    if(node.board.check_player_win(enemy.player_number)):
        return (float('inf'), None)
    
    node.expand_moves(current_player.player_number)

    if(len(node.children) == 0):
        return (node.board.get_score(starting_player), None)
    
    if(current_player == starting_player):
        max_score = float('-inf')

        for child in node.children:
            score, previuos_best_node = minmax_exp(
                depth - 1,
                enemy,
                starting_player,
                enemy,
                child
            )
            if(score > max_score):
                max_score = score
                node.best_child = child
                node.score = max_score

        return (max_score, node.best_child)
    
    else:
        min_score = float('inf')

        for child in node.children:
            score, previous_min_node = minmax_exp(
                depth - 1,
                starting_player,
                starting_player,
                enemy,
                child
            )
            if(score < min_score):
                min_score = score
                node.min_child = child
                node.score = min_score

        return (min_score, node.min_child)

    
def minmax_alfabeta_exp(depth: int, current_player: Player, starting_player: Player, enemy: Player, alpha: float, beta: float, node: Node) -> float:
    if(depth == 0):
        return (node.board.get_score(starting_player), None)
    
    if(node.board.check_player_win(starting_player.player_number)):
        return (float('inf'), None)
    
    if(node.board.check_player_win(enemy.player_number)):
        return (float('inf'), None)
    
    node.expand_moves(current_player.player_number)

    if(len(node.children) == 0):
        return (node.board.get_score(starting_player), None)
    
    if(current_player == starting_player):
        max_score = float('-inf')

        for child in node.children:
            score, previuos_best_node = minmax_alfabeta_exp(
                depth - 1,
                enemy,
                starting_player,
                enemy,
                alpha,
                beta,
                child
            )
            if(score > max_score):
                max_score = score
                node.best_child = child
                node.score = max_score
            alpha = max(alpha, score)
            if(beta <= alpha):
                break
        return (max_score, node.best_child)
    
    else:
        min_score = float('inf')

        for child in node.children:
            score, previous_min_node = minmax_alfabeta_exp(
                depth - 1,
                starting_player,
                starting_player,
                enemy,
                alpha,
                beta,
                child
            )
            if(score < min_score):
                min_score = score
                node.min_child = child
                node.score = min_score
            beta = min(beta, score)
            if(beta <= alpha):
                break
        return (min_score, node.min_child)
    

# to jest tak naprawde jakbym wywolal bez patrzenia na przod. Bo jesli juz mam zewaluowane 2 najlepsze ruchy, to nie mam alternatyw i
# dla tego ruchu wywolam kolejna glebokosc, i jedyne jaki bedzie efekt to zachowam najlepszy lisc, ale on nie spojrzal na przod
def minmax_alfabeta_remember_only_best_move(depth: int, current_player: Player, starting_player: Player, enemy: Player, alpha: float, beta: float, node: Node):
    if(depth == 0 or node.board.is_no_more_possible_moves()):
        return (node.board.get_score(starting_player), None)
    
    if(node.board.check_player_win(starting_player.player_number)):
        return (float('inf'), None)
    
    if(node.board.check_player_win(enemy.player_number)):
        return (float('inf'), None)
    
    node.expand_moves(current_player.player_number)
    
    if(current_player == starting_player):
        max_score = float('-inf')

        for child in node.children:
            score, previuos_best_node = minmax_alfabeta_exp(
                depth - 1,
                enemy,
                starting_player,
                enemy,
                alpha,
                beta,
                child
            )
            if(score > max_score):
                max_score = score
                node.best_child = child
                node.score = max_score
            alpha = max(alpha, score)
            if(beta <= alpha):
                break
            node.children.remove(child)
        node.children.append(node.best_child)
        return (max_score, node.best_child)
    
    else:
        min_score = float('inf')

        for child in node.children:
            score, previous_min_node = minmax_alfabeta_exp(
                depth - 1,
                starting_player,
                starting_player,
                enemy,
                alpha,
                beta,
                child
            )
            if(score < min_score):
                min_score = score
                node.min_child = child
                node.score = min_score
            beta = min(beta, score)
            if(beta <= alpha):
                break
            node.children.remove(child)
        node.children.append(node.min_child)
        return (min_score, node.min_child)
    


# ta wersja nie ma zadnego sensu, bo ewaluujemy cala gre, czyli wszystkie mozliwosci. Lepiej ewaluowac kilka krokow na przod
# zapisac drzewo i potem zewaluowac od miejsca gdzie rzeczywiscie wykonalismy ruch, wtedy ucinamy sprawdzanie innych drog
def minmax_alfabeta_moves(board: GameBoard, depth: int, current_player: Player, starting_player: Player, enemy: Player, alpha: float, beta: float) -> float:
    # print("Board on start processing algorithm")
    # board.display_board()
    if(depth == 0 or board.is_no_more_possible_moves()):
        return (board.get_score(starting_player), [], [])

    if(board.check_player_win(starting_player.player_number)):
        return (float('inf'), [], [])
    
    if(board.check_player_win(enemy.player_number)):
        return (float('-inf'), [], [])
    
    best_moves = []
    min_moves = []
    
    if(current_player == starting_player):
        max_score = float('-inf')
        best_move = None
        possible_moves = board.get_possible_moves(current_player.player_number)
        
        previous_best_moves = []
        for move in possible_moves:
            board.make_move(move)
            score, potential_best_moves, potential_min_moves = minmax_alfabeta_moves(
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
                previous_best_moves = potential_best_moves
            alpha = max(alpha, score)
            if(beta <= alpha):
                break
        best_moves.extend(previous_best_moves)
        best_moves.append(best_move)
        min_moves = potential_min_moves
        return (max_score, best_moves, min_moves)

    else:
        min_score = float('inf')
        min_move = None
        possible_moves = board.get_possible_moves(current_player.player_number)
        
        previous_min_moves = []
        for move in possible_moves:
            board.make_move(move)
            score, potential_best_moves, potential_min_moves = minmax_alfabeta_moves(
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
                previous_min_moves = potential_min_moves
            beta = min(beta, score)
            if(beta <= alpha):
                break
        min_moves.extend(previous_min_moves)
        min_moves.append(min_move)
        best_moves = potential_best_moves
        return (min_score, best_moves, min_moves)