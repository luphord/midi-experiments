#!/usr/bin/env python
import mido

def major(msg):
    yield msg
    yield msg.copy(note=msg.note+4)
    yield msg.copy(note=msg.note+7)

with mido.open_input() as in_port, mido.open_output() as out_port:
    for msg in in_port:
        print(msg)
        for m in major(msg):
            out_port.send(m)