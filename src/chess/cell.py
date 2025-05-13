import pygame
import random
from src import pngHandler
from typing import TYPE_CHECKING, Dict, Optional, List, Tuple
from src.settings import CELL_SIZE
from src.chess import pieces
from src.chess.util import Move
from enum import Enum

GridPos = Tuple[int, int]
ScreenPos = Tuple[int, int]

class FocusType(Enum):
    SELECTED = "selected-focus"
    MOVE = "move-focus"
    PREV = "prev-focus"

class Cell:
    def __init__(self, screen_pos: ScreenPos, grid_pos: GridPos):
        self.rect = pygame.rect.Rect(screen_pos[0], screen_pos[1], CELL_SIZE, CELL_SIZE)
        self.grid_pos = (grid_pos[0], grid_pos[1])
        self.piece = None
        self.focus = {FocusType.SELECTED: False, FocusType.MOVE: False, FocusType.PREV: False}

        self._set_styling()

    def toggle_focus(self, typ: FocusType, mode: bool):
        """
        Set a focus to the tile if its of importance.
        I.e. the move options, if there was a move previously or if its currently selected.
        """
        self.focus[typ] = mode

    def get_screen_position(self) -> ScreenPos:
        return (self.rect.x, self.rect.y)

    def get_grid_position(self) -> GridPos:
        return self.grid_pos

    def set_piece(self, piece: "pieces.Piece" = None):
        self.piece = piece
        if piece:
            self.piece.cell = self

    def _set_styling(self):
        if (self.grid_pos[0]+self.grid_pos[1]) % 2 == 0:
            self.tile = random.choice(pngHandler.light_tiles)
        else:
            self.tile = random.choice(pngHandler.dark_tiles)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.tile, (self.rect.x, self.rect.y))
        if self.piece:
            self.piece.draw(screen)

        if self.focus[FocusType.SELECTED]:
            screen.blit(pngHandler.get_pygame_image(FocusType.SELECTED.value), (self.rect.x, self.rect.y))
        elif self.focus[FocusType.MOVE]:
            screen.blit(pngHandler.get_pygame_image(FocusType.MOVE.value), (self.rect.x, self.rect.y))
        elif self.focus[FocusType.PREV]:
            screen.blit(pngHandler.get_pygame_image(FocusType.PREV.value), (self.rect.x, self.rect.y))
            
    def __repr__(self):
        header = f"[class '{self.__class__.__name__}' Information]"
        positional_info = f"(pos={(self.rect.x, self.rect.y)}, w={self.rect.w}, h={self.rect.h})"
        gameplay_info = f"(grid={self.grid_pos}, piece={self.piece})"
        return f"{header}\n{positional_info}\n{gameplay_info}\n"

cells: Dict[GridPos, Cell] = {}
# API
def create_cell(screen_pos: ScreenPos, grid_pos: GridPos, piece:"pieces.Piece" = None):
    cell = Cell(screen_pos, grid_pos)
    if piece:
        cell.set_piece(piece)
    cells[cell.grid_pos] = cell
    return cell

def full_reset_focus():
    """Resets the focus on all Cells"""
    for cell in cells.values():
        cell.toggle_focus(FocusType.SELECTED, False)
        cell.toggle_focus(FocusType.MOVE, False)
        cell.toggle_focus(FocusType.PREV, False)

def set_piece(x, y, piece: Optional[pieces.Piece]):
    cell = get_cell(x, y)
    cell.set_piece(piece)

def get_cell(x: int, y: int) -> Cell:
    global cells
    return cells.get((x, y), None)

def set_focus(cells: List[Cell], focus_type: FocusType, mode: bool):
    """Sets the focus on a cell"""
    if not cells:
        return
    
    for cell in cells:
        cell.toggle_focus(focus_type, mode)

def draw(surface: pygame.Surface):
    global cells
    for cell in cells.values():
        cell.draw(surface)

def move_piece(frm: Cell, to: Cell):
    """Move a piece from one cell to another."""
    frm.piece.move(to.grid_pos[0], to.grid_pos[1])


# History of previous moves inspired by numeric
record_history = True

def set_record_history():
    global record_history
    record_history = True

def unset_record_history():
    global record_history
    record_history = False

history = ""

def add_history(prev:tuple, next:tuple, promotion:pieces.Piece = None):
    global history, record_history
    if record_history:
        history = history + f"{prev[0]}{prev[1]}{next[0]}{next[1]}"

def remove_history():
    global history
    if history:
        history = history[:-4]

def previous_move() -> Move:
    global history
    if len(history) >= 4:
        return Move((int(history[-4]), int(history[-3])),(int(history[-2]), int(history[-1])))
    else:
        return None
    
def history_to_iterable() -> List[Move]:
    result = []
    for i in range(0, len(history), 4):
        result.append(Move((int(history[i]), int(history[i + 1])),(int(history[i + 2]), int(history[i + 3]))))
    
    return result

def has_been_touched(pos: Tuple[int, int]):
    """Check if given position is in the history"""
    global history
    i = 0
    while len(history[i:]) > 2:
        if history[i + 0] == pos[0] and history[i + 1] == pos[1]:
            return True
        i += 2
    return False

def prev_move_focus():
    global previous_move
    last_move = previous_move()
    if last_move == None:
        return
    prev, next = get_cell(last_move.prev[0], last_move.prev[1]), get_cell(last_move.next[0], last_move.next[1])
    global set_focus
    set_focus([prev, next], FocusType.PREV, True)
    
def prev_move_unfocus():
    global previous_move
    last_move = previous_move()
    if last_move == None:
        return
    prev, next = get_cell(last_move.prev[0], last_move.prev[1]), get_cell(last_move.next[0], last_move.next[1])
    global set_focus
    set_focus([prev, next], FocusType.PREV, False)
    
