import pygame
import random
from src import pngHandler
from typing import TYPE_CHECKING, Dict, Optional, List
from src.settings import CELL_SIZE
from src.chess import pieces


class En_Passante:
    def __init__(self):
        self.checkPos = None
        self.piecePos = None
        self.team = False
        self.active = 0

    def set(self, piecePos:tuple = None, team:bool = False, active = 1):
        self.piecePos = (piecePos[0], piecePos[1])
        self.team = team
        self.active = active
        if self.team:
            self.checkPos = (self.piecePos[0], 5)
        else:
            self.checkPos = (self.piecePos[0], 2)

    def reset(self):
        self.checkPos = None
        self.piecePos = None
        self.active = 0

    def __repr__(self):
        header = f"[class '{self.__class__.__name__}' Information]"
        positionalInfo = f" toCheck={self.checkPos}\tpiecePos={self.piecePos}"
        otherInfo = f" team={self.team}"
        return f"{header}\n{positionalInfo}\n{otherInfo}\n"
    
en_passante = En_Passante()
white_king:pieces.King = None
black_king:pieces.King = None
kings = {
    True  : white_king,
    False : black_king
}

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

    def set_piece(self, piece: "pieces.Piece" = None):
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
def create_cell(pos: tuple, grid_x: int, grid_y: int, piece:"pieces.Piece" = None):
    cell = Cell(pos, grid_x, grid_y)
    if piece:
        cell.set_piece(piece)
        cell.piece.cell = cell
    cells[cell.grid_pos] = cell
    return cell

def get_cell(x: int, y: int) -> Cell:
    global cells
    return cells.get((x, y), None)

def get_cells():
    """Get the entire board"""
    global cells
    return cells

def set_focus(cells: List[Cell], focus_type: str = None):
    """
    Sets a focus on a cell. Valid focus types are:
    - selected
    - move
    - prev
    - None
    """
    if not cells:
        return
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
    to.piece.move(to.grid_pos[0], to.grid_pos[1])


# History of previous moves inspired by numeric
history = ""

def add_history(prev:tuple, next:tuple):
    history.join(f"{prev[0]}{prev[1]}{next[0]}{next[1]}")

def remove_history():
    if history:
        history = history[:-4]

def previous_move() -> tuple[int:int]:
    if history:
        return {
            (int(history[-2]), int(history[-1]))
        }
    else:
        return (-1, -1)
    
def past_move(pos:tuple[int:int]):
    return f"{pos[0]}{pos[1]}" in history