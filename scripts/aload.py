#!/usr/bin/env python

from argparse import ArgumentParser
import sys

from vsc.atools.log_parser import InvalidLogEntryError
from vsc.atools.work_analysis import LogAnalyzer


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Compute the array ID range')
    arg_parser.add_argument('--log', nargs='*',
                            help='log file to compute completed items from')
    arg_parser.add_argument('--no_failed', action='store_true',
                            help='exclude failed tasks from analysis')
    arg_parser.add_argument('--db', help='SQLite3 database file name')
    arg_parser.add_argument('--conf', help='configuration file')
    options = arg_parser.parse_args()
    try:
        analyzer = LogAnalyzer(options.db)
        for log_filename in options.log:
            analyzer.parse(log_filename)
        print('{0:>8s}{1:>20s}{2:>10s}'.format('task ID', 'slave ID',
                                               'time (s)'))
        for row in analyzer.item_times(options.no_failed):
            print('{0:8d}{1:>20s}{2:10d}'.format(*row))

        print('{0:>20s}{1:>10s}{2:>8s}'.format('slave ID', 'time (s)',
                                               'count'))
        for row in analyzer.slave_times(options.no_failed):
            print('{0:>20s}{1:10d}{1:8d}'.format(*row))
    except IOError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except InvalidLogEntryError as error:
        msg = '### error: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
