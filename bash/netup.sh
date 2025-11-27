#!/data/data/com.termux/files/usr/bin/bash
echo "-- netup.sh --"

function src() {
    return $1
}

dig @8.8.4.4 +notcp www.google.com 2>&1 | grep -q "status: NOERROR"
tr=$?
echo "netup rc: " $tr
src $tr
