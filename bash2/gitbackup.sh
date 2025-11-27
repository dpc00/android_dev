#!/bin/bash

[ -z $1 ] && echo "project directory not specified!" && exit 1

! [ -d $1/.git ] &&
    ( echo "not a .git directory apparently;";
    echo "$1 might not be a working tree"
    ) &&
    exit 2


function cer {
   if [ $1 -ne 0 ]; then
       echo "ec: $1 fn: $2"
       popd
       exit $1
   fi
}

function isclean {
    rc=$(git rev-list --count origin/master..master)
    cer $? "git rev-list"
    if [ $rc -gt 0 ]; then
        cc=$(git status --porcelain --untracked-files=all)
        cer $? "git-status (ta1)"
        if [ -n "$cc" ]; then
            return 0
        else
            return 1
        fi
    fi
}

# adder routine
function adder {
    cc=$(git status --porcelain --untracked-files=all)
    cer $? "git-status (ta1)"
    if [ -n "$cc" ]
    then
        a=()
        mapfile -t a <<< "$cc"
        for i in "${a[@]}"; do
            sc=${i:1:1}
            echo "$i"
            if [ "$sc" != " " -a "$sc" != "D" -a "$sc" != "R" ]
            then
                fn=${i:2}
                git add $fn
                cer $?
            fi
        done
    fi
}

# commit
function committer {
    cc=$(git status --porcelain --untracked-files=all)
    cer $? "git-status (ta2)"
    if [ -n "$cc" ]
    then
        a=()
        mapfile -t a <<< "$cc"
        ccn=0
        for i in "${a[@]}"; do
            echo "$i"
            if [ "${i:0:1}" != " " ]
            then
                ccn+=1
            fi
        done
        ([ $ccn -gt 0 ] &&
        git commit -a -m abcde) ||
        [ $ccn -eq 0 ]
        cer $? "git commit"
    fi
}

#---check if needs push
function pusher {
    rc=$(git rev-list --count origin/master..master)
    cer $? "git rev-list"
    if [ $rc -gt 0 ]; then
        netup.sh
        cer $? "netup"
        git push
        cer $? "git push"
    fi
}

pushd $1

pusher &&
committer &&
adder &&
isclean
cer $? "isclean"

popd


