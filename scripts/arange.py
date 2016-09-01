#!/usr/bin/env python

from argparse import ArgumentParser
import csv
import re
import sys

from vsc.atools.int_ranges import (int_ranges2set, set2int_ranges,
                                   InvalidRangeSpecError)
from vsc.atools.log_parser import LogParser, InvalidLogEntryError


def compute_data_ids(options):
    nr_work_items = sys.maxsize
    for filename in options.data:
        with open(filename, 'r') as csv_file:
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(csv_file.read(options.sniff))
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


def compute_t_ids(options):
    return int_ranges2set(options.t)


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Compute the array ID range')
    arg_parser.add_argument('--data', nargs='*',
                            help='CSV files to use')
    arg_parser.add_argument('-t', help='array ID range to consider')
    arg_parser.add_argument('--log', nargs='*',
                            help='log file to compute completed items from')
    arg_parser.add_argument('--redo', action='store_true',
                            help='redo failed items')
    arg_parser.add_argument('--sniff', type=int, default=1024,
                            help='number of bytes to sniff for CSV dialect')
    options = arg_parser.parse_args()
    try:
        if options.data and options.t:
            todo = compute_data_ids(options) & ompute_t_ids(options)
        elif options.data:
            todo = compute_data_ids(options)
        elif options.t:
            todo = compute_t_ids(options)
        else:
            msg = '### error: either --data or -t option is required\n'
            sys.stderr.write(msg)
            sys.exit(20)
    except IOError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except InvalidRangeSpecError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    if options.log:
        completed = set()
        failed = set()
        try:
            for filename in options.log:
                log_parser = LogParser()
                events = log_parser.parse(filename)
                for event in events:
                    if event.type == 'completed':
                        todo.discard(event.item_id)
                        completed.add(event.item_id)
                    elif event.type == 'failed':
                        failed.add(event.item_id)
            if not options.redo:
                failed -= completed
                todo -= failed
        except IOError as error:
            msg = '### IOError: {0}'.format(str(error))
            sys.stderr.write(msg)
            sys.exit(error.errno)
        except InvalidLogEntryError as error:
            msg = '### IOError: {0}'.format(str(error))
            sys.stderr.write(msg)
            sys.exit(error.errno)
    print(set2int_ranges(todo))
