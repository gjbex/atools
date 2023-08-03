#!/usr/bin/env python

import os
import unittest


class TestShell(unittest.TestCase):
    '''Class to test functions in vsc.shell'''

    def test_shells(self):
        from vsc.shell import get_shells
        expected_shells = {'bash', 'sh', 'tcsh', 'csh'}
        self.assertEqual(expected_shells, set(get_shells()))

    def test_bash_var(self):
        from vsc.shell import create_bash_var_def
        expected_var_def = 'export a="b"'
        var_def = create_bash_var_def('a', 'b')
        self.assertEqual(expected_var_def, var_def)

    def test_sh_var(self):
        from vsc.shell import create_var_def
        expected_var_def = 'export a="b"'
        var_def = create_var_def('a', 'b', 'sh')
        self.assertEqual(expected_var_def, var_def)

    def test_csh_var(self):
        from vsc.shell import create_csh_var_def
        expected_var_def = 'setenv a "b"'
        var_def = create_csh_var_def('a', 'b')
        self.assertEqual(expected_var_def, var_def)

    def test_unknown_shell(self):
        from vsc.shell import create_var_def, UnknownShellError
        try:
            _ = create_var_def('a', 'b', 'bla')
        except UnknownShellError:
            pass
        
    def test_sh_vars(self):
        from vsc.shell import create_var_defs
        expected_var_defs = {'export a="b"', 'export c="d"', 'export e="f"'}
        vars = {
            'a': 'b',
            'c': 'd',
            'e': 'f',
        }
        var_defs = create_var_defs(vars, 'sh')
        var_def_set = set(var_defs.split(os.linesep))
        self.assertEqual(expected_var_defs, var_def_set)

    def test_tcsh_vars(self):
        from vsc.shell import create_var_defs
        expected_var_defs = {'setenv a "b"', 'setenv c "d"', 'setenv e "f"'}
        vars = {
            'a': 'b',
            'c': 'd',
            'e': 'f',
        }
        var_defs = create_var_defs(vars, 'tcsh')
        var_def_set = set(var_defs.split(os.linesep))
        self.assertEqual(expected_var_defs, var_def_set)


if __name__ == '__main__':
    unittest.main()
