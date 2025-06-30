import copy
from enum import IntEnum
from typing import List, Optional, Tuple


class Player(IntEnum):
    """Represents a player in Othello: BLACK (1) or WHITE (-1)."""
    BLACK = 1
    WHITE = -1

    def opponent(self) -> 'Player':
        """
        Returns the opposing player.

        Returns:
            Player: The opponent player.
        """
        return Player(-self.value)


class Piece(IntEnum):
    """
    Represents the content of a board cell:
    - BLACK (1): occupied by Black
    - WHITE (-1): occupied by White
    - NO_PIECE (0): empty
    """
    BLACK = 1
    NO_PIECE = 0
    WHITE = -1

    @staticmethod
    def from_player(player: Player) -> 'Piece':
        """
        Converts a Player into the corresponding Piece.

        Args:
            player (Player): The player.

        Returns:
            Piece: The matching piece.
        """
        return Piece(player.value)


class Game:
    """
    Class representing an Othello game state and rules.
    Handles piece placement, legal move checks, and board updates.
    """
    BOARD_SIZE = 8
    DIRS = [
        (-1, 0), (1, 0), (0, 1), (0, -1),
        (-1, 1), (1, 1), (-1, -1), (1, -1)
    ]

    def __init__(self, board: Optional[List[List[Piece]]] = None) -> None:
        """
        Initializes the Othello game board.

        Args:
            board (Optional[List[List[Piece]]]): An optional custom board state.
        """
        if board is not None:
            self.board: List[List[Piece]] = copy.deepcopy(board)
        else:
            self.board = [[Piece.NO_PIECE] * self.BOARD_SIZE for _ in
                          range(self.BOARD_SIZE)]
            self.board[3][3] = Piece.BLACK
            self.board[4][4] = Piece.BLACK
            self.board[3][4] = Piece.WHITE
            self.board[4][3] = Piece.WHITE

    def place_piece(self, player: Player, row: int, col: int) -> None:
        """
        Places a piece for the given player at the specified coordinates
        and flips opponent pieces.

        Args:
            player (Player): The current player.
            row (int): 0-based row index.
            col (int): 0-based column index.

        Raises:
            Exception: If the move is not legal.
        """
        if not self.is_legal_move(player, row, col):
            raise ValueError(f'Illegal move at row {row}, col {col}')
        piece = Piece.from_player(player)
        self.board[row][col] = piece
        for dx, dy, end_x, end_y in self._get_endpoints(player, row, col):
            x, y = row + dx, col + dy
            while (x, y) != (end_x, end_y):
                self.board[x][y] = piece
                x += dx
                y += dy

    def is_legal_move(self, player: Player, row: int, col: int) -> bool:
        """
        Determines if placing a piece at (row, col) is legal for the player.

        Args:
            player (Player): The current player.
            row (int): Row index.
            col (int): Column index.

        Returns:
            bool: True if the move is legal, False otherwise.
        """
        return (
                self.valid_coordinate(row, col)
                and self.board[row][col] == Piece.NO_PIECE
                and self._get_endpoints(player, row, col)
        )

    def valid_coordinate(self, row: int, col: int) -> bool:
        """
        Checks whether a board coordinate is within valid bounds.

        Args:
            row (int): Row index.
            col (int): Column index.

        Returns:
            bool: True if within bounds, False otherwise.
        """
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE

    def _get_endpoints(self, player: Player, row: int, col: int) -> List[
        Tuple[int, int, int, int]]:
        """
        Finds all endpoints where placing a piece at the specified coordinates
        would flip opponent pieces between the coordinate and that endpoint.

        Args:
            player (Player): The current player.
            row (int): Row index.
            col (int): Column index.

        Returns:
            List[Tuple[int, int, int, int]]: A list of tuples containing the
            direction (dx, dy) and endpoint (end_x, end_y) for each valid
            flip.
        """
        endpoints = []
        for dx, dy in self.DIRS:
            x, y = row + dx, col + dy
            sandwiched = False
            while (self.valid_coordinate(x, y) and
                   self.board[x][y].value == player.opponent().value):
                sandwiched = True
                x += dx
                y += dy
            if (sandwiched and self.valid_coordinate(x, y) and
                    self.board[x][y].value == player.value):
                endpoints.append((dx, dy, x, y))
        return endpoints

    def get_legal_moves_for_player(self, player: Player) -> List[
        Tuple[int, int]]:
        """
        Returns all legal move positions for the given player.

        Args:
            player (Player): The player to check.

        Returns:
            List[Tuple[int, int]]: List of (row, col) tuples.
        """
        return [
            (row, col)
            for row in range(self.BOARD_SIZE)
            for col in range(self.BOARD_SIZE)
            if self.is_legal_move(player, row, col)
        ]

    def get_num_pieces(self) -> Tuple[int, int]:
        """
        Returns the number of placed black and white pieces.

        Returns:
            Tuple[int, int]: The number of placed (black_pieces, white_pieces)
        """
        black_pieces = white_pieces = 0
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] == Piece.BLACK:
                    black_pieces += 1
                elif self.board[row][col] == Piece.WHITE:
                    white_pieces += 1
        return black_pieces, white_pieces

    def clone(self) -> 'Game':
        """
        Returns a deep copy of the current game state.

        Returns:
            Game: A new Game instance with the same board.
        """
        return Game(self.board)

    def print_grid(self) -> None:
        """
        Prints the current board state to the console in a human-readable format.
        """
        print("\n    A   B   C   D   E   F   G   H\n")
        for i, row in enumerate(self.board):
            print(f"{i + 1}  ", end="")
            for cell in row:
                if cell == Piece.NO_PIECE:
                    print("--- ", end="")
                elif cell == Piece.BLACK:
                    print(" B  ", end="")
                else:
                    print(" W  ", end="")
            print("\n")
