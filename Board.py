

import csv
import random
from Heuristics import *
from Player import *


class GameBoard:
    def __init__(self, filename = None) -> None:
        self.size = 16
        if(filename):
            self.board: list[list] = self.initialize_board_from_csv(filename)
        else:
            self.board: list[list] = self.initialize_random_board()
        
        self.player1_zone: list[tuple] = self.get_player1_zone_test()
        self.player2_zone: list[tuple] = self.get_player2_zone_test()

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
    
    def get_player1_zone_test(self):
        zone: list[tuple] = []
        for i in range(12, 16):
            for j in range(0, i - 12  + 1):
                zone.append((i, j))
        print(zone)
        return zone

    def get_player2_zone_test(self):
        zone: list[tuple] = []
        for i in range(0, 4):
            for j in range(12 + i, 16):
                zone.append((i, j))
        print(zone)
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

    def display_board_with_cells(self):
        print("      " + "     ".join(str(x) for x in range(10)), end='')
        print("    " + "    ".join(str(x) for x in range(10, self.size)))
        print()
        print("   +" + "-----+" * self.size)
        for i in range(self.size):        
            print(f'{i:2} ', end='  ')    
            for j in range(self.size):
                if(self.board[i][j] == 0):
                    print(f' . ', end=' | ')
                else:    
                    print(f' {self.board[i][j]} ', end=' | ')
            print(f'  {i}')
            print("   +" + "-----+" * self.size)
        print()
        print("      " + "     ".join(str(x) for x in range(10)), end='')
        print("    " + "    ".join(str(x) for x in range(10, self.size)))
        print()

    def display_board(self):
        print("      " + "   ".join(str(x) for x in range(10)), end='')
        print("  " + "  ".join(str(x) for x in range(10, self.size)))
        print()
        for i in range(self.size):        
            print(f'{i:2} ', end='  ')    
            for j in range(self.size):
                if(self.board[i][j] == 0):
                    print(f' . ', end=' ')
                else:    
                    print(f' {self.board[i][j]} ', end=' ')
            print(f'  {i}')
        print()
        print("      " + "   ".join(str(x) for x in range(10)), end='')
        print("  " + "  ".join(str(x) for x in range(10, self.size)))
        print()

    def find_jumps(self, x, y, visited: set, initial_x, initial_y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        jumps = []
        visited.add((x, y))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if(0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] != 0):
                jump_x, jump_y = nx + dx, ny + dy
                if(0 <= jump_x < self.size and 0 <= jump_y < self.size and self.board[jump_x][jump_y] == 0):
                    if((jump_x, jump_y) not in visited):
                        visited.add((jump_x, jump_y))
                        jumps.append((initial_x, initial_y, jump_x, jump_y))
                        jumps.extend(self.find_jumps(jump_x, jump_y, visited, x, y))
        return jumps
                    


    def get_possible_moves(self, player_number):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for x in range(self.size):
            for y in range(self.size):
                if(self.board[x][y] == player_number):
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if(0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == 0):
                            moves.append((x, y, nx, ny))
                    moves.extend(self.find_jumps(x, y, set(), x, y))
                                

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
            case "density":
                return density(self.board, player)
            case "closer_to_enemy_base":
                return closer_to_enemy_base(self.board, player)
            case "density_and_closer_to_enemy_base":
                return density_and_closer_to_enemy_base(self.board, player)
            case "more_moves_strategy":
                return more_moves_strategy(self.board, player, self.get_possible_moves)
            case _:
                return simple_score(self.board, player)
        


