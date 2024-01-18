import tkinter as tk
from enum import Enum
class Color(Enum):
    BLANK = 0
    RED = 1
    BLUE = 2
    YELLOW = 3
    GREEN = 4
    ORANGE = 5
    PURPLE = 6

GRID_SIZE = 6
SQUARE_SIZE = 50
CANVAS_SIZE = GRID_SIZE * SQUARE_SIZE
DISC_RADIUS = 20  # Adjust the radius as needed
DISC_COLOR = "red"  # Adjust the color as needed
LINE_COLOR = "blue"  # Adjust the color as needed
LINE_WIDTH = 23  # Adjust the line width as needed

ex_matrix = [[Color.BLANK,Color.BLANK,Color.BLANK,Color.BLANK,Color.BLANK,Color.BLANK],
             [Color.BLANK,Color.RED,Color.PURPLE,Color.BLANK,Color.BLANK,Color.BLANK],
             [Color.BLANK,Color.BLANK,Color.BLANK,Color.BLANK,Color.BLANK,Color.BLANK],
             [Color.RED,Color.RED,Color.RED,Color.RED,Color.RED,Color.BLANK],
             [Color.BLANK,Color.BLANK,Color.BLANK,Color.BLANK,Color.BLANK,Color.BLANK],
             [Color.BLANK,Color.BLANK,Color.BLANK,Color.BLANK,Color.BLANK,Color.BLANK]]
def draw_board(canvas, matrix):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x1, y1 = col * SQUARE_SIZE, row * SQUARE_SIZE
            x2, y2 = x1 + SQUARE_SIZE, y1 + SQUARE_SIZE

            # Draw the square with light yellow borders
            canvas.create_rectangle(x1, y1, x2, y2, outline="lightyellow", width=1)
            color = matrix[row][col]
            if color != Color.BLANK:
                color_name = str(color.name).lower()
                # Calculate the center of the square
                center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2

                # Draw a filled circle (disc) inside the square
                canvas.create_oval(center_x - DISC_RADIUS, center_y - DISC_RADIUS,
                                center_x + DISC_RADIUS, center_y + DISC_RADIUS,
                                fill=color_name, outline=color_name)

            # Draw a diagonal line inside the square
            # canvas.create_line(x1, y1, x2, y2, fill=LINE_COLOR, width=LINE_WIDTH)

root = tk.Tk()
root.title("Minesweeper Board")

canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="black")
canvas.pack()

draw_board(canvas, ex_matrix)

root.mainloop()
