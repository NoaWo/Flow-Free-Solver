import copy

from solver_by_paths.ArcConsistency import ArcConsistency
from solver_by_paths.Board import Board
from solver_by_paths.FlowGA import FlowGA
from solver_by_paths.FlowGUI import draw_board


board1 = Board(5, 5, [((0,0),(4,1)), ((0,2),(3,1)), ((0,4),(3,3)), ((1,2),(4,2)), ((1,4),(4,3))])
board2 = Board(7, 7, [((0,6),(6,5)), ((1,5),(2,1)), ((1,6),(5,4)), ((3,3),(4,2)), ((3,4),(6,6)),
                                            ((5,5),(4,4))])
board3 = Board(10, 10, [((1,1),(6,8)), ((3,0),(9,8)), ((8,8),(2,6)), ((2,7),(6,7)), ((8,1),(8,7)),
                                           ((9,7),(6,2)), ((5,0),(5,4)), ((5,1),(3,3)), ((3,4),(6,5)), ((8,4),(8,2))])
board4 = Board(10, 10, [((0,0),(3,3)), ((1,0),(3,2)), ((2,0),(8,8)), ((4,0),(0,3)), ((4,2),(6,3)),
                                           ((6,1),(8,2)), ((1,6),(5,7)), ((3,5),(1,8)), ((2,5),(2,8)), ((3,8),(6,9))])

def main():
    quit = False  # todo delete this var when implement input
    while True:
        # todo while true : input of which board from database or quit
        input_board = board4
        if input_board == "quit" or quit:
            break
        board = input_board  # todo convert input to board
        arc_cons = ArcConsistency(copy.deepcopy(board))
        new_board = arc_cons.convert_to_smaller_problem()
        if new_board.is_solved():
            print("Solution by Arc Consistency")
            solved_matrix = new_board.get_solved_matrix()
            draw_board(solved_matrix)
            quit = True
            continue
        else:
            ga = FlowGA(new_board)
            ga.run()
            # quit = True


if __name__ == "__main__":
    main()
