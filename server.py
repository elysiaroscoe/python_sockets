import socket
import select

# header size is in bytes, tells us the amount of bytes in the following message
HEADER = 64
PORT = 5050
# SERVER = "192.168.0.3"
SERVER = socket.gethostbyname(socket.gethostname())
#binding tuple
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# socket.socket(FAMILY OF ADDRESSES, TYPE/METHOD)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# allowing the server to reconnect by setting reuseaddr as true (1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# binding this server to this address
server.bind(ADDR)
server.listen()
print(f"[LISTENING] Server is listening on {SERVER}")

# list to contain sockets, right now its only server but we will add clients later
sockets_list = [server]
# clients dictionary where socket is key and data is value
clients = {}


def receive_message(client):
    try:
        message_header = client.recv(HEADER)

        if not len(message_header):
            return False

        message_length = int(message_header.decode(FORMAT).strip())
        return {"header": message_header, "data": client.recv(message_length)}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notifified_socket in read_sockets:
        if notifified_socket == server:
            client, client_address = server.accept()

            user = receive_message(client)
            if user is False:
                continue
            sockets_list.append(client)

            clients[client] = user
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode(FORMAT)}")

        else:
            message = receive_message(notifified_socket)

            if message is False:
                print(f"Closed connection from {clients[notifified_socket]['data'].decode(FORMAT)}")
                sockets_list.remove(notifified_socket)
                del clients[notifified_socket]
                continue

            user = clients[notifified_socket]

            print(f"Received message from {user['data'].decode(FORMAT)}: {message['data'].decode(FORMAT)}")

            for client in clients:
                if client != notifified_socket:
                    client.send(user['header'] + user['data'] + message['data'])
                
    for notified_socket in exception_sockets:
        sockets_list.remove(notifified_socket)
        del clients[notified_socket]