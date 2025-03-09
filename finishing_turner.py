import random

import constants
from field import Field
from turner import Turner


class FinishingTurner(Turner):
    def __init__(self, field: Field):
        super().__init__(field)
        self.field = field
        self.hunt_mode = False
        self.first_hit = ()
        self.last_hit = ()
        self.current_direction = ()
        self.possible_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def make_turn(self) -> None:
        # print("\n[MAKE TURN] Начало хода")
        if self.ship_was_destroyed():
            # print("[RESET] Корабль уничтожен, сброс состояний")
            self.reset()

        if self.hunt_mode:
            # print("[HUNT MODE] Охота на корабль")
            self.finishing_ship()
        else:
            # print("[RANDOM TURN] Поиск новой цели")
            self.random_turn()

    def finishing_ship(self):
        # print(f"[FINISHING] Продолжение атаки, направление: {self.current_direction}")
        if self.current_direction:
            self.shoot_by_direction()
        else:
            # print("[FIND DIRECTION] Определяем направление атаки")
            self.find_direction()

    def random_turn(self):
        while True:
            x = random.randint(0, self.field.size - 1)
            y = random.randint(0, self.field.size - 1)
            # print(f"[RANDOM TURN] Попытка выстрела в ({x}, {y})")
            was_shot, was_hit = self._turn(x, y)
            if was_hit:
                # print(f"[HIT] Попадание в ({x}, {y}), переход в режим охоты")
                self.first_hit = x, y
                self.last_hit = x, y
                self.hunt_mode = True
            if was_shot:
                # print(f"[SHOT] Выстрел произведён в ({x}, {y}), завершаем ход")
                return

    def find_direction(self):
        while True:
            if not self.possible_directions:
                # print("[ERROR] Все направления исчерпаны, что-то пошло не так!")
                return

            dx, dy = self.possible_directions.pop()
            x = self.last_hit[0] + dx
            y = self.last_hit[1] + dy
            # print(f"[FIND DIRECTION] Проверка направления ({dx}, {dy}), координаты ({x}, {y})")

            if self.is_inside_field(x, y):
                was_shot, was_hit = self._turn(x, y)
                if was_shot:
                    # print(f"[SHOT] Выстрел в направлении ({dx}, {dy}) в ({x}, {y})")
                    if was_hit:
                        # print(f"[HIT] Попадание в ({x}, {y}), направление выбрано")
                        self.last_hit = x, y
                        self.current_direction = dx, dy
                    break

    def shoot_by_direction(self):
        x = self.last_hit[0] + self.current_direction[0]
        y = self.last_hit[1] + self.current_direction[1]
        # print(f"[SHOOT] Стреляем по направлению {self.current_direction} в ({x}, {y})")

        if self.is_inside_field(x, y) and self.is_valid_turn(x, y):
            was_shot, was_hit = self._turn(x, y)
            if was_hit:
                # print(f"[HIT] Попадание в ({x}, {y})")
                self.last_hit = x, y
        else:
            # print("[INVERT] Достигли границы поля, инвертируем направление")
            self.invert_direction()
            self.shoot_by_direction()  # Рекурсия

    def invert_direction(self):
        # print(f"[INVERT] Меняем направление с {self.current_direction} на {(-self.current_direction[0], -self.current_direction[1])}")
        self.current_direction = -self.current_direction[0], -self.current_direction[1]
        self.last_hit = self.first_hit

    def ship_was_destroyed(self):
        destroyed = self.last_hit and self.field.grid[self.last_hit[1]][self.last_hit[0]] == constants.FULLY_DESTROYED_SHIP
        # if destroyed:
        #     print(f"[CHECK DESTROYED] Корабль в ({self.last_hit}) уничтожен")
        return destroyed

    def reset(self):
        # print("[RESET] Сброс состояний после уничтожения корабля")
        self.hunt_mode = False
        self.first_hit = ()
        self.last_hit = ()
        self.current_direction = ()
        self.possible_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]