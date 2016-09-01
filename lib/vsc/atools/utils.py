'''Utilities and auxiliry functions and classes for dealing with job
arrays'''

class ArrayToolsError(Exception):
    '''Base class for all atools exceptions'''

    def __init__(self):
        super(ArrayToolsError, self).__init__()


class EndOfFileError(ArrayToolsError):
    '''Exception to signal that the ID exceeds the number of rows'''

    def __init__(self, data_id, row_nr):
        '''The id exceeds the number of rows in the CSV file'''
        super(EndOfFileError, self).__init__()
        self._id = data_id
        self._row_nr = row_nr
        self.errno = 1

    def __str__(self):
        '''string representation for the exception'''
        return 'CSV file has {0:d} rows, ID is {1}'.format(self._row_nr,
                                                           self._id)


class EnvVarError(ArrayToolsError):
    '''Exception to signal that an environment variable is not set'''

    def __init__(self, var_name):
        '''Constructor for the exception on the environment variable
        var_name'''
        super(EnvVarError, self).__init__()
        self._var_name = var_name
        self.errno = 1

    def __str__(self):
        msg = "enviroment variable '{0}' not defined"
        return msg.format(self._var_name)


class InvalidRangeSpecError(ArrayToolsError):
    '''Exception to signal an invalid array ID range specification'''

    def __init__(self, range_spec):
        '''Constructor for the exception on the range specification'''
        super(InvalidRangeSpecError, self).__init__()
        self._range_spec = range_spec
        self.errno = 21

    def __str__(self):
        msg = "range specification '{0}' is invalid"
        return msg.format(self._range_spec)
