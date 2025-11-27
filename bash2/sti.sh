#!/bin/bash
pushd $scrdev
f1=installs.sh
f2=uninstalls.sh
cp shebang.txt $f1
cp shebang.txt $f2
il=$(apt list-installed)
a=()
mapfile -t a <<< "$il"
for i in "${a[@]:1}"; do
    echo "apt install ${i%%/*}">>$f1
    echo "# apt uninstall ${i%%/*}">>$f2
done
popd
scpy.sh
