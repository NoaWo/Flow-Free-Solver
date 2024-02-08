import random

from eckity.genetic_encodings.ga.vector_individual import Vector
from typing import List
from eckity.genetic_operators.mutations.vector_n_point_mutation import VectorNPointMutation


class FlowNPointMutation(VectorNPointMutation):
    """
    Uniform N Point Integer Mutation
    """
    def __init__(self, board_as_vector, board_size, n=1, probability=1.0, arity=1, events=None):
        super().__init__(probability=probability,
                         arity=arity,
                         mut_val_getter=lambda individual, index: individual.get_random_number_in_bounds(index),
                         events=events,
                         success_checker=self.default_success_checker,
                         n=n)
        self._board_as_vector = board_as_vector
        self._colors = board_size
        self._valid_cells = [i for i in range(len(board_as_vector)) if board_as_vector[i] >= 0]

    def default_cell_selector(self, vec: Vector) -> List[int]:
        # vector_indices = range(vec.size())
        return random.sample(self._valid_cells, k=self.n)

    # def success_checker(self, old_vec: Vector, new_vec: Vector):
    def default_success_checker(self, old_vec: Vector, new_vec: Vector) -> bool:
        vec = new_vec.get_vector()
        for i in range(new_vec.size()):
            if self._board_as_vector[i] < 0:
                if self._board_as_vector[i] != vec[i]:
                    return False
            else:
                if vec[i] < 1 or vec[i] > self._colors:
                    return False
        return True
