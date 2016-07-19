#!/bin/bash

set -e

cd "`dirname \"$0\"`"

echo "# Test with pep8 and add coverage."
# The docs folder is also tested.
(
  cd ..
  py.test --cov=kniteditor --pep8
)

(
  cd /

  echo "# test import from everywhere"
  python3 -c "import kniteditor;print(\"Module kniteditor was successfully imported.\")"

  echo "# run tests from installation"
  py.test --pyargs kniteditor
)

./test_tag.sh

