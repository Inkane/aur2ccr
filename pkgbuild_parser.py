import pyparsing as pypar
from pyparsing import Word
from pyparsing import Literal

compare_operators = pypar.oneOf("< > =  >= <=")
valname = pypar.alphanums+"-_"

# version number
vnum = Word(pypar.nums) + pypar.Optional(Word(pypar.nums + "."))

# a valid name for a package
package = Word(pypar.alphas + "".join((valname,".")))

# match the pkgname variable
pkgname = Literal("pkgname=") + package

# the pkgver variable
pkgver = Literal("pkgver=") + vnum

# the pkgrel variable 
pkgrel = Literal("pkgrel=") + Word(pypar.nums)

# the epoch variable
epoch = Literal("epoch=") + Word(pypar.nums)

# the pkgdesc variable
pkgdesc = Literal("pkgdesc=") + pypar.quotedString(valname) | Word(valname)

# define a valid architecture
valid_arch = pypar.quotedString(valname) | Word(valname)

# the arch variable
arch = Literal("arch=(") + pypar.OneOrMore(valid_arch) + ")"

# the url variable
# TODO replace it with a better url parser
url = Literal("url=") + pypar.quotedString(pypar.printables)

# the license variable
license = Literal("license=(") + pypar.OneOrMore(valname) + ")"

# the groups variable
groups = Literal("groups=(") + pypar.OneOrMore(valname) + ")"

# a dependency is a quoted pkname with optional comparision of version numer
dependency = "'" + package + pypar.Optional(compare_operators + vnum) + "'" | '"' + package + pypar.Optional(compare_operators + vnum) + '"'

# the depends variable
depends = Literal("depends=(") + pypar.ZeroOrMore(dependency) + ")"

# the makedepends variable
makedepends = Literal("makedepends=(") + pypar.ZeroOrMore(dependency) + ")"

# the optdepends variable
optdepends = Literal("optdepends=(") + pypar.ZeroOrMore(dependency) + ")"

# the checkdepends variable
checkdepends = Literal("checkdepends=(") + pypar.ZeroOrMore(dependency) + ")"

# the provides variable, need some checking to disallow pckgname>3.2
provides = Literal("provides=(") + pypar.ZeroOrMore(dependency) + ")"

conflicts = Literal("conflicts=(") + pypar.ZeroOrMore(dependency) + ")"

replaces = Literal("replaces=(") + pypar.ZeroOrMore(dependency) + ")"

backup = Literal("backup=(") + pypar.ZeroOrMore(valname) + ")"

valid_options = pypar.oneOf("strip docs libtool emptydirs zipman ccache"
                            "distcc buildflags makeflags")
options = Literal("options=(") + pypar.ZeroOrMore(valid_options) + ")"

install = Literal("install=") + pypar.ZeroOrMore(pypar.quotedString(valname)
                                                | Word(valname))

changelog = Literal("changelog=") + pypar.ZeroOrMore(pypar.quotedString(valname)
                                                | Word(valname))
# TODO better parsing, allow filename::url, but forbid fi:lename
source = Literal("source=(") + pypar.ZeroOrMore(pypar.quotedString(valname+"$:")
                                                | Word(valname+"$:")) + ")"

noextract = Literal("noxetract=(") +pypar.ZeroOrMore(pypar.quotedString(valname)
                                                     | Word(valname))
valid_chksums = pypar.oneOf("sha1sums sha256sums sha384sums sha512sums md5sums")
chksums = valid_chksums + "=(" + pypar.ZeroOrMore(pypar.quotedString(
                                        pypar.alphanums) | pypar.alphanums) + ")"

# TODO: improve function parsing
function_body = pypar.nestedExpr(opener="{", closer="}")
build = Literal("build() ") + function_body

