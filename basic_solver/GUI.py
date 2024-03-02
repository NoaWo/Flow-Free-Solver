import tkinter as tk
from basic_solver.Color import Color


SQUARE_SIZE = 50
# CANVAS_SIZE = GRID_SIZE * SQUARE_SIZE
DISC_RADIUS = 20  # Adjust the radius as needed
DISC_COLOR = "red"  # Adjust the color as needed
LINE_COLOR = "blue"  # Adjust the color as needed
LINE_WIDTH = 18  # Adjust the line width as needed

plus_line_w = LINE_WIDTH / 2
outline_w = 1


def draw_board(matrix):
    root = tk.Tk()
    root.title("Flow Board")
    GRID_SIZE = len(matrix)
    CANVAS_SIZE = len(matrix) * SQUARE_SIZE
    canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="black")
    canvas.pack()

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x1, y1 = col * SQUARE_SIZE, row * SQUARE_SIZE
            x2, y2 = x1 + SQUARE_SIZE, y1 + SQUARE_SIZE

            # Draw the square with light yellow borders
            canvas.create_rectangle(x1, y1, x2, y2, outline="lightyellow", width=outline_w)

            # Calculate the center of the square
            center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2

            color = matrix[row][col]
            if color < 0:
                color_name = str(Color.get_color_by_number(-1 * color)).lower()

                # Draw a filled circle (disc) inside the square
                canvas.create_oval(center_x - DISC_RADIUS, center_y - DISC_RADIUS,
                                   center_x + DISC_RADIUS, center_y + DISC_RADIUS,
                                   fill=color_name, outline=color_name)
                # start of path
                # on the right
                if col + 1 < GRID_SIZE and abs(color) == abs(matrix[row][col + 1]):
                    canvas.create_line(center_x + 10, center_y, center_x + 30, center_y, fill=color_name,
                                       width=LINE_WIDTH)
                # on the left
                elif col - 1 >= 0 and abs(color) == abs(matrix[row][col - 1]):
                    canvas.create_line(center_x - 10, center_y, center_x - 30, center_y, fill=color_name,
                                       width=LINE_WIDTH)
                # above
                elif row - 1 >= 0 and abs(color) == abs(matrix[row - 1][col]):
                    canvas.create_line(center_x, center_y - 10, center_x, center_y - 30, fill=color_name,
                                       width=LINE_WIDTH)
                # below
                if row + 1 < GRID_SIZE and abs(color) == abs(matrix[row + 1][col]):
                    canvas.create_line(center_x, center_y + 10, center_x, center_y + 30, fill=color_name,
                                       width=LINE_WIDTH)

            elif color > 0:
                color_name = str(Color.get_color_by_number(color)).lower()
                # case left is same color and up is same color
                if (row-1 >= 0 and color == abs(matrix[row - 1][col]) and col - 1 >= 0 and
                        color == abs(matrix[row][col - 1])):
                    canvas.create_line(x1, center_y, center_x + plus_line_w, center_y, fill=color_name,
                                       width=LINE_WIDTH)
                    canvas.create_line(center_x, center_y + plus_line_w, center_x, y1, fill=color_name,
                                       width=LINE_WIDTH)
                # case left is same color and down is same color
                elif (row + 1 < GRID_SIZE and color == abs(matrix[row + 1][col]) and col - 1 >= 0 and
                      color == abs(matrix[row][col - 1])):
                    canvas.create_line(x1, center_y, center_x + plus_line_w, center_y, fill=color_name,
                                       width=LINE_WIDTH)
                    canvas.create_line(center_x, center_y - plus_line_w, center_x, y2, fill=color_name,
                                       width=LINE_WIDTH)
                # case left is same color and right is same color
                elif (col + 1 < GRID_SIZE and color == abs(matrix[row][col + 1]) and col - 1 >= 0 and
                      color == abs(matrix[row][col - 1])):
                    canvas.create_line(x1, center_y, x2, center_y, fill=color_name, width=LINE_WIDTH)
                # case right is same color and up is same color
                elif (row - 1 >= 0 and color == abs(matrix[row-1][col]) and col + 1 < GRID_SIZE and
                      color == abs(matrix[row][col+1])):
                    canvas.create_line(x2, center_y, center_x - plus_line_w, center_y, fill=color_name,
                                       width=LINE_WIDTH)
                    canvas.create_line(center_x, y1, center_x, center_y + plus_line_w, fill=color_name,
                                       width=LINE_WIDTH)
                # case right is same color and down is same color
                elif (row + 1 < GRID_SIZE and color == abs(matrix[row+1][col]) and col + 1 < GRID_SIZE and
                      color == abs(matrix[row][col+1])):
                    canvas.create_line(center_x - plus_line_w, center_y, x2, center_y, fill=color_name,
                                       width=LINE_WIDTH)
                    canvas.create_line(center_x, y2, center_x, center_y - plus_line_w, fill=color_name,
                                       width=LINE_WIDTH)
                # case down is same color and up is same color
                elif (row + 1 < GRID_SIZE and color == abs(matrix[row+1][col]) and row - 1 >= 0 and
                      color == abs(matrix[row-1][col])):
                    canvas.create_line(center_x, y1, center_x, y2, fill=color_name, width=LINE_WIDTH)
                else:
                    canvas.create_line(center_x, y1, center_x, y2, fill=color_name, width=LINE_WIDTH)
                    canvas.create_line(x1, center_y, x2, center_y, fill=color_name, width=LINE_WIDTH)

    root.mainloop()
