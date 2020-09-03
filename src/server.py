import socket
import time

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 5001))

s.listen(5)


def send_msg(client_socket, msg):
    msg = f'{len(msg):<{HEADERSIZE}}' + msg
    client_socket.send(bytes(msg, 'utf-8'))


while True:
    client_socket, address = s.accept()
    print(f'Connection from {address} has been established')

    while True:
        time.sleep(1)
        try:
            send_msg(client_socket, "test")
        except socket.error:
            print(f'{address} disconnected')
            break

    # msg = client_socket.recv(1024).decode('utf-8')
    # print(msg)
