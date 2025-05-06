import pygame
from typing import List, Dict
from src.settings import CELL_SIZE
from src.chess import cell, pieces
from src.chess import pieces

"""
I cant refactor this file, as there is so much here that shouldnt be here.
I would need to effectivly rewrite your entire code to do it. - Joel
"""

current_turn = True # Why??? we have self.players_turn - Joel

class Board:
    """Create the ChessBoard"""
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.white_king = None
        self.black_king = None
        self._initialise_cells()

        self.selected_cell = None
        self.players_turn = None

    def _initialise_cells(self):
        """Creates all the cells and rects upon first initialisation."""
        set_board_position()

        self.white_king = self.get_cell(4,0).piece
        self.black_king = self.get_cell(4,7).piece

    def get_current_turn() -> bool:
        global current_turn
        return current_turn

    def set_current_turn(turn:bool):
        global current_turn
        # This Function does nothing ??? - Joel
        if turn:
            current_turn = turn

    def make_move(self, frm:cell.Cell, to:cell.Cell):
        """
        This method updates the necessary positions of the pieces involved.
        This method makes no validation checks if the move is actually valid.
        """

        if frm.piece == None:
            return
#        global current_turn
#        if frm.piece.team != current_turn:
#            return
        
        if not frm.piece.is_valid_move(to):
            return
        
        cell.move_piece(frm=frm, to=to)

#        current_turn = not current_turn

    def get_all_valid_moves(self) -> Dict[tuple, List[cell.Cell]]: 
        """
        A method to get all the valid moves with the current board state.
        This method will be used for bots if they are implemented
        """
        result = {}
        for x in range(0,8):
            for y in range(0,8):
                temp = self.get_cell(x, y)
                result[temp.grid_pos] = temp.piece.get_valid_moves()
        return result
    
    def is_valid_move(self, curr:cell.Cell, dest:cell.Cell) -> bool:
        """Check to make sure an attempted move is valid."""
        if isinstance(curr.piece,(pieces.Pawn, pieces.Knight)):
            return curr.piece.is_valid_position(curr.grid_pos, dest.grid_pos, dest.piece.identity if dest.piece else 0)
        
        if isinstance(curr.piece, pieces.King):
            if self.in_check(dest, curr.piece.team):
                return False
            if dest.grid_pos in curr.piece.castling:
                return True
            return curr.piece.is_valid_position(curr.grid_pos, dest.grid_pos, dest.piece.team if dest.piece else 0)
            
        elif curr.piece:
            if not curr.piece.is_valid_position(curr.grid_pos, dest.grid_pos, dest.piece.identity if dest.piece else 0):
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
        x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
        return (x, y)

    def get_cell(self, x: int, y: int) ->cell.Cell:
        """
        Return thecell.Cell for the given board coordinates.
        """
        return cell.get_cell(x, y)

    def select_cell(self, cell:cell.Cell):
        """Selects a cell to do actions with. 'None' is also a valid argument."""
        self.selected_cell = cell

    def event(self, event: pygame.event.Event):
        """Handle Click Events from the user"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Leftclick Event
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = (mouse_pos[0], mouse_pos[1] - 50) # TODO: Actual implement logic for this... to lazy to do it right now
                x, y = self.convert_abs_coords_to_grid_coords(mouse_pos)
                clicked_cell = self.get_cell(x, y)
                # deselect cell by clicking on it again.
                if self.selected_cell == clicked_cell:
                    cell.set_focus([self.selected_cell], None)
                    self.select_cell(None)
                # move piece if we have a cell selected.
                elif self.selected_cell:
                    self.make_move(self.selected_cell, clicked_cell)
                    cell.set_focus([self.selected_cell], None)
                    self.select_cell(None)
                # select a cell if the clicked cell has a piece.
                elif clicked_cell.piece:
                    self.select_cell(clicked_cell)
                    cell.set_focus([self.selected_cell], "selected")
                    
    def draw(self):
        """Draw the individual chessboard cells"""
        cell.draw(self.screen)
        
    def __repr__(self):
        """NotImplemented"""
        pass

# API
def set_board_position():
        # Create Cells
    for x in range(8):
        for y in range(8):
            pos = (x * CELL_SIZE, y * CELL_SIZE)
            cell.create_cell(pos, x, y)
    
    piece_row = pieces.get_piece_row()
    pawn_row = pieces.get_pawn_row()
    for x in range(8):
        # get each Row which will contain pieces
        cell_black_piece = cell.cells[(x, 0)]
        cell_black_pawn = cell.cells[(x, 1)]
        cell_white_pawn = cell.cells[(x, 6)]
        cell_white_piece = cell.cells[(x, 7)]
        # place pieces
        cell_black_piece.set_piece(piece_row[x](cell=cell_black_piece, team=False))
        cell_black_pawn.set_piece(pawn_row[x](cell=cell_black_pawn, team=False))
        cell_white_pawn.set_piece(pawn_row[x](cell=cell_white_pawn, team=True))
        cell_white_piece.set_piece(piece_row[x](cell=cell_white_piece, team=True))

def load_board_position():
    pass