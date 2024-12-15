class Pheromone:
    def __init__(self, x, y, matrix, target, creator, distance, creation_time):
        self.target = target
        self.creator = creator
        self.distance = distance
        self.creation_time = creation_time
        self.x = x
        self.y = y
        self.matrix = matrix

    def clear(self):
        self.matrix[self.y][self.x] = None
