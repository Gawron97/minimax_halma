

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


board = GameBoard(filename='small_board_start.csv', small=True)
player1 = Player(player_number=1, actual_strategy=("all_density_and_closer_to_enemy_base", 90, 30), second_strategy=("width", 50, 10))
player2 = Player(player_number=2, actual_strategy=("more_jumps_and_closer_to_enemy_base", 80, 100))

game = Game(board)
visited_nodes = game.play_game_exp(player1, player2, 3, algorithm_name='alfabeta')
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
print(f'Node visited during all game: {visited_nodes}')

log_game_result("game_results.csv", winner, winner_strategies, winner_playing_time, looser, looser_strategies, looser_playing_time)


# def diagonal_coordinates(size):
#     diagonals = []

#     # Top-right to bottom-left diagonals
#     for d in range(-size + 1, size):
#         diagonal = []
#         for x in range(max(0, -d), min(size, size - d)):
#             y = x + d
#             diagonal.append((x, y))
#         diagonals.append(diagonal)

#     return diagonals


# diagonals = diagonal_coordinates(16)
# for diag in diagonals:
#     print(diag)