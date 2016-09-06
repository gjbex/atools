#!/usr/bin/env python

from argparse import ArgumentParser
import csv
import os
import sys

from vsc.atools.config import get_var_config, ConfigFileError
from vsc.atools.utils import EnvVarError, EndOfFileError


def create_bash_statements(row):
    '''given a CSV row, create bash export statements'''
    def_strs = []
    for variable in row:
        def_strs.append('export {0}="{1}"'.format(variable, row[variable]))
    return os.linesep.join(def_strs)


def create_csh_statements(row):
    '''given a CSV row, create csh export statements'''
    def_strs = []
    for variable in row:
        def_strs.append('setenv {0} "{1}"'.format(variable, row[variable]))
    return os.linesep.join(def_strs)


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='update environment with '
                                            'variables with values taken '
                                            'from a CSV file')
    arg_parser.add_argument('--data', required=True, nargs='+',
                            help='CSV files to use')
    arg_parser.add_argument('--id', type=int,
                            help='line to use from CSV file')
    arg_parser.add_argument('--shell', default='bash',
                            choices=['bash', 'tcsh', 'csh', 'sh'],
                            help='shell to generate defintions for')
    arg_parser.add_argument('--sniff', type=int, default=1024,
                            help='number of bytes to sniff for CSV dialect')
    arg_parser.add_argument('--conf', help='configuration file')
    options = arg_parser.parse_args()
    formatters = {
        'bash': create_bash_statements,
        'sh': create_bash_statements,
        'tcsh': create_csh_statements,
        'csh': create_csh_statements,
    }
    if options.conf:
        conf_filename = options.conf
    else:
        conf_filename = os.path.join(os.path.dirname(__file__),
                                     '..', 'conf', 'atools.conf')
    try:
        var_names = get_var_config(conf_filename)
        if options.id:
            work_item_id = options.id
        else:
            try:
                work_item_id = int(os.environ[var_names['array_idx_var']])
            except KeyError as error:
                raise EnvVarError(error.args[0])
        for filename in options.data:
            with open(filename, 'r') as csv_file:
                dialect = csv.Sniffer().sniff(csv_file.read(options.sniff))
                csv_file.seek(0)
                csv_reader = csv.DictReader(csv_file, fieldnames=None,
                                            restkey='rest', restval=None,
                                            dialect=dialect)
                row_nr = 0
                for row in csv_reader:
                    row_nr += 1
                    if row_nr == work_item_id:
                        print(formatters[options.shell](row))
                        break
                else:
                    raise EndOfFileError(work_item_id, row_nr)
    except IOError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except EndOfFileError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except EnvVarError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except ConfigFileError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
