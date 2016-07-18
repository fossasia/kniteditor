#!/bin/bash


HERE="`dirname \"$0\"`"

cd "$HERE"

python3 -m pip uninstall -y kniteditor
( cd .. ; python3 setup.py sdist ; python3 -m pip install --user --upgrade dist/kniteditor-*.tar.gz ; )

python3 -m pip install --user --upgrade -r ../test-requirements.txt

python3 -m PyInstaller KnitEditor.spec || exit 1

# see http://stackoverflow.com/a/367826/1320237
# create the .dmg file
rm -f dist/KnitEditor.dmg
hdiutil create -srcfolder dist/KnitEditor.app dist/KnitEditor.dmg

