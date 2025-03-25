import time
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
            # start_timer = time.perf_counter() * 100000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.clear()
            self.draw_sim()
            self.sim_update()
            update()
            if Globals.delay_rate:
                sleep(Globals.delay_rate)
            # print("Time taken in Graphics big loop: ", time.perf_counter() * 100000 - start_timer)
        quit()

    def draw_sim(self):
        for pheromone in Globals.pheromones:
            if pheromone.target == PheromoneType.TO_COLONY:
                if pheromone.creator == 0:
                    pygame.draw.circle(self.screen, (255, 0, 0), (pheromone.x, pheromone.y), 1)
                elif pheromone.creator == 1:
                    pygame.draw.circle(self.screen, (0, 0, 255), (pheromone.x, pheromone.y), 1)
                else:
                    pygame.draw.circle(self.screen, (0, 0, 0), (pheromone.x, pheromone.y), 1)
        for pheromone in Globals.pheromones:
            if pheromone.target == PheromoneType.TO_FOOD:
                pygame.draw.circle(self.screen, (0, 255, 0), (pheromone.x, pheromone.y), 1)
        for pheromone in Globals.pheromones:
            if pheromone.target == PheromoneType.TO_ENEMY:
                pygame.draw.circle(self.screen, (0, 0, 0), (pheromone.x, pheromone.y), 1)
        for food_source in Globals.food_sources:
            pygame.draw.circle(self.screen, (0, 0, 0), (food_source.x, food_source.y), 26)  # border
            pygame.draw.circle(self.screen, (0, 255, 0), (food_source.x, food_source.y), 25)
            font = pygame.font.SysFont(None, 24)
            food_size_text = font.render(str(food_source.size), True, (0, 0, 0))
            self.screen.blit(food_size_text, (food_source.x - 10, food_source.y - 10))
        for colony in Globals.colonies:
            colony_color = (0, 0, 0)
            if colony.colony_id == 0:
                colony_color = (255, 0, 0) # red
            elif colony.colony_id == 1:
                colony_color = (0, 0, 255) # blue
            pygame.draw.circle(self.screen, (0, 0, 0), (colony.x, colony.y), 31)  # border
            pygame.draw.circle(self.screen, colony_color, (colony.x, colony.y), 30)
            font = pygame.font.SysFont(None, 24)
            food_size_text = font.render(str(colony.food_supply), True, (255, 255, 255))
            self.screen.blit(food_size_text, (colony.x - 10, colony.y - 10))
            x = colony.x
            y = colony.y
            above = int(max(0, y - 30))
            below = int(min(899, y + 30))
            left = int(max(0, x - 30))
            right = int(min(1519, x + 30))
            for ant in colony.ants:
                # pygame.draw.rect(self.screen, (0, 0, 0),
                #                  (ant.x - Globals.ant_FOV, ant.y - Globals.ant_FOV,
                #                   Globals.ant_FOV * 2, Globals.ant_FOV * 2), 1)
                if isinstance(ant, Worker):
                    pygame.draw.circle(self.screen, (0, 0, 0), (ant.x, ant.y), 4)  # border
                    pygame.draw.circle(self.screen, colony_color, (ant.x, ant.y), 3)
                    pygame.draw.circle(self.screen, (0, 0, 0),
                                       (ant.x + 5 * ant.heading_x, ant.y + 5 * ant.heading_y), 4)
                    pygame.draw.circle(self.screen, colony_color,
                                       (ant.x + 5 * ant.heading_x, ant.y + 5 * ant.heading_y), 3)
                elif isinstance(ant, Soldier):
                    pygame.draw.circle(self.screen, (0, 0, 0), (ant.x, ant.y), 6)
                    pygame.draw.circle(self.screen, colony_color, (ant.x, ant.y), 5)
                    pygame.draw.circle(self.screen, (0, 0, 0),
                                       (ant.x + 7 * ant.heading_x, ant.y + 7 * ant.heading_y), 6)
                    pygame.draw.circle(self.screen, colony_color,
                                       (ant.x + 7 * ant.heading_x, ant.y + 7 * ant.heading_y), 5)

            font = pygame.font.SysFont(None, 24)
            red_workers = sum(colony.nr_of_workers for colony in Globals.colonies if colony.colony_id == 0)
            red_soldiers = sum(colony.nr_of_soldiers for colony in Globals.colonies if colony.colony_id == 0)
            blue_workers = sum(colony.nr_of_workers for colony in Globals.colonies if colony.colony_id == 1)
            blue_soldiers = sum(colony.nr_of_soldiers for colony in Globals.colonies if colony.colony_id == 1)
            red_text_surface1 = font.render(f"Red Workers: {red_workers}", True, (0, 0, 0))
            red_text_surface2 = font.render(f"Red Soldiers: {red_soldiers}", True, (0, 0, 0))
            blue_text_surface1 = font.render(f"Blue Workers: {blue_workers}", True, (0, 0, 0))
            blue_text_surface2 = font.render(f"Blue Soldiers: {blue_soldiers}", True, (0, 0, 0))
            self.screen.blit(red_text_surface1, (50, 25))
            self.screen.blit(red_text_surface2, (50, 50))
            self.screen.blit(blue_text_surface1, (Globals.width - blue_text_surface1.get_width() - 50, 25))
            self.screen.blit(blue_text_surface2, (Globals.width - blue_text_surface2.get_width() - 50, 50))
            # print(Globals.ant_FOVs)
            # for FOV in Globals.ant_FOVs:
            #     pygame.draw.rect(self.screen, (0, 0, 0), (FOV[1], FOV[0], 1, 1))

    def clear(self):
        self.screen.fill((255, 255, 255))

    def sim_update(self):
        self.simulation.update()
