from eckity.termination_checkers.termination_checker import TerminationChecker


class FlowTerminationChecker(TerminationChecker):
    def __init__(self, board_size):
        super().__init__()
        self._max_fitness = board_size * board_size

    def should_terminate(self, population, best_individual, gen_number):
        return best_individual.get_pure_fitness() == self._max_fitness
