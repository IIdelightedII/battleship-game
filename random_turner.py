from field import Field
from turner import Turner
import random

class RandomTurner(Turner):
    def __init__(self, field: Field):
        super().__init__(field)

    def make_turn(self):
        while True:
            x = random.randint(0, self.field.size - 1)
            y = random.randint(0, self.field.size - 1)
            result = self._turn(x, y)
            if result[0]:
                if result[1]:
                    return True
                elif not result[1]:
                    return False