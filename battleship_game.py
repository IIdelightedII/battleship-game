import random
from dataclasses import field
from multiprocessing.synchronize import RLock

from field import Field
import constants
from utility import clamp
from ship import Ship
import random


class BattleshipGame:
    def __init__(self, size: int, ship_types: list):
        self.size = size
        self.ship_types = ship_types
        self.player_field = Field(self.size, self.ship_types)
        self.computer_field = Field(self.size, self.ship_types)

    # Это функция расстановки кораблей, она уже полностью написана
    def place_ships_randomly(self, field: Field):
        ship_number = 0
        for ship_len in range(len(self.ship_types)):

            # print(f"{self.ships[ship_len] = }")

            for _ in range(self.ship_types[ship_len]):
                ship_number += 1
                placed = False
                # print(f"{_ + 1} {ship_len + 1}-палубных кораблей")
                while not placed:
                    # ship_len += 1
                    ship = self.generate_ship(ship_len + 1)

                    if not self.is_valid_ship_placement(field, ship):
                        continue
                    field.ships[str(ship_number)] = ship
                    self.place_buffer_zone(field, ship, constants.BUFFER_ZONE)

                    self.place_ship(field, ship, ship_number)

                    placed = True

        return field



    # Это функция проверки расстановки кораблей, она уже полностью написана



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
        if not (0 <= ship.x + ship.x_indent * ship.len < self.size and 0 <= ship.y + ship.y_indent * ship.len < self.size):
            return False
        for k in range(ship.len):
            if (field.grid[ship.y + ship.y_indent * k][ship.x + ship.x_indent * k] == constants.SHIP or
                field.grid[ship.y + ship.y_indent * k][ship.x + ship.x_indent * k] == constants.BUFFER_ZONE):
                return False
        return True

    def place_buffer_zone(self, field:  Field, ship: Ship, symbol: str) -> None:

        point1 = (clamp(ship.x - 1 * (ship.x_indent + ship.y_indent), 0, self.size - 1),
                  clamp((ship.y - 1 * (ship.x_indent + ship.y_indent)), 0, self.size - 1))
        point2 = (clamp((ship.x + ship.x_indent * ship.len + abs(ship.y_indent) * (ship.x_indent + ship.y_indent)), 0, self.size - 1),
                  clamp((ship.y + ship.y_indent * ship.len + abs(ship.x_indent) * (ship.x_indent + ship.y_indent)), 0, self.size - 1))

        for x in range(min(point2[0], point1[0]), max(point2[0], point1[0]) + 1):
            for y in range(min(point2[1], point1[1]), max(point2[1], point1[1]) + 1):
                field.grid[y][x] = symbol



    def place_ship(self, field: Field, ship: Ship, symbol: str | int) -> None:
        for k in range(ship.len):
            field.grid[ship.y + ship.y_indent * k][ship.x + ship.x_indent * k] = str(symbol)


    def play(self):
        self.place_ships_randomly(self.player_field)
        self.place_ships_randomly(self.computer_field)
        while True:
            print("Ваша расстановка кораблей:")
            self.player_field.display()
            print("Расстановка кораблей компьютера:")
            self.computer_field.display()
            print("ход игрока:")
            x, y = self.player_input()
            if not self.player_turn(x, y):
                continue
            if self.computer_field.ship_count == 0:
                print("Все корабли компьютера подбиты, игрок выиграл")
                break
            print("Ход компьютера")
            self.computer_turn()
            if self.player_field.ship_count == 0:
                print("Все корабли игрока подбиты, компьютер выиграл")
                break
        print("Ваша расстановка кораблей:")
        self.player_field.display(True)
        print("Расстановка кораблей компьютера:")
        self.computer_field.display(True)

    def __turn(self, field: Field, x: int, y: int, user):
        if field.grid[y][x].isdigit():
            ship_number = field.grid[y][x]
            ship = field.ships[ship_number]
            ship.hp -= 1
            field.grid[y][x] = constants.DESTROYED_SHIP
            print(f"{user} попал!, координаты: {x + 1}, {y + 1}")
            print("-" * 20)
            if ship.hp == 0:
                field.ship_count -= 1
                self.place_buffer_zone(field, ship, constants.EXTRA_BUFFER_ZONE)

                self.place_ship(field, ship, constants.FULLY_DESTROYED_SHIP)
            return True, True # return [был ли выстрел], [попал ли в корабль], [координата x], [координата y]
        elif field.grid[y][x] == constants.EMPTY or field.grid[y][x] == constants.BUFFER_ZONE:
            field.grid[y][x] = constants.MISS
            print(f"{user} промахнулся, координаты: {x + 1}, {y + 1}")
            print("-" * 20)
            return True, False # return [был ли выстрел], [попал ли в корабль]
        else:
            return False, False

    def player_turn(self, x: int, y: int):
        if not self.__turn(self.computer_field, x, y, "игрок")[0]:
            print(f"Кажется Вы не туда стреляете, координаты: {x + 1}, {y + 1}")
            print("-" * 20)
            return False
        return True


    def computer_turn(self):
        while True:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.__turn(self.player_field, x, y, "Компьютер")[0]:
                break




    def player_input(self) -> tuple:
        while True:
            try:
                x = int(input("x = ")) - 1
                y = int(input("y = ")) - 1

                if 0 <= x < self.size and 0 <= y < self.size:
                    return x, y
                else:
                     print(f"Число, которое вы вводите должно быть в границах поля, т.е. между 1 и {self.size}")

            except ValueError:
                print("Вы должны ввести Числа и при этом они должны быть целым")


