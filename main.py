from random import random

from battleship_game import BattleshipGame
from field import Field
import constants
from ship import Ship
import random

game = BattleshipGame(5, ([0, 0, 0, 1]))
ship = Ship(5, 5, 1, 0, 1)
# grid = Field(12, [0])
#
#
# game.player_field = game.generate_buffer_zone(grid, 11, 0, -1, 0, 3) # правый верхний
# game.player_field = game.place_ship(grid, 11, 0, -1, 0, 3)
#
# # game.player_field = game.generate_buffer_zone(grid, 0, 11, 1, 0, 3) # левый нижний
# # game.player_field = game.place_ship(grid, 0, 11, 1, 0, 3)
#
# game.player_field = game.generate_buffer_zone(grid, 11, 11, 0, -1, 3)   # правый нижний
# game.player_field = game.place_ship(grid, 11, 11, 0, -1, 3)
#
# game.player_field = game.generate_buffer_zone(grid, 4, 5, 0, -1, 3)
# game.player_field = game.place_ship(grid, 4, 5, 0, -1, 3)


# print(game.is_valid_ship_placement(grid, (0, 11), (0, 1), 3))
# game.player_field = game.generate_buffer_zone(grid, 0, 11, 0, 1, 3) # левый верхний
# game.player_field = game.place_ship(grid, 0, 11, 0, 1, 3)

# grid.grid[6][11] = constants.MISS
# game.place_ship(game.computer_field, ship, 1)
# game.place_ships_randomly(game.computer_field)
# print(game.player_field)
# game.computer_field.display(True, True)
# # game.player_turn(5, 5)
# for i in range(1, 100):
#     game.player_turn(random.randint(0, 9), random.randint(0, 9))
# game.computer_field.display(True, True)
# game.play()
# game.player_input()
game.play()