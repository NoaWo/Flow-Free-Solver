from solver_by_paths.Board import Board


class ArcConsistencyBoard(Board):
    def __init__(self, rows, columns, matrix, new_dots, original_dots):
        # dots has already the dummy tup
        super().__init__(rows, columns, original_dots)
        self.matrix = matrix
        self.new_dots = new_dots

    def is_solved(self):
        dots = self.new_dots[1:]
        finite_colors = [dot is True for dot in dots]
        return all(finite_colors)

    def get_solved_matrix(self):
        matrix = [[[-element] for element in row] for row in self.matrix]
        for cells in self.dots:
            if cells == ():
                continue
            dot1 = cells[0]
            dot2 = cells[1]
            matrix[dot1[0]][dot1[1]] = [-1 * matrix[dot1[0]][dot1[1]][0]]
            matrix[dot2[0]][dot2[1]] = [-1 * matrix[dot2[0]][dot2[1]][0]]
        return matrix
