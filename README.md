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

You can also start `fluidsynth` as a tcp server to accept MIDI input via the network by

    fluidsynth -a alsa -p fluidsynth /usr/share/sounds/sf2/FluidR3_GM.sf2 --server

The default port will be `9800` and the data format appears to
[*not* be binary MIDI](https://fluid-dev.nongnu.narkive.com/ovSZ8tNW/how-to-send-manual-midi-commands-to-fluidsynth-from-another-program#post2)
but rather a textual representation of the commands:

    noteon 1 60 64
    noteoff 1 60 64

Note that a linebreak (`\n`) is required for `fluidsynth` to accept the command.

If you want to run `fluidsynth` in the background, i.e. send it to background with `&`,
make sure that you pass `-i/--no-shell` and `-s/--server`. Both options are required
in this case, even if you do not want to listen to tcp.

## MIDI over Websockets

Using [websocketd](https://github.com/joewalnes/websocketd) you can send MIDI messages
from a web page via websockets and pipe them into `midi_stdin.py` to forward them to `fluidsynth`.

    websocketd --binary --port 8080 --devconsole ./midi_stdin.py

Try running the following JavaScript code in your browser's dev console:

    ws.send(new Uint8Array([ 144, 62, 80 ]))

## MIDI Touch Instruments

To start the MIDI touch instruments run

    websocketd --binary --port 8080 --staticdir ./midi-touch-instruments ./midi_stdin.py