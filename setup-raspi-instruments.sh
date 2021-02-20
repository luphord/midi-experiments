#!/bin/sh

# Setup a Raspberry Pi (Zero) for the MIDI touch instruments

sudo apt update
sudo apt install -y fluidsynth git python3-pip python3-dev libasound2-dev libjack0 libjack-dev

git clone https://github.com/luphord/midi-experiments.git
cd midi-experiments
pip3 install --user -r requirements.txt

cd ~/Downloads
wget https://github.com/joewalnes/websocketd/releases/download/v0.4.1/websocketd-0.4.1-linux_arm.zip
unzip websocketd-0.4.1-linux_arm.zip websocketd
chmod +x websocketd
sudo mv websocketd /usr/bin

echo '# MIDI touch instruments' >> ~/.bashrc
echo 'fluidsynth -a alsa -p fluidsynth /usr/share/sounds/sf2/FluidR3_GM.sf2 --server &' >> ~/.bashrc
echo 'git -C ~/midi-experiments pull' >> ~/.bashrc
echo 'websocketd --binary --port 8080 --staticdir ~/midi-experiments/midi-touch-instruments ~/midi-experiments/midi_stdin.py &' >> ~/.bashrc
