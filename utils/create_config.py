#!/usr/bin/python3
import yaml

TEMPLATE = '''\
'TOKEN': False
'BOTID': 'someid'
'BOTUSERID': 'someid'
'BOTNAME': 'slackbot'
'ADMINS':
  - 'UEMN5QPLM'
'''


def create_config():
    with open('data/config.yaml', 'w') as config_file:
        for line in TEMPLATE:
            config_file.write(line)

if __name__ == '__main__':
    try: 
        with open('data/config.yaml', 'r') as config:
            yaml.load(config.read())
            print("Config is valid yaml")
    except FileNotFoundError:
        print("Config doesn't exist: Creating config")
        create_config()
    except yaml.scanner.ScannerError as e: 
        print(e)
        print("Config invalid check your config")
    except: 
        print("Unknown error: check permissions")
