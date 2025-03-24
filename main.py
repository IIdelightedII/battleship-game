from dataclasses import field
from random import random, Random

from battleship_game import BattleshipGame
from field import Field
import constants
from input_turner import InputTurner
from random_turner import RandomTurner
from ship import Ship
import random
from finishing_turner import FinishingTurner
from probability_turner import ProbabilityTurner
from turner import Turner

def choose_difficulty(enemy_field: Field):
    while True:
        try:
            level = int(input("Выберите уровень интеллекта бота:\n1 - низкий\n2 - средний\n3 - высокий\nуровень интеллекта: "))
            if 1 <= level <= 3:
                break
            print("Число должно быть между 1 и 3")
        except ValueError:
            print("вы должны ввести целое число")
    if level == 1:
        turner = RandomTurner(enemy_field)
    elif level == 2:
        turner = FinishingTurner(enemy_field)
    else:
        turner = ProbabilityTurner(enemy_field)
    return turner

def choose_game_type(field1: Field, field2: Field):
    while True:
        try:
            choice = int(input("Выберите режим:\n1 - игрок против игрока\n2 - игрок против бота\n3 - бот против бота\nрежим: "))
            if 1 <= choice <= 3:
                break
            print("Число должно быть между 1 и 3")
        except ValueError:
            print("вы должны ввести целое число")
    if choice == 1:
        turner1 = InputTurner(field2)
        turner2 = InputTurner(field1)
    elif choice == 2:
        turner1 = InputTurner(field2)
        turner2 = choose_difficulty(field1)
    else:
        turner1 = choose_difficulty(field2)
        turner2 = choose_difficulty(field1)
    return turner1, turner2

def choose_size():
    while True:
        try:
            size = int(input("Какой будет размер у поля: "))
            if size > 1:
                break
            print("Число должно быть больше 1")
        except ValueError:
            print("вы должны ввести целое число")
    return size

def choose_max_ship_len():
    while True:
        try:
            max_ship_len = int(input("Какой будет максимальный размер корабля: "))
            if max_ship_len > 0:
                break
            print("число должно быть больше 0")
        except ValueError:
            print("вы должны ввести целое число")
    return max_ship_len

def choose_ship_types(max_ship_len, field_size):
    ship_types = []
    min_field_area = field_size ** 2
    max_field_area = field_size ** 2
    ship_len = 1
    min_ship_area = ship_len * 2 + 2
    max_ship_area = ship_len * 3 + 6
    for i in range(0, max_ship_len):
        min_possible_ships = min_field_area // max_ship_area
        max_possible_ships = max_field_area // min_ship_area
        if min_possible_ships < 0:
            min_possible_ships = 0
        if max_possible_ships < 0:
            print("Похоже, невозможно поставить больше кораблей")
            break
        while True:
            try:
                amount = int(input(f"сколько будет {i + 1}-палубных кораблей?\nрекомендуется от {min_possible_ships} до {max_possible_ships}.(может быть даже 0 кораблей): "))
                if amount < 0:
                    print("вы должны ввести положительное число")
                    continue
            except ValueError:
                print("вы должны ввести целое число")
                continue
            ship_types.append(amount)
            ships_amount = ship_types[i]
            ship_len = i + 2
            min_ship_area = ship_len * 2 + 2
            max_ship_area = ship_len * 3 + 6
            min_field_area -= ships_amount * max_ship_area
            max_field_area -= ships_amount * min_ship_area
            break



    return ship_types


def main():
    while True:
        size = choose_size()
        max_ship_len = choose_max_ship_len()

        ship_types = choose_ship_types(max_ship_len, size)
        print(f"{ship_types = }")
        field1 = Field(size, ship_types.copy())
        field2 = Field(size, ship_types.copy())
        turner1, turner2 = choose_game_type(field1, field2)

        game = BattleshipGame(size, field1, field2, turner1, turner2)
        print(ship_types.copy())
        try:
            game.multiple_place(field1)
            game.multiple_place(field2)
        except ValueError:
            print("Невозможно расставить корабли, попробуйте увеличить поле, либо уменьшить количество кораблей")
            continue
        print("Корабли успешно размещены")
        game.play()
        break

if __name__ == '__main__':
    # main()




