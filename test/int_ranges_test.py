#!/usr/bin/env python

import unittest

from vsc.atools.int_ranges import int_ranges2set


class TestIntRanges(unittest.TestCase):
    '''Test stuff implemented in vsc.atools.int_ranges'''

    def test_single2set(self):
        expected_set = set([2])
        self.assertEqual(expected_set, int_ranges2set('2'))

    def test_simple2set(self):
        expected_set = set(range(1, 11))
        self.assertEqual(expected_set, int_ranges2set('1-10'))


if __name__ == '__main__':
    unittest.main()
