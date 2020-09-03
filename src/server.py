import socket
import time
import sys
import threading
from queue import Queue

HEADERSIZE = 10
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []


def open_socket():
    global s

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 5001))
        s.listen(5)
    except:
        print("Unable to open socket.")


# called when started
# handle connection from multiple clients and save to a list
def accept_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, addr = s.accept()
            s.setblocking(True)  # prevents time outs
            all_connections.append(conn)
            all_address.append(addr)

            print(f'Connection has been established: {addr[0]}')
        except:
            print('Error accepting connections')


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# do next job that is in the queue
def work():
    while True:
        x = queue.get()
        if x == 1:
            open_socket()
            accept_connections()
        if x == 2:
            ping()
        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


def send_msg(client_socket, msg):
    try:
        msg = f'{len(msg):<{HEADERSIZE}}' + msg
        client_socket.send(bytes(msg, 'utf-8'))
    except socket.error:
        print(f'Unable to send message: {msg}')


def ping():
    while True:
        time.sleep(1)
        for i in range(len(all_connections)):
            send_msg(all_connections[i], f'hi {all_address[i]}')


def main():
    create_workers()
    create_jobs()


if __name__ == '__main__':
    main()

#
# while True:
#     client_socket, address = s.accept()
#     print(f'Connection from {address} has been established')
#
#     while True:
#         time.sleep(1)
#         try:
#             send_msg(client_socket, "test")
#         except socket.error:
#             print(f'{address} disconnected')
#             break
#
#     # msg = client_socket.recv(1024).decode('utf-8')
#     # print(msg)
