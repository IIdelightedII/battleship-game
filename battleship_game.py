from dataclasses import field
from itertools import count

from field import Field
import constants
from utility import clamp
from ship import Ship
import random
from turner import Turner


class BattleshipGame:
    def __init__(self, size: int, player1_field: Field, player2_field: Field, player1_turner: Turner,
                 player2_turner: Turner):
        self.size = size
        self.player1_field = player1_field
        self.player2_field = player2_field
        self.player1_turner = player1_turner
        self.player2_turner = player2_turner



    def multiple_place(self, field: Field):
        field_with_ships = None
        counter = 0
        while not field_with_ships:
            counter += 1
            print(f"попытка разместить корабли №{counter}")
            field.reset_grid()
            field_with_ships = self.place_ships_randomly(field)
        print("Корабли успешно размещены")
        return field_with_ships

    # Это функция расстановки кораблей, она уже полностью написана
    def place_ships_randomly(self, field: Field):
        ship_number = 0
        counter = 0
        for ship_len in range(len(field.ship_types)):

            # print(f"{self.ships[ship_len] = }")

            for _ in range(field.ship_types[ship_len]):
                ship_number += 1
                placed = False
                # print(f"{_ + 1} {ship_len + 1}-палубных кораблей")
                while not placed:
                    # ship_len += 1
                    ship = self.generate_ship(ship_len + 1)
                    counter += 1
                    if counter > 100:
                        return
                    if not self.is_valid_ship_placement(field, ship):
                        continue
                    counter = 0
                    field.ships[str(ship_number)] = ship
                    self.place_buffer_zone(field, ship, constants.BUFFER_ZONE)

                    self.place_ship(field, ship, ship_number)

                    placed = True

        return field

    def generate_ship(self, ship_len: int) -> Ship:
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
        return Ship(x, y, x_indent, y_indent, ship_len)

    def is_valid_ship_placement(self, field: Field, ship: Ship) -> bool:
        if not (
                0 <= ship.x + ship.x_indent * ship.len < self.size and 0 <= ship.y + ship.y_indent * ship.len < self.size):
            return False
        for k in range(ship.len):
            if (field.grid[ship.y + ship.y_indent * k][ship.x + ship.x_indent * k].isdigit() or
                    field.grid[ship.y + ship.y_indent * k][ship.x + ship.x_indent * k] == constants.BUFFER_ZONE):
                return False
        return True

    def place_buffer_zone(self, field: Field, ship: Ship, symbol: str) -> None:

        point1 = (clamp(ship.x - 1 * (ship.x_indent + ship.y_indent), 0, self.size - 1),
                  clamp((ship.y - 1 * (ship.x_indent + ship.y_indent)), 0, self.size - 1))
        point2 = (clamp((ship.x + ship.x_indent * ship.len + abs(ship.y_indent) * (ship.x_indent + ship.y_indent)), 0,
                        self.size - 1),
                  clamp((ship.y + ship.y_indent * ship.len + abs(ship.x_indent) * (ship.x_indent + ship.y_indent)), 0,
                        self.size - 1))

        for x in range(min(point2[0], point1[0]), max(point2[0], point1[0]) + 1):
            for y in range(min(point2[1], point1[1]), max(point2[1], point1[1]) + 1):
                field.grid[y][x] = symbol

    def place_ship(self, field: Field, ship: Ship, symbol: str | int) -> None:
        for k in range(ship.len):
            field.grid[ship.y + ship.y_indent * k][ship.x + ship.x_indent * k] = str(symbol)

    def play(self, ship_vision: bool = False):
        print("\n" * 50)
        self.multiple_place(self.player1_field)
        self.multiple_place(self.player2_field)
        counter = 0
        while True:
            print("\nрасстановка кораблей 1 игрока:")
            self.player1_field.display(ship_vision)
            print("расстановка кораблей 2 игрока:")
            self.player2_field.display(ship_vision)
            print("ход 1 игрока:")

            self.player1_turner.make_turn()
            if not self.player2_field.ships:
                print("Все корабли 2 игрока подбиты, 1 игрок выиграл")
                break
            print("Ход 2 игрока:")
            self.player2_turner.make_turn()
            if not self.player1_field.ships:
                print("Все корабли 1 игрока подбиты, 2 игрок выиграл")
                break

        print("расстановка кораблей 1 игрока:")
        self.player1_field.display(True)
        print("Расстановка кораблей 2 игрока:")
        self.player2_field.display(True)
        return not not self.player2_field.ships