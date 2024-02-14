def has_circle(self, start_point: tuple[int, int], board):
    x, y = start_point
    visited = []
    color = Color.color_of(board[x, y])
    neighbors = copy.deepcopy(self._neighbors[color])
    curr_point = start_point
    while curr_point not in visited:
        visited.append(curr_point)
        for i, j in self._neighbors[start_point]:
            if board[i, j] == color:
                next_point = (i, j)
                if Color.is_dot(board[i, j]) and (i, j) != start_point:
                    # full path
                    return 5
                # delete edge
                n1 = neighbors[curr_point]
                n1.remove(next_point)
                n2 = neighbors[next_point]
                n2.remove(curr_point)
                curr_point = next_point
                continue
        return 0
    return -5


def get_start_points(self, board):
    return [(i, j) for i in range(self._board_size) for j in range(self._board_size) if board[i, j] < 0]


"""
def no_square(board, i, j):
    color = abs(board[i,j])
    if i+1 <= len(board) - 1:
        if j+1 <= len(board) - 1:
            if abs(board[i+1,j]) == color and abs(board[i,j+1]) == color and abs(board[i+1,j+1]) == color:
                return False
        if j-1 >= 0:
            if abs(board[i+1,j]) == color and abs(board[i,j-1]) == color and abs(board[i+1,j-1]) == color:
                return False
    if i-1 >= 0:
        if j + 1 <= len(board) - 1:
            if abs(board[i - 1, j]) == color and abs(board[i, j + 1]) == color and abs(board[i - 1, j + 1]) == color:
                return False
        if j - 1 >= 0:
            if abs(board[i - 1, j]) == color and abs(board[i, j - 1]) == color and abs(board[i - 1, j - 1]) == color:
                return False
    return True
"""


def find_square(self, board):
    rows, cols = np.shape(board)
    for i in range(rows - 1):
        for j in range(cols - 1):
            square = board[i:i + 2, j:j + 2]
            if np.all(square == square[0, 0]):
                return True
    return False