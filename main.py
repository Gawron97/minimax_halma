



from Game import *


board = GameBoard(filename='starting_board_small.csv')
player1 = Player(player_number=1, actual_strategy="closer_to_enemy_base", second_strategy='density')
player2 = Player(player_number=2, actual_strategy="more_moves_strategy", second_strategy='density_and_closer_to_enemy_base',
                  third_strategy='closer_to_enemy_base')

game = Game(board)
game.play_game_exp(player1, player2, 3, algorithm_name='alfabeta')
print(f'Player1 playing time: {player1.playing_time}')
print(f'Player2 playing time: {player2.playing_time}')

# score, best_moves, min_moves = minmax_alfabeta_moves(board, 6, player1, player1, player2, float('-inf'), float('inf'))
# print(best_moves)
# print(min_moves)