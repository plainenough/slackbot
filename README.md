# Slackbot - A python slackbot integration
[![BCH compliance](https://bettercodehub.com/edge/badge/plainenough/slackbot?branch=master)](https://bettercodehub.com/)
## Versioning 
major.feature.patch-buildnumber
* Major build numbers are always a breaking change, normally > 50% refactor.
* Feature build numbers are never breaking and will result from adding new commands, or subtle changes like logging.
* Patch build numbers are reserved for trivial changes like bugs or wording inside help docs. 
* Build numbers only represent the amount of times Jenkins has attempted builds on the pipeline. 

## Features:
* Dynamically loads commands
* Dynamically saves userdata
* Fake internet points system
* Banning system
* Testing suite

## Deployment instructions:
Note: Use utils.create_config to generate a config template. This will
also be done on initial launch.

### Requirements:
* python 3.6 or higher
* pip packages
  * pyyaml
  * slack_sdk
  * pytest
* docker
* app setup with api key in existing slack install

### Testing:
```
# Root directory of the repo.
export PYTHONPATH=$PWD
# To execute tests
pytest -v
# To see useful coverage map
pytest -v --cov=commands --cov=fake_points --cov=message
```

### Docker:
```
docker build -t slackbot -f container/Dockerfile .
docker run -v /absolute/path/data:/opt/slackbot/data --name=slackbot
```

This application exepects a config file in the mounted directory.


### Daemonized:
* Target OS: Ubuntu 18 (Bionic)
* Systemd Service File:
```
[Unit]
Description= Slackbot-Service
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=slackbot
WorkingDirectory=/opt/slackbot/
ExecStart=/usr/bin/python3 /opt/slackbot/main.py

[Install]
WantedBy=multi-user.target
```

### Instructions
Commands are loaded on import and should contain the docstring from each
command. Simply using the "help" command will trigger the bot to supply 
the command and the docstring associated.

You will need your bot ID and your general channel id. 

/commands are not implemented.

### TODO:
* generate better user instructions
* convert config to secondary option and retrieve config from environment variables
* auto discover as much about the application as possible to reduce config
* add assertions to testing
