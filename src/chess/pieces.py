import pygame
from src import pngHandler
from typing import List
from src.chess.globals import ChessTeam, ChessPieces
from src.chess import cell
from src.chess.util import Move


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
    def __init__(self, cell: "cell.Cell", team: ChessTeam, piece: ChessPieces):
        # Positional Information
        self.cell = cell
        self.team = team
        self.piece = piece
        self.team_bool = True if self.team == ChessTeam.WHITE else False
        self.identity = 0
        self.has_moved = False
        self.svg = None

        # Gameplay Information
        self._set_styling()

    def _set_styling(self):
        raise NotImplementedError()
    
    def move(self, x: int, y: int):
        cell.add_history(self.cell.grid_pos,(x, y))
        self.cell.piece = None
        self.cell = cell.get_cell(x, y)
        self.cell.piece = self
        if not self.has_moved:
            self.has_moved = True

    def draw(self, surface: pygame.Surface):
        surface.blit(self.svg, (self.cell.rect.x, self.cell.rect.y))

    def __repr__(self):
        header = f"[class '{self.__class__.__name__}' Information]"
        team_info = self.team
        position = f"grid_pos: {self.cell.grid_pos}"
        other_info = f"has moved: {self.has_moved}"
        return f"{header}\n{team_info}\n{position}\n{other_info}\n"

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
    def __init__(self, cell: "cell.Cell", team: ChessTeam, piece: ChessPieces):
        super().__init__(cell, team, piece)
        self.identity = 1 + 8 * self.team_bool

    def _set_styling(self):
        name = "white-pawn" if self.team_bool else "black-pawn"
        self.svg = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr:tuple, dest:tuple) -> bool:
        if out_of_bounds(curr) or out_of_bounds(dest):
            return False
        
        if (dest[1] - curr[1]) != (-1 if self.team_bool else 1):
            return False
        # if the movement is vertical the Cell must be empty
        if curr[0] == dest[0]:
            return cell.get_cell(dest[0], dest[1]).piece == None
        # if the movement is diagonal the Tile has to be occupied by the other team
        if abs(dest[0] - curr[0]) == 1:
            temp = cell.get_cell(dest[0], dest[1])
            if temp.piece != None:
                return self.team_bool != temp.piece.team

        return False
    
    def is_en_passante(self, dest:tuple[int,int]) -> bool:
        last_move = cell.previous_move()
        if last_move == None:
            return False
        pawn_cell = cell.get_cell(last_move.next[0], last_move.next[1])
        if not isinstance(pawn_cell.piece, Pawn):
            return False
        # with the vector of the previous Move you should be able to construct the destination
        diff_x = sign_of_number(last_move.next[0] - last_move.prev[0])
        diff_y = sign_of_number(last_move.next[1] - last_move.prev[1])
        to_check = cell.get_cell(last_move.prev[0] + diff_x, last_move.prev[1] + diff_y)
        if to_check.grid_pos != dest:
            return False
            
        return self.is_valid_position((self.cell.grid_pos[0], self.cell.grid_pos[1] + diff_y), pawn_cell.grid_pos)
    



    def is_valid_move(self, dest, ignore=None):
        if abs(dest.grid_pos[1] - self.cell.grid_pos[1]) == 2:
            if self.has_moved:
                return False
            if (dest.grid_pos[0] != self.cell.grid_pos[0]):
                return False
            diff_y = sign_of_number(dest.grid_pos[1] - self.cell.grid_pos[1])
            return (
                cell.get_cell(dest.grid_pos[0], self.cell.grid_pos[1] + diff_y).piece == None and
                cell.get_cell(dest.grid_pos[0], self.cell.grid_pos[1] + 2 * diff_y).piece == None
                )
        if self.is_en_passante(dest.grid_pos):
            return True

        
        return self.is_valid_position(self.cell.grid_pos, dest.grid_pos)

    def get_valid_moves(self):
        # singular step forward
        result = []
        for i in [-1, 0, 1]:
            dest = cell.get_cell(self.cell.grid_pos[0] + i, self.cell.grid_pos[1] + (-1 if self.team_bool else 1))
            if dest == None:
                continue
            if self.is_valid_move(dest):
                result.append(dest)
        # double step forward
        dest = cell.get_cell(self.cell.grid_pos[0], self.cell.grid_pos[1] + 2* (-1 if self.team_bool else 1))
        if dest:
            if self.is_valid_move(dest):
                result.append(dest)
        return result

    def move(self, x, y):
        if cell.get_cell(x, y).piece == None:
            temp = cell.get_cell(x, self.cell.grid_pos[1])
            temp.piece = None
        super().move(x, y)


class Rook(Piece):
    def __init__(self, cell: "cell.Cell", team: ChessTeam, piece: ChessPieces):
        super().__init__(cell, team, piece)
        self.identity = 2 + 8 * self.team_bool

    def _set_styling(self):
        name = "white-rook" if self.team_bool else "black-rook"
        self.svg = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest) -> bool:
        if out_of_bounds(curr) or out_of_bounds(dest):
            return False
        temp = cell.get_cell(dest[0], dest[1])
        if temp.piece:
            if temp.piece.team == self.team_bool:
                return False
        return bool(dest[0] - curr[0]) ^ bool(dest[1] - curr[1])
    
    def is_valid_move(self, dest, ignore=None):
        if not self.is_valid_position(self.cell.grid_pos, dest.grid_pos):
            return False
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
    
    def move(self, x, y):
        super().move(x, y)
    
    def get_valid_moves(self):
        result = []
        for i in [-1, 1]:
            temp = cell.get_cell(self.cell.grid_pos[0] + i, self.cell.grid_pos[1])
            while temp:
                if not self.cell.piece.is_valid_position(self.cell.grid_pos, temp.grid_pos):
                    break
                result.append(temp)
                temp = cell.get_cell(temp.grid_pos[0] + i, temp.grid_pos[1])
            temp = cell.get_cell(self.cell.grid_pos[0], self.cell.grid_pos[1] + i)
            while temp:
                if not self.is_valid_position(self.cell.grid_pos, temp.grid_pos):
                    break
                result.append(temp)
                temp = cell.get_cell(temp.grid_pos[0], temp.grid_pos[1] + i)
        return result

class Knight(Piece):
    def __init__(self, cell: "cell.Cell", team: ChessTeam, piece: ChessPieces):
        super().__init__(cell, team, piece)
        self.identity = 3 + 8 * self.team_bool

    def _set_styling(self):
        name = "white-knight" if self.team_bool else "black-knight"
        self.svg = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest) -> bool:
        if out_of_bounds(curr) or out_of_bounds(dest):
            return False
        temp = cell.get_cell(dest[0], dest[1])
        if temp.piece:
            if temp.piece.team == self.team_bool:
                return False
        return (dest[0] - curr[0]) ** 2 + (dest[1] - curr[1]) ** 2 == 5
    
    def is_valid_move(self, dest, ignore=None):
        return self.is_valid_position(self.cell.grid_pos, dest.grid_pos)
    
    def get_valid_moves(self):
        result = []
        for i in [-1, 1]:
            for j in [-2, 2]:
                # 1 2
                temp = cell.get_cell(self.cell.grid_pos[0] + i, self.cell.grid_pos[1] + j)
                if temp == None:
                    continue
                if self.cell.piece.is_valid_position(self.cell.grid_pos, temp.grid_pos):
                    result.append(temp)
                # 2 1
                temp = cell.get_cell(self.cell.grid_pos[0] + j, self.cell.grid_pos[1] + i)
                if temp == None:
                    continue
                if self.is_valid_position(self.cell.grid_pos, temp.grid_pos):
                    result.append(temp)
        return result
    def move(self, x, y):
        super().move(x, y)
    
class Bishop(Piece):
    def __init__(self, cell: "cell.Cell", team: ChessTeam, piece: ChessPieces):
        super().__init__(cell, team, piece)
        self.identity = 4 + 8 * self.team_bool

    def _set_styling(self):
        name = "white-bishop" if self.team_bool else "black-bishop"
        self.svg = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest) -> bool:
        if out_of_bounds(curr) or out_of_bounds(dest):
            return False
        temp = cell.get_cell(dest[0], dest[1])
        if temp.piece:
            if temp.piece.team == self.team_bool:
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
                    if not self.is_valid_position(self.cell.grid_pos, temp.grid_pos):
                        break
                    result.append(temp)
                    temp = cell.get_cell(temp.grid_pos[0] + i, temp.grid_pos[1] + j)
        return result

class Queen(Piece):
    def __init__(self, cell: "cell.Cell", team: ChessTeam, piece: ChessPieces):
        super().__init__(cell, team, piece)
        self.identity = 5 + 8 * self.team_bool

    def _set_styling(self):
        name = "white-queen" if self.team_bool else "black-queen"
        self.svg = pngHandler.get_pygame_image(name)

    def is_valid_position(self, curr, dest) -> bool:
        if out_of_bounds(curr) or out_of_bounds(dest):
            return False
        temp = cell.get_cell(dest[0], dest[1])
        if temp.piece:
            if temp.piece.team == self.team_bool:
                return False
        if abs(dest[0] - curr[0]) + abs(dest[1] - curr[1]) == 0:
            return False
        return (abs(dest[0] - curr[0]) == abs(dest[1] - curr[1])) or bool(dest[0] - curr[0]) ^ bool(dest[1] - curr[1])

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
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                temp = cell.get_cell(self.cell.grid_pos[0] + i,self.cell.grid_pos[1] + j)
                while temp:
                    if not self.is_valid_position(self.cell.grid_pos, temp.grid_pos):
                        break
                    result.append(temp)
                    temp = cell.get_cell(temp.grid_pos[0] + i, temp.grid_pos[1] + j)
        return result

class King(Piece):
    def __init__(self, cell: "cell.Cell", team: ChessTeam, piece: ChessPieces):
        super().__init__(cell, team, piece)
        self.identity = 6 + 8 * self.team_bool

    def _set_styling(self):
        name = "white-king" if self.team_bool else "black-king"
        self.svg = pngHandler.get_pygame_image(name)

    def in_check(self, check:"cell.Cell") -> bool:
        for x in range(0, 8):
            for y in range(0, 8):
                threat = cell.get_cell(x, y)
                if threat and threat.piece and threat.piece.team != self.team_bool:
                    if (threat.piece.is_valid_move(check, self.cell)):
                        return True
        return False

    def is_valid_position(self, curr, dest) -> bool:
        if out_of_bounds(curr) or out_of_bounds(dest):
            return False
        temp = cell.get_cell(dest[0], dest[1])
        if temp.piece:
            if temp.piece.team == self.team_bool:
                return False
        return 0 < (curr[0] - dest[0]) ** 2 + (curr[1] - dest[1]) ** 2 <= 2
    
    def is_valid_move(self, dest, ignore=None):
        if self.is_castling(dest.grid_pos):
            return True
        if self.is_valid_position(self.cell.grid_pos, dest.grid_pos):
            return not self.in_check(dest)
        
    def get_valid_moves(self):
        result = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                temp = cell.get_cell(self.cell.grid_pos[0] + i, self.cell.grid_pos[1] + j)
                if not temp:
                    continue
                if self.is_valid_position(self.cell.grid_pos, temp.grid_pos):
                    result.append(temp)
        # check queenside castling
        if self.is_castling((2, self.cell.grid_pos[1])):
            result.append(cell.get_cell(2, self.cell.grid_pos[1]))
        # check kingside castling
        if self.is_castling((6, self.cell.grid_pos[1])):
            result.append(cell.get_cell(6, self.cell.grid_pos[1]))
        return result

    def is_castling(self, dest:tuple[int, int]) -> bool:
        """ Checks rather or not if the move with the given poisition would result in castling"""
        # Checking the initial conditions for castling
        # has the king moved? ; is it the right coordinate
        if self.has_moved:
            return False
        
        if not (dest[0] in [2, 6]):
            return False
        if dest[1] != self.cell.grid_pos[1]:
            return False
        # constructing the position of the queenside or kingside Rook
        if dest[0] < self.cell.grid_pos[0]:
            rook_pos = (0, self.cell.grid_pos[1])
        else:
            rook_pos = (7, self.cell.grid_pos[1])
        
        rook_cell = cell.get_cell(rook_pos[0], rook_pos[1])

        if isinstance(rook_cell.piece, Rook):
            if rook_cell.piece.has_moved:
                return False
            # calculate vector  to check anything between rook and King
            diff_x = sign_of_number(rook_pos[0] - self.cell.grid_pos[0])
            temp = cell.get_cell(self.cell.grid_pos[0] + diff_x, self.cell.grid_pos[1])
            while temp.grid_pos != rook_cell.grid_pos:
                if(temp.piece != None):
                    return False
                temp = cell.get_cell(temp.grid_pos[0] + diff_x, temp.grid_pos[1])
            if temp.grid_pos != rook_pos:
                return False
            # check if the movement of the King would pass over a Check Position
            temp = cell.get_cell(self.cell.grid_pos[0] + diff_x, self.cell.grid_pos[1])
            if (self.in_check(temp)):
                return False
            temp = cell.get_cell(self.cell.grid_pos[0] + 2 * diff_x, self.cell.grid_pos[1])
            if (self.in_check(temp)):
                return False
            return True
        else:
            return False

    def castling_kingside(self):
        if self.team_bool:
            super().move(6,7)
            cell.get_cell(7, 7).piece.move(5,7)
        else:
            super().move(6, 0)
            cell.get_cell(7, 0).piece.move(5, 0)
    
    def castling_queenside(self):
        if self.team_bool:
            super().move(2, 7)
            cell.get_cell(0, 7).piece.move(3,7)
        else:
            super().move(2, 0)
            cell.get_cell(0, 0).piece.move(3, 0)
    
    def move(self, x, y):
        if abs(x - self.cell.grid_pos[0]) == 2:
            if x < self.cell.grid_pos[0]:
                self.castling_queenside()
            else:
                self.castling_kingside()
            
        else:
            super().move(x, y)

# Get a Row full of Pawns
def get_pawn_row() -> List[Piece]:
    """Return a list of pawns."""
    return [Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn]

def get_piece_row() -> List[Piece]:
    """Return a list of pieces in the order they spawn in."""
    return [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]