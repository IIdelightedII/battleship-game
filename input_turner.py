from field import Field
from turner import Turner

class InputTurner(Turner):
    def __init__(self, field: Field):
        super().__init__(field)

    def make_turn(self):
        while True:
            x, y = self.__player_input()
            result = self._turn(x, y)
            if not result[0]:
                print(f"Кажется Вы не туда стреляете, координаты: {x + 1}, {y + 1}")
                print("-" * 20)
                continue
            if result[1]:
                return True
            elif not result[1]:
                return False


    def __player_input(self) -> tuple:
        while True:
            try:
                x = int(input("x = ")) - 1
                y = int(input("y = ")) - 1

                if 0 <= x < self.field.size and 0 <= y < self.field.size:
                    return x, y
                else:
                    print(f"Число, которое вы вводите должно быть в границах поля, т.е. между 1 и {self.field.size}")

            except ValueError:
                print("Вы должны ввести Числа и при этом они должны быть целым")