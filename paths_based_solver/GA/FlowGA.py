from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation

from paths_based_solver.GA.FlowCreator import FlowCreator
from paths_based_solver.GA.FlowCrossover import FlowCrossover
from paths_based_solver.GA.FlowEvaluator import FlowEvaluator
from paths_based_solver.GA.FlowNColorsMutation import FlowNColorsMutation
from paths_based_solver.GA.FlowTerminationChecker import FlowTerminationChecker
from paths_based_solver.gui.FlowGUI import draw_board


class FlowGA:
    def __init__(self, arc_cons_board, population_size=500, max_generation=100, elitism_rate=1/1000):
        self.arc_board = arc_cons_board
        self.creator = FlowCreator(self.arc_board)
        self.evaluator = FlowEvaluator(self.arc_board.rows, self.arc_board.columns)
        self.termination_checker = FlowTerminationChecker()
        self.population_size = population_size
        self.max_generation = max_generation
        self.elitism_rate = elitism_rate
        self.algo = SimpleEvolution(
            Subpopulation(creators=self.creator,
                          population_size=self.population_size,
                          evaluator=self.evaluator,
                          higher_is_better=False,
                          elitism_rate=self.elitism_rate,
                          # genetic operators sequence to be applied in each generation
                          operators_sequence=[
                              FlowCrossover(self.arc_board.rows, self.arc_board.columns, self.arc_board.colors,
                                            random_partition_size=True, probability=1, is_smart=True),
                              # FlowCrossover(self.arc_board.rows, self.arc_board.columns, self.arc_board.colors,
                              #               random_partition_size=True, probability=0.005, is_smart=False),
                              FlowNColorsMutation(self.arc_board.colors, self.arc_board.rows, self.arc_board.columns,
                                                  self.creator.generate_path_with_attempts,
                                                  n=1, probability=0.15, is_smart=False),
                              FlowNColorsMutation(self.arc_board.colors, self.arc_board.rows, self.arc_board.columns,
                                                  self.creator.generate_path_with_attempts,
                                                  n=1, probability=0.90, is_good=True),
                              FlowNColorsMutation(self.arc_board.colors, self.arc_board.rows, self.arc_board.columns,
                                                  self.creator.generate_path_with_attempts,
                                                  n=1, probability=0.35, is_smart=True),
                          ],
                          selection_methods=[
                              # (selection method, selection probability) tuple
                              (TournamentSelection(tournament_size=4, higher_is_better=False), 1)
                              # (ElitismSelection(num_elites=4, higher_is_better=False), 1)
                          ]),
            breeder=SimpleBreeder(),
            max_workers=20,
            max_generation=self.max_generation,
            statistics=BestAverageWorstStatistics(),
            termination_checker=self.termination_checker
        )

    def get_solved_matrix(self, board):
        original_dots = self.arc_board.dots
        # original_dots = FlowCreator.convert_to_set(self.arc_board.dots)
        matrix = [[[abs(color) for color in colors_list] for colors_list in row] for row in board]
        for color, cells in enumerate(original_dots):
            if color == 0:
                continue
            cell1 = cells[0]
            cell2 = cells[1]
            if (len(matrix[cell1[0]][cell1[1]]) == 0 or len(matrix[cell1[0]][cell1[1]]) > 1 or
                matrix[cell1[0]][cell1[1]][0] != color):
                raise Exception("Invalid cell")
            if (len(matrix[cell2[0]][cell2[1]]) == 0 or len(matrix[cell2[0]][cell2[1]]) > 1 or
                matrix[cell2[0]][cell2[1]][0] != color):
                raise Exception("Invalid cell")
            matrix[cell1[0]][cell1[1]] = [-color]
            matrix[cell2[0]][cell2[1]] = [-color]
        return matrix

    def run(self):
        # evolve the generated initial population
        self.algo.evolve()
        # Execute (show) the best solution
        board, result, fitness = self.algo.execute()

        print(result)
        print("Fitness: " + str(fitness))
        matrix_to_draw = self.get_solved_matrix(board)
        draw_board(matrix_to_draw)
        if fitness == 0:
            return True
        return False
