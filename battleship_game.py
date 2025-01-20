import random
from field import Field
import constants
from utility import clamp

class BattleshipGame:
    def __init__(self, size: int, ship_types: list):
        self.size = size
        self.ship_types = ship_types
        self.player_field = Field(self.size, self.ship_types)
        self.computer_field = Field(self.size, self.ship_types)

    # Это функция расстановки кораблей, она уже полностью написана
    def place_ships_randomly(self, grid):

        for ship_len in range(len(self.ship_types)):

            # print(f"{self.ships[ship_len] = }")

            for _ in range(self.ship_types[ship_len]):
                placed = False
                # print(f"{_ + 1} {ship_len + 1}-палубных кораблей")
                while not placed:
                    # ship_len += 1
                    coords, indents = self.generate_ship()
                    x, y = coords
                    x_indent, y_indent = indents
                    #
                    # print(f"{indents = }")
                    # print(f"{x = }")
                    # print(f"{y = }")
                    # print(f"{x_indent = }")
                    # print(f"{y_indent = }")

                    if not self.is_valid_ship_placement(grid, coords, (x_indent, y_indent), ship_len + 1):
                        continue

                    grid = self.generate_buffer_zone(grid, x, y, x_indent, y_indent, ship_len + 1)

                    # grid[coords[1]][coords[0]] = constants.SHIP
                    # grid[point1[1]][point1[0]] = constants.DESTROYED_SHIP
                    # grid[point2[1]][point2[0]] = constants.BUFFER_ZONE
                    # # for j in range(point1[1], point2[1] + 1):
                    #     for k in range(point1[0], point2[1]):
                    grid = self.place_ship(grid, x, y, x_indent, y_indent, ship_len + 1)

                    placed = True
                    # print(f"{ship_len =  }")
        return grid
                    # except IndexError:
                    #     pass
                # if self.is_valid_ship_placement(grid, coords): # либо сделать условие, либо сделать так, чтобы ошибок быть не могло, кроме столкновений
                #     grid.grid[coords[0]][coords[1]] = "S"


    # Это функция проверки расстановки кораблей, она уже полностью написана
    def is_valid_ship_placement(self, grid: Field, coords: tuple[int, int], direction: tuple[int, int], ship_length: int = 1) -> bool:
        x, y = coords
        x_indent, y_indent = direction
        if not (0 <= x + x_indent * ship_length < self.size and 0 <= y + y_indent * ship_length < self.size):
            return False
        for k in range(ship_length):
            if (grid.grid[y + y_indent * k][x + x_indent * k] == constants.SHIP or
                grid.grid[y + y_indent * k][x + x_indent * k] == constants.BUFFER_ZONE):
                return False
        return True
        # # Проверка на наличие соседних клеток по горизонтали и вертикали
        # for i in range(ship_length + 2):
        #     for j in range(-1, 2):
        #         for k in range(-1, 2):
        #             new_x, new_y = x + j, y + k
        #             if 0 <= new_x < self.size and 0 <= new_y < self.size and field.grid[new_x][new_y] == "S":
        #                 return False

    def generate_ship(self) -> tuple[tuple[int, int], tuple[int, int]]:
        direction = random.choice(["left", "right", "down", "up"])
        x, y = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
        if direction == "left":
            x_indent = -1
            y_indent = 0
        elif direction == "right":
            x_indent = 1
            y_indent = 0
        elif direction == "down":
            x_indent = 0
            y_indent = 1
        elif direction == "up":
            x_indent = 0
            y_indent = -1
        return (x, y), (x_indent, y_indent)


    def generate_buffer_zone(self, grid:  Field, x: int, y: int, x_indent: int, y_indent: int, ship_len: int) ->  Field:
        point1 = (clamp(x - 1 * (x_indent + y_indent), 0, self.size - 1),
                  clamp((y - 1 * (x_indent + y_indent)), 0, self.size - 1))
        point2 = (clamp((x + x_indent * ship_len + abs(y_indent) * (x_indent + y_indent)), 0, self.size - 1),
                  clamp((y + y_indent * ship_len + abs(x_indent) * (x_indent + y_indent)), 0, self.size - 1))

        for x in range(min(point2[0], point1[0]), max(point2[0], point1[0]) + 1):
            for y in range(min(point2[1], point1[1]), max(point2[1], point1[1]) + 1):
                grid.grid[y][x] = constants.BUFFER_ZONE

        return grid

    def place_ship(self, grid: Field, x: int, y: int, x_indent: int, y_indent: int, ship_len: int) -> Field:
        for k in range(ship_len):
            grid.grid[y + y_indent * k][x + x_indent * k] = constants.SHIP

        return grid


    def play(self):
        self.place_ships_randomly(self.player_field, self.ship_types)
        self.place_ships_randomly(self.computer_field, self.ship_types)
        print("Расстановка кораблей компьютера:")

        print("Ваша расстановка кораблей:")