from dataclasses import field
from random import random, Random

from battleship_game import BattleshipGame
from field import Field
import constants
from input_turner import InputTurner
from random_turner import RandomTurner
from ship import Ship
import random
from finishing_turner import FinishingTurner
from probability_turner import ProbabilityTurner
from turner import Turner

size = 5
ship_types = [0, 2, 1]
field1 = Field(size, ship_types)
field2 = Field(size, ship_types)
field2.display()
turner1 = FinishingTurner(field2)
turner2 = ProbabilityTurner(field1)
field1.grid[3][3] = constants.SHIP
turner2.searching_ship(3)

print(turner2.probability_grid)
# game = BattleshipGame(size, ship_types, field1, field2, turner1, turner2)
# game.play(True)



