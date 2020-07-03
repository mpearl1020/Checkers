# Name
Matthew Pearl
# PennKey
pearlm
# Hours
12

# Authors
Matthew Pearl and Sneha Patel

# Third Party Packages:
1. pygame (pip install pygame)
2. pillow (pip install pillow)

# First Party Packages:
1. sys
2. os
3. time
4. random

# Files/Classes:
1. piece.py (contains the Piece class)
2. checker_board.py (contains the Board class)
3. checkers_game.py (where the game is run)

# How To Play:
1. Run the following command in your terminal: python checkers_game.py
2. When the start screen comes up, press space to play
3. This is a user vs CPU checkers game. The user has
the first turn and is red. Simply click on a red piece to start. The spaces that you are allowed to move that piece will be highlighted with blue (if the piece you select has available moves). If you want to change which piece is selected, simply click on a different one. Once you press one of the blue squares to make a move, the CPU will make a decision and pick what it believes is the optimal move. The CPU's move is delayed to take approximately 1 second. NOTE: this is currently a single-jump checkers game (you cannot make a double-jump, triple-jump, etc.).
4. Once the player or CPU has lost all of their pieces, the game is over. A new screen will appear declaring the winner and prompting the user with the option to play again. Either press space to start a new game or quit by exiting from the window.
