import pygame


class Cell:
    
    def __init__(self, row:int, col:int, has_bomb:bool, cell_size:int):
        
        pygame.init()

        self.row = row
        self.col = col
        self.has_bomb = has_bomb
        self.cell_size = cell_size

        self.rect = pygame.Rect(cell_size*col, cell_size*(row+2), cell_size, cell_size)

        self.is_revealed = False
    
    def render(self, screen):

        pygame.draw.rect(screen, (0, 0, 0), self.rect, width=2)
    
    def update(self):
        pass