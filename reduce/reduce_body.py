#!/usr/bin/env python

from argparse import ArgumentParser
import sys


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='skip header and footer')
    arg_parser.add_argument('--h', type=int, default=0,
                            help='number of header lines to skip')
    arg_parser.add_argument('--f', type=int, default=0,
                            help='number of footer lines to skip')
    options = arg_parser.parse_args()
    for _ in xrange(options.h):
        sys.stdin.readline()
    buffer = []
    for line in sys.stdin:
        buffer.append(line.rstrip('\n\r'))
        if len(buffer) > options.f:
            print(buffer.pop(0))
