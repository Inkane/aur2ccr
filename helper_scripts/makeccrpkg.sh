makeccrpkg() {  # grab a package from AUR, and make it into a CCR-ready src package
  debug "makeccrpkg('$@')"
  cd "$startdir"
  local pkgname=$1
  mkdir -p "$pkgname" || (err "cannot create directory '$startdir/$pkgname'"; logerr $pkgname; exit 1) || return 1
  cd "$pkgname"
  [[ -r "$pkgname.tar.gz" ]] && rm "$pkgname.tar.gz"
  wget "https://aur.archlinux.org/packages/$(echo "$pkgname" | sed 's/\(..\).*/\1/')/$pkgname/$pkgname.tar.gz" || (err "There was an error while trying to download the package."; logerr $pkgname; exit 1) || return 1
  (tar -xzf "$pkgname.tar.gz" && rm "$pkgname.tar.gz") || (err "tar could not extract the archive"; logerr $pkgname; exit 1) || return 1
  cd "$pkgname"
  dotherest "$pkgname" || (logerr $pkgname; exit 1) || return 1
}

makeccrpkg_r() {    # grab a package from Arch repos, and make it into a CCR-ready src package
  debug "makeccrpkg_r('$@')"
  cd "$startdir"
  local pkgname=$1
  mkdir -p "$pkgname" || (err "cannot create directory '$startdir/$pkgname'"; logerr $pkgname; exit 1) || return 1
  cd "$pkgname"
  [[ -r "$pkgname.tar.gz" ]] && rm "$pkgname.tar.gz"
  # get Arch package with PKGBUILD, .install, etc, using perl or whatever - extract the package if needed
  getarchname $pkgname
  if [[ -z "$archname" || "$archname" == 0 ]]; then
    err "'$pkgname' cannot be found"; logerr $pkgname
    return 1
  fi; msg "found '$pkgname' as '$archname'"
  if sudo abs "$archname"; then
    rm -rf "./$pkgname"
    if sudo mv "/var/abs/$archname" "./$pkgname"; then
      (sudo chown -hR $USER:$GROUPS "./$pkgname" && msg "$pkgname info retrieved from Arch repos successfully") || (err "chown failed"; logerr $pkgname; exit 1) || return 1
    else
      err "could not move /var/abs/$archname to working dir"; logerr $pkgname
      return 1
    fi
  else
    err "abs failed"; logerr $pkgname
    return 1
  fi  #  ^ this is a quick fix ^
  cd "$pkgname"
  dotherest "$pkgname" || (logerr $pkgname; exit 1) || return 1
}
  
makeccrpkg_u() {  # make a package from a URL
  debug "makeccrpkg_u('$@')"
  cd "$startdir"
  local pkgname="$(basename "$url" | sed 's/\([^\.]\)\..*/\1/')"; local pkgname="${pkgname-$BASHPID}" # if $url is http://example.com/path/package.tar.gz, $pkgname is set to "package".
  local myfile="$(basename "$url")"; local myfile="${myfile-$BASHPID}"
  mkdir -p "$pkgname" || (err "cannot create directory '$startdir/$pkgname'"; logerr $pkgname; exit 1) || return 1
  cd "$pkgname"
  wget -O "$myfile" "$url" || (err "There was an error while trying to download the package"; logerr $pkgname; exit 1) || return 1
  local dir="$(tar -taf "$myfile" | head -1)"
  tar -xaf "$myfile" || (err "tar could not extract the archive"; logerr $pkgname; exit 1) || return 1
  cd "$dir"
  [[ -r PKGBUILD ]] || (err "The package you specified does not seem to be a valid source archive."; logerr $pkgname; exit 1) || return 1
  dotherest "$pkgname" || (logerr $pkgname; exit 1) || return 1
}

makeccrpkg_f() {  # make a package from a *.src.tar.gz file
  debug "makeccrpkg_f('$@')"
  cd "$startdir"
  local pkgname="$(basename "$file" | sed 's/\([^\.]\)\..*/\1/')" # same as in _u above
  local dir="$(tar -taf "$file" | head -1)"
  [[ -r "$file" ]] || (err "'$file' cannot be opened or does not exist"; logerr $pkgname; exit 1) || return 1
  mkdir -p "$pkgname" || (err "cannot create directory '$startdir/$pkgname'"; logerr $pkgname; exit 1) || return 1
  tar -xaf "$file" -C "$pkgname" || (err "tar could not extract the archive"; logerr $pkgname; exit 1) || return 1
  cd "$pkgname/$dir"
  [[ -r PKGBUILD ]] || (err "The package you specified does not seem to be a valid source archive."; logerr $pkgname; exit 1) || return 1
  dotherest "$pkgname" || (logerr $pkgname; exit 1) || return 1
}

makeccrpkg_d() {  # uses $pkgdir as directory containting PKGBUILD. (argument to -d)
  debug "makeccrpkg_d('$@')"
  cd "$startdir"
  local pkgname="$(basename "$pkgdir")"
  [[ -d "$pkgdir" ]] || (err "$pkgdir is not a directory or does not exist"; logerr $pkgname; exit 1) || return 1
  cd "$pkgdir"; [[ -r "PKGBUILD" ]] || (debug "cd: `pwd`"; err "'$pkgdir/PKGBUILD' cannot be opened or does not exist"; logerr $pkgname; exit 1) || return 1
  cd "$startdir"
  mkdir -p "$pkgname" || (err "cannot create directory '$startdir/$pkgname'"; logerr $pkgname; exit 1) || return 1
  if [[ "$pkgdir" != "$pkgname/$pkgname" && "$pkgdir" != "$(pwd)/$pkgname/$pkgname" && "$pkgdir" != "./$pkgname/$pkgname" ]]; then # This is bad
    cp -r "$pkgdir" "$pkgname/" || (err "cannot copy files from '$pkgdir'"; logerr $pkgname; exit 1) || return 1
  fi
  cd "$pkgname/$pkgname"
  dotherest "$pkgname" || (logerr $pkgname; exit 1) || return 1
}

makeccrpkg_s() {  # handle split PKGBUILDs
  debug "makeccrpkg_s('$@')"
  local pkgname=$1
  warn "'$pkgname' seems to be a split PKGBUILD, which cannot be uploaded to CCR."
  warn "For more information on split PKGBUILDs, see PKGBUILD(5) or"
  warn "http://www.archlinux.org/pacman/PKGBUILD.5.html#_package_splitting"
  warn "aur2ccr can attempt to rectify this by dividing the PKGBUILD up into multiple"
  warn "packages, but this is an experimantal feature and does not always work. If"
  warn "you do not want this script to attempt to 'unsplit' this package, you will"
  warn "need to do it manually."
  warn "If aur2ccr does try to fix the PKGBUILD, the original will be backed up as"
  warn "PKGBUILD.orig in the package's build dir. "
  warn -n "Should aur2ccr attempt to fix this PKGBUILD? [y/N] "
  read ans
  if [[ -z "$ans" || "$ans" == "n" || "$ans" == "N" || "$ans" == "no" ]]; then
    warn "aur2ccr will not attempt to fix this PKGBUILD. You need to fix it"
    warn "manually before uploading the package to CCR."
    return 0
  else
    warn "Attempting to fix the PKGBUILD..."
    unsplitp PKGBUILD
    warn "Done. There is no way to see if this worked without testing the packages."
    for pkg in ${__PKGNAMES[@]}; do
      [[ "$pkg" == "$__PKGBASE" ]] && continue
      dotherest $pkg || (logerr $pkg; exit 1) || return 1
    done
    [[ -n "$__PKGBASE" ]] && dotherest $__PKGBASE || (logerr $__PKGBASE; exit 1) || return 1
  fi
}

