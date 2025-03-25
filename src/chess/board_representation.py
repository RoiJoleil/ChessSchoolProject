from typing import List
from src.util.config import CHESSBOARD_COLORING

class Cell:
    def __init__(self, pos, w, h):
        self.pos = pos
        self.w = w
        self.h = h

class ChessBoard:
    """Create the BoardCells"""
    def __init__(self):
        self.cells: List[List[Cell]] = []

    def get_cell(self, x, y) -> Cell:
        return self.cells[x][y]

    def draw(self):
        """Draw the individual chessboard cells"""
