'''Module with utilities to deal with integer ranges such as 2,5-9'''

import re

from vsc.atools.utils import ArrayToolsError


class InvalidRangeSpecError(ArrayToolsError):
    '''Exception to signal an invalid array ID range specification'''

    def __init__(self, range_spec):
        '''Constructor for the exception on the range specification'''
        super(InvalidRangeSpecError, self).__init__()
        self._range_spec = range_spec
        self.errno = 41

    def __str__(self):
        msg = "range specification '{0}' is invalid"
        return msg.format(self._range_spec)


def int_ranges2set(ranges):
    '''compute the set of array iDs encoded by a range string'''
    ids = set()
    part_ranges = ranges.split(',')
    for part_range in part_ranges:
        if part_range.isdigit():
            ids.add(int(part_range))
            continue
        if match := re.search(r'^(\d+)-(\d+)$', part_range):
            lower = int(match[1])
            upper = int(match[2])
            if lower <= upper:
                for i in range(lower, upper + 1):
                    ids.add(i)
                continue
        raise InvalidRangeSpecError(part_range)
    return ids


def set2int_ranges(todo):
    '''Compute the ranges of arrays IDs that are still to do'''
    ranges = []
    if todo_list := sorted(todo):
        range_min = todo_list.pop(0)
        previous = range_min
        while todo_list:
            item = todo_list.pop(0)
            if previous + 1 != item:
                if range_min != previous:
                    ranges.append('{0:d}-{1:d}'.format(range_min, previous))
                else:
                    ranges.append('{0:d}'.format(range_min))
                range_min = item
            previous = item
        if range_min != previous:
            ranges.append('{0:d}-{1:d}'.format(range_min, previous))
        else:
            ranges.append('{0:d}'.format(range_min))
    return ','.join(ranges)
