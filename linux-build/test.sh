#!/bin/bash

set -e

cd "`dirname \"$0\"`"
cd ..

echo "# Test with pep8 and add coverage."
# The docs folder is also tested.
py.test --cov=kniteditor --pep8

echo "# test import from everywhere"
(
  cd /
  python3 -c "import kniteditor;print(\"Module kniteditor was successfully imported.\")"
)

echo "# run tests from installation"
(
  cd /
  py.test --pyargs kniteditor
)

./test_tag.sh

