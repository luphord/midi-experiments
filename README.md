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
