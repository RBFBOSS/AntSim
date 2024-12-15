from Graphics import Graphics
from Simulation import Simulation

sim = Simulation(1520, 900)
sim.add_colony(500, 500)
sim.add_colony(1000, 500)
col = sim.get_colony(0)
for _ in range(5):
    col.produce_ant('worker')
col1 = sim.get_colony(1)
for _ in range(0):
    col1.produce_ant('soldier')
sim.add_food_source(300, 300)
sim.add_food_source(700, 700)
graphics = Graphics(sim)
