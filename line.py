import pygame


class Line:
    
    def __init__(self, start:tuple, end:tuple, color=(0, 0, 0)):
        
        self.start = start
        self.end = end
        self.color = color
    
    def render(self, screen):
        
        pygame.draw.line(screen, self.color, self.start, self.end)
    
    def update(self):
        pass