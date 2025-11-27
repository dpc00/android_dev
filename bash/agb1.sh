#!/data/data/com.termux/files/usr/bin/bash
echo "-- agb1.sh --"
source /sdcard/projects/bash/gb.env

# em=cymndDM

function r_fdbackup() {
    if bctck ${dstts["blog,fdb"]} ${srcts["fdb"]}; then
        fdbackup.sh &&
            bctclr ${dstts["blog,fdb"]} ${srcts["fdb"]}
    else
        :
    fi
}

function r_scpy() {
    local v1j
    local dscf=1
    local scc=1
    for v1j in ${binsrcs[@]}; do
        if bctck ${dstts["bin,$v1j"]} ${srcts["$v1j"]}; then
            dscf=0
            break
        fi
    done
    if [ $dscf -eq 0 ]; then
        scpy.sh
        scc=$?
    fi
    if [ $dscf -eq 0 -a $scc -eq 0 ]; then
        for v1j in ${binsrcs[@]}; do
            if bctck ${dstts["bin,$v1j"]} ${srcts["$v1j"]}; then
                bctclr ${dstts["bin,$v1j"]} ${srcts["$v1j"]}
            fi
        done
    fi
}

function r_csbackups() {
    local do_csb=1
    local v2j
    local v4i
    for v4i in ${svcs[@]}; do
        for v2j in ${codes[@]}; do
            bctck ${dstts["$v4i,$v2j"]} ${srcts["$v2j"]} &&
                do_csb=0 &&
                break
        done
        if [ $do_csb -eq 0 ]; then
            break
        fi
    done
    if [ $do_csb -eq 0 ]; then
        csbackup.sh
    else
        return 0
    fi
}

function status() {
    local rc ev
    for ev in ${srcs[@]}; do
        dhck $ev
        nrc=$?
        rc+=$nrc
        if [ $nrc -ne 0 ]; then
            echo $ev changed >>$bklog
        fi
    done
    echo $rc
}

function sup() {
    local rc=$(status)
    local s
    echo "status$1: $rc"
    i=0
    for s in ${srcs[@]}; do
        if [ "${rc:i:1}" != "0" ]; then
            echo "$s changed"
            touch ${rtbk}${srcts["$s"]}
            dhset ${s}
        fi
        i=$((i + 1))
    done
}

function inw1() {
    sup 1
    if r_fdbackup; then
        sup 2
        if r_scpy; then
            r_csbackups
        fi
    fi
}

inw1
rc=$?
echo "agb1 rc: $rc"
exit $rc
