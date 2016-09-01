#!/usr/bin/env python

from argparse import ArgumentParser
import sys

from vsc.atools.int_ranges import (int_ranges2set, set2int_ranges,
                                   InvalidRangeSpecError)
from vsc.atools.log_parser import LogParser, InvalidLogEntryError
from vsc.atools.work_analysis import (compute_items_todo,
                                      MissingSourceError)


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
        todo, _, _ = compute_items_todo(options.data, options.t,
                                        options.log, must_redo=options.redo,
                                        sniff=options.sniff)
        print(set2int_ranges(todo))
    except IOError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except InvalidRangeSpecError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except MissingSourceError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except InvalidLogEntryError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
