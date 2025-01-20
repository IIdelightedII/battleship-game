from battleship_game import BattleshipGame
from field import Field
import constants

game = BattleshipGame(12, [11])
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

game.place_ships_randomly(game.player_field)
game.player_field.display(True)
