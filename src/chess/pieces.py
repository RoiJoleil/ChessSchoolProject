import pygame
from src import pngHandler
from typing import List, TYPE_CHECKING
from src.settings import PIECE_SIZE

if TYPE_CHECKING:
    from src.chess import cell

chessPieces = {
    1:"pawn",
    2:"rook",
    3:"knight",
    4:"bishop",
    5:"queen",
    6:"king"
}
chessTeam = {
    False:  "black",
    True:   "white",
    "black": False,
    "white": True
}

class Piece:
    def __init__(self, cell: "cell.Cell", team: bool):
        # Positional Information
        self.cell = cell
        self.team = team # True = White, False = Black
        self.identity = 0
        self.piece = None

        # Gameplay Information
        self.rect = pygame.rect.Rect(self.cell.rect.x, self.cell.rect.y, PIECE_SIZE, PIECE_SIZE)
        self._set_styling()

    def _set_styling(self):
        raise NotImplementedError()
    
    def move(self, x: int, y: int):
        self.rect.x += x
        self.rect.y += y

    def set_position(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface: pygame.Surface):
        surface.blit(self.piece, (self.rect.x, self.rect.y))

    def __repr__(self):
        header = f"[class '{self.__class__.__name__}' Information]"
        team_info = chessTeam[self.team]
        return f"{header}\n{team_info}\n"
    
    def is_valid_position(self, curr:tuple, dest:tuple, pieceInHex:int):
        """
        checks if the destination is a valid position from the current position
        Args:
            curr(tuple): current Position of the Piece
            dest(tuple): destination position of the Piece
            pieceInHex(int): Value fo what is in the Cell, -1 is None, 0 is White 1 is Black
        """
        raise NotImplementedError()

class Pawn(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 1 + 8 * self.team

    def _set_styling(self):
        name = "white-pawn" if self.team else "black-pawn"
        self.piece = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr:tuple, dest:tuple, pieceInHex:int) -> bool:
        # if the piece is black the direction of the movement must be -1 ( 1 -2 * 1)
        # else when the piece white the direction of movement must be 1 ( 1 - 2 * 0)
        if dest[1] - curr[1] != 1 - 2 * self.team:
            return False
        # if the movement is vertical the Cell must be empty
        if curr[0] == dest[0]:
            return pieceInHex % 8 == 0
        # if the movement is diagonal the Tile has to be occupied by the other team
        elif abs(dest[0] - curr[0]) + abs(dest[1] - curr[1]) == 2:
            if pieceInHex % 8 == 0:
                return
            return self.team != pieceInHex // 8
        return False

class Rook(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 2 + 8 * self.team

    def _set_styling(self):
        name = "white-rook" if self.team else "black-rook"
        self.piece = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest, pieceInHex) -> bool:
        if (pieceInHex // 8 == self.team and pieceInHex % 8 != 0):
            return False
        return bool(dest[0] - curr[0]) ^ bool(dest[1] - curr[1])

class Knight(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 3 + 8 * self.team

    def _set_styling(self):
        name = "white-knight" if self.team else "black-knight"
        self.piece = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest, pieceInHex) -> bool:
        if (pieceInHex // 8 == self.team and pieceInHex % 8 != 0):
            return False
        return pow(dest[0] - curr[0], 2) + pow(dest[1] - curr[1], 2) == 5

class Bishop(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 4 + 8 * self.team

    def _set_styling(self):
        name = "white-bishop" if self.team else "black-bishop"
        self.piece = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest, pieceInHex) -> bool:
        if (pieceInHex // 8 == self.team and pieceInHex % 8 != 0):
            return False
        return (abs(dest[0] - curr[0]) == abs(dest[1] - curr[1])) and (abs(dest[0] - curr[0]) != 0)

class Queen(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 5 + 8 * self.team

    def _set_styling(self):
        name = "white-queen" if self.team else "black-queen"
        self.piece = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest, pieceInHex) -> bool:
        if (pieceInHex // 8 == self.team and pieceInHex % 8 != 0):
            return False
        if abs(dest[0] - curr[0]) + abs(dest[1] - curr[1]) == 0:
            return False
        return (abs(dest[0] - curr[0]) == abs(dest[1] - curr[1])) and (abs(dest[0] - curr[0]) != 0) or bool(dest[0] - curr[0]) ^ bool(dest[1] - curr[1])

class King(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 6 + 8 * self.team
        self.castling = {(2,0),(6,0)} if self.team else {(2,7),(6,7)}

    def _set_styling(self):
        name = "white-king" if self.team else "black-king"
        self.piece = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest, pieceInHex) -> bool:
        if (pieceInHex // 8 == self.team and pieceInHex % 8 != 0):
            return False
        return 0 < pow(curr[0] - dest[0], 2) + pow(curr[1] - dest[1], 2) <= 2

def get_pawn_row() -> List[Piece]:
    """Return a list of pawns."""
    return [Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn]

def get_piece_row() -> List[Piece]:
    """Return a list of pieces in the order they spawn in."""
    return [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]