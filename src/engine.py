"""This file contains the main loop while the application is running"""
import pygame
from src.settings import SCREEN_SIZE, CHESS_SURFACE_POSITION, CHESS_SURFACE_SIZE, FPS
from src.chess.board import Board
from src import pngHandler
from src.util.filemanager import Filemanager
from src.util.filemanager import GameConverter

pygame.init()
pygame.display.set_caption('Chess')
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
pngHandler.init()

chess_board_rect = pygame.rect.Rect(CHESS_SURFACE_POSITION[0], CHESS_SURFACE_POSITION[1], CHESS_SURFACE_SIZE[0], CHESS_SURFACE_SIZE[1])
chess_board_surface = screen.subsurface(chess_board_rect)
chess_board = Board(chess_board_surface)
running = True

def _event(event):
    global chess_board
    chess_board.event(event)

def _draw():
    global chess_board
    chess_board.draw()

def run():
    global running, screen, clock
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
