#!/bin/bash
# modified script, orginally from the Arch linux forum

# determine the location of the user via a duckduckgo request
coun="$(wget -qO - "https://duckduckgo.com/lite/?q=ip" | grep "(your IP\ address)" | sed 's/.*(your IP address) in: .*, \(.*\s*.*\)\..*/\1/; s/ (.*)//')"
[[ "$quiet" == 1 ]] && (echo $coun; exit 0) && exit 0
[[ -z "$coun"  ]] && coun=Any # backup, in case autodetect fails

country="${country-$coun}" 
echo -e "detected country: $coun\nusing: $country"
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
[[ -z "$server" ]] && server='http://ftp.osuosl.org/pub/archlinux/$repo/os/x86_64' # Use a known good server as a backup
sed -i 's|= [^ ]*|= '"$server"'|g' "$apconf"
