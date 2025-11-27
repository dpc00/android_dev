D1=~/projects/rtl-sdr-blog/build/src
D2=$PREFIX/lib

F1=libconvenience_static.a
F2=librtlsdr.a
F3=librtlsdr.so
F4=librtlsdr.so.0
F5=librtlsdr.so.0.6git

cp -u -p "${D1}/${F1}" "${D2}"
cp -u -p "${D1}/${F2}" "${D2}"
cp -u -p "${D1}/${F3}" "${D2}"
cp -u -p "${D1}/${F4}" "${D2}"
cp -u -p "${D1}/${F5}" "${D2}"
