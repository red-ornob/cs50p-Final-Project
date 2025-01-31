import sys
import pytest
import argparse
import chess
from clichess import get_move, get_args, command

board = chess.Board()


# noinspection SpellCheckingInspection
def test_get_move(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "b1c3")
    assert get_move(board) == chess.Move.from_uci("b1c3")
    board.push(get_move(board))
    
    monkeypatch.setattr("builtins.input", lambda _: "d7d5")
    assert get_move(board) == chess.Move.from_uci("d7d5")
    board.push(get_move(board))
    
    assert board.fen() == r"rnbqkbnr/ppp1pppp/8/3p4/8/2N5/PPPPPPPP/R1BQKBNR w KQkq - 0 2"


# noinspection SpellCheckingInspection
def test_get_args(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["./clichess.py", "--board", "-t", "10","-d", "50", "--play", "2",
                                      "--load", r"rnb1kbnr/ppp1pppp/8/3q4/8/8/PPPPPPPP/R1BQKBNR w KQkq - 0 3"])
    args = get_args()
    assert args.load == r"rnb1kbnr/ppp1pppp/8/3q4/8/8/PPPPPPPP/R1BQKBNR w KQkq - 0 3"
    assert args.board is True
    assert args.time == 10
    assert args.depth == 50
    
    monkeypatch.setattr(sys, "argv", ["./clichess.py", "--board", "-time", "10"])
    with pytest.raises(argparse.ArgumentError):
        get_args()


# noinspection SpellCheckingInspection
def test_command(capsys, monkeypatch):
    assert command("save", board) is True
    assert "\"rnbqkbnr/ppp1pppp/8/3p4/8/2N5/PPPPPPPP/R1BQKBNR w KQkq - 0 2\"" in capsys.readouterr().out
    
    assert command("board", board) is True
    assert capsys.readouterr().out == str(board)+"\n"
    
    assert command("dsads", board) is False
    assert command("", board) is False
    
    with pytest.raises(KeyboardInterrupt):
        command("quit", board)
