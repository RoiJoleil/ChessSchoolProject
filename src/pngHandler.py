import os
import pygame

CELL_PNG = "assets/cell"
PIECE_PNG = "assets/piece"

images = {} # {filename: loaded.pygame.image}
light_tiles = []
dark_tiles = []
white_pieces = []
black_pieces = []

def load_pngs(folder: str):
    global images
    pngs = [f for f in os.listdir(folder) if f.lower().endswith('.png') and os.path.isfile(os.path.join(folder, f))]
    for png in pngs:
        name, _ = os.path.splitext(png)
        path = os.path.join(folder, png)
        images[name] = pygame.image.load(path).convert_alpha()

def rescale(image: pygame.Surface, width: int, height: int):
    return pygame.transform.smoothscale(image, (width, height))

def get_pygame_images(keyword):
    """Return a list of pygame.images with a keyword in them."""
    return [surface for name, surface in images.items() if keyword in name]

def get_pygame_image(name):
    """Return the loaded pygame.image"""
    if name not in images:
        raise ValueError(f"get_pygame_image Error:\nname - {name} - not in images")
    return images.get(name)

def init():
    global light_tiles, dark_tiles, white_pieces, black_pieces
    load_pngs(CELL_PNG)
    load_pngs(PIECE_PNG)
    light_tiles = get_pygame_images("light")
    dark_tiles = get_pygame_images("dark")
    white_pieces = get_pygame_images("white")
    black_pieces = get_pygame_images("black")