#!/bin/bash


HERE="`dirname \"$0\"`"

cd "$HERE"

( cd .. ; kivy setup.py sdist ; kivy -m pip install --user dist/kniteditor-*.tar.gz ; )

python3 -m pip install --user ../test-requirements.txt

# see http://stackoverflow.com/a/367826/1320237
# create the .dmg file
hdiutil create -srcfolder dist/KnitEditor.app dist/KnitEditor.dmg

