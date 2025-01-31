import os
import random
import argparse
import chess
import chess.engine


def init() -> None:
    """Initiation for the program."""
    
    board: chess.Board = chess.Board()
    bot: None = None
    
    try:
        bot: chess.engine.SimpleEngine = chess.engine.SimpleEngine.popen_uci("./stockfish")
        main(board, bot)
    
    except (EOFError, KeyboardInterrupt, SystemExit, chess.engine.EngineError):
        with open("autosave.chess", "w+") as autosave:
            autosave.write(board.fen())
    
    except argparse.ArgumentError as err:
        print(str(err))
    
    except FileNotFoundError:
        print("Make sure you have stockfish downloaded and added to path or the execution dir")
    
    if bot is not None:
        bot.quit()


def main(board: chess.Board, bot: chess.engine.SimpleEngine) -> None:
    """
    Main function that calls other functions.
    :return: None
    """
    
    config: argparse.Namespace = get_args()
    
    white, black = set_players(config, board)
    print(f"Playing as {"white" * (white == "user") + "black" * (black == "user")}")
    
    while not board.is_game_over():
        match board.turn:
        
            case chess.WHITE:
                if white == "user" and config.board:
                    print(board)
                play(white, board, bot, config)
        
            case chess.BLACK:
                if black == "user" and config.board:
                    print(board)
                play(black, board, bot, config)
    
    match board.outcome().winner:
        case chess.WHITE:
            print(f"{white.capitalize()} won!")
        case chess.BLACK:
            print(f"{black.capitalize()} won!")
        case _:
            print(f"Draw!")


def play(player: str, board: chess.Board, bot: chess.engine.SimpleEngine, config: argparse.Namespace) -> None:
    """
    Calls the right function for whose turn it is
    :param player: the player in string
    :param board: The chess board.
    :param bot: The chess bot.
    :param config: the configuration set for the bot
    :return: None
    """
    
    match player:
        case "user":
            board.push(get_move(board))
        case "bot":
            move = bot.analysis(board, chess.engine.Limit(time=config.time, depth=config.depth)).wait().move
            board.push(move)
            print(f"bot: {move}")


def get_move(board: chess.Board) -> chess.Move:
    """
    Asks for input from a user and returns the validated move.
    If it is a command, it is executed.
    :param board: The chess board.
    :return: the inputted validated move as a chess.Move object.
    """
    
    while True:
        try:
            move: str = input(">").strip().lower()
            
            if command(move, board):
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
    
    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="python clichess.py", exit_on_error=False,
                                                              description="a cli chess game to play against stockfish")
    parser.add_argument("-l", "--load", type=str,
                        help="loads a chess board from a string, you can copy a board with the save command")
    parser.add_argument("-b", "--board", action='store_true',
                        help="displays the board before each move, alternatively use `board` command in game")
    parser.add_argument("-t", "--time", default=1, type=float,
                        help="sets the time limit in seconds for the bot, defaults to 1")
    parser.add_argument("-d", "--depth", default=20, type=int,
                        help="sets the depth of analysis limit for the bot, defaults to 20")
    parser.add_argument("-p", "--play", default=0, type=int, choices=range(3),
                        help="selects which colour to play as. 0: random [default] 1: white 2: black")
    
    return parser.parse_args()


def set_players(config: argparse.Namespace, board: chess.Board) -> list[str]:
    """
    Sets the white and black players.
    :param config: User set configurations.
    :param board: The active board.
    :return: a list of the order of turns.
    """
    
    loaded = load_if(config.load, board)
    if loaded:
        if board.turn == chess.WHITE:
            return ["user", "bot"]
        else:
            return ["bot", "user"]
    
    match config.play:
        case 0:
            players = ["user", "bot"]
            random.shuffle(players)
            return players
        case 1:
            return ["user", "bot"]
        case 2:
            return ["bot", "user"]


def load_if(fen: str, board: chess.Board) -> bool:
    """
    Loads a fen if needed.
    :param fen: The fen loaded.
    :param board: The current board.
    :return: a status bool.
    """
    
    if fen:
        set_board(fen, board)
    elif not check_autosave(board):
        return False
    return True


def check_autosave(board: chess.Board) -> bool:
    """
    Checks if there is an autosave and prompts before loading it.
    :param board: The chess board.
    :return: The status of if the board was loaded.
    """
    
    status = False
    try:
        with open("autosave.chess", "r") as savefile:
            
            # noinspection SpellCheckingInspection
            if (fen := savefile.read()) != r"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"\
                    and input("Do you want to load the last game?(y/N) ").strip().lower().startswith("y"):
                set_board(fen, board)
                status = True
            os.remove("autosave.chess")
    
    except FileNotFoundError:
        pass
    return status


def command(string: str, board: chess.Board) -> bool:
    """
    Checks if a string is a set command.
    :param string: the string to be checked.
    :param board: The chess board.
    :return: if the string is a command or not.
    """
    
    match string:
        case "board":
            print(board)
        
        case "save":
            print(f"To load this later, just pass in the string with the load argument"
                  f"\n\"{board.fen()}\"")
        
        case "quit":
            raise KeyboardInterrupt
        
        case _:
            return False
    
    return True


def set_board(fen: str, board: chess.Board) -> None:
    """
    Sets the board to state of the passed fen.
    :param fen: fen of a board as a string.
    :param board: The chess board.
    :return: None
    """
    
    try:
        board.set_fen(fen)
    
    except ValueError:
        print("Bad board string")
        raise KeyboardInterrupt


if __name__ == '__main__':
    init()
