#!/data/data/com.termux/files/usr/bin/bash
# iph=$(termux-wifi-connectioninfo | jq -r '.ip')
busybox tcpsvd -vE 0.0.0.0 1024 busybox ftpd -w ~ &
