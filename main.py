#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import pkgbuild_parser as pp
import package_tracker

tracker = package_tracker.PackageTracker()


def track_all(dep_list):
    for dep in dep_list:
        try:
            dep = pp.var.substitute_variable(dep)
        except:
            pass
        tracker.track_package(dep)


def do(pkgbuild_file):
    pkgbuild = pp.parser.parseFile(pkgbuild_file)
    if pkgbuild.depends and pkgbuild.depends.pname:
        track_all(pkgbuild.depends.pname)

    if pkgbuild.optdepends and pkgbuild.optdepends.pname:
        track_all(pkgbuild.optdepends.pname)

    if pkgbuild.makedepends and pkgbuild.makedepends.pname:
        track_all(pkgbuild.makedepends.pname)

if __name__ == "__main__":
    try:
        do(sys.argv[1])
    except IndexError:
        print("you need to specify a PKGBUILD!\n")
        sys.exit(1)

    print tracker.yet_to_install
