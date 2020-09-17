import pygame
import neat
import time
import os
import random

from bird import Bird
from pipe import Pipe
from base import Base

WINDOW_HEIGHT = 700
WINDOW_WIDTH = 500

BACKGROUND_IMAGE = pygame.image.load(os.path.join("images","bg.png"))
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.font.init()
SCORE_FONT = pygame.font.SysFont("comicsans",50)

def update_window(window, bird, pipes, base, score):
    # Paint background
    window.blit(BACKGROUND_IMAGE, (0,0))

    # Paint Bird
    bird_image, bird_image_position = bird.get_bird_image()
    window.blit(bird_image,bird_image_position)

    # Paint pipes
    for pipe in pipes:
        (pipe_top_image, pipe_top_position) , (pipe_bottom_image, pipe_bottom_position) = pipe.get_pipe_images() 
        window.blit(pipe_top_image,pipe_top_position)
        window.blit(pipe_bottom_image, pipe_bottom_position)
    
    # Paint Base
    (base_image, pos_image_1, pos_image_2 ) = base.get_base_image_and_positions()
    window.blit(base_image, pos_image_1)
    window.blit(base_image, pos_image_2)

    # Paint score
    score_label = SCORE_FONT.render("Score: " + str(score),1,(255,255,255))
    window.blit(score_label, (WINDOW_WIDTH - score_label.get_width() - 15, 10))

    pygame.display.update()

def check_collision(bird, pipe):
    bird_mask = bird.get_mask()
    top_pipe_mask = pipe.get_top_pipe_mask()
    bottom_pipe_mask = pipe.get_bottom_pipe_mask()
    
    top_offset = ( int(pipe.x - bird.x) , int(pipe.top_pipe_position - round(bird.y)) )
    bottom_offset = ( int(pipe.x - bird.x) , int(pipe.bottom_pipe_position- round(bird.y)) )

    top_colide = bird_mask.overlap(top_pipe_mask, top_offset)
    bottom_colide = bird_mask.overlap(bottom_pipe_mask, bottom_offset)

    if top_colide or bottom_colide:
        return True
    
    return False

def main():
    bird = Bird(WINDOW_WIDTH/2 - 20,WINDOW_HEIGHT/2 - 60)
    pipes = [Pipe(WINDOW_WIDTH)]
    base = Base(WINDOW_HEIGHT - 100)

    window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    run = True
    clock = pygame.time.Clock()

    score = 0
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        #bird.move()
        pipes_for_remove = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            
            if check_collision(bird, pipe):
               pass
                
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                pipes_for_remove.append(pipe)
            
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True 

        if add_pipe : 
            score += 1
            pipes.append(Pipe(WINDOW_WIDTH + 100))

        for pipe in pipes_for_remove:
            pipes.remove(pipe)

        if bird.y + bird.current_image.get_height() > 500:
            pass

        base.move()
        update_window(window,bird,pipes,base, score)
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()