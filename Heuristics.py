

def simple_score(board: list[list], player):
    score = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if(board[i][j] == player):
                score += 1
            elif(board[i][j] != 0):
                score -= 1
    return score