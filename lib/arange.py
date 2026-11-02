#!/usr/bin/env python

from argparse import ArgumentParser
import os
import sys

from vsc.atools.config import (get_batch_system, get_var_config,
                               ConfigFileError)
from vsc.atools.int_ranges import (int_ranges2set, set2int_ranges,
                                   set2stepped_int_ranges,
                                   InvalidRangeSpecError)
from vsc.atools.log_parser import LogParser, InvalidLogEntryError
from vsc.atools.work_analysis import (compute_items_todo,
                                      group_start_ids, group_task_ids,
                                      MissingSourceError)
from vsc.atools.utils import (EnvVarError, SnifferError,
                              GroupingNotSupportedError, get_array_id,
                              get_group_size, supports_grouping)


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Compute the array ID range')
    arg_parser.add_argument('--data', nargs='*',
                            help='CSV files to use')
    arg_parser.add_argument('-t', help='array ID range to consider '
                                       '(task ID range when using '
                                       '--group_size or --list_tasks)')
    arg_parser.add_argument('--log', nargs='*',
                            help='log file to compute completed items from')
    arg_parser.add_argument('--redo', action='store_true',
                            help='redo failed items')
    arg_parser.add_argument('--group_size', type=int,
                            help='number of consecutive tasks to run in '
                                 'a single array job (Slurm only)')
    arg_parser.add_argument('--list_tasks', action='store_true',
                            help='list the task IDs to run in the current '
                                 'array job, for use in a job script')
    arg_parser.add_argument('--summary', action='store_true',
                            help='print a summary of a job that is '
                                 'running or completed')
    arg_parser.add_argument('--list_failed', action='store_true',
                            help='list failed jobs when summarizing')
    arg_parser.add_argument('--list_completed', action='store_true',
                            help='list completed jobs when summarizing')
    arg_parser.add_argument('--sniff', type=int, default=1024,
                            help='number of bytes to sniff for CSV dialect')
    arg_parser.add_argument('--no_sniffer', action='store_true',
                            help='do not use the sniffer for CSV dialect')
    arg_parser.add_argument('--conf', help='configuration file')
    options = arg_parser.parse_args()
    if options.summary and not options.log:
        msg = '### error: summary information requires log files\n'
        sys.stderr.write(msg)
        sys.exit(1)
    if options.group_size is not None and options.group_size < 1:
        msg = '### error: --group_size must be at least 1\n'
        sys.stderr.write(msg)
        sys.exit(1)
    if options.list_tasks and options.group_size:
        msg = ('### error: --list_tasks takes the group size from the '
               'array job, do not use --group_size\n')
        sys.stderr.write(msg)
        sys.exit(1)
    if options.conf:
        conf_filename = options.conf
    else:
        conf_filename = os.path.join(os.path.dirname(__file__),
                                     '..', 'conf', 'atools.conf')
    try:
        var_names = get_var_config(conf_filename)
        if options.group_size and not supports_grouping(var_names):
            raise GroupingNotSupportedError(get_batch_system(conf_filename))
        todo, completed, failed = compute_items_todo(
            options.data, options.t, options.log, must_redo=options.redo,
            sniff=options.sniff, no_sniffer=options.no_sniffer
        )
        if options.list_tasks:
            tasks = todo & group_task_ids(get_array_id(var_names),
                                          get_group_size(var_names))
            print(' '.join(str(task_id) for task_id in sorted(tasks)))
        elif options.summary:
            print('Summary:')
            print('  items completed: {0:d}'.format(len(completed)))
            print('  items failed: {0:d}'.format(len(failed)))
            print('  items to do: {0:d}'.format(len(todo)))
            if options.list_failed:
                print('failed: {0}'.format(set2int_ranges(failed)))
            if options.list_completed:
                print('completed: {0}'.format(set2int_ranges(completed)))
        else:
            if options.list_completed:
                print(set2int_ranges(completed))
            elif options.group_size:
                array_ids = group_start_ids(todo, options.group_size)
                print(set2stepped_int_ranges(array_ids, options.group_size))
            else:
                print(set2int_ranges(todo))
    except IOError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except InvalidRangeSpecError as error:
        msg = '### error: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except MissingSourceError as error:
        msg = '### error: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except InvalidLogEntryError as error:
        msg = '### error: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except SnifferError as error:
        msg = '### error: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except (EnvVarError, GroupingNotSupportedError) as error:
        msg = '### error: {0}\n'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except ConfigFileError as error:
        msg = '### error: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
