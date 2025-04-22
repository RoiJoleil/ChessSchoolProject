import pygame
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from src.chess.pieces import Piece

CELL_LIGHT = (200, 120, 50)
CELL_DARK = (100, 50, 20)
CELL_BORDER_COLOR = (0, 0, 0)
CELL_BORDER_WIDTH = 1
CELL_SIZE = 75


class Cell:
    def __init__(self, pos, grid_x, grid_y):
        self.rect = pygame.rect.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
        self.grid_pos = (grid_x, grid_y)
        self.piece = None

        self._set_styling()

    def set_piece(self, piece: "Piece" = None):
        self.piece = piece

    def _set_styling(self):
        if (self.grid_pos[0]+self.grid_pos[1]) % 2 == 0:
            self.background_color = CELL_DARK
            self.border_color = CELL_BORDER_COLOR
            self.border_width = CELL_BORDER_WIDTH
        else:
            self.background_color = CELL_LIGHT
            self.border_color = CELL_BORDER_COLOR
            self.border_width = CELL_BORDER_WIDTH

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.background_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
            
    def __repr__(self):
        header = f"[class '{self.__class__.__name__}' Information]"
        positional_info = f"(pos={(self.rect.x, self.rect.y)}, w={self.rect.w}, h={self.rect.h})"
        styling_info = f"(background_color={self.background_color}, border_color={self.border_color}, border_width={self.border_width})"
        gameplay_info = f"(grid={self.grid_pos}, piece={self.piece})"
        return f"{header}\n{positional_info}\n{styling_info}\n{gameplay_info}\n"

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
    to.piece.set_position(to.piece.rect.x, to.piece.rect.y)
    frm.piece = None