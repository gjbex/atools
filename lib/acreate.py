#!/usr/bin/env python

from argparse import ArgumentParser
import os
import sys

from vsc.shell import get_shells, create_var_def, UnknownShellError
from vsc.atools.config import get_default_shell, ConfigFileError


def parse_job_script(filename):
    with open(filename, 'r') as job_file:
        preamble = ''
        while True:
            line = job_file.readline()
            if line.lstrip().startswith('#'):
                preamble += line
            else:
                break

        payload = line
        for line in job_file:
            payload += line
    return preamble.rstrip(), payload.rstrip()


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='create a job script with '
                                            'support for atools')
    arg_parser.add_argument('--data', nargs='*', help='CSV files to use')
    arg_parser.add_argument('--shell', choices=get_shells(),
                            help='shell to generate defintions for')
    arg_parser.add_argument('--tmpl', help='template file to use')
    arg_parser.add_argument('job_script', help='job script to use')
    arg_parser.add_argument('--conf', help='configuration file')
    options = arg_parser.parse_args()
    if options.conf:
        conf_filename = options.conf
    else:
        conf_filename = os.path.join(os.path.dirname(__file__),
                                     '..', 'conf', 'atools.conf')
    try:
        if options.shell:
            shell = options.shell
        else:
            shell = get_default_shell(conf_filename)
        bin_path = os.path.join(os.path.dirname(__file__), '..', 'bin')
        set_path = create_var_def('PATH',
                                  '{0}:${{PATH}}'.format(bin_path),
                                  shell)
        if options.tmpl:
            tmpl_filename = options.tmpl
        else:
            tmpl_filename = os.path.join(os.path.dirname(__file__),
                                         '..', 'tmpls', 'job_script.tmpl')
        if options.data:
            cmd_fmt = '\nsource <(aenv --shell {shell} --data {data})'
            data_vals = cmd_fmt.format(shell=options.shell,
                                       data=' '.join(options.data))
        else:
            data_vals = ''
        preamble, payload = parse_job_script(options.job_script)
        substitutions = {
            'preamble': preamble,
            'set_path': set_path,
            'data_vals': data_vals,
            'payload': payload,
        }
        with open(tmpl_filename, 'r') as tmpl_file:
            for line in tmpl_file:
                line = line.rstrip()
                print(line.format(**substitutions))
    except IOError as error:
        msg = '### IOError: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except ConfigFileError as error:
        msg = '### error: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
    except UnknownShellError as error:
        msg = '### error: {0}'.format(str(error))
        sys.stderr.write(msg)
        sys.exit(error.errno)
