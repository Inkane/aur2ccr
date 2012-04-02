import unittest2
import glob
import pkgbuild_parser
from pyparsing import ParseException


class ParseTest(unittest2.TestCase):

    def test_can_parse(self):
        for f in glob.glob("./pkgbuilds/*"):
            try:
                pkgbuild_parser.parser.parseFile(f)
            except ParseException:
                assert False, "{} failed".format(f)

if __name__ == "__main__":
    unittest2.main()
