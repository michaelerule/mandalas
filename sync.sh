#!/usr/bin/env bash

shopt -s extglob

./maketree.py

git add . 
git add -u :/
git commit -m "$1"
git push origin master
