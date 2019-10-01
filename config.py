#!/usr/bin/env python3
def obtain_config(logging):
    import yaml
    import sys
    try:
        with open('data/config.yaml', 'r') as myconfig:
            config = yaml.load(myconfig.read())
    except FileNotFoundError:
        from utils.create_config import TEMPLATE, create_config
        logging.info('Creating fresh config - Update values.')
        create_config()
        sys.exit(1)
    except yaml.scanner.ScannerError as e:
        logging.info('Config has invalid format.')
        logging.debug(e)
        sys.exit(1)
    return config