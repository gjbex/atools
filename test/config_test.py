#!/usr/bin/env python

import unittest


class TestConfig(unittest.TestCase):
    '''Test stuff implemented in vsc.atools.config'''

    def test_get_var_config_torque(self):
        var_expected = {
            'array_idx_var': 'PBS_ARRAYID',
            'job_id_var': 'PBS_JOBID',
            'job_name_var': 'PBS_JOBNAME',
        }
        file_name = 'data/atools_torque.conf'
        from vsc.atools.config import get_var_config
        var_names = get_var_config(file_name)
        self.assertGreaterEqual(var_expected.items(), var_names.items())

    def test_get_mode_config_default(self):
        scripts_expected = ('empty_text', 'reduce_text')
        file_name = 'data/atools_torque.conf'
        from vsc.atools.config import get_mode_config
        scripts = get_mode_config(file_name)
        self.assertEqual(scripts_expected, scripts)

    def test_get_mode_config_text(self):
        scripts_expected = ('empty_text', 'reduce_text')
        file_name = 'data/atools_torque.conf'
        from vsc.atools.config import get_mode_config
        scripts = get_mode_config(file_name, 'text')
        self.assertEqual(scripts_expected, scripts)

    def test_get_mode_config_csv(self):
        scripts_expected = ('empty_csv', 'reduce_csv')
        file_name = 'data/atools_torque.conf'
        from vsc.atools.config import get_mode_config
        scripts = get_mode_config(file_name, 'csv')
        self.assertEqual(scripts_expected, scripts)

if __name__ == '__main__':
    unittest.main()
