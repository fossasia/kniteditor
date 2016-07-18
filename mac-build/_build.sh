HERE="`dirname \"$0\"`"

cd "$HERE"


( cd .. ; kivy setup.py sdist ; kivy -m pip install --user dist/kniteditor-*.tar.gz ; )
rm -rf dist

# source /Applications/Kivy.app/Contents/Resources/venv/bin/activate

alias python=/usr/bin/python
ln -s -f /Applications/Kivy.app build/buildozer/osx/platform/kivy-sdk-packager-master/Kivy.app

kivy -m buildozer osx debug

# kivy setup.py py2app || exit 1

# see http://stackoverflow.com/a/367826/1320237
# create the .dmg file
# hdiutil create -srcfolder dist/KnitEditor.app dist/KnitEditor.dmg


