import pygame as pg
import socket
import pickle

size = (672,672)
FPS = 60
WHITE = (255,255, 255)
BLACK = (79, 90, 110)



class PieceHandler:
    def __init__(self, pieces_img : pg.Surface, pieces : list) -> None:
        self.img = pieces_img
        self.pieces = pieces
        bsize = self.img.get_size()
        self.psize = min(bsize[0]//6, bsize[1]//2)

    def update(self, state):
        pass

    def draw(self, win : pg.Surface):
        for color, ptype, pos in self.pieces:
            win.blit(self.get_piece(color, ptype), (pos[1]*self.psize, pos[0]*self.psize))
        # test = 

    def get_piece(self, row : int, col : int):
        assert row <= 2 and row >= 0, "The row is not range" 
        assert col <= 6 and col >= 0, "The col is not range"


        return self.img.subsurface(pg.Rect(col*self.psize, row*self.psize, self.psize, self.psize))


current_state = {
    "turn" : 1,
    "position" : ""
}

class Game:
    def __init__(self) -> None:
        pg.font.init()
        pg.init()
        self.win = pg.display.set_mode(size)
        pg.display.set_caption("Chess")
        self.clock = pg.time.Clock()
        self.running = True
    
    def start(self): 
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = (socket.gethostbyname(socket.gethostname()), 5050)
        self.client.connect(ADDR)
        self.get_state()

        temp_header = {
            "size" : 64,
            "type" : "get"
        }
        self.header_size = len(pickle.dumps(temp_header))

        self.board = pg.image.load("assets/pieces.png")
        bsize = self.board.get_size()
        self.board = pg.transform.scale(self.board, (2*bsize[0]//5, 2*bsize[1]//5))
        self.piece = PieceHandler(self.board, self.state["pieces"])
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.end_conn()
                    self.playing = False

    def send_move(self):
        bytes_state = pickle.dumps(self.state)
        self.client.send(pickle.dumps({
            "size" : 64,
            "type" : "set"
        }))


    def get_state(self):
        self.client.send(pickle.dumps({
            "size" : 64,
            "type" : "get"
        }))
        state_size = int.from_bytes(self.client.recv(64), "little")
        state_bytes = self.client.recv(state_size)
        self.state = pickle.loads(state_bytes)

    def end_conn(self):
        self.client.send(pickle.dumps({
            "size" : 64,
            "type" : "end"
        }))

    def update(self):
        # self.send_state()
        pass


    def draw(self):
        self.draw_board()
        self.piece.draw(self.win)
        pg.display.update()

    def draw_board(self):
        p_size = size[0]//8
        self.win.fill(WHITE)
        for row in range(8):
            for col in range(8): 
                if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
                    pg.draw.rect(self.win, BLACK, pg.Rect(row*p_size, col*p_size, p_size, p_size))
        

g = Game()

g.start()