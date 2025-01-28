import os
import random
import argparse
import chess
import chess.engine


def main() -> None:
    """
    Main function that calls other functions.
    :return: None
    """
    
    config: argparse.Namespace = get_args()
    white, black = set_players(config.play)
    print(f"Playing as {"white" * (white == "user") + "black" * (black == "user")}")
    
    while not board.is_game_over():
        
        if white == "user" and config.board:
            print(board)
        play(white, config)
        
        if black == "user" and config.board:
            print(board)
        play(black, config)


def play(player, config):
    """
    Calls the right function for whose turn it is
    :param player: the player in string
    :param config: the configuration set for the bot
    :return: None
    """
    
    match player:
        case "user":
            board.push(get_move())
        case "bot":
            board.push(bot.analysis(board, chess.engine.Limit(time=config.time, depth=config.depth)).wait().move)


def get_move() -> chess.Move:
    """
    Asks for input from a user and returns the validated move.
    If it is a command, it is executed.
    :return: the inputted validated move as a chess.Move object.
    """
    
    while True:
        try:
            move: str = input(">").strip().lower()
            
            if command(move):
                continue
            
            move: chess.Move = chess.Move.from_uci(move)
            if move in board.legal_moves:
                return move
            print("Illegal move")
        
        except chess.InvalidMoveError:
            print("Invalid move or command")


def get_args() -> argparse.Namespace:
    """
    Defines the arguments for the program, calls the appropriate functions
    :return: the arguments as an argparse.Namespace
    """
    
    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="cli-chess", exit_on_error=False,
                                                              description="a cli chess game to play against stockfish")
    parser.add_argument("-l", "--load", type=str,
                        help="Loads a chess board from a string, you can copy a board by using `save` command in game")
    parser.add_argument("-b", "--board", action='store_true',
                        help="displays the board before each move, alternatively use `board` command in game")
    parser.add_argument("-t", "--time", default=1, type=int,
                        help="sets the time limit in seconds for the bot, defaults to 1")
    parser.add_argument("-d", "--depth", default=20, type=int,
                        help="sets the depth of analysis limit for the bot, defaults to 20")
    parser.add_argument("-p", "--play", default=0, type=int, choices=range(3),
                        help="selects which colour to play as. 0: random [default] 1: white 2: black")
    
    args: argparse.Namespace = parser.parse_args()
    
    
    if args.load:
        set_board(args.load)
    else:
        check_autosave()
    
    return args


def set_players(mode: int) -> list[str]:
    """
    Sets the white and black players.
    :param mode: The user inputted mode.
    :return: a list of the order of turns.
    """
    
    match mode:
        case 0:
            players = ["user", "bot"]
            random.shuffle(players)
            return players
        case 1:
            return ["user", "bot"]
        case 2:
            return ["bot", "user"]


def check_autosave() -> None:
    """
    Checks if there is an autosave and prompts before loading it.
    :return: None
    """
    
    try:
        with open("autosave.chess", "r") as savefile:
            
            # noinspection SpellCheckingInspection
            if (fen := savefile.read()) != r"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"\
                    and input("Do you want to load the last game?(y/N) ").strip().lower().startswith("y"):
                set_board(fen)
            os.remove("autosave.chess")
    
    except FileNotFoundError:
        pass


def command(string: str) -> bool:
    """
    Checks if a string is a set command.
    :param string: the string to be checked.
    :return: if the string is a command or not.
    """
    
    match string:
        case "board":
            print(board)
        
        case "save":
            print(f"To load this later, just pass in \n{board.fen()}\n"
                  "with the [-l | --load] argument or the `load` in game command")
        
        case "load":
            set_board(input("Paste board string here: "))
        
        case "quit":
            raise KeyboardInterrupt
        
        case _:
            return False
    
    return True


def set_board(fen: str) -> None:
    """
    Sets the board to state of the passed fen.
    :param fen: fen of a board as a string
    :return: None
    """
    
    try:
        board.set_fen(fen)
    
    except ValueError:
        print("Bad board string")
        raise KeyboardInterrupt


board: chess.Board = chess.Board()
if __name__ == "__main__":
    bot: None = None
    
    try:
        bot: chess.engine.SimpleEngine = chess.engine.SimpleEngine.popen_uci("./stockfish")
        main()
    
    except (EOFError, KeyboardInterrupt, SystemExit, chess.engine.EngineError):
        with open("autosave.chess", "w+") as autosave:
            autosave.write(board.fen())
    
    except argparse.ArgumentError as err:
        print(str(err))
    
    except FileNotFoundError:
        print("Make sure you have stockfish downloaded and added to path or the execution dir")
    
    if bot is not None:
        bot.quit()
