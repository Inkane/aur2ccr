#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# reimplementing edit_package.sh
from __future__ import print_function
from __future__ import unicode_literals
import subprocess
import logging
import shutil
import tempfile

import re
import fileinput

def addmaintainer(pkgbuild, maintainer):
    logging.info("adding maintainer to {}".format(pkgbuild))
    # replace previous maintainer
    regex = re.compile(r"# Maintainer:")
    flag = True
    for line in fileinput.input(pkgbuild, inplace=1):
        if flag:
            print("# Maintainer: {}".format(maintainer))
            flag = not flag
        if re.match(regex, line):
            print(re.sub(regex, "# Contributor:", line), end="")
        else:
            print(line, end="")

def update_chksums(pkgbuild):
    # update the checksum array of a PKGBUILD
    try:
        new_checksums = subprocess.check_output(["makepg", "-gf", pkgbuild])
    except subprocess.CalledProcessError:
        # handle error
        pass
    # replace the old checksums
    regex = re.compile("*sums=")
    with open(pkgbuild) as f, tempfile.NamedTemporaryFile(delete=False) as tmpf:
        for line in f:
            #if re.match(regex, 
            pass
    return new_checksums
