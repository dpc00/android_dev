#!/data/data/com.termux/files/usr/bin/bash
f1=~/storage/documents/cmds.txt
[ -f $f1 ] && rm $f1
a2=()
mapfile -t a2 <<<"${PATH//:/$'\n'}"
for fd in "${a2[@]}"; do
    echo dir: $fd >>$f1
    fl=$(ls $fd)
    a1=()
    mapfile -t a1 <<<"$fl"
    for c in "${a1[@]}"; do
        ! [ -d $fd/$c ] &&
            echo "    $c" >>$f1
    done
done
