import unittest

class ChestPieceMoveLegality_test(unittest.TestCase):

    def test_rook(self):
        from src.chess.pieces import Rook
        rook = Rook(None, (10, 10), 10, 10, True)

        # legal Move
        self.assertTrue(rook.is_valid_position((0,0),(0,1), -1))
        self.assertTrue(rook.is_valid_position((0,0),(0,2), -1))
        self.assertTrue(rook.is_valid_position((0,0),(0,5), -1))

        self.assertTrue(rook.is_valid_position((0,0),(1,0), -1))
        self.assertTrue(rook.is_valid_position((0,0),(2,0), -1))
        self.assertTrue(rook.is_valid_position((0,0),(2,0), 1))

        self.assertTrue(rook.is_valid_position((0,1),(0,0), -1))
        self.assertTrue(rook.is_valid_position((0,2),(0,0), -1))
        self.assertTrue(rook.is_valid_position((0,5),(0,0), -1))

        self.assertTrue(rook.is_valid_position((1,1),(0,1), -1))
        self.assertTrue(rook.is_valid_position((2,1),(0,1), -1))
        self.assertTrue(rook.is_valid_position((5,1),(0,1), -1))

        self.assertTrue(rook.is_valid_position((1,2),(0,2), -1))
        self.assertTrue(rook.is_valid_position((2,2),(0,2), -1))
        self.assertTrue(rook.is_valid_position((5,2),(0,2), -1))

        self.assertTrue(rook.is_valid_position((1,5),(0,5), -1))
        self.assertTrue(rook.is_valid_position((2,5),(0,5), -1))
        self.assertTrue(rook.is_valid_position((5,5),(0,5), -1))

        # illegal Move
        self.assertFalse(rook.is_valid_position((0,0),(0,0), -1))
        self.assertFalse(rook.is_valid_position((0,0),(2,2), -1))
        self.assertFalse(rook.is_valid_position((0,0),(1,2), -1))
        self.assertFalse(rook.is_valid_position((1,1),(5,2), -1))


    def test_knight(self):

        from src.chess.pieces import Knight
        knight = Knight(None, (10, 10), 10, 10, True)
        # legal Move
        self.assertTrue(knight.is_valid_position((0,0),(1,2), -1))

        self.assertTrue(knight.is_valid_position((2,2),(0,1), -1))
        self.assertTrue(knight.is_valid_position((2,2),(1,0), -1))

        self.assertTrue(knight.is_valid_position((2,2),(0,3), -1))
        self.assertTrue(knight.is_valid_position((2,2),(1,4), -1))

        self.assertTrue(knight.is_valid_position((2,2),(3,0), -1))
        self.assertTrue(knight.is_valid_position((2,2),(4,1), -1))

        self.assertTrue(knight.is_valid_position((2,2),(3,4), -1))
        self.assertTrue(knight.is_valid_position((2,2),(4,3), -1))
        # illegal Move
        self.assertFalse(knight.is_valid_position((2,2),(0,0), -1))
        self.assertFalse(knight.is_valid_position((2,2),(1,1), -1))

        self.assertFalse(knight.is_valid_position((2,2),(2,0), -1))
        self.assertFalse(knight.is_valid_position((2,2),(2,4), -1))

        self.assertFalse(knight.is_valid_position((2,2),(4,2), -1))
        self.assertFalse(knight.is_valid_position((2,2),(0,2), -1))

        self.assertFalse(knight.is_valid_position((2,2),(4,4), -1))
        self.assertFalse(knight.is_valid_position((2,2),(4,6), -1))

    def test_bishop(self):

        from src.chess.pieces import Bishop
        bishop = Bishop(None, (10, 10), 10, 10, True)

        # legal Move
        self.assertTrue(bishop.is_valid_position((0,0),(1,1), -1))
        self.assertTrue(bishop.is_valid_position((0,0),(2,2), -1))
        self.assertTrue(bishop.is_valid_position((1,1),(5,5), -1))

        self.assertTrue(bishop.is_valid_position((1,2),(2,3), -1))
        self.assertTrue(bishop.is_valid_position((1,2),(3,4), -1))
        self.assertTrue(bishop.is_valid_position((3,2),(2,1), -1))
        self.assertTrue(bishop.is_valid_position((2,1),(1,2), -1))

        # illegal Move
        self.assertFalse(bishop.is_valid_position((0,0),(0,0), -1))
        self.assertFalse(bishop.is_valid_position((3,2),(2,2), -1))
        self.assertFalse(bishop.is_valid_position((2,2),(3,2), -1))

    def test_queen(self):
        return
        from src.chess.pieces import Queen
        queen = Queen(None, (10, 10), 10, 10, True)
        # legal Move
        self.assertTrue(queen.is_valid_position((2,2),(2,1), -1))
        self.assertTrue(queen.is_valid_position((2,2),(3,2), -1))
        self.assertTrue(queen.is_valid_position((2,2),(2,3), -1))
        self.assertTrue(queen.is_valid_position((2,2),(1,2), -1))

        self.assertTrue(queen.is_valid_position((2,2),(1,1), -1))
        self.assertTrue(queen.is_valid_position((2,2),(3,1), -1))
        self.assertTrue(queen.is_valid_position((2,2),(3,3), -1))
        self.assertTrue(queen.is_valid_position((2,2),(1,3), -1))
        
        self.assertTrue(queen.is_valid_position((2,2),(0,0), -1))
        self.assertTrue(queen.is_valid_position((2,2),(2,6), -1))
        self.assertTrue(queen.is_valid_position((2,2),(6,2), -1))
        self.assertTrue(queen.is_valid_position((1,2),(4,5), -1))
        self.assertTrue(queen.is_valid_position((1,2),(1,7), -1))


        # illegal Move
        self.assertFalse(queen.is_valid_position((0,0),(0,0), -1))

    @unittest.skip("QueenSkip")

    def test_king(self):
        return
        from src.chess.pieces import King
        king = King(None, (10, 10), 10, 10, True)

        # Straight movement
        self.assertTrue(king.is_valid_position((0,0),(1,0), -1))
        self.assertTrue(king.is_valid_position((1,0),(0,0), -1))
        self.assertTrue(king.is_valid_position((0,1),(0,0), -1))
        self.assertTrue(king.is_valid_position((0,0),(0,1), -1))
        self.assertTrue(king.is_valid_position((0,1),(0,2), -1))

        # Diagonal movement
        self.assertTrue(king.is_valid_position((1,1),(0,0), -1))
        self.assertTrue(king.is_valid_position((1,1),(0,2), -1))
        self.assertTrue(king.is_valid_position((1,1),(2,0), -1))
        self.assertTrue(king.is_valid_position((1,1),(2,2), -1))

        # Drunk Movement (Illegal moves, he's drinking on duty)
        self.assertFalse(king.is_valid_position((0,0),(0,0), -1))
        self.assertFalse(king.is_valid_position((0,0),(0,3), -1))
        self.assertFalse(king.is_valid_position((0,0),(3,0), -1))

        self.assertFalse(king.is_valid_position((0,3),(0,0), -1))
        self.assertFalse(king.is_valid_position((3,0),(0,0), -1))
        self.assertFalse(king.is_valid_position((0,0),(2,2), -1))

        self.assertFalse(king.is_valid_position((2,2),(0,3), -1))
        self.assertFalse(king.is_valid_position((0,0),(3,0), -1))
        self.assertFalse(king.is_valid_position((0,3),(0,5), -1))

        self.assertFalse(king.is_valid_position((3,3),(2,1), -1))
