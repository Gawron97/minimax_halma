


from Game import *

board = GameBoard(filename='starting_board')
player1 = Player(player_number=1)
player2 = Player(player_number=2)

game = Game(board)
game.play_game(player1, player2, 2)