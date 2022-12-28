import os
import configparser
import copy

environment = os.getenv('APP_ENV', 'local')
config_path = '/etc/sx_config'
print(f'env:{environment}')

if environment == 'local':
    config = configparser.ConfigParser()
    config.read_file(open(f'../development.ini'))
    get_copy = copy.deepcopy(config.get)
    config.get = lambda key: get_copy('config', key)

elif environment in ('test', 'production'):
    file_names = os.listdir(config_path)
    config = {key: open(config_path + '/' + key).read() for key in file_names}
    print(config)
