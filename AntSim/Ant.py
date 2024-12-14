import random

from Action import Action


class Ant:
    def __init__(self, max_health: int,
                 destination: Action,
                 attack: int,
                 x: int,
                 y: int,
                 heading_x: int,
                 heading_y: int,
                 state: int,
                 colony_id: int,
                 speed: float):
        self.is_carrying_food = False
        self.speed = speed
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

    def max_health(self) -> int:
        return self.max_health

    def drop_pheromone(self, pheromone_type: int) -> None:
        # Implement the logic to drop a pheromone of the given type
        pass

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

    def move(self) -> None:
        if self.destination == Action.IDLE:
            self.move_randomly()
        elif self.destination == Action.FOOD:
            self.move_towards_food()
        elif self.destination == Action.COLONY:
            self.move_towards_colony()
        elif self.destination == Action.FIGHT:
            self.move_towards_enemy()
        elif self.destination == Action.PATROL:
            self.patrol()

    def update(self):
        self.move()

    def move_towards_food(self):
        pass

    def move_towards_colony(self):
        pass

    def move_towards_enemy(self):
        pass

    def patrol(self):
        pass
