def pow(x:int):
    return x * x

class IChessPiece:
    def legalMoveCord(oldX:int, oldY:int, newX:int, newY:int, occupiedCell:bool):
        pass
    def legalMoveStrPos(self, oldPos:str, newPos:str, occupiedCell:bool):
        return self.legalMoveCord(ord(oldPos[0].upper()), ord(oldPos[1].upper()), ord(newPos[0].upper()), ord(newPos[1].upper()), occupiedCell)

class Rook(IChessPiece):
    def legalMoveCord(oldX:int, oldY:int, newX:int, newY:int, occupiedCell:bool):
        return bool(oldX - newX) ^ bool(oldY - newY)
    def legalMoveStrPos(self, oldPos:str, newPos:str, occupiedCell:bool):
        return super().legalMoveStrPos(self, oldPos, newPos, occupiedCell)
    
class King(IChessPiece):
    def legalMoveCord(oldX:int, oldY:int, newX:int, newY:int, occupiedCell:bool):
        return 0 < pow(oldX - newX) + pow(oldY - newY) <= 2
    def legalMoveStrPos(self, oldPos:str, newPos:str, occupiedCell:bool):
        return super().legalMoveStrPos(self, oldPos, newPos, occupiedCell)

class Bishop(IChessPiece):
    def legalMoveCord(oldX:int, oldY:int, newX:int, newY:int, occupiedCell:bool):
        return pow(oldX - newX) == pow(oldY - newY) and pow(oldY - newY) > 0
    def legalMoveStrPos(self, oldPos:str, newPos:str, occupiedCell:bool):
        return super().legalMoveStrPos(self, oldPos, newPos, occupiedCell)
    
class Knight(IChessPiece):
    def legalMoveCord(oldX:int, oldY:int, newX:int, newY:int, occupiedCell:bool):
        return pow(oldX - newX) + pow(oldY - newY) == 5
    def legalMoveStrPos(self, oldPos:str, newPos:str, occupiedCell:bool):
        return super().legalMoveStrPos(self, oldPos, newPos, occupiedCell)
    
class Queen(IChessPiece):
    def legalMoveCord(oldX:int, oldY:int, newX:int, newY:int, occupiedCell:bool):
        if bool(oldX - newX ^ oldY - newY):
            return True
        return pow(oldX - newX) == pow(oldY - newY) and pow(oldY - newY) > 0
    def legalMoveStrPos(self, oldPos:str, newPos:str, occupiedCell:bool):
        return super().legalMoveStrPos(self, oldPos, newPos, occupiedCell)

class Pawn():
    def legalMoveCord(oldX:int, oldY:int, newX:int, newY:int, occupiedCell:bool):
        if occupiedCell:
            return abs(oldX - newX) == 1 and abs(oldY - newY) == 1
        elif abs(oldX - newX) > 0:
            return False
        else:
            return abs(oldY - newY) == 1
    def legalMoveStrPos(self, oldPos:str, newPos:str, occupiedCell:bool):
        return super().legalMoveStrPos(self, oldPos, newPos, occupiedCell)
