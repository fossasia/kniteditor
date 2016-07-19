#!/bin/bash

set -e

HERE="`dirname \"$0\"`"
cd "$HERE"

echo "# install kivy dependencies"
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer

echo "# install python3"
brew install python3

echo "# install requirements"
python3 -m pip install --upgrade pip
python3 -m pip install --user -I Cython==0.23 --install-option="--no-cython-compile"
USE_OSX_FRAMEWORKS=0 pip3 -m pip install --user kivy
python3 -m pip uninstall -y Cython==0.23
python3 -m pip install --user -r ../requirements.txt
python3 -m pip install --user -r ../test-requirements.txt
python3 -m pip install --user pygame==1.9.2b4
python3 -m pip install --user PyInstaller

./build.sh

