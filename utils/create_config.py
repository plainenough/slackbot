"""Create config if one doesn't exist."""

import os

import yaml

DEFAULT_CONFIG = {
    "BOTNAME": "slackbot",
    "BOTID": "B00000000",
    "BOTUSERID": "U00000000",
    "BOT_TOKEN": "xoxb-your-bot-token",
    "APP_TOKEN": "xapp-your-app-level-token",
    "ADMINS": ["U00000000"],
}


def create_config(path="data/config.yaml"):
    """Write a starter config template to disk."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as config_file:
        yaml.safe_dump(DEFAULT_CONFIG, config_file, sort_keys=False)


def main():
    path = os.environ.get("SLACKBOT_CONFIG", "data/config.yaml")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            yaml.safe_load(handle)
        print("Config is valid YAML")
    except FileNotFoundError:
        print("Config doesn't exist: creating template")
        create_config(path)
    except yaml.YAMLError as exc:
        print(exc)
        print("Config invalid; check your config")


if __name__ == "__main__":
    main()
