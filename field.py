import constants
import string

# В классе должен быть метод __init__, который принимает аргументы size — размер поля (целое число) и ships — количество
# кораблей на поле (целое число). Внутри метода должны создаваться атрибуты size и ships. Также должен создаваться
# атрибут grid — список списков, представляющий сетку поля, и атрибут ships_alive, который будет хранить количество
# целых кораблей на поле.
# Корабли могут быть только одинарными.
class Field:
    def __init__(self, size: int, ship_types: list): # значения ships раньше были в int
        self.size = size
        self.ship_types = ship_types
        self.ship_count = sum(ship_types)
        self.ships = {}
        self.grid = []
        for i in range(size):
            line = []
            for j in range(size):
                line.append(constants.EMPTY)
            self.grid.append(line)


    def display(self, show_ships: bool = False, show_numbers: bool = False) -> None:
        indent = len(str(self.size))
        print(" " * (indent + 1), end="")
        for i in range(self.size):
            print(i + 1, end=" " * (indent  + 1 - len(str(i + 1))))
        print()
        for i in range(self.size):
            print(f"{i + 1}", end="")
            print(" " * (indent + 1 - len(str(i + 1))), end="")
            for j in range(self.size):
                if self.grid[i][j].isdigit() and show_numbers and show_ships:
                    print(f"{self.grid[i][j]}", end=" " * indent)
                elif self.grid[i][j] == constants.SHIP  or self.grid[i][j].isdigit() and show_ships == True :
                    print(constants.SHIP, end=" " * indent)
                elif self.grid[i][j] == constants.SHIP  or self.grid[i][j].isdigit() and show_ships == False:
                    print(constants.EMPTY, end=" " * indent)
                else:
                    print(f"{self.grid[i][j]}", end=" " * indent)
            print()

    def __str__(self):
        # return "\n".join(f"{number}: {ship}" for number, ship in self.ships.items())
        line = []

        for number, ship in self.ships.items():
            line.append(f"{number}: {ship}")
        return "\n".join(line)
