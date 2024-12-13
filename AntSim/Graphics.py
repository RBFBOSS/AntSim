import pygame
import sys


def quit_graphics():
    pygame.quit()
    sys.exit()


def update():
    pygame.display.flip()


class Graphics:
    def __init__(self, simulation):
        pygame.init()
        self.screen = pygame.display.set_mode((1520, 900))
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
        quit()

    def draw_sim(self):
        for colony in self.simulation.colonies:
            pygame.draw.circle(self.screen, (0, 0, 0), (colony.x, colony.y), 10)
            for ant in colony.ants:
                pygame.draw.circle(self.screen, (0, 0, 0), (ant.x, ant.y), 5)

    def clear(self):
        self.screen.fill((255, 255, 255))

    def sim_update(self):
        self.simulation.update()
