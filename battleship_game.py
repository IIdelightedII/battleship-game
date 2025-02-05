from field import Field
import constants
from utility import clamp
from ship import Ship
import random
from turner import Turner

class BattleshipGame:
    def __init__(self, size: int, ship_types: list, player1_field: Field, player2_field: Field, player1_turner: Turner, player2_turner: Turner):
        self.size = size
        self.ship_types = ship_types
        self.player1_field = player1_field
        self.player2_field = player2_field
        self.player1_turner = player1_turner
        self.player2_turner = player2_turner

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
        self.place_ships_randomly(self.player1_field)
        self.place_ships_randomly(self.player2_field)
        while True:
            print("\nВаша расстановка кораблей:")
            self.player1_field.display()
            print("Расстановка кораблей компьютера:")
            self.player2_field.display()
            print("ход игрока:")

            self.player1_turner.make_turn()
            if self.player2_field.ship_count == 0:
                print("Все корабли компьютера подбиты, игрок выиграл")
                break
            print("Ход компьютера")
            self.player2_turner.make_turn()
            if self.player1_field.ship_count == 0:
                print("Все корабли игрока подбиты, компьютер выиграл")
                break
        print("Ваша расстановка кораблей:")
        self.player1_field.display(True)
        print("Расстановка кораблей компьютера:")
        self.player2_field.display(True)




    #
    #
    # def finish_off_ship(self, x: int, y: int, x_indent, y_indent, counter: int):
    #     # print(x_indent, y_indent)
    #     if x_indent == 0 and y_indent == 0:
    #         x_indent, y_indent = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
    #         if self.__turn(self.player1_field, x + x_indent, y + y_indent, "Компьютер")[1]:
    #             if self.player1_field.grid[y][x] == constants.FULLY_DESTROYED_SHIP:
    #                 return True, x_indent, y_indent, counter
    #             counter += 1
    #             return False, x_indent, y_indent, counter
    #         else:
    #             return False, 0, 0, 1
    #     else:
    #         if self.__turn(self.player1_field, x + x_indent * counter, y + x_indent * counter, "Компьютер")[1]:
    #             if self.player1_field.grid[y][x] == constants.FULLY_DESTROYED_SHIP:
    #                 return True
    #             counter += 1
    #             return False, x_indent, y_indent, counter
    #         else:
    #             if y_indent == 0:
    #                 x_indent = -1
    #             elif x_indent == 0:
    #                 y_indent = -1
    #             counter = 1
    #             return False, x_indent, y_indent, counter
    #
    #
    # def manual_shoot(self, x: int, y: int, field):
    #     if not self.__turn(field, x, y, "")[0]:
    #         print(f"Кажется Вы не туда стреляете, координаты: {x + 1}, {y + 1}")
    #         print("-" * 20)
    #         return False
    #     return True

    # def first_shoot(self):
    #     calculating_field = []
    #     for i in range(self.size):
    #         line = []
    #         for j in range(self.size):
    #             line.append("0")
    #         calculating_field.append(line)
    #     for i in range(self.size):
    #         for j in range(self.size):
    #             if not self.player_field.grid[i][j] == constants.EMPTY or not self.player_field.grid[i][j] == constants.BUFFER_ZONE:
    #                 calculating_field[i][j] = "+"
    #
    #     for i in range(self.size):
    #         for j in range(self.size):
    #             if self.is_valid_ship_placement(calculating_field, )
    #
    # def p(self, grid: list[list[int]], ship: Ship, num_of_ships) -> None:
    #     for k in range(ship.len):
    #         grid[ship.y + ship.y_indent * k][ship.x + ship.x_indent * k] += 1 * num_of_ships



