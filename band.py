#!/usr/bin/env python
from dataclasses import dataclass
from typing import List, Iterable
from abc import ABC, abstractmethod
from itertools import chain
import time
import mido
from mido import Message

bars = "4/4 3/4 6/8".split()
keys = "C C# D D# E F F# G G# A A# B".split()


@dataclass
class Piece:
    """Core configuration of a piece of music.
    Expected to be 'modified' during performance.

    >>> Piece("4/4", 100, "G", "major", [1, 4, 5])
    Piece(bar='4/4', bpm=100, key='G', tonality='major', progression=[1, 4, 5])
    """

    bar: str
    bpm: int
    key: str
    tonality: str
    progression: List[int]


class Track(ABC):
    @abstractmethod
    def bars(self, piece: Piece) -> Iterable[List[Message]]:
        pass


def open_default_port():
    for name in mido.get_output_names():
        if "fluid" in name.lower():
            return mido.open_output(name)
    return mido.open_output()


def barlength(beatsperbar, bpm):
    return beatsperbar * 60 / bpm


@dataclass
class Player:
    piece: Piece
    tracks: List[Track]

    def play(self):
        with open_default_port() as out_port:
            for bars in zip(*[track.bars(self.piece) for track in self.tracks]):
                beatsperbar = 4
                barlen = barlength(beatsperbar, piece.bpm)
                messages = [
                    msg
                    for msg in sorted(chain(*bars), key=lambda msg: msg.time)
                    if msg.time <= barlen
                ]
                bartime = 0.0
                for msg in messages:
                    time.sleep(msg.time - bartime)
                    bartime = msg.time
                    out_port.send(msg)
                time.sleep(barlen - bartime)


class Beats(Track):
    def bars(self, piece: Piece) -> Iterable[List[Message]]:
        while True:
            yield list(self.next_bar(piece))

    def next_bar(self, piece: Piece) -> Iterable[Message]:
        barlen = barlength(4, piece.bpm)
        yield Message(type="note_on", note=60, channel=9, velocity=90, time=0)
        yield Message(
            type="note_on", note=60, channel=9, velocity=60, time=0.25 * barlen
        )
        yield Message(
            type="note_on", note=60, channel=9, velocity=60, time=0.5 * barlen
        )
        yield Message(
            type="note_on", note=60, channel=9, velocity=60, time=0.75 * barlen
        )


class OffBeats(Beats):
    def next_bar(self, piece: Piece) -> Iterable[Message]:
        barlen = barlength(4, piece.bpm)
        yield Message(
            type="note_on", note=61, channel=9, velocity=50, time=0.125 * barlen
        )
        yield Message(
            type="note_on", note=61, channel=9, velocity=50, time=0.375 * barlen
        )
        yield Message(
            type="note_on", note=61, channel=9, velocity=50, time=0.625 * barlen
        )
        yield Message(
            type="note_on", note=61, channel=9, velocity=50, time=0.875 * barlen
        )


if __name__ == "__main__":
    piece = Piece("4/4", 100, "G", "major", [1, 4, 5])
    Player(piece, [Beats(), OffBeats()]).play()
