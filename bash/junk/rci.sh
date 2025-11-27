cd ~
set -e
tmp_dir=$(mktemp -d 2>/dev/null || mktemp -d -t 'rclone-install')
cd $tmp_dir
pwd
OS='linux'
OS_type='arm'
export XDG_CONFIG_HOME=config
download_link="https://downloads.rclone.org/rclone-current-$OS-$OS_type.zip"
rclone_zip="rclone-current-$OS-$OS_type.zip"
curl -O $download_link
unzip_dir="rclone-tmp"
7z e -o$unzip_dir $rclone_zip
cd $unzip_dir
cp rclone ~/bin/rclone.new
chmod 755 ~/bin/rclone.new
chown root:root ~/bin/rclone.new
mv ~/bin/rclone.new ~/bin/rclone-dl
#manuals
#mkdir -p ~/local/share/man/man1
#cp rclone.1 ~/local/share/man/man1/
#mandb
version=$(rclone --version 2>>errors | head -n 1)

printf "\n${version} has successfully installed."
printf '\nNow run "rclone config" for setup. Check https://rclone.org/docs/ for more details.\n\n'
exit 0
