#!/bin/sh
# modified script, orginally from the Arch linux forum

arch="x86_64"

country='Germany' # replace this with your country
url="http://www.archlinux.org/mirrorlist/?country=$country&protocol=ftp&protocol=http&ip_version=4&use_mirror_status=on"

tmpfile=$(mktemp --suffix=-mirrorlist)

# Get latest mirror list and save to tmpfile
wget -qO- "$url" | sed 's/^#Server/Server/g' > "$tmpfile"

# some sed magic: get all lines including server, drop all but the first
# x86-64 works for all repos, i684 won't work with multilib
server=$(sed -n '/Server/p' $tmpfile | head -1 | sed 's/$arch/x86-64/g')

echo $server 
