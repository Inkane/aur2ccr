#!/bin/bash
# modified script, orginally from the Arch linux forum

# determine the location of the user via a website
$(wget -qiet --referer="http://www.google.com" --user-agent="Mozilla/5.0 (Windows; U;Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6" --header="Accept:text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5" --header="Accept-Language: en-us,en;q=0.5" --header="Accept-Encoding: gzip,deflate"  --header="Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7" --header="Keep-Alive: 300" "$@" -O lang.gz http://www.ip-adress.com/)
gunzip lang.gz
echo $(sed -n 's/flag/&/p' <lang)
rm lang

country="${country-Germany}" # replace this with your country
url="http://www.archlinux.org/mirrorlist/?country=$country&protocol=ftp&protocol=http&ip_version=4&use_mirror_status=on"

tmpfile=$(mktemp --suffix=-mirrorlist)

# Get latest mirror list and save to tmpfile
wget -qO- "$url" | sed 's/^#Server/Server/g' > "$tmpfile"

# some sed magic: get all lines containing "server", drop all but the first
# x86-64 works for all repos, i686 won't work with multilib
server=$(sed -n '/Server/p' $tmpfile | head -1 | sed 's/$arch/x86-64/g')

sed -i 's|= [^ ]*|= '"$server"'|g' ./archrepos.pacman.conf 
