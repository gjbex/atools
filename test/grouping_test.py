#!/usr/bin/env python

import os
import unittest
from unittest import mock

from vsc.atools.int_ranges import set2stepped_int_ranges
from vsc.atools.utils import get_group_size, supports_grouping
from vsc.atools.work_analysis import (group_start_ids, group_task_ids,
                                      read_data_rows)


SLURM_VARS = {
    'array_idx_var': 'SLURM_ARRAY_TASK_ID',
    'array_step_var': 'SLURM_ARRAY_TASK_STEP',
}
TORQUE_VARS = {
    'array_idx_var': 'PBS_ARRAYID',
}


class TestGrouping(unittest.TestCase):
    '''Test grouping of tasks into array jobs'''

    def test_group_task_ids(self):
        self.assertEqual(set(range(1, 6)), group_task_ids(1, 5))
        self.assertEqual(set(range(6, 11)), group_task_ids(6, 5))

    def test_group_size_one(self):
        self.assertEqual({7}, group_task_ids(7, 1))
        self.assertEqual({1, 3, 7}, group_start_ids({1, 3, 7}, 1))

    def test_group_start_ids(self):
        self.assertEqual({1, 6, 11}, group_start_ids(set(range(1, 12)), 5))

    def test_partial_todo(self):
        # task 4 is in group 1-5, task 9 in 6-10, 57 in 56-60
        self.assertEqual({1, 6, 56}, group_start_ids({4, 9, 57}, 5))

    def test_invalid_group_size(self):
        with self.assertRaises(ValueError):
            group_start_ids({1}, 0)
        with self.assertRaises(ValueError):
            group_task_ids(1, 0)

    def test_stepped_ranges(self):
        self.assertEqual('1-101:5',
                         set2stepped_int_ranges(set(range(1, 102, 5)), 5))
        self.assertEqual('1-6:5,56-56:5',
                         set2stepped_int_ranges({1, 6, 56}, 5))
        self.assertEqual('56-56:5', set2stepped_int_ranges({56}, 5))
        self.assertEqual('', set2stepped_int_ranges(set(), 5))

    def test_stepped_ranges_step_one(self):
        self.assertEqual('1-3,7', set2stepped_int_ranges({1, 2, 3, 7}, 1))

    def test_supports_grouping(self):
        self.assertTrue(supports_grouping(SLURM_VARS))
        self.assertFalse(supports_grouping(TORQUE_VARS))

    def test_group_size_from_env(self):
        with mock.patch.dict(os.environ, {'SLURM_ARRAY_TASK_STEP': '5'}):
            self.assertEqual(5, get_group_size(SLURM_VARS))

    def test_group_size_without_step(self):
        with mock.patch.dict(os.environ):
            os.environ.pop('SLURM_ARRAY_TASK_STEP', None)
            self.assertEqual(1, get_group_size(SLURM_VARS))

    def test_group_size_unsupported(self):
        with mock.patch.dict(os.environ, {'SLURM_ARRAY_TASK_STEP': '5'}):
            self.assertEqual(1, get_group_size(TORQUE_VARS))

    def test_read_data_rows(self):
        rows = read_data_rows(['data/data.csv'], [2, 3])
        self.assertEqual({2, 3}, set(rows.keys()))
        with open('data/data.csv') as csv_file:
            names = csv_file.readline().strip().split(',')
        self.assertEqual(set(names), set(rows[2].keys()))

    def test_read_data_rows_empty(self):
        self.assertEqual({}, read_data_rows(['data/data.csv'], []))


if __name__ == '__main__':
    unittest.main()
