from tkinter import *
from tkinter import ttk
from typing import Tuple
import threading
import time
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


class Accompany(ttk.Frame):

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
        ttk.Label(self, text="bpm").grid(row=3, column=0)
        self.bpm = ttk.Spinbox(self,
                               from_=80,
                               to=160,
                               increment=1)
        self.bpm.set(120)
        self.bpm.grid(row=3, column=1)
        ttk.Label(self, text="# beats").grid(row=4, column=0)
        self.nbeats = ttk.Spinbox(self,
                               from_=1,
                               to=12,
                               increment=1)
        self.nbeats.set(4)
        self.nbeats.grid(row=4, column=1)
        ttk.Label(self, text="Channel").grid(row=5, column=0)
        self.channel = ttk.Spinbox(self,
                                   from_=1,
                                   to=12,
                                   increment=1)
        self.channel.set(1)
        self.channel.grid(row=5, column=1)
    
    @property
    def mido_channel(self):
        try:
            return int(self.channel.get()) - 1
        except ValueError:
            return 0
    
    @property
    def key_obj(self):
        key = keys.index(self.key.get())
        tonality = major if self.tonality.get() == "major" else minor
        return Key(key, tonality)
    
    @property
    def chord_method(self):
        return self.key_obj.tetrad if self.maj7.get() == "on" else self.key_obj.triad
    
    def chord(self, message):
        return self.chord_method(message.copy(note=message.note+60))
    
    def play(self):
        with mido.open_output() as out_port:
            while True:
                for degree in (0, 5, 7):
                    for i in range(int(self.nbeats.get())):
                        for m in self.chord(mido.Message(type="note_on", note=degree, channel=self.mido_channel)):
                            out_port.send(m)
                        time.sleep(60 / int(self.bpm.get()))
                        for m in self.chord(mido.Message(type="note_off", note=degree, channel=self.mido_channel)):
                            out_port.send(m)


if __name__ == "__main__":
    root = Tk()
    root.title("Accompany")
    player = Accompany(root)
    player.grid()
    threading.Thread(target=player.play, daemon=True).start()
    root.mainloop()