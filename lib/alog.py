#!/usr/bin/env python

from argparse import ArgumentParser
import fcntl
import os
import re
import socket
import sys
import time

from vsc.atools.config import get_var_config, ConfigFileError
from vsc.atools.log_parser import LogEvent
from vsc.atools.utils import EnvVarError


def get_log_name(var_names):
    '''Compute the log name from the environment variables defined
    by the batch system'''
    try:
        job_name = os.environ[var_names['job_name_var']]
        job_id = os.environ[var_names['job_id_var']]
    except KeyError as error:
        raise EnvVarError(error.args[0])
    job_name = re.sub(r'-\d+$', '', job_name)
    job_id = re.sub(r'\[\d+\].*$', '', job_id)
    return '{0}.log{1}'.format(job_name, job_id)


def create_start_msg(var_names):
    '''Create a work item start log entry'''
    try:
        work_item_id = os.environ[var_names['array_idx_var']]
    except KeyError as error:
        raise EnvVarError(error.args[0])
    hostname = socket.gethostname()
    time_stamp = time.strftime(LogEvent.date_fmt, time.localtime())
    event = LogEvent(time_stamp, 'started', work_item_id, hostname)
    return str(event)


def create_end_msg(exit_code, var_names):
    '''Create a work item start log entry'''
    try:
        work_item_id = os.environ[var_names['array_idx_var']]
    except KeyError as error:
        raise EnvVarError(error.args[0])
    hostname = socket.gethostname()
    time_stamp = time.strftime(LogEvent.date_fmt, time.localtime())
    if exit_code == 0:
        event_type = 'completed'
    else:
        event_type = 'failed'
    event = LogEvent(time_stamp, event_type, work_item_id, hostname,
                     exit_code)
    return str(event)

if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Work item logger')
    arg_parser.add_argument('--state', choices=['start', 'end'],
                            required=True, help='indicate work item '
                                                'start or end')
    arg_parser.add_argument('--exit', type=int,
                            help='exit code of the work item')
    arg_parser.add_argument('--conf', help='configuration file')
    options = arg_parser.parse_args()
    if options.conf:
        conf_filename = options.conf
    else:
        conf_filename = os.path.join(os.path.dirname(__file__),
                                     '..', 'conf', 'atools.conf')
    try:
        var_names = get_var_config(conf_filename)
        if options.state == 'start':
            msg = create_start_msg(var_names)
        else:
            msg = create_end_msg(options.exit, var_names)
        log_name = get_log_name(var_names)
        with open(log_name, 'a') as log_file:
            fcntl.lockf(log_file, fcntl.LOCK_EX)
            log_file.write(msg + os.linesep)
            log_file.flush()
            fcntl.lockf(log_file, fcntl.LOCK_UN)
    except EnvVarError as error:
        sys.stderr.write('### error: {0}\n'.format(str(error)))
        sys.exit(error.errno)
    except IOError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except ConfigFileError as error:
        msg = '### error: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
