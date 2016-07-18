#!/bin/bash

HERE="`dirname \"$0\"`"

cd "$HERE"


brew uninstall sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
brew uninstall python3
rm -rf ~/Library/Python/

rm -rf dist build


