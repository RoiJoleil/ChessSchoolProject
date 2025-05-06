"""This file contains the main loop while the application is running"""
import pygame
from src.settings import SCREEN_SIZE, FPS
from src.chess import board
from src import pngHandler
from src.util.filemanager import Filemanager
from src.util.filemanager import GameConverter

pygame.init()
pygame.display.set_caption('Chess')
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
pngHandler.init()
board.init(screen)

running = True

def _event(event):
    board.event(event)

def _draw():
    board.draw()

def run():
    global running, screen, clock
    board.start_game()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            _event(event)

        # Fill Screen initially as Black
        screen.fill((0, 0, 0))

        _draw()

        # Update the Screen
        pygame.display.flip()
        clock.tick(FPS)

    #print(f"save Data\n{GameConverter.construct_save_data()}")
    #Filemanager.save_file_dialog()
    # Quit the App
    pygame.quit()
