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
brew install wget p7zip
wget https://kivy.org/downloads/1.9.1/Kivy-1.9.1-osx-python3.7z
7z x Kivy-1.9.1-osx-python3.7z
mv Kivy3.app /Applications/Kivy.app
ln -s /Applications/Kivy.app/Contents/Resources/script /usr/local/bin/kivy

##(2) brew
# see https://kivy.org/docs/installation/installation-osx.html#using-homebrew-with-pip
#
#
#brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
#pip3 install --user -I Cython==0.23 --install-option="--no-cython-compile"
#USE_OSX_FRAMEWORKS=0 pip3 install --user kivy
#pip3 uninstall -y Cython==0.23
kivy -m pip install --user -r ../requirements.txt
kivy -m pip install --user -r ../test-requirements.txt
kivy -m pip install --user py2app==0.10

# (3) buildozer
# see https://kivy.org/docs/guide/packaging-osx.html#using-buildozer

pip install virtualenv

kivy -m pip install --user git+http://github.com/kivy/buildozer
kivy -m pip install --user docopt sh

sudo /usr/bin/python -m easy_install pip
sudo /usr/bin/python -m pip install docopt sh

