#!/data/data/com.termux/files/usr/bin/bash
source ~/bin/gb.env

pushd ${pdirs[scrdev]}
f1=installs.sh
f2=uninstalls.sh
cp shebang.txt $f1
cp shebang.txt $f2
il=$(pkg list-installed)
a=()
mapfile -t a <<<"$il"
for i in "${a[@]:1}"; do
    echo "pkg install ${i%%/*}" >>$f1
    echo "# pkg uninstall ${i%%/*}" >>$f2
done
popd
scpy.sh
