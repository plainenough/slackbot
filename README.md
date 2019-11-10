# Slackbot - A python slackbot integration
[![BCH compliance](https://bettercodehub.com/edge/badge/plainenough/slackbot?branch=master)](https://bettercodehub.com/)
## Versioning 
major.minor.feature.patch-buildnumber
* Major build numbers are always a breaking change, normally > 50% refactor.
* Minor build numbers indicate a very likely breaking change (This is the custom version number I'm overloading because my code sucks.)
* Feature build numbers are never breaking and will result from adding new commands, or subtle changes like logging.
* Patch build numbers are reserved for trivial changes like bugs or wording inside help docs. 
* Build numbers only represent the amount of times Jenkins as attempted builds on the pipeline. 

## Features:
* Dynamically loads commands
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
  * slackclient
  * pytest
* docker
* app setup with api key in existing slack install

### Testing:
```
pytest -v
```

### Docker:
```
docker build -t slackbot -f container/Dockerfile .
docker run -v /absolute/path/data:/opt/slackbot/data --name=slackbot
```

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

### TODO:
* create commands
* generate some user instruction
