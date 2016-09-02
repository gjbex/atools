'''Module containing utilities to analyse the work to be done, and the
work done'''

import csv 
import sys

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
