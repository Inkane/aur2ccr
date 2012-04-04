## aur2ccr 
Pull information from AUR or Arch repos, and make source packages that are ready for uploading to CCR.

This script uses the information on converting Arch/AUR packages to CCR source packages from http://chakra-linux.org/wiki/index.php/How_to_upload_a_package_to_CCR_when_it_exists_on_Arch_or_Aur

# Todo:
See issues (https://github.com/redhat69/aur2ccr/issues/).
This script is currently undergoing a transition from bash to Python, so new features will not be implemented until that change has been completed. 

# Installation:
Installation for aur2ccr is simple. Just run
`ccr -S aur2ccr`, `ccr -S aur2ccr-git`, or 

    git clone git://github.com/redhat69/aur2ccr.git
    cd aur2ccr
    make
    sudo make install

This will install the script itself, the needed configuration files, and the **aur2ccr(8)** man page. There is no need for a `./configure`, as the script only works on one platform: Chakra Linux.

# Configuration:
To configure aur2ccr, just run
    aur2ccr --setup
Or edit the configuration files in /etc/aur2ccr/ by hand. All configuration files in /etc/aur2ccr/ can also be copied to ~/.aur2ccr/. Local conf files take precedence over global ones. 

# Documentation:
Usage information for this script can be found in the help output (`aur2ccr -h` or `aur2ccr --help`) and the man page (`man 8 aur2ccr`). Configuration options and files are documented in the aur2ccr man page (`man 8 aur2ccr`), and in the global configuration file (`less /etc/aur2ccr/aur2ccr.conf`).
