from field import Field
import constants
from utility import clamp
from ship import Ship

class Turner:
    def __init__(self, field: Field):
        self.field = field


    def _turn(self, x: int, y: int):
        if self.field.grid[y][x].isdigit():
            ship_number = self.field.grid[y][x]
            ship = self.field.ships[ship_number]
            ship.hp -= 1
            self.field.grid[y][x] = constants.DESTROYED_SHIP
            # print(f"{user} попал!, координаты: {x + 1}, {y + 1}")

            if ship.hp == 0:
                # print(f"{user} уничтожил корабль!")
                self.field.ship_count -= 1
                self.place_buffer_zone(self.field, ship, constants.EXTRA_BUFFER_ZONE)

                self.place_ship(self.field, ship, constants.FULLY_DESTROYED_SHIP)
            print("-" * 20)
            return True  # return [был ли выстрел], [попал ли в корабль], [координата x], [координата y]
        elif self.field.grid[y][x] == constants.EMPTY or self.field.grid[y][x] == constants.BUFFER_ZONE:
            self.field.grid[y][x] = constants.MISS
            # print(f"{user} промахнулся, координаты: {x + 1}, {y + 1}")
            # print("-" * 20)
            return True  # return [был ли выстрел], [попал ли в корабль]
        else:
            return False

    def place_buffer_zone(self, field: Field, ship: Ship, symbol: str) -> None:

        point1 = (clamp(ship.x - 1 * (ship.x_indent + ship.y_indent), 0, self.field.size - 1),
                  clamp((ship.y - 1 * (ship.x_indent + ship.y_indent)), 0, self.field.size - 1))
        point2 = (clamp((ship.x + ship.x_indent * ship.len + abs(ship.y_indent) * (ship.x_indent + ship.y_indent)), 0,
                        self.field.size - 1),
                  clamp((ship.y + ship.y_indent * ship.len + abs(ship.x_indent) * (ship.x_indent + ship.y_indent)), 0,
                        self.field.size - 1))

        for x in range(min(point2[0], point1[0]), max(point2[0], point1[0]) + 1):
            for y in range(min(point2[1], point1[1]), max(point2[1], point1[1]) + 1):
                field.grid[y][x] = symbol

    def place_ship(self, field: Field, ship: Ship, symbol: str | int) -> None:
        for k in range(ship.len):
            field.grid[ship.y + ship.y_indent * k][ship.x + ship.x_indent * k] = str(symbol)


    def make_turn(self):
        pass


