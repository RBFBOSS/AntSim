import copy

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
                 colony_id: int, matrix, pheromones):
        super().__init__(10, destination,
                         attack, x, y,
                         heading_x, heading_y,
                         state, colony_id,
                         matrix, pheromones)

    def move(self, object_sighted, x, y) -> None:
        if self.destination == Action.IDLE:
            self.last_pheromone_distance = -1
            self.move_to_explore()
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
                            self.time_of_last_visit = Globals.global_time_frame
                            self.heading_towards_objective = False
                            break
            if food_in_reach:
                self.is_carrying_food = True
                self.destination = Action.COLONY
                self.heading_y = -self.heading_y
                self.heading_x = -self.heading_x

        elif self.destination == Action.COLONY:
            colony_in_reach = False
            for i in range(self.y - 1, self.y + 1):
                for j in range(self.x - 1, self.x + 1):
                    if self.matrix[i][j]:
                        if self.matrix[i][j].m_type == MarkerType.COLONY \
                                and self.matrix[i][j].creator == self.colony_id:
                            colony_in_reach = True
                            self.last_visited_object = self.matrix[i][j]
                            self.last_pheromone_distance = -1
                            self.time_of_last_visit = Globals.global_time_frame
                            self.heading_towards_objective = False
                            break
            if colony_in_reach:
                self.is_carrying_food = False
                self.destination = Action.FOOD
                self.heading_y = -self.heading_y
                self.heading_x = -self.heading_x

    def look_for_object_at_precise_spot(self, i, j):
        object_sighted = None
        object_i = -1
        object_j = -1
        if i != self.y or j != self.x:
            if self.matrix[i][j] is not None:
                if self.matrix[i][j].m_type == MarkerType.PHEROMONE:
                    Globals.pheromones_sighted += 1
                elif self.matrix[i][j].m_type == MarkerType.COLONY:
                    Globals.colonies_sighted += 1
                elif self.matrix[i][j].m_type == MarkerType.ANT:
                    Globals.ants_sighted += 1
                elif self.matrix[i][j].m_type == MarkerType.FOOD:
                    Globals.food_sources_sighted += 1
                Globals.objects_sighted += 1
                if self.matrix[i][j].m_type == MarkerType.COLONY \
                        and self.matrix[i][j].creator == self.colony_id \
                        and self.destination == Action.COLONY:
                    object_sighted = copy.deepcopy(self.matrix[i][j])
                    self.heading_towards_objective = True
                    self.last_objective_sighted = object_sighted
                    self.last_objective_sighted_x = j
                    self.last_objective_sighted_y = i
                    return object_sighted, i, j
                if self.matrix[i][j].m_type == MarkerType.FOOD \
                        and not self.is_carrying_food \
                        and self.destination == Action.FOOD:
                    object_sighted = copy.deepcopy(self.matrix[i][j])
                    self.heading_towards_objective = True
                    self.last_objective_sighted = object_sighted
                    self.last_objective_sighted_x = j
                    self.last_objective_sighted_y = i
                    return object_sighted, i, j
                elif self.matrix[i][j].m_type == MarkerType.PHEROMONE:
                    # print('ANT -> ', self.destination)
                    # print('PHEROMONE -> ', self.matrix[i][j].target)
                    if ((self.matrix[i][j].target == PheromoneType.TO_FOOD
                         and self.destination == Action.FOOD) or
                            (self.matrix[i][j].target == PheromoneType.TO_COLONY
                             and self.destination == Action.COLONY)):
                        print('XXXXXXXXXXXXXXXXXXX')
                        if self.matrix[i][j].creator == self.colony_id:
                            # Globals.avg_pheromone_creation_time += self.matrix[i][j].creation_time
                            # Globals.new_count += 1
                            # if (Globals.global_time_frame - self.matrix[i][j].creation_time <
                            #         Globals.how_young_pheromone_to_consider):
                            # if pheromones_checked < Globals.pheromones_to_check:
                            #     pheromones_checked += 1
                            # else:
                            #     self.last_pheromone_distance = object_sighted.distance
                            #     return object_sighted, object_i, object_j
                            gasit_feromon = True
                            if self.last_pheromone_distance == -1 \
                                    or self.last_pheromone_distance > \
                                    self.matrix[i][j].distance:
                                if gasit_feromon:
                                    e_bun = True
                                    # if object_sighted is not None:
                                    #     if object_sighted.distance > self.matrix[i][j].distance:
                                    #         object_sighted = copy.deepcopy(self.matrix[i][j])
                                    #         object_i = i
                                    #         object_j = j
                                    #         self.last_pheromone_distance =
                                    #         copy.deepcopy(self.matrix[i][j].distance)
                                    # else:
                                object_sighted = copy.deepcopy(self.matrix[i][j])
                                object_i = i
                                object_j = j
                                self.last_pheromone_distance = copy.deepcopy(self.matrix[i][j].distance)
                                self.heading_towards_objective = True
                                self.last_objective_sighted = object_sighted
                                self.last_objective_sighted_x = j
                                self.last_objective_sighted_y = i
                                return object_sighted, object_i, object_j
                                # else:
                                #     if self.last_pheromone_distance < \
                                #             self.matrix[i][j].distance:
                                #         print('K', self.last_pheromone_distance,
                                #               self.matrix[i][j].distance)
                                #     else:
                                #         print('am castigat cox', self.last_pheromone_distance,
                                #               self.matrix[i][j].distance)
                            # else:
                            #     print('Pheromone was too old')
                    # elif self.matrix[i][j].m_type == MarkerType.ANT:
                            #     object_sighted = self.matrix[i][j]
        return object_sighted, object_i, object_j

    def object_sighted(self):
        above = int(max(0, self.y - Globals.ant_FOV))
        below = int(min(899, self.y + Globals.ant_FOV))
        left = int(max(0, self.x - Globals.ant_FOV))
        right = int(min(1519, self.x + Globals.ant_FOV))
        object_sighted = None
        object_i = -1
        object_j = -1
        pheromones_checked = 0
        e_bun = False
        gasit_feromon = False
        first_checked_position_x, first_checked_position_y = self.get_first_angle_to_check()
        if first_checked_position_y == above:
            if first_checked_position_x == left:
                for i in range(0, self.y + 1 - above):
                    for j in range(i, self.x + 1 - left):
                        object_sighted, object_i, object_j = \
                            self.look_for_object_at_precise_spot(i + above, j + left)
                        if object_sighted is not None:
                            return object_sighted, object_i, object_j
                        if i != j:
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(j + above, i + left)
                            if object_sighted is not None:
                                return object_sighted, object_i, object_j
            elif first_checked_position_x == right:
                for i in range(0, self.y + 1 - above):
                    for j in range(i, right - self.x, -1):
                        object_sighted, object_i, object_j = \
                            self.look_for_object_at_precise_spot(i + above, j + right)
                        if object_sighted is not None:
                            return object_sighted, object_i, object_j
                        if i + j != below - above:
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(j + above, i + right)
                            if object_sighted is not None:
                                return object_sighted, object_i, object_j
            else:
                for i in range(0, self.y + 1 - above):
                    for j in range(left, right):
                        object_sighted, object_i, object_j = \
                            self.look_for_object_at_precise_spot(i + above, j)
                        if object_sighted is not None:
                            return object_sighted, object_i, object_j

        for i in range(above, below):
            for j in range(left, right):
                object_sighted, object_i, object_j = self.look_for_object_at_precise_spot(i, j)
        # if not e_bun and gasit_feromon:
        #     print('Not found a better pheromone')
        if object_sighted is not None:
            self.heading_towards_objective = True
            self.last_objective_sighted = object_sighted
            self.last_objective_sighted_x = self.last_objective_sighted_x
            self.last_objective_sighted_y = self.last_objective_sighted_y
        return object_sighted, object_i, object_j

    def move_to_explore(self):
        movement_change = True if random.random() < Globals.exploration_rate else False
        if movement_change:
            self.slightly_change_direction()
        else:
            self.perform_movement()
