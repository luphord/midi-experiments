#!/usr/bin/env python
from dataclasses import dataclass
from typing import List, Iterable, Tuple
from abc import ABC, abstractmethod
from itertools import chain
import time
import mido
from mido import Message

major_halftones = (0, 2, 4, 5, 7, 9, 11)
minor_halftones = (0, 2, 3, 5, 7, 8, 10)

keys = "C C# D D# E F F# G G# A A# B".split()


class Key:
    def __init__(self, base: int, halftones: Tuple[int]):
        self.base = base
        for note in halftones:
            assert note >= 0
            assert note < 12
        self.halftones = halftones + tuple(n + 12 for n in halftones)

    def chord(self, msg, steps):
        rel_note = (msg.note - self.base) % 12
        if rel_note in self.halftones:
            for steps in steps:
                rel = self.halftones[(self.halftones.index(rel_note) + steps)]
                yield msg.copy(note=msg.note - rel_note + rel)

    def triad(self, msg):
        yield from self.chord(msg, (0, 2, 4))

    def tetrad(self, msg):
        yield from self.chord(msg, (0, 2, 4, 6))

    def noteonstep(self, step):
        return self.halftones[step] + self.base

    def harmony_on(self, harmony: int, channel: int, velocity: int, time: int):
        yield from piece.key_obj.triad(
            Message(
                type="note_on",
                note=self.noteonstep(harmony) + 60,
                channel=channel,
                velocity=velocity,
                time=time,
            )
        )


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

    @property
    def key_obj(self):
        return Key(
            keys.index(self.key),
            major_halftones if self.tonality == "major" else minor_halftones,
        )


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


class BasicChordProgression(Track):
    def bars(self, piece: Piece) -> Iterable[List[Message]]:
        while True:
            for harmony in piece.progression:
                yield list(piece.key_obj.harmony_on(harmony, 0, 90, 0.0))


class BasicBassLine(Track):
    def notesonbeat(self, piece, step):
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
                type="note_on",
                note=piece.key_obj.noteonstep(step) + 36,
                channel=15,
                velocity=velocity,
                time=time,
            )

    def bars(self, piece: Piece) -> Iterable[List[Message]]:
        while True:
            for harmony in piece.progression:
                yield list(self.notesonbeat(piece, harmony))


if __name__ == "__main__":
    piece = Piece(4, 100, "G", "major", [0, 3, 4])
    Player(
        piece, [Beats(), OffBeats(), BasicChordProgression(), BasicBassLine()]
    ).play()
