#!/data/data/com.termux/files/usr/bin/bash

pl=$(ps -o pid,comm)
a=()
mapfile -s 1 -t a <<<"$pl"
for ln in "${a[@]}"; do
    b=()
    read -a b <<<"$ln"
    if [ ${b[0]} -ne $$ -a ${b[0]} -ne $PPID -a "${b[1]}" != "ps" ]; then
        kill -15 ${b[0]}
    fi
done
unset a
