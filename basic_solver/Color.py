from enum import Enum


class Color(Enum):
    WHITE = 0
    RED = 1
    BLUE = 2
    YELLOW = 3
    GREEN = 4
    ORANGE = 5
    PURPLE = 6
    LIME = 7
    BROWN = 8
    TEAL = 9
    CYAN = 10

    @staticmethod
    def color_of(num):
        return abs(num)

    @staticmethod
    def is_dot(num):
        return num < 0

    @classmethod
    def get_color_by_number(cls, number):
        for color in cls:
            if color.value == number:
                return color.name
        raise ValueError(f"Invalid color number {number}")
