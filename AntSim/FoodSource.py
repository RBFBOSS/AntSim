from Globals import Globals
from Marker import Marker
from MarkerType import MarkerType


class FoodSource:
    def __init__(self, food_id, x, y, matrix, size=300):
        self.food_id = food_id
        self.size = size
        self.x = x
        self.y = y
        self.matrix = matrix
        above = int(max(0, self.y - 25))
        below = int(min(Globals.height - 1, self.y + 25))
        left = int(max(0, self.x - 25))
        right = int(min(Globals.width - 1, self.x + 25))
        for i in range(above, below):
            for j in range(left, right):
                self.matrix[i][j] = Marker(MarkerType.FOOD,
                                           None, food_id, 0,
                                           Globals.global_time_frame)

    def remove_food(self, amount):
        self.size = max(0, self.size - amount)
        if self.size == 0:
            above = int(max(0, self.y - 25))
            below = int(min(Globals.height - 1, self.y + 25))
            left = int(max(0, self.x - 25))
            right = int(min(Globals.width - 1, self.x + 25))
            for i in range(above, below):
                for j in range(left, right):
                    self.matrix[i][j] = None
            Globals.food_sources.remove(self)
