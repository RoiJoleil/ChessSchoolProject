import pygame
from typing import List
from src.util.config import CellStyling, StartTable, PieceStyling
from src.util.config import CellStyling as CS
from src.util.config import PieceStyling as PS
from src.chess.pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King
from src.chess import cell
from src.chess import pieces

class ChessBoard:
    """Create the ChessBoard"""
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self._initialise_cells()

        self.selected_cell = None
        self.players_turn = None
        self.current_turn = False
        self.en_passante = None # if en passante is possible it will have a tuple of the coordinate of possible on passante

    def _initialise_cells(self):
        """Creates all the cells and rects upon first initialisation."""
        # Create Cells
        for x in range(8):
            for y in range(8):
                pos = (x * cell.CELL_SIZE, y * cell.CELL_SIZE)
                cell.create_cell(pos, x, 7-y)
        
        piece_row = pieces.get_piece_row()
        pawn_row = pieces.get_pawn_row()
        for x in range(8):
            cell_black_piece = cell.cells[(x, 7)]
            cell_black_pawn = cell.cells[(x, 6)]
            cell_white_pawn = cell.cells[(x, 1)]
            cell_white_piece = cell.cells[(x, 0)]
            cell_black_piece.set_piece(piece_row[x](cell=cell_black_piece, team=False))
            cell_black_pawn.set_piece(pawn_row[x](cell=cell_black_pawn, team=False))
            cell_white_pawn.set_piece(pawn_row[x](cell=cell_white_pawn, team=True))
            cell_white_piece.set_piece(piece_row[x](cell=cell_white_piece, team=True))

    def is_occupied(self, cell: cell.Cell = None, x: int = None, y: int = None) -> bool:
        """
        Returns a bool if the target cell is currently occupied.
        Either acell.Cell, or the Grid Position of the cell can be given.

        Args:
            cell (class): The Targetcell.Cell.
            x (int): X Grid Position.
            y (int): Y Grid Position
        """
        # Get thecell.Cell if x and y is given.
        if x and y:
            cell = self.get_cell(x, y)

        return bool(cell.piece)
    
    def make_move(self, frm:cell.Cell, to:cell.Cell):
        """
        This method updates the necessary positions of the pieces involved.
        This method makes no validation checks if the move is actually valid.
        """
        if frm.piece == None:
            return
        if frm.piece.team // 8 == self.current_turn:
            return
        if not self.is_valid_move(frm, to):
            return
        cell.move_piece(frm=frm, to=to)
        self.current_turn = not self.current_turn

    def get_all_valid_moves(self):
        """
        A method to get all the valid moves with the current board state.
        This method will be used for bots if they are implemented
        """
        raise NotImplementedError()
    
    def signOfNumber(self, number):
        if number == 0:
            return 0
        return 1 if number > 0 else -1
    
    def get_valid_moves(self, curr:cell.Cell) -> List[cell.Cell]:
        """
        Return a list of valid Cells a piece can move to.
        Optionally:
            Implement a highlight on cells to visually help the user.
        """
        raise NotImplementedError()
    
    def is_valid_move(self, curr:cell.Cell, dest:cell.Cell) -> bool:
        """Check to make sure an attempted move is valid."""
        if isinstance(curr.piece, Pawn):
            # En Passante not implemented
            if curr.piece.team // 8:
                if curr.grid_pos[1] == 6 and dest.grid_pos[1] == 4:
                    if curr.grid_pos[0] != dest.grid_pos[0]:
                        return False
                    
                    if (
                        self.get_cell(curr.grid_pos[0], 5).piece == None and
                        self.get_cell(curr.grid_pos[0], 4).piece == None
                        ):
                        self.en_passante = (curr.grid_pos[0], 5)
                        return True
                else:
                    return curr.piece.is_valid_position(curr.grid_pos, dest.grid_pos, dest.piece.team if dest.piece != None else 0)
            else:
                if curr.grid_pos[1] == 1 and dest.grid_pos[1] == 3:
                    if curr.grid_pos[0] != dest.grid_pos[0]:
                        return False
                    if (
                        self.get_cell(curr.grid_pos[0], 2).piece == None and
                        self.get_cell(curr.grid_pos[0], 3).piece == None):
                        self.en_passante = (curr.grid_pos[0], 2)
                else:
                    if self.en_passante:
                        if dest.grid_pos[0] == self.en_passante[0] and dest.grid_pos[0] == self.en_passante[0]:
                            return curr.piece.is_valid_position(curr.grid_pos, dest.grid_pos, self.get_cell(curr) if dest.piece != None else 0)
                    else:
                        return curr.piece.is_valid_position(curr.grid_pos, dest.grid_pos, dest.piece.team if dest.piece != None else 0)

        elif isinstance(curr.piece,(King, Knight)):
            return curr.piece.is_valid_position(curr.grid_pos, dest.grid_pos, dest.piece.team if dest.piece != None else 0)
        
        elif curr.piece != None:
            if not curr.piece.is_valid_position(curr.grid_pos, dest.grid_pos, dest.piece.team if dest.piece != None else 0):
                return False
            diff = (self.signOfNumber(dest.grid_pos[0] - curr.grid_pos[0]), self.signOfNumber(dest.grid_pos[1] - curr.grid_pos[1]))
            for i in range(1,8):
                if (curr.grid_pos[0] + diff[0] * i == dest.grid_pos[0]) and (curr.grid_pos[1] + diff[1] * i == dest.grid_pos[1]) :
                    return True
                if self.get_cell(curr.grid_pos[0] + diff[0] * i, curr.grid_pos[1] + diff[1] * i).piece != None:
                    return False
        else:
            return False

    def convert_abs_coords_to_grid_coords(self, pos: tuple) -> tuple:
        """
        Turns the screen coordinates into grid coordinates.
        This method is used to identify what cells the user clicked on.
        """
        x, y = pos[0] // CS.CELL_SIZE, pos[1] // CS.CELL_SIZE
        return (x, y)

    def get_cell(self, x: int, y: int) ->cell.Cell:
        """
        Return thecell.Cell for the given board coordinates.
        """
        return cell.get_cell((x, y))

    def select_cell(self, cell:cell.Cell):
        """Selects a cell to do actions with. 'None' is also a valid argument."""
        self.selected_cell = cell

    def event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Leftclick Event
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = (mouse_pos[0], mouse_pos[1] - 50) # TODO: Actual implement logic for this... to lazy to do it right now
                print(f"Mouse Pos: {mouse_pos}")
                x, y = self.convert_abs_coords_to_grid_coords(mouse_pos)
                print(f"x/y: {(x, y)}")
                cell = self.get_cell(x, y)
                print(f"Cell: {cell}")

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
        cell.draw(self.screen)
        
    def __repr__(self):
        """NotImplemented"""
        pass