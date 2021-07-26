# Chess game. I might create an AI after if I'm capable.

import pygame

def main():
    pygame.init()
    # Set window size, title of window, and creating surface.
    pygame.display.set_mode((500, 400))
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
        self.board = []
        self.create_board()
        self.piece = None
        self.piece_selected = False
    
    def create_board(self):
        # Creates a nested list representing the board of the Game.
        # - self is the Game that the board belongs to
        width = self.surface.get_width() // self.board_size
        height = self.surface.get_height() // self.board_size
        colours = ("white",'black')
        # for each row index
        for row_index in range(self.board_size):
            # create row as an empty list
            row = []
            # for each column index
            for col_index in range(self.board_size):
                # create tile using row index and column index
                tile = Tile(col_index * width,row_index * height,width,height,
                            colours[(col_index + row_index) % 2],self.surface)
                # append tile to row
                row.append(tile)
            # append row to board
            self.board.append(row)
    
    def play(self):
        # Play frame.
        temp_clicked = self.piece_selected
        while not self.close_clicked:
            while temp_clicked == self.piece_selected:
                self.handle_events()
            self.draw()    
            #if self.continue_game:
                #self.update()
                #self.decide_continue()
    
    def handle_events(self):
        # Handles events for the frame.
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouseup(event)
    
    def handle_mouseup(self,event):
        if self.continue_game:
            # Selecting the pieces.
            if not self.piece_selected:
                while not self.piece_selected:
                    for piece in pieces:
                        if piece.check_clicked(event.pos):
                            piece_selected = True
                            self.piece = piece
            # Moving the pieces.
            else:
                tile_selected = False
                for row in self.board:
                    for tile in row:
                        if tile.check_clicked(event.pos):
                            piece.move(tile)
    
    def draw(self):
        # Draw board. Drawing the tiles will reset the board.
        for row in self.board:
            for tile in row:
                tile.draw()
        #for piece in self.pieces:
            #piece.draw()
        pygame.display.update()  # make the updated surface appear on the display

    def decide_continue(self):
        pass
    
class Tile:
    def __init__(self, x, y, width, height, colour, surface):
        self.rect = pygame.Rect(x,y,width,height)
        self.surface = surface
        self.colour = pygame.Color(colour)

    def draw(self):
        pygame.draw.rect(self.surface,self.colour,self.rect)

class Piece:
    def __init__(self):
        pass

    def check_clicked(self,pos):
        # Checks if the given point is inside of self.
        # - self is the Tile that we are checking if the point fits into
        clicked = False
        if self.rect.collidepoint(pos):
            clicked = True
        return clicked

main()