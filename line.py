import pygame


class Line:
    
    def __init__(self, start:tuple, end:tuple, color=(0, 0, 0)):
        
        pygame.init()

        self.start = start
        self.end = end
        self.color = color
    
    def render(self, screen):
        
        pygame.draw.line(screen, self.color, self.start, self.end, width=2)
    
    def update(self):
        pass