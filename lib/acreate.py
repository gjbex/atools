#!/usr/bin/env python

from argparse import ArgumentParser
import os


def parse_job_script(filename):
    with open(filename, 'r') as job_file:
        preamble = ''
        while (True):
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
    arg_parser.add_argument('--set_path', help='call to modify PATH to '
                                               'include atools/bin')
    arg_parser.add_argument('--data', nargs='*', help='CSV files to use')
    arg_parser.add_argument('--shell', default='bash',
                            choices=['bash', 'tcsh', 'csh', 'sh'],
                            help='shell to generate defintions for')
    arg_parser.add_argument('--tmpl', help='template file to use')
    arg_parser.add_argument('job_script', help='job script to use')
    arg_parser.add_argument('--conf', help='configuration file')
    options = arg_parser.parse_args()
    set_path = options.set_path
    if options.tmpl:
        tmpl_filename = options.tmpl
    else:
        tmpl_filename = os.path.join(os.path.dirname(__file__),
                                     '..', 'tmpls', 'job_script.tmpl')
    if options.conf:
        conf_filename = options.conf
    else:
        conf_filename = os.path.join(os.path.dirname(__file__),
                                     '..', 'conf', 'atools.conf')
    if options.data:
        cmd_fmt = 'source <(aenv --shell {shell} --data {data})'
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
