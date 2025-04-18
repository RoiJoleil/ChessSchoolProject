import pygame
from typing import List
from src.util.config import CellStyling, StartTable, PieceStyling
from src.util.config import CellStyling as CS
from src.util.config import PieceStyling as PS
from src.chess.cell import Cell
from src.chess.pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King

class ChessBoard:
    """Create the ChessBoard"""
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.cells: List[List[Cell]] = []
        self._initialise_cells()

        self.selected_cell = None
        self.players_turn = None

    def _initialise_cells(self):
        """Creates all the cells and rects upon first initialisation."""
        # Cell Config
        cell_size = CellStyling.CELL_SIZE
        cell_dark = CellStyling.CELL_DARK
        cell_light = CellStyling.CELL_LIGHT
        cell_border_color = CellStyling.CELL_BORDER_COLOR
        cell_border_width = CellStyling.CELL_BORDER_WIDTH

        # Start Config
        start_table = StartTable.TABLE

        for x in range(8):
            self.cells.append([])
            for y in range(8):
                # Create Tiles
                pos = (cell_size*x, cell_size*y)
                cell = Cell(self.screen, pos, cell_size, cell_size, x, y)
                if (x+y) % 2 == 0: # Dark
                    cell.set_styling(cell_dark, cell_border_color, cell_border_width)
                else: # Light
                    cell.set_styling(cell_light, cell_border_color, cell_border_width)
                cell.rect = pygame.rect.Rect(pos[0], pos[1], cell_size, cell_size)
                self.cells[x].append(cell)

                # Create Pieces
                piece = start_table[y][x]
                piece = piece.split(';')
                
                pos = (cell.c[0] - PS.PIECE_SIZE // 2, cell.c[1] - PS.PIECE_SIZE // 2)
                team_color = PS.PIECE_BLACK if piece[1] == 'B' else PS.PIECE_WHITE
                if piece[0] == 'P':
                    cell.piece = Pawn(self.screen, pos, PS.PIECE_SIZE, PS.PIECE_SIZE)
                    cell.piece.set_styling(PS.PAWN, team_color, PS.PIECE_BORDER_WIDTH)
                elif piece[0] == 'R':
                    cell.piece = Rook(self.screen, pos, PS.PIECE_SIZE, PS.PIECE_SIZE)
                    cell.piece.set_styling(PS.ROOK, team_color, PS.PIECE_BORDER_WIDTH)
                elif piece[0] == 'N':
                    cell.piece = Knight(self.screen, pos, PS.PIECE_SIZE, PS.PIECE_SIZE)
                    cell.piece.set_styling(PS.KNIGHT, team_color, PS.PIECE_BORDER_WIDTH)
                elif piece[0] == 'B':
                    cell.piece = Bishop(self.screen, pos, PS.PIECE_SIZE, PS.PIECE_SIZE)
                    cell.piece.set_styling(PS.BISHOP, team_color, PS.PIECE_BORDER_WIDTH)
                elif piece[0] == 'Q':
                    cell.piece = Queen(self.screen, pos, PS.PIECE_SIZE, PS.PIECE_SIZE)
                    cell.piece.set_styling(PS.QUEEN, team_color, PS.PIECE_BORDER_WIDTH)
                elif piece[0] == 'K':
                    cell.piece = King(self.screen, pos, PS.PIECE_SIZE, PS.PIECE_SIZE)
                    cell.piece.set_styling(PS.KING, team_color, PS.PIECE_BORDER_WIDTH)
                if cell.piece:
                    cell.piece.rect = pygame.rect.Rect(pos[0], pos[1], PS.PIECE_SIZE, PS.PIECE_SIZE)

    def is_occupied(self, cell: Cell = None, x: int = None, y: int = None) -> bool:
        """
        Returns a bool if the target cell is currently occupied.
        Either a Cell, or the Grid Position of the cell can be given.

        Args:
            cell (class): The Target Cell.
            x (int): X Grid Position.
            y (int): Y Grid Position
        """
        # Get the Cell if x and y is given.
        if x and y:
            cell = self.get_cell(x, y)

        return bool(cell.piece)
    
    def make_move(self, frm: Cell, to: Cell):
        """
        This method updates the necessary positions of the pieces involved.
        This method makes no validation checks if the move is actually valid.
        """
        if frm.piece:
            frm.piece.update_position(to.c)
        if to.piece:
            to.piece.update_position(frm.c)
        to.piece = frm.piece
        frm.piece = None

    def get_all_valid_moves(self):
        """
        A method to get all the valid moves with the current board state.
        This method will be used for bots if they are implemented
        """
        raise NotImplementedError()

    def get_valid_moves(self, cell: Cell) -> List[Cell]:
        """
        Return a list of valid Cells a piece can move to.
        Optionally:
            Implement a highlight on cells to visually help the user.
        """
        # TODO - Richard
        raise NotImplementedError()
    
    def is_valid_move(self) -> bool:
        """Check to make sure an attempted move is valid."""
        # TODO - Richard
        raise NotImplementedError()

    def convert_abs_coords_to_grid_coords(self, pos: tuple) -> tuple:
        """
        Turns the screen coordinates into grid coordinates.
        This method is used to identify what cells the user clicked on.
        """
        x, y = pos[0] // CS.CELL_SIZE, pos[1] // CS.CELL_SIZE
        return (x, y)

    def get_cell(self, x: int, y: int) -> Cell:
        """
        Return the Cell for the given board coordinates.
        """
        return self.cells[x][y]

    def select_cell(self, cell: Cell):
        """Selects a cell to do actions with. 'None' is also a valid argument."""
        self.selected_cell = cell

    def event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Leftclick Event
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = (mouse_pos[0], mouse_pos[1] - 50) # TODO: Actual implement logic for this... to lazy to do it right now
                x, y = self.convert_abs_coords_to_grid_coords(mouse_pos)
                cell = self.get_cell(x, y)

                # deselect cell by clicking on it again.
                if self.selected_cell == cell:
                    self.select_cell(None)
                # move piece if we have a cell selected.
                elif self.selected_cell:
                    self.make_move(self.selected_cell, cell)
                    self.select_cell(None)
                # select a cell if the clicked cell has a piece.
                elif cell.piece:
                    self.select_cell(cell)

    def draw(self):
        """Draw the individual chessboard cells"""
        for row_cells in self.cells:
            for cell in row_cells:
                cell.draw() # Draw Cells
                if isinstance(cell.piece, Piece):
                    cell.piece.draw() # Draw Pieces
        
    def __repr__(self):
        len_active_pieces = 0
        len_cells = 0
        for row_cells in self.cells:
            for cell in row_cells:
                if self.is_occupied(cell):
                    len_active_pieces += 1
                len_cells += 1
        header = f"[class '{self.__class__.__name__}' Information]"
        cells_info = f"(len_cells={len_cells}, len_pieces={len_active_pieces}, selected_cell={self.selected_cell})"
        return f"{header}\n{cells_info}\n"