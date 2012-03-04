#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# reimplementing edit_package.sh
from __future__ import print_function
from __future__ import unicode_literals
import logging

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

def update_uchksums(pkbuild):
    # update the checksum array of a PKGBUILD
    pass
