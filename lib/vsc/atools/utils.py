'''Utilities and auxiliry functions and classes for dealing with job
arrays'''

import os


class ArrayToolsError(Exception):
    '''Base class for all atools exceptions'''

    def __init__(self):
        super().__init__()


class EndOfFileError(ArrayToolsError):
    '''Exception to signal that the ID exceeds the number of rows'''

    def __init__(self, data_id, row_nr):
        '''The id exceeds the number of rows in the CSV file'''
        super().__init__()
        self._id = data_id
        self._row_nr = row_nr
        self.errno = 21

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
        self.errno = 22

    def __str__(self):
        msg = "enviroment variable '{0}' not defined"
        return msg.format(self._var_name)


class SnifferError(ArrayToolsError):
    '''Exception denoting that the CSV sniffer failed to determine
    the CSV dialect'''

    def __init__(self, error):
        self.errno = 23
        self._error = str(error)

    def __str__(self):
        msg = 'sniffer error: {error}'.format(error=self._error)
        msg += '\n  if you have a one-column data file, use the --no_sniffer options'
        msg += '\n  otherwise, try a larger vaue for --sniff'
        return msg


class GroupingNotSupportedError(ArrayToolsError):
    '''Exception to signal that the batch system doesn't support
    grouping tasks into array jobs'''

    def __init__(self, batch_system):
        super().__init__()
        self._batch_system = batch_system
        self.errno = 24

    def __str__(self):
        msg = "task grouping is not supported for batch system '{0}'"
        return msg.format(self._batch_system)


def get_array_id(var_names):
    '''Return the array ID set by the batch system'''
    try:
        return int(os.environ[var_names['array_idx_var']])
    except KeyError as error:
        raise EnvVarError(error.args[0])


def supports_grouping(var_names):
    '''Return True if the batch system supports grouping of tasks,
    i.e., it provides the step of the array ID range'''
    return 'array_step_var' in var_names


def get_group_size(var_names):
    '''Return the number of tasks per array job, i.e., the step of the
    array ID range set by the batch system.  This is 1 if the batch
    system doesn't support grouping, or if it doesn't define the step,
    e.g., when not running as an array job.'''
    if not supports_grouping(var_names):
        return 1
    return int(os.environ.get(var_names['array_step_var'], 1))
