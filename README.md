# Slackbot — Python Slack integration (v2)

[![BCH compliance](https://bettercodehub.com/edge/badge/plainenough/slackbot?branch=master)](https://bettercodehub.com/)

Modernized Slack bot using **Socket Mode** (RTM is deprecated). Same personality — fake internet points, bans, dice, help — with a cleaner architecture, slash commands, audit logging, and Python 3.12 support.

## Versioning

`major.feature.patch-buildnumber`

## Features

- **Socket Mode** — no public URL required
- **Text commands** — `roll d20`, `ban <@user>`, `++` / `--`, etc.
- **Slash commands** — `/roll`, `/ban`, `/mypoints`, `/scoreboard`, `/help`, `/wtf`, …
- **Fake internet points** with leaderboard medals and score deltas
- **Admin ban/unban** with centralized `AccessControl`
- **Audit log** — `data/audit.jsonl` for admin actions
- **JSON persistence** with automatic pickle migration
- **Dynamic command plugins** in `commands/`
- **53 tests** + mypy on core modules

## Architecture

| Module | Role |
|--------|------|
| `message_parser.py` | Parse Slack events and slash payloads |
| `dispatcher.py` | Route parsed input to command handlers |
| `context.py` | `CommandContext` passed to every command |
| `access.py` | Admin/ban policy |
| `audit.py` | Append-only admin audit log |
| `scoreboard.py` | FIP leaderboard formatting + snapshots |
| `storage.py` | JSON persistence for score/ban data |

## Requirements

- Python 3.10+
- Slack app with:
  - **Bot Token** (`xoxb-...`) — `chat:write` and related scopes
  - **App-Level Token** (`xapp-...`) — `connections:write`
  - **Socket Mode** enabled
  - Event subscriptions: `message.channels`, `message.groups`, `message.im`, `message.mpim`
  - Slash commands registered in the Slack app (see below)

### Slash commands to register

| Command | Description |
|---------|-------------|
| `/help` | List commands |
| `/roll` | Roll dice (`/roll d20`) |
| `/ban` | Ban a user |
| `/unban` | Unban a user |
| `/unbanall` | Clear ban list (admin) |
| `/mypoints` | Show your FIP score |
| `/scoreboard` | Show team leaderboard (admin) |
| `/wtf` | Urban Dictionary lookup |

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

Generate a config template:

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

## Testing & quality

```bash
pytest -v
pytest -v --cov=commands --cov=access --cov=dispatcher --cov=message_parser
mypy access.py bot_state.py context.py dispatcher.py message_parser.py storage.py audit.py scoreboard.py main.py
```

## Docker

```bash
docker build -t slackbot -f container/Dockerfile .
docker run -v /absolute/path/data:/opt/slackbot/data --name=slackbot slackbot
```

## Admin behavior

- Non-admins running admin commands get a **DM**: `<@you>, you are not an admin`
- Banned users get a **DM**: `You are banned. Please contact an admin.`
- Admin actions are logged to `data/audit.jsonl`

## Migration from v1 (RTM)

1. Enable Socket Mode and create an app-level token
2. Add `APP_TOKEN` to config
3. Register slash commands in the Slack app manager
4. Existing pickle `score` / `banned` files migrate to JSON on first run

## Notes

Still a small team bot — not a Slack platform framework. Use responsibly.
