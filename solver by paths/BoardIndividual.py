import copy

from eckity.individual import Individual


class BoardIndividual(Individual):
    def __init__(self, rows, columns, dots, fitness):
        """

        :param rows:
        :param columns:
        :param dots: dots[0] is a dummy element.
        :param fitness:
        """
        super().__init__(fitness)
        self.colors = len(dots)  # colors = {1,...,self._colors-1}
        self.dots = dots
        self.board = [[list() for _ in range(columns)] for _ in range(rows)]
        self.init_board()
        self.has_path = [False for _ in range(self.colors)]

    def init_board(self):
        for i, tup in enumerate(self.dots):
            if i == 0:  # dummy element
                continue
            cell1 = tup[0]
            r1 = cell1[0]
            c1 = cell1[1]
            cell2 = tup[1]
            r2 = cell2[0]
            c2 = cell2[1]
            color = -1 * i  # dot cell
            self.board[r1][c1].append(color)
            self.board[r2][c2].append(color)

    def get_board(self):
        return self.board

    @staticmethod
    def init_neighbors(rows, columns):
        neighbors_dict = dict()
        is_in_bounds = lambda n: 0 <= n[0] < rows and 0 <= n[1] < columns
        for i in range(rows):
            for j in range(columns):
                curr_cell = (i, j)
                neighbors_all = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                neighbors = [neighbor for neighbor in neighbors_all if is_in_bounds(neighbor)]
                neighbors_dict[curr_cell] = neighbors
        return neighbors_dict

    def has_path_of(self, color):
        return self.has_path[color]

    def set_has_path_of(self, color, boolean):
        self.has_path[color] = boolean

    def get_colors(self):
        return self.colors

    def add_path(self, path, color):
        for cell in path:
            self.board[cell[0]][cell[1]].append(color)
        self.has_path[color] = True

    def get_cell(self, i, j):
        return self.board[i][j]
        # return copy.copy(self.board[i][j])

    def set_cell(self, i, j, colors_list):
        self.board[i][j] = colors_list

    def get_dots_of(self, color):
        return self.dots[color]

    def show(self):
        for row in self.board:
            for cell in row:
                print(cell, end=" "),
            print("", end="\n")

    def execute(self, *args, **kwargs):
        """
        Execute the board.
        Input is a numpy array or keyword arguments (but not both).

        Parameters
        ----------
        args : arguments
            A numpy array, this is mostly relevant to GP representation.

        kwargs : keyword arguments
            Input to program, this is mostly relevant to GP representation.

        Returns
        -------
        object
            Vector (genome) of this individual.
        """
        return self.has_path
