import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.chess.pieces import Piece


class Cell:
    def __init__(self, screen: pygame.Surface, pos, w, h, x, y):
        # Positional Information
        self.pos = pos # Draw Position
        self.w = w # draw width
        self.h = h # draw height
        self.c = (pos[0] + w//2, pos[1] + h//2) # center

        #Styling Information
        self.background_color = (0, 0, 0)
        self.border_color = (0, 0, 0)
        self.border_width = 1
        self.rect = None

        # Gameplay Information
        self.screen = screen
        self.grid = (x, y) # Chessboard position
        self.piece: 'Piece' = None

    def set_styling(self, background_color, border_color, border_width):
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width

    def set_piece(self, piece: 'Piece' = None):
        self.piece = piece

    def draw(self):
        pygame.draw.rect(self.screen, self.background_color, self.rect) # Draw Background
        pygame.draw.rect(self.screen, self.border_color, self.rect, self.border_width) # Draw Border
        self.piece.draw() if self.piece != None else None

    def __repr__(self):
        header = f"[class '{self.__class__.__name__}' Information]"
        positional_info = f"(pos={self.pos}, w={self.w}, h={self.h}, c={self.c})"
        styling_info = f"(background_color={self.background_color}, border_color={self.border_color}, border_width={self.border_width})"
        gameplay_info = f"(grid={self.grid}, piece={self.piece})"
        return f"{header}\n{positional_info}\n{styling_info}\n{gameplay_info}\n"
