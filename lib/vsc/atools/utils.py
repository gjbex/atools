'''Utilities and auxiliry functions and classes for dealing with job
arrays'''

class EndOfFileError(Exception):
    '''Exception to signal that the ID exceeds the number of rows'''

    def __init__(self, data_id, row_nr):
        '''The id exceeds the number of rows in the CSV file'''
        self._id = data_id
        self._row_nr = row_nr
        self.errno = 1

    def __str__(self):
        '''string representation for the exception'''
        return 'CSV file has {0:d} rows, ID is {1}'.format(self._row_nr,
                                                           self._id)


class EnvVarError(Exception):
    '''Exception to signal that an environment variable is not set'''

    def __init__(self, var_name):
        '''Constructor for the exception on the environment variable
        var_name'''
        self._var_name = var_name
        self.errno = 1

    def __str__(self):
        msg = "enviroment variable '{0}' not defined"
        return msg.format(self._var_name)


class InvalidLogEntryError(Exception):
    '''Exception to signal that a log file entry is invalid'''

    def __init__(self, log_line):
        '''Constructor for the exception on the log entry'''
        self._log_line = log_line
        self.errno = 1

    def __str__(self):
        msg = "log line '{0}' is invalid"
        return msg.format(self._log_line)


class InvalidRangeSpecError(Exception):
    '''Exception to signal an invalid array ID range specification'''

    def __init__(self, range_spec):
        '''Constructor for the exception on the range specification'''
        self._range_spec = range_spec
        self.errno = 21

    def __str__(self):
        msg = "range specification '{0}' is invalid"
        return msg.format(self._range_spec)
