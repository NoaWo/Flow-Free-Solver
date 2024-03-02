import copy

from solver_by_paths.ArcConsistency import ArcConsistency
from solver_by_paths.Board import Board
from solver_by_paths.FlowGA import FlowGA
from solver_by_paths.FlowGUI import draw_board
from Board import boards
import random

def main():
    size = input('Which size of board would you like? (type a number between 5 and 13): ')
    pop = 100 if int(size) < 10 else 500
    gens = 10 if int(size) < 10 else 50
    gens_inc = int(gens * 0.5)
    pop_inc = int(pop * 0.5)
    board_options = boards[size]
    quit = False  # todo delete this var when implement input
    while True:
        input_board = board_options[random.randint(0, len(board_options) - 1)]
        if input_board == "quit" or quit:
            break
        board = input_board
        arc_cons = ArcConsistency(copy.deepcopy(board))
        new_board = arc_cons.convert_to_smaller_problem()
        if new_board.is_solved():
            print("Solution by Arc Consistency")
            solved_matrix = new_board.get_solved_matrix()
            draw_board(solved_matrix)
            quit = True
            continue
        else:
            ga = FlowGA(new_board, pop, gens)
            quit = ga.run()
            if quit:
                print(f'\nPuzzle solved with population: {pop} and generations: {gens}')
            if not quit:
                quit = input('try with more resources? enter y for yes: ') != 'y'
            pop += pop_inc
            gens += gens_inc


if __name__ == "__main__":
    main()
