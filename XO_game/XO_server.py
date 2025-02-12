import socket
import random
import copy

# Создаем механизм для игры в крестики-нолики
clear_field = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "],
]
order_def = ['X', '0', 'X', '0', 'X', '0', 'X', '0', 'X', '0']


# Функция отображения игрового поля по формату
# -------
# | | | |
# -------
# | | | |
# -------
# | | | |
# -------
def print_field(field):
    a = "-" * 7 + '\n'
    answer = a
    for x in range(3):
        b = ''
        for y in range(3):
            c = "|" + f'{field[x][y]}'
            b += c
        b += "|\n"
        answer += b + a
    return answer


# Функция для проверки, есть ли какая-то строка, столбец или диагональ заполненная одинаковым символом
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


# Функция для изменения в игровом поле пустых ячеек.
# Если ячейка уже имеет символ - его нельзя перезаписать и вы получите свежее поле для ввода.
def change_elem(field, sym):
    try:
        client_socket.sendall("Chose a line to change (1/2/3): ".encode())
        x = int(client_socket.recv(1024).decode()) - 1
        client_socket.sendall("Chose a column to change (1/2/3): ".encode())
        y = int(client_socket.recv(1024).decode()) - 1
        if x in {0, 1, 2, } and y in {0, 1, 2, }:
            if field[x][y] == " ":
                field[x][y] = sym
            else:
                client_socket.sendall('You need to choose empty slot! Try again\n'.encode())
                change_elem(field, sym)
        else:
            client_socket.sendall(f'x {type(x)} y {type(y)}\n'.encode())
            client_socket.sendall('1You need to enter only numbers 1 or 2 or 3! Try again\n'.encode())
            change_elem(field, sym)
    except ValueError:
        client_socket.sendall('2You need to enter only numbers 1 or 2 or 3! Try again\n'.encode())
        change_elem(field, sym)


# Механизм самой игры, где игра спрашивает, начать ли новую игру или выйти.
# Очередность крстика или нолика, кто первый ходит - реализована рандомно.
# Каждый ход идет проверка на то, выиграли крестики или нолики, если никто не побеждает, через 9 ходов будет ничья.
# Клиент с клавиатуры ввода вводит только y n для старта игры или выхода из игры, и 1 2 3 для выбора ячейки.
# Игра сама выбирает крестик или нолик ставить по очереди.
# При вводе любого другого значения игра выдаст ошибку в текстовом сообщении и предложит сделать предыдущий ход снова.
def start_game():
    while True:
        client_socket.sendall('Do you want to start a new game? (y/n): '.encode())
        game = client_socket.recv(1024).decode()
        field = copy.deepcopy(clear_field)
        if game == 'n':
            client_socket.sendall('Game finished'.encode())
        elif game == 'y':
            client_socket.sendall(print_field(field).encode())
            first_player = random.randint(0, 1)
            order = order_def.copy()
            if first_player:
                client_socket.sendall("First player use X\n".encode())
                order.pop(-1)
            else:
                client_socket.sendall("First player use 0\n".encode())
                order.remove('X')
            for turn in order:
                client_socket.sendall(f"Player {turn} turn\n".encode())
                change_elem(field, turn)
                client_socket.sendall(print_field(field).encode())
                if is_win(field, "X"):
                    client_socket.sendall("Player X won\n".encode())
                    break
                elif is_win(field, "0"):
                    client_socket.sendall("Player 0 won\n".encode())
                    break
            client_socket.sendall("Draw\n".encode()) if is_win(field, "X") == is_win(field, "0") else print('', end='')
        else:
            client_socket.sendall('Wrong input - choose y or n\n'.encode())


# Запуск сервера для одного игрока.
HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f'Server starting at {HOST}:{PORT}')

client_socket, addr = server_socket.accept()
print(f'Client connected: {addr}')

# if len(clients) == 2:
while True:
    data = client_socket.recv(1024).decode()
    if not data or data.lower() == "exit":
        break
    print(f'Client: {data}')
    if data.lower() == 'start':
        start_game()
    print(f'Client: {data}')
    response = input('Server answer: ')
    client_socket.sendall(response.encode())
client_socket.close()
server_socket.close()
