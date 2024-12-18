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
                 matrix,
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
        self.matrix = matrix
        self.last_visited_object = self.matrix[y][x]
        self.time_of_last_visit = Globals.global_time_frame
        self.pheromones = pheromones
        self.pheromone_drop_count = 0
        self.last_pheromone_distance = -1
        self.times_pheromone_not_dropped = 0
        self.last_x = x
        self.last_y = y
        self.time_no_pheromone_sighted = 0
        self.heading_towards_objective = False
        self.last_objective_sighted = None
        self.last_objective_sighted_x = -1
        self.last_objective_sighted_y = -1

    def max_health(self) -> int:
        return self.max_health

    def find_and_clear_precise_spot_for_drop(self, x, y, purpose):
        if purpose == 'ant':
            if self.matrix[y][x] is None:
                return True, x, y
            elif self.matrix[y][x].m_type == MarkerType.PHEROMONE:
                Ant.delete_pheromone_on_position(x, y)
                return True, x, y

        elif purpose == 'pheromone':
            if self.matrix[y][x] is None:
                return True, x, y
            elif self.matrix[y][x].m_type == MarkerType.PHEROMONE:
                if ((self.matrix[y][x].target == PheromoneType.TO_COLONY
                     and self.last_visited_object.m_type == MarkerType.COLONY)
                        or (self.matrix[y][x].target == PheromoneType.TO_FOOD
                            and self.last_visited_object.m_type == MarkerType.FOOD)):
                    print("Overriding pheromone")
                    if Globals.global_time_frame - self.matrix[y][x].creation_time > \
                            Globals.time_until_pheromone_override:
                        if self.last_pheromone_distance < self.matrix[y][x].distance:
                            self.last_pheromone_distance = self.matrix[y][x].distance
                            Ant.delete_pheromone_on_position(x, y)
                            return True, x, y
                else:
                    print('Found irrelevant pheromone')

        return False, -1, -1

    def find_and_clear_spot_for_drop(self, purpose):
        alternative_x = -1
        alternative_y = -1
        if purpose == 'ant':
            done, x, y = self.find_and_clear_precise_spot_for_drop(self.x, self.y, purpose)
            return x, y
        elif purpose == 'pheromone':
            for dist in range(0, Globals.pheromone_drop_FOV):
                done, x, y = self.find_and_clear_precise_spot_for_drop(self.x,
                                                                       self.y, purpose)
                if done:
                    return x, y
                else:
                    if x != -1 and y != -1:
                        alternative_x = x
                        alternative_y = y
                above = int(max(0, self.y - dist))
                below = int(min(899, self.y + dist))
                left = int(max(0, self.x - dist))
                right = int(min(1519, self.x + dist))
                for i in range(above, below):
                    for j in range(left, right):
                        done, x, y = self.find_and_clear_precise_spot_for_drop(j, i, purpose)
                        if done:
                            return x, y
                        else:
                            if x != -1 and y != -1:
                                alternative_x = x
                                alternative_y = y

            if alternative_x != -1 and alternative_y != -1:
                print('Ant -> ', self.last_visited_object.m_type)
                print('Pheromone -> ', self.matrix[alternative_y][alternative_x].target)
                Ant.delete_pheromone_on_position(alternative_x, alternative_y)
            return alternative_x, alternative_y

    @staticmethod
    def delete_pheromone_on_position(x: int, y: int):
        for i in range(len(Globals.pheromones)):
            if Globals.pheromones[i].x == x and Globals.pheromones[i].y == y:
                # Globals.pheromones[i].clear()
                # Globals.pheromones.pop(i)
                break

    def drop_pheromone(self) -> None:
        if self.times_pheromone_not_dropped < Globals.pheromone_drop_rate:
            self.times_pheromone_not_dropped += 1
            return
        if (self.time_of_last_visit <
                Globals.global_time_frame - Globals.how_recent_last_visit_has_to_be_for_pheromone_drop):
            return
        placement_x, placement_y = self.find_and_clear_spot_for_drop('pheromone')
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
                                             Globals.global_time_frame - self.time_of_last_visit,
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
                                             Globals.global_time_frame - self.time_of_last_visit,
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
            print('-----------------------------------')
            print('-----------------------------------')
            print("STANDING STILL")
            print('-----------------------------------')
            print('-----------------------------------')
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
        if self.matrix[self.last_y][self.last_x] is not None:
            if self.matrix[self.last_y][self.last_x].m_type == MarkerType.PHEROMONE:
                Ant.delete_pheromone_on_position(self.last_x, self.last_y)
        if not self.heading_towards_objective:
            object_sighted, y, x = self.object_sighted()
        else:
            if self.last_objective_sighted_x == self.x and self.last_objective_sighted_y == self.y:
                self.heading_towards_objective = False
                object_sighted, y, x = self.object_sighted()
            else:
                object_sighted = self.last_objective_sighted
                x = self.last_objective_sighted_x
                y = self.last_objective_sighted_y
        object_sighted_time = time.perf_counter() * 100000
        if object_sighted is None:
            if self.time_no_pheromone_sighted > Globals.how_long_until_ant_forgets_last_pheromone:
                self.last_pheromone_distance = -1
            else:
                self.time_no_pheromone_sighted += 0.01
            self.time_no_pheromone_sighted = 0
        self.pheromone_drop_count += 1
        if self.pheromone_drop_count >= Globals.pheromone_drop_rate:
            self.drop_pheromone()
            self.pheromone_drop_count = 0
        pheromone_drop_time = time.perf_counter() * 100000
        self.move(object_sighted, x, y)
        move_time = time.perf_counter() * 100000
        self.perform_action()
        perform_action_time = time.perf_counter() * 100000
        placement_x, placement_y = self.find_and_clear_spot_for_drop('ant')
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
            print('No object sighted, exploring')
            self.move_to_explore()
            return
        self.turn_towards(x, y)
        self.perform_movement()

    def turn_towards(self, x, y) -> None:
        # if x == self.x and y == self.y:
        #     return
        # if abs(x - self.x) > abs(y - self.y):
        #     if x > self.x:
        #         self.heading_x = 1
        #     elif x < self.x:
        #         self.heading_x = -1
        #     else:
        #         self.heading_x = 0
        # else:
        #     if y > self.y:
        #         self.heading_y = 1
        #     elif y < self.y:
        #         self.heading_y = -1
        #     else:
        #         self.heading_y = 0
        aux_x = self.x
        aux_y = self.y
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
        if aux_x != self.x or aux_y != self.y:
            print('Direction changed')
        if random.random() < Globals.chance_to_deviate_from_path:
            print('============DEVIATION ERROR======================')
            self.slightly_change_direction()

    @abstractmethod
    def object_sighted(self) -> Marker:
        pass

    @abstractmethod
    def perform_action(self):
        pass
