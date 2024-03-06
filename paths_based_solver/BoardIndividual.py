import copy

from eckity.individual import Individual


class BoardIndividual(Individual):
    def __init__(self, rows, columns, dots, basic_matrix, fixed_cells, fitness):
        """

        :param rows:
        :param columns:
        :param dots: dots[0] is a dummy element.
        :param fitness:
        """
        super().__init__(fitness)
        self.colors = len(dots)  # colors = {1,...,self._colors-1}
        self.dots = dots
        self.rows = rows
        self.columns = columns
        self.board = [[list() for _ in range(columns)] for _ in range(rows)]
        self.basic_matrix = basic_matrix
        self.fixed_cells = fixed_cells
        self.init_board()
        self.has_path = [self.dots[color] is True for color in range(self.colors)]
        self.fixed_colors = [color for color in range(1, self.colors) if self.has_path[color]]

    def init_board(self):
        for cell in self.fixed_cells:
            i = cell[0]
            j = cell[1]
            self.board[i][j].append(self.basic_matrix[i][j])

    def get_board(self):
        return self.board

    def get_fixed_cells(self):
        return copy.copy(self.fixed_cells)

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

    def get_has_path(self):
        return copy.copy(self.has_path)

    def get_colors(self):
        return self.colors

    def add_path(self, path, color):
        for cell in path:
            self.board[cell[0]][cell[1]].append(color)
        self.set_has_path_of(color, True)

    def get_cell(self, i, j):
        return self.board[i][j]
        # return copy.copy(self.board[i][j])

    def is_in_dots(self, cell):
        for cells in self.dots:
            if cells == () or cells is True:
                continue
            if cells[0] == cell or cells[1] == cell:
                return True
        return False

    def is_dot_cell(self, i, j):
        return self.is_in_dots((i, j))
        # return len(self.board[i][j]) == 1 and self.board[i][j][0] < 0 and self.is_in_dots((i, j))

    def is_fixed_cell(self, i, j):
        cell = (i, j)
        return cell in self.fixed_cells

    def is_fixed_color(self, color):
        return color in self.fixed_colors

    def set_cell(self, i, j, colors_list):
        self.board[i][j] = colors_list

    def get_dots_of(self, color):
        return self.dots[color]

    # def get_dots(self):
    #     return self.dots

    def show(self):
        """
        Displays the fixed board (not the original dots!) # todo fix?
        :return:
        """
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
        return self.board, self.has_path, self.get_pure_fitness()
