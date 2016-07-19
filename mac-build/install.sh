#!/bin/bash
#
# execute with --user to pip install in the user home
#
set -e

HERE="`dirname \"$0\"`"
USER="$1"
cd "$HERE"

echo "# install python3"
brew install python3
python3 -m pip install --upgrade pip

echo "# install pygame"
# see https://bitbucket.org/pygame/pygame/issues/82/homebrew-on-leopard-fails-to-install#comment-636765
brew install sdl sdl_image sdl_mixer sdl_ttf portmidi
brew install mercurial
python3 -m pip install $USER hg+http://bitbucket.org/pygame/pygame

echo "# install kivy dependencies"
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer

echo "# install requirements"
python3 -m pip install $USER -I Cython==0.23 --install-option="--no-cython-compile"
USE_OSX_FRAMEWORKS=0 python3 -m pip install $USER kivy
python3 -m pip uninstall -y Cython==0.23
python3 -m pip install $USER -r ../requirements.txt
python3 -m pip install $USER -r ../test-requirements.txt
python3 -m pip install $USER PyInstaller

./build.sh $USER

