#!/usr/bin/env python3
import mido
import sys

parser = mido.Parser()

with mido.open_output("fluidsynth") as out_port:
    while True:
        msg_bytes = sys.stdin.buffer.read(1)
        parser.feed(msg_bytes)
        for msg in parser:
            print(msg)
            out_port.send(msg)
