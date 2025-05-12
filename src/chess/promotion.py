import pygame
from src import pngHandler
from typing import List
from pygame_kit import Element, Icon, Click
from src.settings import SCREEN_SURFACE, CLOCK, FPS

def return_queen():
    return "Queen"

def return_rook():
    return "Rook"

def return_bishop():
    return "Bishop"

def return_knight():
    return "Knight"

def promotion_selection(team: str) -> str:
    """
    Creates a sub-loop to handle the Promotion.
    
    Args:
        team (str): 'white' or 'black'.
    """
    if team not in ['white', 'black']:
        raise ValueError(f"the variable team in {__name__}.promotion_selection needs to be either 'black' or 'white'.")

    buttons: List[Element] = []
    queen_button = Element(200, 200, 75, 75)
    queen_button.add_extension("icon", Icon(pngHandler.get_pygame_image(f"{team}-queen")))
    queen_button.add_extension("click", Click(return_queen))
    buttons.append(queen_button)

    rook_button = Element(300, 200, 75, 75)
    rook_button.add_extension("icon", Icon(pngHandler.get_pygame_image(f"{team}-rook")))
    rook_button.add_extension("click", Click(return_rook))
    buttons.append(rook_button)

    bishop_button = Element(200, 300, 75, 75)
    bishop_button.add_extension("icon", Icon(pngHandler.get_pygame_image(f"{team}-bishop")))
    bishop_button.add_extension("click", Click(return_bishop))
    buttons.append(bishop_button)

    knight_button = Element(300, 300, 75, 75)
    knight_button.add_extension("icon", Icon(pngHandler.get_pygame_image(f"{team}-knight")))
    knight_button.add_extension("click", Click(return_knight))
    buttons.append(knight_button)

    # Save the current screenbackground for drawing in this sub-loop
    chess_board = SCREEN_SURFACE.copy()

    sub_running = True
    while sub_running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sub_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in buttons:
                        if button.is_clicked(mouse_pos):
                            return button.update()

        overlay = pygame.Surface((600, 650), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        SCREEN_SURFACE.blit(chess_board, (0, 0))
        SCREEN_SURFACE.blit(overlay, (0, 0))

        for button in buttons:
            button.is_hovered(mouse_pos)
            button.draw(SCREEN_SURFACE)

        pygame.display.flip()
        
        CLOCK.tick(FPS)