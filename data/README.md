# Application data directory

Place your runtime config here:

```bash
cp config.example.yaml config.yaml
# Edit BOT_TOKEN, APP_TOKEN, BOTID, BOTUSERID, and ADMINS
```

Runtime files written by the bot:

- `score.json` — fake internet points
- `banned.json` — banned user IDs
- `slackbot.log` — application log

Legacy pickle files (`score`, `banned`) are migrated to JSON on first load.
