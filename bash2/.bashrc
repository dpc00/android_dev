# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

export proj=/sdcard/projects
export PS1='$PWD\n\$ '

export HISTCONTROL=ignoreboth:erasedups

source /usr/local/bin/gb.env

alias ab='agb1.sh &'
alias fd='fdb.sh'
alias gb='gb.sh'
alias grc='grc.sh'
alias pk='pka.sh'
alias pke='pka.sh; exit'

ps -o pid,comm

alias ps='ps -o pid,comm'
alias sc='scpy.sh'
alias netup='netup.sh'

source ~/.bashrc0
