from enum import Enum, auto
import random
import sys


class BoardState(Enum):
    BLANK = auto()
    PLAYER = auto()
    CPU = auto()


class GameState(Enum):
    PLAYING = auto()
    PLAYER_WIN = auto()
    CPU_WIN = auto()
    DRAW = auto()


class Board():
    def __init__(self):
        # ボードの幅
        self.board_length = 3
        # マスの数
        self.board_area = self.board_length ** 2
        # 初期化
        self.board = [BoardState.BLANK] * self.board_area
        # 先攻:True、後攻:False
        self.is_player_turn = True
        # ゲームの状態
        self.state = GameState.PLAYING

    def display(self):
        print_length = len(str(self.board_area)) + 1
        for i in range(self.board_area):
            if self.board[i] == BoardState.PLAYER:
                print('o'.rjust(print_length), end='')
            elif self.board[i] == BoardState.CPU:
                print('x'.rjust(print_length), end='')
            else:
                print('{0:{print_length}d}'.format(
                    i, print_length=print_length), end='')
            if (i + 1) % self.board_length == 0:
                print()

    def input_player(self):
        while True:
            i = int(input())
            if i < 0 or i >= self.board_area or self.stone_exists(i) is True:
                print('error: invalid number')
                continue
            self.set_stone(i)
            break

    def input_cpu(self):
        idxs = [i for i, x in enumerate(self.board) if x == BoardState.BLANK]
        i = random.randint(0, len(idxs) - 1)
        self.set_stone(idxs[i])

    def stone_exists(self, i):
        return True if self.board[i] != BoardState.BLANK else False

    def set_stone(self, i):
        self.board[i] = BoardState.PLAYER if self.is_player_turn else BoardState.CPU
        self.update_state()
        self.next_turn()

    def next_turn(self):
        self.is_player_turn = not self.is_player_turn

    def judge(self, board_sub):
        return True if board_sub[0] != BoardState.BLANK and all([board_sub[0] == i for i in board_sub]) else False

    def update_state(self):
        if self.judge(self.board[0: self.board_area: self.board_length + 1]) or \
                self.judge(self.board[self.board_length - 1: (self.board_length - 1) * self.board_length + 1: self.board_length - 1]):
            if self.is_player_turn:
                self.state = GameState.PLAYER_WIN
            else:
                self.state = GameState.CPU_WIN
            return
        for i in range(self.board_length):
            if self.judge(self.board[i: self.board_area: self.board_length]) or \
                    self.judge(self.board[self.board_length * i: self.board_length * (i + 1)]):
                if self.is_player_turn:
                    self.state = GameState.PLAYER_WIN
                else:
                    self.state = GameState.CPU_WIN
                return
        if BoardState.BLANK not in self.board:
            self.state = GameState.DRAW
            return
        self.state = GameState.PLAYING


class TicTacToe(Board):
    def input_cpu(self):
        self.set_stone(self.minimax(0))

    def unset_stone(self, i):
        self.board[i] = BoardState.BLANK
        self.next_turn()

    def evaluate(self, depth):
        if self.state == GameState.CPU_WIN:
            self.state = GameState.PLAYING
            return 10 - depth
        elif self.state == GameState.PLAYER_WIN:
            self.state = GameState.PLAYING
            return depth - 10
        else:
            self.state = GameState.PLAYING
            return 0

    def minimax(self, depth):
        if self.state != GameState.PLAYING:
            return self.evaluate(depth)
        best_i = 0
        evaluation_value = sys.maxsize if self.is_player_turn else (
            -1) * sys.maxsize
        for i in range(self.board_area):
            if self.stone_exists(i) is False:
                self.set_stone(i)
                evaluation_value_tmp = self.minimax(depth + 1)
                if self.is_player_turn:
                    if evaluation_value_tmp > evaluation_value:
                        evaluation_value = evaluation_value_tmp
                        best_i = i
                else:
                    if evaluation_value_tmp < evaluation_value:
                        evaluation_value = evaluation_value_tmp
                        best_i = i
                self.unset_stone(i)
        if depth == 0:
            return best_i
        else:
            return evaluation_value

    def run(self):
        self.display()
        while self.state == GameState.PLAYING:
            msg = 'PLAYER' if self.is_player_turn else 'CPU'
            print(msg)
            if self.is_player_turn:
                self.input_player()
            else:
                self.input_cpu()
            self.display()
        msg = 'player win' if self.state == GameState.PLAYER_WIN else 'cpu win' if self.state == GameState.CPU_WIN else 'draw'
        print(msg)


if __name__ == "__main__":
    tictactoe = TicTacToe()
    tictactoe.run()
