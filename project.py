import os
import argparse
import chess
import chess.engine


def main():
    config = get_args()
    while not board.is_game_over():
        if config.board:
            print(board)
        board.push(get_move())
        board.push(engine.analysis(board, chess.engine.Limit(time=config.time, depth=config.depth)).wait().move)


def get_move():
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


def check_save():
    try:
        with open("autosave.chess", "r") as savefile:
            if (fen := savefile.read()) \
                    and input("Do you want to load the last game?(y/N) ").strip().lower().startswith("y"):
                board.set_fen(fen)
            os.remove("autosave.chess")
    except FileNotFoundError:
        pass


def get_args():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="cli-chess", exit_on_error=False,
                                                              description="a cli chess game to play against stockfish")
    parser.add_argument("-l", "--load", type=str,
                        help="Loads a chess board from a string,\nyou can copy a board by typing save in game")
    parser.add_argument("-b", "--board", action='store_true',
                        help="displays the board before each move,\nalternatively use board command in game")
    parser.add_argument("-t", "--time", default=1, type=int,
                        help="sets the time limit in seconds for the bot,\ndefaults to 1")
    parser.add_argument("-d", "--depth", default=20, type=int,
                        help="sets the depth of analysis limit for the bot,\ndefaults to 20")
    
    args = parser.parse_args()
    if args.load:
        try:
            board.set_fen(args.load)
        except ValueError:
            print("Bad board string")
            raise KeyboardInterrupt
    else:
        check_save()
    return args


def command(move: str):
    match move:
        case "board":
            print(board)
        case "save":
            print(f"To load this later, just pass in \n{board.fen()}\n"
                  "with the [-l | --load] argument or the load in game command")
        case "load":
            try:
                board.set_fen(input("Paste board string here: "))
            except (ValueError, EOFError, KeyboardInterrupt):
                return False
        case _:
            return False
    return True


if __name__ == "__main__":
    board: chess.Board = chess.Board()
    engine: None = None
    
    try:
        engine: chess.engine.SimpleEngine = chess.engine.SimpleEngine.popen_uci("./stockfish")
        main()
    except (EOFError, KeyboardInterrupt):
        with open("autosave.chess", "w+") as autosave:
            autosave.write(board.fen())
    except argparse.ArgumentError as err:
        print(str(err))
    except FileNotFoundError:
        print("Make sure you have stockfish downloaded and added to path or the execution dir")
    
    if engine is not None:
        engine.quit()