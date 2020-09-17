import pygame
import random
import os

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images","pipe.png")))

class Pipe():
    VELOCITY = 5
    GAP = 150

    def __init__(self,x):
        self.x = x
        self.passed = False
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE
        
        self.height = random.randrange(25,410)
        self.top_pipe_position = self.height - self.PIPE_TOP.get_height()
        self.bottom_pipe_position = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def get_pipe_images(self):
        top_pipe = (self.PIPE_TOP, (self.x,self.top_pipe_position))
        bottom_pipe = (self.PIPE_BOTTOM, (self.x,self.bottom_pipe_position)) 
        return ( top_pipe , bottom_pipe )

    def get_top_pipe_mask(self):
        return pygame.mask.from_surface(self.PIPE_TOP)

    def get_bottom_pipe_mask(self):
        return pygame.mask.from_surface(self.PIPE_BOTTOM)