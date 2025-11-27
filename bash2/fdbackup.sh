#!/bin/bash
echo "-- fdbackup.sh --"
rc=0

[ -d $blog/dist ] || mkdir $blog/dist
rc=$(($rc + $?))

if ! [ -f ~/Finance.db ] ||
    [ /sdcard/documents/Finance.db -nt ~/Finance.db ]; then
    cp -u -p /sdcard/documents/Finance.db ~
fi
rc=$(($rc + $?))

if ! [ -f $blog/dist/Finance.db ] ||
    [ /sdcard/documents/Finance.db -nt $blog/dist/Finance.db ]; then
    cp -u -p /sdcard/documents/Finance.db $blog/dist
fi
rc=$(($rc + $?))

echo fdb: $rc
src $rc
