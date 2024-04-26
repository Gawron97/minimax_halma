


from Game import *

board = GameBoard(filename='starting_board_small.csv')
player1 = Player(player_number=1, actual_strategy="closer_to_enemy_base")
player2 = Player(player_number=2, actual_strategy="density_and_closer_to_enemy_base")

game = Game(board)
game.play_game_exp(player1, player2, 3, algorithm_name='alfabeta')
print(f'Player1 playing time: {player1.playing_time}')
print(f'Player2 playing time: {player2.playing_time}')