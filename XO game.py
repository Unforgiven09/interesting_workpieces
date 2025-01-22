'''Данная версия игры в крестики-нолики создана за короткое время.
Перечень задач, которые я поставил для решения в этой игре:
1. Выводить игровое поле после каждого хода,чтоб не терять ход игры.
2. Выбор случайной очередности, кто ходит первый, Х или 0. (список из 10 ходов, где убираем первый или последний ход,
чтоб кол-во ходов было ровно 9 и в случае ничьей не делала бескоечный цикл ввода)
3. Алгоритм просчета, есть ли победитель после каждого хода (просчет идет прямо с первого хода,
но при необходимости, можно ввести показатель "count_turn" и после 5 хода включать проверку,
так как первые 4 хода точно никто не победит. Но есть ли смысл, так как проверка очень простая
и не ресурсозатратная?)
4. Ввод клетки, которую  менять, реализовал через 2 строчки: введите линию и введите колонку (можно
было сделать через передачу кортежа, но мой вариант простой и лаконичный)
При этом сам символ не выбирает игрок, а игра сама меняет его автоматически до 9 ходов максимум (прописанно в пункте 2)
5. Защита от ввода симовла поверх уже нарисованного символа, чтоб не жульничать (проверка "пустая ли ячейка,
есои нет - рекурсия с вводом новых координат, но не меняя ход и символ ввода)'''

import random
import copy

clear_field = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "],
]
order_def = ['X', '0', 'X', '0', 'X', '0', 'X', '0', 'X', '0']


def print_field(field):
    for x in range(3):
        print("-" * 7)
        for y in range(3):
            print("|", field[x][y], end="", sep="")
        print("|")
    print("-" * 7)


def is_win(field, sym):
    for x in range(3):
        if field[x][0] == field[x][1] == field[x][2] == sym:
            return True
        elif field[0][x] == field[1][x] == field[2][x] == sym:
            return True
    if field[0][0] == field[1][1] == field[2][2] == sym:
        return True
    elif field[2][0] == field[1][1] == field[0][2] == sym:
        return True
    else:
        return False


def change_elem(field, sym):
    x = int(input("Chose a line to change (1/2/3): ")) - 1
    y = int(input("Chose a column to change (1/2/3): ")) - 1
    if field[x][y] == " ":
        field[x][y] = sym
    else:
        print('You need to choose empty slot! Try again')
        change_elem(field, sym)


while True:
    game = input('Do you want to start a new game? (y/n): ')
    field = copy.deepcopy(clear_field)
    if game == 'n':
        break
    elif game == 'y':
        print_field(field)
        first_player = random.randint(0, 1)
        order = order_def.copy()
        if first_player:
            print("First player use X")
            order.pop(-1)
        else:
            print("First player use 0")
            order.remove('X')
        for turn in order:
            print(f"Player {turn} turn")
            change_elem(field, turn)
            print_field(field)
            if is_win(field, "X"):
                print("Player X won")
                break
            elif is_win(field, "0"):
                print("Player 0 won")
                break
        print("Draw") if is_win(field, "X") == is_win(field, "0") else print('', end='')
    else:
        print('Wrong input - choose y or n')