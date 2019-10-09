# Slackbot - A python slackbot integration
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
** pyyaml
** slackclient
** pytest
* docker
* app setup with api key in existing slack install

### Testing:
```
pytest -v
```

### Docker:
```
docker build -t slackbot -f container/Dockerfile .
docker run -v source=myvol1,target=/opt/slackbot/data --name=slackbot
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
