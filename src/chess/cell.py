import pygame
import random
from src import pngHandler
from typing import TYPE_CHECKING, Dict, Optional, List
from src.settings import CELL_SIZE

if TYPE_CHECKING:
    from src.chess.pieces import Piece


class Cell:
    def __init__(self, pos, grid_x, grid_y):
        self.rect = pygame.rect.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
        self.grid_pos = (grid_x, grid_y)
        self.piece = None
        self.focus = None

        self._set_styling()

    def set_focus(self, img: Optional[pygame.Surface]):
        """
        Set a focus to the tile if its of importance.
        I.e. the move options, if there was a move previously or if its currently selected.
        """
        self.focus = img

    def get_position(self) -> tuple:
        return (self.rect.x, self.rect.y)

    def set_piece(self, piece: "Piece" = None):
        self.piece = piece

    def _set_styling(self):
        if (self.grid_pos[0]+self.grid_pos[1]) % 2 == 0:
            self.tile = random.choice(pngHandler.light_tiles)
        else:
            self.tile = random.choice(pngHandler.dark_tiles)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.tile, (self.rect.x, self.rect.y))
        if self.piece:
            self.piece.draw(screen)
        if self.focus:
            screen.blit(self.focus, (self.rect.x, self.rect.y))
            
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

def get_cell(x: int, y: int) -> Cell:
    global cells
    return cells.get((x, y), None)

def set_focus(cells: List[Cell], focus_type: str = None):
    """
    Sets a focus on a cell. Valid focus types are:
    - selected
    - move
    - prev
    - None
    """
    for cell in cells:
        if focus_type == "selected":
            cell.set_focus(pngHandler.get_pygame_image("selected-focus"))
        elif focus_type == "move":
            cell.set_focus(pngHandler.get_pygame_image("move-focus"))
        elif focus_type == "prev":
            cell.set_focus(pngHandler.get_pygame_image("prev-focus"))
        elif focus_type is None:
            cell.set_focus(None)

def clear_board():
    """For restarting a game."""
    global cells
    cells.clear()

def draw(surface: pygame.Surface):
    global cells
    for cell in cells.values():
        cell.draw(surface)

def move_piece(frm: Cell, to: Cell):
    """Move a piece from one cell to another."""
    to.piece = frm.piece
    to.piece.set_position(to.rect.x, to.rect.y)
    frm.piece = None

def is_occupied(cell: Cell = None, x: int = None, y: int = None) -> bool:
    """
    Returns a bool if the target cell is currently occupied.
    Either a Cell, or the Grid Position of the cell can be given.

    Args:
        cell (class): The Target Cell.
        x (int): X Grid Position
        y (int): Y Grid Position
    """
    # Get the cell.Cell if x and y is given.
    if x and y:
        cell = get_cell(x, y)

    return bool(cell.piece)
