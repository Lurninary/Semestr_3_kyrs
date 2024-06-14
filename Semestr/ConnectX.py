import random

import numpy as np


class ConnectX():
    def __init__(self, row_size, column_size, connect_number, agent_1=None, agent_2=None):
        self.row_size = row_size if row_size > connect_number else connect_number
        self.column_size = column_size if column_size > connect_number else connect_number
        self.connect_number = connect_number

        self.players = []
        self.agents = [agent for agent in [agent_1, agent_2] if agent]
        if len(self.agents) > 0:
            for _, agent in enumerate(self.agents):
                self.players.append(_)
        for i in range(1):
            if len(self.players) != 2:
                self.players.append(f"player_{len(self.players)}")

        self.board = [[0 for _ in range(self.column_size)] for _ in range(self.row_size)]
        self.prev_board = []
        self.current_player = 1

    def print_board(self, board):
        for row in board:
            print(' '.join(map(str, row)))
        print('-'*self.column_size)

    def check_valid_moves(self):
        return [i for i in range(self.column_size) if self.board[0][i] == 0]

    def get_row(self, board, col):
        return [i for i in range(self.row_size - 1, -1, -1) if board[i][col] == 0]

    def drop_piece(self, column):
        self.prev_board = [row[:] for row in self.board]
        if column < 0 or column > self.column_size - 1:
            return False

        if len(self.get_row(self.board, column)) > 0:
            self.board[self.get_row(self.board, column)[0]][column] = self.current_player
        else:
            return False

        return True

    def step(self, column):
        if self.drop_piece(column):
            self.print_board(self.board)
            if len(self.check_valid_moves()) == 0:
                print(f"Draw!")
                return self.board, -1, True, {"player": self.current_player}
            if self.check_win(self.current_player, self.get_row(self.prev_board, column)[0], column)[0]:
                print(f"Player {self.current_player} wins!")
                return self.board, 1, True, {"player": self.current_player}
            self.current_player = 2 if self.current_player == 1 else 1
        else:
            print("Invalid move. Try again.")
            return self.board, -10, True, {"player": self.current_player}

        return self.board, 1 / (self.column_size * self.row_size), False, {"player": self.current_player}


    def check_win(self, player, row, col):
        count = 0

        for i in range(row, self.row_size):
            if self.board[i][col] == player:
                count += 1
            else:
                break

            if count >= self.connect_number:
                print(f"{player} - wins!(column)")
                return True, self.current_player

        for row in ''.join(map(str, self.board[row])).replace("0", "1" if player == 2 else "2").split(
                "1" if player == 2 else "2"):
            if len(row) >= self.connect_number:
                print(f"{player} - wins!(row)")
                return True, self.current_player

        for i in range(0, self.row_size - self.connect_number + 1, 1):

            for cur_col, num in enumerate(self.board[i]):
                count_left, count_right = 0, 0
                if self.current_player == num:
                    count_left += 1
                    count_right += 1

                    for j in range(1, self.connect_number, 1):
                        if cur_col + (self.connect_number - 1) < self.column_size:
                            if self.board[i + j][cur_col + j] == self.current_player:
                                count_right += 1
                        if cur_col - (self.connect_number - 1) >= 0:
                            if self.board[i + j][cur_col - j] == self.current_player:
                                count_left += 1

                if count_left >= self.connect_number or count_right >= self.connect_number:
                    print(f"{player} - wins!(diagonal)")
                    return True, self.current_player
        return False, self.current_player

    def reset(self):
        self.board = [[0 for _ in range(self.column_size)] for _ in range(self.row_size)]
        self.prev_board = []
        self.current_player = 1

        return self

    def play(self):
        print("Welcome to Connect X!")
        self.print_board(self.board)

        while True:
            for player in self.players:
                try:
                    column = int(input(
                        f"Player_{self.current_player} - Enter the column to drop piece (1-7): ")) - 1 if "player" in str(
                        player) else self.agents[player](self.board, self.row_size, self.column_size)
                    print(f"Player - {column + 1}" if "player" in str(player) else f"Agent_{player} - {column + 1}")

                    step = self.step(column)
                    if step[2]:
                        if step[1] == -1:
                            return 0
                        elif step[1] == -10:
                            return -self.current_player
                        else:
                            return self.current_player

                except ValueError:
                    print("Please enter a valid number.")
                    break


def agent_random(board, rows, columns):
    valid_moves = [i for i in range(columns) if board[0][i] == 0]


    return random.choice(valid_moves)


def agent_leftmost(board, rows, columns):
    valid_moves = [i for i in range(columns) if board[0][i] == 0]
    return valid_moves[0]

game = ConnectX(6, 7, 4, agent_1=agent_random, agent_2=agent_random)
game.play()