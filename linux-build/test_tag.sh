#!/bin/bash

set -e

cd "`dirname \"$0\"`"

TAG_NAME="`./tag_name`"

echo "# test that the tag represents the version"
# https://docs.travis-ci.com/user/environment-variables/#Default-Environment-Variables
if [ -n "$TRAVIS_TAG" ]
then
  if [ "$TAG_NAME" != "$TRAVIS_TAG" ]
  then
    echo "ERROR: This tag is for the wrong version. Got \"$TRAVIS_TAG\" but expected \"$TAG_NAME\"."
    exit 1
  else
    echo "OK: Tag matches version."
  fi
else
  echo "OK: Untagged build."
fi





