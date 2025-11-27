pushd /sdcard/projects
for sf in prolog/*.pl; do
    cp ${sf} ${sf}.swii
    swipl reindent/swi-indent.pl --lib='./prolog' --output='./prolog' "${sf}.swii"
done
popd
