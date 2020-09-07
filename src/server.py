import socket
import time
import threading
from queue import Queue
import select

HEADER_SIZE = 10
NUMBER_OF_THREADS = 3
JOB_NUMBER = [1, 2, 3]
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

            print(f'Connection has been established: {addr}')
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
        # 1st thread: accept new connections
        if x == 1:
            open_socket()
            accept_connections()
        # 2nd thread: ping and keep track of connections
        if x == 2:
            ping()
        # 3rd thread: listen for log messages
        if x == 3:
            listen()
        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


def send_msg(client_socket, msg):
    msg = f'{len(msg):<{HEADER_SIZE}}' + msg
    client_socket.send(bytes(msg, 'utf-8'))


def ping():
    while True:
        time.sleep(1)
        for i in range(len(all_connections)):
            try:
                send_msg(all_connections[i], f'server wave to {all_address[i]}')
            except socket.error:
                print(f'Lost connection with: {all_address[i]}')
                all_connections.pop(i)
                all_address.pop(i)
                break


def listen():
    while True:
        for conn in all_connections:
            ready = select.select([conn], [], [], 1)
            msg_len = -1
            new_msg = True
            full_msg = ''
            while ready[0]:
                try:
                    msg = conn.recv(16)
                    if new_msg:
                        try:
                            msg_len = int(msg[:HEADER_SIZE])
                        except ValueError:
                            break
                        new_msg = False
                    full_msg += msg.decode('utf-8')
                    if len(full_msg) - HEADER_SIZE >= msg_len:
                        print(full_msg[HEADER_SIZE:])
                        break
                except socket.error:
                    # should be handled by ping thread
                    break


def main():
    create_workers()
    create_jobs()


if __name__ == '__main__':
    main()
