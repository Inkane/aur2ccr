#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# unit test

import edit_package
import unittest
import tempfile
import shutil

class Addmaintainer(unittest.TestCase):

    base_file = "./PKGBUILD"
    compare_file = "./PKGBUILD_addmaintainer"
    
    def create_test_file(self, file):
        f = tempfile.TemporaryFile()
        with open(base_file) as src:
            shutil.copyfile(src, f)
        return f
    
    def test_addmaintainer_nochange_rest(self):
        e
