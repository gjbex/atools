#!/usr/bin/env python

import unittest

from vsc.atools.int_ranges import int_ranges2set, InvalidRangeSpecError


class TestIntRanges(unittest.TestCase):
    '''Test stuff implemented in vsc.atools.int_ranges'''

    def test_single2set(self):
        expected_set = set([2])
        self.assertEqual(expected_set, int_ranges2set('2'))

    def test_ind2set(self):
        expected_set = set([2, 4, 8])
        self.assertEqual(expected_set, int_ranges2set('2,4,8'))

    def test_simple2set(self):
        expected_set = set(range(1, 11))
        self.assertEqual(expected_set, int_ranges2set('1-10'))

    def test_multiple2set(self):
        expected_set = set(range(1, 11)) | set(range(21, 31))
        self.assertEqual(expected_set, int_ranges2set('1-10,21-30'))

    def test_multiple_ind2set(self):
        expected_set = set(range(5, 11)) | set(range(21, 31))
        expected_set.add(3)
        expected_set.add(15)
        expected_set.add(35)
        self.assertEqual(expected_set, int_ranges2set('3,5-10,15,35,21-30'))

    def test_invalid_bounds2set(self):
        try:
            _ = int_ranges2set('5-1')
            self.assertTrue(False)
        except InvalidRangeSpecError:
            pass

    def test_invalid_expr2set(self):
        try:
            _ = int_ranges2set('-1')
            self.assertTrue(False)
        except InvalidRangeSpecError:
            pass

    
if __name__ == '__main__':
    unittest.main()
