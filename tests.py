# coding=utf-8
"""
 coding=utf-8
 Author:
   Active8 (04-03-15)
   license: GNU-GPL2
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from unittester import *
import historybash
import sys

from io import StringIO


class HistoryBashTest(unittest.TestCase):
    """
    @type unittest.TestCase: class
    @return: None
    """
    def setUp(self):
        """
        setUp
        """
        sto = open(os.path.join(os.path.expanduser("~"), ".bash_history"), "rt", encoding='utf-8').read()
        open(os.path.join(os.path.expanduser("~"), ".bash_history.bak"), "wt", encoding='utf-8').write(sto)
        sto2 = "ls\ncd\ncd\nsudo updatedb"
        open(os.path.join(os.path.expanduser("~"), ".bash_history"), "wt", encoding='utf-8').write(sto2)

    def tearDown(self):
        """
        tearDown
        """
        sto = open(os.path.join(os.path.expanduser("~"), ".bash_history.bak"), "rt", encoding='utf-8').read()
        open(os.path.join(os.path.expanduser("~"), ".bash_history"), "wt", encoding='utf-8').write(sto)

    def test_context(self):
        """
        test_context
        """
        out = StringIO()
        std = sys.stdout
        sys.stdout = out
        historybash.main()
        self.assertEqual(out.getvalue(), 'ls\ncd\nsudo updatedb\n')

    def test_fails(self):
        """
        test_fails
        """
        self.assertTrue(False)


def main():
    """
    main
    """
    unit_test_main(globals())


if __name__ == "__main__":
    main()
