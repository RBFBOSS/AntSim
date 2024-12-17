from Ant import Ant
from Action import Action


class Soldier(Ant):
    def __init__(self, destination: Action, attack: int,
                 x: int, y: int, heading_x: int,
                 heading_y: int, state: int,
                 colony_id: int, matrix, pheromones):
        super().__init__(30, destination,
                         attack, x, y,
                         heading_x, heading_y,
                         state, colony_id,
                         matrix, pheromones)

    def move(self, object_sighted, x, y) -> None:
        if self.destination == Action.IDLE:
            self.move_to_explore()
        elif self.destination == Action.PATROL:
            self.patrol()
        else:
            self.move_towards_objective(object_sighted, x, y)

    def perform_action(self):
        pass

    def patrol(self):
        pass

    def object_sighted(self):
        return False, -1, -1
        # above = int(max(0, self.y - self.ant_FOV))
        # below = int(min(899, self.y + self.ant_FOV))
        # left = int(max(0, self.x - self.ant_FOV))
        # right = int(min(1519, self.x + self.ant_FOV))
        # object_sighted = None
        #
        # for i in range(above, below):
        #     for j in range(left, right):
        #         if self.matrix[i][i]:
        #             if self.matrix[i][j] == MarkerType.COLONY:
        #                 object_sighted = self.matrix[i][j]
        #                 return object_sighted
        #             elif self.matrix[i][j] == MarkerType.FOOD\
        #                     and isinstance(self, Worker):
        #                 object_sighted = self.matrix[i][j]
        #             elif self.matrix[i][j] == MarkerType.ANT:
        #                 object_sighted = self.matrix[i][j]
        # return object_sighted
