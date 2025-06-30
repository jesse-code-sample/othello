import unittest

from game import Game, Piece, Player


class TestOthelloGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_initial_board(self):
        self.assertEqual(self.game.board[3][3], Piece.WHITE)
        self.assertEqual(self.game.board[4][4], Piece.WHITE)
        self.assertEqual(self.game.board[3][4], Piece.BLACK)
        self.assertEqual(self.game.board[4][3], Piece.BLACK)

    def test_valid_moves(self):
        self.assertTrue(self.game.is_legal_move(Player.BLACK, 2, 3))
        self.assertTrue(self.game.is_legal_move(Player.BLACK, 4, 5))
        self.assertTrue(self.game.is_legal_move(Player.WHITE, 2, 4))
        self.assertTrue(self.game.is_legal_move(Player.WHITE, 3, 5))

    def test_invalid_moves(self):
        self.assertFalse(self.game.is_legal_move(Player.WHITE, 0, 0))
        self.assertFalse(
            self.game.is_legal_move(Player.WHITE, 3, 3))  # Occupied

    def test_invalid_placement(self):
        with self.assertRaises(ValueError):
            self.game.place_piece(Player.WHITE, 3, 3)  # Already occupied
        with self.assertRaises(ValueError):
            self.game.place_piece(Player.WHITE, -1, 0)  # Out of bounds
        with self.assertRaises(ValueError):
            self.game.place_piece(Player.WHITE, 2, 3)  # No white piece to flip

    def test_flip_one_piece(self):
        """
        W B 'W'  ->  W W W
        B W          B W
        """
        self.game.place_piece(Player.WHITE, 3, 5)
        self.assertEqual(self.game.board[3][5], Piece.WHITE)
        self.assertEqual(self.game.board[3][4],
                         Piece.WHITE)  # Flipped from BLACK

    def test_flip_multiple_pieces(self):
        """
        W B B B 'W'  ->  W W W W W
        B W              B W
        """
        self.game.board[3][5] = self.game.board[3][6] = Piece.BLACK
        self.game.place_piece(Player.WHITE, 3, 7)
        for col in range(3, 8):
            self.assertEqual(self.game.board[3][col], Piece.WHITE)

    def test_flip_two_directions(self):
        """
        W B B 'W'  ->  W W W W
        B B B          B B W
          W              W
        """
        self.game.board[3][5] = Piece.BLACK
        self.game.board[4][4] = Piece.BLACK
        self.game.board[4][5] = Piece.BLACK
        self.game.board[5][4] = Piece.WHITE
        self.game.place_piece(Player.WHITE, 3, 6)
        for col in range(3, 7):
            self.assertEqual(self.game.board[3][col], Piece.WHITE)
        self.assertEqual(self.game.board[4][5], Piece.WHITE)


if __name__ == '__main__':
    unittest.main()
