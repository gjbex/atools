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
        match = re.search(r'^(\d+)-(\d+)$', part_range)
        if match:
            lower = int(match.group(1))
            upper = int(match.group(2))
            if lower <= upper:
                for i in range(lower, upper + 1):
                    ids.add(i)
                continue
        raise InvalidRangeSpecError(part_range)
    return ids


def set2int_ranges(todo):
    '''Compute the ranges of arrays IDs that are still to do'''
    todo_list = sorted(todo)
    ranges = []
    if todo_list:
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


def set2stepped_int_ranges(ids, step):
    '''Compute ranges with the given step for a set of IDs, e.g.,
    {1, 6, 11, 56} with step 5 is 1-11:5,56-56:5.  Each range has an
    explicit step, also when it contains a single ID, since Slurm uses
    the step of the array ID range to set the group size.'''
    if step == 1:
        return set2int_ranges(ids)
    ranges = []
    for item in sorted(ids):
        if ranges and item == ranges[-1][1] + step:
            ranges[-1][1] = item
        else:
            ranges.append([item, item])
    return ','.join('{0:d}-{1:d}:{2:d}'.format(lower, upper, step)
                    for lower, upper in ranges)
