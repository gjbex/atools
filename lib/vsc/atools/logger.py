'''Module to write task start and end events to the job's log file'''

import fcntl
import os
import re
import socket
import time

from vsc.atools.log_parser import LogEvent
from vsc.atools.utils import EnvVarError


def get_log_name(var_names):
    '''Compute the log name from the environment variables defined
    by the batch system'''
    try:
        job_name = os.environ[var_names['job_name_var']]
        job_id = os.environ[var_names['job_id_var']]
        submission_dir = os.environ[var_names['submission_dir']]
    except KeyError as error:
        raise EnvVarError(error.args[0])
    job_name = re.sub(r'-\d+$', '', job_name)
    job_id = re.sub(r'\[\d+\].*$', '', job_id)
    return '{0}/{1}.log{2}'.format(submission_dir, job_name, job_id)


def _get_work_item_id(var_names, work_item_id):
    '''Return the given work item ID, or the array ID set by the
    batch system if none is given'''
    if work_item_id is not None:
        return work_item_id
    try:
        return os.environ[var_names['array_idx_var']]
    except KeyError as error:
        raise EnvVarError(error.args[0])


def create_start_msg(var_names, work_item_id=None):
    '''Create a work item start log entry'''
    work_item_id = _get_work_item_id(var_names, work_item_id)
    hostname = socket.gethostname()
    time_stamp = time.strftime(LogEvent.date_fmt, time.localtime())
    event = LogEvent(time_stamp, 'started', work_item_id, hostname)
    return str(event)


def create_end_msg(exit_code, var_names, work_item_id=None):
    '''Create a work item end log entry'''
    work_item_id = _get_work_item_id(var_names, work_item_id)
    hostname = socket.gethostname()
    time_stamp = time.strftime(LogEvent.date_fmt, time.localtime())
    if exit_code == 0:
        event_type = 'completed'
    else:
        event_type = 'failed'
    event = LogEvent(time_stamp, event_type, work_item_id, hostname,
                     exit_code)
    return str(event)


def write_log_msg(log_name, msg):
    '''Append a message to the log file, using a lock since tasks
    write to the same file concurrently'''
    with open(log_name, 'a') as log_file:
        fcntl.lockf(log_file, fcntl.LOCK_EX)
        log_file.write(msg + os.linesep)
        log_file.flush()
        fcntl.lockf(log_file, fcntl.LOCK_UN)
