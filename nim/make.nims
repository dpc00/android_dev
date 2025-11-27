#!/data/data/com.termux/files/usr/bin/env nim

echo "hello from make.nims"
exec("nimble build")
cpFile("/sdcard/projects/nim/test1","/data/data/com.termux/files/home/nim/test1")
exec("/data/data/com.termux/files/home/nim/test1")
