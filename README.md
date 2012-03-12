## aur2ccr 
Pull information from AUR or Arch repos, and make source packages that are ready for uploading to CCR.

This script uses the information on converting Arch/AUR packages to CCR source packages from http://chakra-linux.org/wiki/index.php/How_to_upload_a_package_to_CCR_when_it_exists_on_Arch_or_Aur

# Todo:
See TODO (https://github.com/redhat69/aur2ccr/blob/master/TODO).

# Installation:
Installation for aur2ccr is simple. Just run:
  ccr -S aur2ccr
 -- OR --
  ccr -S aur2ccr-git
 -- OR --
  git clone git://github.com/redhat69/aur2ccr.git
  cd aur2ccr
  make
  sudo make install
This will install the script itself, the needed configuration files, and the aur2ccr(8) man page. There is no need for a ./configure, as the script only works on one platform: Chakra Linux.
