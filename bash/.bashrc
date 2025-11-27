# If not running interactively, don't do anything
case $- in
    *i*) ;;
    *) return ;;
esac
export PS1="\W>"
export HISTCONTROL=ignoreboth:erasedups
#export PYTHONPATH=/sdcard/projects/pybackup

export LD_LIBRARY_PATH=$PREFIX/lib
export PATH=$PATH:$LD_LIBRARY_PATH:~/go/bin
export NODE_PATH=$PREFIX/lib/node_modules
export FDB_PATH=/sdcard/Android/data/com.smartphoneremote.androidscriptfree/files/Droidscript/blog
#export PYTHONDEBUG=1
#export PYTHONASYNCIODEBUG=1
#export PYTHONDEVMODE=1
export RCLONE_CONFIG=$HOME/.config/rclone/rclone.conf
export XDG_CONFIG_HOME=$HOME/.config
export CDPATH=/sdcard/projects

alias pb='cd /sdcard/projects/pybackup'
alias pp='cd $PYTHON_SITE_PACKAGES'
export PYTHON_SITE_PACKAGES=/data/data/com.termux/files/usr/lib/python3.11/site-packages
export PYTHON_PACKAGES=/data/data/com.termux/files/usr/lib/python3.11
export app=/data/data/com.termux/files
source ~/.bashrc0
