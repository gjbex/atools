#!/usr/bin/env python

from argparse import ArgumentParser


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='create a job script with '
                                            'support for atools')
    options = arg_parser.parse_args()
