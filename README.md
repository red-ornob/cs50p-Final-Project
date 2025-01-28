# CLI Chess
#### Video Demo:  <URL HERE>
#### Description: Chess for the command line emjoyers.

The program is a game of chess intended to be played on the terminal. It can be started using `python <path to project.py>` and it takes a handful of arguments to customise the chess bot and the board. A running game can be saved and later loaded by copy-pasting a string, called a fen. There is also an autosave feature that prompts the user next time if they would like to load the last game.

Starting with the non-function part of the code. There is not much there, used to be much more, and has some weird global variables. But then I did a large refactor to clean up my global variables. Unfortunately `main` is no longer the first function called.

Moving to `init`, it initiates the board and the bot. It also has error handling to autosave the board fen in a file when there is an early exit, print the error when it is a user error and make it hard to keep the bot running after an early exit.

Then we come to `main`, which deals with calling most of the functions needed for the game. There is a messy bit of code which stop randomly assigning who goes first if the game is being loaded and assigns colour correctly when loaded. After which it starts a loop that continues until the game ends. In the loop, user and bot take turns to move and the board is printed before the user's turn if the argument was set. The turns need to be in if statements or match case block since when loaded during black's turn, black will need to go first. `main` also prints who the winner of the game is at the end.

The `play` function is simple, it either makes a move from user input or bot analysis.

The `get_move` gets user input and validates it. If the input is a command, it executes it by calling `command` and then re-prompts for move. It checks if the input is formatted correct and that it is a legal move. Failure will result in a re-prompt.

`get_args` defines the argparse arguments and returns the arguments. There is a load argument which loads from the given fen string. The board argument will result in a board showing up before user's turn, this can be manually invoked using the board command. The time and depth sets these configurations for the bot, they have a default value of 1 and 20 respectively. Lastly there is an argument for who goes first, it defaults to being random.

The `set_players` function takes the play mode argument and returns a list of string based on the mode.

There is, in my opinion, a pretty great autosave feature. `check_autosave` checks for a file called "autosave.chess" and loads it after prompting the user for confirmation and then removes the file. It also returns a status code for if there was a load, this is done so the random player set can be overridden.

`command` simply matches the string passed in with a set of commands and executes it. Non commands return a false status code. The commands are:
- board: which prints the board.
- save: which prints the board fen.
- load: which takes the fen and loads it.
- quit: which ends the game early.

Lastly `set_board` takes a fen string and updates the board. There is error handling of course.