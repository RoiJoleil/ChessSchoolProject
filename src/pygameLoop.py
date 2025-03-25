"""This file contains the main loop while the application is running"""
import pygame
from src.util.config import SCREEN_SIZE

class Chess:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Chess')
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.running = True # Boolean controlling if the app is running
        self.chess_board = []

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Fill Screen initially as Black
            self.screen.fill((0, 0, 0))

            # Update the Screen
            pygame.display.flip()

        # Quit the App
        pygame.quit()