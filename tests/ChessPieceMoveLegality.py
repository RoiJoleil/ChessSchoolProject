import unittest

class ChestPieceMoveLegality(unittest.TestCase):
    def test_rook(self):

        from src.Chesspieces.IChessPiece import Rook
        # legal Move
        self.assertTrue(Rook.legalMoveCord(0,0,0,1))
        self.assertTrue(Rook.legalMoveStrPos(Rook,"A0", "A1"))

        # illegal Move
        self.assertFalse(Rook.legalMoveCord(0,0,0,0))
        self.assertFalse(Rook.legalMoveStrPos(Rook,"A0","A0"))


    def test_king(self):

        from src.Chesspieces.IChessPiece import King

        # Straight movement
        self.assertTrue(King.legalMoveCord(0,0,1,0))
        self.assertTrue(King.legalMoveCord(1,0,0,0))
        self.assertTrue(King.legalMoveCord(0,1,0,0))
        self.assertTrue(King.legalMoveCord(0,0,0,1))
        self.assertTrue(King.legalMoveCord(0,1,0,2))

        self.assertTrue(King.legalMoveStrPos(King,"A0","B0"))
        self.assertTrue(King.legalMoveStrPos(King,"B0","A0"))
        self.assertTrue(King.legalMoveStrPos(King,"A1","A0"))
        self.assertTrue(King.legalMoveStrPos(King,"A0","A1"))
        self.assertTrue(King.legalMoveStrPos(King,"A1","A2"))

        # Diagonal movement
        self.assertTrue(King.legalMoveCord(1,1,0,0))
        self.assertTrue(King.legalMoveCord(1,1,0,2))
        self.assertTrue(King.legalMoveCord(1,1,2,0))
        self.assertTrue(King.legalMoveCord(1,1,2,2))

        self.assertTrue(King.legalMoveStrPos(King,"B1","A0"))
        self.assertTrue(King.legalMoveStrPos(King,"B1","A2"))
        self.assertTrue(King.legalMoveStrPos(King,"B1","C0"))
        self.assertTrue(King.legalMoveStrPos(King,"B1","C2"))

        # Drunk Movement (Illegal moves, he's drinking on duty)
        self.assertFalse(King.legalMoveCord(0,0,0,0))
        self.assertFalse(King.legalMoveCord(0,0,0,3))
        self.assertFalse(King.legalMoveCord(0,0,3,0))

        self.assertFalse(King.legalMoveCord(0,3,0,0))
        self.assertFalse(King.legalMoveCord(3,0,0,0))
        self.assertFalse(King.legalMoveCord(0,0,2,2))

        self.assertFalse(King.legalMoveCord(2,2,0,3))
        self.assertFalse(King.legalMoveCord(0,0,3,0))
        self.assertFalse(King.legalMoveCord(0,3,0,5))

        self.assertFalse(King.legalMoveCord(3,3,2,1))

        self.assertFalse(King.legalMoveStrPos(King,"A0","A0"))
        self.assertFalse(King.legalMoveStrPos(King,"A0","A3"))
        self.assertFalse(King.legalMoveStrPos(King,"A0","D0"))

        self.assertFalse(King.legalMoveStrPos(King,"A3","A0"))
        self.assertFalse(King.legalMoveStrPos(King,"D3","Q0"))
        self.assertFalse(King.legalMoveStrPos(King,"D3","D0"))

        self.assertFalse(King.legalMoveStrPos(King,"A0","B6"))
        self.assertFalse(King.legalMoveStrPos(King,"A0","A3"))
        self.assertFalse(King.legalMoveStrPos(King,"A0","D1"))

        self.assertFalse(King.legalMoveStrPos(King,"A3","A0"))
        self.assertFalse(King.legalMoveStrPos(King,"D3","A0"))
        self.assertFalse(King.legalMoveStrPos(King,"D3","F6"))

    def test_bishop(self):

        from src.Chesspieces.IChessPiece import Bishop
        # legal Move
        self.assertTrue(Bishop.legalMoveCord(0,0,1,1))
        self.assertTrue(Bishop.legalMoveStrPos(Bishop,"A0", "B1"))

        # illegal Move
        self.assertFalse(Bishop.legalMoveCord(0,0,0,0))
        self.assertFalse(Bishop.legalMoveStrPos(Bishop,"A0","A0"))

    def test_knight(self):

        from src.Chesspieces.IChessPiece import Knight
        # legal Move
        self.assertTrue(Knight.legalMoveCord(0,0,1,2))
        self.assertTrue(Knight.legalMoveStrPos(Knight,"A0", "B2"))

        # illegal Move
        self.assertFalse(Knight.legalMoveCord(0,0,0,0))
        self.assertFalse(Knight.legalMoveStrPos(Knight, "A0","A0"))

    def test_queen(self):

        from src.Chesspieces.IChessPiece import Queen
        # legal Move
        self.assertTrue(Queen.legalMoveCord(0,0,0,1))
        self.assertTrue(Queen.legalMoveStrPos(Queen, "A0", "A1"))

        # illegal Move
        self.assertFalse(Queen.legalMoveCord(0,0,0,0))
        self.assertFalse(Queen.legalMoveStrPos(Queen,"A0","A0"))
""""
    def test_pawn(self):

        from src.Chesspieces.IChessPiece import Pawn
        # legal Move
        self.assertTrue(Pawn.legalMoveCord(0,0,0,1, False))
        self.assertTrue(Pawn.legalMoveStrPos(Pawn, "A0", "A1", False))

        # illegal Move
        self.assertFalse(Pawn.legalMoveCord(0,0,0,0, False))
        self.assertFalse(Pawn.legalMoveStrPos(Pawn, "A0","A0", False))
"""
if __name__ == "__main__":
    unittest.main()