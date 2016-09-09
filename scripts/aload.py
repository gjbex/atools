#!/usr/bin/env python

from argparse import ArgumentParser
import sys

from vsc.atools.log_parser import InvalidLogEntryError
from vsc.atools.work_analysis import LogAnalyzer


def show_item_times(analyzer, csv_format=False):
    field_names = ('task ID', 'slave ID', 'time (s)')
    if csv_format:
        print('{0},{1},{2}'.format(*field_names))
    else:
        print('{0:>8s}{1:>20s}{2:>10s}'.format(*field_names))
    for row in analyzer.item_times(options.no_failed):
        if csv_format:
            print('{0:d},{1},{2:d}'.format(*row))
        else:
            print('{0:8d}{1:>20s}{2:10d}'.format(*row))


def show_slave_times(analyzer, csv_format=False):
    field_names = ('slave ID', 'time (s)', 'count')
    if csv_format:
        print('{0},{1},{2}'.format(*field_names))
    else:
        print('{0:>20s}{1:>10s}{2:>8s}'.format(*field_names))
    for row in analyzer.slave_times(options.no_failed):
        if csv_format:
            print('{0},{1:d},{2:d}'.format(*row))
        else:
            print('{0:>20s}{1:10d}{2:8d}'.format(*row))

def show_item_stats(analyzer):
    results = analyzer.item_stats(options.no_failed)
    fmt_str = (
        '\tnr. tasks:     {0:d}\n'
        '\tavg. time (s): {1:.2f}\n'
        '\tmin. time (s): {2:d}\n'
        '\tmax. time (s): {3:d}\n'
        '\ttot. taime (): {4:d}'
    )
    print('task statistics:')
    print(fmt_str.format(*results))


def show_slave_stats(analyzer):
    results = analyzer.slave_stats(options.no_failed)
    fmt_str = (
        '\tnr. slaves:    {0:d}\n'
        '\tavg. time (s): {1:.2f}\n'
        '\tmin. time (s): {2:d}\n'
        '\tmax. time (s): {3:d}\n'
        '\ttot. taime (): {4:d}'
    )
    print('slave statistics:')
    print(fmt_str.format(*results))

if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Compute the array ID range')
    arg_parser.add_argument('--log', nargs='*',
                            help='log file to compute completed items from')
    arg_parser.add_argument('--no_failed', action='store_true',
                            help='exclude failed tasks from analysis')
    arg_parser.add_argument('--csv', action='store_true',
                            help='CSV output format')
    lists = arg_parser.add_mutually_exclusive_group()
    lists.add_argument('--list_tasks', action='store_true',
                       help='show all task information')
    lists.add_argument('--list_slaves', action='store_true',
                       help='show all slave information')
    arg_parser.add_argument('--db', help='SQLite3 database file name')
    arg_parser.add_argument('--conf', help='configuration file')
    options = arg_parser.parse_args()
    try:
        analyzer = LogAnalyzer(options.db)
        for log_filename in options.log:
            analyzer.parse(log_filename)
        if options.list_tasks:
            show_item_times(analyzer, options.csv)
        elif options.list_slaves:
            show_slave_times(analyzer, options.csv)
        else:
            show_item_stats(analyzer)
            show_slave_stats(analyzer)
    except IOError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except InvalidLogEntryError as error:
        msg = '### error: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
