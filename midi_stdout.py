#!/usr/bin/env python3
import mido
import sys
import time
from random import randint

while True:
    msg = mido.Message(type="note_on", note=randint(60, 72), channel=2)
    sys.stdout.buffer.write(bytes(msg.bytes()))
    sys.stdout.buffer.flush()
    time.sleep(1)
    msg_off = mido.Message(type="note_off", note=msg.note, channel=msg.channel)
    sys.stdout.buffer.write(bytes(msg_off.bytes()))
    sys.stdout.buffer.flush()

