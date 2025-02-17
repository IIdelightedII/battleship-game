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

from turner import Turner

size = 7
ship_types = [0, 3, 3]
field1 = Field(size, ship_types)
field2 = Field(size, ship_types)
turner1 = FinishingTurner(field2)
turner2 = RandomTurner(field1)
game = BattleshipGame(size, ship_types, field1, field2, turner1, turner2)
game.play(True)

# todo 1. Дописать display - если встречается буферная зона, то изменять на пустую клетку
# todo 2. Добавить цвета в дисплей(переписать)
# todo 3. Продолжить finishing turner

