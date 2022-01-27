#!/usr/bin/env python
from dataclasses import dataclass
from typing import List, Iterable, Tuple
from abc import ABC, abstractmethod
from itertools import chain
import time
import mido
from mido import Message

keys = "C C# D D# E F F# G G# A A# B".split()


@dataclass
class Piece:
    """Core configuration of a piece of music.
    Expected to be 'modified' during performance.

    >>> Piece(4, 100, "G", "major", [1, 4, 5])
    Piece(beatsperbar=4, bpm=100, key='G', tonality='major', progression=[1, 4, 5])
    """

    beatsperbar: int
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
                barlen = barlength(piece.beatsperbar, piece.bpm)
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
        barlen = barlength(piece.beatsperbar, piece.bpm)
        stress = 3 if piece.beatsperbar % 3 == 0 else 2
        for i in range(piece.beatsperbar):
            time = i / piece.beatsperbar * barlen
            if i == 0:
                velocity = 90
            elif i % stress == 0:
                velocity = 75
            else:
                velocity = 60
            yield Message(
                type="note_on", note=60, channel=9, velocity=velocity, time=time
            )


class OffBeats(Beats):
    def next_bar(self, piece: Piece) -> Iterable[Message]:
        barlen = barlength(piece.beatsperbar, piece.bpm)
        for i in range(piece.beatsperbar):
            time = (i + 0.5) / piece.beatsperbar * barlen
            yield Message(type="note_on", note=61, channel=9, velocity=50, time=time)


if __name__ == "__main__":
    piece = Piece(4, 100, "G", "major", [1, 4, 5])
    Player(piece, [Beats(), OffBeats()]).play()
