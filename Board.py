

import csv
import random
from Heuristics import *
from Player import Player


class GameBoard:
    def __init__(self, filename = None) -> None:
        self.size = 16
        if(filename):
            self.board: list[list] = self.initialize_board_from_csv(filename)
        else:
            self.board: list[list] = self.initialize_random_board()
        
        self.player1_zone: list[tuple] = self.get_player1_zone()
        self.player2_zone: list[tuple] = self.get_player2_zone()

        self.display_board()

    
    def initialize_random_board(self):
        board = [[0] * self.size for _ in range(self.size)]
        
        possible_places = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(possible_places)

        for _ in range(19):
            i, j = possible_places.pop()
            board[i][j] = 1
            i, j = possible_places.pop()
            board[i][j] = 2


        return board
        

    def initialize_board_from_csv(self, filename):
        board = []
        try:
            with open(filename, mode='r', newline='') as file:
                reader = csv.reader(file, delimiter=' ')
                for row in reader:
                    board.append([int(value) for value in row])
        except Exception as e:
            print("Blad podczas odczytywania csv, losuje ulozenie pionkow")
            return self.initialize_random_board()
        
        return board


    def get_player1_zone(self):
        zone: list[tuple] = []
        for i in range(10, 16):
            for j in range(0, i - 10 + 1):
                zone.append((i, j))
        return zone

    def get_player2_zone(self):
        zone: list[tuple] = []
        for i in range(0, 6):
            for j in range(10 + i, 16):
                zone.append((i, j))
        return zone
    
    def check_player1_win(self):
        for (i, j) in self.player2_zone:
            if(self.board[i][j] != 1):
                return False
        return True
    
    def check_player_win(self, player):
        if(player == 1):
            fields_to_check = self.player2_zone
        else:
            fields_to_check = self.player1_zone
        
        for (i, j) in fields_to_check:
            if(self.board[i][j] != player):
                return False
        return True

    def check_player2_win(self):
        for (i, j) in self.player1_zone:
            if(self.board[i][j] != 2):
                return False
        return True

    def display_board(self):
        for i in range(self.size):            
            for j in range(self.size):
                print(f'{self.board[i][j]}  ', end='')
            print()

    def get_possible_moves(self, player_number):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for x in range(self.size):
            for y in range(self.size):
                if(self.board[x][y] == player_number):
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if(0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == 0):
                            moves.append((x, y, nx, ny))

        random.shuffle(moves)
        return moves
    
    def is_no_more_possible_moves(self):
        return not self.get_possible_moves(1) or not self.get_possible_moves(2)


    def make_move(self, move):
        start_x, start_y, end_x, end_y = move
        self.board[end_x][end_y] = self.board[start_x][start_y]
        self.board[start_x][start_y] = 0

    def undo_move(self, move):
        start_x, start_y, end_x, end_y = move
        self.board[start_x][start_y] = self.board[end_x][end_y]
        self.board[end_x][end_y] = 0

    def get_score(self, player: Player) -> float:
        match(player.actual_strategy):
            case "simple":
                return simple_score(self.board, player)
            case "rand":
                return rand()
            case _:
                return simple_score(self.board, player)
        


GameBoard()