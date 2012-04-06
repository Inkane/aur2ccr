import pyparsing
from pyparsing import Word, OneOrMore, Literal, alphanums, Optional, oneOf, nums, alphas, quotedString, printables, ZeroOrMore, Combine, nestedExpr, restOfLine, stringEnd, Group, Forward, LineEnd, QuotedString, White
import re
# import logging


# define some utility classes/functions/constants

# TODO: decide if this should be in an extra file
class variable_tracker:
    """used to track variables in a shell """

    def __init__(self):
        self.variables = dict()
        #_base_var = Literal("$") + (("{" + Word(alphanums + "_-").setResultsName("var_name", listAllMatches=True) + Optional("[" + Word(nums + "*@") + "]") + "}")
                 #| Word(alphanums))
        _simple_var = Literal("$") + Word(alphanums + "_-").setResultsName("varname")
        _brace_substitute_part = Optional("/" + (Word(alphanums + "_-").setResultsName("orig"))
                                 + Optional("/" + Word(alphanums + "_-!?/\\").setResultsName("new")))
        _array_access = "[" + Word(nums + "@*").setResultsName("position") + "]"
        _brace_var = Literal("${") + Word(alphanums + "_-").setResultsName("text") + _brace_substitute_part + Optional(_array_access) + "}"
        _brace_var.setParseAction(lambda x: x if not x.new else re.sub(x.orig, x.new, x.text))
        _base_var = _simple_var | _brace_var
        self.var = ('"' + _base_var + '"') | _base_var
        self.var("variable")

    def track_variable(self, varname, value):
        """track a variable, overriding previous existing values"""
        self.variables[varname] = value

    def substitute_variable(self, expression):
        """replace all variables with its value, raises an error if one does not exist"""
        if "$" not in expression:
            # abort if there is no variable
            raise pyparsing.ParseException
        #for variable in self.var.searchString(expression)
        # what needs to be substituted:
        # $foo, "$foo"
        # ${foo}, "${foo}"
        # ${foo[1]}, ${foo[@]}, ${foo[*]}


# TODO: accept only the neccessary characters
ac_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&*+,-./:;<>?@[\\]^_`{|}~'


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
# vnum = Word(nums) + Optional(Word(alphanums + ".-_"))
# It seems like j3.134l.i is a valid version number...
# It is not allowed, but some PKGBUILDs seem to contain hyphens (freeorion)
vnum = Word(alphanums + "._-")

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

# helper defintion for license, to allow license=('custom: "commercial"')
tmp_lic = opQuotedString(Word(ac_chars)) | opQuotedString(Literal("custom") + ":" + opQuotedString(Word(ac_chars)))
license = Array("license", OneOrMore(tmp_lic), tmp_lic)

# TODO: replace it with a better url parser
url = Literal("url=") + opQuotedString(Word(printables))

groups = Combine(Literal("groups=(") + OneOrMore(opQuotedString(Word(valname))) + ")")
groups = Array("groups", OneOrMore(opQuotedString(Word(valname))), opQuotedString(Word(valname)))

# all about dependencies
# normal dependency format: name + [qualifier] + version
dependency = (opQuotedString((val_package_name.setResultsName("pname", listAllMatches=True)
             + Optional(Group(compare_operators + vnum)).setResultsName("pversion", listAllMatches=True))))
# descriptive dependency: name + [qualifier] + version + ':' + description
descriptive_dep = (opQuotedString(val_package_name.setResultsName("pname", listAllMatches=True)
             + ZeroOrMore(':' + ZeroOrMore(Word(ac_chars)))))


depends = Group(Array("depends", ZeroOrMore(dependency), dependency))

makedepends = Group(Array("makedepends", ZeroOrMore(dependency), dependency))

optdepends = Group(Array("optdepends", ZeroOrMore(descriptive_dep)))

checkdepends = Group(Array("checkdepends", ZeroOrMore(dependency), dependency))

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
def function_head(name):
    """name must be a pyparsing object, e.g. Literal, not a string"""
    return (Optional("function") + name + "()" | Literal("function") + name)

function_body = nestedExpr(opener="{", closer="}")
build = function_head(Literal("build")) + function_body
check = function_head(Literal("check")) + function_body
package = function_head(Literal("package")) + function_body

maintainer = Combine(Literal("#") + Optional(White()) + Literal("Maintainer:") + restOfLine)
comment = Combine("#" + restOfLine)

# variables, arrays, functions, etc...
safe_variable = Combine("_" + Word(ac_chars) + "=" + opQuotedString(Word(ac_chars.replace(";", ""))))
var_array = "(" + OneOrMore(opQuotedString(Word(ac_chars + " ="))) + ")"
bad_variable = Combine(Word(ac_chars) + "=" + (var_array | opQuotedString(Word(ac_chars))))

generic_function = function_head(Word(alphas + "_", alphanums + "_")) + function_body

if_expression = Forward()
case_statement = Forward()
statement_seperator = Literal(";")
statement_block = Forward()
bash_functions = oneOf("echo sed awk") + restOfLine


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
        | case_statement
        | generic_function
        | screenshot.setResultsName("screenshot")
        | bash_functions  # those shouldn't be in PKGBUILDs outside of build
        | statement_seperator)

statement_block << (nestedExpr(opener="{", closer="}", content=OneOrMore(pkgbuildline)) | OneOrMore(pkgbuildline))

# TODO: there has to be a better way...

condition = ((QuotedString(quoteChar="[[", endQuoteChar="]]", multiline=True)
           | QuotedString(quoteChar="[", endQuoteChar="]", multiline=True)) + ZeroOrMore(";"))
bool_operator = Literal("&&") | Literal("||")
con_then = condition + Literal("then") + statement_block
if_expression << ((condition + bool_operator + (statement_block))
        | Literal("if") + con_then + ((ZeroOrMore("elif" + con_then))
                                     + Optional("else" + statement_block)) + "fi")

case_statement << (Literal("case") + opQuotedString(Word(ac_chars)) + "in"
                   + OneOrMore(opQuotedString(Word(ac_chars)) + ")" + OneOrMore(pkgbuildline)) + "esac")

pb = OneOrMore(pkgbuildline)
parser = OneOrMore(pkgbuildline) + stringEnd
