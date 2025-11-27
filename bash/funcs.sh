#!/data/data/com.termux/files/usr/bin/bash
# echo "-- bkfunc.sh --"
function lk() {
    #echo "lk $1"
    ! [ -d ${bkx}$1 ] && mkdir ${bkx}$1
}
function unlk() {
    #echo "unlk $1"
    [ -d ${bkx}$1 ] && rmdir ${bkx}$1
}

function clr {
    if ! [ bctck $1 $2 ]; then
        echo "clearing ct$1 from rtbk$2"
        bctclr $1 $2
    fi
}

function ts2 {
   local _n2=$3
   local _n1=$4
   eval $_n2="'${dstts["$1,$2"]}'"
   eval $_n1="'${srcts["$2"]}'"
}

function prefn {
    local _rv=$3
    eval $_rv="'${!1}$2'"
}

function dhfn {
    local _rv=$2
    eval $_rv="'${dh}_${1}'"
}

function bctck() {
    # echo "bctck rtbk$2 -nt ct$1"
    [ ${rtbk}${2} -nt ${ct}${1} ]
}

function bctclr() {
    # echo "touch ct$1 --reference=rtbk$2"
    touch ${ct}${1} --reference=${rtbk}${2}
}

function rtset {
    local fn1
    prefn rtbk $1 fn1
    # echo "touching $fn1"
    touch $fn1
}


function src() {
    return $1
}

function dhs() {
    ls -AgGlR --block-size=1 --time-style=+%s --color=never $1 | sha256sum
}

function dhck() {
    # echo "dhck $1"
    local dhs1=$(<${dh}_${1})
    local dhs2=$(dhs ${pdir["$1"]})
    [ "${dhs1}" == "${dhs2}" ]
}
function dhset() {
    # echo "updating ${dh}_${1} from ${pdir[${1}]}"
    dhs ${pdir["$1"]} >${dh}_${1}
}

export -f lk
export -f unlk
export -f src
export -f dhs
export -f dhck
export -f dhset
export -f bctck
export -f bctclr
