import os, argparse, chess, chess.engine


def main() -> None:
    config: argparse.Namespace = get_args()
    
    while not board.is_game_over():
        
        if config.board:
            print(board)
        
        board.push(get_move())
        board.push(bot.analysis(board, chess.engine.Limit(time=config.time, depth=config.depth)).wait().move)


def get_move() -> chess.Move:
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
    
    args: argparse.Namespace = parser.parse_args()
    
    if args.load:
        set_board(args.load)
    else:
        check_autosave()
    
    return args


def check_autosave() -> None:
    try:
        with open("autosave.chess", "r") as savefile:
            
            # noinspection SpellCheckingInspection
            if (fen := savefile.read()) != r"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"\
                    and input("Do you want to load the last game?(y/N) ").strip().lower().startswith("y"):
                set_board(fen)
            os.remove("autosave.chess")
    
    except FileNotFoundError:
        pass


def command(move: str) -> bool:
    match move:
        case "board":
            print(board)
        
        case "save":
            print(f"To load this later, just pass in \n{board.fen()}\n"
                  "with the [-l | --load] argument or the load in game command")
        
        case "load":
            set_board(input("Paste board string here: "))
        
        case "quit":
            raise KeyboardInterrupt
        
        case _:
            return False
    
    return True


def set_board(fen: str) -> None:
    try:
        board.set_fen(fen)
    
    except ValueError:
        print("Bad board string")
        raise KeyboardInterrupt


if __name__ == "__main__":
    board: chess.Board = chess.Board()
    bot: None = None
    
    try:
        bot: chess.engine.SimpleEngine = chess.engine.SimpleEngine.popen_uci("./stockfish")
        main()
    
    except (EOFError, KeyboardInterrupt):
        with open("autosave.chess", "w+") as autosave:
            autosave.write(board.fen())
    
    except argparse.ArgumentError as err:
        print(str(err))
    
    except FileNotFoundError:
        print("Make sure you have stockfish downloaded and added to path or the execution dir")
    
    if bot is not None:
        bot.quit()
