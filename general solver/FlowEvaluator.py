import numpy as np
from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator

from Color import Color


class FlowEvaluator(SimpleIndividualEvaluator):
    """
    Evaluator class for flow puzzle, responsible of defining a fitness evaluation method and evaluating it.
    In our implementation, fitness is the sum of evaluations of each cell, while evaluation of cell is 1 if
    the cell has exactly 2 neighbors in the same color (or 1 if the sell is a dot) and 0 otherwise.
    """

    def __init__(self, board_size, colors):
        super().__init__()
        self._board_size = board_size
        self._colors = colors
        self._neighbors = {}
        self.init_neighbors()

    def init_neighbors(self):
        is_in_bounds = lambda n: 0 <= n[0] < self._board_size and 0 <= n[1] < self._board_size
        for i in range(self._board_size):
            for j in range(self._board_size):
                curr_cell: tuple[int, int] = (i, j)
                neighbors_all: list[tuple[int, int]] = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                neighbors = [neighbor for neighbor in neighbors_all if is_in_bounds(neighbor)]
                self._neighbors[curr_cell] = neighbors

    def evaluate_individual(self, individual):
        """
        Compute the fitness value of a given individual.

        Parameters
        ----------
        individual: Vector
            The individual to compute the fitness value for.

        Returns
        -------
        int
            The evaluated fitness value of the given individual.
        """

        board = individual.get_vector()
        board = np.array(board).reshape(self._board_size, self._board_size)

        value = 0

        for i in range(self._board_size):
            for j in range(self._board_size):
                value += self.eval_cell(i, j, board)
        return value

    def eval_cell(self, i, j, board):
        curr_cell: tuple[int, int] = (i, j)
        curr_node = board[i, j]
        if curr_node == 0:
            return -np.inf
        neighbors_colors = [Color.color_of(board[i, j]) for (i, j) in self._neighbors[curr_cell]]
        curr_color = Color.color_of(curr_node)
        if curr_node < 0:  # dot cell
            # need to be exactly one neighbor in the same color
            eval_cell = (neighbors_colors.count(curr_color) == 1)
            # eval_cell += self.find_path(board, i, j)
        else:
            # need to be exactly two neighbor in the same color
            eval_cell = neighbors_colors.count(curr_color) == 2 and self.no_square(board, i, j)
        return eval_cell

    def find_path(self, board, i, j):
        curr_cell = (i, j)
        curr_color = Color.color_of(board[i, j])
        visited = set()
        path_len = 0
        while curr_cell is not None:
            visited.add(curr_cell)
            path_len += 1
            for neighbor in self._neighbors[curr_cell]:
                neighbor_color = Color.color_of(board[neighbor[0]][neighbor[1]])
                if neighbor_color == curr_color and neighbor not in visited:
                    curr_cell = neighbor
                    break
            curr_cell = None
        return path_len - 1


    @staticmethod
    def no_square(board, i, j):
        color = Color.color_of(board[i, j])
        if i + 1 < len(board):
            if j + 1 < len(board):
                if (Color.color_of(board[i + 1, j]) == color and Color.color_of(board[i, j + 1]) == color and
                        Color.color_of(board[i + 1, j + 1]) == color):
                    return False
            if j - 1 >= 0:
                if (Color.color_of(board[i + 1, j]) == color and Color.color_of(board[i, j - 1]) == color and
                        Color.color_of(board[i + 1, j - 1]) == color):
                    return False
        if i - 1 >= 0:
            if j + 1 < len(board):
                if (Color.color_of(board[i - 1, j]) == color and Color.color_of(board[i, j + 1]) == color and
                        Color.color_of(board[i - 1, j + 1]) == color):
                    return False
            if j - 1 >= 0:
                if (Color.color_of(board[i - 1, j]) == color and Color.color_of(board[i, j - 1]) == color and
                        Color.color_of(board[i - 1, j - 1]) == color):
                    return False
        return True

    def is_optimal(self, individual):
        return self.evaluate_individual(individual) == self._board_size * self._board_size
        # return self.evaluate_individual(individual) == self._board_size * self._board_size + self._board_size
