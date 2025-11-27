#!/data/data/com.termux/files/usr/bin/bash
source bin/gb.env

mkdir $bkx
if [ $? -ne 0 ]; then exit $?; fi

function eex() {
    if [ -d $bkx ]; then rmdir $bkx; fi
    exit 1
}

if ! netup.sh; then eex; fi

gitbackup.sh $blog

if [ $? -ne 0 ]; then eex; fi

pushd $blog

git branch -D temp

lcnt=$(git rev-list --count master)
echo rev cnt: $lcnt
hcnt=$((lcnt / 2))

if [ $hcnt -ge $lcnt ]; then
    popd
    eex
fi

echo half cnt: $hcnt
pc=$(git rev-list --max-count=1 --skip=$hcnt master)
echo prune commit: $pc

git checkout --orphan temp $pc
git commit -m edcba
git rebase --onto temp $pc master
git branch -D temp

(git gc --prune=all &&
    git repack -a -f -F -d &&
    git push --force origin master) ||
    (
        popd
        eex
    )

popd

pushd $proj
if [ -d _bak ]; then rm -f -R _bak; fi
mv blog _bak
git clone https://bitbucket.org/dpchitester/blog.git &&
    cp _bak/.git/config blog/.git/config
cp _bak/.git/info/exclude blog/.git/info/exclude
eex
popd
