#!/bin/bash

HERE="`dirname \"$0\"`"

cd "$HERE"

brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
brew install python3
pyhon3 -m pip install --user -I Cython==0.23 --install-option="--no-cython-compile"
USE_OSX_FRAMEWORKS=0 pip3 -m pip install --user kivy
python3 -m pip uninstall -y Cython==0.23
python3 -m pip install --user -r ../requirements.txt
python3 -m pip install --user -r ../test-requirements.txt
python3 -m pip install --user pygame==1.9.2b4

