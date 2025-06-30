import operator
from abc import abstractmethod, ABC
from typing import Optional, Tuple

from game import Game, Player


class MinimaxBot(ABC):
    """
    A simple AI for Othello using minimax with alpha-beta pruning.
    """

    def __init__(self, depth: int) -> None:
        """
        Initializes the bot with a search depth.

        Args:
            depth (int): Depth of the minimax search tree.
        """
        self.depth = depth

    def get_best_move(self, game: Game, player: Player) -> Optional[
        Tuple[int, int]]:
        """
        Returns the best move for the given player.

        Args:
            game (Game): The current game state.
            player (Player): The player to make the move.

        Returns:
            Optional[Tuple[int, int]]: The (row, col) of the best move, or
            None if no legal moves.
        """
        _, move = self._minimax(game, player, self.depth, float('-inf'),
                                float('inf'))
        return move

    @abstractmethod
    def evaluate(self, game: Game) -> int:
        """
        Evaluates the game state. Positive values should indicate a more
        favorable evaluation for BLACK, while negative values should indicate a
        more favorable evaluation for WHITE.

        Args:
            game (Game): The current game state.

        Returns
            int: The evaluation of the game state.
        """
        pass

    def _minimax(
            self,
            game: Game,
            player: Player,
            depth: int,
            alpha: float,
            beta: float,
    ) -> Tuple[int, Optional[Tuple[int, int]]]:
        """
        Minimax algorithm with alpha-beta pruning. Maximizes the evaluation for
        the BLACK player, and minimizes the evaluation for the WHITE player.

        Args:
            game (Game): Current game state.
            player (Player): Player for whom to evaluate.
            depth (int): Remaining depth to search.
            alpha (float): Alpha pruning value.
            beta (float): Beta pruning value.

        Returns:
            Tuple[int, Optional[Tuple[int, int]]]: Evaluation score and move.
        """
        legal_moves = game.get_legal_moves_for_player(player)
        if depth == 0 or not legal_moves:
            return self.evaluate(game), None
        best_move = None
        best_eval = -float('inf') if player == Player.BLACK else float('inf')
        comparator = operator.gt if player == Player.BLACK else operator.lt
        for row, col in legal_moves:
            new_game = game.clone()
            new_game.place_piece(player, row, col)
            cur_eval, _ = self._minimax(new_game, player.opponent(), depth - 1,
                                        alpha, beta)
            if comparator(cur_eval, best_eval):
                best_eval = cur_eval
                best_move = (row, col)
            if player == Player.BLACK:
                alpha = max(alpha, cur_eval)
            else:
                beta = min(beta, cur_eval)
            if beta <= alpha:
                break
        return best_eval, best_move


class GreedyBot(MinimaxBot):
    """A simple bot that maximizes the difference in number of pieces."""

    @staticmethod
    def coin_score(game: Game) -> int:
        black_pieces, white_pieces = game.get_num_pieces()
        return black_pieces - white_pieces

    def evaluate(self, game: Game) -> int:
        return self.coin_score(game)


class CornersBot(GreedyBot):
    """A more advanced bot that prioritizes placing pieces on corners."""

    @staticmethod
    def corners_score(game: Game) -> int:
        corners_indices = [
            (0, 0),
            (0, game.BOARD_SIZE - 1),
            (game.BOARD_SIZE - 1, 0),
            (game.BOARD_SIZE - 1, game.BOARD_SIZE - 1),
        ]
        return sum(
            game.board[row][col] for row, col in corners_indices
        )

    def evaluate(self, game: Game) -> int:
        return self.coin_score(game) + 25 * self.corners_score(game)


def play_game(black_bot, white_bot, print_moves=False):
    """
    Minimax algorithm with alpha-beta pruning. Maximizes the evaluation for
    the BLACK player, and minimizes the evaluation for the WHITE player.

    Args:
        black_bot (MinimaxBot): The bot playing black pieces.
        white_bot (MinimaxBot): The bot playing white pieces.
        print_moves (bool): Whether to print the game state and moves made
                            by the bots.

    Returns:
        Tuple[int, Optional[Tuple[int, int]]]: Evaluation score and move.
    """
    game = Game()
    if print_moves:
        game.print_grid()
    bots = [black_bot, white_bot]
    cur_bot, cur_player = 0, Player.BLACK
    while move := bots[cur_bot].get_best_move(game, cur_player):
        row, col = move
        game.place_piece(cur_player, row, col)
        if print_moves:
            print(
                f'{cur_player.name} moves at {row + 1}{chr(col + ord("A"))}'
            )
            game.print_grid()
        cur_bot = ~cur_bot
        cur_player = cur_player.opponent()
    return game.get_num_pieces()
