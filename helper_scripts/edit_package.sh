
addmaintainer() {  # change maintainer info in the PKGBUILD
  debug "addmaintainer('$@')"
  sed -i 's/^# Maintainer: /# Contributer: /' PKGBUILD
  (printf "# Maintainer: ${maintainer}\n$(cat PKGBUILD)" > PKGBUILD.1 && mv PKGBUILD.1 PKGBUILD) || return 1
}

addad() {
  debug "addad('$@')"
  ed -s PKGBUILD << EOF && msg "Ad added. Thanks for supporting aur2ccr! :)"
2i
# Contributer: aur2ccr (http://ddg.gg/?q=!ccr+aur2ccr)
.
wq
EOF
}

uchksums() {  # update checksums with 'makepkg -gf'
  debug "uchksums($@)"
  debug "current dir: $(pwd; ls)"
  if makepkg -gf > "$tmpdir/${PID}${UID}.sums"; then
    sums="$(cat "$tmpdir/${PID}${UID}.sums")"
  else
    err "'makepkg -g' failed in '$(pwd)'!"
    return 1
  fi
  stype="$(echo $sums | grep -o "^..*sums=")"
  if echo "$sums" | grep -q "^$stype"; then
    if grep -q "^$stype" PKGBUILD; then
      stype="$(echo "$stype" | sed 's/=//; s/\s//g')" ; debug "awking..."
      local new="$(awk -v "newsums=$sums" -v "stype=$stype" '$1 ~ stype { t = 1; } t == 1 { if ($0 ~ "\)") { t = 0; print(newsums); next; } next; } { print; }' PKGBUILD 2>/dev/null)" # sheesh. awk courtesy of pr3d4t0r, I haven't a clue how it works.
      debug "sending awk output to PKGBUILD..."
      echo "$new" > PKGBUILD
    elif [[ -z "$sums" ]]; then
      return 0
    else
      return 1
    fi
  else
    err "something went wrong while updating checksums"
    return 1
  fi
}

optipkg() {  # optimize PKGBUILDs by getting rid of a few easy-to-fix errors, etc - note that this must be run AFTER the unsplitp function, or it will break split packages.
  debug "optipkg($@)"
  grep -q '^# $Id' PKGBUILD && sed -i '/^# $Id[$:].*$/d' PKGBUILD # get rid of $Id tags, which are not used by CCR.
  grep -q "^[^ ]*=(['\"\s]*)" PKGBUILD && sed -i "/^[^ ]*=(['\"\s]*)/d" PKGBUILD # get rid of empty arrays, like depends=()
  grep -q "^[^ ]*=([^'\"\s][^ ]*[^'\"\s])" PKGBUILD && sed -i "s/\(^[^ ]*=(\)\([^'\"\s][^ ]*[^'\"\s]\)\().*$\)/\1\"\2\"\3/" PKGBUILD # quote unquoted single values in arrays, like arch=(any)
}   # seems to cause errors: grep -q "^package()" PKGBUILD || grep -q "^build()" PKGBUILD && sed -i "/^build()/s//package()/" PKGBUILD # if there is no package() function, but there is a build() function, rename build() to package()

isplitp() {  # is $1 a split PKGBUILD?
  debug "isplitp('$@')"
  grep -q "package_.*()" "$1" && grep -q "build()" "$1" || return 1 #grep -q "^pkgbase=" "$1" &&  
}

unsplitp() {  # take one split PKGBUILD and create multiple normal PKGBUILDs
  debug "unsplitp('$@')"
  local pkgname=; local pkgbase=; local pkgver=; local pkgrel=; local url=; local arch=; local license=; local source=; local md5sums=; local srcdir=; local pkgdir=; local install= 
  unstartd="$(pwd)"
  cp PKGBUILD PKGBUILD$BASHPID.orig
  . PKGBUILD # get the PKGBUILD's vars into our mem
  [[ -z "$pkgbase" ]] && pkgbase=$pkgname
  for pkg in ${pkgname[@]}; do # seperate PKGBUILDs
    [[ "$pkg" == "$pkgbase" ]] && continue # skip pkgbase
    mkdir -p "../../$pkg/$pkg" && cd "../../$pkg/$pkg" || return 1
    cp -f "$unstartd/PKGBUILD" ./ || return 1
    sed -i "/^pkgbase=.*/d; /^package_$pkg()/s//package()/; /^true && pkgname=.*/d; /^pkgname=.*/s//pkgname=$pkg/; /true && depends=()/d; /^package_.*()/,/^}\s*$/d; s/\(.*\)\$pkgbase\(.*\)/\1$pkgbase\2/; s/\(.*\)\$pkgname\([^\[].*\)/\1$pkgname\2/; s/\(.*\)\$pkgname\[\(\d\d*\)\]\(.*\)/\1${pkgname[\2]}\3/; s/\([^=]\)$pkg/\1\${pkgname}/g" PKGBUILD || return 1
  done; cd "$unstartd"
  sed -i "/^pkgbase=.*/d; /^package_$pkgbase()/s//package()/; /^true && pkgname=.*/d; /^pkgname=.*/s//pkgname=$pkgbase/; /true && depends=()/d; /^package_.*()/,/^}\s*$/d; s/\(.*\)\$pkgbase\(.*\)/\1$pkgbase\2/; s/\(.*\)\$pkgname\([^\[].*\)/\1$pkgname\2/; s/\(.*\)\$pkgname\[\(\d\d*\)\]\(.*\)/\1${pkgname[\2]}\3/; s/\([^=]\)$pkgbase/\1\${pkgname}/g" PKGBUILD || return 1 # fix pkgbase PKGBUILD
  grep -q "^package()" PKGBUILD || sed -i "/^build()/s//package()/" PKGBUILD || return 1 # if no package(), rename build() to package()
  __PKGNAMES=( ${pkgname[@]} ) __PKGBASE="$pkgbase"
}


namelookup() {  # see https://github.com/redhat69/aur2ccr/issues/1
  debug "namelookup('$@')"
  if [[ -r "$namesconf" ]]; then
    if grep -q "$1=..*" "$namesconf"; then
      apkgname="$1"
      cpkgname="$(grep "^$1=..*" "$namesconf" | sed "s/$1=//")"
      return 0
    else
      return 1
    fi
  else 
    return 1
  fi
}

namechange() {  # companion function to namelookup()
  debug "namechange('$@')"
  namelookup $1 && sed -i "s/\(^[^ ]*depends=.*[(\s'\"]*\)${apkgname}\([\s'\")]\)/\1${cpkgname}\2/g; s/\(['\"]\)${apkgname}\(['\"]\)/\1${cpkgname}\2/g" PKGBUILD || return 1
  debug "new PKGBUILD: $(cat PKGBUILD)"
  depends
}

