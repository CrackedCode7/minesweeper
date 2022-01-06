import pygame
import math as mt
import time
import random

from text import Text
from line import Line
from cell import Cell


class GameScene:
    
    def __init__(self, cols:int, rows:int, num_bombs:int, screen_size:tuple):
        
        pygame.init()
        
        self.cols = cols
        self.rows = rows
        self.num_bombs = num_bombs
        self.screen_size = screen_size
        
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        self.start_time = int(time.time())
        self.current_time = int(time.time())
        self.elapsed_time = self.current_time - self.start_time

        # First click is true if we need to still generate bombs, otherwise false
        self.first_click = True
        
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
        self.title = Text("Minesweeper", self.cell_height*2)
        self.title.text_rect.center = (self.total_width//2, self.title_height//2)
        self.objects.append(self.title)
        
        # Add time text object
        self.elapsed_time_object = Text(str(self.elapsed_time), self.cell_height)
        self.elapsed_time_object.text_rect.bottomright = (self.total_width-5, self.title_height-5)
        self.objects.append(self.elapsed_time_object)
        
        # Add number of mines left object
        self.num_bombs_object = Text(str(self.num_bombs), self.cell_height)
        self.num_bombs_object.text_rect.bottomleft = (5, self.title_height-5)
        self.objects.append(self.num_bombs_object)
        
        # Generate line to separate title from cells
        line = Line((0, self.title_height), (self.total_width, self.title_height))
        self.objects.append(line)

        # Generate cells. All empty to start, bombs generated after first click
        self.cells = {}
        for i in range(cols):
            for j in range(rows):
                self.cells[(i, j)] = Cell(i, j, False, self.cell_height)
                self.objects.append(self.cells[(i, j)])
    
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
        
        # Wait for first click to generate board
        self.running = True
        while (self.first_click is True) and (self.running is True):
            
            self.events = []
            self.keys_pressed = pygame.key.get_pressed()
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # Determine start cell indices based on mouse position
                        pos = pygame.mouse.get_pos()
                        col_index = mt.floor(pos[0]/self.cell_height)
                        row_index = mt.floor(pos[1]/self.cell_height)-2
                        if (col_index >=0) and (row_index>=0):
                            self.first_click = False
                            self.start_cell = (col_index, row_index)
                            self.place_mines()
                
                else:
                    self.events.append(event)
            
            #self.process_input()
            self.update()
            self.render()
            
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        while self.running is True:
            
            self.events = []
            self.keys_pressed = pygame.key.get_pressed()
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    
                    self.running = False
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    pos = pygame.mouse.get_pos()
                    col_index = mt.floor(pos[0]/self.cell_height)
                    row_index = mt.floor(pos[1]/self.cell_height)-2
                    cell_index = (col_index, row_index)
                    
                    if event.button == 1:                        
                        
                        if cell_index in self.cells:
                        
                            if self.cells[cell_index].has_bomb and self.cells[cell_index].flagged is False:

                                self.cells[cell_index].is_revealed = True
                                
                                lose_str = "GAME OVER"
                                lose_text = Text(lose_str, self.cell_height)
                                lose_text.text_rect.center = (self.total_width//2, self.total_height//2)
                                lose_text.background = True
                                
                                self.objects.append(lose_text)
                            
                            elif self.cells[cell_index].is_revealed is False and self.cells[cell_index].flagged is False:
                                self.cells[cell_index].is_revealed = True
                                self.reveal()
                            
                            elif self.cells[cell_index].is_revealed is True:
                                self.cells[cell_index].clicked_again = True
                                self.reveal()
                    
                    elif event.button == 3:
                        
                        # Flag
                        if cell_index in self.cells:
                            
                            if self.cells[cell_index].flagged is False:
                                
                                self.cells[cell_index].flagged = True
                                self.num_bombs -= 1
                            
                            else:
                                
                                self.cells[cell_index].flagged = False
                                self.num_bombs += 1
                else:
                    
                    self.events.append(event)
            
            #self.process_input()
            self.update()
            self.render()
            
            pygame.display.flip()
            self.clock.tick(self.fps)
    
    def place_mines(self):
        
        # List of all cell tuples
        choices = [(i, j) for i in range(self.cols) for j in range(self.rows)]
        
        # Remove first selected cell and surrounding cells to make first
        # cell selected a "0"
        for i in range(-1, 2):
            for j in range(-1, 2):
                index = (self.start_cell[0]+i, self.start_cell[1]+j)
                choices.remove(index)
                self.cells[index].is_revealed = True
        
        # Place bombs in available cells
        for _ in range(self.num_bombs):
            
            choice = random.choice(choices)
            choices.remove(choice)
            self.cells[choice].has_bomb = True
        
        # Update adjacent bombs number for cells without bomb
        for cell in self.cells:
            
            if self.cells[cell].has_bomb is False:
                
                # Count number of adjacent cells with bomb
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        index = (self.cells[cell].col+i,
                                 self.cells[cell].row+j)
                        if index in self.cells:
                            if self.cells[index].has_bomb:
                                self.cells[cell].adjacent_bombs += 1
                
                # Generate text object to be displayed when cell revealed
                self.cells[cell].generate_text()
        
        # Reveal after first click
        self.reveal()
    
    def reveal(self):
        
        # Iterate over cells, revealing what is needed if a 0 is 
        # revealed (show nums, keep bombs covered all around it.
        # Recurse if another zero is revealed
        recurse = True
        while recurse:
        
            recurse = False
            for cell in self.cells:
                
                if self.cells[cell].adjacent_bombs == 0 and self.cells[cell].is_revealed is True:
                    
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            index = (self.cells[cell].col+i, self.cells[cell].row+j)
                            if index in self.cells:
                                if self.cells[index].is_revealed is False and self.cells[index].has_bomb is False:
                                    self.cells[index].is_revealed = True
                                    recurse = True
                
                elif self.cells[cell].clicked_again is True:
                    
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            index = (self.cells[cell].col+i, self.cells[cell].row+j)
                            if index in self.cells:
                                if self.cells[index].is_revealed is False and self.cells[index].has_bomb is False:
                                    self.cells[index].is_revealed = True
                                    recurse = True
                                elif self.cells[index].flagged is False and self.cells[index].has_bomb is True:
                                    
                                    self.cells[index].is_revealed = True
                                    recurse = False
                                    
                                    lose_str = "GAME OVER"
                                    lose_text = Text(lose_str, self.cell_height)
                                    lose_text.text_rect.center = (self.total_width//2, self.total_height//2)
                                    lose_text.background = True
                                    
                                    self.objects.append(lose_text)
        
        # Check if game has been won
        game_won = True
        for cell in self.cells:
            
            if self.cells[cell].has_bomb is False and self.cells[cell].is_revealed is False:
                
                game_won = False
                break
        
        if game_won:
        
            # Display time it took to win, and win message
            win_time = self.elapsed_time
            win_str = f"You won in {win_time} seconds."
            win_text = Text(win_str, self.cell_height)
            win_text.text_rect.center = (self.total_width//2, self.total_height//2)
            win_text.background = True
            
            self.objects.append(win_text)
