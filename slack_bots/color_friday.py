from pathlib import Path

from slack_bots.common.choicer import RandomChoicer
from slack_bots.common.client import get_client
from slack_bots.common.files import load_yaml

APP_DIR = Path('color_friday')
DATA_DIR = Path('data') / APP_DIR


def main(client):
    config = load_yaml(DATA_DIR / 'config.yaml')
    choicer = RandomChoicer(APP_DIR / 'colors.txt', non_repeated_len=3)

    client.chat_postMessage(
        channel=config['channel'],
        text=config['message'].format(color=choicer.select()),
    )


if __name__ == '__main__':
    main(get_client())
