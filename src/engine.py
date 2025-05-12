"""This file contains the main loop while the application is running"""
import pygame
pygame.init()

from .gui import start_game_button
from src.settings import FPS, SCREEN_SURFACE, CLOCK
from src.chess import board
from src import pngHandler

pygame.display.set_caption('Chess')
pngHandler.init()
board.init(SCREEN_SURFACE)

running = True

def run():
    global running, SCREEN_SURFACE, CLOCK
    board.start_game()
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            board.event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_game_button.is_clicked(mouse_pos):
                        start_game_button.update()

        SCREEN_SURFACE.fill((0, 0, 0))
        board.draw()
        start_game_button.is_hovered(mouse_pos)
        start_game_button.draw(SCREEN_SURFACE)

        pygame.display.flip()
        CLOCK.tick(FPS)

    pygame.quit()
