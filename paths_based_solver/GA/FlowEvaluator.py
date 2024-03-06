import math

from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from paths_based_solver.GA.BoardIndividual import BoardIndividual


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
        fitness is number of collisions between paths.

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
                value += colors * colors
        for i in range(self.rows):
            for j in range(self.columns):
                value += self.eval_cell(individual.get_cell(i, j))
        return value

    @staticmethod
    def eval_cell(colors_list):
        if len(colors_list) == 0:
            return 1
        if len(colors_list) == 1:
            return 0
        if any(color < 0 for color in colors_list):
            return math.inf
        return len(colors_list) - 1

# todo delete
    # def is_edge(self, cell):
    #     return cell[0] == 0 or cell[1] == 0 or cell[0] == self.rows - 1 or cell[1] == self.columns - 1
    #     # if cell[0] == 0:
    #     #     return 0
    #     # if cell[1] == 0:
    #     #     return 3
    #     # if cell[0] == self.rows - 1:
    #     #     return 2
    #     # if cell[1] == self.columns - 1:
    #     #     return 1
    #     # return -1
    #
    # def detect_deadend_path(self, color, individual):
    #     dots = individual.get_dots_of(color)
    #     start = dots[0]
    #     end = dots[1]
    #     path = self.find_path(color, individual, start, end)
    #     # detect bad squares
    #     if self.detect_squares(path, individual):
    #         # self.add_deadend_path(color, path)
    #         return True
    #     # detect dead end
    #     path_edge = [self.is_edge(v) for v in path]
    #     if path_edge.count(True) <= 1:
    #         return False
    #     for i in range(len(path)):
    #         if path_edge[i]:
    #             found = False
    #             for j in range(i + 1, len(path)):
    #                 if path_edge[j]:
    #                     found = True
    #                     if j != i + 1:
    #                         if self.is_deadend(path[i:j + 1], color, individual):
    #                             # self.add_deadend_path(color, path)
    #                             return True
    #                     break
    #             if not found:
    #                 return False
    #     return False
    #
    # def find_path(self, color, ind, start, end):
    #     visited = set()
    #     path = list()
    #
    #     curr_v = start
    #     # find the path
    #     while curr_v != end:
    #         visited.add(curr_v)
    #         path.append(curr_v)
    #         curr_neighbors = self.neighbors_dict[curr_v]
    #         found = False
    #         for neighbor in curr_neighbors:
    #             if (neighbor not in visited and
    #                     (color in ind.get_cell(neighbor[0], neighbor[1]) or
    #                      -color in ind.get_cell(neighbor[0], neighbor[1]))):
    #                 curr_v = neighbor
    #                 found = True
    #                 break
    #         if not found:
    #             raise Exception()
    #     path.append(curr_v)
    #     return path
    #
    # def is_deadend(self, path, color, ind):
    #     partition1 = set()
    #     partition2 = set()
    #     # divide to 2 connected components
    #     curr_cell = (0, 0)
    #     if curr_cell in path:
    #         raise Exception("(0,0) is on the path")
    #     self.recursive_divide_to_groups(curr_cell, partition1, path)
    #     for i in range(self.rows):
    #         for j in range(self.columns):
    #             curr_cell = (i, j)
    #             if curr_cell not in path and curr_cell not in partition1:
    #                 partition2.add(curr_cell)
    #
    #     return self.is_deadend_partition(partition1, partition2, color, ind)
    #
    # def recursive_divide_to_groups(self, curr_cell, partition1, path):
    #     if curr_cell in path:
    #         return
    #     if curr_cell in partition1:
    #         return
    #     partition1.add(curr_cell)
    #     for n in self.neighbors_dict[curr_cell]:
    #         if n not in partition1:
    #             self.recursive_divide_to_groups(n, partition1, path)
    #
    # @staticmethod
    # def is_deadend_partition(partition1, partition2, path_color, ind):
    #     colors = ind.get_colors()
    #     has_dot = [False, False]
    #     for color in range(1, colors):
    #         if color == path_color:
    #             continue
    #         dots = ind.get_dots_of(color)
    #         if dots[0] in partition1 and dots[1] in partition2:
    #             return True
    #         if dots[0] in partition2 and dots[1] in partition1:
    #             return True
    #         if dots[0] in partition1:
    #             has_dot[0] = True
    #         else:
    #             has_dot[1] = True
    #     if has_dot[0] is False or has_dot[1] is False:
    #         return True
    #     return False
    #
    # def detect_squares(self, path, ind):
    #     for cell in path:
    #         r = cell[0]
    #         c = cell[1]
    #         # square type |- _|
    #         if (r + 2 < self.rows and c + 2 < self.columns and (r + 1, c) in path and (r, c + 1) in path and
    #             (r + 2, c + 1) in path and (r + 2, c + 2) in path and (r + 1, c + 2) in path):
    #             return True
    #         # square type L -|
    #         if (r - 2 < self.rows and c + 2 < self.columns and (r - 1, c) in path and (r, c + 1) in path and
    #             (r - 2, c + 1) in path and (r - 2, c + 2) in path and (r - 1, c + 2) in path):
    #             return True
    #         # square type |_-
    #         if (r + 2 < self.rows and c + 1 < self.columns and (r + 1, c) in path and (r + 2, c) in path and
    #             (r, c + 1) in path and (r + 2, c + 1) in path and not ind.is_dot_cell(r + 1, c + 1)):
    #             return True
    #         # square type -_|
    #         if (r + 2 < self.rows and c + 1 < self.columns and (r, c + 1) in path and
    #             (r + 1, c + 1) in path and (r + 2, c + 1) in path and (r + 2, c) in path and not ind.is_dot_cell(r + 1, c)):
    #             return True
    #         # square type |_|
    #         if (r + 1 < self.rows and c + 2 < self.columns and (r + 1, c) in path and (r + 1, c + 1) in path and
    #             (r + 1, c + 2) in path and (r, c + 2) in path and not ind.is_dot_cell(r, c + 1)):
    #             return True
    #         # square type |-|
    #         if (r + 1 < self.rows and c + 2 < self.columns and (r + 1, c) in path and (r, c + 1) in path and
    #             (r, c + 2) in path and (r + 1, c + 2) in path and not ind.is_dot_cell(r + 1, c + 1)):
    #             return True
    #     return False
    #
    # # def add_deadend_path(self, color, path):
    # #     self.deadend_paths.add((color, tuple(path)))
