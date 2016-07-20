#!/bin/bash
#
# execute with --user to make pip install in the user home
#
set -e

HERE="`dirname \"$0\"`"
USER="$1"
cd "$HERE"

(
  cd ..

  echo "# removing old installation of kniteditor"
  python3 -m pip uninstall -y kniteditor || true

  echo "# build the distribution"
  python3 -m pip install $USER wheel
  python3 setup.py sdist --formats=zip
  python3 setup.py bdist_wheel
  python3 -m pip uninstall -y wheel

  echo "# install the current version from the build"
  python3 -m pip install $USER --upgrade dist/kniteditor-`linux-build/package_version`.zip

  echo "# install test requirements"
  python3 -m pip install $USER --upgrade -r test-requirements.txt
)

echo "# build the app"
# see https://pythonhosted.org/PyInstaller/usage.html
python3 -m PyInstaller -d -y KnitEditor.spec

echo "# create the .dmg file"
# see http://stackoverflow.com/a/367826/1320237
KNITEDITOR_DMG="`pwd`/dist/KnitEditor.dmg"
rm -f "$KNITEDITOR_DMG"
hdiutil create -srcfolder dist/KnitEditor.app "$KNITEDITOR_DMG"

echo "The installer can be found in \"$KNITEDITOR_DMG\"."

