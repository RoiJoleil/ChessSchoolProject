import pygame
from typing import List, Dict
from src.settings import CELL_SIZE
from src.settings import SCREEN_SIZE, CHESS_SURFACE_POSITION, CHESS_SURFACE_SIZE, FPS
from src.chess import cell, pieces
from src.chess import pieces

board_rect = None
board_surface =  None
selected_cell = None
player_turn = None
game_started = None

def init(screen: pygame.Surface):
    global board_rect, board_surface, player_turn, game_started
    player_turn = True
    board_rect = pygame.rect.Rect(CHESS_SURFACE_POSITION[0], CHESS_SURFACE_POSITION[1], CHESS_SURFACE_SIZE[0], CHESS_SURFACE_SIZE[1])
    board_surface = screen.subsurface(board_rect)
    game_started = False

def make_move(frm: cell.Cell, to: cell.Cell):
    """
    This method updates the necessary positions of the pieces involved.
    This method makes no validation checks if the move is actually valid.
    """
    global player_turn

    # Return if frm has no Piece
    if frm.piece == None:
        print(f"{__name__}: make_move failed as 'frm' has no Piece.")
        return
    
    # Return if its not our Turn
    if frm.piece.team != player_turn:
        print(f"{__name__}: make_move failed as its not '{player_turn}' Turn.")
        return
    
    # Return if its not a valid move
    if not frm.piece.is_valid_move(to):
        print(f"{__name__}: make_move failed as the attempted move is Invalid.")
        return
    
    # Move is successful and being made.
    cell.move_piece(frm=frm, to=to)
    toggle_player_turn()

def toggle_player_turn():
    global player_turn
    player_turn != player_turn

def set_player_turn(turn: bool):
    global player_turn
    player_turn = turn

def get_player_turn() -> bool:
    global player_turn
    return player_turn

def conclude_game():
    global game_started
    game_started = False

def start_game():
    """Starts a new Game"""
    global game_started
    cell.set_start_position()
    game_started = True

def load_game():
    """Load a saved Game"""
    global game_started
    game_started = True
    raise NotImplementedError()

def get_all_valid_moves() -> Dict[tuple, List[cell.Cell]]: 
    """
    A method to get all the valid moves with the current board state.
    This method will be used for bots if they are implemented
    """
    result = {}
    for x in range(0,8):
        for y in range(0,8):
            temp = get_cell(x, y)
            result[temp.grid_pos] = temp.piece.get_valid_moves()
    return result

def convert_abs_coords_to_grid_coords(pos: tuple) -> tuple:
    """
    Turns the screen coordinates into grid coordinates.
    This method is used to identify what cells the user clicked on.
    """
    x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
    return (x, y)

def get_cell(x: int, y: int) ->cell.Cell:
    """
    Return thecell.Cell for the given board coordinates.
    """
    return cell.get_cell(x, y)

def select_cell(selected:cell.Cell):
    """Selects a cell to do actions with. 'None' is also a valid argument."""
    global selected_cell
    selected_cell = selected
        
def event(event: pygame.event.Event):
    """Handle Click Events from the user"""
    global game_started
    # Return if the game hasnt started yet
    if not game_started:
        return
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1: # Leftclick Event
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0], mouse_pos[1] - 50) # TODO: Actual implement logic for this... to lazy to do it right now
            x, y = convert_abs_coords_to_grid_coords(mouse_pos)
            clicked_cell = get_cell(x, y)
            # deselect cell by clicking on it again.
            if selected_cell == clicked_cell:
                cell.set_focus([selected_cell], None)
                select_cell(None)
            # move piece if we have a cell selected.
            elif selected_cell:
                make_move(selected_cell, clicked_cell)
                cell.set_focus([selected_cell], None)
                select_cell(None)
            # select a cell if the clicked cell has a piece.
            elif clicked_cell.piece:
                select_cell(clicked_cell)
                cell.set_focus([selected_cell], "selected")
                cell.set_focus(clicked_cell.piece.get_valid_moves(), "move")
                
def draw():
    """Draw the individual chessboard cells"""
    global board_surface
    cell.draw(board_surface)
