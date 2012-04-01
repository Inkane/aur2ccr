from pyparsing import Word, OneOrMore, Literal, alphanums, Optional, oneOf, nums, alphas, quotedString, printables, ZeroOrMore, Combine, nestedExpr, lineEnd, restOfLine, stringEnd
# import logging


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

pkgname = Literal("pkgname=") + opQuotedString(val_package_name)

pkgver = Literal("pkgver=") + vnum

pkgrel = Literal("pkgrel=") + Word(nums)

epoch = Literal("epoch=") + Word(nums)

pkgdesc = Literal("pkgdesc=") + quotedString

screenshot = "screenshot=" + quotedString

# define a valid architecture
valid_arch = opQuotedString(Word(valname))

arch = Literal("arch=(") + OneOrMore(valid_arch) + ")"

# TODO: replace it with a better url parser
url = Literal("url=") + quotedString

# TODO: accept only the neccessary characters
ac_chars = printables.replace("(", "").replace(")", "")
license = Combine(Literal("license=(") + OneOrMore(opQuotedString(Word(ac_chars))) + ")")

groups = Combine(Literal("groups=(") + OneOrMore(opQuotedString(Word(valname))) + ")")

# all about dependencies
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
options = Combine(Literal("options=(") + ZeroOrMore(valid_options) + ")")

install = Combine(Literal("install=") + ZeroOrMore(opQuotedString(Word(valname))))

changelog = Combine(Literal("changelog=") + ZeroOrMore(opQuotedString(Word(valname))))

# TODO better parsing, allow filename::url, but forbid fi:lename
source = Literal("source=(") + ZeroOrMore(opQuotedString(Word(ac_chars))) + ")"

noextract = Literal("noxetract=(") + ZeroOrMore(opQuotedString(Word(valname)))
valid_chksums = oneOf("sha1sums sha256sums sha384sums sha512sums md5sums")
chksums = valid_chksums + "=(" + ZeroOrMore(opQuotedString(Word(alphanums))) + ")"

# TODO: improve function parsing
function_body = nestedExpr(opener="{", closer="}")
build = Literal("build()") + function_body
check = Literal("check()") + function_body
package = Literal("package()") + function_body

maintainer = Combine("#" + Literal("Maintainer:") + restOfLine)
comment = Combine("#" + restOfLine)

# TODO: match all possible PKGBUILDs
pkgbuildline = (pkgname.setResultsName("pkgname") | pkgver.setResultsName("pkgver") | pkgrel.setResultsName("pkgrel") | pkgdesc.setResultsName("pkgdesc") | epoch.setResultsName("epoch") | url.setResultsName("url") | license.setResultsName("license")
               | install.setResultsName("install") | changelog.setResultsName("changelog") | source.setResultsName("source") | noextract.setResultsName("noextract") | chksums.setResultsName("chksums") | groups.setResultsName("groups")
               | arch.setResultsName("arch") | backup.setResultsName("backup") | depends.setResultsName("depends") | makedepends.setResultsName("makedepends") | optdepends.setResultsName("optdepends") | conflicts.setResultsName("conflicts")
               | provides.setResultsName("provides") | replaces.setResultsName("replaces") | options.setResultsName("options") | build.setResultsName("build") | check.setResultsName("check") | package.setResultsName("package")
               | maintainer.setResultsName("maintainer") | comment.setResultsName("comment")) | screenshot.setResultsName("screenshot") + ZeroOrMore(lineEnd)
pkgbuild = OneOrMore(pkgbuildline) + stringEnd
