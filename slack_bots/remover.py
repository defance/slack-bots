from slack_bots.common.client import get_client


CHANNEL_ID = 'CXXXXXXXX'
MESSAGE_TS = '1000000000.000000'


def main(client):
    client.chat_delete(
        channel=CHANNEL_ID,
        ts=MESSAGE_TS,
    )


if __name__ == '__main__':
    main(get_client())
