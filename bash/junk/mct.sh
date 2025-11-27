#!/data/data/com.termux/files/usr/bin/bash

pushd $scrdev
ctags -x *.sh *.env .bashrc >x.txt
popd
