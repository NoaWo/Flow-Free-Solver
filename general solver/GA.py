import numpy as np
from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.creators.ga_creators.int_vector_creator import GAIntVectorCreator
from eckity.genetic_operators.crossovers.vector_k_point_crossover import VectorKPointsCrossover
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation

from Flow import Flow
from FlowEvaluator import FlowEvaluator
from FlowNPointMutation import FlowNPointMutation
from FlowTerminationChecker import FlowTerminationChecker

board = [[-1, 0, -2, 0, -3],
         [0, 0, -4, 0, -5],
         [0, 0, 0, 0, 0],
         [0, -2, 0, -3, 0],
         [0, -1, -4, -5, 0]]
board = [[0, 0, 0, 0, 0, 0, -1],
         [0, 0, 0, 0, 0, -2, -3],
         [0, -2, 0, 0, 0, 0, 0],
         [0, 0, 0, -4, -5, 0, 0],
         [0, 0, -4, 0, -6, 0, 0],
         [0, 0, 0, 0, -3, -6, 0],
         [0, 0, 0, 0, 0, -1, -5]]
colors = 6
# board =[
# [0,0,0,0,0,0,0,0,0,0],
# [0,-1,0,0,0,0,0,0,0,0],
# [0,0,0,0,0,0,-3,-4,0,0],
# [-2,0,0,-8,-9,0,0,0,0,0],
# [0,0,0,0,0,0,0,0,0,0],
# [-7,-8,0,0,-7,0,0,0,0,0],
# [0,0,-6,0,0,-9,0,-4,-1,0],
# [0,0,0,0,0,0,0,0,0,0],
# [0,-5,-10,0,-10,0,0,-5,-3,0],
# [0,0,0,0,0,0,0,-6,-2,0]]
# colors = 10
board_size = len(board)
flow = Flow(board, colors)
evaluator = FlowEvaluator(board_size, colors)
termination_checker = FlowTerminationChecker(board_size)
algo = SimpleEvolution(
        Subpopulation(creators=GAIntVectorCreator(length=board_size * board_size, bounds=(1, colors),
                                                  gene_creator=flow.creator),
                      population_size=1000,
                      # user-defined fitness evaluation method
                      evaluator=evaluator,
                      # maximization problem (fitness is sum of values), so higher fitness is better
                      higher_is_better=True,
                      elitism_rate=1/500,
                      # genetic operators sequence to be applied in each generation
                      operators_sequence=[
                          VectorKPointsCrossover(probability=1, k=2),
                          FlowNPointMutation(board_as_vector=flow.get_board_as_vector(), board_size=board_size,
                                             colors=colors, evaluator=evaluator, probability=0.9, n=1, is_smart=False),
                          FlowNPointMutation(board_as_vector=flow.get_board_as_vector(), board_size=board_size,
                                             colors=colors, evaluator=evaluator, probability=0, n=3, is_smart=False),
                          FlowNPointMutation(board_as_vector=flow.get_board_as_vector(), board_size=board_size,
                                             colors=colors, evaluator=evaluator, probability=0.01, n=colors, is_smart=True),
                          # FlowNPointMutation(board_as_vector=flow.get_board_as_vector(), board_size=board_size,
                          #                   evaluator=evaluator, probability=0.1, n=4, is_smart=True)
                      ],
                      selection_methods=[
                          # (selection method, selection probability) tuple
                          (TournamentSelection(tournament_size=4, higher_is_better=True), 1)
                          # (ElitismSelection(num_elites=10, higher_is_better=True), 0)

                      ]),
        breeder=SimpleBreeder(),
        max_workers=15,
        max_generation=500,
        statistics=BestAverageWorstStatistics(),
        termination_checker=termination_checker
    )

# evolve the generated initial population
algo.evolve()
# Execute (show) the best solution
result = algo.execute()
solved_board = np.array(result).reshape((board_size, board_size))

print(solved_board)