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
    print('open config from dev')
    config.read_file(open('development.ini'))
elif os.environ.get('APP_ENV') == 'production':
    config.read_file(open('production.ini'))
elif os.environ.get('APP_ENV') == 'idctest':
    config.read_file(open('idctest.ini'))

print(f"get config of {os.environ.get('APP_ENV')}")
print(config.get('DATABASE', 'host'))
