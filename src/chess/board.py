import pygame
from typing import List, Dict
from src.settings import CELL_SIZE
from src.chess import cell, pieces
from src.chess import pieces

"""
I cant refactor this file, as there is so much here that shouldnt be here.
I would need to effectivly rewrite your entire code to do it. - Joel
"""

# This cass shouldnt be here.
# What is this class doing exactly? - Joel
class En_Passante:
    def __init__(self):
        self.checkPos = None
        self.piecePos = None
        self.team = False
        self.active = 0

    def set(self, piecePos:tuple = None, team:bool = False, active = 1):
        self.piecePos = (piecePos[0], piecePos[1])
        self.team = team
        self.active = active
        if self.team:
            self.checkPos = (self.piecePos[0], 5)
        else:
            self.checkPos = (self.piecePos[0], 2)

    def reset(self):
        self.checkPos = None
        self.piecePos = None
        self.active = 0

    def __repr__(self):
        header = f"[class '{self.__class__.__name__}' Information]"
        positionalInfo = f" toCheck={self.checkPos}\tpiecePos={self.piecePos}"
        otherInfo = f" team={self.team}"
        return f"{header}\n{positionalInfo}\n{otherInfo}\n"
    
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
        self.en_passante = En_Passante()

    def _initialise_cells(self):
        """Creates all the cells and rects upon first initialisation."""
        # Create Cells
        for x in range(8):
            for y in range(8):
                pos = (x * cell.CELL_SIZE, y * cell.CELL_SIZE)
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

        # I dont know what is going on here, but its to much.
        # Having 100 lines of code for a single function is way to much.
        # All the seperate pieces in this function have to be seperated into their own function with descriptives
        # Names so its easier understandable what is actually going on. - Joel

        if frm.piece == None:
            return
        global current_turn
        if frm.piece.team != current_turn:
            return
        if isinstance(frm.piece,pieces.Pawn):
            oui_passante = False
            if self.en_passante.active:
                if to.grid_pos[0] == self.en_passante.checkPos[0] and to.grid_pos[1] == self.en_passante.checkPos[1]:
                    print(f"make_move en passante oppurtunity\ndest:\n{to}\n{self.en_passante}")
                    if not frm.piece.is_valid_position(frm.grid_pos, to.grid_pos, 1 + self.en_passante.team * 8):
                        return
                    else:
                        self.get_cell(self.en_passante.piecePos[0],self.en_passante.piecePos[1]).set_piece()
                        oui_passante = True
                        self.en_passante.reset()
                        
            if not oui_passante:
                if frm.piece.team:
                    if frm.grid_pos[1] == 6 and to.grid_pos[1] == 4 and frm.grid_pos[0] == to.grid_pos[0]:
                        if (
                            self.get_cell(frm.grid_pos[0], 5).piece == None and
                            self.get_cell(frm.grid_pos[0], 4).piece == None
                            ):
                            self.en_passante.set(to.grid_pos, frm.piece.team)
                    elif not self.is_valid_move(frm, to):
                        return
            
                else:
                    if frm.grid_pos[1] == 1 and to.grid_pos[1] == 3 and frm.grid_pos[0] == to.grid_pos[0]:
                        if (
                            self.get_cell(frm.grid_pos[0], 2).piece == None and
                            self.get_cell(frm.grid_pos[0], 3).piece == None
                            ):
                            self.en_passante.set(to.grid_pos, frm.piece.team)
                    elif not self.is_valid_move(frm, to):
                        return
        
        elif not self.is_valid_move(frm, to):
            return
        if isinstance(frm.piece, pieces.Rook):
            if frm.piece.team:
                if self.white_king.castling:
                    if(frm.grid_pos[0] == 0,frm.grid_pos[0] == 0):
                        if((2,0) in self.white_king.castling):
                            self.white_king.castling.remove(2,0)
                    if(frm.grid_pos[0] == 7,frm.grid_pos[0] == 0):
                        if((6,0) in self.white_king.castling):
                            self.white_king.castling.remove(6,0)
            else:
                if self.black_king.castling:
                    if(frm.grid_pos[0] == 0,frm.grid_pos[0] == 7):
                        if((2,7) in self.black_king.castling):
                            self.black_king.castling.remove(2,7)
                    if(frm.grid_pos[0] == 7,frm.grid_pos[0] == 7):
                        if((6,7) in self.black_king.castling):
                            self.black_king.castling.remove(6,7)

        elif isinstance(frm.piece, pieces.King):
            if frm.piece.team:
                if self.white_king.castling:
                    self.white_king.castling = None
            else:
                if self.black_king.castling:
                    self.black_king.castling = None
            
        cell.move_piece(frm=frm, to=to)

        # reset en Passante after oppurtunity for it
        if self.en_passante.active > 1:
            self.en_passante.reset()
        if self.en_passante.active == 1:
            self.en_passante.active = 2
        # switch turn
        current_turn = not current_turn

    def get_all_valid_moves(self) -> Dict[tuple, List[cell.Cell]]: 
        """
        A method to get all the valid moves with the current board state.
        This method will be used for bots if they are implemented
        """
        result = {}
        for x in range(0,8):
            for y in range(0,8):
                temp = self.get_cell(x, y)
                result[temp.grid_pos] = self.get_valid_moves(temp)
        return result

    def in_check(self, curr:cell.Cell, team:bool) -> bool:
        #beware of recursions
        for x in range(0, 8):
            for y in range(0,8):
                threat = self.get_cell(x, y)
                if threat.piece if threat else False:
                    if (threat.piece.is_valid_position(threat.grid_pos, curr.grid_pos, team)):
                        return True
        return False

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
        if curr.piece == None:
            return []
        result = []

        if isinstance(curr.piece,pieces.Pawn):
            # singular step forward
            for i in range(-1, 2):
                dest = self.get_cell(curr.grid_pos[0] + i, curr.grid_pos[1] + (1 if curr.piece.team else -1))
                if dest == None:
                    continue
                if curr.piece.is_valid_position(curr.grid_pos, dest.grid_pos, dest.piece.identity if dest.piece else 0):
                    result.append(dest)
            dest = self.get_cell(curr.grid_pos[0], curr.grid_pos[1] + 2 *(1 if curr.piece.team else -1))
            # double step forward
            if dest:
                if curr.piece.is_valid_position(curr.grid_pos, dest.grid_pos, dest.piece.identity if dest.piece else 0):
                    result.append(dest)

        elif isinstance(curr.piece, pieces.Rook):
            for i in [-1,1]:
                temp = self.get_cell(curr.grid_pos[0] + i, curr.grid_pos[1])
                while temp:
                    if not curr.piece.is_valid_position(curr.grid_pos, temp.grid_pos, temp.piece.identity if temp.piece else 0):
                        break
                    result.append(temp)
                    temp = self.get_cell(curr.grid_pos[0] + i, curr.grid_pos[1])
                temp = self.get_cell(curr.grid_pos[0], curr.grid_pos[1] + i)
                while temp:
                    if not curr.piece.is_valid_position(curr.grid_pos, temp.grid_pos, temp.piece.identity if temp.piece else 0):
                        break
                    result.append(temp)
                    temp = self.get_cell(curr.grid_pos[0], curr.grid_pos[1] + i)

        elif isinstance(curr.piece, pieces.Knight):
            for i in [-1, 1]:
                for j in [-2, 2]:
                    temp = self.get_cell(curr.grid_pos[0] + i, curr.grid_pos[1] + j)
                    if temp == None:
                        continue
                    if curr.piece.is_valid_position(curr.grid_pos, temp.grid_pos, temp.piece.identity if temp.piece else 0):
                        result.append(temp)
                    temp = self.get_cell(curr.grid_pos[0] + j, curr.grid_pos[1] + i)
                    if temp == None:
                        continue
                    if curr.piece.is_valid_position(curr.grid_pos, temp.grid_pos, temp.piece.identity if temp.piece else 0):
                        result.append(temp)

        elif isinstance(curr.piece, pieces.Bishop):
            for i in [-1, 1]:
                for j in [-1, 1]:
                    temp = self.get_cell(curr.grid_pos[0] + i, curr.grid_pos[1] + j)
                    while temp:
                        if not curr.piece.is_valid_position(curr.grid_pos, temp.grid_pos, temp.piece.identity if temp.piece else 0):
                            break
                        result.append(temp)
                        temp = self.get_cell(curr.grid_pos[0] + i, curr.grid_pos[1] + j)

        elif isinstance(curr.piece, pieces.Queen):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    temp = self.get_cell(curr.grid_pos[0] + i,curr.grid_pos[1] + j)
                    while temp:
                        if not curr.piece.is_valid_position(curr.grid_pos, temp.grid_pos, temp.piece.identity if temp.piece else 0):
                            break
                        result.append(temp)
                        temp = self.get_cell(curr.grid_pos[0] + i,curr.grid_pos[1] + j)

        elif isinstance(curr.piece, pieces.King):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    temp = self.get_cell(curr.grid_pos[0] + i,curr.grid_pos[1] + j)
                    if temp:
                        continue
                    if curr.piece.is_valid_position(curr.grid_pos, temp.grid_pos, temp.piece.identity if temp.piece else 0):
                        result.append(temp)
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