import copy
import time

from Ant import Ant
from Action import Action
import random

from Globals import Globals
from Marker import Marker
from MarkerType import MarkerType
from Pheromone import Pheromone
from PheromoneType import PheromoneType


class Soldier(Ant):
    def __init__(self, destination: Action,
                 x: int, y: int, heading_x: int,
                 heading_y: int, state: int,
                 colony_id: int, matrix, pheromones, simulation):
        super().__init__(30, destination,
                         3, x, y,
                         heading_x, heading_y,
                         state, colony_id,
                         matrix, pheromones, simulation)

    def move(self, object_sighted, x, y) -> None:
        if self.destination == Action.IDLE:
            self.last_pheromone_distance = -1
            self.move_to_explore()
        else:
            self.move_towards_objective(object_sighted, x, y)

    def perform_action(self):
        if self.destination == Action.TO_ENEMY:
            enemy_in_reach = False
            above = self.y - Globals.ant_FOV
            above = max(0, above)
            below = self.y + Globals.ant_FOV + 1
            below = min(Globals.height, below)
            left = self.x - Globals.ant_FOV
            left = max(0, left)
            right = self.x + Globals.ant_FOV + 1
            right = min(Globals.width, right)
            for i in range(above, below):
                for j in range(left, right):
                    if self.matrix[i][j]:
                        if self.matrix[i][j].m_type == MarkerType.ANT \
                                and self.matrix[i][j].creator != self.colony_id:
                            enemy_in_reach = True
                            self.target_ant = self.matrix[i][j].ant_reference
                            self.target_ant.is_attacked = True
                            self.is_attacked = True
                            self.target_ant.target_ant = self
                            self.matrix[i][j].ant_reference.target_ant = self
                            self.destination = Action.ATTACK
                            self.last_visited_object = PheromoneType.TO_ENEMY
                            self.last_pheromone_distance = -1
                            self.time_of_last_visit = Globals.global_time_frame
                            self.heading_towards_objective = False
                            self.last_objective_sighted = None

        if self.destination == Action.ATTACK:
            print('ATTACKING')
            if self.target_ant is None:
                if self.health < self.max_health / 3:
                    self.destination = Action.COLONY
                else:
                    self.destination = Action.IDLE
                return
            if self.target_ant.health > 0:
                self.target_ant.health = max(0, self.target_ant.health - self.attack)
            if self.target_ant.health == 0:
                self.is_attacked = False
                self.target_ant = None
                if self.health < self.max_health / 3:
                    self.destination = Action.COLONY
                else:
                    self.destination = Action.IDLE

        elif self.destination == Action.COLONY:
            colony_in_reach = False
            for i in range(self.y - 1, self.y + 1):
                for j in range(self.x - 1, self.x + 1):
                    if self.matrix[i][j]:
                        if self.matrix[i][j].m_type == MarkerType.COLONY \
                                and self.matrix[i][j].creator == self.colony_id:
                            if self.is_carrying_food:
                                Globals.add_food_to_colony(self.colony_id, 1)
                                self.is_carrying_food = False
                            if self.is_warning_about_enemy:
                                Globals.colony_received_warning(self.colony_id)
                                self.is_warning_about_enemy = False
                            colony_in_reach = True
                            self.health = self.max_health
                            self.last_visited_object = PheromoneType.TO_COLONY
                            self.last_pheromone_distance = -1
                            self.time_of_last_visit = Globals.global_time_frame
                            self.heading_towards_objective = False
                            self.destination = Action.FOOD
                            self.heading_y = -self.heading_y
                            self.heading_x = -self.heading_x
                            self.last_objective_sighted = None
                            return

    def look_for_object_at_precise_spot(self, i, j):
        # Globals.pause_pheromone_cleanup()
        # while not Globals.waiting_event.is_set():
        #     pass
        object_sighted = None
        object_i = -1
        object_j = -1
        timed = time.perf_counter() * 100000
        # Globals.ant_FOVs.append((i, j))
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
                if self.matrix[i][j].m_type == MarkerType.ANT and self.matrix[i][j].creator != self.colony_id \
                        and self.destination == Action.TO_ENEMY:
                    object_sighted = self.matrix[i][j]
                    self.heading_towards_objective = True
                    self.last_objective_sighted = object_sighted
                    self.last_objective_sighted_x = j
                    self.last_objective_sighted_y = i
                    return object_sighted, object_i, object_j
                if self.matrix[i][j].m_type == MarkerType.COLONY \
                        and self.matrix[i][j].creator == self.colony_id \
                        and self.destination == Action.COLONY:
                    object_sighted = self.matrix[i][j]
                    self.heading_towards_objective = True
                    self.last_objective_sighted = object_sighted
                    self.last_objective_sighted_x = j
                    self.last_objective_sighted_y = i
                    # Globals.resume_pheromone_cleanup()
                    return object_sighted, i, j
                if self.matrix[i][j].m_type == MarkerType.PHEROMONE:
                    # print('ANT -> ', self.destination)
                    # print('PHEROMONE -> ', self.matrix[i][j].target)
                    if ((self.matrix[i][j].target == PheromoneType.TO_ENEMY
                         and self.destination == Action.TO_ENEMY) or
                            (self.matrix[i][j].target == PheromoneType.TO_COLONY
                             and self.destination == Action.COLONY)):
                        if self.matrix[i][j].creator == self.colony_id:
                            object_sighted = self.matrix[i][j]
                            object_i = i
                            object_j = j
                            self.last_pheromone_distance = self.matrix[i][j].distance
                            self.heading_towards_objective = True
                            self.last_objective_sighted = object_sighted
                            self.last_objective_sighted_x = j
                            self.last_objective_sighted_y = i
                            # Globals.resume_pheromone_cleanup()
                            return object_sighted, object_i, object_j
        # Globals.resume_pheromone_cleanup()
        return object_sighted, object_i, object_j

    def object_sighted(self):
        above = self.y - Globals.ant_FOV
        below = self.y + Globals.ant_FOV + 1
        left = self.x - Globals.ant_FOV
        right = self.x + Globals.ant_FOV + 1
        object_sighted = None
        object_i = -1
        object_j = -1
        first_checked_position_x, first_checked_position_y = self.get_first_angle_to_check()
        best_object = None
        best_object_i = -1
        best_object_j = -1
        if first_checked_position_y == above:
            if first_checked_position_x == left:
                for i in range(0, Globals.ant_FOV + 1):
                    for j in range(i, Globals.ant_FOV + 1):
                        if 0 < i + above < Globals.height and 0 < j + left < Globals.width:
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(i + above, j + left)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
                        if i != j and 0 < j + above < Globals.height and 0 < i + left < Globals.width:
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(j + above, i + left)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
            elif first_checked_position_x == right:
                for i in range(0, Globals.ant_FOV + 1):
                    for j in range(2 * Globals.ant_FOV - i, Globals.ant_FOV - 1, -1):
                        if 0 < i + above < Globals.height and 0 < j + left < Globals.width:
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(i + above, j + left)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
                        if (i + j != below - above - 1 and 0 < below - j - 1 < Globals.height
                                and 0 < right - i - 1 < Globals.width):
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(below - j - 1, right - i - 1)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
            else:
                for i in range(0, Globals.ant_FOV + 1):
                    for j in range(Globals.ant_FOV, 2 * Globals.ant_FOV - i + 1):
                        if 0 < i + above < Globals.height and 0 < j + left < Globals.width:
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(i + above, j + left)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
                        if (j != self.x - left and 0 < i + above < Globals.height
                                and 0 < 2 * self.x - j - left < Globals.width):
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(i + above, 2 * self.x - j - left)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
        elif first_checked_position_y == below:
            if first_checked_position_x == left:
                for i in range(0, Globals.ant_FOV + 1):
                    for j in range(i, Globals.ant_FOV + 1):
                        if 0 < below - i - 1 < Globals.height and 0 < j + left < Globals.width:
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(below - i - 1, j + left)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
                        if (i + j != below - above and 0 < below - j - 1 < Globals.height
                                and 0 < i + left < Globals.width):
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(below - j - 1, i + left)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
            elif first_checked_position_x == right:
                for i in range(0, Globals.ant_FOV + 1):
                    for j in range(2 * Globals.ant_FOV - i, Globals.ant_FOV - 1, -1):
                        if 0 < below - i - 1 < Globals.height and 0 < j + left < Globals.width:
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(below - i - 1, j + left)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
                        if i != j and 0 < above + j < Globals.height and 0 < right - i - 1 < Globals.width:
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(above + j, right - i - 1)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
            else:
                for i in range(0, Globals.ant_FOV + 1):
                    for j in range(Globals.ant_FOV, 2 * Globals.ant_FOV + 1 - i):
                        if 0 < below - i - 1 < Globals.height and 0 < j + left < Globals.width:
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(below - i - 1, j + left)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
                        if (j != self.x - left and 0 < below - i - 1 < Globals.height
                                and 0 < 2 * self.x - j - left < Globals.width):
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(below - i - 1, 2 * self.x - j - left)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
        else:
            if first_checked_position_x == left:
                for j in range(0, Globals.ant_FOV):
                    for i in range(0, Globals.ant_FOV - j + 1):
                        if 0 < i + self.y < Globals.height and 0 < j + left < Globals.width:
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(i + self.y, j + left)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
                        if i != 0 and 0 < self.y - i < Globals.height and 0 < j + left < Globals.width:
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(self.y - i, j + left)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
            else:
                for j in range(Globals.ant_FOV, 0, -1):
                    for i in range(0, j + 1):
                        if 0 < i + self.y < Globals.height and 0 < j + self.x < Globals.width:
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(i + self.y, j + self.x)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
                        if i != 0 and 0 < self.y - i < Globals.height and 0 < j + self.x < Globals.width:
                            object_sighted, object_i, object_j = \
                                self.look_for_object_at_precise_spot(self.y - i, j + self.x)
                        if object_sighted is not None:
                            if object_sighted.m_type == MarkerType.PHEROMONE:
                                if best_object is None:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                                elif object_sighted.distance < best_object.distance:
                                    best_object = object_sighted
                                    best_object_i = object_i
                                    best_object_j = object_j
                            else:
                                return object_sighted, object_i, object_j
        return best_object, best_object_i, best_object_j

    def move_to_explore(self):
        movement_change = True if random.random() < Globals.exploration_rate else False
        if movement_change:
            self.slightly_change_direction()
        else:
            self.perform_movement()
