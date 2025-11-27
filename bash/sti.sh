#!/data/data/com.termux/files/usr/bin/bash
# source ~/projects/bash/gb.env

pushd /sdcard/projects/bash
    f1=installs.sh
    f2=uninstalls.sh
    f3=pkgdeps.txt
    cp shebang.txt $f1
    cp shebang.txt $f2
    il1=$(pkg list-installed)
    a=()
    mapfile -t a <<<"$il1"
    for i in "${a[@]:1}"; do
        echo "====="
        j="${i%%/*}"
        echo "j: $j"
        il2=$(apt-cache rdepends --installed "$j")
        b=()
        mapfile -t b <<<"$il2"
        c="${b[0]}"
        echo "c: $c"
        echo "# pkg install ${i%%/*}" >>$f1
        bl=${#b[@]}
        echo "bl: $bl"
        if [ $bl -le 2 ]
        then
            echo "# pkg uninstall ${i%%/*}" >>$f2
        fi
        echo "***"
    done
    pl=$(pip list)
    a=()
    mapfile -t a <<<"$pl"
    for i in "${a[@]:1}"; do
        echo "# pip install ${i%% *}" >>$f1
        echo "# pip uninstall ${i%% *}" >>$f2
    done
popd

