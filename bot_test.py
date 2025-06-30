import unittest

from bot import CornersBot, GreedyBot, play_game


class TestMinimaxBot(unittest.TestCase):

    def test_depth(self):
        shallow_bot = CornersBot(depth=1)
        deep_bot = CornersBot(depth=2)
        black_pieces, white_pieces = play_game(black_bot=shallow_bot,
                                               white_bot=deep_bot)
        self.assertTrue(black_pieces < white_pieces)

    def test_corners(self):
        greedy_bot = GreedyBot(depth=2)
        corners_bot = CornersBot(depth=2)
        black_pieces, white_pieces = play_game(black_bot=greedy_bot,
                                               white_bot=corners_bot)
        self.assertTrue(black_pieces < white_pieces)


if __name__ == '__main__':
    unittest.main()
