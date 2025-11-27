#!/data/data/com.termux/files/usr/bin/bash

rclone lsf $1 --recursive --format pst --files-only --exclude ".git/**" --exclude "__pycache__/**" | sort
