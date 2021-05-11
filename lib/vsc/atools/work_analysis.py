'''Module containing utilities to analyse the work to be done, and the
work done'''

import csv 
import os
import sqlite3
import sys

from vsc.atools.log_parser import LogParser
from vsc.atools.int_ranges import int_ranges2set
from vsc.atools.utils import ArrayToolsError


class MissingSourceError(ArrayToolsError):
    '''Exception denoting that no data sources were specified in a
    function call'''

    def __init__(self, function_name):
        super(MissingSourceError, self).__init__()
        self._function_name = function_name
        self.errno = 61

    def __str__(self):
        msg = "expecting data files and/or array range calling '{0}'"
        return msg.format(self._function_name)


def _compute_data_ids(data_files, sniff=1024, no_sniffer=False):
    nr_work_items = sys.maxsize
    for filename in data_files:
        with open(filename, 'r') as csv_file:
            if no_sniffer:
                csv_reader = csv.DictReader(csv_file, fieldnames=None,
                                            restkey='rest',
                                            restval=None)
            else:
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(csv_file.read(sniff))
                csv_file.seek(0)
                csv_reader = csv.DictReader(csv_file, fieldnames=None,
                                            restkey='rest',
                                            restval=None,
                                            dialect=dialect)
            row_nr = 0
            for _ in csv_reader:
                row_nr += 1
            if row_nr < nr_work_items:
                nr_work_items = row_nr
    return set(range(1, nr_work_items + 1))


def compute_items_todo(data_files, t_str, log_files, must_redo=False,
                       sniff=1024, no_sniffer=False):
    if data_files and t_str:
        todo = (_compute_data_ids(data_files, sniff, no_sniffer) &
                int_ranges2set(t_str))
    elif data_files:
        todo = _compute_data_ids(data_files, sniff, no_sniffer)
    elif t_str:
        todo = int_ranges2set(t_str)
    else:
        raise MissingSourceError('compute_todo')
    completed = set()
    failed = set()
    if log_files:
        for filename in log_files:
            log_parser = LogParser()
            events = log_parser.parse(filename)
            for event in events:
                if event.type == 'completed':
                    todo.discard(event.item_id)
                    completed.add(event.item_id)
                elif event.type == 'failed':
                    failed.add(event.item_id)
        if not must_redo:
            failed -= completed
            todo -= failed
    return todo, completed, failed


class LogAnalyzer(object):
    '''Class representing a log analyzer, creating a SQLite3 database
    for the actual analysis'''

    def __init__(self, db_name=None):
        '''Create the database and its tables'''
        if not db_name:
            db_name = ':memory:'
        must_init = not os.path.exists(db_name)
        self._conn = sqlite3.connect(db_name)
        if must_init:
            self.init()

    def init(self):
        cursor = self._conn.cursor()
        sql = '''
            CREATE TABLE work_items (
                item_id     INTEGER    PRIMARY KEY,
                slave_id    TEXT,
                start_time  INTEGER
            );'''
        cursor.execute(sql)
        sql = '''
            CREATE TABLE results (
                item_id     INTEGER    PRIMARY KEY,
                exit_code   INTEGER,
                end_time    INTEGER,
                FOREIGN KEY (item_id)
                    REFERENCES work_items (item_id)
            );'''
        cursor.execute(sql)
        self._conn.commit()

    def reset(self):
        cursor = self._conn.cursor()
        for table in ['work_items', 'results']:
            cursor.execute('DROP TABLE ?', (table, ))
        self._conn.commit()
        self.init()

    def parse(self, filename):
        cursor = self._conn.cursor()
        log_parser = LogParser()
        results_sql = '''
            INSERT INTO results (item_id, exit_code, end_time)
                VALUES (?, ?, strftime('%s', ?));'''
        work_items_sql = '''
            INSERT INTO work_items (item_id, slave_id, start_time)
                VALUES (?, ?, strftime('%s', ?));'''
        for event in log_parser.parse(filename):
            if event.type == 'completed' or event.type == 'failed':
                cursor.execute(results_sql, (event.item_id,
                                             event.exit_status,
                                             event.time_stamp))
            else:
                cursor.execute(work_items_sql, (event.item_id,
                                                event.slave_id,
                                                event.time_stamp))
        self._conn.commit()

    def item_times(self, exclude_failed=False):
        '''returns a list of tuples with the item IDs, slave IDx, and the
         run time in seconds'''
        no_failed = ' AND e.exit_code = 0' if exclude_failed else ''
        sql = '''
            SELECT s.item_id, s.slave_id, e.end_time - s.start_time
                FROM work_items AS s, results AS e
                WHERE s.item_id = e.item_id{0}
                ORDER BY s.item_id;'''.format(no_failed)
        cursor = self._conn.cursor()
        return cursor.execute(sql).fetchall()
                                               
    def slave_times(self, exclude_failed=False):
        '''returns a list of tuples with the slave IDs, run time in
        seconds, and the number of items computed by the slave'''
        no_failed = ' AND e.exit_code = 0' if exclude_failed else ''
        sql = '''
            SELECT s.slave_id, s.item_id, e.end_time - s.start_time
                FROM work_items AS s, results AS e
                WHERE s.item_id = e.item_id{0}
                ORDER BY s.slave_id, s.item_id;'''.format(no_failed)
        cursor = self._conn.cursor()
        return cursor.execute(sql).fetchall()

    def nr_slaves(self):
        sql = '''
            SELECT COUNT(DISTINCT slave_id)
                FROM work_items'''
        cursor = self._conn.cursor()
        return cursor.execute(sql).fetchone()

    def item_stats(self, exclude_failed=False):
        '''returns a tuple containing the number of items computed,
        the minimum, average, and maximum run time'''
        no_failed = ' AND e.exit_code = 0' if exclude_failed else ''
        sql = '''
            SELECT COUNT(*),
                   AVG(e.end_time - s.start_time),
                   MIN(e.end_time - s.start_time),
                   MAX(e.end_time - s.start_time),
                   SUM(e.end_time - s.start_time)
                FROM work_items AS s, results AS e
                WHERE s.item_id = e.item_id{0};'''.format(no_failed)
        cursor = self._conn.cursor()
        return cursor.execute(sql).fetchone()

    def slave_stats(self, exclude_failed=False):
        '''returns a tuple containing the number of items computed,
        the minimum, average, and maximum run time'''
        no_failed = ' AND e.exit_code = 0' if exclude_failed else ''
        sql = '''
            SELECT t.slave_id as slave,
                   COUNT(t.item_id) AS 'nr. items',
                   AVG(t.time) AS 'average time per task',
                   MIN(t.time) AS 'minimum time for task',
                   MAX(t.time) AS 'maximum time for task',
                   SUM(t.time) AS 'total time'
                FROM (SELECT s.slave_id AS slave_id,
                             s.item_id AS item_id,
                             e.end_time - s.start_time AS time
                          FROM work_items AS s, results AS e
                          WHERE s.item_id = e.item_id{0}) AS t
                GROUP BY t.slave_id
                ORDER BY t.slave_Id;'''.format(no_failed)
        cursor = self._conn.cursor()
        return cursor.execute(sql).fetchall()
