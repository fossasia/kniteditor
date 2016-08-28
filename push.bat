@echo off 

git push
if ERRORLEVEL 1 GOTO eof

cd _site
git push
cd ..
