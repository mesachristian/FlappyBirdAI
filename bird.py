import pygame
import os

BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("images","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("images","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("images","bird3.png")))]

class Bird:
    IMAGES = BIRD_IMAGES
    ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.image_time_counter = 0
        self.current_image = self.IMAGES[0]

    def jump(self):
        self.tick_count = 0
        self.velocity = -30.5
        self.height = self.y

    def move(self):
        self.tick_count += 1 # One unit of time passsed

        dy = ( self.velocity*self.tick_count ) + ( 1.5 * self.tick_count**2 ) 

        if dy >= 16:
            dy = 16

        if dy < 0:
            dy = -2

        self.y += dy

        if dy < 0 or self.y < self.height + 50: # Bird moving up
            if self.tilt < self.ROTATION:
                self.tilt = self.ROTATION

        else: # Bird moving down
            if self.tilt > -90 : 
                self.tilt -= self.ROTATION_VELOCITY

    def get_bird_image(self):

        # Select the bird image to draw 
        self.image_time_counter += 1

        if self.image_time_counter < self.ANIMATION_TIME:
            self.current_image = self.IMAGES[0]

        elif self.image_time_counter < self.ANIMATION_TIME * 2:
            self.current_image = self.IMAGES[1]

        elif self.image_time_counter < self.ANIMATION_TIME * 3:
            self.current_image = self.IMAGES[2]

        elif self.image_time_counter < self.ANIMATION_TIME * 4:
            self.current_image = self.IMAGES[1]

        elif self.image_time_counter < self.ANIMATION_TIME * 4 + 1:
            self.current_image = self.IMAGES[0]
            self.image_time_counter = 0

        if self.tilt <= -80:
            self.current_image = self.IMAGES[1]
            self.image_time_counter = self.ANIMATION_TIME*2

        # Rotate the bird image based on its current tilt
        rotated_image = pygame.transform.rotate(self.current_image, self.tilt)
        new_rect = rotated_image.get_rect(center = self.current_image.get_rect(topleft=(self.x,self.y)).center)
        
        return (rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.current_image)
