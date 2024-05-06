

import os
from Game import *

def log_game_result(filename, winner, winner_strategies, winner_playing_time, looser, looser_strategies, looser_playing_time):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write header only if file does not exist
        if not file_exists:
            writer.writerow(["Winner", "Winner Strategies", "Winner Playing Time", "Looser", "Looser Strategies", "Looser Playing Time"])
        writer.writerow([winner, winner_strategies, winner_playing_time, looser, looser_strategies, looser_playing_time])


board = GameBoard(filename='starting_board_small.csv')
player1 = Player(player_number=1, actual_strategy=("closer_to_enemy_base", 50))
player2 = Player(player_number=2, actual_strategy=("density_and_closer_to_enemy_base", 90))

game = Game(board)
game.play_game_exp(player1, player2, 3, algorithm_name='alfabeta')
if player1.isWin:
    winner = 'player1'
    winner_strategies = player1.strategies
    winner_playing_time = player1.playing_time
    looser = 'player2'
    looser_strategies = player2.strategies
    looser_playing_time = player2.playing_time
else:
    winner = 'player2'
    winner_strategies = player2.strategies
    winner_playing_time = player2.playing_time
    looser = 'player1'
    looser_strategies = player1.strategies
    looser_playing_time = player1.playing_time

print(f'{winner} Won')
print(f'{winner} playing time: {winner_playing_time} with strategy: {winner_strategies}')
print(f'{looser} playing time: {looser_playing_time} with strategy: {looser_strategies}')

log_game_result("game_results.csv", winner, winner_strategies, winner_playing_time, looser, looser_strategies, looser_playing_time)
