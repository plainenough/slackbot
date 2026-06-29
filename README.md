# Slackbot — Python Slack integration (v2)

[![BCH compliance](https://bettercodehub.com/edge/badge/plainenough/slackbot?branch=master)](https://bettercodehub.com/)

Modernized Slack bot using **Socket Mode** (RTM is deprecated). Same commands, fake internet points, bans, and dynamic plugin loading — with JSON persistence and Python 3.12 support.

## Versioning

`major.feature.patch-buildnumber`

## Features

- Dynamically loads commands from `commands/`
- Fake internet points (`++` / `--`)
- Admin ban / unban system
- Socket Mode (no public URL required)
- JSON persistence with pickle migration
- Centralized admin/ban checks via `AccessControl`
- Test suite with pytest

## Requirements

- Python 3.10+
- Slack app with:
  - **Bot Token** (`xoxb-...`) — scopes: `chat:write`, `app_mentions:read` (and any others your commands need)
  - **App-Level Token** (`xapp-...`) — scope: `connections:write`
  - **Socket Mode** enabled in the Slack app settings
  - Event subscription: `message.channels`, `message.groups`, `message.im`, `message.mpim`

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p data
cp data/config.example.yaml data/config.yaml
# Edit data/config.yaml with your tokens and IDs
python3 main.py
```

Or generate a config template:

```bash
python3 -m utils.create_config
```

### Environment variables (optional)

| Variable | Config key |
|----------|------------|
| `SLACK_BOT_TOKEN` | `BOT_TOKEN` |
| `SLACK_APP_TOKEN` | `APP_TOKEN` |
| `SLACK_BOT_ID` | `BOTID` |
| `SLACK_BOT_USER_ID` | `BOTUSERID` |
| `SLACK_BOT_NAME` | `BOTNAME` |
| `SLACKBOT_CONFIG` | path to config file |

## Testing

```bash
pytest -v
pytest -v --cov=commands --cov=fake_points --cov=message --cov=storage
```

## Docker

```bash
docker build -t slackbot -f container/Dockerfile .
docker run -v /absolute/path/data:/opt/slackbot/data --name=slackbot slackbot
```

Mount a directory containing `config.yaml` with your tokens.

## Systemd (example)

```ini
[Unit]
Description=Slackbot Service
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=5
User=slackbot
WorkingDirectory=/opt/slackbot/
Environment=SLACKBOT_CONFIG=/opt/slackbot/data/config.yaml
ExecStart=/usr/bin/python3 /opt/slackbot/main.py

[Install]
WantedBy=multi-user.target
```

## Commands

Commands live in `commands/*.py` and register via an `alias()` function. The `help` command lists all registered commands and their docstrings.

You will need your bot ID, bot user ID, and admin user IDs in config.

Slash commands (`/command`) are not implemented.

## Migration from v1 (RTM)

1. Enable Socket Mode on your Slack app and create an app-level token
2. Add `APP_TOKEN` to config (or `SLACK_APP_TOKEN` env var)
3. Rename `TOKEN` to `BOT_TOKEN` if desired (both still work)
4. On first run, existing `data/score` and `data/banned` pickle files migrate to JSON automatically

## Notes

Still a small team bot — not a Slack platform framework. Use responsibly.
