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



def starting_position():
    pieces = []
    for i in range(8):
        pieces.append((0,0, (1, i)))
        pieces.append((1,0, (6, i)))

    pieces.extend([ (0, type, (0, i)) for i, type in enumerate([3,2,1,4,5,1,2,3])])
    pieces.extend([ (1, type, (7, i)) for i, type in enumerate([3,2,1,4,5,1,2,3])])
    print(pieces)

    return pieces 



def update_state(move):
    pass

def handle_client(conn : socket.socket, addr):
    state = {
        "player" : 0,
        "pieces" : starting_position(),
        "turn" : 0,
    }

    print(f"[CONNECTED] the addr {addr} connected")
    connected = True


    while connected:
        bytes_header = conn.recv(HEADER_SIZE)
        header = pickle.loads(bytes_header)

        if header["type"] == "get":
            state_bytes = pickle.dumps(state)
            conn.send(int.to_bytes(len(state_bytes), 64, "little"))
            conn.send(pickle.dumps(state))

        elif header["type"] == "set":
            # piece
            assert False, f"set is not implemented"
        elif header["type"] == "end":
            connected = False
            print(f"[ENDING] {addr} closed")
        else:
            assert False, f"{header['type']} is not implemented"
    conn.close()




def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while 1:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print("[STARTING] server is starting...")
start()