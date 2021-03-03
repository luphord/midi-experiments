from tkinter import *
from tkinter import ttk
from typing import Tuple
import threading
import mido

major = (0, 2, 4, 5, 7, 9, 11)
minor = (0, 2, 3, 5, 7, 8, 10)

keys = "C C# D D# E F F# G G# A A# B".split()

class Key:
    def __init__(self, base: int, tonality: Tuple[int]):
        self.base = base
        for note in tonality:
            assert note >= 0
            assert note < 12
        self.tonality = tonality + tuple(n + 12 for n in tonality)
    
    def chord(self, msg, steps):
        rel_note = (msg.note - self.base) % 12
        if rel_note in self.tonality:
            for steps in steps:
                rel = self.tonality[(self.tonality.index(rel_note) + steps)]
                yield msg.copy(note=msg.note - rel_note + rel)
    
    def triad(self, msg):
        yield from self.chord(msg, (0, 2, 4))
    
    def tetrad(self, msg):
        yield from self.chord(msg, (0, 2, 4, 6))


class ChordPlayer(ttk.Frame):

    def __init__(self, root):
        super().__init__(root)
        ttk.Label(self, text="Key").grid(row=0, column=0)
        self.key = StringVar(value=keys[0])
        ttk.Combobox(self,
                     textvariable=self.key,
                     state="readonly",
                     values=keys
                     ).grid(row=0, column=1)
        ttk.Label(self, text="Tonality").grid(row=1, column=0)
        self.tonality = StringVar(value="major")
        ttk.Combobox(self,
                     textvariable=self.tonality,
                     state="readonly",
                     values=["major", "minor"]
                     ).grid(row=1, column=1)
        self.maj7 = StringVar()
        ttk.Checkbutton(self,
                        text="maj7",
                        variable=self.maj7,
                        onvalue="on",
                        offvalue="off"
                        ).grid(row=2, column=1)
    
    def play(self):
        with mido.open_input() as in_port, \
             mido.open_output() as out_port:
            for msg in in_port:
                key = 60 + keys.index(self.key.get())
                tonality = major if self.tonality.get() == "major" else minor
                key_obj = Key(key, tonality)
                method = key_obj.tetrad if self.maj7.get() == "on" else key_obj.triad
                for m in method(msg):
                    out_port.send(m)


if __name__ == "__main__":
    root = Tk()
    player = ChordPlayer(root)
    player.grid()
    threading.Thread(target=player.play, daemon=True).start()
    root.mainloop()