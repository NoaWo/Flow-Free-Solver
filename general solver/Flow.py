import numpy as np
from random import randint


class Flow:
    def __init__(self, board, colors):
        self._board = np.array(board)
        self._board_as_vector = np.array(board).reshape(-1)
        self._colors = colors
        self._board_size = len(board)

    def get_board_as_vector(self):
        return self._board_as_vector

    def set_board(self, board, colors):
        self._board = np.array(board)
        self._board_as_vector = np.array(board).reshape(-1)
        self._colors = colors
        self._board_size = len(board)

    def creator(self, individual, index):
        if self._board_as_vector[index] < 0:
            return self._board_as_vector[index]
        else:
            return randint(1, self._colors)
