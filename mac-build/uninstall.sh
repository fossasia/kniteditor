#!/bin/bash

HERE="`dirname \"$0\"`"

cd "$HERE"

brew uninstall sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
brew uninstall python3
brew uninstall sdl sdl_image sdl_mixer sdl_ttf smpeg portmidi
brew uninstall mercurial
rm -rf ~/Library/Python/

