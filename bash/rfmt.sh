pushd ~/projects
[ -d tmp ] && rm -rf tmp
! [ -d tmp ] && mkdir tmp && mkdir tmp/junk
pushd bash
fl=".bashrc .bashrc0 .profile *.sh *.env junk/*.sh"
for sf in $fl; do
    shfmt -s -i 4 -ci $sf >../tmp/$sf &&
        if ! diff -q ../tmp/$sf $sf; then
            cp ../tmp/$sf $sf
        fi
done
popd
[ -d tmp ] && rm -rf tmp
popd
