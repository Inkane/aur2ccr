RED='\e[1;31m'          YELLOW='\e[1;33m'
BLUE='\e[1;34m'         PINK='\e[1;35m'
WHITE='\e[1;37m'        ENDCOLOR='\e[0m'        


# output formatting functions
debug() { # echo things when called like 'debug doing stuff...' only when debug=1
  pushd "$(pwd)" >/dev/null; cd "$startdir"
  if [[ "$debug" == 1 ]]; then
    if [[ "$1" == "-n" ]]; then
      local eopts="$1"; shift
    fi; ([[ -n "$logfile" ]] && echo -e $eopts "${PINK}++>${ENDCOLOR}" "$@" | tee -a "$logfile") || echo -e $eopts "${PINK}++>${ENDCOLOR}" "$@"
  fi; popd >/dev/null
}

msg() { # make aur2ccr's normal output prettier and more unified.
  debug "msg('$@')"
  pushd "$(pwd)" >/dev/null; cd "$startdir"
  if [[ "$1" == "-n" ]]; then
    local eopts="$1"
    shift
  fi; ([[ -n "$logfile" ]] && echo -e $eopts "${BLUE}==>${ENDCOLOR}" "$@" | tee -a "$logfile") || echo -e $eopts "${BLUE}==>${ENDCOLOR}" "$@" 
  popd >/dev/null
}

warn() { # make aur2ccr's warning messages prettier and more unified.
  debug "warn('$@')"
  pushd "$(pwd)" >/dev/null; cd "$startdir"
  if [[ "$1" == "-n" ]]; then
    local eopts="$1"
    shift
  fi; ([[ -n "$logfile" ]] && echo -e $eopts "${YELLOW}==>${ENDCOLOR}" "$@" | tee -a "$logfile") || echo -e $eopts "${YELLOW}==>${ENDCOLOR}" "$@"
  popd >/dev/null
}

err() { # make aur2ccr's error messages prettier and more unified.
  debug "err('$@')"
  pushd "$(pwd)" >/dev/null; cd "$startdir"
  if [[ "$1" == "-n" ]]; then
    local eopts="$1"
    shift
  fi; ([[ -n "$logfile" ]] && echo -e $eopts "${RED}==> ERROR:${ENDCOLOR}" "$@" | tee -a "$logfile") || echo -e $eopts "${RED}==> ERROR:${ENDCOLOR}" "$@" >&2
  popd >/dev/null
}

