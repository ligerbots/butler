# Liger Butler
Slack butler for LigerBots workspace

# Setup

## Python Environment

## Secrets
Slack bot requires an API token. Place the API token in a file called config.json in the config folder. Then run the python script `config-load.py` to load secrets into the environment.

## File Tree
The listener workflow is based off of the [`bolt-python-starter-template`](https://github.com/slack-samples/bolt-python-starter-template) by [`slack-samples`](https://github.com/slack-samples). You specify listener functions in each respective listener type (`actions`, `commands`, etc) file. You then import them into each base `__init__.py` file under the `register` function. This `register` function is what is called to initiate each listener type for the app.

### Hidden Folders/Files
- /
    - config
        - config.json
    - .venv

## Deployment
- Install requirements.txt
- Start your python virtual env
- Load in secret keys with `source config/secrets-load.sh`
- Run `python src.app` to start the slack app
- In another terminal, run `python src.processes.messenger` to start the messenger process. 

## Features
- [] Allow members to auto-do attendance
- [] Allow members to put in their attendance for the upcoming week via emojis
- [] Remind build leads to message their channel on a status update
- [] Have custom send out commands for execs


# Further Resources
- [Slack API Documentation](https://api.slack.com/)
- [Slack Bolt Examples](https://slack.dev/bolt-python/tutorial/getting-started)
- [Slack Bolt Documentation](https://slack.dev/bolt-python/api-docs/slack_bolt/)
- [Liger App](https://api.slack.com/apps/A04E01L56FK)