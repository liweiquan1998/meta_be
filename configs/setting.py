import configparser
import json
import os



config = configparser.ConfigParser()
if os.environ.get('APP_ENV', 'development') == 'development':
    config.readfp(open('development.ini'))
elif os.environ.get('APP_ENV') == 'sxtest':
    config.readfp(open('sxtest.ini'))
elif os.environ.get('APP_ENV') == 'sxprod':
    config.readfp(open('sxprod.ini'))

root_path = config.get('app', 'prefix') if config.get('app', 'enabled') in ['true', 'True', True] else '/'
print(f'root path is {root_path}')

print(f"get config of {os.environ.get('APP_ENV')}")
print(f'db config: {config.get("db", "host")}')