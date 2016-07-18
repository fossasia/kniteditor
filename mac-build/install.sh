HERE="`dirname \"$0\"`"

cd "$HERE"

# I follow this tutorial:
# see https://kivy.org/docs/installation/installation-osx.html
#

## (1) download the kivy app
# see https://kivy.org/docs/installation/installation-osx.html#using-the-kivy-app
# not working
#  cura:mac-installer nicco$ kivy -m pip install -r ../requirements.txt
#  Collecting knittingpattern==0.1.11 (from -r ../requirements.txt (line 1))
#    Using cached knittingpattern-0.1.11.zip
#  dyld: lazy symbol binding failed: Symbol not found: _fdopendir$INODE64
#    Referenced from: /Applications/Kivy.app/Contents/Resources/python
#    Expected in: /usr/lib/libSystem.B.dylib
#
#  dyld: Symbol not found: _fdopendir$INODE64
#    Referenced from: /Applications/Kivy.app/Contents/Resources/python
#    Expected in: /usr/lib/libSystem.B.dylib
#
#wget https://github.com/AllYarnsAreBeautiful/kniteditor/releases/download/kivy-mac-binaries-1/Kivy3.app.zip
#unzip Kivy3.app.zip
#
#wget https://kivy.org/downloads/1.9.1/Kivy-1.9.1-osx-python3.7z
#7z x Kivy-1.9.1-osx-python3.7z
#mv Kivy3.app 
#function kivy() {   "/Applications/Kivy.app/Contents/Resources/script" "$@"; }

##(2) brew
# see https://kivy.org/docs/installation/installation-osx.html#using-homebrew-with-pip
#
#
brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
pip3 install --user -I Cython==0.23 --install-option="--no-cython-compile"
USE_OSX_FRAMEWORKS=0 pip3 install --user kivy
pip3 uninstall -y Cython==0.23
pip3 install --user -r ../requirements.txt
pip3 install --user -r ../test-requirements.txt

# same as the windows build
pip3 install --user pyinstaller
( cd .. ; setup.py sdist ; pip3 install --user dist/kniteditor-*.tar.gz ; )

python3 -m PyInstaller KnitEditor.spec




