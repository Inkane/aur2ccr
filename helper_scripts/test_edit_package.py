#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# unit test

from __future__ import print_function

import os
import sys
import unittest
import tempfile
import filecmp
import shutil
import edit_package

class Addmaintainer(unittest.TestCase):

    base_dir = "./pkgbuilds/"
    compare_dir = "after_addmaintainer"
    maintainer = "Unittest <test@example.com>"
    workaround = "/home/{}/tmp.txt".format(os.environ["USER"])
    
    def create_test_file(self, path_to_file):
        #tmpf = tempfile.NamedTemporaryFile(mode="w+t")
        #shutil.copy(path_to_file, tmpf.name)
        #return tmpf
        shutil.copy(path_to_file, self.workaround)
        return self.workaround
    
    def test_addmaintainer_nochange_rest(self):
        root, tmp, files = next(os.walk(self.base_dir))
        root = os.path.abspath(root)
        for file in files:
            tempf = self.create_test_file(os.path.join(root,file))
            edit_package.addmaintainer(tempf, self.maintainer)
            cmp = os.path.join(root,self.compare_dir,file)
            assert filecmp.cmp(tempf, cmp), "Files are not equal. Error in {}".format(file)


if __name__ == "__main__":
    unittest.main()
