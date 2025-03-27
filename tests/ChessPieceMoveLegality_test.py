import unittest

class ChestPieceMoveLegality_test(unittest.TestCase):
    def test_rook(self):

        from src.Chesspieces.IChessPiece import Rook
        # legal Move
        self.assertTrue(Rook.legalMoveCord(0,0,0,1, False))
        self.assertTrue(Rook.legalMoveCord(0,0,0,2, False))
        self.assertTrue(Rook.legalMoveCord(0,0,0,5, False))

        self.assertTrue(Rook.legalMoveCord(0,0,1,0, False))
        self.assertTrue(Rook.legalMoveCord(0,0,2,0, False))
        self.assertTrue(Rook.legalMoveCord(0,0,5,0, False))

        self.assertTrue(Rook.legalMoveCord(0,1,0,0, False))
        self.assertTrue(Rook.legalMoveCord(0,2,0,0, False))
        self.assertTrue(Rook.legalMoveCord(0,5,0,0, False))

        self.assertTrue(Rook.legalMoveCord(1,1,0,1, False))
        self.assertTrue(Rook.legalMoveCord(2,1,0,1, False))
        self.assertTrue(Rook.legalMoveCord(5,1,0,1, False))

        self.assertTrue(Rook.legalMoveCord(1,2,0,2, False))
        self.assertTrue(Rook.legalMoveCord(2,2,0,2, False))
        self.assertTrue(Rook.legalMoveCord(5,2,0,2, False))

        self.assertTrue(Rook.legalMoveCord(1,5,0,5, False))
        self.assertTrue(Rook.legalMoveCord(2,5,0,5, False))
        self.assertTrue(Rook.legalMoveCord(5,5,0,5, False))

        # illegal Move
        self.assertFalse(Rook.legalMoveCord(0,0,0,0, False))
        self.assertFalse(Rook.legalMoveCord(0,0,2,2, False))
        self.assertFalse(Rook.legalMoveCord(0,0,1,2, False))
        self.assertFalse(Rook.legalMoveCord(1,1,5,2, False))


    def test_king(self):

        from src.Chesspieces.IChessPiece import King

        # Straight movement
        self.assertTrue(King.legalMoveCord(0,0,1,0, False))
        self.assertTrue(King.legalMoveCord(1,0,0,0, False))
        self.assertTrue(King.legalMoveCord(0,1,0,0, False))
        self.assertTrue(King.legalMoveCord(0,0,0,1, False))
        self.assertTrue(King.legalMoveCord(0,1,0,2, False))

        self.assertTrue(King.legalMoveStrPos(King,"A0","B0", False))
        self.assertTrue(King.legalMoveStrPos(King,"B0","A0", False))
        self.assertTrue(King.legalMoveStrPos(King,"A1","A0", False))
        self.assertTrue(King.legalMoveStrPos(King,"A0","A1", False))
        self.assertTrue(King.legalMoveStrPos(King,"A1","A2", False))

        # Diagonal movement
        self.assertTrue(King.legalMoveCord(1,1,0,0, False))
        self.assertTrue(King.legalMoveCord(1,1,0,2, False))
        self.assertTrue(King.legalMoveCord(1,1,2,0, False))
        self.assertTrue(King.legalMoveCord(1,1,2,2, False))

        self.assertTrue(King.legalMoveStrPos(King,"B1","A0", False))
        self.assertTrue(King.legalMoveStrPos(King,"B1","A2", False))
        self.assertTrue(King.legalMoveStrPos(King,"B1","C0", False))
        self.assertTrue(King.legalMoveStrPos(King,"B1","C2", False))

        # Drunk Movement (Illegal moves, he's drinking on duty)
        self.assertFalse(King.legalMoveCord(0,0,0,0, False))
        self.assertFalse(King.legalMoveCord(0,0,0,3, False))
        self.assertFalse(King.legalMoveCord(0,0,3,0, False))

        self.assertFalse(King.legalMoveCord(0,3,0,0, False))
        self.assertFalse(King.legalMoveCord(3,0,0,0, False))
        self.assertFalse(King.legalMoveCord(0,0,2,2, False))

        self.assertFalse(King.legalMoveCord(2,2,0,3, False))
        self.assertFalse(King.legalMoveCord(0,0,3,0, False))
        self.assertFalse(King.legalMoveCord(0,3,0,5, False))

        self.assertFalse(King.legalMoveCord(3,3,2,1, False))

        self.assertFalse(King.legalMoveStrPos(King,"A0","A0", False))
        self.assertFalse(King.legalMoveStrPos(King,"A0","A3", False))
        self.assertFalse(King.legalMoveStrPos(King,"A0","D0", False))

        self.assertFalse(King.legalMoveStrPos(King,"A3","A0", False))
        self.assertFalse(King.legalMoveStrPos(King,"D3","Q0", False))
        self.assertFalse(King.legalMoveStrPos(King,"D3","D0", False))

        self.assertFalse(King.legalMoveStrPos(King,"A0","B6", False))
        self.assertFalse(King.legalMoveStrPos(King,"A0","A3", False))
        self.assertFalse(King.legalMoveStrPos(King,"A0","D1", False))

        self.assertFalse(King.legalMoveStrPos(King,"A3","A0", False))
        self.assertFalse(King.legalMoveStrPos(King,"D3","A0", False))
        self.assertFalse(King.legalMoveStrPos(King,"D3","F6", False))

    def test_bishop(self):

        from src.Chesspieces.IChessPiece import Bishop
        # legal Move
        self.assertTrue(Bishop.legalMoveCord(0,0,1,1, False))
        self.assertTrue(Bishop.legalMoveCord(0,0,2,2, False))
        self.assertTrue(Bishop.legalMoveCord(1,1,5,5, False))

        self.assertTrue(Bishop.legalMoveCord(1,2,2,3, False))
        self.assertTrue(Bishop.legalMoveCord(1,2,3,4, False))
        self.assertTrue(Bishop.legalMoveCord(3,2,2,1, False))
        self.assertTrue(Bishop.legalMoveCord(2,1,1,2, False))

        # illegal Move
        self.assertFalse(Bishop.legalMoveCord(0,0,0,0, False))
        self.assertFalse(Bishop.legalMoveCord(3,2,2,2, False))
        self.assertFalse(Bishop.legalMoveCord(2,2,3,2, False))
        """
        self.assertTrue(Bishop.legalMoveStrPos(Bishop,"A0", "B1", False))
        self.assertFalse(Bishop.legalMoveStrPos(Bishop,"A0","A0", False))
        """
    def test_knight(self):

        from src.Chesspieces.IChessPiece import Knight
        # legal Move
        self.assertTrue(Knight.legalMoveCord(0,0,1,2, False))
        self.assertTrue(Knight.legalMoveStrPos(Knight,"A0", "B2", False))

        self.assertTrue(Knight.legalMoveCord(2,2,0,1, False))
        self.assertTrue(Knight.legalMoveCord(2,2,1,0, False))

        self.assertTrue(Knight.legalMoveCord(2,2,0,3, False))
        self.assertTrue(Knight.legalMoveCord(2,2,1,4, False))

        self.assertTrue(Knight.legalMoveCord(2,2,3,0, False))
        self.assertTrue(Knight.legalMoveCord(2,2,4,1, False))

        self.assertTrue(Knight.legalMoveCord(2,2,3,4, False))
        self.assertTrue(Knight.legalMoveCord(2,2,4,3, False))
        # illegal Move
        self.assertFalse(Knight.legalMoveCord(2,2,0,0, False))
        self.assertFalse(Knight.legalMoveCord(2,2,1,1, False))

        self.assertFalse(Knight.legalMoveCord(2,2,2,0, False))
        self.assertFalse(Knight.legalMoveCord(2,2,2,4, False))

        self.assertFalse(Knight.legalMoveCord(2,2,4,2, False))
        self.assertFalse(Knight.legalMoveCord(2,2,0,2, False))

        self.assertFalse(Knight.legalMoveCord(2,2,4,4, False))
        self.assertFalse(Knight.legalMoveCord(2,2,4,6, False))

        self.assertFalse(Knight.legalMoveStrPos(Knight, "A0","A0", False))

    def test_queen(self):

        from src.Chesspieces.IChessPiece import Queen
        # legal Move
        self.assertTrue(Queen.legalMoveCord(2,2,2,1, False))
        self.assertTrue(Queen.legalMoveCord(2,2,3,2, False))
        self.assertTrue(Queen.legalMoveCord(2,2,2,3, False))
        self.assertTrue(Queen.legalMoveCord(2,2,1,2, False))

        self.assertTrue(Queen.legalMoveCord(2,2,1,1, False))
        self.assertTrue(Queen.legalMoveCord(2,2,3,1, False))
        self.assertTrue(Queen.legalMoveCord(2,2,3,3, False))
        self.assertTrue(Queen.legalMoveCord(2,2,1,3, False))
        
        self.assertTrue(Queen.legalMoveCord(2,2,0,0, False))
        self.assertTrue(Queen.legalMoveCord(2,2,2,6, False))
        self.assertTrue(Queen.legalMoveCord(2,2,6,2, False))
        self.assertTrue(Queen.legalMoveCord(1,2,4,5, False))
        self.assertTrue(Queen.legalMoveCord(1,2,1,7, False))

        self.assertTrue(Queen.legalMoveStrPos(Queen, "A0", "A1", False))

        # illegal Move
        self.assertFalse(Queen.legalMoveCord(0,0,0,0, False))
        self.assertFalse(Queen.legalMoveStrPos(Queen,"A0","A0", False))
""""
    def test_pawn(self):

        from src.Chesspieces.IChessPiece import Pawn
        # legal Move
        self.assertTrue(Pawn.legalMoveCord(0,0,0,1, False, False))
        self.assertTrue(Pawn.legalMoveStrPos(Pawn, "A0", "A1", False, False))

        # illegal Move
        self.assertFalse(Pawn.legalMoveCord(0,0,0,0, False, False))
        self.assertFalse(Pawn.legalMoveStrPos(Pawn, "A0","A0", False, False))
"""
if __name__ == "__main__":
    unittest.main()