'''Module containing utilities to deal with configuration files'''

import ConfigParser

from vsc.atools.utils import ArrayToolsError


class ConfigFileError(ArrayToolsError):
    '''Exception to signify a problem iwth the configuration file'''

    def __init__(self, message):
        super(ConfigFileError, self).__init__()
        self._message = message
        self.errno = 51

    def __str__(self):
        return 'config file error: {0}'.format(self._message)


def get_var_config(config_file_name):
    '''returns a dictionary with the relevant shell variable names for
    for the selected batch system'''
    config_parser = ConfigParser.SafeConfigParser()
    try:
        config_parser.read(config_file_name)
        batch_system = config_parser.get('global', 'batch_system', None)
        var_names = dict()
        for key, value in config_parser.items(batch_system):
            var_names[key] = value
        return var_names
    except ConfigParser.Error as error:
        raise ConfigFileError(str(error))
