"""
Pygame asset manager for loading and managing game graphics.

This module handles loading, storing, accessing and transforming game assets
(specifically PNG images for tiles and chess pieces) in a Pygame application.
"""
import os
import pygame
from typing import List
from src.settings import CELL_SIZE, PIECE_SIZE

CELL_PNG = "assets/cell"
PIECE_PNG = "assets/piece"
FOCUS_PNG = "assets/focus"

images = {} # {filename: loaded.pygame.image}
light_tiles = []
dark_tiles = []
white_pieces = []
black_pieces = []
tile_focus = []

def load_pngs(folder: str, width: int, height: int):
    global images
    pngs = [f for f in os.listdir(folder) if f.lower().endswith('.png') and os.path.isfile(os.path.join(folder, f))]
    for png in pngs:
        name, _ = os.path.splitext(png)
        path = os.path.join(folder, png)
        img_raw = pygame.image.load(path).convert_alpha()
        img_scaled = pygame.transform.smoothscale(img_raw, (width, height))
        images[name] = img_scaled

def rescale(image: pygame.Surface, width: int, height: int):
    return pygame.transform.smoothscale(image, (width, height))

def rescale_list(images: List[pygame.Surface], width: int, height: int):
    temp_list = []
    for image in images:
        tmp_img = pygame.transform.smoothscale(image, (width, height))
        temp_list.append(tmp_img)
    return temp_list

def get_pygame_images(keyword) -> List[pygame.Surface]:
    """Return a list of pygame.images with a keyword in them."""
    return [surface for name, surface in images.items() if keyword in name]

def get_pygame_image(name) -> pygame.Surface:
    """Return the loaded pygame.image"""
    if name not in images:
        raise ValueError(f"get_pygame_image Error:\nname - {name} - not in images")
    return images.get(name)

def init():
    global light_tiles, dark_tiles, white_pieces, black_pieces, tile_focus
    load_pngs(CELL_PNG, CELL_SIZE, CELL_SIZE)
    load_pngs(PIECE_PNG, PIECE_SIZE, PIECE_SIZE)
    load_pngs(FOCUS_PNG, CELL_SIZE, CELL_SIZE)

    light_tiles = get_pygame_images("light")
    dark_tiles = get_pygame_images("dark")
    white_pieces = get_pygame_images("white")
    black_pieces = get_pygame_images("black")
    tile_focus = get_pygame_images("focus")