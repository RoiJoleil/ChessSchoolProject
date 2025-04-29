import pygame
from src import pngHandler
from typing import List, TYPE_CHECKING
from src.settings import PIECE_SIZE

from src.chess import cell

class Piece:
    def __init__(self):
        pass

    def get_theoretical_moves(self):
        """
        Returns a list of cells the piece can theoreticly move to ignoring all other pieces
        """