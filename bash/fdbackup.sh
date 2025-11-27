#!/data/data/com.termux/files/usr/bin/bash
echo "-- fdbackup.sh --"
source /sdcard/projects/bash/gb.env
rc=0

cp -u -p pdir["fdb"] pdir["blog"]/dist
rc=$((rc + $?))

echo fdb: $rc
src $rc
