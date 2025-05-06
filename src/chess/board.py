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

        self._initialise_cells()

        self.selected_cell:cell.Cell = None
        self.players_turn:bool = True

    def _initialise_cells(self):
        """Creates all the cells and rects upon first initialisation."""
        # Create Cells
        cell.init_standard_board()

    def get_current_turn() -> bool:
        global current_turn
        return current_turn

    def set_current_turn(turn:bool):
        global current_turn
        # This Function does nothing ??? - Joel
        current_turn = turn
    
    def make_move(self, frm:cell.Cell, to:cell.Cell):
        """
        This method updates the necessary positions of the pieces involved.
        This method makes no validation checks if the move is actually valid.
        """

        # I dont know what is going on here, but its to much.
        # Having 100 lines of code for a single function is way to much.
        # All the seperate pieces in this function have to be seperated into their own function with descriptives
        # Names so its easier understandable what is actually going on. - Joel

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

    def select_cell(self, selected:cell.Cell):
        """Selects a cell to do actions with. 'None' is also a valid argument."""
        self.selected_cell = selected
            

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
                    cell.set_focus(clicked_cell.piece.get_valid_moves(), "prev")
                    

    def draw(self):
        """Draw the individual chessboard cells"""
        cell.draw(self.screen)
        
    def __repr__(self):
        """NotImplemented"""
        pass