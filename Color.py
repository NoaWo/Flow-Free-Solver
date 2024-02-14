from enum import Enum


class Color(Enum):
    BLANK = 0
    RED = 1
    BLUE = 2
    YELLOW = 3
    GREEN = 4
    ORANGE = 5
    PURPLE = 6

    @staticmethod
    def color_of(num):
        return abs(num)

    @staticmethod
    def is_dot(num):
        return num < 0
