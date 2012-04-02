from pyparsing import Word, OneOrMore, Literal, alphanums, Optional, oneOf, nums, alphas, quotedString, printables, ZeroOrMore, Combine, nestedExpr, lineEnd, restOfLine, stringEnd, Group
# import logging


# define some utility classes/functions/constants
# TODO: recalculate the need for a global variable
class expand_variable():
    """class which is needed to replace variables"""

    def __init__(self):
        self.vars = {}


def opQuotedString(pattern):
    return "'" + pattern + "'" | pattern | '"' + pattern + '"'

compare_operators = oneOf("< > =  >= <=")
valname = alphanums + "-_${}"

# version number
vnum = Word(nums) + Optional(Word(nums + ".-_"))

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
ac_chars = printables.replace("(", "").replace(")", "").replace("'", "").replace('"', "").replace("=", "")
license = Combine(Literal("license=(") + OneOrMore(opQuotedString(Word(ac_chars))) + ")")

groups = Combine(Literal("groups=(") + OneOrMore(opQuotedString(Word(valname))) + ")")

# all about dependencies
# normal dependency format: name + [qualifier] + version
dependency = (opQuotedString(val_package_name.setResultsName("pname", listAllMatches=True)
             + Optional(Group(compare_operators + vnum)).setResultsName("pversion", listAllMatches=True)))
# descriptive dependency: name + [qualifier] + version + ':' + description
descriptive_dep = (opQuotedString(val_package_name.setResultsName("pname", listAllMatches=True)
             + ZeroOrMore(':' + ZeroOrMore(Word(ac_chars)))))


depends = Literal("depends=(") + ZeroOrMore(dependency) + ")"

makedepends = Literal("makedepends=(") + ZeroOrMore(dependency) + ")"

optdepends = Literal("optdepends=(") + ZeroOrMore(descriptive_dep) + ")"

checkdepends = Literal("checkdepends=(") + ZeroOrMore(dependency) + ")"

provides = Literal("provides=(") + ZeroOrMore(dependency) + ")"

conflicts = Literal("conflicts=(") + ZeroOrMore(dependency) + ")"

replaces = Literal("replaces=(") + ZeroOrMore(dependency) + ")"

backup = Literal("backup=(") + ZeroOrMore(opQuotedString(Word(valname))) + ")"

valid_options = oneOf("strip docs libtool emptydirs zipman ccache"
                            "distcc buildflags makeflags")
options = Combine(Literal("options=(") + ZeroOrMore(opQuotedString(Optional("!") + valid_options)) + ")")

install = Combine(Literal("install=") + ZeroOrMore(opQuotedString(Optional("!") + Word(ac_chars))))

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

safe_variable = Combine("_" + Word(ac_chars) + "=" + opQuotedString(Word(ac_chars)))

# TODO: match all possible PKGBUILDs
pkgbuildline = (pkgname.setResultsName("pkgname")
        | pkgver.setResultsName("pkgver")
        | pkgrel.setResultsName("pkgrel")
        | pkgdesc.setResultsName("pkgdesc")
        | epoch.setResultsName("epoch")
        | url.setResultsName("url")
        | license.setResultsName("license")
        | install.setResultsName("install")
        | changelog.setResultsName("changelog")
        | source.setResultsName("source")
        | noextract.setResultsName("noextract")
        | chksums.setResultsName("chksums")
        | groups.setResultsName("groups")
        | arch.setResultsName("arch")
        | backup.setResultsName("backup")
        | depends.setResultsName("depends")
        | makedepends.setResultsName("makedepends")
        | optdepends.setResultsName("optdepends")
        | conflicts.setResultsName("conflicts")
        | provides.setResultsName("provides")
        | replaces.setResultsName("replaces")
        | options.setResultsName("options")
        | build.setResultsName("build")
        | check.setResultsName("check")
        | package.setResultsName("package")
        | maintainer.setResultsName("maintainer")
        | comment.setResultsName("comment")
        | safe_variable.setResultsName("variable")
        | screenshot.setResultsName("screenshot")) + ZeroOrMore(lineEnd)
parser = OneOrMore(pkgbuildline) + stringEnd
