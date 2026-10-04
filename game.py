"""Tic-Tac-Toe game engine."""
from copy import deepcopy

class TicTacToe:
    WIN_LINES = (
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    )
    def __init__(self, board=None):
        self.board = list(board) if board is not None else [" "]*9

    def display(self):
        b=self.board
        print(f" {b[0]} | {b[1]} | {b[2]}\n---+---+---\n {b[3]} | {b[4]} | {b[5]}\n---+---+---\n {b[6]} | {b[7]} | {b[8]}")

    def get_valid_moves(self):
        return [i for i,v in enumerate(self.board) if v==" "]

    def make_move(self, position, player):
        if position not in range(9) or self.board[position]!=" ":
            raise ValueError("Invalid move")
        self.board[position]=player

    def check_winner(self):
        for a,b,c in self.WIN_LINES:
            if self.board[a]!=" " and self.board[a]==self.board[b]==self.board[c]:
                return self.board[a]
        return None

    def is_draw(self):
        return self.check_winner() is None and not self.get_valid_moves()

    def is_terminal(self):
        return self.check_winner() is not None or self.is_draw()

    def copy(self):
        return TicTacToe(deepcopy(self.board))
