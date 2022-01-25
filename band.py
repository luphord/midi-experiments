#!/usr/bin/env python
from dataclasses import dataclass

bars = "4/4 3/4 6/8".split()
keys = "C C# D D# E F F# G G# A A# B".split()

@dataclass
class Piece:
    """Core configuration of a piece of music.
    Expected to be 'modified' during performance,
    but realized as immutable structure.

    >>> Piece("4/4", 100, "G", "major")
    Piece(bar='4/4', bpm=100, key='G', tonality='major')
    """
    bar: str
    bpm: int
    key: str
    tonality: str
