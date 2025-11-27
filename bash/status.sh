source /sdcard/projects/bash/gb.env

for v2i in ${svcs[@]}; do
    for v4j in ${projs[@]}; do
        if [ "$v4j" != "fdb" ]; then
            ds=${pdirs[$v4j]}
            dstr1=${ds##$proj}
            dstr2=${dstr1:1}
            oneps ${dstts[v2i, v4j]} ${srcts[$v4j]} ${snms[$v2i]} $dstr2
            vrc=$((vrc + $?))
        fi
    done
done
