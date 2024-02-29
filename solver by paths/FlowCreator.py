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
                path = self.generate_path(dots[0], dots[1], color)
                if path is not None:
                    individual.add_path(path, color)

    def generate_path_with_attempts(self, start, end, color, attempts=5):
        for _ in range(attempts):
            result = self.generate_path(start, end, color)
            if result is not None:
                return result
        return None

    def generate_path(self, start, end, color):
        """

        :param neighbors_in_board:
        :param start:
        :param end:
        :return: path of cells or None if doesn't succeed
        """
        illegal_cells = set()
        for cells in self.dots:
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
            curr_neighbors = copy.copy(self.neighbors_in_board[curr_cell])
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
        if self.detect_deadend_path(path, color):
            return None
        path = path[1:-1]
        return path

    def is_edge(self, cell):
        return cell[0] == 0 or cell[1] == 0 or cell[0] == self.rows - 1 or cell[1] == self.columns - 1

    def detect_deadend_path(self, path, color):
        # detect bad squares
        if self.detect_squares(path):
            # self.add_deadend_path(color, path)
            return True
        # detect dead end
        path_edge = [self.is_edge(v) for v in path]
        if path_edge.count(True) <= 1:
            return False
        for i in range(len(path)):
            if path_edge[i]:
                found = False
                for j in range(i + 1, len(path)):
                    if path_edge[j]:
                        found = True
                        if j != i + 1:
                            if self.is_deadend(path[i:j + 1], color):
                                # self.add_deadend_path(color, path)
                                return True
                        break
                if not found:
                    return False
        return False

    def is_deadend(self, path, color):
        partition1 = set()
        partition2 = set()
        # divide to 2 connected components
        curr_cell = (0, 0)
        if curr_cell in path:
            raise Exception("(0,0) is on the path")
        self.recursive_divide_to_groups(curr_cell, partition1, path)
        for i in range(self.rows):
            for j in range(self.columns):
                curr_cell = (i, j)
                if curr_cell not in path and curr_cell not in partition1:
                    partition2.add(curr_cell)

        return self.is_deadend_partition(partition1, partition2, color)

    def recursive_divide_to_groups(self, curr_cell, partition1, path):
        if curr_cell in path:
            return
        if curr_cell in partition1:
            return
        partition1.add(curr_cell)
        for n in self.neighbors_in_board[curr_cell]:
            if n not in partition1:
                self.recursive_divide_to_groups(n, partition1, path)

    def is_deadend_partition(self, partition1, partition2, path_color):
        has_dot = [False, False]
        for color in range(1, self.colors):
            if color == path_color:
                continue
            dots = self.dots[color]
            if dots[0] in partition1 and dots[1] in partition2:
                return True
            if dots[0] in partition2 and dots[1] in partition1:
                return True
            if dots[0] in partition1:
                has_dot[0] = True
            else:
                has_dot[1] = True
        if has_dot[0] is False or has_dot[1] is False:
            return True
        return False

    def is_dot_cell(self, i, j):
        cell = (i, j)
        for d in self.dots:
            if d == ():
                continue
            if d[0] == cell or d[1] == cell:
                return True
        return False

    def detect_squares(self, path):
        for cell in path:
            r = cell[0]
            c = cell[1]
            # square type |- _|
            if (r + 2 < self.rows and c + 2 < self.columns and (r + 1, c) in path and (r, c + 1) in path and
                (r + 2, c + 1) in path and (r + 2, c + 2) in path and (r + 1, c + 2) in path):
                return True
            # square type L -|
            if (r - 2 < self.rows and c + 2 < self.columns and (r - 1, c) in path and (r, c + 1) in path and
                (r - 2, c + 1) in path and (r - 2, c + 2) in path and (r - 1, c + 2) in path):
                return True
            # square type |_-
            if (r + 2 < self.rows and c + 1 < self.columns and (r + 1, c) in path and (r + 2, c) in path and
                (r, c + 1) in path and (r + 2, c + 1) in path and not self.is_dot_cell(r + 1, c + 1)):
                return True
            # square type -_|
            if (r + 2 < self.rows and c + 1 < self.columns and (r, c + 1) in path and
                (r + 1, c + 1) in path and (r + 2, c + 1) in path and (
                r + 2, c) in path and not self.is_dot_cell(r + 1, c)):
                return True
            # square type |_|
            if (r + 1 < self.rows and c + 2 < self.columns and (r + 1, c) in path and (r + 1, c + 1) in path and
                 (r + 1, c + 2) in path and (r, c + 2) in path and not self.is_dot_cell(r, c + 1)):
                return True
            # square type |-|
            if (r + 1 < self.rows and c + 2 < self.columns and (r + 1, c) in path and (r, c + 1) in path and
                (r, c + 2) in path and (r + 1, c + 2) in path and not self.is_dot_cell(r + 1, c + 1)):
                return True
        return False

        # def add_deadend_path(self, color, path):
        #     self.deadend_paths.add((color, tuple(path)))


