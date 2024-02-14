from eckity.termination_checkers.termination_checker import TerminationChecker


class FlowTerminationChecker(TerminationChecker):
    def __init__(self, evaluator):
        super().__init__()
        self._evaluator = evaluator

    def should_terminate(self, population, best_individual, gen_number):
        return self._evaluator.is_optimal(best_individual)