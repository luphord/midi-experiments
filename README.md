# midi-experiments
Experiments with MIDI and Python.

## Installation

Ensure that the following system packages are installed:

    sudo apt install python3-dev libasound2-dev libjack0 libjack-dev

Then run (ideally within a virtual environment)

    pip install -r requirements.txt

## FluidSynth

Before running any of the programs in this repo, start [FluidSynth](https://www.fluidsynth.org) by 

    fluidsynth -a alsa -p fluidsynth /usr/share/sounds/sf2/FluidR3_GM.sf2

## MIDI over Websockets

Using [websocketd](https://github.com/joewalnes/websocketd) you can send MIDI messages
from a web page via websockets and pipe them into `midi_stdin.py` to forward them to `fluidsynth`.

    websocketd --binary --devconsole --port 8080 ./midi_stdin.py

Try running the following JavaScript code in your browser's dev console:

    ws.send(new Uint8Array([ 144, 62, 80 ]))