from pyparsing import Word, OneOrMore, Literal, alphanums, Optional, oneOf, nums, alphas, quotedString, printables, ZeroOrMore, Combine, nestedExpr, restOfLine, stringEnd, Group, Forward, LineEnd, QuotedString, White
# import logging


# define some utility classes/functions/constants


# TODO: accept only the neccessary characters
ac_chars = printables.replace("(", "").replace(")", "").replace("'", "").replace('"', "").replace("=", "")


# TODO: recalculate the need for a global variable
class expand_variable():
    """class which is needed to replace variables"""

    def __init__(self):
        self.vars = {}


def opQuotedString(pattern):
    return "'" + pattern + "'" | pattern | '"' + pattern + '"'


def Array(name, body, body2=None):
    if not body2:
        body2 = body
    return (Literal(name) + "=(" + body + ")" | Literal(name) + "[" + Word(nums) + "]" + body2)

compare_operators = oneOf("< > =  >= <=")
valname = alphanums + "-_${}+"

# version number
vnum = Word(nums) + Optional(Word(alphanums + ".-_"))

# a valid name for a package
val_package_name = Combine(Word(alphas + "".join((valname, "."))))

pkgname = Literal("pkgname=") + (opQuotedString(val_package_name)
          | "(" + opQuotedString(val_package_name) + ")")

pkgver = Literal("pkgver=") + vnum.leaveWhitespace() + LineEnd()

pkgrel = Literal("pkgrel=") + Word(nums)

epoch = Literal("epoch=") + Word(nums)

pkgdesc = Literal("pkgdesc=") + (QuotedString(quoteChar="'", multiline=True) | QuotedString(quoteChar='"', multiline=True))


screenshot = "screenshot=" + quotedString

# define a valid architecture
valid_arch = opQuotedString(Word(valname))

arch = Array("arch", OneOrMore(valid_arch), valid_arch)


license = Array("license", OneOrMore(opQuotedString(Word(ac_chars))), opQuotedString(Word(ac_chars)))

# TODO: replace it with a better url parser
url = Literal("url=") + opQuotedString(Word(printables))

groups = Combine(Literal("groups=(") + OneOrMore(opQuotedString(Word(valname))) + ")")
groups = Array("groups", OneOrMore(opQuotedString(Word(valname))), opQuotedString(Word(valname)))

# all about dependencies
# normal dependency format: name + [qualifier] + version
dependency = (opQuotedString(val_package_name.setResultsName("pname", listAllMatches=True)
             + Optional(Group(compare_operators + vnum)).setResultsName("pversion", listAllMatches=True)))
# descriptive dependency: name + [qualifier] + version + ':' + description
descriptive_dep = (opQuotedString(val_package_name.setResultsName("pname", listAllMatches=True)
             + ZeroOrMore(':' + ZeroOrMore(Word(ac_chars)))))


depends = Array("depends", ZeroOrMore(dependency), dependency)

makedepends = Array("makedepends", ZeroOrMore(dependency), dependency)

optdepends = Array("optdepends", ZeroOrMore(descriptive_dep))

checkdepends = Array("checkdepends", ZeroOrMore(dependency), dependency)

provides = Array("provides", ZeroOrMore(dependency), dependency)

conflicts = Array("conflicts", ZeroOrMore(dependency), dependency)

replaces = Array("replaces", ZeroOrMore(dependency), dependency)

backup = Array("backup", ZeroOrMore(opQuotedString(Word(ac_chars))), opQuotedString(Word(ac_chars)))

valid_options = oneOf("strip docs libtool emptydirs zipman ccache"
                            "distcc buildflags makeflags")
options = Array("options", ZeroOrMore(opQuotedString(Optional("!") + valid_options)))

install = Combine(Literal("install=") + ZeroOrMore(opQuotedString(Optional("!") + Word(ac_chars))))

changelog = Combine(Literal("changelog=") + ZeroOrMore(opQuotedString(Word(valname))))

# TODO better parsing, allow filename::url, but forbid fi:lename
source = Array("source", ZeroOrMore(opQuotedString(Word(ac_chars + '='))), opQuotedString(Word(ac_chars + '=')))

noextract = Literal("noextract=(") + ZeroOrMore(opQuotedString(Word(ac_chars))) + ")"
valid_chksums = oneOf("sha1sums sha256sums sha384sums sha512sums md5sums")
chksums = valid_chksums + "=(" + ZeroOrMore(opQuotedString(Word(alphanums))) + ")"

# TODO: improve function parsing
function_body = nestedExpr(opener="{", closer="}")
build = Literal("build()") + function_body
check = Literal("check()") + function_body
package = Literal("package()") + function_body

maintainer = Combine(Literal("#") + Optional(White()) + Literal("Maintainer:") + restOfLine)
comment = Combine("#" + restOfLine)

safe_variable = Combine("_" + Word(ac_chars) + "=" + opQuotedString(Word(ac_chars.replace(";", ""))))
var_array = "(" + opQuotedString(Word(ac_chars + " =")) + ")"
bad_variable = Combine(Word(ac_chars) + "=" + (var_array | opQuotedString(Word(ac_chars))))

if_expression = Forward()
statement_seperator = Literal(";")
statement_block = Forward()

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
        | comment.setResultsName("comment", listAllMatches=True)
        | safe_variable.setResultsName("variable")
        | bad_variable.setResultsName("variable")
        | if_expression
        | screenshot.setResultsName("screenshot")
        | statement_seperator)

statement_block << nestedExpr(opener="{", closer="}", content=OneOrMore(pkgbuildline))

# TODO: there has to be a better way...
if_expression << (
   Group("[[" + OneOrMore(Word(alphanums + r'''$=_-'"''')) + "]]" + (Literal("&&") | Literal("||")) + (statement_block | pkgbuildline))
 | Group("[" + OneOrMore(Word(alphanums + r'''$=_-'"''')) + "]" + (Literal("&&") | Literal("||")) + (statement_block | pkgbuildline))
 | Group(Literal("if") + QuotedString(quoteChar="[", endQuoteChar="]", multiline=True) + "then" + OneOrMore(pkgbuildline) + Optional("else" + OneOrMore(pkgbuildline)) + "fi")
)

pb = OneOrMore(pkgbuildline)
parser = OneOrMore(pkgbuildline) + stringEnd
