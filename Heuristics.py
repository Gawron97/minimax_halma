

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