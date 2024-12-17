from time import sleep

import pygame
import sys

from Globals import Globals
from PheromoneType import PheromoneType
from Soldier import Soldier
from Worker import Worker


def quit_graphics():
    pygame.quit()
    sys.exit()


def update():
    pygame.display.flip()


class Graphics:
    def __init__(self, simulation):
        pygame.init()
        self.screen = pygame.display.set_mode((Globals.width, Globals.height))
        self.simulation = simulation
        pygame.display.set_caption("AntSim")
        self.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.clear()
            self.draw_sim()
            self.sim_update()
            update()
            if Globals.delay_rate:
                sleep(Globals.delay_rate)
        quit()

    def draw_sim(self):
        for pheromone in Globals.pheromones:
            if pheromone.target == PheromoneType.TO_COLONY:
                pygame.draw.circle(self.screen, (255, 0, 0), (pheromone.x, pheromone.y), 1)
        for pheromone in Globals.pheromones:
            if pheromone.target == PheromoneType.TO_FOOD:
                pygame.draw.circle(self.screen, (0, 0, 255), (pheromone.x, pheromone.y), 1)
        for food_source in Globals.food_sources:
            pygame.draw.circle(self.screen, (0, 255, 0), (food_source.x, food_source.y), 25)
        for colony in Globals.colonies:
            pygame.draw.circle(self.screen, (0, 0, 0), (colony.x, colony.y), 30)
            x = colony.x
            y = colony.y
            above = int(max(0, y - 30))
            below = int(min(899, y + 30))
            left = int(max(0, x - 30))
            right = int(min(1519, x + 30))
            for ant in colony.ants:
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 (ant.x - Globals.ant_FOV, ant.y - Globals.ant_FOV,
                                  Globals.ant_FOV * 2, Globals.ant_FOV * 2), 1)
                if isinstance(ant, Worker):
                    pygame.draw.circle(self.screen, (0, 0, 0), (ant.x, ant.y), 5)
                    pygame.draw.circle(self.screen, (0, 0, 0),
                                       (ant.x + 5 * ant.heading_x, ant.y + 5 * ant.heading_y), 5)
                elif isinstance(ant, Soldier):
                    pygame.draw.circle(self.screen, (0, 0, 0), (ant.x, ant.y), 7)
                    pygame.draw.circle(self.screen, (0, 0, 0),
                                       (ant.x + 7 * ant.heading_x, ant.y + 7 * ant.heading_y), 7)

    def clear(self):
        self.screen.fill((255, 255, 255))

    def sim_update(self):
        self.simulation.update()
