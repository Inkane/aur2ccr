
aursearch() {  # this code is stolen from 'packer'. This used to be, and is the equivalent of: packer --auronly -Ss $1 
  debug "aursearch('$@')" >&2 ; aret=0
  RPCURL="https://aur.archlinux.org/rpc.php?type"
  curl -LfGs --data-urlencode "arg=$1" "$RPCURL=search" | sed -e 's/","/"\n"/g' -e 's/\\//g' > "$tmpdir/$1$UID.search" 
  parsefile="$tmpdir/$1$UID.search" IFS=$'\n' aurname=( $(grep -F '"Name":"' "$parsefile" | cut -d '"' -f 4) )
  version=( $(grep -F '"Version":"' "$parsefile" | cut -d '"' -f 4) ) aurtotal="${#aurname[@]}"
  description=( $(grep -F '"Description":"' "$parsefile" | sed -e 's/^"Description":"//' -e 's/"$/ /') )
  for ((i=0 ; i<$aurtotal ; i++)); do
    printf "aur/${aurname[$i]} ${version[$i]}\n    ${description[$i]}\n" ; aret=1
  done
}

pkgsearch() {  # there is no reason for this function to ever be called except right after isinarchr returns 1
  debug "pkgsearch('$@')"
  warn "Package '$1' not found in AUR or Arch repos."; warn "Did you mean: "; debug "checking aursearch..."
  aursearch $1 ;  ([[ -n "$aret" && "$aret" == 1 ]] || grepacfull $1)
  exit 1
}

checkaur() {
  debug "checkaur('$@')"
  if isinaur $1; then 
    msg "'$1' found in AUR..."
    if isoutofdate $1; then
      warn "$1 is marked as out of date in AUR!"
      warn -n "Are you sure you want to continue? [y/N] "; read ans
      ([[ -z "$ans" || "$ans" == "n" || "$ans" == "N" || "$ans" == "no" ]] && (warn "Skipping $1"; exit 0)) || (warn "Continuing. This is a bad idea!"; sleep 2)
    fi
    makeccrpkg $1 || logerr $1
  elif isinarchr $1; then
    msg "'$1' found in the Arch repos..."
    makeccrpkg_r $1 || logerr $1
  else
    pkgsearch $1
  fi
}
