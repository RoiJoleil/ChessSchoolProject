from src.settings import CELL_SIZE

def convert_abs_coords_to_grid_coords(pos: tuple) -> tuple:
    """
    Turns the screen coordinates into grid coordinates.
    This method is used to identify what cells the user clicked on.
    """
    x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
    return (x, y)
