#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# reimplementing edit_package.sh
from __future__ import print_function
from __future__ import unicode_literals

import re
import fileinput

def addmaintainer(pkgbuild, maintainer):
    # replace previous maintainer
    regex = re.compile(r"# Maintainer:")
    flag = True
    for line in fileinput.input(pkgbuild, inplace=1):
        if flag:
            print("# Maintainer: {}".format(maintainer))
            flag = not flag
        if re.match(regex, line):
            print("match")
        print(re.sub(regex, "# Contributor:", line), end="")

