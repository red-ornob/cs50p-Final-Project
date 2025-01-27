import sys
import chess
import pytest
from project import get_move, get_args, command, board


# noinspection SpellCheckingInspection
def test_get_move(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "b1c3")
    assert get_move() == chess.Move.from_uci("b1c3")
    board.push(get_move())
    
    monkeypatch.setattr("builtins.input", lambda _: "d7d5")
    assert get_move() == chess.Move.from_uci("d7d5")
    board.push(get_move())
    
    assert board.fen() == r"rnbqkbnr/ppp1pppp/8/3p4/8/2N5/PPPPPPPP/R1BQKBNR w KQkq - 0 2"


# noinspection SpellCheckingInspection
def test_get_args(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["./project.py", "--board", "-t", "10","-d", "50",
                                      "--load", r"rnb1kbnr/ppp1pppp/8/3q4/8/8/PPPPPPPP/R1BQKBNR w KQkq - 0 3"])
    args = get_args()
    assert args.load == r"rnb1kbnr/ppp1pppp/8/3q4/8/8/PPPPPPPP/R1BQKBNR w KQkq - 0 3"
    assert board.fen() == r"rnb1kbnr/ppp1pppp/8/3q4/8/8/PPPPPPPP/R1BQKBNR w KQkq - 0 3"
    assert args.board is True
    assert args.time == 10
    assert args.depth == 50


# noinspection SpellCheckingInspection
def test_command(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: r"r1bqkbnr/ppp2ppp/2n5/4p3/4P3/3P1N2/PPP2PPP/R1BQKB1R w KQkq - 1 6")
    assert command("load") is True
    assert board.fen() == r"r1bqkbnr/ppp2ppp/2n5/4p3/4P3/3P1N2/PPP2PPP/R1BQKB1R w KQkq - 1 6"
    
    assert command("save") is True
    assert r"r1bqkbnr/ppp2ppp/2n5/4p3/4P3/3P1N2/PPP2PPP/R1BQKB1R w KQkq - 1 6" in capsys.readouterr().out
    
    assert command("board") is True
    assert capsys.readouterr().out == str(board)+"\n"
    
    assert command("dsads") is False
    assert command("") is False
    
    with pytest.raises(KeyboardInterrupt):
        command("quit")
