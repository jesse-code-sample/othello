from bot import CornersBot
from game import Game, Player


def get_alpha_notation(row, col):
    return f'{row + 1}{chr(col + ord('A'))}'


if __name__ == "__main__":
    game = Game()
    game.print_grid()
    bot = CornersBot(depth=4)
    # Demo where you play the black pieces against a bot.
    while True:
        # You have no available moves
        if bot.get_best_move(game, Player.BLACK) is None:
            break
        # Parse input into a move
        print('>', end=' ')
        input_str = input().strip()
        try:
            row = int(input_str[0]) - 1
            col = ord(input_str[1].upper()) - ord('A')
        except (IndexError, ValueError):
            print('Invalid input')
            continue
        if not game.is_legal_move(Player.BLACK, row, col):
            print(f'{input_str} is not a valid move')
            continue
        # Player's move
        print(f'You moved at: {get_alpha_notation(row, col)}')
        game.place_piece(Player.BLACK, row, col)
        game.print_grid()
        # Bot's move
        bot_move = bot.get_best_move(game, Player.WHITE)
        if bot_move is None:
            break
        print(f'AI moved at: {get_alpha_notation(*bot_move)}')
        game.place_piece(Player.WHITE, *bot_move)
        game.print_grid()

    black_pieces, white_pieces = game.get_num_pieces()
    print(
        f'Final piece count: {black_pieces} black pieces, '
        f'{white_pieces} white pieces'
    )
