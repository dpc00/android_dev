# termux-setup-storage
cd /sdcard/projects/bash
cp .bash* ~
cp .profile ~
mkdir ~/bin
mkdir ~/bin/sh
mkdir ~/.config
mkdir ~/.config/rclone
mkdir ~/.termux
cp -r .config/** ~/.config
cp -r .termux/** ~/.termux
cp .git-credentials .gitconfig ~
cp pbu ~/bin
chmod 755 ~/bin/pbu
source installs.sh


