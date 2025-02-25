from time import sleep

from Globals import Globals
from Graphics import Graphics
from Simulation import Simulation

w = 20
h = 20
m = [['.' for _ in range(w)] for _ in range(h)]
y = 3
x = 18
above = y - Globals.ant_FOV
below = y + Globals.ant_FOV + 1
left = x - Globals.ant_FOV
right = x + Globals.ant_FOV + 1
print('above', above)
print('below', below)
print('right', right)
print('left', left)
heading_y = 1
heading_x = -1
sleep_time = 0.25

for i in range(max(above, 0), min(below, h)):
    for j in range(max(left, 0), min(right, w)):
        m[i][j] = '_'

if heading_y == -1:
    if heading_x == 0:
        first_checked_position_x, first_checked_position_y = x, above
    elif heading_x == 1:
        first_checked_position_x, first_checked_position_y = right, above
    else:
        first_checked_position_x, first_checked_position_y = left, above
elif heading_y == 1:
    if heading_x == 0:
        first_checked_position_x, first_checked_position_y = x, below
    elif heading_x == 1:
        first_checked_position_x, first_checked_position_y = right, below
    else:
        first_checked_position_x, first_checked_position_y = left, below
else:
    if heading_x == 1:
        first_checked_position_x, first_checked_position_y = right, y
    else:
        first_checked_position_x, first_checked_position_y = left, y

if first_checked_position_y == above:
    if first_checked_position_x == left:
        for i in range(0, Globals.ant_FOV + 1):
            for j in range(i, Globals.ant_FOV + 1):
                sleep(sleep_time)
                m[y][x] = 'X'

                for f in range(h):
                    for g in range(w):
                        print(m[f][g], " ", end=' ')
                    print()
                print('MMMMMMMMMMMMMMMMMMMMMMMMMM')
                if 0 < i + above < h and 0 < j + left < w:
                    m[i + above][j + left] = '0'
                if i != j and 0 < j + above < h and 0 < i + left < w:
                    m[j + above][i + left] = '0'
    elif first_checked_position_x == right:
        for i in range(0, Globals.ant_FOV + 1):
            for j in range(2 * Globals.ant_FOV - i, Globals.ant_FOV - 1, -1):
                sleep(sleep_time)
                m[y][x] = 'X'

                for f in range(h):
                    for g in range(w):
                        print(m[f][g], " ", end=' ')
                    print()
                print('MMMMMMMMMMMMMMMMMMMMMMMMMM')
                if 0 < i + above < h and 0 < j + left < w:
                    m[i + above][j + left] = '0'
                if i + j != below - above - 1 and 0 < below - j - 1 < h and 0 < right - i - 1 < w:
                    m[below - j - 1][right - i - 1] = '0'
    else:
        for i in range(0, y + 1 - above):
            for j in range(Globals.ant_FOV, 2 * Globals.ant_FOV - i + 1):
                sleep(sleep_time)
                m[y][x] = 'X'

                for f in range(h):
                    for g in range(w):
                        print(m[f][g], " ", end=' ')
                    print()
                if 0 < i + above < h and 0 < j + left < w:
                    m[i + above][j + left] = '0'
                if j != x - left and 0 < i + above < h and 0 < 2 * x - j - left < w:
                    m[i + above][2 * x - j - left] = '0'
elif first_checked_position_y == below:
    if first_checked_position_x == left:
        for i in range(0, below - y):
            for j in range(i, x + 1 - left):
                sleep(sleep_time)
                m[y][x] = 'X'

                for f in range(h):
                    for g in range(w):
                        print(m[f][g], " ", end=' ')
                    print()
                m[below - i - 1][j + left] = '0'
                if i + j != below - above:
                    m[below - j - 1][left + i] = '0'
    elif first_checked_position_x == right:
        for i in range(0, below - y):
            for j in range(right - left - i - 1, x - left - 1, -1):
                sleep(sleep_time)
                m[y][x] = 'X'

                for f in range(h):
                    for g in range(w):
                        print(m[f][g], " ", end=' ')
                    print()
                m[below - i - 1][j + left] = '0'
                if i != j:
                    m[above + j][right - i - 1] = '0'
    else:
        for i in range(0, below - y):
            for j in range(x - left, right - left - i):
                sleep(sleep_time)
                m[y][x] = 'X'

                for f in range(h):
                    for g in range(w):
                        print(m[f][g], " ", end=' ')
                    print()
                m[below - i - 1][j + left] = '0'
                if j != x - left:
                    m[below - i - 1][2*x - j - left] = '0'
else:
    if first_checked_position_x == left:
        for j in range(0, x - left):
            for i in range(0, Globals.ant_FOV):
                sleep(sleep_time)
                m[y][x] = 'X'

                for f in range(h):
                    for g in range(w):
                        print(m[f][g], " ", end=' ')
                    print()
                print('MMMMMMMMMMMMMMMMMMMMMMMMMM')
                if i + y < 20:
                    m[i + y][j + left] = '0'
                if i != 0 and y - i > 0:
                    m[y - i][j + left] = '0'
    else:
        for j in range(right - x - 1, 0, -1):
            for i in range(0, j + 1):
                sleep(sleep_time)
                m[y][x] = 'X'

                for f in range(h):
                    for g in range(w):
                        print(m[f][g], " ", end=' ')
                    print()
                print('MMMMMMMMMMMMMMMMMMMMMMMMMM')
                if i + y < 20:
                    m[i + y][j + x] = '0'
                if i != 0 and y - i > 0:
                    m[y - i][j + x] = '0'

m[y][x] = 'X'

for i in range(h):
    for j in range(w):
        print(m[i][j], " ", end=' ')
    print()
# sim = Simulation()
# sim.add_colony(500, 500)
# sim.add_colony(1000, 500)
# col = sim.get_colony(0)
# for _ in range(Globals.col1_ants_generated):
#     col.produce_ant('worker')
# col1 = sim.get_colony(1)
# for _ in range(Globals.col2_ants_generated):
#     col1.produce_ant('soldier')
# # sim.add_food_source(1300, 200)
# sim.add_food_source(700, 300)
# sim.add_food_source(300, 300)
# sim.add_food_source(700, 700)
# sim.add_food_source(300, 700)
# sim.add_food_source(800, 500)
# sim.add_food_source(200, 500)
# sim.add_food_source(500, 800)
# sim.add_food_source(500, 200)
# graphics = Graphics(sim)
