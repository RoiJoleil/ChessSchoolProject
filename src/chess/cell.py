import pygame
import random
from src import pngHandler
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from src.chess.pieces import Piece

CELL_SIZE = 75


class Cell:
    def __init__(self, pos, grid_x, grid_y):
        self.rect = pygame.rect.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
        self.grid_pos = (grid_x, grid_y)
        self.piece = None

        self._set_styling()

    def get_position(self) -> tuple:
        return (self.rect.x, self.rect.y)

    def set_piece(self, piece: "Piece" = None):
        self.piece = piece

    def _set_styling(self):
        if (self.grid_pos[0]+self.grid_pos[1]) % 2 == 0:
            self.tile = random.choice(pngHandler.light_tiles)
            self.tile = pngHandler.rescale(self.tile, CELL_SIZE, CELL_SIZE)
        else:
            self.tile = random.choice(pngHandler.dark_tiles)
            self.tile = pngHandler.rescale(self.tile, CELL_SIZE, CELL_SIZE)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.tile, (self.rect.x, self.rect.y))
            
    def __repr__(self):
        header = f"[class '{self.__class__.__name__}' Information]"
        positional_info = f"(pos={(self.rect.x, self.rect.y)}, w={self.rect.w}, h={self.rect.h})"
        gameplay_info = f"(grid={self.grid_pos}, piece={self.piece})"
        return f"{header}\n{positional_info}\n{gameplay_info}\n"

cells: Dict[tuple, Cell] = {} # {tuple: Cell}

# API
def create_cell(pos: tuple, grid_x: int, grid_y: int):
    cell = Cell(pos, grid_x, grid_y)
    cells[cell.grid_pos] = cell

def get_cell(pos):
    global cells
    return cells.get(pos, None)

def draw(surface: pygame.Surface):
    global cells
    for cell in cells.values():
        cell.draw(surface)
        if cell.piece:
            cell.piece.draw(surface)

def move_piece(frm: Cell, to: Cell):
    """'frm' moves 'to'"""
    to.piece = frm.piece
    to.piece.set_position(to.rect.x, to.rect.y)
    frm.piece = None