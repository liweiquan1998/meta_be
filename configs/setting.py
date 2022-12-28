import os
import configparser
import copy

environment = os.getenv('APP_ENV', 'local')
config_path = '/etc/sx_config'
config = dict()
print(f'env:{environment}\n{"-"*30}\n')

if environment == 'local':
    config = configparser.ConfigParser()
    config.read_file(open(f'./development.ini'))
    get_copy = copy.deepcopy(config.get)
    config.get = lambda key: get_copy('config', key)

elif environment in ('test', 'production'):
    file_names = os.listdir(config_path)
    config = {key: open('/'.join([config_path, key])).read() for key in file_names
              if not key.startswith('.')}
    for c in config:
        print(c, ':', '*'*(len(c)))
    print('-'*30, '\n')
