import copy
import random

from eckity.creators.creator import Creator
from eckity.fitness.simple_fitness import SimpleFitness

from BoardIndividual import BoardIndividual


class FlowCreator(Creator):
    def __init__(self, rows, columns, dots, fitness_type=SimpleFitness, events=None):
        if events is None:
            events = ["after_creation"]
        super().__init__(events, fitness_type)
        dummy_tup = ()
        dots.insert(0, dummy_tup)
        self.colors = len(dots)  # colors = {1,...,self._colors-1}
        self.rows = rows
        self.columns = columns
        self.dots = dots  # dots[0] is a dummy element
        self.type = BoardIndividual
        self.neighbors_in_board = BoardIndividual.init_neighbors(self.rows, self.columns)

    def create_individuals(self, n_individuals, higher_is_better=False):
        individuals = [self.type(rows=self.rows, columns=self.columns, dots=self.dots,
                                 fitness=self.fitness_type(higher_is_better=higher_is_better))
                       for _ in range(n_individuals)]
        for ind in individuals:
            self.create_individual(ind)
        self.created_individuals = individuals
        return individuals

    def create_individual(self, individual):
        for color in range(1, self.colors):
            if not individual.has_path_of(color):  # sanity check
                dots = self.dots[color]
                path = self.generate_path(dots[0], dots[1])
                if path is not None:
                    individual.add_path(path, color)

    def generate_path(self, start, end):
        return self.generate_path_static(self.neighbors_in_board, start, end, self.dots)

    def generate_path_with_attempts(self, start, end, attempts=5):
        for _ in range(attempts):
            result = self.generate_path_static(self.neighbors_in_board, start, end, self.dots)
            if result is not None:
                return result
        return None


    @staticmethod
    def generate_path_static(neighbors_in_board, start, end, dots):
        """

        :param neighbors_in_board:
        :param start:
        :param end:
        :return: path of cells or None if doesn't succeed
        """
        illegal_cells = set()
        for cells in dots:
            if cells == ():
                continue
            if cells == (start, end):
                continue
            illegal_cells.add(cells[0])
            illegal_cells.add(cells[1])
        path = [start]
        illegal_cells.add(start)
        curr_cell = start
        while curr_cell != end:
            curr_neighbors = copy.copy(neighbors_in_board[curr_cell])
            if end in curr_neighbors:
                next_cell = end
            else:
                next_cell = random.choice(curr_neighbors)
                while next_cell in illegal_cells:
                    curr_neighbors.remove(next_cell)
                    if len(curr_neighbors) == 0:
                        return None
                    next_cell = random.choice(curr_neighbors)
            path.append(next_cell)
            illegal_cells.add(next_cell)
            for neighbor in curr_neighbors:
                illegal_cells.add(neighbor)
            curr_cell = next_cell
        path = path[1:-1]
        return path
