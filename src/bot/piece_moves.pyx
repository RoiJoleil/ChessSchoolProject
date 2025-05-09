from libc.stdint cimport uint64_t

"""
These masks allow us to quickly check what pieces are in specific rows / files.
"""

# File masks
cdef uint64_t FILE_A = 0x0101010101010101
cdef uint64_t FILE_B = 0x0202020202020202
cdef uint64_t FILE_C = 0x0404040404040404
cdef uint64_t FILE_D = 0x0808080808080808
cdef uint64_t FILE_E = 0x1010101010101010
cdef uint64_t FILE_F = 0x2020202020202020
cdef uint64_t FILE_G = 0x4040404040404040
cdef uint64_t FILE_H = 0x8080808080808080

# Rank masks
cdef uint64_t RANK_1 = 0x00000000000000FF
cdef uint64_t RANK_2 = 0x000000000000FF00
cdef uint64_t RANK_3 = 0x0000000000FF0000
cdef uint64_t RANK_4 = 0x00000000FF000000
cdef uint64_t RANK_5 = 0x000000FF00000000
cdef uint64_t RANK_6 = 0x0000FF0000000000
cdef uint64_t RANK_7 = 0x00FF000000000000
cdef uint64_t RANK_8 = 0xFF00000000000000

cdef uint64_t FILES[8]
cdef uint64_t RANKS[8]

# Initialize our lookup tables
cpdef void initialize_lookup_tables():
    global FILES, RANKS
    FILES = [FILE_A, FILE_B, FILE_C, FILE_D, FILE_E, FILE_F, FILE_G, FILE_H]
    RANKS = [RANK_1, RANK_2, RANK_3, RANK_4, RANK_5, RANK_6, RANK_7, RANK_8]

cdef uint64_t get_rook_moves(piece_bitboard, all_bitboard, friendly_bitboard):
    """
    Calculate all moves for the specific piece given.

    Returns:
        Bitboard with bits set for all valid destination squares.
    """
