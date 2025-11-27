#!/bin/bash

echo "-- agb1.sh --"
# em=cymndDM
sleep 2

function r_scpy {
    bctck 1 4 &&
    (   scpy.sh &&
        bctclr 1 4
        )
    ! bctck 1 4
}

function r_fdbackup {
    bctck 2 1  &&
    (   fdbackup.sh && 
        bctclr 2 1
        )
    ! bctck 2 1
}

function r_csbackups {
    bctck 3 2 &&
    (   csbackup.sh &&
        bctclr 3 2
        )
    ! bctck 3 2
}

function status {
    local rc=0
    if dhck fdb; then
        rc=$(($rc | 1))
    fi
    if dhck blog; then
        rc=$(($rc | 2))
    fi
    if dhck scrdev; then
        rc=$(($rc | 4))
    fi
    if dhck pyth; then
        rc=$(($rc | 8))
    fi
    src $rc
}

function inw1 {
    status
    local rc=$?
    if [ $(($rc & 1)) -ne 0 ]; then
        echo "fdb changed"
        touch ${rtbk}1
        r_fdbackup &&
        dhset fdb
    fi
    status
    local rc=$?
    if [ $(($rc & 2)) -ne 0 ]; then
        echo "blog changed"
        touch ${rtbk}2
        touch ${rtbk}3
        dhset blog
    fi
    status
    local rc=$?
    if [ $(($rc & 4)) -ne 0 ]; then
        echo "scrdev changed"
        touch ${rtbk}2
        touch ${rtbk}4
        r_scpy &&
        dhset scrdev
    fi
    status
    local rc=$?
    if [ $(($rc & 8)) -ne 0 ]; then
        echo "pyth changed"
        touch ${rtbk}2
        touch ${rtbk}5
        r_scpy &&
        dhset pyth
    fi
    r_csbackups
}

inw1
echo "agb1 rc: $?"
