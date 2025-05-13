import pygame
from typing import List, Dict
from src.settings import CELL_SIZE
from src.settings import CHESS_SURFACE_POSITION, CHESS_SURFACE_SIZE
from src.globals import ChessTeam
from src.chess import cell, pieces
from src.chess.util import convert_abs_coords_to_grid_coords
from src.chess.cell import FocusType

board_rect = None
board_surface =  None
player_turn = None
game_started = None
selected_cell = None
valid_target_cells = []
start_replay_time = None

def init(screen: pygame.Surface):
    global board_rect, board_surface, player_turn, game_started
    player_turn = True
    board_rect = pygame.rect.Rect(CHESS_SURFACE_POSITION[0], CHESS_SURFACE_POSITION[1], CHESS_SURFACE_SIZE[0], CHESS_SURFACE_SIZE[1])
    board_surface = screen.subsurface(board_rect)
    game_started = False
    create_board()

def toggle_player_turn():
    global player_turn
    player_turn = not player_turn

def reset_game():
    """Reset Game"""
    global player_turn, game_started, selected_cell, valid_target_cells, start_replay_time
    set_start_position()
    cell.full_reset_focus()
    player_turn = True
    game_started = True
    selected_cell = None
    valid_target_cells = []
    start_replay_time = None
    cell.history = ""

def start_game():
    """Starts a new Game"""
    global game_started
    set_start_position()
    game_started = True

def load_game():
    """Load a saved Game"""
    global game_started
    game_started = True
    raise NotImplementedError()

def select_cell(selected: cell.Cell):
    """Selects a cell to do actions with. 'None' is also a valid argument."""
    global selected_cell
    selected_cell = selected

def reset_valid_target_cells():
    global valid_target_cells
    cell.set_focus(valid_target_cells, FocusType.MOVE, False)
    valid_target_cells = None

def set_valid_target_cells(cells: List[cell.Cell]):
    """This function handles the highlight of valid target cells"""
    global valid_target_cells
    valid_target_cells = cells
    cell.set_focus(valid_target_cells, FocusType.MOVE, True)

def create_board():
    """Create the initial board and all Cells"""
    for x in range(8):
        for y in range(8):
            screen_pos = (x * CELL_SIZE, y * CELL_SIZE)
            grid_pos = (x, y)
            cell.create_cell(screen_pos, grid_pos)

def set_start_position():
    """Sets the default start position"""
    for x in range(8):
        for y in range(8):
            team = ChessTeam.WHITE if bool(y // 4) else ChessTeam.BLACK
            # Pawn Rows
            if y in [1,6]:
                cell.set_piece(x, y, pieces.Pawn(None, team=team))
            # Nobility Row
            elif y in [0,7]:
                # Rooks
                if x in [0,7]:
                    cell.set_piece(x, y, pieces.Rook(None, team=team))
                # Knights
                if x in [1,6]:
                    cell.set_piece(x, y, pieces.Knight(None, team=team))
                # Bishops
                if x in [2,5]:
                    cell.set_piece(x, y, pieces.Bishop(None, team=team))
                # Queen
                if x == 3:
                    cell.set_piece(x, y, pieces.Queen(None, team=team))
                # King
                if x == 4:
                    cell.set_piece(x, y, pieces.King(None, team=team))
            else:
                cell.set_piece(x, y, None)

def replay_history(delay: float = 1.2):
    pass

def make_move(frm: cell.Cell, to: cell.Cell) -> bool:
    """
    This method updates the necessary positions of the pieces involved.
    This method makes no validation checks if the move is actually valid.

    Returns:
        A boolean value if the move was made.
    """
    global player_turn

    if start_replay_time:
        return False
    
    # Return if frm has no Piece
    if frm.piece == None:
        print(f"{__name__}: make_move failed as 'frm' has no Piece.")
        return False
    
    # Return if its not our Turn
    if frm.piece.team != player_turn:
        print(f"{__name__}: make_move failed as its not '{player_turn}' Turn.")
        return False
    
    # Return if its not a valid move
    if not frm.piece.is_valid_move(to):
        print(f"{__name__}: make_move failed as the attempted move is Invalid.")
        return False
    
    # Move is successful and being made.
    cell.move_piece(frm=frm, to=to)
    toggle_player_turn()
    return True

def event(event: pygame.event.Event):
    """Handle Click Events from the user"""
    global game_started
    # Return if the game hasnt started yet
    if not game_started:
        return
    if not pygame.key.get_focused():
        return
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1: # Leftclick Event
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0], mouse_pos[1] - 50) # TODO: Actual implement logic for this... to lazy to do it right now
            x, y = convert_abs_coords_to_grid_coords(mouse_pos)
            clicked_cell = cell.get_cell(x, y)
            if clicked_cell: # TODO: Temporary sollution to avoid crashing when we click outside of the board
                # deselect cell by clicking on it again.
                if selected_cell == clicked_cell:
                    cell.set_focus([selected_cell], FocusType.SELECTED, False)
                    reset_valid_target_cells()
                    select_cell(None)
                # move piece if we have a cell selected.
                elif selected_cell:
                    cell.set_focus([selected_cell], FocusType.SELECTED, False)
                    reset_valid_target_cells()
                    cell.prev_move_unfocus()
                    make_move(selected_cell, clicked_cell)
                    cell.prev_move_focus()
                    select_cell(None)
                # select a cell if the clicked cell has a piece.
                elif clicked_cell.piece:
                    select_cell(clicked_cell)
                    cell.set_focus([selected_cell], FocusType.SELECTED, True)
                    set_valid_target_cells(clicked_cell.piece.get_valid_moves())
        # Debug Tool to check contents of a cell with middle mouse click
        elif event.button == 3:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0], mouse_pos[1] - 50) # TODO: Actual implement logic for this... to lazy to do it right now
            x, y = convert_abs_coords_to_grid_coords(mouse_pos)
            print(cell.get_cell(x, y))
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_INSERT:
            replay_history()

def draw():
    """Draw the individual chessboard cells"""
    global board_surface
    cell.draw(board_surface)
