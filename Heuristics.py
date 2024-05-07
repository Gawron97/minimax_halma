

from math import sqrt
import random
from Player import Player

pawn_number = 19

def simple_score(board: list[list], player: Player) -> float:
    score = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if(board[i][j] == player.player_number):
                score += 1
            elif(board[i][j] != 0):
                score -= 1
    return score

def rand():
    return random.random()

#0 - 8 * ilosc pionkow
def density(board: list[list], player: Player) -> float:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    score = 0

    for x in range(len(board)):
        for y in range(len(board)):
            if(board[x][y] == player.player_number):
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if(0 <= nx < len(board) and 0 <= ny < len(board)):
                        if(board[nx][ny] == player.player_number):
                            score += 1
    return score / (8 * pawn_number)

#0 - 8 * ilosc pionkow
def all_density(board: list[list], player: Player) -> float:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    score = 0

    for x in range(len(board)):
        for y in range(len(board)):
            if(board[x][y] == player.player_number):
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if(0 <= nx < len(board) and 0 <= ny < len(board)):
                        if(board[nx][ny] != 0):
                            score += 1
    return score / (8 * pawn_number)

#0 - 5,47 * ilosc pionkow
def closer_to_enemy_base(board: list[list], player: Player, player1_zone: list[tuple], player2_zone: list[tuple]) -> float:
    score = 0
    if(player.player_number == 1):
        for x in range(len(board)):
            for y in range(len(board)):
                if(board[x][y] == player.player_number and (x, y) not in player2_zone):
                    rows_distance = (x - 15)
                    columns_distance = (y - 0)
                    distance = (abs(rows_distance) + abs(columns_distance)) ** (0.5)
                    score += distance

    else:
        for x in range(len(board)):
            for y in range(len(board)):
                if(board[x][y] == player.player_number and (x, y) not in player1_zone):
                    rows_distance = (x - 0)
                    columns_distance = (y - 15)
                    distance = (abs(rows_distance) + abs(columns_distance)) ** (0.5)
                    score += distance

    return score / (5.47 * pawn_number)

def density_and_closer_to_enemy_base(board: list[list], player: Player, player1_zone: list[tuple], player2_zone: list[tuple]) -> float:
    first_weight = (100 - player.strategy_ratio) / 100
    second_weight = player.strategy_ratio / 100
    return (density(board, player) * first_weight) + (closer_to_enemy_base(board, player, player1_zone, player2_zone) * second_weight) + winning_bonus(board, player)

def all_density_and_closer_to_enemy_base(board: list[list], player: Player, player1_zone: list[tuple], player2_zone: list[tuple]) -> float:
    first_weight = (100 - player.strategy_ratio) / 100
    second_weight = player.strategy_ratio / 100
    return (all_density(board, player) * first_weight) + (closer_to_enemy_base(board, player, player1_zone, player2_zone) * second_weight) + winning_bonus(board, player)


# 0 - ~40 * ilosc pionkow
def more_moves_strategy(board: list[list], player: Player, get_possible_moves) -> float:

    score = 0

    for x in range(len(board)):
        for y in range(len(board)):
            if(board[x][y] == player.player_number):
                score += len(get_possible_moves(player.player_number))

    return score / (40 * pawn_number)
    
def more_moves_and_closer_to_enemy_base(board: list[list], player: Player, get_possible_moves, player1_zone: list[tuple], player2_zone: list[tuple]) -> float:
    first_weight = (100 - player.strategy_ratio) / 100
    second_weight = player.strategy_ratio / 100
    return (more_moves_strategy(board, player, get_possible_moves) * first_weight) + (closer_to_enemy_base(board, player, player1_zone, player2_zone) * second_weight) + winning_bonus(board, player)

# 0 - 16 * ilosc pionkow
def more_jumps(board: list[list], player: Player, get_possible_jumps):
    score = 0
    for x in range(len(board)):
            for y in range(len(board)):
                if(board[x][y] == player.player_number):
                    score += len(get_possible_jumps(x, y, set(), x, y))
    return score / (16 * pawn_number)

def more_jumps_and_closer_to_enemy_base(board: list[list], player: Player, get_possible_jumps, player1_zone: list[tuple], player2_zone: list[tuple]) -> float:
    first_weight = (100 - player.strategy_ratio) / 100
    second_weight = player.strategy_ratio / 100
    return (more_jumps(board, player, get_possible_jumps) * first_weight) + (closer_to_enemy_base(board, player, player1_zone, player2_zone) * second_weight) + winning_bonus(board, player)


def winning_bonus(board: list[list], player: Player) -> float:
    score = 0
    if(player.player_number == 1):
        for i in range(0, 6):
            for j in range(10 + i, 16):
                if(board[i][j] == 1):
                    score += j - i
    else:
        for i in range(10, 16):
            for j in range(0, i - 10 + 1):
                if(board[i][j] == 2):
                    score += i - j
    return score

def width_2(board: list[list], player: Player) -> float:
    diagonals = []
    size = 16

    for d in range(-size + 1, size):
        diagonal = []
        for x in range(max(0, -d), min(size, size - d)):
            y = x + d
            diagonal.append((x, y))
        diagonals.append(diagonal)

    diagonal_pawns_count = []
    for coords in diagonals:
        count = sum(1 for x, y in coords if board[x][y] == player.player_number)
        diagonal_pawns_count.append(count)

    max_average = 0
    for i in range(len(diagonal_pawns_count) - 1):
        average = (diagonal_pawns_count[i] + diagonal_pawns_count[i + 1]) / 2
        max_average = max(max_average, average)
    
    return max_average

# 0 - 9 * ilosc pionkow
def width(board: list[list], player: Player) -> float:
    score = 0

    if(player.player_number == 1):
        critical_directions = [(-1, -1), (1, 1)]
        directions = [(0, -1), (1, -1), (1, 0)]
        for x in range(len(board)):
            for y in range(len(board)):
                if(board[x][y] == player.player_number):
                    for dx, dy in critical_directions:
                        nx, ny = x + dx, y + dy
                        if(0 <= nx < len(board) and 0 <= ny < len(board)):
                            if(board[nx][ny] == player.player_number):
                                score += 3
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if(0 <= nx < len(board) and 0 <= ny < len(board)):
                            if(board[nx][ny] == player.player_number):
                                score += 1


    else:
        critical_directions = [(-1, -1), (1, 1)]
        directions = [(-1, 0), (-1, 1), (0, 1)]
        for x in range(len(board)):
            for y in range(len(board)):
                if(board[x][y] == player.player_number):
                    for dx, dy in critical_directions:
                        nx, ny = x + dx, y + dy
                        if(0 <= nx < len(board) and 0 <= ny < len(board)):
                            if(board[nx][ny] == player.player_number):
                                score += 3
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if(0 <= nx < len(board) and 0 <= ny < len(board)):
                            if(board[nx][ny] == player.player_number):
                                score += 1

    return score / pawn_number

def width_and_closer_to_enemy_base(board: list[list], player: Player, player1_zone: list[tuple], player2_zone: list[tuple]) -> float:
    first_weight = (100 - player.strategy_ratio) / 100
    second_weight = player.strategy_ratio / 100
    return (width(board, player) * first_weight) + (closer_to_enemy_base(board, player, player1_zone, player2_zone) * second_weight) + winning_bonus(board, player)