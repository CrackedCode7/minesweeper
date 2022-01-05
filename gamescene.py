import pygame
import math as mt
import time

from text import Text
from line import Line


class GameScene:
    
    def __init__(self, rows:int, cols:int, num_bombs:int, screen_size:tuple):
        
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        self.start_time = int(time.time())
        self.current_time = int(time.time())
        self.elapsed_time = self.current_time - self.start_time
        
        self.num_bombs = num_bombs
        
        # Empty list to iterate over to display objects
        self.objects = []
        
        # Calculate object heights
        self.cell_height = mt.floor(screen_size[1] / (rows+2))
        self.title_height = self.cell_height * 2
        self.cell_width = self.cell_height
        
        # Calcualte total required screen size
        self.total_width = self.cell_width*cols
        self.total_height = self.title_height + self.cell_height*rows
        
        # Set screen size to exactly equal to required size
        self.screen = pygame.display.set_mode((self.total_width, self.total_height))
        
        # Add title text object
        self.title = Text("Test Title", self.cell_height*2)
        self.title.text_rect.center = (self.total_width//2, self.title_height//2)
        self.objects.append(self.title)
        
        # Add time text object
        self.elapsed_time_object = Text(str(self.elapsed_time), self.cell_height)
        self.elapsed_time_object.text_rect.bottomleft = (5, self.title_height-5)
        self.objects.append(self.elapsed_time_object)
        
        # Add number of mines left object
        self.num_bombs_object = Text(str(self.num_bombs), self.cell_height)
        self.num_bombs_object.text_rect.bottomright = (self.total_width-5, self.title_height-5)
        self.objects.append(self.num_bombs_object)
        
        # Generate line to separate title from cells
        line = Line((0, self.title_height), (self.total_width, self.title_height))
        self.objects.append(line)
    
    def render(self):
        
        # Fill screen with white
        self.screen.fill((255, 255, 255))
        
        # Run general render function on all objects
        for item in self.objects:
            item.render(self.screen)
    
    def update(self):
        
        # Update time counter
        self.current_time = int(time.time())
        self.elapsed_time = self.current_time - self.start_time
        self.elapsed_time_object.change_text(str(self.elapsed_time))
        
        # Update number of bombs counter
        self.num_bombs_object.change_text(str(self.num_bombs))
        
        # Run general update function on all objects
        for item in self.objects:
            item.update()
    
    def loop(self):
        
        self.running = True
        while self.running is True:
            
            self.events = []
            self.keys_pressed = pygame.key.get_pressed()
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    
                    self.running = False
                
                else:
                    
                    self.events.append(event)
            
            #self.process_input()
            self.update()
            self.render()
            
            pygame.display.flip()
            self.clock.tick(self.fps)