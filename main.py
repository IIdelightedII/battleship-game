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

size = 100
ship_types = [0, 4, 3, 2, 1]
field1 = Field(size, ship_types.copy())
field2 = Field(size, ship_types.copy())
turner1 = ProbabilityTurner(field2)
turner2 = InputTurner(field1)

game = BattleshipGame(size, ship_types, field1, field2, turner1, turner2)
turner1.make_field_map()
print(turner1.field_map)
print(field2.ship_types)
game.play()



