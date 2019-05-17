#!/usr/bin/env bash

shopt -s extglob

./generate_previews.py
./maketree.py

find -type f -size +50M > ./.gitignore

echo "*~" >>  ./.gitignore

echo "THE FOLLOWING LARGE FILES ARE NOT TRACKED"
cat ./.gitignore
echo "THESE FILES ARE NOT TRACKED"

#git add -A

echo "Adding new files..."
git add . 

echo "Tracking updates..."
git add -u

# For some reason the above "git add" commands managed to ignore 
# .gitignore (really!). 

# hopefully removes everything that shouldn't be being tracked as per
# .gitignore. Possibly dangerous. 
echo "Untracking files matching .gitignore..."
cat .gitignore | awk "/^[.\*]/" | sed 's/"/"\\""/g;s/.*/"&"/' |  xargs -E '' -I{} git rm -rf --cached {}

echo "Committing..."
# :/
git commit -m "$1"

echo "Pushing to origin master..."
git push origin master
