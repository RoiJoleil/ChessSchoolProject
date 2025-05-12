from pygame_kit import Element, Click
from .chess.board import set_pieces_standard

start_game_button = Element(0, 0, 100, 50)
start_game_button.add_extension("click", Click(set_pieces_standard))