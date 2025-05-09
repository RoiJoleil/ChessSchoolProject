import pygame
import random
from src import pngHandler
from typing import TYPE_CHECKING, Dict, Optional, List
from src.settings import CELL_SIZE
from src.chess import pieces
from src.chess.util import Move


class Cell:
    def __init__(self, pos, grid_x, grid_y):
        self.rect = pygame.rect.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
        self.grid_pos = (grid_x, grid_y)
        self.piece = None
        self.focus = {"selected-focus": None, "move-focus": None, "prev-focus": None}

        self._set_styling()

    def set_focus(self, img: Optional[pygame.Surface], typ: str):
        """
        Set a focus to the tile if its of importance.
        I.e. the move options, if there was a move previously or if its currently selected.
        """
        self.focus[typ] = img

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
        if self.focus["selected-focus"]:
            screen.blit(self.focus["selected-focus"], (self.rect.x, self.rect.y))
        elif self.focus["move-focus"]:
            screen.blit(self.focus["move-focus"], (self.rect.x, self.rect.y))
        elif self.focus["prev-focus"]:
            screen.blit(self.focus["prev-focus"], (self.rect.x, self.rect.y))
            
    def __repr__(self):
        header = f"[class '{self.__class__.__name__}' Information]"
        positional_info = f"(pos={(self.rect.x, self.rect.y)}, w={self.rect.w}, h={self.rect.h})"
        gameplay_info = f"(grid={self.grid_pos}, piece={self.piece})"
        return f"{header}\n{positional_info}\n{gameplay_info}\n"

cells: Dict[tuple[int, int], Cell] = {} # {tuple: Cell}
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

def unfocus(cells: List[Cell], focus_type: str = None):
    """
    Sets a focus on a cell. Valid focus types are:
    - selected
    - move
    - prev
    """
    if not cells:
        return
    for cell in cells:
        if focus_type == "selected":
            cell.set_focus(None, "selected-focus")
        elif focus_type == "move":
            cell.set_focus(None, "move-focus")
        elif focus_type == "prev":
            cell.set_focus(None, "prev-focus")

def set_focus(cells: List[Cell], focus_type: str = None):
    """
    Sets a focus on a cell. Valid focus types are:
    - selected
    - move
    - prev
    """
    if not cells:
        return
    for cell in cells:
        if focus_type == "selected":
            cell.set_focus(pngHandler.get_pygame_image("selected-focus"), "selected-focus")
        elif focus_type == "move":
            cell.set_focus(pngHandler.get_pygame_image("move-focus"), "move-focus")
        elif focus_type == "prev":
            cell.set_focus(pngHandler.get_pygame_image("prev-focus"), "prev-focus")

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

def has_been_touched(pos:tuple[int:int]):
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
    set_focus([prev, next], "prev")
    

def prev_move_unfocus():
    global previous_move
    last_move = previous_move()
    if last_move == None:
        return
    prev, next = get_cell(last_move.prev[0], last_move.prev[1]), get_cell(last_move.next[0], last_move.next[1])
    global set_focus
    set_focus([prev, next])
    
