#!/data/data/com.termux/files/usr/bin/bash

for wt in $blog $scrdev; do
    pushd ${wt}
    git status --porcelain
    git rev-list --count origin/master..master
    popd
done
