from src.settings import CELL_SIZE
from src.pngHandler import get_pygame_image as get_image


def convert_abs_coords_to_grid_coords(pos: tuple) -> tuple:
    """
    Turns the screen coordinates into grid coordinates.
    This method is used to identify what cells the user clicked on.
    """
    x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
    return (x, y)

class Move:
    def __init__(self, prev:tuple[int,int], next:tuple[int,int]):
        self.prev:tuple[int,int] = prev
        self.next:tuple[int,int] = next
    def __repr__(self):
        return f"prev: {self.prev}\tnext: {self.next}"