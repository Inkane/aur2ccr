from pyparsing import Word, OneOrMore, Literal, alphanums, Optional, oneOf, nums, Group, alphas, quotedString, printables, ZeroOrMore, Combine, nestedExpr, lineEnd
import logging


# define a class which tracks all packages
class PackageTracker(object):
    """This will track all packages.
    Future versions will have better dependency tracking"""

    def __init__(self):
        self.yet_to_install = []
        self.already_installed = set()
        self.errorneous_package = []

    def track_package(self, package):
        """tracks a package, but only if it is not converted yet."""
        if package not in self.already_installed:
            self.yet_to_install.append(package)
        else:
            # move package up
            pass

# TODO: use something useful
ptrack_tmp = []


# define some utility classes/functions/constants

def opQuotedString(pattern):
    return "'" + pattern + "'" | pattern | '"' + pattern + '"'

compare_operators = oneOf("< > =  >= <=")
valname = alphanums + "-_"

# version number
vnum = Word(nums) + Optional(Word(nums + "."))

# a valid name for a package
val_package_name = Combine(Word(alphas + "".join((valname, "."))))

pkgname = Literal("pkgname=") + val_package_name

pkgver = Literal("pkgver=") + vnum

pkgrel = Literal("pkgrel=") + Word(nums)

epoch = Literal("epoch=") + Word(nums)

pkgdesc = Literal("pkgdesc=") + opQuotedString(Word(valname))

# define a valid architecture
valid_arch = opQuotedString(Word(valname))

arch = Literal("arch=(") + OneOrMore(valid_arch) + ")"

# TODO replace it with a better url parser
url = Literal("url=") + quotedString(printables)

license = Literal("license=(") + OneOrMore(opQuotedString(Word(valname))) + ")"

groups = Literal("groups=(") + OneOrMore(opQuotedString(Word(valname))) + ")"

dependency = opQuotedString(val_package_name.setResultsName("pname", listAllMatches=True) + Optional(compare_operators + vnum))

depends = Literal("depends=(") + ZeroOrMore(dependency) + ")"

makedepends = Literal("makedepends=(") + ZeroOrMore(dependency) + ")"

optdepends = Literal("optdepends=(") + ZeroOrMore(dependency) + ")"

checkdepends = Literal("checkdepends=(") + ZeroOrMore(dependency) + ")"

provides = Literal("provides=(") + ZeroOrMore(dependency) + ")"

conflicts = Literal("conflicts=(") + ZeroOrMore(dependency) + ")"

replaces = Literal("replaces=(") + ZeroOrMore(dependency) + ")"

backup = Literal("backup=(") + ZeroOrMore(opQuotedString(Word(valname))) + ")"

valid_options = oneOf("strip docs libtool emptydirs zipman ccache"
                            "distcc buildflags makeflags")
options = Literal("options=(") + ZeroOrMore(valid_options) + ")"

install = Literal("install=") + ZeroOrMore(opQuotedString(Word(valname)))

changelog = Literal("changelog=") + ZeroOrMore(opQuotedString(Word(valname)))

# TODO better parsing, allow filename::url, but forbid fi:lename
source = Literal("source=(") + ZeroOrMore(opQuotedString(Word(valname + "$:"))) + ")"

noextract = Literal("noxetract=(") + ZeroOrMore(opQuotedString(Word(valname)))
valid_chksums = oneOf("sha1sums sha256sums sha384sums sha512sums md5sums")
chksums = valid_chksums + "=(" + ZeroOrMore(opQuotedString(Word(alphanums))) + ")"

# TODO: improve function parsing
function_body = nestedExpr(opener="{", closer="}")
build = Literal("build() ") + function_body
check = Literal("check()") + function_body
package = Literal("package() ") + function_body

comment = "#" + OneOrMore(Word(printables)) + ZeroOrMore(lineEnd)

# TODO: match all possible PKGBUILDs
pkgbuildline = (pkgname | pkgver | pkgrel | pkgdesc | epoch | url | license
               | install | changelog | source | noextract | chksums | groups
               | arch | backup | depends | makedepends | optdepends | conflicts
               | provides | replaces | options | build | check | package | comment)
pkgbuildline.addParseAction(logging.info)
pkgbuild = OneOrMore(pkgbuildline)
