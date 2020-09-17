import pygame
import os

BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("images","base.png")))

class Base:

    IMAGE = BASE_IMAGE
    VELOCITY = 5

    def __init__(self, pos_y):
        self.pos_y = pos_y
        self.WIDTH = self.IMAGE.get_width()
        self.pos_x_image_1 = 0
        self.pos_x_image_2 = self.WIDTH

    def move(self):
        self.pos_x_image_1 -= self.VELOCITY
        self.pos_x_image_2 -= self.VELOCITY

        if self.pos_x_image_1 + self.WIDTH < 0:
            self.pos_x_image_1 = self.WIDTH

        if self.pos_x_image_2 + self.WIDTH < 0:
            self.pos_x_image_2 = self.WIDTH

    def get_base_image_and_positions(self):
        pos_image_1 = (self.pos_x_image_1, self.pos_y)
        pos_image_2 = (self.pos_x_image_2, self.pos_y)

        return (self.IMAGE, pos_image_1, pos_image_2)