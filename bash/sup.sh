pushd /sdcard/projects
    git remote update
    if [ $? -eq 0 ]; then
        rv=$(git status --porcelain)
        if [ "$rv" != "" ]; then
            git add .
            git commit -a -m sup
        fi
        LOCAL=$(git rev-parse @)
        REMOTE=$(git rev-parse @{u})
        BASE=$(git merge-base @ @{u})
        if [ $LOCAL = $REMOTE ]; then
            echo "UP-TO-DATE"
        elif [ $LOCAL = $BASE ]; then
            echo "NEED-TO-PULL"
            git pull
        elif [ $REMOTE = $BASE ]; then
            echo "NEED-TO-PUSH"
            git add .
            git commit -a -m sup
            git push
        else
            echo "DIVERGED"
        fi
    fi
    rclone check /sdcard/Documents/Finance.db GoogleDrive:/Documents
    if [ $? -ne 0 ]; then
        r1=$(rclone lsjson /sdcard/Documents/Finance.db | jq .[0].ModTime)
        if [ $? -eq 0 ]; then
            r2=$(rclone lsjson GoogleDrive:/Documents/Finance.db | jq .[0].ModTime)
            if [ $? -eq  0 ]; then
                if [ "$r2" > "$r1" ]; then
                    echo "Finance.db appears out of date"
                    rclone sync GoogleDrive:/Documents/Finance.db /sdcard/Documents
                else
                    if [ "$r1" > "$r2" ]; then
                        echo "Finance.db appears ahead of cloud"
                        rclone sync /sdcard/Documents/Finance.db GoogleDrive:/Documents
                    fi
                fi
            fi
        fi
    fi
popd