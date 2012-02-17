#!/bin/bash
# modified script, orginally from the Arch linux forum

country="${country-Germany}" # replace this with your country
apconf="${apconf-./archrepos.pacman.conf}"
url="http://www.archlinux.org/mirrorlist/?country=$country&protocol=ftp&protocol=http&ip_version=4&use_mirror_status=on"
tmpfile=$(mktemp --suffix=-mirrorlist)

# Get latest mirror list and save to tmpfile
wget -qO- "$url" | sed 's/^#Server/Server/g' > "$tmpfile"

# Check for invalid countries
grep -o " $country is not one of the available choices." "$tmpfile" && exit 1

# some sed magic: get all lines containing "server", drop all but the first
# x86-64 works for all repos, i686 won't work with multilib
server=$(sed -n 's/^Server = //p' $tmpfile | head -1 | sed 's/$arch/x86-64/g')

sed -i 's|= [^ ]*|= '"$server"'|g' "$apconf"
