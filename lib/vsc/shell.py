'''Module with some useful shell related functions'''

import os


class UnknownShellError(Exception):
    '''Exception denoting an unknow shell has been specified'''

    def __init__(self, shell):
        super(UnknownShellError, self).__init__()
        self._shell = shell
        self._errno = 2

    def __str__(self):
        return 'unknown shell: {0}'.format(self._shell)


def create_bash_var_def(var, value):
    '''given a name and a value, create bash export statement'''
    return 'export {0}="{1}"'.format(var, value)


def create_csh_var_def(var, value):
    '''given a name and a value, create csh setenv statement'''
    return 'setenv {0} "{1}"'.format(var, value)


formatters = {
    'bash': create_bash_var_def,
    'sh': create_bash_var_def,
    'tcsh': create_csh_var_def,
    'csh': create_csh_var_def,
}


def get_shells():
    return list(formatters.keys())


def create_var_defs(row, shell):
    '''given a dict-like object, row, create shell variable definition
     statements'''
    try:
        formatter = formatters[shell]
    except KeyError:
        raise UnknownShellError(shell)
    def_strs = [formatter(variable, row[variable]) for variable in row]
    return os.linesep.join(def_strs)


def create_var_def(var, value, shell):
    '''given a name and a value, create shell definition statement'''
    try:
        return formatters[shell](var, value)
    except KeyError:
        raise UnknownShellError(shell)
