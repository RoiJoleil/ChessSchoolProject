import pygame
from src import pngHandler
from typing import List, TYPE_CHECKING
from src.settings import PIECE_SIZE

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

def sign_of_number(nmb:int) -> int:
    if nmb == 0:
        return 0
    return 1 if nmb > 0 else -1

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
        self.cell = cell.get_cell(x, y)
        self.set_position(self.cell.rect.x, self.cell.rect.y)

    def set_position(self, x: int, y: int):
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface: pygame.Surface):
        surface.blit(self.piece, (self.rect.x, self.rect.y))

    def __repr__(self):
        header = f"[class '{self.__class__.__name__}' Information]"
        team_info = chessTeam[self.team]
        return f"{header}\n{team_info}\n"

    def is_valid_position(self, curr:tuple, dest:tuple):
        """
        checks if the destination is a valid position from the current position
        Args:
            curr(tuple): current Position of the Piece
            dest(tuple): destination position of the Piece
            pieceInHex(int): Value fo what is in the Cell, -1 is None, 0 is White 1 is Black
        """
        raise NotImplementedError()
    def is_valid_move(self, dest : "cell.Cell") -> bool:
        raise not NotImplementedError
    def get_valid_moves(self) -> List["cell.Cell"]:
        raise NotImplementedError()

class Pawn(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 1 + 8 * self.team

    def _set_styling(self):
        name = "white-pawn" if self.team else "black-pawn"
        self.piece = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr:tuple, dest:tuple) -> bool:
        # if the piece is black the direction of the movement must be -1 ( 1 -2 * 1)
        # else when the piece white the direction of movement must be 1 ( 1 - 2 * 0)
        if dest[1] - curr[1] != (-1 if self.team else 1):
            return False
        temp = cell.get_cell(dest[0], dest[1])
        # if the movement is vertical the Cell must be empty
        if temp.piece == None:
            return curr[0] == dest[0]
        # if the movement is diagonal the Tile has to be occupied by the other team
        if abs(dest[0] - curr[0]) == 1:
            temp = cell.get_cell(dest[0], dest[1])
            return self.team != temp.piece.team
        return False
    def is_valid_move(self, dest):
        if abs(dest.grid_pos[1] - self.cell.grid_pos[1]) == 2:
            if self.team:
                if(dest.grid_pos[1] == 4):
                    return (
                        cell.get_cell(dest.grid_pos[0], 5).piece == None and
                        cell.get_cell(dest.grid_pos[0], 4).piece == None
                        )
            else:
                if(dest.grid_pos[1] == 3):
                    return (
                        cell.get_cell(dest.grid_pos[0], 3).piece == None and
                        cell.get_cell(dest.grid_pos[0], 2).piece == None
                        )
            return False
        
        return self.is_valid_position(self.cell.grid_pos, dest.grid_pos)

    def get_valid_moves(self):
        # singular step forward
        result = []
        for i in range(-1, 2):
            dest = cell.get_cell(self.cell.grid_pos[0] + i, self.cell.grid_pos[1] + (1 if self.team else -1))
            if dest == None:
                continue
            if self.is_valid_move(dest):
                result.append(dest)
        # double step forward
        dest = cell.get_cell(self.cell.grid_pos[0], self.cell.grid_pos[1] + 2 *(1 if self.team else -1))
        if dest:
            if self.is_valid_position(self.cell.grid_pos, dest.grid_pos):
                result.append(dest)


class Rook(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 2 + 8 * self.team

    def _set_styling(self):
        name = "white-rook" if self.team else "black-rook"
        self.piece = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest) -> bool:
        temp = cell.get_cell(dest[0], dest[1])
        if not temp:
            return False
        if temp.piece:
            if temp.piece.team == self.team:
                return False
        return bool(dest[0] - curr[0]) ^ bool(dest[1] - curr[1])
    def is_valid_move(self, dest):
        if not self.is_valid_position(self.cell.grid_pos, dest.grid_pos):
            return False        
        global sign_of_number
        diff = (sign_of_number(dest.grid_pos[0] - self.cell.grid_pos[0]), sign_of_number(dest.grid_pos[1] - self.cell.grid_pos[1]))
        for i in range(1,8):
            temp_x = self.cell.grid_pos[0] + diff[0] * i
            temp_y = self.cell.grid_pos[1] + diff[1] * i
            if (
                temp_x == dest.grid_pos[0] and
                temp_y == dest.grid_pos[1]
            ):
                return True
            temp = cell.get_cell(temp_x, temp_y)
            if temp is None:
                return False
            if temp.piece is not None:
                return False
        return False
    def get_valid_moves(self):
        result = []
        for i in [-1, 1]:
            temp = cell.get_cell(self.cell.grid_pos[0] + i, self.cell.grid_pos[1])
            while temp:
                if not self.cell.piece.is_valid_position(self.cell.grid_pos, temp.grid_pos, temp.piece.identity if temp.piece else 0):
                    break
                result.append(temp)
                temp = cell.get_cell(self.cell.grid_pos[0] + i, self.cell.grid_pos[1])
            temp = cell.get_cell(self.cell.grid_pos[0], self.cell.grid_pos[1] + i)
            while temp:
                if not self.is_valid_position(self.cell.grid_pos, temp.grid_pos, temp.piece.identity if temp.piece else 0):
                    break
                result.append(temp)
                temp = cell.get_cell(self.cell.grid_pos[0], self.cell.grid_pos[1] + i)


class Knight(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 3 + 8 * self.team

    def _set_styling(self):
        name = "white-knight" if self.team else "black-knight"
        self.piece = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest) -> bool:
        temp = cell.get_cell(dest[0], dest[1])
        if temp.piece:
            if temp.piece.team == self.team:
                return False
        return pow(dest[0] - curr[0], 2) + pow(dest[1] - curr[1], 2) == 5
    def is_valid_move(self, dest):
        return self.is_valid_position(self.cell.grid_pos, dest.grid_pos)
    def get_valid_moves(self):
        result = []
        for i in [-1, 1]:
            for j in [-2, 2]:
                temp = cell.get_cell(self.cell.grid_pos[0] + i, self.cell.grid_pos[1] + j)
                if temp == None:
                    continue
                if self.cell.piece.is_valid_position(self.cell.grid_pos, temp.grid_pos, temp.piece.identity if temp.piece else 0):
                    result.append(temp)
                temp = cell.get_cell(self.cell.grid_pos[0] + j, self.cell.grid_pos[1] + i)
                if temp == None:
                    continue
                if self.is_valid_position(self.cell.grid_pos, temp.grid_pos, temp.piece.identity if temp.piece else 0):
                    result.append(temp)
    
class Bishop(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 4 + 8 * self.team

    def _set_styling(self):
        name = "white-bishop" if self.team else "black-bishop"
        self.piece = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest) -> bool:
        temp = cell.get_cell(dest[0], dest[1])
        if temp.piece:
            if temp.piece.team == self.team:
                return False
        return (abs(dest[0] - curr[0]) == abs(dest[1] - curr[1])) and (abs(dest[0] - curr[0]) != 0)
    def is_valid_move(self, dest):
        if not self.is_valid_position(self.cell.grid_pos, dest.grid_pos):
            return False        
        global sign_of_number
        diff = (sign_of_number(dest.grid_pos[0] - self.cell.grid_pos[0]), sign_of_number(dest.grid_pos[1] - self.cell.grid_pos[1]))
        for i in range(1,8):
            temp_x = self.cell.grid_pos[0] + diff[0] * i
            temp_y = self.cell.grid_pos[1] + diff[1] * i
            if (
                temp_x == dest.grid_pos[0] and
                temp_y == dest.grid_pos[1]
            ):
                return True
            temp = cell.get_cell(temp_x, temp_y)
            if temp is None:
                return False
            if temp.piece is not None:
                return False
        return False
    def get_valid_moves(self):
        result = []
        for i in [-1, 1]:
            for j in [-1, 1]:
                temp = cell.get_cell(self.cell.grid_pos[0] + i, self.cell.grid_pos[1] + j)
                while temp:
                    if not self.is_valid_position(self.cell.grid_pos, temp.grid_pos, temp.piece.identity if temp.piece else 0):
                        break
                    result.append(temp)
                    temp = cell.get_cell(self.cell.grid_pos[0] + i, self.cell.grid_pos[1] + j)
        return result

class Queen(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 5 + 8 * self.team

    def _set_styling(self):
        name = "white-queen" if self.team else "black-queen"
        self.piece = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest) -> bool:
        temp = cell.get_cell(dest[0], dest[1])
        if temp.piece:
            if temp.piece.team == self.team:
                return False
        if abs(dest[0] - curr[0]) + abs(dest[1] - curr[1]) == 0:
            return False
        return (abs(dest[0] - curr[0]) == abs(dest[1] - curr[1])) and (abs(dest[0] - curr[0]) != 0) or bool(dest[0] - curr[0]) ^ bool(dest[1] - curr[1])

    def is_valid_move(self, dest):
        if not self.is_valid_position(self.cell.grid_pos, dest.grid_pos):
            return False        
        global sign_of_number
        diff = (sign_of_number(dest.grid_pos[0] - self.cell.grid_pos[0]), sign_of_number(dest.grid_pos[1] - self.cell.grid_pos[1]))
        for i in range(1,8):
            temp_x = self.cell.grid_pos[0] + diff[0] * i
            temp_y = self.cell.grid_pos[1] + diff[1] * i
            if (
                temp_x == dest.grid_pos[0] and
                temp_y == dest.grid_pos[1]
            ):
                return True
            temp = cell.get_cell(temp_x, temp_y)
            if temp is None:
                return False
            if temp.piece is not None:
                return False
        return False
    def get_valid_moves(self):
        result = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                temp = cell.get_cell(self.cell.grid_pos[0] + i,self.cell.grid_pos[1] + j)
                while temp:
                    if not self.is_valid_position(self.cell.grid_pos, temp.grid_pos, temp.piece.identity if temp.piece else 0):
                        break
                    result.append(temp)
                    temp = cell.get_cell(self.cell.grid_pos[0] + i, self.cell.grid_pos[1] + j)

class King(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 6 + 8 * self.team
        self.castling = {(2,0),(6,0)} if self.team else {(2,7),(6,7)}

    def _set_styling(self):
        name = "white-king" if self.team else "black-king"
        self.piece = pngHandler.get_pygame_image(name)

    def in_check(self, check:"cell.Cell" = None) -> bool:
        if not check:
            check = self.cell
        for x in range(0, 8):
            for y in range(0,8):
                threat = cell.get_cell(x, y)
                if threat.piece if threat else False:
                    if (threat.piece.is_valid_move(check)):
                        return True
        return False

    def is_valid_position(self, curr, dest) -> bool:
        temp = cell.get_cell(dest[0], dest[1])
        if temp.piece:
            if temp.piece.team == self.team:
                return False
        return 0 < (curr[0] - dest[0]) ** 2 + (curr[1] - dest[1]) ** 2 <= 2
    def is_valid_move(self, dest,):
        if dest in self.castling:
            if dest.grid_pos[1] - self.cell.grid_pos[1] == 2:

                x_mod = sign_of_number(dest.grid_pos[0] - self.cell.grid_pos[0])
                y_mod = sign_of_number(dest.grid_pos[1] - self.cell.grid_pos[1])
                if (
                    self.is_valid_position(self.cell.grid_pos, (self.cell.grid_pos[0] + x_mod, self.cell.grid_pos[1] + y_mod)) and
                    self.is_valid_position(self.cell.grid_pos, dest.grid_pos)
                ):
                    return not (self.in_check(cell.get_cell) or self.in_check(dest))
        if self.is_valid_position(self.cell.grid_pos, dest.grid_pos):
            return not self.in_check(dest)
    def get_valid_moves(self):
        result = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                temp = cell.get_cell(self.cell.grid_pos[0] + i, self.cell.grid_pos[1] + j)
                if not temp:
                    continue
                if self.is_valid_position(self.cell.grid_pos, temp.grid_pos):
                    result.append(temp)
        if self.castling:
            for i in self.castling:
                result.append(cell.get_cell(i[0], i[1]))
        return result
    
def get_pawn_row() -> List[Piece]:
    """Return a list of pawns."""
    return [Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn]

def get_piece_row() -> List[Piece]:
    """Return a list of pieces in the order they spawn in."""
    return [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]