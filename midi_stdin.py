#!/usr/bin/env python
import mido
import sys

with mido.open_output("Synth input port (2986:0)") as out_port:
    while True:
        msg_bytes = sys.stdin.buffer.read(3)
        msg = mido.Message.from_bytes(msg_bytes)
        print(msg)
        out_port.send(msg)
