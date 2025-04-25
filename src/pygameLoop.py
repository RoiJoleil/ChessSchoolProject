"""This file contains the main loop while the application is running"""
import pygame
from src.util.config import SCREEN_SIZE
from src.util.config import ChessBoardSurface as CBS
from src.chess.chessBoard import ChessBoard
from src import pngHandler
from src.util.filemanager import Filemanager
from src.util.filemanager import GameConverter

class Chess:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Chess')
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pngHandler.init()
        self.chess_board_rect = pygame.rect.Rect(CBS.x, CBS.y, CBS.w, CBS.h)
        self.chess_board_surface = self.screen.subsurface(self.chess_board_rect)
        self.chess_board = ChessBoard(self.chess_board_surface)
        self.running = True # Boolean controlling if the app is running

    def event(self, event):
        self.chess_board.event(event)

    def draw(self):
        # Draw Chessboard
        self.chess_board.draw()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.event(event)

            # Fill Screen initially as Black
            self.screen.fill((0, 0, 0))

            self.draw()

            # Update the Screen
            pygame.display.flip()

#        print(f"save Data\n{GameConverter.construct_save_data()}")
#        Filemanager.save_file_dialog()
        # Quit the App
        pygame.quit()