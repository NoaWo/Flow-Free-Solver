import math

from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from genetic_algorithm.BoardIndividual import BoardIndividual


class FlowEvaluator(SimpleIndividualEvaluator):
    """
    Evaluator class for flow puzzle, responsible of defining a fitness evaluation method and evaluating it.
    In our implementation, fitness is the sum of evaluations of each cell, while evaluation of cell is 1 if
    the cell has exactly 2 neighbors in the same color (or 1 if the sell is a dot) and 0 otherwise.
    """
    def __init__(self, rows, columns):
        super().__init__()
        self.rows = rows
        self.columns = columns
        self.neighbors_dict = BoardIndividual.init_neighbors(rows, columns)

    def evaluate_individual(self, individual):
        """
        Compute the fitness value of a given individual.

        Parameters
        ----------
        individual: BoardIndividual
            The individual to compute the fitness value for.

        Returns
        -------
        int
            The evaluated fitness value of the given individual.
        """
        value = 0
        colors = individual.get_colors()
        for color in range(1, colors):
            if not individual.has_path_of(color):
                # value += self.rows * self.columns
                value += 2 * colors
                # value += self.rows * self.columns / (colors - 1)
                # return math.inf
        for i in range(self.rows):
            for j in range(self.columns):
                value += self.eval_cell(individual.get_cell(i, j))
        return value

    @staticmethod
    def eval_cell(colors_list):
        if len(colors_list) == 0:  # todo
            return 1
        if len(colors_list) == 1:
            return 0
        if any(color < 0 for color in colors_list):  # can be replaced by if curr_list[0] < 0
            return math.inf
        return len(colors_list) - 1
