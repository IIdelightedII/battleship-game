from dataclasses import field

import constants
from field import Field
from turner import Turner
import random

class FinishingTurner(Turner):
    def __init__(self, field: Field):
        super().__init__(field)
        self.field = field
        self.hunt_mode = False
        self.current_direction = []  # Список для направления (x, y)
        self.last_hit = []  # Список для последней координаты (x, y)
        self.first_hit = []  # Список для первой координаты (x, y)
        self.possible_directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]  # Списки

    def make_turn(self):
        if self.hunt_mode:
            return self.finishing_ship()
        else:
            result, x, y = self.random_turn()
            if result[1]:
                if not self.field.grid[y][x] == constants.FULLY_DESTROYED_SHIP:
                    self.first_hit = [x, y]  # Теперь список
                    self.last_hit = [x, y]  # Теперь список
                    self.possible_directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
                    self.hunt_mode = True
                    return True
                else:
                    self.reset_if_destroyed(x, y)
                    return True
            return False

    def random_turn(self):
        while True:
            x = random.randint(0, self.field.size - 1)
            y = random.randint(0, self.field.size - 1)
            result = self._turn(x, y)
            if result[0]:
                return result, x, y

    def finishing_ship(self):
        if self.current_direction:

            x = self.last_hit[0] + self.current_direction[0]
            y = self.last_hit[1] + self.current_direction[1]
            if not self.is_possible_shoot(x, y):
                x, y = self.invert_direction()

            result = self._turn(x, y)
            print(f"{result = }")
            print()
            if not result[0]:
                x, y = self.invert_direction()
                result = self._turn(x, y)

            if result[1]:
                self.last_hit = [x, y]
                self.reset_if_destroyed(x, y)
                return True
            else:
                # Инвертируем направление
                self.invert_direction()
                return False

        else:

            direction = self.possible_directions[-1]
            del self.possible_directions[-1]
            x = self.last_hit[0] + direction[0]
            y = self.last_hit[1] + direction[1]
            while not self.is_possible_shoot(x, y):
                print(f"{self.possible_directions = } *")
                direction = self.possible_directions[-1]
                del self.possible_directions[-1]
                x = self.last_hit[0] + direction[0]
                y = self.last_hit[1] + direction[1]

            result = self._turn(x, y) # result[0]

            if not result[0]:
                print(f"{x, y = }")
                self.find_direction()

            print(f"{result = }")
            if result[1]:
                self.current_direction = direction
                self.last_hit = [x, y]

                self.reset_if_destroyed(x, y)

                return True
            else:
                return False

    def reset_if_destroyed(self, x, y):
        if self.field.grid[y][x] == constants.FULLY_DESTROYED_SHIP:
            self.hunt_mode = False
            self.current_direction = []
            self.possible_directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]

    def generate_possible_directions(self, x, y):
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.possible_directions = []
        for i in range(len(directions)):
            if 0 <= x < self.field.size and 0 <= y < self.field.size:

                self.possible_directions.append(directions[i])

    def is_possible_shoot(self, x, y) -> bool:
        return 0 <= x < self.field.size and 0 <= y < self.field.size

    def invert_direction(self):
        self.current_direction[0] *= -1
        self.current_direction[1] *= -1
        self.last_hit = self.first_hit
        x = self.last_hit[0] + self.current_direction[0]
        y = self.last_hit[1] + self.current_direction[1]
        return x, y

    def find_direction(self):
        while True:
            print(f"{self.possible_directions = } +")
            direction = self.possible_directions[-1]
            del self.possible_directions[-1]
            x = self.last_hit[0] + direction[0]
            y = self.last_hit[1] + direction[1]
            if not self.is_possible_shoot(x, y):
                continue
            result = self._turn(x, y)
            if result[0]:
                return

