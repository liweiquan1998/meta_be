import os
import configparser
import copy

environment = 'k8s'
config_path = '/etc/sx_config'
try:
    os.listdir(config_path)
except FileNotFoundError:
    environment = 'local'
config = dict()
print(f'env:{environment}\n{"-"*30}\n')

if environment == 'local':
    config = configparser.ConfigParser()
    config.read_file(open(f'./development.ini'))
    get_copy = copy.deepcopy(config.get)
    config.get = lambda key: get_copy('config', key)

elif environment == 'k8s':
    file_names = os.listdir(config_path)
    config = {key: open('/'.join([config_path, key])).read() for key in file_names
              if not key.startswith('.')}
    for c in config:
        print(c, ':', '*'*(len(c)))
    print('-'*30, '\n')
