from time import sleep

from Globals import Globals
from Graphics import Graphics
from Simulation import Simulation

sim = Simulation()
sim.add_colony(500, 400)
# sim.add_colony(1000, 400)
col = sim.get_colony(0)
for _ in range(Globals.col1_ants_generated):
    col.produce_ant('worker')
# col1 = sim.get_colony(1)
# for _ in range(Globals.col2_ants_generated):
#     col1.produce_ant('soldier')
# sim.add_food_source(50, 50)
# sim.add_food_source(Globals.width - 50, 50)
# sim.add_food_source(50, Globals.height - 50)
# sim.add_food_source(Globals.width - 50, Globals.height - 50)
# sim.add_food_source(1000, 200)
# sim.add_food_source(1100, 200)
# sim.add_food_source(300, 200)
# sim.add_food_source(700, 600)
# sim.add_food_source(300, 600)
# sim.add_food_source(1100, 400)
# sim.add_food_source(1100, 600)
# sim.add_food_source(300, 400)
# sim.add_food_source(700, 400)
# sim.add_food_source(500, 600)
# sim.add_food_source(500, 200)
graphics = Graphics(sim)
