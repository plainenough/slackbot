"""Create config if one doesn't exist."""


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
    """Write template to disk."""
    with open('data/config.yaml', 'w') as config_file:
        for line in TEMPLATE:
            config_file.write(line)


def main():
    """Open or create config.yaml."""
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
    except Exception as e:
        print("Unknown error: check permissions - {0}".format(e))
    return


if __name__ == '__main__':
    main()
