#!/bin/bash

set -e

cd "`dirname \"$0\"`"

PACKAGE_VERSION="`./package_version`"
TAG_NAME="`./tag_name`"

cd ..

# https://docs.travis-ci.com/user/installing-dependencies/
# install kivy https://kivy.org/docs/installation/installation-linux.html
# see the cython package https://pypi.python.org/pypi/Cython
echo "# install Cython to build kivy"
python3 -m pip install --user Cython --install-option="--no-cython-compile"
python3 -m pip install --user kivy
python3 -m pip install --user kivy-garden

echo "# build the distribution"
python3 -m pip install --user wheel
python3 setup.py sdist --formats=zip
python3 setup.py bdist_wheel
python3 -m pip uninstall -y wheel

echo "# install from the zip file to see if files were forgotten"
python3 -m pip install --user dist/kniteditor-${PACKAGE_VERSION}.zip

echo "# install the test requirements"
python3 -m pip install -r test-requirements.txt

echo "# remove the build folder because it creates problems for py.test"
rm -rf build

echo "# show the versions"
echo -n "setup.py --version: "
python3 setup.py --version
echo -n "py.test --version"
py.test --version
echo -n "requirements: "
python3 setup.py requirements
echo "Package version $PACKAGE_VERSION with possible tag name $TAG_NAME"



