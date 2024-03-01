from solver_by_paths.ArcConsistencyBoard import ArcConsistencyBoard
from solver_by_paths.BoardIndividual import BoardIndividual


class ArcConsistency:
    def __init__(self, board):
        self.board = board
        self.dots = board.dots
        dummy_tup = ()
        self.dots.insert(0, dummy_tup)
        self.neighbors_dict = BoardIndividual.init_neighbors(board.rows, board.columns)
        self.matrix = [[0 for _ in range(board.columns)] for _ in range(board.rows)]
        self.queue = []
        self.init_queue()
        self.arc_consistency()

    def init_queue(self):
        for color, cells in enumerate(self.dots):
            if color == 0:
                continue
            cell1 = cells[0]
            cell2 = cells[1]
            self.matrix[cell1[0]][cell1[1]] = -color
            self.matrix[cell2[0]][cell2[1]] = -color
            self.queue.append(cell1)
            self.queue.append(cell2)

    def arc_consistency(self):
        while self.queue:
            curr_cell = self.queue.pop(0)
            curr_color = self.matrix[curr_cell[0]][curr_cell[1]]
            if curr_color == 0:
                continue
            if ((curr_color > 0 and self.has_all_neighbors(2, curr_cell)) or
                    (curr_color < 0 and self.has_all_neighbors(1, curr_cell))):
                continue
            neighbors = self.neighbors_dict[curr_cell]
            available_neighbors = [self.is_available(cell) for cell in neighbors]
            if available_neighbors.count(True) == 1:
                i = available_neighbors.index(True)
                cell = neighbors[i]
                self.matrix[cell[0]][cell[1]] = abs(self.matrix[curr_cell[0]][curr_cell[1]])
                self.queue.append(cell)
                for neighbor in neighbors:
                    self.queue.append(neighbor)

    def has_all_neighbors(self, num, cell):
        neighbors = self.neighbors_dict[cell]
        color = abs(self.matrix[cell[0]][cell[1]])
        neighbors_color = [abs(self.matrix[n[0]][n[1]]) == color for n in neighbors]
        return neighbors_color.count(True) == num

    def is_available(self, cell):
        return self.matrix[cell[0]][cell[1]] == 0

    def find_new_dot(self, old_dot, color):
        """

        :param old_dot:
        :param color:
        :return: new dot after arc consistency check or True if path is complete
        """
        visited = set()
        # path = list()
        curr_v = old_dot
        # find the path
        while True:
            visited.add(curr_v)
            # path.append(curr_v)
            curr_neighbors = self.neighbors_dict[curr_v]
            found = False
            for neighbor in curr_neighbors:
                if neighbor not in visited and abs(self.matrix[neighbor[0]][neighbor[1]]) == color:
                    curr_v = neighbor
                    found = True
                    if self.matrix[curr_v[0]][curr_v[1]] == -color:  # path is complete!
                        return True
            if not found:  # the path is end here
                return curr_v
        # path.append(curr_v)
        # return path

    def convert_to_smaller_problem(self):
        """

        :return: Board that represent the smaller problem, after arc consistency
        """
        # find new dots
        new_dots = []
        for color, cells in enumerate(self.dots):
            if color == 0:
                new_dots.append(cells)  # dummy tup
                continue
            dot1 = cells[0]
            dot2 = cells[1]
            new_dot1 = self.find_new_dot(dot1, color)
            if new_dot1 is True:
                new_cells = True  # path is complete
            else:
                new_dot2 = self.find_new_dot(dot2, color)
                new_cells = (new_dot1, new_dot2)
            new_dots.append(new_cells)
        # convert all cells in matrix to be <= 0
        new_matrix = [[-abs(element) for element in row] for row in self.matrix]
        return ArcConsistencyBoard(self.board.rows, self.board.columns, new_matrix, new_dots, self.dots)
