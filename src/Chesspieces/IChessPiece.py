class IChessPiece:
    def legalMove(oldX:int, oldY:int, newX:int, newY:int):
        pass
    def legalMove(oldPos:str, newPos:str):
        pass

class Rook(IChessPiece):
    def legalMove(oldX:int, oldY:int, newX:int, newY:int):
        return bool(oldX - newX ^ oldY - newY)
    def legalMove(oldPos:str, newPos:str):
        return bool(oldPos[0] - newPos[0] ^ oldPos[1] - newPos[1])

class King(IChessPiece):
    def legalMove(oldX:int, oldY:int, newX:int, newY:int):
        return (oldX - newX) * (oldX - newX) + (oldY - newY) * (oldY - newY) <= 2
    def legalMove(oldPos, newPos):
        return (oldPos[0] - newPos[0]) * (oldPos[0] - newPos[0]) + (oldPos[1] - newPos[1]) * (oldPos[1] - newPos[1]) <= 2

class Bishop(IChessPiece):
    def legalMove(oldX:int, oldY:int, newX:int, newY:int):
        return (oldX - newX) * (oldX - newX) == (oldY - newY) * (oldY - newY)
    def legalMove(oldPos, newPos):
        return (oldPos[0] - newPos[0]) * (oldPos[0] - newPos[0]) == (oldPos[1] - newPos[1]) * (oldPos[1] - newPos[1])
    
class Knight(IChessPiece):
    def legalMove(oldX:int, oldY:int, newX:int, newY:int):
        return (oldX - newX) * (oldX - newX) + (oldY - newY) * (oldY - newY) == 5
    def legalMove(oldPos, newPos):
        return (oldPos[0] - newPos[0]) * (oldPos[0] - newPos[0]) + (oldPos[1] - newPos[1]) * (oldPos[1] - newPos[1]) == 5
    
class Queen(IChessPiece):
    def legalMove(oldX:int, oldY:int, newX:int, newY:int):
        if bool(oldX - newX ^ oldY - newY):
            return True
        return (oldX - newX) * (oldX - newX) == (oldY - newY) * (oldY - newY)
    def legalMove(oldPos, newPos):
        if bool(oldPos[0] - newPos[0] ^ oldPos[1] - newPos[1]):
            return True
        return (oldPos[0] - newPos[0]) * (oldPos[0] - newPos[0]) == (oldPos[1] - newPos[1]) * (oldPos[1] - newPos[1])
class Pawn():
    def legalMove(oldX:int, oldY:int, newX:int, newY:int, occupiedTile:bool):
        if occupiedTile:
            return abs(oldX - newX) == 1 and abs(oldY - newY) == 1
        elif abs(oldX - newX) > 0:
            return False
        else:
            return abs(oldY - newY) == 1

    def legalMove(oldPos:str, newPos:str, occupiedTile:bool):
        if occupiedTile:
            return abs(oldPos[0] - newPos[0]) == 1 and abs(oldPos[1] - newPos[1]) == 1
        elif abs(oldPos[0] - newPos[0]) > 0:
            return False
        else:
            return abs(oldPos[1] - newPos[1]) == 1

    
