#!/bin/bash
echo "-- scpy.sh --"
cd ~

cp -u $proj/bash2/.bashrc ~
cp -u $proj/bash2/.bashrc0 ~

for ex in .sh .pl .env; do
    cp -u $proj/bash2/*$ex /usr/local/bin
    chmod 755 /usr/local/bin/*$ex
done

for ex in .py; do
    cp -u $pyth/*$ex /usr/local/bin
    chmod 755 /usr/local/bin/*$ex
done

if [ -f "$blog/.git-credentials" ]
then
    cp $blog/.git-credentials ~
    rm $blog/.git-credentials
fi
cp -u /sdcard/rclone /usr/bin
chmod 755 /usr/bin/rclone