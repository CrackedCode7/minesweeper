import pygame


class Text:
    
    def __init__(self, text:str, font_size:int):
    
        pygame.init()
        
        self.font = pygame.font.Font(None, font_size)
        self.text = text
        self.rendered_text = self.font.render(self.text, True, (0, 0, 0))
        
        # This should be adjusted for each text object upon creation
        self.text_rect = self.rendered_text.get_rect()
        
        self.background = False # Default
        
    def render(self, screen):
    
        if self.background is True:
            pygame.draw.rect(screen, (255, 255, 255), self.text_rect)
        
        screen.blit(self.rendered_text, self.text_rect)
    
    def update(self):
        pass
    
    def change_text(self, text:str):
        
        self.text = text
        self.rendered_text = self.font.render(self.text, True, (0, 0, 0))   