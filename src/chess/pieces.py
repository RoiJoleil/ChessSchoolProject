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

def out_of_bounds(pos:tuple[int,int]):
    return (
        pos[0] < 0 or pos[0] >= 8 or
        pos[1] < 0 or pos[1] >= 8
    )

class Piece:
    def __init__(self, cell: "cell.Cell", team: bool):
        # Positional Information
        self.cell = cell
        self.team = team # True = White, False = Black
        self.identity = 0
        self.piece = None

        # Gameplay Information
        self._set_styling()

    def _set_styling(self):
        raise NotImplementedError()
    
    def move(self, x: int, y: int):
        self.cell.piece = None
        self.cell = cell.get_cell(x, y)
        self.cell.piece = self

        
    def draw(self, surface: pygame.Surface):
        surface.blit(self.piece, (self.cell.rect.x, self.cell.rect.y))

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
        raise not NotImplementedError
    
    def is_valid_move(self, dest : "cell.Cell", ignore:"cell.Cell") -> bool:
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
        if out_of_bounds(curr) or out_of_bounds(dest):
            return False
        # if the piece is black the direction of the movement must be -1 ( 1 -2 * 1)
        # else when the piece white the direction of movement must be 1 ( 1 - 2 * 0)
        if dest[1] - curr[1] != (-1 if self.team else 1):
            return False
        # if the movement is vertical the Cell must be empty
        if curr[0] == dest[0]:
            return cell.get_cell(dest[0], dest[1]).piece == None
        # if the movement is diagonal the Tile has to be occupied by the other team
        if abs(dest[0] - curr[0]) == 1:
            if cell.en_passante.active:
                if cell.en_passante.checkPos == dest:
                    return cell.en_passante.team != self.team
            else:
                temp = cell.get_cell(dest[0], dest[1])
                if temp.piece != None:
                    return self.team != temp.piece.team
                else:
                    return False
        return False
    
    def is_valid_move(self, dest, ignore=None):
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
        return result

    def move(self, x, y):
        if abs(y - self.cell.grid_pos[1]) == 2:
            cell.en_passante.set((x, y), self.team)
        elif cell.en_passante.checkPos == (x, y):
            cell.get_cell(cell.en_passante.piecePos[0], cell.en_passante.piecePos[1]).piece = None
            cell.en_passante.reset()
        super().move(x, y)

class Rook(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 2 + 8 * self.team

    def _set_styling(self):
        name = "white-rook" if self.team else "black-rook"
        self.piece = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest) -> bool:
        if out_of_bounds(curr) or out_of_bounds(dest):
            return False
        temp = cell.get_cell(dest[0], dest[1])
        if temp.piece:
            if temp.piece.team == self.team:
                return False
        return bool(dest[0] - curr[0]) ^ bool(dest[1] - curr[1])
    
    def is_valid_move(self, dest, ignore=None):
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
            if temp.piece is not None and temp != ignore:
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
        if out_of_bounds(curr) or out_of_bounds(dest):
            return False
        temp = cell.get_cell(dest[0], dest[1])
        if temp.piece:
            if temp.piece.team == self.team:
                return False
        return (dest[0] - curr[0]) ** 2 + (dest[1] - curr[1]) ** 2 == 5
    
    def is_valid_move(self, dest, ignore=None):
        return self.is_valid_position(self.cell.grid_pos, dest.grid_pos)
    
    def get_valid_moves(self):
        result = []
        for i in [-1, 1]:
            for j in [-2, 2]:
                temp = (self.cell.grid_pos[0] + i, self.cell.grid_pos[1] + j)
                if temp == None:
                    continue
                if self.cell.piece.is_valid_position(self.cell.grid_pos, temp):
                    result.append(temp)
                temp = (self.cell.grid_pos[0] + j, self.cell.grid_pos[1] + i)
                if temp == None:
                    continue
                if self.is_valid_position(self.cell.grid_pos, temp):
                    result.append(temp)
    
class Bishop(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 4 + 8 * self.team

    def _set_styling(self):
        name = "white-bishop" if self.team else "black-bishop"
        self.piece = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest) -> bool:
        if out_of_bounds(curr) or out_of_bounds(dest):
            return False
        temp = cell.get_cell(dest[0], dest[1])
        if temp.piece:
            if temp.piece.team == self.team:
                return False
        return (abs(dest[0] - curr[0]) == abs(dest[1] - curr[1])) and (abs(dest[0] - curr[0]) != 0)
    
    def is_valid_move(self, dest, ignore=None):
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
            if temp.piece is not None and temp is not ignore:
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
        if out_of_bounds(curr) or out_of_bounds(dest):
            return False
        temp = cell.get_cell(dest[0], dest[1])
        if temp.piece:
            if temp.piece.team == self.team:
                return False
        if abs(dest[0] - curr[0]) + abs(dest[1] - curr[1]) == 0:
            return False
        return (abs(dest[0] - curr[0]) == abs(dest[1] - curr[1])) and (abs(dest[0] - curr[0]) != 0) or bool(dest[0] - curr[0]) ^ bool(dest[1] - curr[1])

    def is_valid_move(self, dest, ignore = None):
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
            if temp.piece is not None and temp is not ignore:
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
                    if not self.is_valid_position(self.cell.grid_pos, temp.grid_pos):
                        break
                    result.append(temp)
                    temp = cell.get_cell(self.cell.grid_pos[0] + i, self.cell.grid_pos[1] + j)

class King(Piece):
    def __init__(self, cell: "cell.Cell", team: bool):
        super().__init__(cell, team)
        self.identity = 6 + 8 * self.team
        self.castling = {(2,7),(6,7)} if self.team else {(2,0),(6,0)}

    def _set_styling(self):
        name = "white-king" if self.team else "black-king"
        self.piece = pngHandler.get_pygame_image(name)

    def in_check(self, check:"cell.Cell") -> bool:
        for x in range(0, 8):
            for y in range(0, 8):
                threat = cell.get_cell(x, y)
                if threat and threat.piece and threat.piece.team != self.team:
                    if (threat.piece.is_valid_move(check, self.cell)):
                        return True
        return False

    def is_valid_position(self, curr, dest) -> bool:
        if out_of_bounds(curr) or out_of_bounds(dest):
            return False
        temp = cell.get_cell(dest[0], dest[1])
        if temp.piece:
            if temp.piece.team == self.team:
                return False
        return 0 < (curr[0] - dest[0]) ** 2 + (curr[1] - dest[1]) ** 2 <= 2
    
    def is_valid_move(self, dest, ignore=None):
        if self.is_castling(dest.grid_pos):
            if abs(dest.grid_pos[0] - self.cell.grid_pos[0]) == 2:
                x_mod = sign_of_number(dest.grid_pos[0] - self.cell.grid_pos[0])
                y_mod = sign_of_number(dest.grid_pos[1] - self.cell.grid_pos[1])
                mid_way = cell.get_cell(self.cell.grid_pos[0] + x_mod, self.cell.grid_pos[1] + y_mod)
                if (
                    mid_way.piece == None and
                    dest.piece == None
                ):
                    return not (self.in_check(cell.get_cell(self.cell.grid_pos[0], self.cell.grid_pos[0])) or self.in_check(dest))

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

    def is_castling(self, dest:tuple[int, int]) -> bool:
        """ Checks rather or not if the move with the given poisition would result in castling"""
        if self.castling == None:
            return False
        return dest in self.castling

    def castling_kingside(self):
        if self.team:
            super().move(6,7)
            cell.get_cell(7, 7).piece.move(5,7)
        else:
            super().move(6, 0)
            cell.get_cell(7, 0).piece.move(5, 0)
    
    def castling_queenside(self):
        if self.team:
            super().move(2, 7)
            cell.get_cell(0, 7).piece.move(3,7)
        else:
            super().move(2, 0)
            cell.get_cell(0, 0).piece.move(3, 0)
    
    def remove_castling(self, toRemove:tuple[int, int] = None):
        if self.castling == None:
            return
        elif toRemove == None:
            self.castling = None
            return
        elif toRemove[0] == 0:
            try:
                self.castling.remove((2,toRemove[1]))
            except:
                pass
        elif toRemove[0] == 7:
            try:
                self.castling.remove((6,toRemove[1]))
            except:
                pass

    def move(self, x, y):
        if self.is_castling((x, y)):
            if x < self.cell.grid_pos[0]:
                self.castling_queenside()
            else:
                self.castling_kingside()
            
        else:
            super().move(x, y)
        self.remove_castling()


#
#   functions in the global space of pieces
#
# Get a Row full of Pawns
def get_pawn_row() -> List[Piece]:
    """Return a list of pawns."""
    return [Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn]

def get_piece_row() -> List[Piece]:
    """Return a list of pieces in the order they spawn in."""
    return [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]