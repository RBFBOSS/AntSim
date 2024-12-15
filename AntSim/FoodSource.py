from Globals import Globals
from Marker import Marker
from MarkerType import MarkerType


class FoodSource:
    def __init__(self, max_size, x, y, matrix):
        self.max_size = max_size
        self.size = max_size
        self.x = x
        self.y = y
        self.matrix = matrix
        above = int(max(0, self.y - 10))
        below = int(min(899, self.y + 10))
        left = int(max(0, self.x - 10))
        right = int(min(1519, self.x + 10))
        for i in range(above, below):
            for j in range(left, right):
                self.matrix[i][j] = Marker(MarkerType.FOOD,
                                           None, 0,
                                           0,
                                           Globals.global_time_frame)
