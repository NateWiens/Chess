# Chess game. I might create an AI after if I'm capable.

import pygame

def main():
    pygame.init()
    # Set window size, title of window, and creating surface.
    pygame.display.set_mode((480, 480))
    pygame.display.set_caption('Chess')
    w_surface = pygame.display.get_surface()
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit()    

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object
  
        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.close_clicked = False
        self.continue_game = True
  
        # === game specific objects
        self.board_size = 8
        self.board = dict()
        self.columns = ('a','b','c','d','e','f','g','h')
        self.rows = ('8','7','6','5','4','3','2','1')
        self.create_board()
        self.populate()
        self.need_draw = True
        
        self.tile_clicked = None
    
    def create_board(self):
        # Creates a nested list representing the board of the Game.
        # - self is the Game that the board belongs to
        width = self.surface.get_width() // self.board_size
        height = self.surface.get_height() // self.board_size
        colours = ("beige",'brown')
        # for each row index
        for num in self.rows:
            # create row as an empty list
            # for each column index
            for letter in self.columns:
                # create tile using row index and column index
                col_index = self.columns.index(letter)
                row_index = self.rows.index(num)
                tile = Tile(col_index * width,row_index * height,width,height,
                            letter + num,
                            colours[(col_index + row_index) % 2],self.surface)
                self.board[letter + num] = tile
    
    def populate(self):
        for col in self.columns:
            # Black pawns
            BlackPawn('BlackPawn.png', col + '7', self.board, self.columns)
            
            # White pawns
            WhitePawn('WhitePawn.png', col + '2', self.board, self.columns)
        WhiteRook('WhiteRook.png', 'a1', self.board, self.columns)
        WhiteRook('WhiteRook.png', 'h1', self.board, self.columns)

    def play(self):
        # Play frame.
        while not self.close_clicked:
            self.draw()
            while not self.need_draw and not self.close_clicked:
                self.handle_events()
            # self.decide_continue()
    
    def handle_events(self):
        # Handles events for the frame.
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouseup(event)
    
    def handle_mouseup(self,event):
        if self.tile_clicked == None:
            self.select(event)
        else:
            self.move(event)
            
    def select(self,event):
        for tile in self.board.values():
            if tile.check_clicked(event.pos):
                if tile.check_populated():
                    tile.select()
                    self.tile_clicked = tile
                    self.need_draw = True
    
    def move(self,event):
        for t_not,tile in self.board.items():
            if tile.check_clicked(event.pos):
                piece = self.tile_clicked.get_piece()
                if tile == self.tile_clicked:
                    tile.deselect()
                    self.tile_clicked = None
                elif piece.moveable(t_not):
                    piece.move(t_not)
                    self.tile_clicked = None
        self.need_draw = True
    
    def draw(self):
        # Draw board. Drawing the tiles will reset the board.
        for tile in self.board:
            self.board[tile].draw()
        pygame.display.update()  # make the updated surface appear on the display
        self.need_draw = False

    def decide_continue(self):
        pass
    
class Tile:
    def __init__(self, x, y, width, height, str, colour, surface):
        self.rect = pygame.Rect(x,y,width,height)
        self.str = str
        self.surface = surface
        self.colour = pygame.Color(colour)
        self.n_colour = self.colour
        self.piece = None

    def draw(self):
        pygame.draw.rect(self.surface,self.colour,self.rect)
        if self.piece != None:
            self.surface.blit(self.piece.get_image(),(self.rect[0], self.rect[1]))
    
    def select(self):
        self.colour = pygame.Color('yellow')

    def deselect(self):
        self.colour = self.n_colour

    def add_piece(self, piece):
        self.piece = piece
        
    def remove_piece(self):
        self.piece = None

    def check_clicked(self,pos):
        # Checks if the given point is inside of self.
        # - self is the Tile that we are checking if the point fits into
        clicked = False
        if self.rect.collidepoint(pos):
            clicked = True
        return clicked

    def check_populated(self):
        return isinstance(self.piece, Piece)

    def get_piece(self):
        return self.piece

    def __str__(self):
        return self.str

class Piece:
    def __init__(self, image, t_not, board, columns):
        self.image = pygame.image.load(image)
        self.t_not = t_not
        self.board = board
        self.board[self.t_not].add_piece(self)
        self.columns = columns
    
    def get_image(self):
        return self.image
    
    def move(self, new_tile):
        self.board[self.t_not].remove_piece()
        self.board[self.t_not].deselect()
        self.t_not = new_tile
        self.board[self.t_not].add_piece(self)

class BlackPiece(Piece):
    pass

class BlackPawn (BlackPiece):
    def moveable(self,t_not):
        moveable = False
        if int(t_not[1]) == int(self.t_not[1]) - 1:
            if t_not[0] == self.t_not[0]:
                if self.board[t_not].get_piece() == None:
                    moveable = True
            elif abs(self.columns.index(t_not[0]) - self.columns.index(self.t_not[0])) == 1:
                if isinstance(self.board[t_not].get_piece(), WhitePiece):
                    moveable = True
        elif self.t_not[1] == '7':
            if int(t_not[1]) == int(self.t_not[1]) - 2 and t_not[0] == self.t_not[0]:
                if self.board[t_not].get_piece() == None:
                    moveable = True           
        return moveable

class WhitePiece(Piece):
    pass

class WhitePawn (WhitePiece):
    def moveable(self,t_not):
        moveable = False
        if int(t_not[1]) == int(self.t_not[1]) + 1:
            if t_not[0] == self.t_not[0]:
                if self.board[t_not].get_piece() == None:
                    moveable = True
            elif abs(self.columns.index(t_not[0]) - self.columns.index(self.t_not[0])) == 1:
                if isinstance(self.board[t_not].get_piece(), BlackPiece):
                    moveable = True
        elif self.t_not[1] == '2':
            if int(t_not[1]) == int(self.t_not[1]) + 2 and t_not[0] == self.t_not[0]:
                if self.board[t_not].get_piece() == None:
                    moveable = True            
        return moveable

class WhiteRook (WhitePiece):
    def moveable(self,t_not):
        moveable = False
        if t_not[0] == self.t_not[0]:
            moveable = True
            if int(t_not[1]) > int(self.t_not[1]):
                for i in range(1, int(t_not[1]) - int(self.t_not[1]) + 1):
                    if int(t_not[1]) == int(self.t_not[1]) + i and isinstance(self.board[t_not[0] +str(int(self.t_not[1]) + i)].get_piece(),BlackPiece):
                        pass
                    elif isinstance(self.board[t_not[0] + str(int(self.t_not[1]) + i)].get_piece(),Piece):
                        moveable = False
            else:
                for i in range(1, int(self.t_not[1]) - int(t_not[1]) + 1):
                    if int(t_not[1]) == int(self.t_not[1]) - i and isinstance(self.board[t_not[0] +str(int(self.t_not[1]) - i)].get_piece(),BlackPiece):
                        pass
                    elif isinstance(self.board[t_not[0] + str(int(self.t_not[1]) - i)].get_piece(),Piece):
                        moveable = False
        elif t_not[1] == self.t_not[1]:
            moveable = True
        return moveable

main()