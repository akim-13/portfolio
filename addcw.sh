#!/bin/bash

CW=$1

# Check if a branch name is provided.
if [ -z "$CW" ]; then
  echo "Usage: $0 <coursework-dir-name>"
  exit 1
fi

# Check if the directory exists.
if [ ! -d "../$CW" ]; then
  echo "Error: \"../$CW/\" directory doesn't exist"
  exit 1
fi

# Remove the remote if it already exists.
if git remote | grep -q "$CW"; then
    echo "WARNING: Remote already exists, removing..."
    git remote remove $CW
    echo
fi

echo "git remote add $CW ../$CW"
git remote add $CW ../$CW
echo

echo "Fetch branches from $CW:"
git fetch $CW
echo

echo "Create $CW branch from $CW/master:"
git checkout -b $CW $CW/master
echo

if [ -f ".gitignore" ]; then
    echo "Remove .gitignore:"
    git rm .gitignore
    git commit -m "Remove .gitignore to avoid merge conflict"
    echo
fi

echo "Move everything into $CW/:"
mkdir $CW
for file in * .*; do
  if [ "$file" != "$CW" ]; then
    git mv "$file" "$CW/"
    echo "Moved \"$file\" into $CW/"
  fi
done
echo

echo "Commit the changes:"
git commit -m "Move $CW coursework files into $CW/ directory"
echo

git checkout master
echo

echo "Merge $CW into master, preserving history:"
git merge --allow-unrelated-histories $CW -m "Merge $CW into master"
echo

echo "Move $CW branch reference back to the original commit:"
git branch -f $CW $CW/master
echo

echo "Coursework $CW added successfully. Don't forget to git push --all origin."

