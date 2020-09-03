import socket
import time

HEADERSIZE = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

full_msg = ''
new_msg = True
while True:
    try:
        msg = s.recv(16)
        if new_msg:
            msg_len = int(msg[:HEADERSIZE])
            new_msg = False
        full_msg += msg.decode('utf-8')
        if len(full_msg) - HEADERSIZE == msg_len:
            print(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ''

        # s.sendall("client wave".encode())
    except socket.error:
        connected = False
        while not connected:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((socket.gethostname(), 5001))
                connected = True
                print("Re-connected")
            except socket.error:
                print("Disconnected. Trying to re-connect.")
                time.sleep(2)
