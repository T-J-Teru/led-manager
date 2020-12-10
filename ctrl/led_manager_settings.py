import configparser
import os

class led_manager_settings:
    def __init__ (self, filename):
        config = configparser.ConfigParser (interpolation=configparser.ExtendedInterpolation())
        config.read (filename)

        self._port = 8080
        self._default = None
        self._scripts = {}

        if config.has_option ('settings', 'port'):
            self._port = config.getint ('settings', 'port')

        if config.has_option ('settings', 'default'):
            self._default = config.get ('settings', 'default')

        # If the 'scripts' value in the 'DEFAULT' section is a
        # relative path then convert it to an absolute path relative
        # to wherever the config file is located.
        if config.has_option ('DEFAULT', 'scripts'):
            pth = config.get ('DEFAULT', 'scripts')
            if not os.path.isabs (pth):
                pth = os.path.join (os.path.dirname (filename), pth)
                pth = os.path.abspath (pth)
                config.set ('DEFAULT', 'scripts', pth)

        for section in config.sections ():
            if section == 'settings':
                continue
            if not config.has_option (section, 'command'):
                raise RuntimeError ("config section '%s' missing 'command'" % section)
            self._scripts[section] = config.get (section, 'command')

        if self._default != None:
            if not self._default in self._scripts:
                raise RuntimeError ("default '%s' was not found" % self._default)

    def port (self):
        return self._port

    def default (self):
        return self._default

    def scripts (self):
        return self._scripts
