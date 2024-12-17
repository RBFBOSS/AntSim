import time
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
                 ant_FOV: int, matrix,
                 pheromones):
        self.aux = 0
        self.is_carrying_food = False
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
        self.last_pheromone_distance = -1
        self.times_pheromone_not_dropped = 0
        self.last_x = x
        self.last_y = y

    def max_health(self) -> int:
        return self.max_health

    def find_spot_for_drop(self):
        alternative_x = -1
        alternative_y = -1

        if self.matrix[self.y][self.x] is None:
            if self.aux == 1:
                print('time done', Globals.global_time_frame, "X: ", self.x, " Y: ", self.y)
            return self.x, self.y
        elif self.matrix[self.y][self.x].m_type == MarkerType.PHEROMONE:
            alternative_y = self.y
            alternative_x = self.x

        if self.x + 1 < 1515:
            if self.matrix[self.y][self.x + 1] is None:
                return self.x + 1, self.y
            elif self.matrix[self.y][self.x + 1].m_type == MarkerType.PHEROMONE:
                alternative_y = self.y
                alternative_x = self.x + 1

        if self.x - 1 > 5:
            if self.matrix[self.y][self.x - 1] is None:
                return self.x - 1, self.y
            elif self.matrix[self.y][self.x - 1].m_type == MarkerType.PHEROMONE:
                alternative_y = self.y
                alternative_x = self.x - 1

        if self.y + 1 < 890:
            if self.matrix[self.y + 1][self.x] is None:
                return self.x, self.y + 1
            elif self.matrix[self.y + 1][self.x].m_type == MarkerType.PHEROMONE:
                alternative_y = self.y + 1
                alternative_x = self.x

        if self.y - 1 > 5:
            if self.matrix[self.y - 1][self.x] is None:
                return self.x, self.y - 1
            elif self.matrix[self.y - 1][self.x].m_type == MarkerType.PHEROMONE:
                alternative_y = self.y - 1
                alternative_x = self.x

        return alternative_x, alternative_y

    def drop_pheromone(self) -> None:
        if self.times_pheromone_not_dropped < Globals.pheromone_drop_rate:
            self.times_pheromone_not_dropped += 1
            return
        if (self.time_of_last_visit <
                Globals.global_time_frame - Globals.how_recent_last_visit_has_to_be_for_pheromone_drop):
            return
        placement_x, placement_y = self.find_spot_for_drop()
        if placement_x == -1 or placement_y == -1:
            return
        if self.last_visited_object.m_type == MarkerType.FOOD:
            self.matrix[placement_y][placement_x] = Marker(MarkerType.PHEROMONE,
                                                           PheromoneType.TO_FOOD,
                                                           self.colony_id,
                                                           Globals.global_time_frame - self.time_of_last_visit,
                                                           Globals.global_time_frame)
            self.pheromones.append(Pheromone(placement_x, placement_y, self.matrix,
                                             PheromoneType.TO_FOOD, self.colony_id,
                                             self.time_of_last_visit,
                                             Globals.global_time_frame))
        elif self.last_visited_object.m_type == MarkerType.COLONY \
                and self.last_visited_object.creator == self.colony_id:
            self.matrix[placement_y][placement_x] = Marker(MarkerType.PHEROMONE,
                                                           PheromoneType.TO_COLONY,
                                                           self.colony_id,
                                                           Globals.global_time_frame - self.time_of_last_visit,
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
        movement_change = True if random.random() < Globals.exploration_rate else False
        if movement_change:
            self.slightly_change_direction()
        self.perform_movement()

    def perform_movement(self) -> None:
        if self.heading_x == 0 and self.heading_y == 0:
            self.heading_x = random.choice([-1, 0, 1])
            if self.heading_x == 0:
                self.heading_y = random.choice([-1, 1])
            else:
                self.heading_y = random.choice([-1, 0, 1])
        if self.x >= 1518:
            self.heading_x = -1
        elif self.x <= 2:
            self.heading_x = 1
        if self.y >= 890:
            self.heading_y = -1
        elif self.y <= 10:
            self.heading_y = 1
        self.x += self.heading_x * Globals.speed
        self.y += self.heading_y * Globals.speed

    def move_randomly(self) -> None:
        r = random.randint(0, 2)
        self.heading_x = 0
        self.heading_y = 0
        if r == 0:
            self.x += Globals.speed
            self.heading_x = 1
        elif r == 1:
            self.x -= Globals.speed
            self.heading_x = -1
        r = random.randint(0, 2)
        if r == 0:
            self.y += Globals.speed
            self.heading_y = 1
        elif r == 1:
            self.y -= Globals.speed
            self.heading_y = -1

    @abstractmethod
    def move(self, object_sighted, x, y) -> None:
        pass

    def update(self):
        start_time = time.perf_counter() * 100000
        self.matrix[self.last_y][self.last_x] = None
        object_sighted, y, x = self.object_sighted()
        object_sighted_time = time.perf_counter() * 100000
        if object_sighted is None:
            self.last_pheromone_distance = -1
        self.pheromone_drop_count += 1
        if self.pheromone_drop_count >= Globals.pheromone_drop_rate:
            self.drop_pheromone()
            self.pheromone_drop_count = 0
        pheromone_drop_time = time.perf_counter() * 100000
        self.move(object_sighted, x, y)
        move_time = time.perf_counter() * 100000
        self.perform_action()
        perform_action_time = time.perf_counter() * 100000
        placement_x, placement_y = self.find_spot_for_drop()
        self.last_y = placement_y
        self.last_x = placement_x
        if placement_x != -1 and placement_y != -1:
            self.matrix[placement_y][placement_x] = Marker(MarkerType.ANT, None,
                                                           self.colony_id,
                                                           Globals.global_time_frame,
                                                           Globals.global_time_frame)
        end_time = time.perf_counter() * 100000
        Globals.avg_object_sighted_time += object_sighted_time - start_time
        # Globals.avg_pheromone_drop_time += pheromone_drop_time - object_sighted_time
        # Globals.avg_move_time += move_time - pheromone_drop_time
        # Globals.avg_perform_action_time += perform_action_time - move_time
        # Globals.avg_placement_time += end_time - perform_action_time
        Globals.entire_time += end_time - start_time
        Globals.ant_operations += 1

    def move_towards_objective(self, object_sighted, x, y):
        if object_sighted is None:
            self.move_to_explore()
            return
        self.turn_towards(x, y)
        self.perform_movement()

    def turn_towards(self, x, y) -> None:
        if x == self.x and y == self.y:
            return
        if abs(x - self.x) > abs(y - self.y):
            if x > self.x:
                self.heading_x = 1
            else:
                self.heading_x = -1
        else:
            if y > self.y:
                self.heading_y = 1
            else:
                self.heading_y = -1
        if random.random() < Globals.chance_to_deviate_from_path:
            self.slightly_change_direction()
        # if x > self.x:
        #     self.heading_x = 1
        # elif x < self.x:
        #     self.heading_x = -1
        # else:
        #     self.heading_x = 0
        # if y > self.y:
        #     self.heading_y = 1
        # elif y < self.y:
        #     self.heading_y = -1
        # else:
        #     self.heading_y = 0

    @abstractmethod
    def object_sighted(self) -> Marker:
        pass

    @abstractmethod
    def perform_action(self):
        pass
