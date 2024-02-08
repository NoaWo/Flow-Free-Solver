import numpy as np
from random import randint


class Flow():
    def __init__(self, board):
        self._board = board
        self._board_as_vector = np.array(board).reshape(-1)
        self._colors = len(board)

    def get_board_as_vector(self):
        return self._board_as_vector

    def creator(self, individual, index):
        if self._board_as_vector[index] < 0:
            return self._board_as_vector[index]
        else:
            return randint(1, self._colors)
