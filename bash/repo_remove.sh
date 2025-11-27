#!/data/data/com.termux/files/usr/bin/bash

git filter-branch -f  --index-filter "git rm -rf --cached --ignore-unmatch '$1'" HEAD