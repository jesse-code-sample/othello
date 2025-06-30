# Othello

## Game Overview

Othello (also known as Reversi) is a board game played on a 8x8 board. Players
alternate placing discs of their color, and any opponent's discs in a straight
line between the new disc and an existing disc of the player's color are flipped
to the player's color. A legal move must flip at least one opponent disc.

The goal is to have the more discs of your color on the board than your
opponent at the end of the game. The game ends when the player to move has no
legal moves. Full rules can be found
[here](https://www.worldothello.org/about/about-othello/othello-rules/official-rules/english).

## Bot

`bot.py` implements a simple bot that uses minimax with alpha-beta pruning to
decide its next move. See
this [Wikipedia page](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
for more information on the algorithm.

We provide two simple bots: `GreedyBot` and `CornersBot`. `GreedyBot` simply
aims to maximize the difference in number of pieces on the board.
`CornersBot` heavily weights placing pieces on corners, as corner pieces can
never be recaptured. Try implementing your custom bot by creating a subclass of
`MinimaxBot` and implementing the `evaluate` function!

You can also try running `bot_demo.py`, which has a `GreedyBot` playing the 
black pieces against a `CornersBot` as white. The moves made by each bot and the
game state are printed. As expected, `CornersBot` easily wins with its more
advanced heuristic.

## Interactive Play
Run `interactive_demo.py` to try playing with the black pieces against a bot.
The input is in alphanumeric notation (e.g. 1B) corresponds to the first
(one-indexed) row and the second column.