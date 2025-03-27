def pow(x:int):
    return x * x

class IChessPiece:
    def legalMoveCord(oldX:int, oldY:int, newX:int, newY:int):
        pass
    def legalMoveStrPos(self, oldPos:str, newPos:str):
        return self.legalMoveCord(ord(oldPos[0].upper()), ord(oldPos[1].upper()), ord(newPos[0].upper()), ord(newPos[1].upper()))

class Rook(IChessPiece):
    def legalMoveCord(oldX:int, oldY:int, newX:int, newY:int):
        return bool(oldX - newX ^ oldY - newY)
    def legalMoveStrPos(self, oldPos:str, newPos:str):
        return super().legalMoveStrPos(self, oldPos, newPos)
    
class King(IChessPiece):
    def legalMoveCord(oldX:int, oldY:int, newX:int, newY:int):
        return 0 < pow(oldX - newX) + pow(oldY - newY) <= 2
    def legalMoveStrPos(self, oldPos:str, newPos:str):
        return super().legalMoveStrPos(self, oldPos, newPos)

class Bishop(IChessPiece):
    def legalMoveCord(oldX:int, oldY:int, newX:int, newY:int):
        return pow(oldX - newX) == pow(oldY - newY) and pow(oldY - newY) > 0
    def legalMoveStrPos(self, oldPos:str, newPos:str):
        return super().legalMoveStrPos(self, oldPos, newPos)
    
class Knight(IChessPiece):
    def legalMoveCord(oldX:int, oldY:int, newX:int, newY:int):
        return pow(oldX - newX) + pow(oldY - newY) == 5
    def legalMoveStrPos(self, oldPos:str, newPos:str):
        return super().legalMoveStrPos(self, oldPos, newPos)
    
class Queen(IChessPiece):
    def legalMoveCord(oldX:int, oldY:int, newX:int, newY:int):
        if bool(oldX - newX ^ oldY - newY):
            return True
        return pow(oldX - newX) == pow(oldY - newY) and pow(oldY - newY) > 0
    def legalMoveStrPos(self, oldPos:str, newPos:str):
        return super().legalMoveStrPos(self, oldPos, newPos)

class Pawn():
    def legalMoveCord(oldX:int, oldY:int, newX:int, newY:int, occupiedTile:bool):
        if occupiedTile:
            return abs(oldX - newX) == 1 and abs(oldY - newY) == 1
        elif abs(oldX - newX) > 0:
            return False
        else:
            return abs(oldY - newY) == 1
    def legalMoveStrPos(self, oldPos:str, newPos:str):
        return super().legalMoveStrPos(self, oldPos, newPos)
