#!/bin/sh

pwd="$(pwd)"

for dir in ./hugo-src/*; do
  cd "$dir" || exit
  hugo
  cd "$pwd" || exit
done
