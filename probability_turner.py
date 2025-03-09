from colorama import Fore, Style, init
import constants
from field import Field
from finishing_turner import FinishingTurner
from copy import deepcopy
init()

class ProbabilityTurner(FinishingTurner):
    def __init__(self, enemy_field: Field):
        super().__init__(enemy_field)
        self.probability_grid = []
        for i in range(self.field.size):
            line = []
            for j in range(self.field.size):
                line.append(0)
            self.probability_grid.append(line)
        self.field_map = deepcopy(self.field.grid)

    def make_turn(self):
        # print("\n[MAKE TURN] Начало хода")
        if self.ship_was_destroyed():

            # print("[RESET] Корабль уничтожен, сброс состояний")
            self.reset()
        if self.hunt_mode:
            return self.finishing_ship()
        else:
            self.make_field_map()
            self.null_probability_grid()
            max_ship_len = self.get_max_ship_len()
            # print(f"{max_ship_len = }")
            return self.searching_ship(max_ship_len)

    def searching_ship(self, max_ship_len):
        self.make_probability_grid(max_ship_len)

        y, x = self.find_max_element()

        # self.display_field_map()
        # print(f"выстрел в координаты: {x, y}")

        was_shot, was_hit = self._turn(x, y)
        # self.display_probability_grid()
        # print(f"{was_shot = }")
        # print(f"{was_hit = }")
        if self.ship_was_destroyed():
            self.reset()
            return True
        if was_hit:
            self.hunt_mode = True
            self.last_hit = x, y
            self.first_hit = x, y
            return True
        else:
            return False


    def can_be_placed(self, x: int, y: int, direction: list[int], ship_len: int):
        if not( 0 <=  x + direction[0] * (ship_len - 1) < self.field.size and 0 <=  y + direction[1] * (ship_len - 1) < self.field.size):
            return False
        for k in range(ship_len):
            if not self.field_map[y + direction[1] * k][x + direction[0] * k] == constants.EMPTY:
                return False
        return True

    def add_chances(self, x: int, y: int, direction: list[int], ship_len: int):
        for k in range(ship_len):
            self.probability_grid[y + direction[1] * k][x + direction[0] * k] += 1

    def find_max_element(self):
        max_element = self.probability_grid[0][0]
        row_index = 0
        col_index = 0

        for i in range(len(self.probability_grid)):
            for j in range(len(self.probability_grid[i])):
                if self.probability_grid[i][j] > max_element:
                    max_element = self.probability_grid[i][j]
                    row_index = i
                    col_index = j

        return row_index, col_index

    def make_field_map(self):
        self.field_map = deepcopy(self.field.grid)
        for i in range(self.field.size):
            for j in range(self.field.size):
                if self.field.grid[i][j].isdigit() or self.field.grid[i][j] == constants.BUFFER_ZONE:
                    self.field_map[i][j] = constants.EMPTY

    def calc_probability(self, direction, max_ship_len):
        for x in range(self.field.size):
            for y in range(self.field.size):
                if self.can_be_placed(x, y, direction, max_ship_len):
                    self.add_chances(x, y, direction, max_ship_len)
                    # print(f"{x = }\n{y = }\n{direction = }\n{max_ship_len = }")

    def make_probability_grid(self, max_ship_len):
        direction = [1, 0]
        self.calc_probability(direction, max_ship_len)
        direction = [0, 1]
        self.calc_probability(direction, max_ship_len)

    def get_max_ship_len(self) -> int:
        for i in range(len(self.field.ship_types) - 1, -1, -1):
            if not self.field.ship_types[i] == 0:
                return i + 1
            # print(f"{self.field.ship_types[i] = }\n{i = }")
        return 0


    def display_probability_grid(self):
        indent = len(str(len(self.probability_grid)))
        print(" " * (indent + 1), end="")
        for i in range(len(self.probability_grid)):
            print(Fore.LIGHTBLACK_EX + str(i + 1) + Style.RESET_ALL, end=" " * (indent  + 1 - len(str(i + 1))))
        print()
        for i in range(len(self.probability_grid)):
            print(f"{Fore.LIGHTBLACK_EX}{i + 1}{Style.RESET_ALL}", end="")
            print(" " * (indent + 1 - len(str(i + 1))), end="")
            for j in range(len(self.probability_grid)):
                print(self.probability_grid[i][j], end=" " * indent)
            print()

    def display_field_map(self):
        indent = len(str(len(self.field_map)))
        print(" " * (indent + 1), end="")
        for i in range(len(self.field_map)):
            print(Fore.LIGHTBLACK_EX + str(i + 1) + Style.RESET_ALL, end=" " * (indent  + 1 - len(str(i + 1))))
        print()
        for i in range(len(self.field_map)):
            print(f"{Fore.LIGHTBLACK_EX}{i + 1}{Style.RESET_ALL}", end="")
            print(" " * (indent + 1 - len(str(i + 1))), end="")
            for j in range(len(self.field_map)):
                print(self.field_map[i][j], end=" " * indent)
            print()

    def null_probability_grid(self):
        for i in range(len(self.probability_grid[0])):
            for j in range(len(self.probability_grid[0])):
                self.probability_grid[i][j] = 0
        self.display_probability_grid()
        # print("-----------------------------------")
