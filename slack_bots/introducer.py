"""
Bot introduces person
"""
from datetime import datetime
import random
from pathlib import Path
from string import digits

import yaml

from slack_bots.common.choicer import RandomChoicer
from slack_bots.common.client import get_client

DATA_DIR = Path('data', 'introducer')
CACHE_DIR = Path('cache', 'introducer')


def main(client):
    config = load_file(DATA_DIR / 'config.yaml')
    questions = RandomChoicer('questions.txt', base_dir=DATA_DIR, cache_dir=CACHE_DIR)

    try:
        state = load_file(CACHE_DIR / 'state.yaml')
    except IOError:
        state = {}

    if 'victim' not in state:
        victims = RandomChoicer('victims.txt', base_dir=DATA_DIR, cache_dir=CACHE_DIR)
        victim = victims.select()
        state['victim'] = victim

    if 'thread' not in state:
        print('Generating thread')
        message = client.chat_postMessage(
            channel=config['channel'],
            text=config['messages']['greeting'].format(victim=state["victim"]),
        )
        state['thread'] = message['ts']

    if 'last_victim_message' not in state:
        state['last_victim_message'] = datetime.fromtimestamp(0)

    save_file(CACHE_DIR / 'state.yaml', state)

    client.chat_postMessage(
        channel=config['channel'],
        text=questions.select(),
        thread_ts=state['thread'],
    )


def load_file(filename):
    with open(filename) as f:
        return yaml.safe_load(f)


def save_file(filename, data):
    with open(filename, 'w') as f:
        return yaml.safe_dump(data, f)


if __name__ == '__main__':
    main(get_client())
