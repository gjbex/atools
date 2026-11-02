#!/usr/bin/env python

import unittest

from vsc.atools.utils import check_var_names, ProtectedVariableError


class TestVarNames(unittest.TestCase):
    '''Test the check on variable names defined from data files'''

    def test_valid_names(self):
        names = {'alpha', 'beta', '_x', 'PATH_TO_DATA', 'rest', 'a1'}
        self.assertEqual([], check_var_names(names))

    def test_invalid_names(self):
        names = {'alpha', 'my-param', '1st', '', 'two words'}
        self.assertEqual(['', '1st', 'my-param', 'two words'],
                         check_var_names(names))

    def test_protected_names(self):
        for name in ['BASH_ENV', 'ENV', 'SHELLOPTS', 'BASHOPTS', 'PS4',
                     'PATH', 'LD_PRELOAD', 'LD_LIBRARY_PATH']:
            with self.assertRaises(ProtectedVariableError):
                check_var_names({'alpha', name})

    def test_exported_function(self):
        with self.assertRaises(ProtectedVariableError):
            check_var_names({'BASH_FUNC_ls%%'})

    def test_protected_before_invalid(self):
        with self.assertRaises(ProtectedVariableError):
            check_var_names({'my-param', 'BASH_ENV'})


if __name__ == '__main__':
    unittest.main()
