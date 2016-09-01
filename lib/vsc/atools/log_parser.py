'''Module to parse logs geenrated by alog'''

from datetime import datetime
from operator import attrgetter
import re
import sys


class InvalidLogEventError(Exception):
    '''Exception that signals a problem when creating a new alog event'''

    def __init__(self, event_type):
        self._event_type
        self.errno = 30

    def __str__(self):
        return "event type '{0}' is invalid".format(self._event_type)


class InvalidLogEntryError(Exception):
    '''Exception to signal that a log file entry is invalid'''

    def __init__(self, log_line):
        '''Constructor for the exception on the log entry'''
        self._log_line = log_line
        self.errno = 1

    def __str__(self):
        msg = "log line '{0}' is invalid"
        return msg.format(self._log_line)


class LogEvent(object):
    '''Class representing events in an alog log file'''

    event_types = ['started', 'completed', 'failed']
    date_fmt = '%Y-%m-%d %H:%M:%S'

    def __init__(self, time_stamp, event_type, item_id, slave_id,
                 exit_status):
        '''Constructor with event type, item number, slave ID, time stamp,
        and, if applicable, exit status'''
        if event_type not in LogEvent.event_types:
            raise InvalidLogEventError(event_type)
        self._type = event_type
        self._item_id = item_id
        self._slave_id = slave_id
        self._time_stamp = datetime.strptime(time_stamp,
                                             LogEvent.date_fmt)
        self._exit = exit_status

    @property
    def type(self):
        return self._type

    @property
    def item_id(self):
        return self._item_id

    @property
    def slave_id(self):
        return self._slave_id

    @property
    def time_stamp(self):
        return self._time_stamp

    @property
    def exit_status(self):
        return self._exit

    def __str__(self):
        time_stamp_str = self.time_stamp.strftime(LogEvent.date_fmt)
        event_str = '{0:d} {1} by {2} at {3}'.format(self.item_id,
                                                     self.type,
                                                     self.slave_id,
                                                     time_stamp_str)
        if self.type == 'failed':
            event_str += ': {0:d}'.format(self.exit_status)
        return event_str


class LogParser(object):
    '''Class implementing a parser for alog files'''

    def __init__(self):
        '''alog parser constructor'''
        expr = r'^(\d+) (\w+) by (\w+) at (.+)(?::\s+(\d+))?$'
        self._line_re = re.compile(expr)

    def _parse_line(self, line):
        '''Parse given log line, and retrun a list of events'''
        match = self._line_re.match(line.rstrip())
        if match:
            event_type = match.group(2)
            item_id = int(match.group(1))
            slave_id = match.group(3)
            time_stamp = match.group(4)
            if event_type == 'failed':
                exit_status = int(match.group(5))
            elif event_type == 'completed':
                exit_status = 0
            else:
                exit_status = None
            return LogEvent(time_stamp, event_type, item_id, slave_id,
                            exit_status)
        else:
            raise InvalidLogEntryError(line.rstrip())

    def parse(self, log_file, ignore_invalid=False):
        '''Parse given log file, and retrun a list of events'''
        events = []
        for line in log_file:
            try:
                events.append(self._parse_line(line.rstrip()))
            except InvalidLogEntryError as error:
                if ignore_invalid:
                    msg = '### warning: {0}\n'.format(str(error))
                    sys.stderr.write(msg)
                else:
                    raise error
        return events.sort(key=attrgetter('time_stamp'))

    def parse_file(self, log_filename, ignore_invalid=False):
        '''Parse given log file, and retrun a list of events'''
        with open(log_filename, 'r') as log_file:
            return self.parse(log_file, ignore_invalid)
