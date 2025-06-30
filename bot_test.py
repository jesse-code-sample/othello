import unittest

from bot import CornersBot, GreedyBot, play_game


class TestMinimaxBot(unittest.TestCase):

    def test_depth(self):
        """
        Tests that a bot with greater search depth wins.
        Note that this may not be the case with GreedyBot, as it uses a poor
        heuristic.
        """
        shallow_bot = CornersBot(depth=1)
        deep_bot = CornersBot(depth=2)
        # Deep bot wins when going first
        black_pieces, white_pieces = play_game(black_bot=deep_bot,
                                               white_bot=shallow_bot)
        self.assertGreater(black_pieces, white_pieces)
        # Deep bot wins when going second
        black_pieces, white_pieces = play_game(black_bot=shallow_bot,
                                               white_bot=deep_bot)
        self.assertLess(black_pieces, white_pieces)

    def test_corners(self):
        """
        Tests that the CornersBot beats the GreedyBot.
        Note that this may not work at lower depths when GreedyBot goes first,
        as there is inherent first-player advantage.
        """
        greedy_bot = GreedyBot(depth=4)
        corners_bot = CornersBot(depth=4)
        # Corners bot wins when going first
        black_pieces, white_pieces = play_game(black_bot=corners_bot,
                                               white_bot=greedy_bot)
        self.assertGreater(black_pieces, white_pieces)
        # Corners bot wins when going second
        black_pieces, white_pieces = play_game(black_bot=greedy_bot,
                                               white_bot=corners_bot)
        self.assertLess(black_pieces, white_pieces)


if __name__ == '__main__':
    unittest.main()
