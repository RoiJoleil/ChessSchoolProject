import pygame

class Piece:
    def __init__(self, screen: pygame.Surface, pos, w, h):
        # Positional Information
        self.pos = pos
        self.w = w
        self.h = h
        self.c = (pos[0] + w//2, pos[1] + h//2)

        # Styling Information
        self.background_color = (0, 0, 0)
        self.border_color = (0, 0, 0)
        self.border_width = 1

        # Gameplay Information
        self.screen = screen
        self.rect: pygame.rect.Rect = None

    def update_position(self, cell_c: tuple):
        """
        Updates the Piece information when it is being moved.
        
        Args:
            cell_c (tuple): The Center Position of the new cell its on.
        """
        self.pos = (cell_c[0] - self.w // 2, cell_c[1] - self.h // 2)
        self.c = cell_c
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def set_styling(self, background_color, border_color, border_width):
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width

    def draw(self):
        """
        TODO
        This is temporary until we replace them with actual .png files of the pieces
        """
        pygame.draw.rect(self.screen, self.background_color, self.rect) # Draw Background
        pygame.draw.rect(self.screen, self.border_color, self.rect, self.border_width) # Draw Border

    def __repr__(self):
        header = f"[class '{self.__class__.__name__}' Information]"
        positional_info = f"\t(pos={self.pos}, w={self.w}, h={self.h}, c={self.c})"
        styling_info = f"\t(background_color={self.background_color}, border_color={self.border_color}, border_width={self.border_width})"
        return f"{header}\n{positional_info}\n{styling_info}\n"
    
class Pawn(Piece):
    def __init__(self, screen, pos, w, h):
        super().__init__(screen, pos, w, h)

class Rook(Piece):
    def __init__(self, screen, pos, w, h):
        super().__init__(screen, pos, w, h)

class Knight(Piece):
    def __init__(self, screen, pos, w, h):
        super().__init__(screen, pos, w, h)

class Bishop(Piece):
    def __init__(self, screen, pos, w, h):
        super().__init__(screen, pos, w, h)

class Queen(Piece):
    def __init__(self, screen, pos, w, h):
        super().__init__(screen, pos, w, h)

class King(Piece):
    def __init__(self, screen, pos, w, h):
        super().__init__(screen, pos, w, h)