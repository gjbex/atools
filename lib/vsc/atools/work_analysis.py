'''Module containing utilities to analyse the work to be done, and the
work done'''

import csv 
import os
import sqlite3
import sys

from vsc.atools.log_parser import LogParser
from vsc.atools.utils import ArrayToolsError


class MissingSourceError(ArrayToolsError):
    '''Exception denoting that no data sources were specified in a
    function call'''

    def __init__(self, function_name):
        super(MissingSourceError, self).__init__()
        self._function_name = function_name

    def __str__(self):
        msg = "expecting data files and/or array range calling '{0}'"
        return msg.format(self._function_name)


def compute_items_todo(data_files, t_str, log_files, must_redo=False,
                       sniff=1024):
    def compute_data_ids(daata_files, sniff=1024):
        nr_work_items = sys.maxsize
        for filename in data_files:
            with open(filename, 'r') as csv_file:
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(csv_file.read(sniff))
                csv_file.seek(0)
                csv_reader = csv.DictReader(csv_file, fieldnames=None,
                                            restkey='rest',
                                            restval=None,
                                            dialect=dialect)
                row_nr = 0
                for row in csv_reader:
                    row_nr += 1
                if row_nr < nr_work_items:
                    nr_work_items = row_nr
        return set(xrange(1, nr_work_items + 1))
    if data_files and t_str:
        todo = compute_data_ids(data_files, sniff) & int_ranges2set(t_str)
    elif data_files:
        todo = compute_data_ids(data_files, sniff)
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

    def __init__(self, db_name=':memory:'):
        '''Create the database and its tables'''
        self._conn = sqlite3.connect(db_name)
        if not os.path.exists(db_name):
            self.init()

    def init(self):
        cursor = self._conn.cursor()
        sql = '''
            CREATE TABLE work_items (
                item_id   INTEGER    PRIMARY KEY,
                slave_id   TEXT,
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

    def reset(self):
        cursor = self._conn.cursor()
        for table in ['work_items', 'results']:
            cursor.execute('DROP TABLE ?', (table, ))
        self.init()

    def parse(self, filename)
        cursor = self._conn.cursor()
        log_parser = LogParser()
        events = log_parser.parse(filename)
        for event in events:
            if event.type == 'completed' or event.type == 'failed':
                sql = '''
                    INSERT INTO work_tiems (item_id, slave_id, end_time)
                        VALUES (?, ?, ?);'''
                cursor.execute(sql, (event.item_id, event.slave_id,
                                     event.timestamp))
            else:
                sql = '''
                    INSERT INTO results (item_id, exit_code, end_time)
                        VALUES (?, ?, ?);'''
                cursor.execute(sql, (event.item_id, event.exit_code,
                                     event.timestamp))
    def item_times(self, exclude_failed=False):
        '''returns a list of tuples with the item IDs, slave IDx, and the
         run time in seconds'''
        no_failed = ' AND e.exit_code = 0' if exclude_failed else ''
        sql = '''
            SELECT s.item_id, s.slave_id, e.end_time - s.start_time
                FROM work_items AS s, results AS e
                WHERE s.item_id = e.item_id{0}
                ORDER BY s.work_item;'''.format(no_failed)
        cursor = self._conn.cursor()
        return cursor.execute(sql).fetchall()
                                               
    def slave_times(self, exclude_failed=False):
        pass

    def item_stats(self, exclude_failed=False):
        '''returns a tuple containing the number of items computed,
        the minimum, average, and maximum run time'''
        no_failed = ' AND e.exit_code = 0' if exclude_failed else ''
        sql = '''
            SELECT COUNT(*),
                   AVG(e.end_time - s.start_time),
                   MIN(e.end_time - s.start_time),
                   MAX(e.end_time - s.start_time)
                FROM work_items AS s, results AS e
                WHERE s.work_item = e.work_item{0};'''.format(no_failed)
        return cursor.execute(sql).fetchone()

    def salve_stats(self, exclude_failed=False);
        '''returns a tuple containing the number of items computed,
        the minimum, average, and maximum run time'''
        no_failed = ' AND e.exit_code = 0' if exclude_failed else ''
        sql = '''
            SELECT COUNT(t.worker_id) AS 'nr. workers',
                   AVG(t.time) AS 'average time per work item',
                   MIN(t.time) AS 'minimum time for work item',
                   MAX(t.time) AS 'maximum time for work item'
                FROM (SELECT s.worker_id AS worker_id,
                             e.end_time - s.start_time AS time
                          FROM work_items AS s, results AS e
                          WHERE s.work_item = e.work_item{0}
                          GROUP BY s.worker_id) AS t;'''.format(no_failed)
        return cursor.execute(sql).fetchone()
