import socket
import errno
# matches error codes
import sys


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

my_username = input("Username: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
client.setblocking(False)

username = my_username.encode(FORMAT)
username_header = f"{len(username):<{HEADER}}".encode(FORMAT)

client.send(username_header + username)

while True:
    message = input(f"{my_username} > ")
    if message:
        message = message.encode(FORMAT)
        message_header = f"{len(message):<{HEADER}}".encode(FORMAT)
        client.send(message_header + message)
        message_length = int(message_header.decode(FORMAT).strip())
        message = client.recv(message_length).decode(FORMAT)


        print(f"{username} > {message}")


    # try:
    # while True:
    #     print(f"here is a print")
    #     # receive things until we hit an error
    #     # username_header = client.recv(HEADER)
    #     # if not len(username_header):
    #     #     print("Connection closed by the server")
    #     #     sys.exit()
    #     # print(type(username_header.decode(FORMAT).strip()))
    #     # username_length = int(username_header.decode(FORMAT).strip())
    #     # username = client.recv(username_header).decode(FORMAT)

    #     message_header = client.recv(HEADER)

    # except IOError as e:
    #     if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
    #         print('Reading error',str(e))
    #         sys.exit()
    #     continue

    # except Exception as e:
    #     print('General error',str(e))
    #     sys.exit()


