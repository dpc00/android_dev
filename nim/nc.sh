cp -r -u /sdcard/projects/nim/* .
chmod 755 nc.sh
if [ $? -eq 0 ]; then
    nimble build
    if [ $? -eq 0 ]; then
        cp -r -u ./* /sdcard/projects/nim
        ./test1
    fi
fi
