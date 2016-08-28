@echo off

cd _site
git pull
cd ..
cmd /c jekyll build --trace

cd _site
git add .

git commit %*

cd ..
git add _site

git commit %*
