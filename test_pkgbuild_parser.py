import unittest
import glob
import pkgbuild_parser
from pyparsing import ParseException


class ParseTest(unittest.TestCase):

    def test_can_parse(self):
        for f in glob.glob("./pkgbuilds/valid/*"):
            try:
                pkgbuild_parser.parser.parseFile(f)
            except ParseException:
                assert False, "{} failed".format(f)

    def test_dependency(self):
        pass


if __name__ == "__main__":
    unittest.main()
