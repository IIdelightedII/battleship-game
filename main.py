from dataclasses import field
from random import random

from battleship_game import BattleshipGame
from field import Field
import constants
from input_turner import InputTurner
from random_turner import RandomTurner
from ship import Ship
import random

from turner import Turner

size = 3
ship_types = [1]
field1 = Field(size, ship_types)
field2 = Field(size, ship_types)
turner1 = InputTurner(field2)
turner2 = RandomTurner(field1)
game = BattleshipGame(size, ship_types, field1, field2, turner1, turner2)
game.play()