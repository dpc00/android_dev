#!/data/data/com.termux/files/usr/bin/bash
 
od=/sdcard/projects/prolog
ofn=temp.pl

:>$od/$ofn

function fb {
    echo "">>$od/$ofn
    echo "% ---- $1 ----">>$od/$ofn
    cat $1>>$od/$ofn
}

for sf in $od/*.pl; do
    if [ "$sf" != "$od/rfmt.pl" \
        -a "$sf" != "$od/temp.pl" \
        -a "$sf" != "$od/test.pl" \
        -a "$sf" != "$od/test2.pl" \
       ]; then
        fb $sf
    fi
done
