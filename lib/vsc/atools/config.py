'''Module containing utilities to deal with configuration files'''

import sys
from configparser import ConfigParser, Error

from vsc.atools.utils import ArrayToolsError


class ConfigFileError(ArrayToolsError):
    '''Exception to signify a problem iwth the configuration file'''

    def __init__(self, message):
        super().__init__()
        self._message = message
        self.errno = 51

    def __str__(self):
        return 'config file error: {0}'.format(self._message)


def get_default_shell(config_filename):
    '''returns the default shell specified in the configuration file'''
    config_parser = ConfigParser()
    try:
        config_parser.read(config_filename)
        return config_parser['global'].get('shell', None)
    except Error as error:
        raise ConfigFileError(str(error))


def get_var_config(config_filename):
    '''returns a dictionary with the relevant shell variable names for
    for the selected batch system'''
    config_parser = ConfigParser()
    try:
        config_parser.read(config_filename)
        batch_system = config_parser['global'].get('batch_system', None)
        return dict(config_parser.items(batch_system))
    except Error as error:
        raise ConfigFileError(str(error))


def get_mode_config(config_filename, mode=None):
    '''Retrieve the empty and reduce script for the given mode, or for
    the default if none is given'''
    config_parser = ConfigParser()
    try:
        config_parser.read(config_filename)
        if not mode:
            mode = config_parser['global'].get('mode')
        empty_script = config_parser[mode].get('empty')
        reduce_script = config_parser[mode].get('reduce')
        return empty_script, reduce_script
    except KeyError as error:
        raise ConfigFileError(str(error))
