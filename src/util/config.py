"""Any BASE values"""
SCREEN_SIZE = (600, 650)

class ChessBoardSurface:
    x = 0
    y = 50
    w = 600
    h = 600

class CellStyling:
    CELL_LIGHT = (200, 120, 50)
    CELL_DARK = (100, 50, 20)
    CELL_BORDER_COLOR = (0, 0, 0)
    CELL_BORDER_WIDTH = 1
    CELL_SIZE = 75

class PieceStyling:
    PIECE_BLACK = (255, 255, 255)
    PIECE_WHITE = (0, 0, 0)
    PIECE_BORDER_WIDTH = 2
    PIECE_SIZE = 35
    PAWN = (0, 215, 215)
    ROOK = (215, 0, 0)
    BISHOP = (0, 215, 0)
    KNIGHT = (145, 25, 100)
    QUEEN = (255, 0, 255)
    KING = (255, 255, 0)

class StartTable:
    TABLE = [
        ['R;B','N;B','B;B','Q;B','K;B','B;B','N;B','R;B'],
        ['P;B','P;B','P;B','P;B','P;B','P;B','P;B','P;B'],
        ['X;X','X;X','X;X','X;X','X;X','X;X','X;X','X;X'],
        ['X;X','X;X','X;X','X;X','X;X','X;X','X;X','X;X'],
        ['X;X','X;X','X;X','X;X','X;X','X;X','X;X','X;X'],
        ['X;X','X;X','X;X','X;X','X;X','X;X','X;X','X;X'],
        ['P;W','P;W','P;W','P;W','P;W','P;W','P;W','P;W'],
        ['R;W','N;W','B;W','Q;W','K;W','B;W','N;W','R;W'],
    ]