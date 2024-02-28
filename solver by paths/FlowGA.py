import threading

from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.genetic_operators.selections.elitism_selection import ElitismSelection
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation

from Board import Board
from FlowCreator import FlowCreator
from FlowCrossover import FlowCrossover
from FlowEvaluator import FlowEvaluator
from FlowNColorsMutation import FlowNColorsMutation
from FlowTerminationChecker import FlowTerminationChecker
from FlowGUI import draw_board

board = Board(5, 5, [((0,0),(4,1)), ((0,2),(3,1)), ((0,4),(3,3)), ((1,2),(4,2)), ((1,4),(4,3))])
board = Board(7, 7, [((0,6),(6,5)), ((1,5),(2,1)), ((1,6),(5,4)), ((3,3),(4,2)), ((3,4),(6,6)),
                                            ((5,5),(4,4))])
board = Board(10, 10, [((1,1),(6,8)), ((3,0),(9,8)), ((8,8),(2,6)), ((2,7),(6,7)), ((8,1),(8,7)),
                                           ((9,7),(6,2)), ((5,0),(5,4)), ((5,1),(3,3)), ((3,4),(6,5)), ((8,4),(8,2))])
creator = FlowCreator(board.rows, board.columns, board.dots)
# deadend_paths = set()

algo = SimpleEvolution(
        Subpopulation(creators=creator,
                      population_size=3000,
                      # user-defined fitness evaluation method
                      evaluator=FlowEvaluator(board.rows, board.columns),
                                              #, deadend_paths=deadend_paths),
                      # maximization problem (fitness is sum of values), so higher fitness is better
                      higher_is_better=False,
                      elitism_rate=1/1000,
                      # genetic operators sequence to be applied in each generation
                      operators_sequence=[
                          FlowCrossover(board.rows, board.columns, board.colors, random_partition_size=True,
                                        probability=1, is_smart=True),
                          FlowCrossover(board.rows, board.columns, board.colors, random_partition_size=True,
                                        probability=0.05, is_smart=False),
                          # FlowCrossover(board.rows, board.columns, board.colors, random_partition_size=True,
                          #               probability=0.1),
                          FlowNColorsMutation(board.colors, board.rows, board.columns, creator.generate_path_with_attempts,
                                              n=1, probability=0.4, is_smart=False),
                      #, deadend_paths=deadend_paths),
                          FlowNColorsMutation(board.colors, board.rows, board.columns, creator.generate_path_with_attempts,
                                              n=1, probability=0.1, is_smart=True),
                      #, deadend_paths=deadend_paths),
                          # FlowNColorsMutation(board.colors, board.rows, board.columns, creator.generate_path_with_tries,
                          #                     n=3, probability=0.4, is_smart=True),
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
        max_generation=600,
        statistics=BestAverageWorstStatistics(),
        termination_checker=FlowTerminationChecker()
    )

# evolve the generated initial population
algo.evolve()
# Execute (show) the best solution
board, result, result1, fitness = algo.execute()

print(result)
print(result1)
print(fitness)
draw_board(board)

# results_lock = threading.Lock()
# results = []
#
#
# def run_genetic_algo():
#     # evolve the generated initial population
#     algo.evolve()
#     # Execute (show) the best solution
#     board, result, fitness = algo.execute()
#     results_lock.acquire()
#     results.append((board, fitness))
#     results_lock.release()
#
#
# threads = []
# RUNS = 5
# for i in range(RUNS):
#     thread = threading.Thread(target=run_genetic_algo)
#     threads.append(thread)
#
# for thread in threads:
#     thread.start()
#
# for thread in threads:
#     thread.join()
#
# best_index = results.index(min([res[1] for res in results]))
# best_board = results[best_index][0]
# draw_board(best_board)
