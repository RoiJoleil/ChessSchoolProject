import pygame
from pygame_kit import Element, Click, Background, Text
from .chess.board import reset_game

start_game_button = Element(0, 0, 100, 50)
start_game_button.add_extension("click", Click(reset_game))
start_game_button.add_extension("background", Background((55, 55, 55), (255, 255, 255), 2, 1))
start_game_button.add_extension("text", Text("Neustart", pygame.Font(None, 20), pygame.Color(255, 255, 255)))