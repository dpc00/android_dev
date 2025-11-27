#!/bin/bash
echo "-- csbackup.sh --"

# csname projsubdir
function csb {
    echo "csb $1 $2"
    local spn=$1
    local pjd=$2
    netup.sh &&
    echo "$pjd -> $spn" &&
    rclone sync $proj/$pjd $spn:/projects/$pjd --progress --exclude .git/** --delete-excluded
}
function oneps {
    echo "oneps $1 $2 $3 $4"
    bctck $1 $2 &&
        (   csb $3 $4 &&
            bctclr $1 $2
        )
    ! bctck $1 $2
}
function r_cs {
    local vrc=0
    local v1k=4
    for v2i in DropBox GoogleDrive OneDrive; do
        local v3l=3
        for v4j in blog bash2 python; do
            oneps $v1k $v3l $v2i $v4j
            vrc=$(($vrc + $?))
            v1k=$(($v1k + 1))
            v3l=$(($v3l + 1))
        done
    done
    unset v2i v4j v1k v3l
    echo "r_cs rc: $vrc"
    src $vrc
}
r_cs
rc=$?
echo csb: $rc
src $rc

