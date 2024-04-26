

from math import sqrt
import random
from Player import Player


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
    return random.randint(-10, 10)

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
    return score

def closer_to_enemy_base(board: list[list], player: Player) -> float:
    score = 0
    if(player.player_number == 1):
        for x in range(len(board)):
            for y in range(len(board)):
                if(board[x][y] == player.player_number):
                    rows_distance = (x - 15) / 2
                    columns_distance = (y - 0) / 2
                    distance = sqrt(abs(rows_distance)) + sqrt(abs(columns_distance))
                    score += distance

    else:
        for x in range(len(board)):
            for y in range(len(board)):
                if(board[x][y] == player.player_number):
                    rows_distance = (x - 0) / 2
                    columns_distance = (y - 15) / 2
                    distance = sqrt(abs(rows_distance)) + sqrt(abs(columns_distance))
                    score += distance

    return score

def density_and_closer_to_enemy_base(board: list[list], player: Player) -> float:
    return density(board, player) + closer_to_enemy_base(board, player)


