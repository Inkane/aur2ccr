import sys
import pkgbuild_parser as pp
import package_tracker

tracker = package_tracker.PackageTracker()


def do(pkgbuild_file):
    pkgbuild = pp.parser.parseFile(pkgbuild_file)
    if pkgbuild.depends and pkgbuild.depends.pname:
        for dep in pkgbuild.depends.pname:
            tracker.track_package(dep)

    if pkgbuild.optdepends and pkgbuild.optdepends.pname:
        for dep in pkgbuild.optdepends.pname:
            tracker.track_package(dep)

    if pkgbuild.makedepends and pkgbuild.makedepends.pname:
        for dep in pkgbuild.makedepends.pname:
            tracker.track_package(dep)

if __name__ == "__main__":
    try:
        do(sys.argv[1])
    except IndexError:
        print("you need to specify a PKGBUILD!\n")
        sys.exit(1)

    print tracker.yet_to_install
