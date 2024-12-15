from Ant import Ant
from Action import Action
import random

from Globals import Globals
from MarkerType import MarkerType
from PheromoneType import PheromoneType


class Worker(Ant):
    def __init__(self, destination: Action, attack: int,
                 x: int, y: int, heading_x: int,
                 heading_y: int, state: int,
                 colony_id: int, speed: int,
                 exploration_rate: float, ant_FOV: int,
                 matrix, pheromones):
        super().__init__(10, destination,
                         attack, x, y,
                         heading_x, heading_y,
                         state, colony_id,
                         speed, exploration_rate,
                         ant_FOV, matrix, pheromones)

    def move(self, object_sighted, x, y) -> None:
        if self.destination == Action.IDLE:
            self.move_randomly()
        else:
            self.move_towards_objective(object_sighted, x, y)

    def perform_action(self):
        if self.destination == Action.FOOD:
            food_in_reach = False
            for i in range(self.y - 1, self.y + 1):
                for j in range(self.x - 1, self.x + 1):
                    if self.matrix[i][j]:
                        if self.matrix[i][j].m_type == MarkerType.FOOD:
                            food_in_reach = True
                            self.last_visited_object = self.matrix[i][j]
                            self.last_pheromone_distance = -1
                            break
            if food_in_reach:
                self.is_carrying_food = True
                self.destination = Action.COLONY
                self.heading_y = -self.heading_y
                self.heading_x = -self.heading_x
                print("Worker got food")

        if self.destination == Action.COLONY:
            colony_in_reach = False
            for i in range(self.y - 1, self.y + 1):
                for j in range(self.x - 1, self.x + 1):
                    if self.matrix[i][j]:
                        if self.matrix[i][j].m_type == MarkerType.COLONY\
                                and self.matrix[i][j].creator == self.colony_id:
                            colony_in_reach = True
                            self.last_visited_object = self.matrix[i][j]
                            self.last_pheromone_distance = -1
                            break
            if colony_in_reach:
                self.is_carrying_food = False
                self.destination = Action.FOOD
                self.heading_y = -self.heading_y
                self.heading_x = -self.heading_x
                print("Worker has returned to colony")

    def object_sighted(self):
        above = int(max(0, self.y - self.ant_FOV))
        below = int(min(899, self.y + self.ant_FOV))
        left = int(max(0, self.x - self.ant_FOV))
        right = int(min(1519, self.x + self.ant_FOV))
        object_sighted = None
        object_i = -1
        object_j = -1
        for i in range(above, below):
            for j in range(left, right):
                if i != self.y and j != self.x:
                    if self.matrix[i][j] is not None:
                        if self.matrix[i][j].m_type == MarkerType.COLONY \
                                and self.matrix[i][j].creator == self.colony_id \
                                and self.destination == Action.COLONY:
                            object_sighted = self.matrix[i][j]
                            self.last_visited_object = object_sighted
                            self.time_of_last_visit = Globals.global_time_frame
                            self.last_pheromone_distance = -1
                            return object_sighted, i, j
                        if self.matrix[i][j].m_type == MarkerType.FOOD \
                                and not self.is_carrying_food:
                            object_sighted = self.matrix[i][j]
                            self.last_visited_object = object_sighted
                            self.time_of_last_visit = Globals.global_time_frame
                            self.last_pheromone_distance = -1
                            return object_sighted, i, j
                        elif self.matrix[i][j].m_type == MarkerType.PHEROMONE:
                            if (self.matrix[i][j].target == PheromoneType.TO_FOOD
                                and self.destination == Action.FOOD) or \
                                    (self.matrix[i][j].target == PheromoneType.TO_COLONY
                                     and self.destination == Action.COLONY):
                                if object_sighted is not None:
                                    if self.last_pheromone_distance == -1 \
                                        or self.last_pheromone_distance > \
                                            self.matrix[i][j].distance:
                                        if object_sighted.distance > self.matrix[i][j].distance:
                                            object_sighted = self.matrix[i][j]
                                            object_i = i
                                            object_j = j
                                            self.last_pheromone_distance = self.matrix[i][j].distance
                                else:
                                    if self.last_pheromone_distance == -1 \
                                            or self.last_pheromone_distance > \
                                            self.matrix[i][j].distance:
                                        object_sighted = self.matrix[i][j]
                                        object_i = i
                                        object_j = j
                                        self.last_pheromone_distance = self.matrix[i][j].distance
                        # elif self.matrix[i][j].m_type == MarkerType.ANT:
                        #     object_sighted = self.matrix[i][j]
        return object_sighted, object_i, object_j

    def move_to_explore(self):
        movement_change = True if random.random() < self.exploration_rate else False
        if movement_change:
            self.slightly_change_direction()
        else:
            self.perform_movement()
