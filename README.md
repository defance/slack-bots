# Collection of slack bots

## Setup

Slack client requires `SLACK_API_TOKEN` environment variable, which is Bot User OAuth access token. 
Consult slack documentation on how to retrieve it.

For scheduling, cron tab is an option. You may create cron file under `/etc/cron.d` owned by `root:root` 
with the following content:

```crontab
MAILTO=user@localhost
BOTS_DIR=/full/path/to/bots/repo
PYTHON=/full/path/to/python/env

SLACK_API_TOKEN=xoxb-YOUR-BOT-KEY

0 12 * * 4 user bash -c "cd $BOTS_DIR && PYTHONPATH=$BOTS_DIR $PYTHON ./slack_bots/color_friday.py"
```

Consider the following changes:
* `MAILTO` cron parameter to report command execution
* `PYTHON` should be set to full path to python environment with packages installed, 
  that are listed in `requirements.txt`
* `SLACK_API_TOKEN` is a bot key
* Command for each bot run should be set for specific user

## Color Friday Bot

При запуске бот выбирает цвет, и сообщает о всем об этом.


## Introducer Bot

При запуске бот выбирает человека и знакомит его со всеми остальными, задавая ему вопросы.
