#!/usr/bin/env python

from argparse import ArgumentParser
import os
import subprocess
import sys

from vsc.atools.int_ranges import int_ranges2set, InvalidRangeSpecError
from vsc.atools.config import (get_var_config, get_mode_config,
                               ConfigFileError)


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Reduce the output of multiple '
                                            'tasks to a single file')
    arg_parser.add_argument('-t', help='array ID range to consider')
    arg_parser.add_argument('--pattern', help='file name pattern')
    arg_parser.add_argument('--mode', choices=['text', 'csv'],
                            help='predefined reduction mode to use')
    script_group = arg_parser.add_argument_group(title='reduction scripts')
    script_group.add_argument('--empty', help='script to create empty '
                                              'output file to use')
    script_group.add_argument('--reduce', help='script to reduce output')
    arg_parser.add_argument('--out', required=True, help='output file name')
    arg_parser.add_argument('--rm_orig', action='store_true',
                            help='remove original output files')
    arg_parser.add_argument('--quiet', action='store_true',
                            help='do not warn on missing output files')
    arg_parser.add_argument('--conf', help='configuration file')
    options = arg_parser.parse_args()
    if options.conf:
        conf_filename = options.conf
    else:
        conf_filename = os.path.join(os.path.dirname(__file__),
                                     '..', 'conf', 'atools.conf')
    if ((not options.empty and options.reduce) or
            (options.empty and not options.reduce)):
        msg = ('### error: either both --empty and --reduce or neither '
               'should be given\n')
        sys.stderr.write(msg)
        sys.exit(1)
    try:
        var_names = get_var_config(conf_filename)
        if options.empty:
            empty_filename, reduce_filename = options.empty, options.reduce
        else:
            mode = options.mode if options.mode else None
            empty_script, reduce_script = get_mode_config(conf_filename,
                                                          mode)
            empty_filename = os.path.join(os.path.dirname(__file__), '..',
                                          'reduce', empty_script)
            reduce_filename = os.path.join(os.path.dirname(__file__), '..',
                                           'reduce', reduce_script)
        array_ids = list(int_ranges2set(options.t))
        if not array_ids:
            sys.stderr.write('empty array ID set\n')
            sys.exit(0)
        array_ids.sort()
        array_id_idx = 0
        while True:
            array_id = array_ids[array_id_idx]
            args = {
                't': array_id,
                var_names['array_idx_var']: array_id,
            }
            filename = options.pattern.format(**args)
            if os.path.exists(filename):
                subprocess.check_call([empty_filename, options.out,
                                       filename])
                break
            elif not options.quiet:
                msg = "### warming: '{0}' does not exist\n".format(filename)
                sys.stderr.write(msg)
            array_id_idx += 1
        for idx in xrange(array_id_idx, len(array_ids)):
            array_id = array_ids[idx]
            args = {
                't': array_id,
                var_names['array_idx_var']: array_id,
            }
            filename = options.pattern.format(**args)
            if os.path.exists(filename):
                subprocess.check_call([reduce_filename, options.out,
                                       filename])
            elif not options.quiet:
                msg = "### warming: '{0}' does not exist\n".format(filename)
                sys.stderr.write(msg)
            if options.rm_orig:
                os.remove(filename)
    except subprocess.CalledProcessError as error:
        msg = '### Subprocess error: {0}\n'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.returncode)
    except IOError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except ConfigFileError as error:
        msg = '### error: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
