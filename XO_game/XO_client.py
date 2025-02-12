import socket
import time

# Данный клиент создан для подключения к серверу с игрой крести-нолики и интерфейс заточен под него.
HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print('Connecting to server.\nEnter "start" to start the game.\nEnter "exit" for quit.\nPress Enter to update!')

while True:
    message = input()
    client_socket.sendall(message.encode())
    if message.lower() == 'exit':
        break
    time.sleep(0.3)
    # Данный time.sleep нужен для того, чтоб клиент терминал корректно отображал ответы от сервера, так некоторые
    # вычисления могут занять немного времени. Если ваш ПК не успевает - увеличьте time.sleep(1), задержка между ходами
    # будет искусственно увеличена.
    response = client_socket.recv(1024).decode()
    print(response)

client_socket.close()
