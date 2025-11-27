#!/bin/bash

pushd $scrdev
    ctags -x *.sh *.env .bashrc .bashrc0 >x.txt
popd