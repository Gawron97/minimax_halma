

import csv
import random
from Heuristics import *
from Player import *


class GameBoard:
    def __init__(self, filename = None, small = False) -> None:
        
        if(filename):
            self.board: list[list] = self.initialize_board_from_csv(filename)
        else:
            self.board: list[list] = self.initialize_random_board()
        
        if(small is False):
            self.size = 16
            self.player1_zone: list[tuple] = self.get_player1_zone()
            self.player2_zone: list[tuple] = self.get_player2_zone()
        else:
            self.size = 14
            self.player1_zone: list[tuple] = self.get_player1_zone_small()
            self.player2_zone: list[tuple] = self.get_player2_zone_small()
        

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
    
    def get_player1_zone_small(self):
        zone: list[tuple] = [(9, 0), (10, 0), (10, 1), (11, 0), (11, 1), (11, 2), (12, 0), (12, 1), (12, 2), (12, 3), (13, 0), (13, 1), (13, 2), (13, 3), (13, 4)]
        return zone

    def get_player2_zone_small(self):
        zone: list[tuple] = [(0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (1, 10), (1, 11), (1, 12), (1, 13), (2, 11), (2, 12), (2, 13), (3, 12), (3, 13), (4, 13)]
        return zone

    def get_player1_zone(self):
        zone: list[tuple] = [(12, 0), (12, 1), (13, 0), (13, 1), (13, 2), (14, 0), (14, 1), (14, 2), (14, 3), (15, 0), (15, 1), (15, 2), (15, 3), (15, 4)
                (16, 0), (16, 1), (16, 2), (16, 3), (16, 4)]
        return zone

    def get_player2_zone(self):
        zone: list[tuple] = [(0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (2, 12), (2, 13), (2, 14), (2, 15)
                (3, 13), (3, 14), (3, 15), (4, 14), (4, 15)]
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
                        jumps.extend(self.find_jumps(jump_x, jump_y, visited, initial_x, initial_y))
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
            case "all_density":
                return all_density(self.board, player)
            case "closer_to_enemy_base":
                return closer_to_enemy_base(self.board, player, self.player1_zone, self.player2_zone) + winning_bonus(self.board, player, self.player1_zone, self.player2_zone)
            case "density_and_closer_to_enemy_base":
                return density_and_closer_to_enemy_base(self.board, player, self.player1_zone, self.player2_zone)
            case "all_density_and_closer_to_enemy_base":
                return all_density_and_closer_to_enemy_base(self.board, player, self.player1_zone, self.player2_zone)
            case "more_moves_strategy":
                return more_moves_strategy(self.board, player, self.get_possible_moves)
            case "more_moves_and_closer_to_enemy_base":
                return more_moves_and_closer_to_enemy_base(self.board, player, self.get_possible_moves, self.player1_zone, self.player2_zone)
            case "more_jumps":
                return more_jumps(self.board, player, self.find_jumps)
            case "more_jumps_and_closer_to_enemy_base":
                return more_jumps_and_closer_to_enemy_base(self.board, player, self.find_jumps, self.player1_zone, self.player2_zone)
            case "width":
                return width(self.board, player) + winning_bonus(self.board, player, self.player1_zone, self.player2_zone)
            case "width_and_closer_to_enemy_base":
                return width_and_closer_to_enemy_base(self.board, player, self.player1_zone, self.player2_zone)
            case _:
                return simple_score(self.board, player)
        


