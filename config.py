"""Load config from disk or environment variables."""

import logging
import os
import sys

import yaml

ENV_MAP = {
    "SLACK_BOT_TOKEN": "BOT_TOKEN",
    "SLACK_APP_TOKEN": "APP_TOKEN",
    "SLACK_BOT_ID": "BOTID",
    "SLACK_BOT_USER_ID": "BOTUSERID",
    "SLACK_BOT_NAME": "BOTNAME",
}


def _apply_env(config):
    for env_key, config_key in ENV_MAP.items():
        value = os.environ.get(env_key)
        if value:
            config[config_key] = value
    return config


def _normalize_config(config):
    if not config.get("BOT_TOKEN") and config.get("TOKEN"):
        config["BOT_TOKEN"] = config["TOKEN"]
    if not config.get("ADMINS"):
        config["ADMINS"] = []
    return config


def obtain_config(logger):
    config_path = os.environ.get("SLACKBOT_CONFIG", "data/config.yaml")
    try:
        with open(config_path, "r", encoding="utf-8") as handle:
            config = yaml.safe_load(handle) or {}
    except FileNotFoundError:
        from utils.create_config import create_config

        logger.info("Creating fresh config template at %s", config_path)
        create_config(config_path)
        sys.exit(1)
    except yaml.YAMLError as exc:
        logger.error("Config has invalid format: %s", exc)
        sys.exit(1)

    config = _normalize_config(_apply_env(config))
    if not config.get("BOT_TOKEN"):
        logger.error("BOT_TOKEN (or TOKEN) is required")
        sys.exit(1)
    if not config.get("APP_TOKEN"):
        logger.error("APP_TOKEN is required for Socket Mode")
        sys.exit(1)
    return config
