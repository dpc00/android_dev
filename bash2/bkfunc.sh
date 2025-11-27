#!/bin/bash
echo "-- bkfunc.sh --"
function lk {
    #echo "lk $1"
    ! [ -d ${bkx}$1 ] && mkdir ${bkx}$1
}
function unlk {
    #echo "unlk $1"
    [ -d ${bkx}$1 ] && rmdir ${bkx}$1
}
function src {
    return $1
}
function dhs {
    ls -AgGlR --block-size=1 --time-style=+%s $1 | sha256sum
}
function dhck {
    #echo "dhck $1"
    local dhs1=$(cat ${dh}_${1})
    local dhs2=$(dhs ${!1})
    [ "$dhs1" != "$dhs2" ]
}
function dhset {
    #echo "updating ${dh}_${1} from ${!1}"
    dhs ${!1}>${dh}_${1}
}
function bctck {
    #echo "bctck rtbk$2 -nt ct$1"
    [ ${rtbk}${2} -nt ${ct}${1} ]
}
function bctclr {
    #echo "touch ct$1 --reference=rtbk$2"
    touch ${ct}${1} --reference=${rtbk}${2}
}

export -f lk
export -f unlk
export -f src
export -f dhs
export -f dhck
export -f dhset
export -f bctck
export -f bctclr

