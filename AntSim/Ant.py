from abc import ABC, abstractmethod
import random
from Action import Action
from Globals import Globals
from Marker import Marker
from MarkerType import MarkerType
from Pheromone import Pheromone
from PheromoneType import PheromoneType


class Ant(ABC):
    def __init__(self, max_health: int,
                 destination: Action,
                 attack: int,
                 x: int,
                 y: int,
                 heading_x: int,
                 heading_y: int,
                 state: int,
                 colony_id: int,
                 speed: int,
                 exploration_rate: float,
                 ant_FOV: int, matrix,
                 pheromones):
        self.is_carrying_food = False
        self.speed = speed
        self.exploration_rate = exploration_rate
        self.max_health = max_health
        self.health = max_health
        self.destination = destination
        self.attack = attack
        self.x = x
        self.y = y
        self.heading_x = heading_x
        self.heading_y = heading_y
        self.state = state
        self.colony_id = colony_id
        self.ant_FOV = ant_FOV
        self.matrix = matrix
        self.last_visited_object = self.matrix[y][x]
        self.time_of_last_visit = Globals.global_time_frame
        self.pheromones = pheromones
        self.pheromone_drop_count = 0
        self.last_pheromone_time_target_observed = 0

    def max_health(self) -> int:
        return self.max_health

    def find_spot_for_drop(self):
        if self.matrix[self.y][self.x]:
            if self.matrix[self.y][self.x].m_type == MarkerType.PHEROMONE:
                return self.x, self.y
        else:
            return self.x, self.y

        if self.x + 1 < 1515:
            if self.matrix[self.y][self.x + 1]:
                if self.matrix[self.y][self.x + 1].m_type == MarkerType.PHEROMONE:
                    return self.x + 1, self.y
            else:
                return self.x + 1, self.y

        if self.x - 1 > 5:
            if self.matrix[self.y][self.x - 1]:
                if self.matrix[self.y][self.x - 1].m_type == MarkerType.PHEROMONE:
                    return self.x - 1, self.y
            else:
                return self.x - 1, self.y

        if self.y + 1 < 890:
            if self.matrix[self.y + 1][self.x]:
                if self.matrix[self.y + 1][self.x].m_type == MarkerType.PHEROMONE:
                    return self.x, self.y + 1
            else:
                return self.x, self.y + 1

        if self.y - 1 > 5:
            if self.matrix[self.y - 1][self.x]:
                if self.matrix[self.y - 1][self.x].m_type == MarkerType.PHEROMONE:
                    return self.x, self.y - 1
            else:
                return self.x, self.y - 1

        return -1, -1

    def drop_pheromone(self) -> None:
        if self.last_visited_object.m_type == MarkerType.FOOD:
            placement_x, placement_y = self.find_spot_for_drop()
            if placement_x == -1 or placement_y == -1:
                return
            self.matrix[placement_y][placement_x] = Marker(MarkerType.PHEROMONE,
                                                           PheromoneType.TO_FOOD,
                                                           self.colony_id,
                                                           self.time_of_last_visit,
                                                           Globals.global_time_frame)
            self.pheromones.append(Pheromone(placement_x, placement_y, self.matrix,
                                             PheromoneType.TO_FOOD, self.colony_id,
                                             self.time_of_last_visit,
                                             Globals.global_time_frame))
            if placement_x == -1 or placement_y == -1:
                return
        elif self.last_visited_object.m_type == MarkerType.COLONY \
                and self.last_visited_object.creator == self.colony_id:
            placement_x, placement_y = self.find_spot_for_drop()
            if placement_x == -1 or placement_y == -1:
                return
            self.matrix[placement_y][placement_x] = Marker(MarkerType.PHEROMONE,
                                                           PheromoneType.TO_COLONY,
                                                           self.colony_id,
                                                           self.time_of_last_visit,
                                                           Globals.global_time_frame)
            self.pheromones.append(Pheromone(placement_x, placement_y, self.matrix,
                                             PheromoneType.TO_COLONY, self.colony_id,
                                             self.time_of_last_visit,
                                             Globals.global_time_frame))

    def slightly_change_direction(self) -> None:
        clockwise_change = random.choice([0, 1])
        if self.heading_y == -1 and self.heading_x == 0:
            if clockwise_change:
                self.heading_x = 1
            else:
                self.heading_x = -1
        elif self.heading_y == -1 and self.heading_x == 1:
            if clockwise_change:
                self.heading_y = 0
            else:
                self.heading_x = 0
        elif self.heading_y == 0 and self.heading_x == 1:
            if clockwise_change:
                self.heading_y = 1
            else:
                self.heading_y = -1
        elif self.heading_y == 1 and self.heading_x == 1:
            if clockwise_change:
                self.heading_x = 0
            else:
                self.heading_y = 0
        elif self.heading_y == 1 and self.heading_x == 0:
            if clockwise_change:
                self.heading_x = -1
            else:
                self.heading_x = 1
        elif self.heading_y == 1 and self.heading_x == -1:
            if clockwise_change:
                self.heading_y = 0
            else:
                self.heading_x = 0
        elif self.heading_y == 0 and self.heading_x == -1:
            if clockwise_change:
                self.heading_y = -1
            else:
                self.heading_y = 1
        else:
            if clockwise_change:
                self.heading_x = 0
            else:
                self.heading_y = 0

    def move_to_explore(self) -> None:
        movement_change = True if random.random() < self.exploration_rate else False
        if movement_change:
            self.slightly_change_direction()
        self.perform_movement()

    def perform_movement(self) -> None:
        if self.x >= 1518:
            self.heading_x = -1
        elif self.x <= 2:
            self.heading_x = 1
        if self.y >= 890:
            self.heading_y = -1
        elif self.y <= 10:
            self.heading_y = 1
        self.x += self.heading_x * self.speed
        self.y += self.heading_y * self.speed

    def move_randomly(self) -> None:
        r = random.randint(0, 2)
        self.heading_x = 0
        self.heading_y = 0
        if r == 0:
            self.x += self.speed
            self.heading_x = 1
        elif r == 1:
            self.x -= self.speed
            self.heading_x = -1
        r = random.randint(0, 2)
        if r == 0:
            self.y += self.speed
            self.heading_y = 1
        elif r == 1:
            self.y -= self.speed
            self.heading_y = -1

    @abstractmethod
    def move(self, object_sighted, x, y) -> None:
        pass

    def update(self):
        object_sighted, y, x = self.object_sighted()
        self.pheromone_drop_count += 1
        if self.pheromone_drop_count >= 10:
            self.drop_pheromone()
            self.pheromone_drop_count = 0
        self.move(object_sighted, x, y)
        self.perform_action()
        placement_x, placement_y = self.find_spot_for_drop()
        if placement_x != -1 and placement_y != -1:
            self.matrix[placement_y][placement_x] = Marker(MarkerType.ANT, None,
                                                           self.colony_id,
                                                           Globals.global_time_frame,
                                                           Globals.global_time_frame)

    def move_towards_objective(self, object_sighted, x, y):
        if object_sighted is None:
            self.move_to_explore()
            return
        self.turn_towards(x, y)
        self.perform_movement()

    def turn_towards(self, x, y) -> None:
        if x > self.x:
            self.heading_x = 1
        elif x < self.x:
            self.heading_x = -1
        else:
            self.heading_x = 0
        if y > self.y:
            self.heading_y = 1
        elif y < self.y:
            self.heading_y = -1
        else:
            self.heading_y = 0

    @abstractmethod
    def object_sighted(self) -> Marker:
        pass

    @abstractmethod
    def perform_action(self):
        pass
