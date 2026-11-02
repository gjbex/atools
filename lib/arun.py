#!/usr/bin/env python

from argparse import ArgumentParser, REMAINDER
import os
import subprocess
import sys

from vsc.atools.config import get_var_config, ConfigFileError
from vsc.atools.int_ranges import InvalidRangeSpecError
from vsc.atools.log_parser import InvalidLogEntryError
from vsc.atools.logger import (get_log_name, create_start_msg,
                               create_end_msg, write_log_msg)
from vsc.atools.work_analysis import (compute_items_todo, group_task_ids,
                                      read_data_rows, MissingSourceError)
from vsc.atools.utils import (EnvVarError, SnifferError,
                              InvalidVariableNameError,
                              ProtectedVariableError, check_var_names,
                              get_array_id, get_group_size)


TASK_ID_VAR = 'ATOOLS_TASK_ID'


def create_task_env(task_id, row):
    '''Create the environment for a task, i.e., the current environment
    extended with the task's variables from the CSV files'''
    env = dict(os.environ)
    for name, value in row.items():
        env[name] = '' if value is None else str(value)
    env[TASK_ID_VAR] = str(task_id)
    return env


def run_task(command, env):
    '''Run the command with bash in the given environment, and return
    its exit code'''
    sys.stdout.flush()
    sys.stderr.flush()
    exit_code = subprocess.call(['bash', '-c', command], env=env)
    if exit_code < 0:
        # killed by a signal, use the shell convention
        exit_code = 128 - exit_code
    return exit_code


if __name__ == '__main__':
    arg_parser = ArgumentParser(
        description='run a command for each task of the current array '
                    'job, with variables defined from a CSV file, and log '
                    'task start and end; when tasks are grouped, the '
                    'group size is taken from the array job',
        epilog="example: arun --data data.csv -- "
               "'Rscript bootstrap.R $alpha $beta'"
    )
    arg_parser.add_argument('--data', nargs='+',
                            help='CSV files to use')
    arg_parser.add_argument('-t', help='task ID range to consider')
    arg_parser.add_argument('--log', nargs='+',
                            help='log files of previous runs, tasks that '
                                 'completed are skipped')
    arg_parser.add_argument('--redo', action='store_true',
                            help='also redo tasks that failed in previous '
                                 'runs')
    arg_parser.add_argument('--no_logging', action='store_true',
                            help='do not log task start and end')
    arg_parser.add_argument('--sniff', type=int, default=1024,
                            help='number of bytes to sniff for CSV dialect')
    arg_parser.add_argument('--no_sniffer', action='store_true',
                            help='do not use the sniffer for CSV dialect')
    arg_parser.add_argument('--conf', help='configuration file')
    arg_parser.add_argument('command', nargs=REMAINDER,
                            help='command to run for each task, executed '
                                 'by bash')
    options = arg_parser.parse_args()
    command = options.command
    if command and command[0] == '--':
        command = command[1:]
    if not command:
        sys.stderr.write('### error: no command to run given\n')
        sys.exit(1)
    command = ' '.join(command)
    if options.conf:
        conf_filename = options.conf
    else:
        conf_filename = os.path.join(os.path.dirname(__file__),
                                     '..', 'conf', 'atools.conf')
    try:
        var_names = get_var_config(conf_filename)
        todo, _, _ = compute_items_todo(
            options.data, options.t, options.log, must_redo=options.redo,
            sniff=options.sniff, no_sniffer=options.no_sniffer
        )
        task_ids = sorted(todo & group_task_ids(get_array_id(var_names),
                                                get_group_size(var_names)))
        if options.data:
            rows = read_data_rows(options.data, task_ids,
                                  sniff=options.sniff,
                                  no_sniffer=options.no_sniffer)
            invalid_names = check_var_names({name for row in rows.values()
                                             for name in row})
            if invalid_names:
                raise InvalidVariableNameError(invalid_names)
        else:
            rows = {task_id: {} for task_id in task_ids}
        log_name = None if options.no_logging else get_log_name(var_names)
        nr_failed = 0
        for task_id in task_ids:
            if log_name:
                write_log_msg(log_name, create_start_msg(var_names, task_id))
            exit_code = run_task(command, create_task_env(task_id,
                                                          rows[task_id]))
            if exit_code != 0:
                nr_failed += 1
            if log_name:
                write_log_msg(log_name, create_end_msg(exit_code, var_names,
                                                       task_id))
        if nr_failed:
            msg = '### error: {0:d} of {1:d} tasks failed\n'
            sys.stderr.write(msg.format(nr_failed, len(task_ids)))
            sys.exit(1)
    except IOError as error:
        msg = '### IOError: {0}\n'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except (InvalidRangeSpecError, MissingSourceError, InvalidLogEntryError,
            SnifferError, EnvVarError, ConfigFileError,
            ProtectedVariableError, InvalidVariableNameError) as error:
        msg = '### error: {0}\n'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
