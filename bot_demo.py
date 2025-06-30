from bot import CornersBot, GreedyBot, play_game

if __name__ == "__main__":
    # Demo of the CornersBot (white) beating the GreedyBot (black)
    greedy_bot = GreedyBot(depth=3)
    corners_bot = CornersBot(depth=3)
    black_pieces, white_pieces = play_game(black_bot=greedy_bot,
                                           white_bot=corners_bot,
                                           print_moves=True)
    print(
        f'Final piece count: {black_pieces} black pieces, '
        f'{white_pieces} white pieces'
    )
