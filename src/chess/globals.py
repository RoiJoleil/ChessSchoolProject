player_turn = False

class ChessPieces:
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6

# this is to signal which color is the bottom row (start at row 6/7)
BOTTOMROW = True

class ChessTeam:
    WHITE = BOTTOMROW
    BLACK = not BOTTOMROW
    team = {
        True : WHITE,
        False: BLACK
    }
# Line 
class Territory:
    line = {
        True : 7,
        False: 0
    }