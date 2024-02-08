import numpy as np
from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.creators.ga_creators.bit_string_vector_creator import GABitStringVectorCreator
from eckity.creators.ga_creators.int_vector_creator import GAIntVectorCreator
from eckity.genetic_operators.crossovers.vector_k_point_crossover import VectorKPointsCrossover
from eckity.genetic_operators.mutations.vector_random_mutation import BitStringVectorFlipMutation, \
    IntVectorOnePointMutation
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation

from examples.vectorga.knapsack.knapsack_evaluator import KnapsackEvaluator, NUM_ITEMS

from Color import Color
from Flow import Flow
from FlowEvaluator import FlowEvaluator
from FlowNPointMutation import FlowNPointMutation

board = [[-1, 0, -2, 0, -3],
         [0, 0, -4, 0, -5],
         [0, 0, 0, 0, 0],
         [0, -2, 0, -3, 0],
         [0, -1, -4, -5, 0]]
board_size = len(board)
flow = Flow(board)

algo = SimpleEvolution(
        Subpopulation(creators=GAIntVectorCreator(length=board_size * board_size, bounds=(1, board_size),
                                                  gene_creator=flow.creator),
                      population_size=500,
                      # user-defined fitness evaluation method
                      evaluator=FlowEvaluator(board_size),
                      # maximization problem (fitness is sum of values), so higher fitness is better
                      higher_is_better=True,
                      # genetic operators sequence to be applied in each generation
                      operators_sequence=[
                          VectorKPointsCrossover(probability=0.75, k=2),
                          FlowNPointMutation(board_as_vector=flow.get_board_as_vector(), board_size=board_size,
                                             probability=0.1, n=3)
                      ],
                      selection_methods=[
                          # (selection method, selection probability) tuple
                          (TournamentSelection(tournament_size=4, higher_is_better=True), 1)
                      ]),
        breeder=SimpleBreeder(),
        max_workers=1,
        max_generation=100,
        statistics=BestAverageWorstStatistics()
    )

# evolve the generated initial population
algo.evolve()
# Execute (show) the best solution
result = algo.execute()
solved_board = np.array(result).reshape((board_size, board_size))

print(solved_board)