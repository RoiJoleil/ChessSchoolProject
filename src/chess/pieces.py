import pygame

class Piece:
    def __init__(self, screen: pygame.Surface, pos, w, h, isBlack:bool):
        # Positional Information
        self.pos = pos # position on screen
        self.w = w # width of piece
        self.h = h # height of piece
        self.c = (pos[0] + w//2, pos[1] + h//2) # center of Piece 
        self.isBlack = isBlack # which team the Piece is
        
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
        team_info = "Schwarz" if self.isBlack else "Weiß"
        return f"{header}\n{positional_info}\n{styling_info}\n"
    
    def is_valid_position(self, curr:tuple, dest:tuple, pieceInHex:int):
        """
        checks if the destination is a valid position from the current position
        Args:
            curr(tuple): current Position of the Piece
            dest(tuple): destination position of the Piece
            pieceInHex(int): Value fo what is in the Cell, -1 is None, 0 is White 1 is Black
        """
        raise NotImplementedError()

class Pawn(Piece):
    def __init__(self, screen, pos, w, h,isBlack):
        super().__init__(screen, pos, w, h, isBlack)

    def is_valid_position(self, curr:tuple, dest:tuple, pieceInHex:int) -> bool:
        # if the piece is black the direction of the movement must be -1 ( 1 -2 * 1)
        # else when the piece white the direction of movement must be 1 ( 1 - 2 * 0)
        if dest[1] - curr[1] != 1 - 2 * self.isBlack:
            return False
        # if the movement is vertical the Cell must be empty
        if curr[0] == dest[0]:
            return pieceInHex % 8 == 0 
        # if the movement is diagonal the Tile has to be occupied by the other team
        elif abs(dest[0] - curr[0]) + abs(dest[1] - curr[1]) == 2:
            return self.isBlack != (pieceInHex // 8) if pieceInHex > 0 else False
        return False

class Rook(Piece):
    def __init__(self, screen, pos, w, h, isBlack):
        super().__init__(screen, pos, w, h, isBlack)

    def is_valid_position(self, curr, dest, pieceInHex) -> bool:
        if (pieceInHex // 8 == self.isBlack):
            return False
        return bool(dest[0] - curr[0]) ^ bool(dest[1] - curr[1])

class Knight(Piece):
    def __init__(self, screen, pos, w, h, isBlack):
        super().__init__(screen, pos, w, h, isBlack)

    def is_valid_position(self, curr, dest, pieceInHex) -> bool:
        if (pieceInHex // 8 == self.isBlack):
            return False
        return pow(dest[0] - curr[0], 2) + pow(dest[1] - curr[1], 2) == 5

class Bishop(Piece):
    def __init__(self, screen, pos, w, h, isBlack):
        super().__init__(screen, pos, w, h, isBlack)

    def is_valid_position(self, curr, dest, pieceInHex) -> bool:
        if (pieceInHex // 8 == self.isBlack):
            return False
        return (abs(dest[0] - curr[0]) == abs(dest[1] - curr[1])) and (abs(dest[0] - curr[0]) != 0)

class Queen(Piece):
    def __init__(self, screen, pos, w, h, isBlack):
        super().__init__(screen, pos, w, h, isBlack)

    def is_valid_position(self, curr, dest, pieceInHex) -> bool:
        if (pieceInHex // 8 == self.isBlack):
            return False
        if abs(dest[0] - curr[0]) + abs(dest[1] - curr[1]) == 0:
            return False
        return (abs(dest[0] - curr[0]) == abs(dest[1] - curr[1])) and (abs(dest[0] - curr[0]) != 0) or bool(dest[0] - curr[0]) ^ bool(dest[1] - curr[1])

class King(Piece):
    def __init__(self, screen, pos, w, h, isBlack):
        super().__init__(screen, pos, w, h, isBlack)

    def is_valid_position(self, curr, dest, pieceInHex) -> bool:
        if (pieceInHex // 8 == self.isBlack):
            return False
        return 0 < pow(curr[0] - dest[0], 2) + pow(curr[1] - dest[1], 2) <= 2