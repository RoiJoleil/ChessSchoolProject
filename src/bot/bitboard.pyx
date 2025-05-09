from libc.stdint cimport uint64_t

# Bitboards
cdef uint64_t all_pieces = 0
cdef uint64_t black_pieces = 0
cdef uint64_t white_pieces = 0

cdef uint64_t black_pawns = 0
cdef uint64_t black_knights = 0
cdef uint64_t black_bishops = 0
cdef uint64_t black_rooks = 0
cdef uint64_t black_queen = 0
cdef uint64_t black_king = 0

cdef uint64_t white_pawns = 0
cdef uint64_t white_knights = 0
cdef uint64_t white_bishops = 0
cdef uint64_t white_rooks = 0
cdef uint64_t white_queen = 0
cdef uint64_t white_king = 0

def print_raw_bits(uint64_t value):
    """
    Print the raw binary representation of a 64-bit value.
    Shows all 64 bits from most significant (bit 63) to least significant (bit 0).
    """
    print("Binary representation (bit 63 to bit 0):")
    binary = ""
    # Process all 64 bits
    for i in range(63, -1, -1):
        bit = 1 if (value & (1 << i)) else 0
        binary += str(bit)
        # Add a space every 8 bits for readability
        if i % 8 == 0 and i > 0:
            binary += " "
    print(binary)
    
    # Also print in groups of 8 rows of 8 bits to match chess board layout
    print("\nChess board layout (a8-h8 at top, a1-h1 at bottom):")
    for row in range(8):
        row_bits = ""
        for col in range(8):
            # Calculate bit position: top row = bits 56-63, etc.
            bit_pos = (7-row) * 8 + col
            bit = 1 if (value & (1 << bit_pos)) else 0
            row_bits += str(bit) + " "
        print(row_bits)

def print_bitboard(uint64_t bitboard):
    """
    Print a visual representation of a bitboard as an 8x8 chess board.
    1 indicates a piece is present, 0 indicates an empty square.
    """
    print("  +-----------------+")
    for rank in range(8):
        # Chess boards traditionally have rank 8 at the top
        r = 7 - rank
        print(f"{r+1} | ", end="")
        for file in range(8):
            # Calculate bit position (0-63)
            pos = r * 8 + file
            # Check if bit is set at position
            if bitboard & (1 << pos):
                print("1 ", end="")
            else:
                print("0 ", end="")
        print("|")
    print("  +-----------------+")
    print("    a b c d e f g h")
    print(f"Value: {bitboard}")

cdef void reset_bitboard():
    global all_pieces, black_pieces, white_pieces
    global black_bishops, black_king, black_knights, black_pawns, black_queen, black_rooks
    global white_bishops, white_king, white_knights, white_pawns, white_queen, white_rooks

    all_pieces = 0
    black_pieces = 0
    white_pieces = 0
    black_pawns = 0
    black_knights = 0
    black_bishops = 0
    black_rooks = 0
    black_queen = 0
    black_king = 0
    white_pawns = 0
    white_knights = 0
    white_bishops = 0
    white_rooks = 0
    white_queen = 0
    white_king = 0

cdef convert_position_to_bitboard(list pieces_list):
    global all_pieces, black_pieces, white_pieces
    global black_bishops, black_king, black_knights, black_pawns, black_queen, black_rooks
    global white_bishops, white_king, white_knights, white_pawns, white_queen, white_rooks
    
    cdef int index
    cdef int identity
    cdef uint64_t bit_mask
    
    for piece_tuple in pieces_list:
        index = piece_tuple[0]
        identity = piece_tuple[1]
        bit_mask = (<uint64_t>1) << index
        
        # Update all_pieces bitboard
        all_pieces |= bit_mask

        if identity == 1:  # White pawn
            white_pieces |= bit_mask
            white_pawns |= bit_mask
        elif identity == 2:  # White rook
            white_pieces |= bit_mask
            white_rooks |= bit_mask
        elif identity == 3:  # White knight
            white_pieces |= bit_mask
            white_knights |= bit_mask
        elif identity == 4:  # White bishop
            white_pieces |= bit_mask
            white_bishops |= bit_mask
        elif identity == 5:  # White queen
            white_pieces |= bit_mask
            white_queen |= bit_mask
        elif identity == 6:  # White king
            white_pieces |= bit_mask
            white_king |= bit_mask
        elif identity == 9:  # Black pawn
            black_pieces |= bit_mask
            black_pawns |= bit_mask
        elif identity == 10:  # Black rook
            black_pieces |= bit_mask
            black_rooks |= bit_mask
        elif identity == 11:  # Black knight
            black_pieces |= bit_mask
            black_knights |= bit_mask
        elif identity == 12:  # Black bishop
            black_pieces |= bit_mask
            black_bishops |= bit_mask
        elif identity == 13:  # Black queen
            black_pieces |= bit_mask
            black_queen |= bit_mask
        elif identity == 14:  # Black king
            black_pieces |= bit_mask
            black_king |= bit_mask
        
cpdef bot_execute(list pieces_list):
    global all_pieces, black_pieces, black_bishops, black_king, black_knights, black_pawns, black_queen, black_rooks, white_pieces, white_rooks
    reset_bitboard()
    convert_position_to_bitboard(pieces_list)