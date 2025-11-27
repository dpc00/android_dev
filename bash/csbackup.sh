#!/data/data/com.termux/files/usr/bin/bash
echo "-- csbackup.sh --"
source /sdcard/projects/bash/gb.env

# csname projsubdir
function csb() {
    # echo "csb $1 $2"
    local spn=$1
    local pjd=$2

    echo "$pjd -> $spn" &&
        rclone copy $proj/$pjd $spn:/projects/$pjd --progress --exclude '.git/**' --delete-excluded
}

# dep(N2, N1, Svc, Pdir)

function oneps() {
    bctck $1 $2 &&
        (
            echo "oneps $1 $2 $3 $4"
            csb $3 $4 &&
                bctclr $1 $2
        )
    ! bctck $1 $2
}

function r_cs() {
    local vrc=0
    local s c ds dstr1 dstr2

    for s in ${svcs[@]}; do
        for c in ${codes[@]}; do
            ds=${pdir["$c"]}
            dstr1=${ds##$proj}
            dstr2=${dstr1:1}
            oneps ${dstts["$s,$c"]} ${srcts["$c"]} ${snms["$s"]} $dstr2
            vrc=$((vrc + $?))
        done
    done
    return $vrc
}

r_cs
rc=$?
echo csb: $rc
exit $rc
