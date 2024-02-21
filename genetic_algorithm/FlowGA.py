from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.genetic_operators.selections.elitism_selection import ElitismSelection
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation

from Board import Board
from genetic_algorithm.FlowCreator import FlowCreator
from genetic_algorithm.FlowCrossover import FlowCrossover
from genetic_algorithm.FlowEvaluator import FlowEvaluator
from genetic_algorithm.FlowNColorsMutation import FlowNColorsMutation
from genetic_algorithm.FlowTerminationChecker import FlowTerminationChecker

board = Board(5, 5, [((0,0),(4,1)), ((0,2),(3,1)), ((0,4),(3,3)), ((1,2),(4,2)), ((1,4),(4,3))])
board = Board(7, 7, [((0,6),(6,5)), ((1,5),(2,1)), ((1,6),(5,4)), ((3,3),(4,2)), ((3,4),(6,6)),
                                            ((5,5),(4,4))])
board = Board(10, 10, [((1,1),(6,8)), ((3,0),(9,8)), ((8,8),(2,6)), ((2,7),(6,7)), ((8,1),(8,7)),
                                            ((9,7),(6,2)), ((5,0),(5,4)), ((5,1),(3,3)), ((3,4),(6,5)), ((8,4),(8,2))])
creator = FlowCreator(board.rows, board.columns, board.dots)

algo = SimpleEvolution(
        Subpopulation(creators=creator,
                      population_size=5000,
                      # user-defined fitness evaluation method
                      evaluator=FlowEvaluator(board.rows, board.columns),
                      # maximization problem (fitness is sum of values), so higher fitness is better
                      higher_is_better=False,
                      elitism_rate=1/2500,
                      # genetic operators sequence to be applied in each generation
                      operators_sequence=[
                          FlowCrossover(board.rows, board.columns, board.colors, random_partition_size=True,
                                        probability=1),
                          # FlowCrossover(board.rows, board.columns, board.colors, random_partition_size=True,
                          #               probability=0.1),
                          FlowNColorsMutation(board.colors, board.rows, board.columns, creator.generate_path,
                                              n=1, probability=0.4),
                          # FlowNColorsMutation(board.colors, board.rows, board.columns, creator.generate_path,
                          #                     n=board.colors, probability=0.001),
                          # FlowNColorsMutation(board.colors, board.rows, board.columns, creator.generate_path,
                          #                     n=board.colors, probability=0.01)
                      ],
                      selection_methods=[
                          # (selection method, selection probability) tuple
                          (TournamentSelection(tournament_size=4, higher_is_better=False), 1)
                          # (ElitismSelection(num_elites=4, higher_is_better=False), 1)
                      ]),
        breeder=SimpleBreeder(),
        max_workers=20,
        max_generation=5000,
        statistics=BestAverageWorstStatistics(),
        termination_checker=FlowTerminationChecker()
    )

# evolve the generated initial population
algo.evolve()
# Execute (show) the best solution
result = algo.execute()

print(result)
