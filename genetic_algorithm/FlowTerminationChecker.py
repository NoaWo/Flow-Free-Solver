from eckity.termination_checkers.termination_checker import TerminationChecker


class FlowTerminationChecker(TerminationChecker):
    def should_terminate(self, population, best_individual, gen_number):
        return best_individual.get_pure_fitness() == 0
