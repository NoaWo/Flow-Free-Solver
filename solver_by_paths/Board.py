class Board:
    def __init__(self, rows, columns, dots):
        self.rows = rows
        self.columns = columns
        self.dots = dots
        self.colors = len(dots)
