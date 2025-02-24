import constants
from field import Field
from finishing_turner import FinishingTurner
class ProbabilityTurner(FinishingTurner):
    def __init__(self, enemy_field: Field):
        super().__init__(enemy_field)
        self.probability_grid = []
        for i in range(self.field.size):
            line = []
            for j in range(self.field.size):
                line.append(0)
            self.probability_grid.append(line)
        self.field_map = Field(enemy_field.size, enemy_field.ship_types)
        self.alive_ships = enemy_field.ship_types.copy()

    def make_turn(self):
        if self.hunt_mode:
            return self.finishing_ship()
        else:
            return self.searching_ship(len(self.alive_ships))

    def searching_ship(self, max_ship_len):
        direction = [1, 0]
        for x in range(self.field.size):
            for y in range(self.field.size):
                if self.can_be_placed(x, y, direction, max_ship_len):
                    self.add_chances(x, y, direction, max_ship_len)
        direction = [0, 1]
        for x in range(self.field.size):
            for y in range(self.field.size):
                if self.can_be_placed(x, y, direction, max_ship_len):
                    self.add_chances(x, y, direction, max_ship_len)

        y, x = self.find_max_element()
        result = self._turn(x, y)
        if result[1]:
            self.hunt_mode = True
            self.last_hit = x, y
            self.first_hit = x, y


    def can_be_placed(self, x: int, y: int, direction: list[int], ship_len: int):
        if not( 0 <=  x + direction[0] * (ship_len - 1) < self.field.size and 0 <=  y + direction[1] * (ship_len - 1) < self.field.size):
            return False
        for k in range(ship_len):
            if not self.field_map.grid[y + direction[1] * k][x + direction[0] * k] == constants.EMPTY:
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