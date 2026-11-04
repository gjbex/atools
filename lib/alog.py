#!/usr/bin/env python

from argparse import ArgumentParser
import os
import sys

from vsc.atools.config import get_var_config, ConfigFileError
from vsc.atools.logger import (get_log_name, create_start_msg,
                               create_end_msg, write_log_msg)
from vsc.atools.utils import EnvVarError


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Work item logger')
    arg_parser.add_argument('--state', choices=['start', 'end'],
                            required=True, help='indicate work item '
                                                'start or end')
    arg_parser.add_argument('--exit', type=int,
                            help='exit code of the work item')
    arg_parser.add_argument('--id', type=int,
                            help='work item ID to log, defaults to the '
                                 'array ID set by the batch system')
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
            msg = create_start_msg(var_names, options.id)
        else:
            msg = create_end_msg(options.exit, var_names, options.id)
        write_log_msg(get_log_name(var_names), msg)
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
