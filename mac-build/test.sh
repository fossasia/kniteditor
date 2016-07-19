#!/bin/bash

set -e

cd "`dirname \"$0\"`"

echo "# execute the tests in the built binary"
dist/KnitEditor.app/Contents/MacOS/KnitEditorX /test

echo "# test that there is a binary"
test -f dist/KnitEditor.dmg

../linux-build/test_tag.sh
