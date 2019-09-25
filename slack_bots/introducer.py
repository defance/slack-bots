"""
Bot introduces person
"""
import asyncio
import logging
import os
import re
from asyncio import create_task, ensure_future, get_event_loop
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import yaml
from slack import RTMClient

from slack_bots.common.choicer import RandomChoicer
from slack_bots.common.client import get_client

DATA_DIR = Path('data', 'introducer')
CACHE_DIR = Path('cache', 'introducer')


logger = logging.getLogger(__name__)


class IntroducerRTMClient(RTMClient):
    """We need this client to keep callbacks isolated,
    so they are actually tied to instance.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._callbacks = defaultdict(list)

    def register(self, event, callback):
        self._validate_callback(callback)
        self._callbacks[event].append(callback)


class IntroducerBot:

    def __init__(self, state=None, config=None):
        self.state = state or {}
        self.config = config or {}

    def handle_message(self, **kwargs):
        # No thread in payload
        thread = kwargs['data'].get('thread_ts')
        if not thread:
            return

        # No thread in state, or they mismatch
        expected_thread = self.state.get('thread')
        if not expected_thread or thread != expected_thread:
            return

        # No user in payload or they mismatch
        user = kwargs['data'].get('user')
        if not user or self.state.get('victim_id') != user:
            return

        # Post reaction
        reactions = RandomChoicer('reactions.txt', base_dir=DATA_DIR, cache_dir=CACHE_DIR)
        kwargs['web_client'].chat_postMessage(
            channel=self.config['channel'],
            text=reactions.select(),
            thread_ts=self.state['thread'],
        )
        self.state['state'] = 'question'
        self.state['last_victim_message'] = datetime.utcnow().timestamp()
        save_file(CACHE_DIR / 'state.yaml', self.state)
        print('Question answered')

    async def timed_questions(self, client):
        now = datetime.utcnow().timestamp()
        last_victim_message = int(self.state.get('last_victim_message', 0))

        if self.state.get('state', 'question') == 'question':
            if now - last_victim_message > int(self.config.get('messages_delay')):

                self.state['state'] = 'answer'
                save_file(CACHE_DIR / 'state.yaml', self.state)
                questions = RandomChoicer('questions.txt', base_dir=DATA_DIR, cache_dir=CACHE_DIR)
                await client.chat_postMessage(
                    channel=self.config['channel'],
                    text=questions.select(),
                    thread_ts=self.state['thread'],
                )
                print('Question asked')

        await asyncio.sleep(5)
        create_task(self.timed_questions(client))


def main(client):
    config = load_file(DATA_DIR / 'config.yaml')

    try:
        state = load_file(CACHE_DIR / 'state.yaml')
    except IOError:
        state = {}

    if 'victim' not in state:
        victims = RandomChoicer('victims.txt', base_dir=DATA_DIR, cache_dir=CACHE_DIR)
        while True:
            victim = victims.select()
            victim_id = re.match('<@(\w*)\|.*>', victim)
            if not victim_id:
                logger.error(f'Bad victim format in registry: {victim}. Reselecting...')
                continue
            state['victim'] = victim
            state['victim_id'] = victim_id.group(1)
            break

    if 'thread' not in state:
        print('Generating thread')
        message = get_event_loop().run_until_complete(client.chat_postMessage(
            channel=config['channel'],
            text=config['messages']['greeting'].format(victim=state["victim"]),
        ))
        state['thread'] = message['ts']

    if 'last_victim_message' not in state:
        state['last_victim_message'] = 0

    save_file(CACHE_DIR / 'state.yaml', state)

    bot_obj = IntroducerBot(state=state, config=config)

    client_2 = IntroducerRTMClient(token=os.environ['SLACK_API_TOKEN'], run_async=True)
    client_2.register('message', bot_obj.handle_message)

    loop = get_event_loop()
    ensure_future(bot_obj.timed_questions(client))
    loop.run_until_complete(client_2.start())


def load_file(filename):
    with open(filename) as f:
        return yaml.safe_load(f)


def save_file(filename, data):
    with open(filename, 'w') as f:
        return yaml.safe_dump(data, f)


if __name__ == '__main__':
    main(get_client(run_async=True))
