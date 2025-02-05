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
            if self._turn(x, y):
                break