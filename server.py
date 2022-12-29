import socket
import threading
import pickle


PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MSSG = "!DISCONNECT"

temp_header = {
    "size" : 64,
    "type" : "get"
}
HEADER_SIZE = len(pickle.dumps(temp_header))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn : socket.socket, addr):
    print(f"[CONNECTED] the addr {addr} connected")
    connected = True
    state = ["hello world"]

    while connected:
        bytes_header = conn.recv(HEADER_SIZE)
        header = pickle.loads(bytes_header)

        if header["type"] == "get":
            conn.send(pickle.dumps(state))
            # assert False, f"get is not implemented"

        elif header["type"] == "set":
            assert False, f"set is not implemented"




def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while 1:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print("[STARTING] server is starting...")
start()