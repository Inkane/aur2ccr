import pkgbuild_parser as pp
import package_tracker

tracker = package_tracker.PackageTracker()

def do(pkgbuild_file):
    pkgbuild = pp.parser.parseFile(pkgbuild_file)
    if pkgbuild.depends:
        for dep in pkgbuild.depends.pname.asList():
            tracker.track_package(dep)

    if pkgbuild.optdepends:
        for dep in pkgbuild.optdepends.pname.asList():
            tracker.track_package(dep)

    if pkgbuild.makedepends:
        for dep in pkgbuild.makedepends.pname.asList():
            tracker.track_package(dep)
