'''Utilities and auxiliry functions and classes for dealing with job
arrays'''

import os
import re


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


# environment variables that change which code runs, either in the shell
# that runs the command or in the programs it starts, so they can't be
# defined from data files
PROTECTED_VARS = {'BASH_ENV', 'ENV', 'SHELLOPTS', 'BASHOPTS', 'PS4',
                  'PATH', 'LD_PRELOAD', 'LD_LIBRARY_PATH'}
PROTECTED_VAR_PREFIX = 'BASH_FUNC_'

VAR_NAME_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


class ProtectedVariableError(ArrayToolsError):
    '''Exception to signal that a data file defines a variable that
    would change which code runs'''

    def __init__(self, var_name):
        super().__init__()
        self._var_name = var_name
        self.errno = 25

    def __str__(self):
        msg = ("data file defines '{0}', which can't be used as a "
               "variable name, since it changes which code runs")
        return msg.format(self._var_name)


class InvalidVariableNameError(ArrayToolsError):
    '''Exception to signal that a data file has column names that are
    not valid shell variable names'''

    def __init__(self, var_names):
        super().__init__()
        self._var_names = var_names
        self.errno = 26

    def __str__(self):
        msg = ('data file has column names that are not valid variable '
               'names: {0}; names can only contain letters, digits and '
               'underscores, and can not start with a digit')
        return msg.format(', '.join("'{0}'".format(name)
                                    for name in self._var_names))


def check_var_names(var_names):
    '''Check the variable names defined from a data file.  Raise an
    exception if a name would change which code runs, and return the
    sorted list of names that are not valid shell variable names, so that
    the caller can decide how to handle those.'''
    for var_name in sorted(var_names):
        if (var_name in PROTECTED_VARS or
                var_name.startswith(PROTECTED_VAR_PREFIX)):
            raise ProtectedVariableError(var_name)
    return sorted(var_name for var_name in var_names
                  if not VAR_NAME_RE.match(var_name))


class ReservedVariableError(ArrayToolsError):
    '''Exception to signal that a data file defines a variable that is
    set by atools itself'''

    def __init__(self, var_name):
        super().__init__()
        self._var_name = var_name
        self.errno = 27

    def __str__(self):
        msg = ("data file defines '{0}', which can't be used as a "
               "variable name, since it is set by atools")
        return msg.format(self._var_name)
