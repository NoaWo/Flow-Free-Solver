import copy
import random

from paths_based_solver.arc_consistency.ArcConsistency import ArcConsistency
from paths_based_solver.GA.FlowGA import FlowGA
from paths_based_solver.gui.FlowGUI import draw_board
from Puzzles import boards


def main():
    sys_random = random.SystemRandom()
    while True:
        size = input('Choose size of puzzle (type a number between 5 and 12 or q for quit): ')
        while size not in ['5', '6', '7', '8', '9', '10', '11', '12', 'q']:
            print('Invalid input, please try again.')
            size = input('Choose size of puzzle (type a number between 5 and 12 or q for quit): ')
        if size == 'q':
            break
        board_options = boards[size]
        pop = 500 if int(size) < 10 else 1000
        gens = 30 if int(size) < 10 else 50
        pop_inc = int(pop)
        gens_inc = int(gens * 0.5)
        print('Choose random puzzle of size ' + str(size) + 'x' + str(size) + '...')
        input_board = sys_random.choice(board_options)
        print('Puzzle selected.')
        draw_board(input_board.get_matrix())
        print('Solve...')
        board = input_board
        arc_cons = ArcConsistency(copy.deepcopy(board))
        new_board = arc_cons.convert_to_smaller_problem()
        if new_board.is_solved():
            print("Puzzle solved by Arc Consistency")
            solved_matrix = new_board.get_solved_matrix()
            draw_board(solved_matrix)
            continue
        else:
            cont = True
            while cont:
                print("Population: " + str(pop))
                print("Generations: " + str(gens))
                ga = FlowGA(copy.deepcopy(new_board), pop, gens)
                is_solved = ga.run()
                if is_solved:
                    print(f'\nPuzzle solved with population: {pop} and generations: {gens}')
                    cont = False
                if not is_solved:
                    cont = input('Try again? press y for try with more population and generations, '
                                 'press c for try again same as before, press n for not try again: ')
                if cont == 'y':
                    pop += pop_inc
                    gens += gens_inc
                cont = cont == 'y' or cont == 'c'


if __name__ == "__main__":
    main()
