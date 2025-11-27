#!/bin/bash
echo "-- netup.sh --"
#curl -s --head --request GET www.google.com | grep "200 OK"
tr=$?
echo "netup rc: " $tr

src $tr

