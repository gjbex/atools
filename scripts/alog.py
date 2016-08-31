#!/usr/bin/env python

from argparse import ArgumentParser
import os
import posixfile
import re
import socket
import sys
import time

from vsc.atools.utils import EnvVarError


def get_log_name():
    '''Compute the log name from the environment variables defined
    by PBS'''
    try:
        job_name = os.environ['PBS_JOBNAME']
        job_id = os.environ['PBS_JOBID']
    except KeyError as error:
        raise EnvVarError(error.args[0])
    job_name = re.sub(r'-\d+$', '', job_name)
    job_id = re.sub(r'\[\d+\].*$', '', job_id)
    return '{0}.log{1}'.format(job_name, job_id)


def create_start_msg():
    '''Create a work item start log entry'''
    try:
        work_item_id = os.environ['PBS_ARRAYID']
    except KeyError as error:
        raise EnvVarError(error.args[0])
    hostname = socket.gethostname()
    return '{0} started by {1} at {2}'.format(work_item_id, hostname,
                                              time.asctime())


def create_end_msg(exit_code):
    '''Create a work item start log entry'''
    try:
        work_item_id = os.environ['PBS_ARRAYID']
    except KeyError as error:
        raise EnvVarError(error.args[0])
    hostname = socket.gethostname()
    if exit_code == 0:
        return '{0} completed by {1} at {2}'.format(work_item_id,
                                                    hostname,
                                                    time.asctime())
    else:
        return '{0} failed by {1} at {2}: {3:d}'.format(work_item_id,
                                                        hostname,
                                                        time.asctime(),
                                                        exit_code)

if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Work item logger')
    arg_parser.add_argument('--state', choices=['start', 'end'],
                            required=True, help='indicate work item '
                                                'start or end')
    arg_parser.add_argument('--exit', type=int,
                            help='exit code of the work item')
    options = arg_parser.parse_args()
    try:
        if options.state == 'start':
            msg = create_start_msg()
        else:
            msg = create_end_msg(options.exit)
        log_name = get_log_name()
        log_file = posixfile.open(log_name, 'a')
        log_file.lock('w|')
        log_file.write(msg + os.linesep)
        log_file.lock('u')
        log_file.close()
    except EnvVarError as error:
        sys.stderr.write('### error: {0}\n'.format(str(error)))
        sys.exit(error.errno)
