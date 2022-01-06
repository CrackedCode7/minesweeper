import pygame
from text import Text


class Cell:
    
    def __init__(self, col:int, row:int, has_bomb:bool, cell_size:int):
        
        pygame.init()

        self.col = col
        self.row = row
        self.has_bomb = has_bomb
        self.cell_size = cell_size

        self.rect = pygame.Rect(cell_size*col, cell_size*(row+2), cell_size, cell_size)

        self.is_revealed = False
        self.flagged = False
        self.clicked_again = False
        
        self.adjacent_bombs = 0
    
    def render(self, screen):

        if self.flagged is True:
            pygame.draw.rect(screen, (255, 255, 0), self.rect)
            
        else:
        
            if self.is_revealed is True:
            
                if self.has_bomb:
                    pygame.draw.rect(screen, (255, 0, 0), self.rect)
                else:
                    self.text.render(screen)
            
            else:
                pygame.draw.rect(screen, (151, 218, 218), self.rect)
        
        pygame.draw.rect(screen, (0, 0, 0), self.rect, width=2)
    
    def update(self):
        pass
    
    def generate_text(self):
        
        if self.adjacent_bombs != 0:
            self.text = Text(str(self.adjacent_bombs), self.cell_size)
        else:
            self.text = Text("", self.cell_size)
        
        self.text.text_rect.center = self.rect.center