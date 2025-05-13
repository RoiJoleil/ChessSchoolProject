"""This file contains the main loop while the application is running"""
import pygame
from src import pngHandler
pygame.init()
pngHandler.init()

from .gui import start_game_button
from src.settings import FPS, SCREEN_SURFACE, CLOCK
from src.chess import board

pygame.display.set_caption('Chess')
board.init(SCREEN_SURFACE)

running = True

def run():
    global running, SCREEN_SURFACE, CLOCK
    board.start_game()
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            board.event(event)

        SCREEN_SURFACE.fill((0, 0, 0))
        board.draw()
        start_game_button.update_states(mouse_pos, mouse_press[0])
        start_game_button.update()
        start_game_button.draw(SCREEN_SURFACE)

        pygame.display.flip()
        CLOCK.tick(FPS)

    pygame.quit()
