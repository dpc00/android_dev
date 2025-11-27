#!/data/data/com.termux/files/usr/bin/bash
cd ~
if [ -z $insc ]; then
    insc=0
    source /sdcard/projects/bash/gb.env
    source /sdcard/projects/bash/scpy.sh
else

echo "-- scpy.sh --"

cp -u -p ${pdir["scrdev"]}/.bashrc ~
cp -u -p ${pdir["scrdev"]}/.bashrc0 ~
cp -u -p ${pdir["scrdev"]}/.profile ~
cp -u -p ${pdir["scrdev"]}/.swiplrc ~
cp -u -r -p ${pdir["scrdev"]}/.termux ~

for ex in .sh .env; do
    cp -u -p ${pdir["scrdev"]}/*$ex ~/bin/sh
    chmod +x ~/bin/sh/*$ex
done

for fn in termux-url-opener termux-file-editor; do
    cp -u -p ${pdir["scrdev"]}/$fn ~/bin
    chmod +x ~/bin/$fn
done

for ex in .pl; do
    cp -u -p ${pdir["pro"]}/*$ex ~/bin/pl
    chmod +x ~/bin/pl/*$ex
done

if [ -f "${pdir["blog"]}/.git-credentials" ]; then
    cp -u -p ${pdir["blog"]}/.git-credentials ~
    rm ${pdir["blog"]}/.git-credentials
fi

fi