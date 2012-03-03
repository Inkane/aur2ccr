
isoutofdate() {  # stolen from the isoutofdate() and rpcinfo() functions in 'ccr'
  debug "isoutofdate('$@')"
  RPCURL="https://aur.archlinux.org/rpc.php?type"
  [[ -f "$tmpdir/$1.info" ]] || curl -LfGs --data-urlencode "arg=$1" "$RPCURL=info" > "$tmpdir/$1.info"
  [[ "$(jshon -Q -e results -e OutOfDate -u < "$tmpdir/$1.info")" = "1" ]]
}

vcsver() {  # look for version control system versions, like pkgname-git
  debug "vcsver('$@')"
  if isinccr "$1-git"; then # git
    vpkgname="$1-git"
    return 0
  elif isinccr "$1-bzr"; then # bazaar
    vpkgname="$1-bzr"
    return 0
  elif isinccr "$1-svn"; then # subversion
    vpkgname="$1-svn"
    return 0
  elif isinccr "$1-hg"; then # mercurial
    vpkgname="$1-hg"
    return 0
  else
    return 1
  fi
}

isinccr() {  # check in CCR and main repos for package
  debug "isinccr('$@')"
  ccr -Ssq $1 | grep -q "^$1$"
}

isinrepos() {  # check in main Chakra repos for package - stolen from 'ccr'
  debug "isinrepos('$@')"
  pacman -Si -- "$1" &>/dev/null
}

isinaur() {
  debug "isinaur('$@')"
  echo "$1" | grep -q '^..' || (err "Package names must be at least two characters in length"; exit 1) || exit 1 # if the package name is not at least 2 chars, checking aur will fail.
  wget -q --spider "https://aur.archlinux.org/packages/$(echo "$1" | sed 's/\(..\).*/\1/')/$1/PKGBUILD"
}

isinarchr() {
  debug "isinarchr('$@')"
  msg "Checking Arch repos..."
  [[ "$archrinit" == 0 ]] && initarchr
  echo "$areplist" | grep -q "^$1$"  # much nicer than the old function
}

getarchname() {
  debug "getarchname('$@')"
  if isinarchr $1; then
    archname=$(echo "$afullist" | grep -o "^[^ ]*/$1\s" | sed 's/\s//g')
  else
    err "'$1' not found in Arch repos"
  fi
}

depends() {  # get the dependencies from the PKGBUILD - stolen from 'ccr'
  local pkgname=; local pkgbase=; local pkgver=; local pkgrel=; local url=; local arch=; local license=; local source=; local md5sums=; local srcdir=; local pkgdir=; local install=    # declare vars from the PKGBUILD as local, so aur2ccr doens't get confused
  debug "depends($@)"; debug "current dir: $(pwd; ls)"
  . PKGBUILD; IFS=$'\n'
  depends=( $(echo -e "${depends[*]}\n${makedepends[*]}" | sed -e 's/=.*//' -e 's/>.*//' -e 's/<.*//'| sort -u) ); IFS=' '
  debug "depends=( ${depends[@]} )"
}
