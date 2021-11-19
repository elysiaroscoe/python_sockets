# runs concurrently for each client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        # conn.recv is a blocking line, in a thread 
        # decode the header message into a string using utf-8
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            # convert header info about msg bytes to integer
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            #dont need strip() in python but that removes spaces
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
    conn.close()

# handle new connections
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # server.accept waits for new connections- a "blocking" line of code (in threads so we don't block other clients)
        # stores socket object that allows us to connect, as well as IP address and port
        conn, addr = server.accept()
        # thread connects one client to one server
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # we subtract 1 from the active thread count because our "start" thread is always running
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()