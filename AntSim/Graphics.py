import threading
from time import sleep
import pygame
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Globals import Globals
from PheromoneType import PheromoneType
from Soldier import Soldier
from Worker import Worker


def quit_graphics():
    pygame.quit()
    sys.exit()


class Graphics:
    def __init__(self, simulation):
        pygame.init()
        self.screen = pygame.display.set_mode((Globals.width, Globals.height))
        self.simulation = simulation
        pygame.display.set_caption("AntSim")

        # Initialize the graph in a separate thread
        self.graph_thread = threading.Thread(target=self.init_graph)
        self.graph_thread.start()

        self.run()

    def init_graph(self):
        self.fig, self.ax = plt.subplots()
        self.colony1_population, = self.ax.plot([], [], label='Colony 1 Population', color='#00FFFF')  # Cyan
        self.colony2_population, = self.ax.plot([], [], label='Colony 2 Population', color='#FF00FF')  # Magenta
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.legend()
        self.time_data = []
        self.colony1_data = []
        self.colony2_data = []

        self.ani = FuncAnimation(self.fig, self.update_graph, interval=1000, cache_frame_data=False)
        plt.show()

    def update_graph(self, frame):
        self.time_data.append(Globals.global_time_frame)
        self.colony1_data.append(
            sum(colony.nr_of_workers + colony.nr_of_soldiers for colony in Globals.colonies if colony.colony_id == 0))
        self.colony2_data.append(
            sum(colony.nr_of_workers + colony.nr_of_soldiers for colony in Globals.colonies if colony.colony_id == 1))

        self.colony1_population.set_data(self.time_data, self.colony1_data)
        self.colony2_population.set_data(self.time_data, self.colony2_data)

        self.ax.set_xlim(0, max(100, Globals.global_time_frame))
        self.ax.set_ylim(0, max(100, max(self.colony1_data + self.colony2_data)))
        self.fig.canvas.draw()

    def update(self):
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.clear()
            self.draw_sim()
            self.sim_update()
            self.update()
            if Globals.delay_rate:
                sleep(Globals.delay_rate)
        quit()

    def draw_sim(self):
        for pheromone in Globals.pheromones:
            if pheromone.target == PheromoneType.TO_COLONY:
                if pheromone.creator == 0:
                    pygame.draw.circle(self.screen, Globals.first_colony_color, (pheromone.x, pheromone.y), 1)
                elif pheromone.creator == 1:
                    pygame.draw.circle(self.screen, Globals.second_colony_color, (pheromone.x, pheromone.y), 1)
                else:
                    pygame.draw.circle(self.screen, (255, 0, 0), (pheromone.x, pheromone.y), 1)
        for pheromone in Globals.pheromones:
            if pheromone.target == PheromoneType.TO_FOOD:
                pygame.draw.circle(self.screen, (0, 255, 0), (pheromone.x, pheromone.y), 1)
            elif pheromone.target == PheromoneType.TO_ENEMY:
                pygame.draw.circle(self.screen, (0, 0, 0), (pheromone.x, pheromone.y), 1)
            elif pheromone.target == PheromoneType.BLOOD:
                pygame.draw.circle(self.screen, (255, 0, 0), (pheromone.x, pheromone.y), 1)
        for food_source in Globals.food_sources:
            pygame.draw.circle(self.screen, (0, 0, 0), (food_source.x, food_source.y), 21)  # border
            pygame.draw.circle(self.screen, (0, 255, 0), (food_source.x, food_source.y), 20)
            font = pygame.font.SysFont(None, 24)
            food_size_text = font.render(str(food_source.size), True, (0, 0, 0))
            self.screen.blit(food_size_text, (food_source.x - 10, food_source.y - 10))
        for colony in Globals.colonies:
            colony_color = (0, 0, 0)
            if colony.colony_id == 0:
                colony_color = Globals.first_colony_color
            elif colony.colony_id == 1:
                colony_color = Globals.second_colony_color
            pygame.draw.circle(self.screen, (0, 0, 0), (colony.x, colony.y), 21)  # border
            pygame.draw.circle(self.screen, colony_color, (colony.x, colony.y), 20)
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
                if isinstance(ant, Worker):
                    pygame.draw.circle(self.screen, (0, 0, 0), (ant.x, ant.y), 2)  # border
                    pygame.draw.circle(self.screen, colony_color, (ant.x, ant.y), 1)
                    pygame.draw.circle(self.screen, (0, 0, 0),
                                       (ant.x + 2 * ant.heading_x, ant.y + 2 * ant.heading_y), 2)
                    pygame.draw.circle(self.screen, colony_color,
                                       (ant.x + 2 * ant.heading_x, ant.y + 2 * ant.heading_y), 1)
                elif isinstance(ant, Soldier):
                    pygame.draw.circle(self.screen, (0, 0, 0), (ant.x, ant.y), 3)
                    pygame.draw.circle(self.screen, colony_color, (ant.x, ant.y), 2)
                    pygame.draw.circle(self.screen, (0, 0, 0),
                                       (ant.x + 4 * ant.heading_x, ant.y + 4 * ant.heading_y), 3)
                    pygame.draw.circle(self.screen, colony_color,
                                       (ant.x + 4 * ant.heading_x, ant.y + 4 * ant.heading_y), 2)

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

    def clear(self):
        self.screen.fill((255, 255, 255))

    def sim_update(self):
        self.simulation.update()