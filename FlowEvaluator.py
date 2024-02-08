import numpy as np

from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator


class FlowEvaluator(SimpleIndividualEvaluator):
    """ FIXME: commands
    Evaluator class for the Knapsack problem, responsible of defining a fitness evaluation method and evaluating it.
    In this example, fitness is the total price of the knapsack

    Attributes
    -------
    items: dict(int, tuple(int, float))
        dictionary of (item id: (weights, prices)) of the items
    """

    def __init__(self, board_size):
        super().__init__()
        self._board_size = board_size
        self._colors = board_size
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
        float
            The evaluated fitness value of the given individual.
        """

        board = individual.get_vector()
        board = np.array(board).reshape(self._board_size, self._board_size)

        value = 0

        for i in range(self._board_size):
            for j in range(self._board_size):
                curr_cell: tuple[int, int] = (i, j)
                curr_color = board[i, j]
                if curr_color == 0:
                    return -np.inf
                elif curr_color < 0:  # dot cell
                    # need to be exactly one neighbor in the same color
                    curr_color = -curr_color
                    neighbors_colors = [board[i, j] for (i, j) in self._neighbors[curr_cell]]
                    num_of_same_color = neighbors_colors.count(curr_color)
                    eval_cell = num_of_same_color == 1
                    # if num_of_same_color > 1:
                    #     eval_cell = -5
                    value += eval_cell
                else:
                    # need to be exactly two neighbor in the same color
                    neighbors_colors = [board[i, j] for (i, j) in self._neighbors[curr_cell]]
                    num_of_same_color = neighbors_colors.count(curr_color)
                    eval_cell = num_of_same_color == 2
                    if num_of_same_color > 1:
                        eval_cell = -2
                    value += eval_cell

        # fitness value is the total value of the bag
        return value
