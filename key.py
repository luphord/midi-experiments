#!/usr/bin/env python
from typing import Tuple
import mido

major = (0, 2, 4, 5, 7, 9, 11)
minor = (0, 2, 3, 5, 7, 8, 10)

class Key:
    def __init__(self, base: int, tonality: Tuple[int]):
        self.base = base
        for note in tonality:
            assert note >= 0
            assert note < 12
        self.tonality = tonality + tuple(n + 12 for n in tonality)
    
    def triad(self, msg):
        rel_note = (msg.note - self.base) % 12
        if rel_note in self.tonality:
            yield msg
            rel_third = self.tonality[(self.tonality.index(rel_note) + 2)]
            third = msg.copy(note=msg.note - rel_note + rel_third)
            yield third
            rel_fifth = self.tonality[(self.tonality.index(rel_note) + 4)]
            fifth = msg.copy(note=msg.note - rel_note + rel_fifth)
            yield fifth
            print(msg, third, fifth)

with mido.open_input() as in_port, mido.open_output() as out_port:
    for msg in in_port:
        for m in Key(60, major).triad(msg):
            out_port.send(m)