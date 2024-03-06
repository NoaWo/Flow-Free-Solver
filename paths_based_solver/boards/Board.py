class Board:
    def __init__(self, rows, columns, dots):
        self.rows = rows
        self.columns = columns
        if dots[0] != ():
            dummy_tup = ()
            dots.insert(0, dummy_tup)
        self.dots = dots
        self.colors = len(dots)

    def get_matrix(self):
        matrix = [[[] for _ in range(self.columns)] for _ in range(self.rows)]
        for color, cells in enumerate(self.dots):
            if color == 0:
                continue
            cell1 = cells[0]
            cell2 = cells[1]
            matrix[cell1[0]][cell1[1]].append(-color)
            matrix[cell2[0]][cell2[1]].append(-color)
        return matrix
