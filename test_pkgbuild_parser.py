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

    def test_maintainer(self):
        # maintainer should be Inkane
        maintainer_Inkane = [
            "./pkgbuilds/valid/pd_pd_PKGBUILD",
            "./pkgbuilds/valid/vimpager_vimpager_PKGBUILD",
            "./pkgbuilds/valid/setconf_setconf_PKGBUILD",
            "./pkgbuilds/valid/libdesktop-agnostic_libdesktop-agnostic_PKGBUILD",
            "./pkgbuilds/valid/taskwarrior_taskwarrior_PKGBUILD",
            "./pkgbuilds/valid/e4rat-preload-lite_e4rat-preload-lite_PKGBUILD",
            "./pkgbuilds/valid/g15daemon_g15daemon_PKGBUILD",
            "./pkgbuilds/valid/freemind-unstable_freemind-unstable_PKGBUILD",
            "./pkgbuilds/valid/kdeplasma-applets-wolframalpha_kdeplasma-applets-wolframalpha_PKGBUILD",
            "./pkgbuilds/valid/xmonad_xmonad_PKGBUILD",
            "./pkgbuilds/valid/fim_fim_PKGBUILD"
                ]
        accept_maintainer = {
            "# Maintainer: John Doe <j.doe@xample.com>": "# Maintainer: John Doe <j.doe@xample.com>",
            "#Maintainer: John Doe <j.doe@xample.com>": "#Maintainer: John Doe <j.doe@xample.com>",
            "# Maintainer:John Doe <j.doe@xample.com>": "# Maintainer:John Doe <j.doe@xample.com>",
            "#Maintainer     :  John Doe <j.doe@xample.com>": "#Maintainer     :  John Doe <j.doe@xample.com>"
                }

        for f in maintainer_Inkane:
            self.assertEqual('# Maintainer: Inkane <neoinkaneglade@aol.com>',
                    pkgbuild_parser.parser.parseFile(f).maintainer,
                    msg="error in {}".format(f))

        for m in accept_maintainer:
            # TODO: test is currently useless
            self.assertEqual(accept_maintainer[m], m)

    def test_dependency(self):
        depends_list = {
                "depends=( 'foo' )": ["foo"],
                "depends=( 'xyz=23' )": ['xyz'],
                "depends=( 'foo>=4.1' \"bar<=2.21\" )": ["foo", "bar"]
                }
        for d in depends_list:
            self.assertEqual(pkgbuild_parser.depends.parseString(d).pname.asList(), depends_list[d])


if __name__ == "__main__":
    unittest.main()
