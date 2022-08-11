#!/usr/bin/env python

import unittest


class TestWorkAnalysis(unittest.TestCase):
    '''Test stuff implemented in vsc.atools.work_analysis'''

    def test_todo(self):
        from vsc.atools.work_analysis import compute_items_todo 
        expected_todo = set([4, 9])
        expected_completed = set([6, 7, 10])
        expected_failed = set([1, 2, 3, 5, 8])
        data_files = []
        t_str = '1-10'
        log_files = ['data/test.log']
        todo, completed, failed = compute_items_todo(data_files, t_str,
                                                     log_files)
        self.assertEqual(expected_todo, todo)
        self.assertEqual(expected_failed, failed)
        self.assertEqual(expected_completed, completed)

    def test_todo_redo(self):
        from vsc.atools.work_analysis import compute_items_todo 
        expected_todo = set([4, 9])
        expected_completed = set([6, 7, 10])
        expected_failed = set([1, 2, 3, 5, 8])
        data_files = []
        t_str = '1-10'
        log_files = ['data/test.log']
        todo, completed, failed = compute_items_todo(data_files, t_str,
                                                     log_files,
                                                     must_redo=True)
        self.assertEqual(expected_todo | expected_failed, todo)
        self.assertEqual(expected_failed, failed)
        self.assertEqual(expected_completed, completed)

    def test_todo_data(self):
        from vsc.atools.work_analysis import compute_items_todo 
        expected_todo = set([4, 9])
        expected_completed = set([6, 7, 10])
        expected_failed = set([1, 2, 3, 5, 8])
        data_files = ['data/data.csv']
        t_str = None
        log_files = ['data/test.log']
        todo, completed, failed = compute_items_todo(data_files, t_str,
                                                     log_files)
        self.assertEqual(expected_todo, todo)
        self.assertEqual(expected_failed, failed)
        self.assertEqual(expected_completed, completed)

    def test_todo_redo_data(self):
        from vsc.atools.work_analysis import compute_items_todo 
        expected_todo = set([4, 9])
        expected_completed = set([6, 7, 10])
        expected_failed = set([1, 2, 3, 5, 8])
        data_files = ['data/data.csv']
        t_str = None
        log_files = ['data/test.log']
        todo, completed, failed = compute_items_todo(data_files, t_str,
                                                     log_files,
                                                     must_redo=True)
        self.assertEqual(expected_todo | expected_failed, todo)
        self.assertEqual(expected_failed, failed)
        self.assertEqual(expected_completed, completed)

    def test_analysis(self):
        expeted_nr_items = 8
        expeted_nr_slaves = 1
        expected_slave = 'r1i1n3'
        from vsc.atools.work_analysis import LogAnalyzer
        log_file = 'data/test.log'
        analyzer = LogAnalyzer()
        analyzer.parse(log_file)
        item_times = analyzer.item_times()
        self.assertEqual(expeted_nr_items, len(item_times))
        slave_times = analyzer.slave_times()
        self.assertEqual(expeted_nr_items, len(slave_times))
        self.assertEqual(expected_slave, slave_times[0][0])
                 

if __name__ == '__main__':
    unittest.main()
