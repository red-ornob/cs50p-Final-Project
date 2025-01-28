# CLI Chess
#### Video Demo:  <URL HERE>
#### Description: Chess for the command line enjoyers.

The program is a game of chess intended to be played on the terminal. It can be started using `python <path to project.py>` and it takes a handful of arguments to customise the chess bot and the board. A running game can be saved and later loaded by copy-pasting a string, called a fen. There is also an autosave feature that prompts the user next time if they would like to load the last game.

Starting with the non-function part of the code. I needed to set the board outside of `if __name__ == "__main__"` as unit testing the function requires it. A better way would be to make the functions take in a board parameter but that will require a lot of refactoring, especially considering my error checking.