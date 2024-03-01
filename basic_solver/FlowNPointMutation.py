import random
import numpy as np
from eckity.genetic_encodings.ga.vector_individual import Vector
from typing import List
from eckity.genetic_operators.mutations.vector_n_point_mutation import VectorNPointMutation


class FlowNPointMutation(VectorNPointMutation):
    def __init__(self, board_as_vector, board_size, colors, evaluator, n=1, probability=1.0, is_smart=False, arity=1, events=None):
        super().__init__(probability=probability,
                         arity=arity,
                         mut_val_getter=lambda individual, index: individual.get_random_number_in_bounds(index),
                         events=events,
                         cell_selector=self.cell_selector,
                         success_checker=self.success_checker,
                         n=n)
        self._board_as_vector = board_as_vector
        self._evaluator = evaluator
        self._colors = colors
        self._board_size = board_size
        self._valid_cells = [i for i in range(len(board_as_vector)) if board_as_vector[i] >= 0]
        if is_smart:
            self.cell_selector = self.smart_cell_selector

    def cell_selector(self, vec: Vector) -> List[int]:
        return random.sample(self._valid_cells, k=self.n)

    def smart_cell_selector(self, vec: Vector) -> List[int]:
        board = np.array(vec.get_vector()).reshape((self._board_size, self._board_size))
        defected_cells = [i for i in self._valid_cells if
                          self._evaluator.eval_cell(i // self._board_size, i % self._board_size, board) <= 0]
        k = self.n
        while len(defected_cells) < k and k > 1:
            k = k - 1
        return random.sample(defected_cells, k=k)

    def success_checker(self, old_vec: Vector, new_vec: Vector) -> bool:
        vec = new_vec.get_vector()
        for i in range(new_vec.size()):
            if self._board_as_vector[i] < 0:
                if self._board_as_vector[i] != vec[i]:
                    return False
            else:
                if vec[i] < 1 or vec[i] > self._colors:
                    return False
        return True
