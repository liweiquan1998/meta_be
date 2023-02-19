import configparser
import json
import os

class DefaultOption(dict):
    def __init__(self, config, section, **kv):
        self._config = config
        self._section = section
        dict.__init__(self, **kv)
    def items(self):
        _items = []
        for option in self:
            if not self._config.has_option(self._section, option):
                _items.append((option, self[option]))
            else:
                value_in_config = self._config.get(self._section, option)
                _items.append((option, value_in_config))
        return _items

config = configparser.ConfigParser()
if os.environ.get('APP_ENV', 'development') == 'development':
    config.readfp(open('development.ini'))
elif os.environ.get('APP_ENV') == 'sxtest':
    config.readfp(open('sxtest.ini'))
elif os.environ.get('APP_ENV') == 'sxprod':
    config.readfp(open('sxprod.ini'))

print(f"get config of {os.environ.get('APP_ENV')}")
print(f'db config: {config.get("db", "host")}')